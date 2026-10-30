"""Push and cue on Modal (the user, 28 Oct; designs/rd2/PLAN_PUSH_CUE.md). Two rereads of B's saved careers at UBS's
12 January request; no career is run and nothing is sampled.

1. The carry (GPU): each of B's 50 careers at 12 January, with UBS's earlier words set back to neutral and everything
   the agent wrote and did kept (`sim/push_carry.py`): as saved, the 7 January request neutral, every earlier UBS line
   neutral; each with the 12 January request as saved and neutral. P(the order goes along) after the fixed neutral
   reasoning line, as in the matched rereads. About 4 minutes of model loading and half a minute per framed career on
   one H100: about $2-4.
2. The cue (CPU, no model): from the matched rereads already on the volume (/states/v2/matched/B_bf16), at 12 January,
   P(the order goes along) with UBS's blame line ("I'm counting on you to deliver it") against the neutral line, in
   every career; and the change that line makes to the state against the change the blame line made on 7 January.
   Pennies.
Then `designs/rd2/analysis/push_carry.py` writes results/push_carry/PUSH_CARRY.md and the results are pushed.

    modal run scripts/modal_push_carry.py --check             # no Modal call: builds every version, prints counts
    modal run --detach scripts/modal_push_carry.py --part cue  # the cue only (CPU)
    modal run --detach scripts/modal_push_carry.py             # both, then the analysis
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
MATCHED = "/states/v2/matched/B_bf16"
OUT = "/states/v2/push_carry/B_bf16"
RESULTS = "results/push_carry"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-push-carry", image=image)
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


def todo_moments():
    """B's 50 careers at UBS's 12 January request."""
    from inside_careers import moments
    from push_carry import CUE_CHAT
    return sorted((m for m in moments(FOLDER, "B") if m["chat"] == CUE_CHAT), key=lambda m: m["career_file"])


@app.function(gpu="H100", timeout=4 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def carry_part(part, parts):
    import json, os, time
    import torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from framing_set import read_set
    from push_carry import score_moment
    chats, todo = read_set(), todo_moments()[part::parts]
    os.makedirs(OUT, exist_ok=True)
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    opening, t0 = career_opening(), time.time()
    for n, m in enumerate(todo):
        path = f"{OUT}/{m['career_file']}"
        if os.path.exists(path):
            continue
        career = json.load(open(f"{FOLDER}/careers/{m['career_file']}"))
        rows = score_moment(model, tok, career, m, chats, opening)
        with open(path + ".tmp", "w") as fh:                # written whole, then renamed, so a retry skips only
            json.dump(rows, fh)                             # finished careers
        os.replace(path + ".tmp", path)
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} careers | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} careers"


@app.function(cpu=4, memory=16384, timeout=3600, secrets=SECRETS, volumes=VOLUMES)
def cue():
    """From the matched rereads on the volume: each career's 12 January request with the blame line and the neutral
    one, and the state change each blame line makes (12 and 7 January) at the kept layers."""
    import json, os
    import numpy as np
    setup()
    from push_carry import CUE_CHAT, PUSH_CHAT, cue_row
    states_vol.reload()
    out = []
    for m in todo_moments():
        stem = m["career_file"][:-5]
        out.append(cue_row(np.load(f"{MATCHED}/{stem}__{CUE_CHAT}.npz"), np.load(f"{MATCHED}/{stem}__{PUSH_CHAT}.npz"),
                           m["career_file"]))
    os.makedirs("/states/v2/push_carry", exist_ok=True)
    json.dump(out, open("/states/v2/push_carry/cue_rows.json", "w"))
    states_vol.commit()
    return f"cue: {len(out)} careers"


@app.function(cpu=4, memory=16384, timeout=3600, secrets=SECRETS, volumes=VOLUMES)
def analyse():
    import glob, json, os, shutil, subprocess
    repo = setup()
    states_vol.reload()
    os.makedirs(RESULTS, exist_ok=True)
    rows = [r for p in sorted(glob.glob(f"{OUT}/*.json")) for r in json.load(open(p))]
    if rows:
        json.dump(rows, open(f"{RESULTS}/carry_rows.json", "w"), indent=0)
    if os.path.exists("/states/v2/push_carry/cue_rows.json"):
        shutil.copy("/states/v2/push_carry/cue_rows.json", f"{RESULTS}/cue_rows.json")
    subprocess.run(f"python designs/rd2/analysis/push_carry.py {RESULTS}", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {RESULTS} && git -C {repo} commit -q -m 'Push and cue: the rereads'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "push-and-cue results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=6 * 3600)
def dispatch(part, parts):
    """Starts the parts inside Modal and waits for them there, then the analysis (survives the laptop closing)."""
    done = []
    if part in ("all", "cue"):
        done.append(cue.remote())
    if part in ("all", "carry"):
        calls = [(k, carry_part.spawn(k, parts)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(analyse.remote())
    return done


@app.local_entrypoint()
def main(part: str = "all", parts: int = 1, check: bool = False):
    assert part in ("all", "carry", "cue"), "part: all, carry (GPU) or cue (CPU)"
    if check:                                             # local only: every version built from the saved careers
        import collections, json, os, sys
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sim"))
        from framing_set import read_set
        from push_carry import reread_versions
        chats, seen = read_set(), collections.Counter()
        for m in todo_moments():
            career = json.load(open(f"{FOLDER}/careers/{m['career_file']}"))
            for (cond, req), (_, changed) in reread_versions(career, m["history_index"], chats).items():
                seen[(career["version"], cond, tuple((d, n) for _, d, n in changed))] += 1
        for k, n in sorted(seen.items()):
            print(f"{k[0]:11s} | {k[1]:13s} | UBS lines set to neutral: {list(k[2]) or 'none'} | x{n}")
        print(f"{len(todo_moments())} careers at 12 January; nothing sent to Modal")
        return
    print(f"push and cue: {part}, {parts} GPU part(s) for the carry, then the analysis")
    for line in dispatch.remote(part, parts):
        print(line)
