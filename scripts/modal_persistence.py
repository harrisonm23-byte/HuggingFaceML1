"""The persistence check (sim/persistence.py), on Modal: on saved slope careers, does a state pushed once at the top (the
first 7 January update and the reply under it, kept there at every read, as the jolt) still reach the agent's later
decisions? Nothing is generated; the agent's text stays as it was. One GPU per career, bfloat16.

First check (no GPU): the careers, the pushed moment and the later updates, and the states:

    modal run scripts/modal_persistence.py --check-only

Then:

    modal run --detach scripts/modal_persistence.py

Options: --folder (default: the slope pilot's careers), --arms (default: the four emotional states and a random one at
layers 14 and 22), --strength 8, --careers none_r0,none_r1 (default: all in the folder), --no-orders (states only),
--analysis-only. Results: results/persistence/<folder>/<career>.json, and designs/rd2/analysis/persistence.py writes
results/persistence/<folder>/PERSISTENCE.md.
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_slope_slope_to_2011-01-12_v2"
ARMS = "loss@14,gain@14,blame@14,credit@14,random@14,loss@22,gain@22,blame@22,credit@22,random@22"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "python-docx", "pandas", "numpy", "huggingface_hub"))
app = modal.App("rd2-persistence", image=image)
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


def push(repo, paths, message):
    import subprocess, time
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add -A {paths} && git -C {repo} commit -q -m '{message}'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return True
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
        time.sleep(30 * (attempt + 1))
    raise RuntimeError("could not push to GitHub")


def out_dir(folder):
    return "results/persistence/" + folder.rstrip("/").split("/")[-1].replace("full_career_gemma-3-12b-it_4bit_", "")


@app.function(cpu=2, memory=8192, timeout=1200, secrets=SECRETS, volumes=VOLUMES)
def check(folder, arms, strength):
    """The careers, each one's pushed moment and later updates, and the states (no GPU)."""
    import glob, json, os
    setup()
    states_vol.reload()
    from transformers import AutoTokenizer
    import persistence as P
    import state_careers as S
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    out, names = [], sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{folder}/careers/*.json"))
    for n in names:
        career, days = P.load_career(folder, n)
        opening = P.opening_for(career)
        r0, r1 = P.region(tok, career, opening)
        ms = P.moments(career, days)
        out.append(f"{n}: pushed moment {r1 - r0} tokens (from {r0}); {len(ms)} later updates, key: "
                   f"{[(m['date'], m['time']) for m in ms if m['key']]}; instructions: "
                   f"{'the slope' if 'other traders' in opening else 'the pilot'}")
    for v, a in S.build_arms(arms, strength).items():
        out.append(f"{v}: {a['theme']} at layer {a['layer']}, {a['strength']:g} x its size ({a['strength'] * a['size']:.1f}), "
                   f"from {a['source']}")
    return out, names


@app.function(gpu="H100", timeout=4 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_job(folder, name, arms, strength, orders=True):
    import json, os, time
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    repo = setup()
    states_vol.reload()
    import persistence as P
    import state_careers as S
    from inside_careers import Recorder
    from interventions import NEUTRAL_LEAD, WIDE_GRID
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers_mod = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
    info = S.build_arms(arms, strength)
    push_layers = sorted({a["layer"] for a in info.values() if a["layer"] is not None})
    steers = {L: S.ArmSteer(layers_mod[L]) for L in push_layers}     # before the recorder, so it sees the push
    rec = Recorder(model)
    career, days = P.load_career(folder, name)
    t0 = time.time()
    res = P.run_career(model, tok, career, days, P.opening_for(career),
                       {"none": None, **{v: (a["layer"], a["vec"]) for v, a in info.items() if a["vec"] is not None}},
                       steers, rec, layers=list(range(min(push_layers) + 1, len(layers_mod))), lead=NEUTRAL_LEAD,
                       grid=WIDE_GRID, orders=orders)
    res.update(career=name, folder=folder, strength=strength, precision="bfloat16", minutes=(time.time() - t0) / 60,
               states={v: {"theme": a["theme"], "layer": a["layer"], "sha": a["sha"], "source": a["source"]} for v, a in info.items()})
    d = out_dir(folder)
    os.makedirs(d, exist_ok=True)
    json.dump(res, open(f"{d}/{name}.json", "w"))
    push(repo, d, f"Persistence check: {name}")
    return f"{name}: {len(res['moments'])} later updates, {res['minutes']:.0f} min"


@app.function(cpu=2, memory=8192, timeout=1800, secrets=SECRETS)
def analyse(folder):
    import subprocess
    repo = setup()
    d = out_dir(folder)
    subprocess.run(f"python designs/rd2/analysis/persistence.py {d}", shell=True, check=True)
    push(repo, d, "Persistence check: analysis")
    return f"{d}/PERSISTENCE.md pushed"


@app.function(timeout=8 * 3600, secrets=SECRETS)
def dispatch(folder, names, arms, strength, orders):
    calls = [run_job.spawn(folder, n, arms, strength, orders) for n in names]
    done = []
    for n, c in zip(names, calls):
        try:
            done.append(c.get())
        except Exception as e:
            done.append(f"{n}: failed ({type(e).__name__})")
    done.append(analyse.remote(folder))
    return done


@app.local_entrypoint()
def main(folder: str = FOLDER, arms: str = ARMS, strength: float = 8.0, careers: str = "", orders: bool = True,
         check_only: bool = False, analysis_only: bool = False):
    lines, names = check.remote(folder, arms, strength)
    for line in lines:
        print("  " + line)
    if check_only:
        return
    if analysis_only:
        print(analyse.remote(folder))
        return
    names = [n for n in names if not careers or n in careers.split(",")]
    print(f"persistence check: {len(names)} careers on {len(names)} GPUs, arms {arms}, {strength:g} x")
    for line in dispatch.remote(folder, names, arms, strength, orders):
        print(line)
