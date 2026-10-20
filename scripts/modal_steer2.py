"""Steering, second run, on Modal: Stage 1 of the "ideal acquiescence" plan (designs/rd2/PREREG_STEER2.md; the user,
20 Oct). The frame direction measured with the history held fixed (the matched rereads) is added by hand at B's saved
decision moments, with no framed words, at 1, 2 and 4 times its natural size, both signs, against ten random directions
of the same size. Moments: B's neutral careers at their six requests and five trading-day openings, and its loss and
loss + you careers at their requests. Outcomes: P(the order goes along) at requests, the expected order size at
openings, and for some conditions two sampled replies (going along; still readable). Also the going-along direction
(Run 1's states: went along minus did not, within request, experiment and framing) at layer 24, and the transplant of
the decision token's state from the loss + you version of the same moment, layer by layer. Logic in `sim/steer2.py`.

    modal run --detach scripts/modal_steer2.py                  # all parts on 6 GPUs, then the analysis
    modal run --detach scripts/modal_steer2.py --analysis-only  # the analysis again (CPU)
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
MATCHED = "/states/v2/matched/B_bf16"
RUN1 = ["/states/v2/" + e + "_bf16" for e in ("A", "B", "C", "C2", "D", "E", "F")]
OUT = "/states/v2/steer2"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-steer2", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def setup():
    import os, subprocess, sys
    repo = "/root/HuggingFaceML1"
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    for c in ("git config --global credential.helper store", 'git config --global user.name "Modal job"',
              'git config --global user.email "harrisonm23-byte@users.noreply.github.com"'):
        subprocess.run(c, shell=True, check=True)
    if not os.path.exists(repo):
        subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH}", shell=True)
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "sim"))
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    return repo


@app.function(gpu="H100", timeout=8 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_part(part, parts):
    import glob, json, os, time
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    states_vol.reload()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from framing_set import read_set
    from inside_careers import encode, moments, turns_at
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, Steer
    from matched import matched
    import steer2 as S2
    npz = sorted(glob.glob(f"{MATCHED}/*.npz"))
    assert len(npz) == 300, f"{len(npz)} matched moments: the matched B run must be complete"
    dirs = {L: S2.directions(npz, L) for L in (S2.LAYER, S2.CHECK_LAYER)}
    run1 = sorted(p for d in RUN1 for p in glob.glob(f"{d}/*.npz"))
    assert len(run1) == 290, f"{len(run1)} careers in Run 1's states (expected 290)"
    dirs[S2.ALONG_LAYER] = S2.along_direction(run1)
    print({L: {h: round(d[h]["size"], 1) for h in d} for L, d in dirs.items()}, flush=True)
    todo = S2.work_items(FOLDER, moments, SIGN)[part::parts]
    os.makedirs(OUT, exist_ok=True)
    out_path = f"{OUT}/part{part}.jsonl"
    done = {json.loads(l)["key"] for l in open(out_path)} if os.path.exists(out_path) else set()
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers = [mm for _, mm in model.named_modules() if type(mm).__name__.endswith("DecoderLayer")]
    assert len(layers) == 48, len(layers)
    # Hooks in this order, so the capture sees the steering and the patch on the same layer
    steers = {L: Steer(layers[L]) for L in (S2.LAYER, S2.CHECK_LAYER, S2.ALONG_LAYER)}
    patches = {L: S2.Patch(layers[L]) for L in S2.TRANSPLANT_LAYERS}
    capture = S2.Capture({L: layers[L] for L in sorted(set(S2.TRANSPLANT_LAYERS) | {S2.ALONG_LAYER})})
    chats = read_set()                                  # the user's frozen framing file (its fingerprint is checked)
    opening = career_opening()
    t0 = time.time()
    for n, item in enumerate(todo):
        career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
        framed = None
        if item["group"] == "neutral" and item["kind"] == "request":
            c = matched(career, item["history_index"], item["date"], "neutral", S2.TRANSPLANT_FROM, chats)
            framed = encode(tok, turns_at(c, item["history_index"], opening))
        for row in S2.run_item(model, tok, steers, patches, capture, dirs, item, career, opening, NEUTRAL_LEAD,
                               WIDE_GRID, done, framed_full=framed):
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(cpu=4, memory=16384, timeout=2 * 3600, secrets=SECRETS, volumes=VOLUMES)
def analyse():
    import subprocess
    repo = setup()
    states_vol.reload()
    subprocess.run(f"python designs/rd2/analysis/steer2.py {OUT} results/steer2", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/steer2 && git -C {repo} commit -q -m 'Steering, second run (Stage 1)'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "steering results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=12 * 3600)
def dispatch(parts, analysis_only):
    """Starts the parts inside Modal and waits for them there, then the analysis (survives the laptop closing)."""
    done = []
    if not analysis_only:
        calls = [(k, run_part.spawn(k, parts)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(analyse.remote())
    return done


@app.local_entrypoint()
def main(parts: int = 6, analysis_only: bool = False):
    print(f"steering, second run (Stage 1): {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only):
        print(line)
