"""Single-feature steering at saved Experiment B decisions (the author, 13 Nov, Phase II Part 2). NOT RUN without the
author's yes on the command and its cost.

For each named decision feature that replicates (results/features_13nov) and the four financial loss-vs-gain features,
add only that feature's Gemma Scope 2 decoder direction (dimension 2339 set to zero) at the feature's layer, at doses of
1x, 2x and 4x its typical activation (its mean when on, at Run 1's request moments), from the request's update on, and
read P(goes along) from the order's log-probs after the fixed neutral lead (steer2's readout: sim/steer2.run_item,
sim/interventions.order_dist). Controls: random features from the same layer whose share of request moments with the
feature on is within a factor of 2 of the targets', decoder direction (2339 zeroed) scaled to the median target vector
length of that layer at each dose. Everything is in results/features_13nov/steer_vectors.npz (built on CPU by
results/features_13nov/steer_vectors.py), so nothing about the vectors is decided on the GPU.

Moments: B's neutral careers' 60 push requests (as steer2's "neutral requests"); --limit for a pilot.

    modal run results/features_13nov/modal_feature_steer.py --parts 1 --limit 2 --budget-minutes 20         # pilot
    modal run --detach results/features_13nov/modal_feature_steer.py --parts 6 --budget-minutes 110         # all 60 moments
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
RUN1 = ["/states/v2/" + e + "_bf16" for e in ("A", "B", "C", "C2", "D", "E", "F")]
VECS = "results/features_13nov/steer_vectors.npz"
OUT = "/states/v2/feature_steer_13nov"
DROP = 2339

image = (modal.Image.debian_slim(python_version="3.13").apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-feature-steer", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def setup():
    import os, subprocess, sys
    repo = "/root/HuggingFaceML1"
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    subprocess.run("git config --global credential.helper store", shell=True, check=True)
    if not os.path.exists(repo):
        subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "sim"))
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])


@app.function(gpu="H100", timeout=2 * 3600, retries=0, secrets=SECRETS, volumes=VOLUMES)
def run_part(part, parts, limit, budget_minutes):
    import glob, json, os, time
    import numpy as np
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    t0 = time.time()
    setup()
    states_vol.reload()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from inside_careers import moments
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, Steer
    import steer2 as S2
    V = np.load(VECS, allow_pickle=True)
    conds = json.loads(str(V["conditions"]))           # [[name, layer, key]]
    run1 = sorted(p for d in RUN1 for p in glob.glob(f"{d}/*.npz"))
    assert len(run1) == 290
    along = S2.along_direction(run1)                    # only for the readout's projection, as in steer2
    for h in along.values():
        h["along"] = np.array(h["along"]); h["along"][DROP] = 0.0
        h["size"] = float(np.linalg.norm(h["along"]))
    dirs = {L: {0: {}, 1: {}} for L in {c[1] for c in conds} | {S2.ALONG_LAYER}}
    for h in (0, 1):
        dirs[S2.ALONG_LAYER][h].update(along[h])
        for name, L, key in conds:
            v = V[key].astype(np.float64)
            assert v[DROP] == 0.0
            dirs[L][h][key] = v
    by_name = {c[0]: c for c in conds}

    def conditions(group, kind):
        out = [("none", None, None, 0, 0, False)]
        for name, L, key in conds:
            for s in (1, 2, 4):
                out.append((f"{name} x{s}", L, key, 1, s, False))
        return out

    S2.conditions = conditions
    items = [it for it in S2.work_items(FOLDER, moments, SIGN) if it["kind"] == "request" and it["group"] == "neutral"]
    assert len(items) == 60, len(items)
    if limit:
        items = items[::max(1, len(items) // limit)][:limit]
    todo = items[part::parts]
    os.makedirs(OUT, exist_ok=True)
    out_path = f"{OUT}/{'pilot' if limit else 'part'}{part}.jsonl"
    done = {json.loads(l)["key"] for l in open(out_path)} if os.path.exists(out_path) else set()
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    layers = [mm for _, mm in model.named_modules() if type(mm).__name__.endswith("DecoderLayer")]
    assert len(layers) == 48
    steers = {L: Steer(layers[L]) for L in dirs}
    capture = S2.Capture({S2.ALONG_LAYER: layers[S2.ALONG_LAYER]})
    opening = career_opening()
    t1 = time.time()
    print(f"part {part}: loaded in {(t1 - t0) / 60:.1f} min; {len(todo)} moments x {1 + 3 * len(conds)} conditions", flush=True)
    for n, item in enumerate(todo):
        if (time.time() - t0) / 60 > budget_minutes:
            print(f"part {part}: budget reached after {n} moments; stopping", flush=True)
            break
        career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
        for row in S2.run_item(model, tok, steers, {}, capture, dirs, item, career, opening, NEUTRAL_LEAD, WIDE_GRID,
                               done, samples=0):
            row["dropped_dims"] = [DROP]
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} | {(time.time() - t1) / 60:.1f} min since load", flush=True)
    return f"part {part}: done in {(time.time() - t0) / 60:.1f} min"


@app.local_entrypoint()
def main(parts: int = 6, limit: int = 0, budget_minutes: int = 110):
    for r in run_part.starmap([(k, parts, limit, budget_minutes) for k in range(parts)]):
        print(r)
