"""Same moment, different frame, on Modal (the user, 20 Oct; from an outside review of the inside plan).

The full careers compare loss and gain agents at the same request, but by then their histories, positions and P&L
differ. Here every saved B moment (50 careers x 6 push requests) is kept exactly as it was up to UBS's request, and only
the request itself changes: UBS's lines in each of the five framings (the user's frozen lines, `sim/matched.py`), each
with and without Bank C's line (F's frozen line in the same framing). For each of the 10 versions of the moment:
- the state at the last token before the reply (layers KEEP; no reply is sampled);
- P(the order goes along), by log-probs over the wide order grid after a fixed neutral reasoning line, and the grid's
  coverage (the share of all probability its orders take).
This separates the request's immediate effect (same history, different request) from the history's (different
careers, same request), and gives Bank C's line alone (same moment, with and without it). At bfloat16, like the
states and the steering.

    modal run --detach scripts/modal_matched.py                  # all parts, then the analysis
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]            # the Gemma Scope layers (12, 24, 31, 41), the steering layer and more
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
OUT = "/states/v2/matched/B_bf16"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-matched", image=image)
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
    import copy, json, math, os, time
    import numpy as np, torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from framing_set import FRAMINGS, read_set
    from inside_careers import Recorder, encode, moments, turns_at
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, order_prob, prefill, split_point
    from matched import matched
    from peer_lines import CHAT_ID, read_peers
    chats, peers = read_set(), read_peers()
    pid_of = {c: p for p, c in CHAT_ID.items()}
    todo = sorted(moments(FOLDER, "B"), key=lambda m: (m["career_file"], m["history_index"]))[part::parts]
    os.makedirs(OUT, exist_ok=True)
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    rec = Recorder(model)
    opening = career_opening()
    t0 = time.time()
    for n, m in enumerate(todo):
        path = f"{OUT}/{m['career_file'][:-5]}__{m['chat']}.npz"
        if os.path.exists(path):
            continue
        career = json.load(open(f"{FOLDER}/careers/{m['career_file']}"))
        idx, position = m["history_index"], m["held_their_way"] * SIGN[m["wants"]]
        full0, k = split_point(tok, career, idx, opening)
        rec.reset([])
        cache = prefill(model, full0[:k])               # the history before the request: the same in all 10 versions
        rows, states = [], []
        for v1 in FRAMINGS:
            for bank_c in (False, True):
                c = matched(career, idx, m["date"], m["version"], v1, chats,
                            peers[pid_of[m["chat"]]][v1]["peer"] if bank_c else None)
                full = encode(tok, turns_at(c, idx, opening))
                assert full[:k] == full0[:k], "the history before the request changed"
                rec.reset([len(full) - 1])
                rec.seen = [k] * len(rec.layers)             # the cache holds the first k tokens
                with torch.no_grad():
                    model(input_ids=torch.tensor([full[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                          use_cache=True, cache_position=torch.arange(k, len(full), device=model.device))
                states.append(rec.states(len(full) - 1)[KEEP].numpy())
                rec.reset([])
                p, scores = order_prob(model, tok, full, cache, NEUTRAL_LEAD, position, m["wants"], detail=True,
                                       grid=WIDE_GRID)
                rows.append({"experiment": "B", "history": m["version"], "run": m["run"], "chat": m["chat"],
                             "date": m["date"], "wants": m["wants"], "career_file": m["career_file"],
                             "held_their_way": m["held_their_way"], "saved_joined": m["joined"],
                             "framing": v1, "bank_c": bank_c, "p_order_along": p,
                             "coverage": float(sum(math.exp(s) for s in scores)), "tokens": len(full)})
        arr = np.stack(states).astype(np.float32)
        assert np.isfinite(arr).all(), f"{path}: a state is not finite"
        np.savez_compressed(path, states=arr, layers=np.array(KEEP), meta=np.array(json.dumps(rows)))
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(cpu=8, memory=65536, timeout=4 * 3600, secrets=SECRETS, volumes=VOLUMES)
def analyse():
    import subprocess
    repo = setup()
    states_vol.reload()
    subprocess.run("python designs/rd2/analysis/matched_history.py /states/v2 results/matched", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/matched && git -C {repo} commit -q -m 'Same moment, different frame'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "matched-history results pushed"
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
def main(parts: int = 4, analysis_only: bool = False):
    print(f"same moment, different frame: {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only):
        print(line)
