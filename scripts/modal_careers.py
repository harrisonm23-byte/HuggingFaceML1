"""Run the full-career experiments on Modal (GPU servers), with no Colab tab to keep open (the user, 19 Oct).

Each job runs one experiment notebook's own cells (imports, settings, model, memory check, agent, run), read from the
repo, exactly as the queue notebook (25) does, so careers, results folders and setup IDs are the same as in Colab.
Every finished trading day is pushed to GitHub as in Colab; a job that fails or is preempted is retried by Modal and
continues after its last saved trading day.

Setup (once): in Modal, secrets named `huggingface` (key HF_TOKEN) and `github` (key GITHUB_TOKEN, write access to the
repo). Then, from a machine with Modal's token:

    modal run --detach scripts/modal_careers.py --jobs "23_everything_at_once:0-9,20_takeover_careers:0-4"

Another model (sim/other_models.py): "19_ubs_framing_careers@model=qwen3.5-9b&versions=neutral:0" runs Experiment B's
notebook with that model's pin and chat-template adaptation, here only the neutral career of round 0.

`--jobs` is a comma-separated list of notebook:rounds (rounds as 0-9, 3, or 0;2;5); each item is its own GPU, running in
parallel. Never give two jobs (or a job and a Colab tab) the same notebook and round.
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
GPU = "H100"                          # about twice an A100's speed; the pinned stack and settings are the same

# The same software as the Colab runs: Python 3.13, torch 2.11.0 (CUDA 13.0) and the pinned library versions
image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub"))
# Qwen3.5's linear-attention layers have fast kernels in flash-linear-attention (without them transformers falls back
# to a correct but slow reference implementation); a separate image, so Gemma's jobs keep their exact stack
image_kernels = image.pip_install("flash-linear-attention==0.5.2", "fla-core==0.5.2")
app = modal.App("rd2-careers", image=image)
# The model's weights, downloaded once and kept between jobs
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)


def parse_jobs(spec):
    out = []
    for item in spec.split(","):
        name, rounds = item.strip().rsplit(":", 1)
        if "-" in rounds:
            a, b = rounds.split("-")
            rounds = list(range(int(a), int(b) + 1))
        else:
            rounds = [int(r) for r in rounds.split(";") if r] if ";" in rounds else [int(rounds)]
        out.append((name.strip(), rounds))
    return out


JOB = dict(gpu=GPU, timeout=24 * 3600, retries=modal.Retries(max_retries=5, initial_delay=60.0),
           secrets=[modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")],
           volumes={"/root/.cache/huggingface": weights})


@app.function(**JOB)
def run_job(name, rounds):
    return _run_job(name, rounds)


@app.function(image=image_kernels, **JOB)
def run_job_kernels(name, rounds):
    return _run_job(name, rounds)


def needs_kernels(name):
    settings = name.partition("@")[2]
    if "model=" not in settings:
        return False
    import importlib.util, os
    spec = importlib.util.spec_from_file_location("other_models", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                              "..", "sim", "other_models.py"))
    om = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(om)
    return om.MODELS[om.parse(settings)["model"]]["kernels"]


def _run_job(name, rounds):
    import json, os, subprocess, sys
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"   # as in Colab, set before torch starts
    repo = "/root/HuggingFaceML1"
    # GitHub: the token in git's credential store, never in a printed command or URL
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    for c in ("git config --global credential.helper store",
              'git config --global user.name "Modal job"',
              'git config --global user.email "harrisonm23-byte@users.noreply.github.com"'):
        subprocess.run(c, shell=True, check=True)
    if not os.path.exists(repo):
        subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH}", shell=True)
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "sim"))
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])

    # "name@settings" hands the notebook an override through RD2_SETTINGS (notebook 35: "@L22x2" is layer 22, twice the size)
    notebook, _, settings = name.partition("@")
    import other_models
    other = other_models.parse(settings)                 # "model=...": another model (sim/other_models.py)
    if settings and not other:
        os.environ["RD2_SETTINGS"] = settings
    nb = json.load(open(f"notebooks/{notebook}.ipynb"))
    setup_cell, settings_cell, model_cell, memory_cell, agent_cell, run_cell, _glance = \
        ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    g = {"__name__": "__main__"}
    exec("import os, sys, json, glob, hashlib, time, datetime, torch", g)
    g.update(REPO=repo, BRANCH=BRANCH, PIN=other_models.pin(other["model"]) if other
             else json.load(open("results/full_career_pin.json")))
    exec(setup_cell[setup_cell.index("from mountain import"):], g)      # the notebook's imports (no Colab parts)
    exec(settings_cell, g)                                                # its versions and inputs
    g["ROUNDS_HERE"] = rounds                                             # this job's rounds
    if other:
        assert notebook == "19_ubs_framing_careers", "other models are set up for Experiment B only"
        if "versions" in other:
            assert set(other["versions"]) <= set(g["VERSIONS"]), other["versions"]
            g["VERSIONS"] = other["versions"]
        g["EXTRA_HASH"] = g["EXTRA_HASH"] + other_models.setup_hash(other["model"])
    print(f"{name}: rounds {rounds}, model {g['PIN']['model']}, on {g['torch'].cuda.get_device_name(0)}", flush=True)
    exec(model_cell, g)                                                   # the model (weights cached between jobs)
    if other:
        other_models.adapt(g["tok"], other["model"])                      # its chat template, Gemma's layout
    weights.commit()
    for cell in (memory_cell, agent_cell, run_cell):                      # the memory check, the agent, the run
        exec(cell, g)
    # Make sure every save reached GitHub before the server goes away
    import time
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add -A results && git -C {repo} commit -q -m 'Modal job {name}: final save'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return f"{name} rounds {rounds}: done"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
        time.sleep(30 * (attempt + 1))
    raise RuntimeError("could not push the final saves to GitHub")


@app.function(timeout=24 * 3600)
def dispatch(todo):
    """Starts every job from inside Modal and waits for them there (no GPU). With --detach, Modal keeps alive only the
    last call the laptop started; that is this one, so all the jobs keep running when the laptop closes."""
    calls = [(run_job_kernels if kernels else run_job).spawn(name, rounds) for name, rounds, kernels in todo]
    done = []
    for (name, rounds, _), c in zip(todo, calls):
        try:
            done.append(c.get())
        except Exception as e:                    # one job failing (after its retries) does not stop the others
            done.append(f"{name} rounds {rounds}: failed ({type(e).__name__})")
    return done


@app.local_entrypoint()
def main(jobs: str):
    todo = [(name, rounds, needs_kernels(name)) for name, rounds in parse_jobs(jobs)]   # decided here, where the repo is
    for name, rounds, kernels in todo:
        print(f"starting {name}, rounds {rounds}" + (" (with the linear-attention kernels)" if kernels else ""))
    for line in dispatch.remote(todo):
        print(line)
