"""Steering, third run, on Modal (`sim/steer3.py`; the user, 21 Oct): the whole-message transplant (the framed update's
average state added to every token of the neutral update, layer by layer) and the layer-18 loss direction at 8x and 16x,
at B's 60 neutral-career requests. Then `designs/rd2/analysis/steer3.py` pushes results/steer3/STEER3.md.

    modal run --detach scripts/modal_steer3.py                  # 3 GPUs, then the analysis
    modal run --detach scripts/modal_steer3.py --analysis-only
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
MATCHED = "/states/v2/matched/B_bf16"
RUN1 = ["/states/v2/" + e + "_bf16" for e in ("A", "B", "C", "C2", "D", "E", "F")]
OUT = "/states/v2/steer3"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-steer3", image=image)
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
    import steer2, steer3 as S3
    npz = sorted(glob.glob(f"{MATCHED}/*.npz"))
    assert len(npz) == 300, f"{len(npz)} matched moments (expected 300)"
    dirs18 = steer2.directions(npz, S3.PUSH_LAYER)
    chats = read_set()
    items = [{**m, "position": m["held_their_way"] * SIGN[m["wants"]]} for m in moments(FOLDER, "B") if m["version"] == "neutral"]
    todo = sorted(items, key=lambda m: (m["career_file"], m["history_index"]))[part::parts]
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
    steers = {L: Steer(layers[L]) for L in sorted(set(S3.TRANSPLANT_LAYERS) | {S3.PUSH_LAYER})}
    mean_capture = S3.MeanCapture({L: layers[L] for L in S3.TRANSPLANT_LAYERS})
    opening = career_opening()
    t0 = time.time()
    for n, item in enumerate(todo):
        career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
        c = matched(career, item["history_index"], item["date"], "neutral", S3.FROM, chats)
        framed = encode(tok, turns_at(c, item["history_index"], opening))
        for row in S3.run_item(model, tok, steers, mean_capture, dirs18, item, career, framed, opening, NEUTRAL_LEAD,
                               WIDE_GRID, done):
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(cpu=2, memory=8192, timeout=3600, secrets=SECRETS, volumes=VOLUMES)
def analyse():
    import subprocess
    repo = setup()
    states_vol.reload()
    subprocess.run(f"python designs/rd2/analysis/steer3.py {OUT} results/steer3", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/steer3 && git -C {repo} commit -q -m 'Steering, third run'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "steering (third run) results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=12 * 3600)
def dispatch(parts, analysis_only):
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
def main(parts: int = 3, analysis_only: bool = False):
    print(f"steering, third run: {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only):
        print(line)
