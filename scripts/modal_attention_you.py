"""Attention onto "you" at B's 300 saved requests, on Modal (the user, 30 Oct; sim/attention_you.py).

Each saved moment is kept exactly as it was up to UBS's request and the request is read in each of the five framings
(sim/matched.py). The history is read once into the cache; each framed update is read once with eager attention, and
every layer's attention weights are tapped at the decision token and at each "you" of the framed extra. Nothing is
sampled. Saved to /states/v2/attention_you/<career>__<chat>.npz: decision [framings x layers x heads x groups],
into_you [framings x layers x heads x groups], meta. Then the analysis (designs/rd2/analysis/attention_you.py), which
also reads the matched run's P(order goes along) at the same moments, and the results are pushed.

    modal run --detach scripts/modal_attention_you.py                 # 4 GPUs, then the analysis
    modal run --detach scripts/modal_attention_you.py --parts 1 --limit 2   # a trial: two moments on one GPU
    modal run --detach scripts/modal_attention_you.py --days chat           # the chat-only days (850 moments)

The chat-only days (the user, 30 Oct): every chat-only-day update with a UBS line in B's careers (17 a career), the
same reading; saved to /states/v2/attention_you_chat, results in results/attention_you_chat (linked to the blind words
labels, results/words_b, since there is no order on those days).
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
OUT = "/states/v2/attention_you"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-attention-you", image=image)
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


@app.function(gpu="H100", timeout=6 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_part(part, parts, limit=0, days="trading"):
    import json, os, time
    import numpy as np, torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import attention_you as A
    from career import career_opening
    from framing_set import FRAMINGS, read_set
    from inside_careers import moments
    from interventions import prefill
    chats = read_set()
    found = moments(FOLDER, "B") if days == "trading" else A.chat_moments(FOLDER)
    todo = sorted(found, key=lambda m: (m["career_file"], m["history_index"]))[part::parts]
    out_dir = OUT if days == "trading" else OUT + "_chat"
    if limit:
        todo = todo[:limit]
    os.makedirs(out_dir, exist_ok=True)
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16, attn_implementation="eager").eval()
    weights.commit()
    tap = A.Tap(model)
    opening = career_opening()
    t0 = time.time()
    for n, m in enumerate(todo):
        path = f"{out_dir}/{m['career_file'][:-5]}__{m['chat']}.npz"
        if os.path.exists(path):
            continue
        career = json.load(open(f"{FOLDER}/careers/{m['career_file']}"))
        dec, into, rows = A.run_moment(model, tok, tap, career, m, chats, opening, FRAMINGS, prefill)
        for r in rows:
            r.update({"experiment": "B", "history": m["version"], "run": m["run"], "chat": m["chat"], "date": m["date"],
                      "wants": m["wants"], "career_file": m["career_file"], "history_index": m["history_index"],
                      "saved_joined": m["joined"]})
        assert np.isfinite(dec).all(), f"{path}: a decision mass is not finite"
        with open(path + ".tmp", "wb") as fh:                # written whole, then renamed: a crash cannot leave a
            np.savez_compressed(fh, decision=dec, into_you=into, decision_groups=np.array(A.DECISION_GROUPS),
                                into_you_groups=np.array(A.INTO_YOU_GROUPS),
                                layer_types=np.array(model.config.get_text_config().layer_types), meta=np.array(json.dumps(rows)))
        os.replace(path + ".tmp", path)                     # half-written file that a retry would skip
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(cpu=4, memory=16384, timeout=2 * 3600, secrets=SECRETS, volumes=VOLUMES)
def analyse(days="trading"):
    import subprocess
    repo = setup()
    states_vol.reload()
    res = "results/attention_you" + ("" if days == "trading" else "_chat")
    flag = "" if days == "trading" else " --chat"
    subprocess.run(f"python designs/rd2/analysis/attention_you.py /states/v2 {res}{flag}", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {res} && git -C {repo} commit -q -m 'Attention onto you ({days} days)'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "attention-you results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=8 * 3600)
def dispatch(parts, limit, analysis_only, days="trading"):
    """Starts the parts inside Modal and waits for them there, then the analysis (survives the laptop closing)."""
    done = []
    if not analysis_only:
        calls = [(k, run_part.spawn(k, parts, limit, days)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(analyse.remote(days))
    return done


@app.local_entrypoint()
def main(parts: int = 4, limit: int = 0, analysis_only: bool = False, days: str = "trading"):
    assert days in ("trading", "chat"), "days: trading (the push requests) or chat (the chat-only days)"
    print(f"attention onto \"you\", {days} days: {parts} GPUs" + (f", {limit} moments each" if limit else "")
          + ", then the analysis")
    for line in dispatch.remote(parts, limit, analysis_only, days):
        print(line)
