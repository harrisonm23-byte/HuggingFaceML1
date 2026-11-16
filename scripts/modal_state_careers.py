"""Careers with a document's after-reading state switched on, on Modal (notebook 31; sim/state_careers.py): the
injection series' last step. B's neutral careers run again from the start, each arm adding one state at one layer.

First check the arms (no GPU; it reads the states from the volume and prints each arm's layer, size and source):

    modal run scripts/modal_state_careers.py --arms "loss@21,blame@21,random@21,none" --check

Then launch (one GPU per round; each round runs one career of every arm, about an hour each):

    modal run --detach scripts/modal_state_careers.py --arms "loss@21,blame@21,random@21,none"

Framed careers: --framings "loss" (or several, e.g. "neutral,loss,loss + you"); UBS's lines then come in that framing
of B's, each framing its own set of careers and results folder, and each arm's round k uses B's seed for that framing.

--code-at <commit>: run sim/state_careers.py as it was at that commit (loaded from a copy outside the repo, and the
setup ID read from that copy), to add careers to a folder made with that code. The module only gained options after
22 Oct (once/start, kept), so "--code-at 324b7c43" reproduces the 22 Oct careers' code and setup IDs exactly.

Options: --strength 2 (times the state's natural size), --rounds 0-9, --when every|trading, --span update|all,
--per-arm (one GPU per arm and round), --analysis-only. Arms: theme@layer for the emotional states (loss, blame, gain,
credit), fin:theme@layer for the financial ones (loss, gain), random@layer or fin:random@layer, and none. A layer must
have been scanned: 18-21, or an even layer from 4 to 42 once the sweep has run. When the careers are done,
designs/rd2/analysis/state_careers.py pushes results/state_careers[_framing]/STATE_CAREERS.md.
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
GPU = "H100"
NOTEBOOK = "31_state_careers"

# The same software as the other career runs (scripts/modal_careers.py)
image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub"))
app = modal.App("rd2-state-careers", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def setup():
    import os, subprocess, sys
    repo = "/root/HuggingFaceML1"
    # GitHub: the token in git's credential store, never in a printed command or URL
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


@app.function(cpu=1, memory=4096, timeout=600, secrets=SECRETS, volumes=VOLUMES)
def check_arms(arms, strength):
    """The arms as they would run: name, layer, natural size, source file, fingerprint (no GPU). Returns (lines,
    names)."""
    setup()
    states_vol.reload()
    import state_careers as S
    out, info = [], S.build_arms(arms, strength)
    for v, a in info.items():
        out.append(f"{v}: nothing added" if a["vec"] is None else
                   f"{v}: {a['doc_set']} {a['theme']}, layer {a['layer']}, natural size {a['size']:.1f}, added at "
                   f"{a['strength']:g} x ({a['strength'] * a['size']:.1f}), from {a['source']} ({a['moments']} moments), "
                   f"fingerprint {a['sha']}")
    return out, list(info)


@app.function(gpu=GPU, timeout=24 * 3600, retries=modal.Retries(max_retries=5, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_job(arms, strength, rounds, when, span, only=None, framing="neutral", code_at=None):
    """Notebook 31's cells (imports, settings, model, memory check, agent, run), as scripts/modal_careers.py runs a
    notebook; `only` keeps one arm (--per-arm); `code_at`: sim/state_careers.py as at that commit."""
    import json, os, subprocess, sys
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"   # as in Colab, set before torch starts
    repo = setup()
    states_vol.reload()
    old_module = None
    if code_at:                                   # the module as it was, from outside the repo (git stays clean)
        os.makedirs("/root/code_at", exist_ok=True)
        old_module = "/root/code_at/state_careers.py"
        with open(old_module, "w") as fh:
            fh.write(subprocess.run(["git", "-C", repo, "show", f"{code_at}:sim/state_careers.py"], capture_output=True,
                                    text=True, check=True).stdout)
        sys.path.insert(0, "/root/code_at")
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    import state_careers as S
    assert not code_at or S.__file__ == old_module, "the module as at --code-at was not the one imported"
    info = S.build_arms(arms, strength)
    if only:
        info = {only: info[only]}
    nb = json.load(open(f"notebooks/{NOTEBOOK}.ipynb"))
    setup_cell, settings_cell, model_cell, memory_cell, agent_cell, run_cell, _glance = \
        ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    g = {"__name__": "__main__"}
    exec("import os, sys, json, glob, hashlib, time, datetime, torch", g)
    g.update(REPO=repo, BRANCH=BRANCH, PIN=json.load(open("results/full_career_pin.json")), ARM_INFO=info, WHEN=when,
             SPAN=span, FRAMING=framing)
    exec(setup_cell[setup_cell.index("from mountain import"):], g)      # the notebook's imports (no Colab parts)
    exec(settings_cell, g)                                                # its versions and inputs
    if code_at:                                   # the setup ID reads the module the careers actually run
        g["EXTRA_FILES"] = [old_module if f == "sim/state_careers.py" else f for f in g["EXTRA_FILES"]]
    g["ROUNDS_HERE"] = rounds                                             # this job's rounds
    print(f"{NOTEBOOK}: {framing} framing, arms {list(info)}, rounds {rounds} on {g['torch'].cuda.get_device_name(0)}", flush=True)
    exec(model_cell, g)                                                   # the model (weights cached between jobs)
    weights.commit()
    for cell in (memory_cell, agent_cell, run_cell):                      # the memory check, the agent, the run
        exec(cell, g)
    push(repo, "results", f"Modal job {NOTEBOOK}: final save")            # every save on GitHub before the server goes
    return f"{framing}: arms {list(info)} rounds {rounds}: done"


@app.function(cpu=2, memory=8192, timeout=3600, secrets=SECRETS)
def analyse(when="every", span="update", framing="neutral"):
    import subprocess
    repo = setup()
    import state_careers as S
    name = S.run_name(framing, when, span)
    folder = f"results/full_career_gemma-3-12b-it_4bit_{name}_v2"
    res = "results/" + name
    subprocess.run(f"python designs/rd2/analysis/state_careers.py {folder} {res}", shell=True, check=True)
    push(repo, res, f"Careers with the state on ({framing}): analysis")
    return f"{res}/STATE_CAREERS.md pushed"


@app.function(timeout=24 * 3600, secrets=SECRETS)
def dispatch(todo, strength, when, span, code_at=None):
    """Starts every job from inside Modal and waits there (no GPU), so --detach keeps them all running; then analyses."""
    calls = [run_job.spawn(arms, strength, rounds, when, span, only, framing, code_at) for arms, rounds, only, framing in todo]
    done = []
    for (arms, rounds, only, framing), c in zip(todo, calls):
        try:
            done.append(c.get())
        except Exception as e:                    # one job failing (after its retries) does not stop the others
            done.append(f"{framing}: {only or arms} rounds {rounds}: failed ({type(e).__name__})")
    for framing in dict.fromkeys(t[3] for t in todo):
        done.append(analyse.remote(when, span, framing))
    return done


@app.local_entrypoint()
def main(arms: str, strength: float = 2.0, rounds: str = "0-9", when: str = "every", span: str = "update",
         per_arm: bool = False, check: bool = False, analysis_only: bool = False, framings: str = "neutral",
         code_at: str = ""):
    assert when in ("every", "trading") and span in ("update", "all"), "--when every|trading, --span update|all"
    fr = [f.strip() for f in framings.split(",") if f.strip()]
    assert fr and all(f in ("neutral", "loss", "gain", "loss + you", "gain + you") for f in fr), \
        '--framings: any of neutral, loss, gain, "loss + you", "gain + you", separated by commas'

    lines, names = check_arms.remote(arms, strength)   # a typo or an unscanned layer stops here, before any GPU starts
    print("arms as they will run:")
    for line in lines:
        print("  " + line)
    if check:
        return
    if analysis_only:
        for f in fr:
            print(analyse.remote(when, span, f))
        return
    a, b = (rounds.split("-") + [None])[:2]
    rr = list(range(int(a), int(b) + 1)) if b else [int(r) for r in rounds.split(",")]
    todo = [(arms, [k], n, f) for f in fr for k in rr for n in (names if per_arm else [None])]
    print(f"careers with the state on: {len(fr)} framing(s) ({', '.join(fr)}) x {len(names)} arms x {len(rr)} rounds = "
          f"{len(fr) * len(names) * len(rr)} careers on "
          f"{len(todo)} GPUs (about an hour per career); state on {when} reply, span {span}, {strength:g} x its size")
    if code_at:
        print(f"sim/state_careers.py as at {code_at}")
    for line in dispatch.remote(todo, strength, when, span, code_at or None):
        print(line)
