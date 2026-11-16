"""The screenplay history and the injected end state on Modal (`sim/screenplay.py`). F's framed careers at every
request after the first: the user's scripted replies in place of the agent's chat replies (UBS's request in each of its
five framings), the real history, and the screenplay's state at the request injected into the real one (layers 12, 18,
24; random at 18). Then `designs/rd2/analysis/screenplay.py` pushes results/screenplay/SCREENPLAY.md.

    modal run --detach scripts/modal_screenplay.py                  # 2 GPUs, then the analysis
    modal run --detach scripts/modal_screenplay.py --analysis-only
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
OUT = "/states/v2/screenplay"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-screenplay", image=image)
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
    import json, os, time
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    states_vol.reload()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from framing_set import read_set
    from inside_careers import moments
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, Steer
    import ideal as I, screenplay as P
    chats = read_set()                                  # the author's frozen framing file (fingerprint checked)
    scripted = P.read_replies()                         # the user's scripted replies (fingerprint checked)
    todo = I.work_items(moments, SIGN)[part::parts]
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
    steers = {L: Steer(layers[L]) for L in P.INJECT_LAYERS}
    mean_capture = P.MeanCapture({L: layers[L] for L in P.INJECT_LAYERS})
    opening = career_opening()
    t0 = time.time()
    for n, item in enumerate(todo):
        career = json.load(open(f"{item['folder']}/careers/{item['career_file']}"))
        for row in P.run_item(model, tok, steers, mean_capture, career, item, scripted[item["version"]], chats,
                              opening, NEUTRAL_LEAD, WIDE_GRID, done):
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
    subprocess.run(f"python designs/rd2/analysis/screenplay.py {OUT} results/screenplay", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/screenplay && git -C {repo} commit -q -m 'The screenplay history and the injected end state'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "screenplay results pushed"
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
def main(parts: int = 2, analysis_only: bool = False):
    print(f"the screenplay history: {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only):
        print(line)
