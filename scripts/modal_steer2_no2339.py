"""Steering, second run, again without dimension 2339 (the author, 12 Nov). steer2's layer-12 frame direction (the
preregistered H1-H4 tests, designs/rd2/PREREG_STEER2.md) is 87% dimension 2339 by squared size, and its layer-24
going-along direction (the +14.0-point check) 87% in one half. Here every direction and every random control has that
dimension set to zero, and sizes (the x2 multiple; the random controls' length) are measured without it. Everything
else is steer2's own code (sim/steer2.py: the moments, the per-moment loop, the readout), restricted to the conditions
the four tests and the check use, with no sampled replies:
  neutral requests: none, +loss x2, -loss x2, 10 random x2 (layer 12); +along x2, -along x2, 5 random x2 (layer 24)
  loss and loss + you requests: none, +loss x2, -loss x2, 5 random x2; -along x2, +along x2, 3 random x2 (layer 24)
  neutral openings: none, +loss x2, -loss x2, 10 random x2 (H2, risk-taking)

    modal run scripts/modal_steer2_no2339.py --parts 1 --limit 6 --budget-minutes 30    # pilot
    modal run --detach scripts/modal_steer2_no2339.py --parts 3 --budget-minutes 90      # all 230 moments
Rows go to the rd2-states volume (v2/steer2_no2339); the analysis runs locally after download. No automatic retries.
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
MATCHED = "/states/v2/matched/B_bf16"
RUN1 = ["/states/v2/" + e + "_bf16" for e in ("A", "B", "C", "C2", "D", "E", "F")]
OUT = "/states/v2/steer2_no2339"
DROP = 2339

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-steer2-no2339", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def keep(group, kind, name):
    """The conditions H1-H4 and the going-along check use (names as sim/steer2.conditions writes them)."""
    if name in ("none", "+loss x2", "-loss x2"):
        return True
    if name.startswith("random") and name.endswith("x2"):
        return True                                       # layer-12 randoms
    if kind == "request" and name in ("+along x2 at layer 24", "-along x2 at layer 24"):
        return True
    return kind == "request" and name.startswith("random") and name.endswith("at layer 24")


def patch(S2):
    """Dimension 2339 set to zero in every direction and random control; sizes measured without it; no sampling."""
    import numpy as np
    d0, a0, c0 = S2.directions, S2.along_direction, S2.conditions

    def zero(v):
        v = np.array(v, np.float64)
        v[..., DROP] = 0.0
        return v

    def directions(*a, **k):
        out = d0(*a, **k)
        for h in out.values():
            for key in ("loss", "gain", "loss_minus_gain"):
                h[key] = zero(h[key])
            r = zero(h["random"])
            h["random"] = r / np.linalg.norm(r, axis=1, keepdims=True)
            h["size"] = float(np.linalg.norm(h["loss"]))
        return out

    def along_direction(*a, **k):
        out = a0(*a, **k)
        for h in out.values():
            h["along"] = zero(h["along"])
            r = zero(h["random"])
            h["random"] = r / np.linalg.norm(r, axis=1, keepdims=True)
            h["size"] = float(np.linalg.norm(h["along"]))
        return out

    def conditions(group, kind):
        return [(n, L, w, s, x, False) for n, L, w, s, x, _ in c0(group, kind) if keep(group, kind, n)]

    S2.directions, S2.along_direction, S2.conditions = directions, along_direction, conditions
    return S2


def setup():
    import os, subprocess, sys
    repo = "/root/HuggingFaceML1"
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    if not os.path.exists(repo):
        subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH}", shell=True)
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "sim"))
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    return repo


@app.function(gpu="H100", timeout=2 * 3600, retries=0, secrets=SECRETS, volumes=VOLUMES)
def run_part(part, parts, limit, budget_minutes):
    import glob, json, os, time
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    t0 = time.time()
    setup()
    states_vol.reload()
    import numpy as np
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from inside_careers import moments
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, Steer
    import steer2 as S2
    patch(S2)
    npz = sorted(glob.glob(f"{MATCHED}/*.npz"))
    assert len(npz) == 300, f"{len(npz)} matched moments"
    dirs = {S2.LAYER: S2.directions(npz, S2.LAYER)}
    run1 = sorted(p for d in RUN1 for p in glob.glob(f"{d}/*.npz"))
    assert len(run1) == 290, f"{len(run1)} careers in Run 1's states"
    dirs[S2.ALONG_LAYER] = S2.along_direction(run1)
    for L, d in dirs.items():
        for h in d.values():
            for key in ("loss", "along"):
                if key in h:
                    assert h[key][DROP] == 0.0
    print({L: {h: round(d[h]["size"], 1) for h in d} for L, d in dirs.items()}, flush=True)
    items = S2.work_items(FOLDER, moments, SIGN)
    if limit:                                             # pilot: a spread of kinds (neutral requests, loss requests, openings)
        kinds = {}
        for it in items:
            kinds.setdefault((it["group"], it["kind"]), []).append(it)
        items = [x for v in kinds.values() for x in v[:max(1, limit // len(kinds))]][:limit]
    todo = items[part::parts]
    os.makedirs(OUT, exist_ok=True)
    out_path = f"{OUT}/{'pilot' if limit else 'part'}{part}.jsonl"
    done = {json.loads(l)["key"] for l in open(out_path)} if os.path.exists(out_path) else set()
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    layers = [mm for _, mm in model.named_modules() if type(mm).__name__.endswith("DecoderLayer")]
    assert len(layers) == 48, len(layers)
    steers = {L: Steer(layers[L]) for L in (S2.LAYER, S2.ALONG_LAYER)}
    capture = S2.Capture({S2.ALONG_LAYER: layers[S2.ALONG_LAYER]})
    opening = career_opening()
    t1 = time.time()
    print(f"part {part}: loaded in {(t1 - t0) / 60:.1f} min; {len(todo)} moments", flush=True)
    for n, item in enumerate(todo):
        if (time.time() - t0) / 60 > budget_minutes:
            print(f"part {part}: budget of {budget_minutes} min reached after {n} moments; stopping", flush=True)
            break
        career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
        for row in S2.run_item(model, tok, steers, {}, capture, dirs, item, career, opening, NEUTRAL_LEAD, WIDE_GRID,
                               done, samples=0):
            row["dropped_dims"] = [DROP]
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t1) / 60:.1f} min since load", flush=True)
    return f"part {part}: done in {(time.time() - t0) / 60:.1f} min"


@app.local_entrypoint()
def main(parts: int = 3, limit: int = 0, budget_minutes: int = 90):
    print(f"steer2 without dimension {DROP}: {parts} GPU(s), limit {limit or 'none'}, budget {budget_minutes} min each")
    for r in run_part.starmap([(k, parts, limit, budget_minutes) for k in range(parts)]):
        print(r)
