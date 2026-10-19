"""Inside the model at the push requests of the full careers, on Modal (the user, 19 Oct). Two steps:

1. `read`: for each career of an experiment, one reading of its conversation by Gemma 3 12B at full precision (bfloat16,
   the precision Gemma Scope 2 was trained on; the careers ran in 4-bit, so `--precision 4bit` reads the exact states
   instead, as a check), keeping all 48 layers' residual stream at the last token before each push-request reply
   (sim/inside_careers.py). Saved to the Modal volume `rd2-states` (large; never committed to GitHub).
2. `features`: Gemma Scope 2 features and the decision read-out from those states
   (designs/rd2/analysis/inside_features.py); the summary (small) is pushed to GitHub in results/inside_full_career/.

From a machine with Modal's token:

    modal run --detach scripts/modal_inside.py --exps "B,F,A,C,D,E"          # read every experiment, then the features
    modal run --detach scripts/modal_inside.py --exps "" --features-only     # the features again, from saved states
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDERS = {"A": "career_book_neutral_lines_v2", "B": "ubs_framing_v2", "C": "takeover_ladder_v2",
           "D": "memo_and_ubs_framing_v2", "E": "memo_ubs_bank_c_v2", "F": "peer_same_frame_v2"}

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-inside", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def setup():
    """The repo at the latest commit, GitHub and Hugging Face sign-in (tokens never printed)."""
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
def read(exp, precision="bf16", part=0, parts=1):
    import collections, json, os, time
    import numpy as np, torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from career import career_opening
    from inside_careers import Recorder, encode, moments, positions, read as read_ids, turns_at
    pin = json.load(open("results/full_career_pin.json"))
    folder = "results/full_career_gemma-3-12b-it_4bit_" + FOLDERS[exp]
    by = collections.defaultdict(list)
    for m in moments(folder, exp):
        by[m["career_file"]].append(m)
    mine = sorted(by)[part::parts]
    out = f"/states/{exp}_{precision}"
    os.makedirs(out, exist_ok=True)
    todo = [cf for cf in mine if not os.path.exists(f"{out}/{cf[:-5]}.npz")]
    print(f"{exp} ({precision}), part {part + 1}/{parts}: {len(mine)} careers, {len(todo)} to read", flush=True)
    if not todo:
        return f"{exp} part {part}: nothing to do"
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    kw = {"quantization_config": BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                                    bnb_4bit_compute_dtype=torch.bfloat16)} if precision == "4bit" \
        else {"dtype": torch.bfloat16}
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto", **kw).eval()
    weights.commit()
    rec = Recorder(model)
    opening = career_opening()
    t0 = time.time()
    for n, cf in enumerate(todo):
        career = json.load(open(f"{folder}/careers/{cf}"))
        ms = by[cf]
        ids, pos, prompts = positions(tok, career, [m["history_index"] for m in ms], opening)
        ok = [p for p in pos if p is not None]
        got = read_ids(model, ids[:max(ok) + 1], ok, rec) if ok else {}
        rows, separate = [], 0
        for m, p, prompt in zip(ms, pos, prompts):
            if p is None:                            # not an exact prefix: read this moment on its own
                p = len(prompt) - 1
                got_one = read_ids(model, prompt, [p], rec)
                rows.append(got_one[p])
                separate += 1
            else:
                rows.append(got[p])
            m["tokens"] = p + 1
        np.savez_compressed(f"{out}/{cf[:-5]}.npz", states=torch.stack(rows).numpy().astype(np.float16),
                            meta=np.array(json.dumps(ms)))
        states_vol.commit()
        print(f"{exp} {cf}: {len(ms)} moments ({separate} read on their own), {len(ids):,} tokens | {n + 1}/{len(todo)} | "
              f"{(time.time() - t0) / 60:.0f} min", flush=True)
    return f"{exp} part {part}: {len(todo)} careers read"


@app.function(cpu=8, memory=65536, timeout=4 * 3600, secrets=SECRETS, volumes=VOLUMES)
def features(precision="bf16"):
    import subprocess
    repo = setup()
    states_vol.reload()
    subprocess.run(f"python designs/rd2/analysis/inside_features.py /states {precision} results/inside_full_career",
                   shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/inside_full_career && git -C {repo} commit -q -m "
                       f"'Inside the full careers: features and read-out ({precision})'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "features pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the features summary")


@app.function(timeout=12 * 3600)
def dispatch(exps, precision, parts, features_only):
    """Starts the readings inside Modal and waits for them there, then the features (survives the laptop closing)."""
    done = []
    if not features_only:
        calls = [(e, k, read.spawn(e, precision, k, parts)) for e in exps for k in range(parts)]
        for e, k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"{e} part {k}: failed ({type(err).__name__})")
    done.append(features.remote(precision))
    return done


@app.local_entrypoint()
def main(exps: str = "B,F,A,C,D,E", precision: str = "bf16", parts: int = 2, features_only: bool = False):
    todo = [e.strip() for e in exps.split(",") if e.strip()]
    print(f"reading {todo} ({precision}), {parts} GPUs per experiment; then the features")
    for line in dispatch.remote(todo, precision, parts, features_only):
        print(line)
