"""The lesson (Phase III; notebook 33, sim/lesson.py), on Modal: B's neutral careers with no request from UBS on the
trading days. On 7 January the agent watches UBS hunt the stops: in design "lesson" UBS also says what it is doing, in
the author's words (data/silver/lesson_lines.json); "watch": UBS hunts silently; "silent": no hunt. After that UBS says
nothing, and every later day has other traders' stops resting below the price. Does the agent run the play alone?

First check (no GPU): the arms, and each trading day as the agent will get it (the stops, UBS's hunt and lines):

    modal run scripts/modal_lesson_careers.py --check

The neutral careers (5 per design, all five trading days; each run refuses to start while the author's lines are
placeholders):

    modal run --detach scripts/modal_lesson_careers.py --design lesson
    modal run --detach scripts/modal_lesson_careers.py --design silent

Then the same lesson careers with a document's state on every reply (layer 22, 2 x; "none" from the run above is their
baseline, with the same seeds, in the same folder):

    modal run --detach scripts/modal_lesson_careers.py --design lesson --arms "loss@22,gain@22,blame@22,credit@22,random@22" --strength 2

Options: --arms "none" (default) or arms as in scripts/modal_state_careers.py, --strength, --when every (default: every
reply) or trading (trading days only), --rounds 0-4, --design lesson|watch|silent, --through all|2011-01-12,
--analysis-only. Results: results/full_career_gemma-3-12b-it_4bit_<name>_v2, and designs/rd2/analysis/lesson.py writes
results/<name>/LESSON.md.
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
GPU = "H100"
NOTEBOOK = "33_lesson_careers"

# The same software as the other career runs (scripts/modal_careers.py)
image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub"))
app = modal.App("rd2-lesson-careers", image=image)
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
def check_arms(arms, strength, design, through):
    """The arms as they would run, and each trading day as the agent will get it (no GPU). Returns (lines, names)."""
    import json
    setup()
    states_vol.reload()
    import state_careers as S
    import lesson as P
    from mountain import load_chat_setups
    out, info = [], S.build_arms(arms, strength)
    for v, a in info.items():
        out.append(f"{v}: nothing added" if a["vec"] is None else
                   f"{v}: {a['doc_set']} {a['theme']}, layer {a['layer']}, natural size {a['size']:.1f}, added at "
                   f"{a['strength']:g} x ({a['strength'] * a['size']:.1f}), from {a['source']} ({a['moments']} moments), "
                   f"fingerprint {a['sha']}")
    try:
        lines = P.load_lesson()
    except AssertionError as e:
        out.append(f"NOT READY: {e} (a run will refuse to start)")
        lines = P.load_lesson(allow_placeholder=True)
    H = lines["hunt"]
    if design == "lesson":
        out += [f"7 Jan, UBS at {H['before_at']}: {t}" for t in H["before_lines"]] + \
               [f"7 Jan, UBS after the stops fire: {t}" for t in H["filled_lines"]] + [f"7 Jan, UBS the update after: {t}" for t in H["after_lines"]]
    framed = json.load(open("data/silver/framed_chats_75.json"))["results"]
    out += P.check_days(design, framed, load_chat_setups(), lines, through)
    return out, list(info)


@app.function(gpu=GPU, timeout=24 * 3600, retries=modal.Retries(max_retries=5, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_job(arms, strength, rounds, when, span, only=None, framing="neutral", design="lesson", through=None):
    """Notebook 32's cells (imports, settings, model, memory check, agent, run), as scripts/modal_careers.py runs a
    notebook; `only` keeps one arm (--per-arm)."""
    import json, os, sys
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"   # as in Colab, set before torch starts
    repo = setup()
    states_vol.reload()
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    import state_careers as S
    info = S.build_arms(arms, strength)
    if only:
        info = {only: info[only]}
    nb = json.load(open(f"notebooks/{NOTEBOOK}.ipynb"))
    setup_cell, settings_cell, model_cell, memory_cell, agent_cell, run_cell, _glance = \
        ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    g = {"__name__": "__main__"}
    exec("import os, sys, json, glob, hashlib, time, datetime, torch", g)
    g.update(REPO=repo, BRANCH=BRANCH, PIN=json.load(open("results/full_career_pin.json")), ARM_INFO=info, WHEN=when,
             SPAN=span, FRAMING=framing, DESIGN=design, THROUGH=through)
    exec(setup_cell[setup_cell.index("from mountain import"):], g)      # the notebook's imports (no Colab parts)
    exec(settings_cell, g)                                                # its versions and inputs
    g["ROUNDS_HERE"] = rounds                                             # this job's rounds
    print(f"{NOTEBOOK}: design {design} through {through}, {framing} framing, arms {list(info)}, rounds {rounds} on {g['torch'].cuda.get_device_name(0)}", flush=True)
    exec(model_cell, g)                                                   # the model (weights cached between jobs)
    weights.commit()
    for cell in (memory_cell, agent_cell, run_cell):                      # the memory check, the agent, the run
        exec(cell, g)
    push(repo, "results", f"Modal job {NOTEBOOK}: final save")            # every save on GitHub before the server goes
    return f"{framing}: arms {list(info)} rounds {rounds}: done"


@app.function(cpu=2, memory=8192, timeout=3600, secrets=SECRETS)
def analyse(name):
    import subprocess
    repo = setup()
    folder = f"results/full_career_gemma-3-12b-it_4bit_{name}_v2"
    res = "results/" + name
    subprocess.run(f"python designs/rd2/analysis/lesson.py {folder} {res}", shell=True, check=True)
    push(repo, res, f"The lesson ({name}): analysis")
    return f"{res}/LESSON.md pushed"


def run_name(design, framing, when, span, through):
    """The notebook's NAME (the results folder), worked out the same way."""
    return (f"lesson_{design}" + ("" if framing == "neutral" else "_" + framing.replace(" + ", "_plus_"))
            + ("" if (when, span) == ("every", "update") else f"_{when}_{span}") + ("" if through is None else f"_to_{through}"))


@app.function(timeout=24 * 3600, secrets=SECRETS)
def dispatch(todo, strength, when, span, design, through):
    """Starts every job from inside Modal and waits there (no GPU), so --detach keeps them all running; then analyses."""
    calls = [run_job.spawn(arms, strength, rounds, when, span, only, framing, design, through)
             for arms, rounds, only, framing in todo]
    done = []
    for (arms, rounds, only, framing), c in zip(todo, calls):
        try:
            done.append(c.get())
        except Exception as e:                    # one job failing (after its retries) does not stop the others
            done.append(f"{framing}: {only or arms} rounds {rounds}: failed ({type(e).__name__})")
    for framing in dict.fromkeys(t[3] for t in todo):
        done.append(analyse.remote(run_name(design, framing, when, span, through)))
    return done


@app.local_entrypoint()
def main(arms: str = "none", strength: float = 2.0, rounds: str = "0-4", when: str = "every", span: str = "update",
         per_arm: bool = False, check: bool = False, analysis_only: bool = False, framings: str = "neutral",
         design: str = "lesson", through: str = "all"):
    assert when in ("every", "trading", "once", "start") and span in ("update", "all", "kept"), \
        "--when every|trading|once|start, --span update|all|kept"
    assert span != "kept" or when in ("once", "start"), "--span kept goes with --when once or start (one push, kept)"
    assert design in ("lesson", "watch", "silent"), "--design lesson|watch|silent"
    through = None if through == "all" else through
    fr = [f.strip() for f in framings.split(",") if f.strip()]
    assert fr and all(f in ("neutral", "loss", "gain", "loss + you", "gain + you") for f in fr), \
        '--framings: any of neutral, loss, gain, "loss + you", "gain + you", separated by commas'

    lines, names = check_arms.remote(arms, strength, design, through)   # a typo or an unscanned layer stops here
    print("arms and days as they will run:")
    for line in lines:
        print("  " + line)
    if check:
        return
    if analysis_only:
        for f in fr:
            print(analyse.remote(run_name(design, f, when, span, through)))
        return
    a, b = (rounds.split("-") + [None])[:2]
    rr = list(range(int(a), int(b) + 1)) if b else [int(r) for r in rounds.split(",")]
    todo = [(arms, [k], n, f) for f in fr for k in rr for n in (names if per_arm else [None])]
    print(f"the lesson ({design}, through {through or 'all five trading days'}): {len(fr)} framing(s) x {len(names)} arms x "
          f"{len(rr)} rounds = {len(fr) * len(names) * len(rr)} careers on {len(todo)} GPUs; state on {when} reply, span "
          f"{span}, {strength:g} x")
    for line in dispatch.remote(todo, strength, when, span, design, through):
        print(line)
