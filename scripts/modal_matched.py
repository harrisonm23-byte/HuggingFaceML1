"""Same moment, different frame, on Modal (the user, 20 Oct; from an outside review of the inside plan).

The full careers compare loss and gain agents at the same request, but by then their histories, positions and P&L
differ. Here every saved B moment (50 careers x 6 push requests) is kept exactly as it was up to UBS's request, and only
the request itself changes: UBS's lines in each of the five framings (the user's frozen lines, `sim/matched.py`), each
with and without Bank C's line (F's frozen line in the same framing). For each of the 10 versions of the moment:
- the state at the last token before the reply (layers KEEP; no reply is sampled);
- P(the order goes along), by log-probs over the wide order grid after a fixed neutral reasoning line (each size
  scored as a whole number, in both ways the agents write a positive order: `order_dist`), and the grid's coverage (the
  share of all probability its orders take).
This separates the request's immediate effect (same history, different request) from the history's (different
careers, same request), and gives Bank C's line alone (same moment, with and without it). At bfloat16, like the
states and the steering.

Experiment A, the same idea for management's priming (the user, 20 Oct): every A career (25, the "no ask" ones left
out) kept exactly as saved, with only the memo and all five morning books set to each of the five versions (their
30-day P&L still carries the agent's own; `sim/matched.py` swap_priming). Moments: the six push requests (P(order goes
along)) and the first update of each trading day, where A's effect showed (it traded far bigger before any chat): the
expected size of its order and the chance it changes its position, from the same log-probs. Rows (the career's own
version) x columns (the priming it is given) separate the priming itself (a neutral career given the loss memo) from
what its own earlier words carry (a loss career with the memo taken away).

    modal run --detach scripts/modal_matched.py                  # B: all parts, then the analysis
    modal run --detach scripts/modal_matched.py --exp A          # A: management's priming
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]            # the Gemma Scope layers (12, 24, 31, 41), the steering layer and more
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
OUT = "/states/v2/matched/B_bf16"
FOLDER_A = "results/full_career_gemma-3-12b-it_4bit_career_book_neutral_lines_v2"
OUT_A = "/states/v2/matched/A_bf16"
A_VERSIONS = ["neutral", "loss", "gain", "loss + you", "gain + you"]

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
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, order_dist, prefill, split_point, summarise_orders
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
                orders, probs, cover = order_dist(model, tok, full, cache, NEUTRAL_LEAD, WIDE_GRID)
                rows.append({"experiment": "B", "history": m["version"], "run": m["run"], "chat": m["chat"],
                             "date": m["date"], "wants": m["wants"], "career_file": m["career_file"],
                             "held_their_way": m["held_their_way"], "saved_joined": m["joined"],
                             "framing": v1, "bank_c": bank_c, **summarise_orders(orders, probs, position, m["wants"]),
                             "coverage": cover, "probs": probs, "tokens": len(full)})
        arr = np.stack(states).astype(np.float32)
        assert np.isfinite(arr).all(), f"{path}: a state is not finite"
        with open(path + ".tmp", "wb") as fh:                # written whole, then renamed: a crash cannot leave a
            np.savez_compressed(fh, states=arr, layers=np.array(KEEP), meta=np.array(json.dumps(rows)))
        os.replace(path + ".tmp", path)                     # half-written file that a retry would skip
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(gpu="H100", timeout=8 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_part_memo(part, parts):
    import copy, glob, json, math, os, re, time
    import numpy as np, torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from inside_careers import Recorder, encode, moments, turns_at
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, order_dist, prefill, split_point, summarise_orders
    from matched import priming_days, swap_priming
    requests = {}
    for m in moments(FOLDER_A, "A"):
        if m["asked"]:
            requests.setdefault(m["career_file"], []).append(m)
    files = sorted(f for f in os.listdir(f"{FOLDER_A}/careers")
                   if json.load(open(f"{FOLDER_A}/careers/{f}"))["version"] in A_VERSIONS)[part::parts]
    os.makedirs(OUT_A, exist_ok=True)
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    rec = Recorder(model)
    opening = career_opening()
    t0 = time.time()
    for n, cf in enumerate(files):
        path = f"{OUT_A}/{cf[:-5]}.npz"
        if os.path.exists(path):
            continue
        career, days = json.load(open(f"{FOLDER_A}/careers/{cf}")), priming_days(FOLDER_A, cf)
        v0 = career["version"]
        books = [i for i, t in enumerate(career["history"]) if t["role"] == "user" and "Morning book, " in t["content"]]
        # The moments: each trading day's first update (where the book is) and each push request
        todo = [{"kind": "opening", "history_index": i, "wants": None, "position": None} for i in books] + \
               [{"kind": "request", "history_index": m["history_index"], "wants": m["wants"], "chat": m["chat"],
                 "position": m["held_their_way"] * SIGN[m["wants"]], "saved_joined": m["joined"]}
                for m in requests.get(cf, [])]
        full0, k0 = split_point(tok, career, books[0], opening)
        rec.reset([])
        shared = prefill(model, full0[:k0])               # everything before the memo: the same in every version
        rows, states = [], []
        for x in todo:
            for v1 in A_VERSIONS:
                c1 = swap_priming(career, v0, v1, days)
                full, k = split_point(tok, c1, x["history_index"], opening)
                assert full[:k0] == full0[:k0], "the history before the memo changed"
                cache = copy.deepcopy(shared)
                rec.reset([])
                for a in range(k0, k, 4096):              # the career from the memo to this moment, in this version,
                    b = min(a + 4096, k)                  # in pieces (one piece would need ~58 GB for its logits)
                    with torch.no_grad():
                        model(input_ids=torch.tensor([full[a:b]], device=model.device), past_key_values=cache,
                              use_cache=True, cache_position=torch.arange(a, b, device=model.device))
                rec.reset([len(full) - 1])
                rec.seen = [k] * len(rec.layers)
                with torch.no_grad():
                    model(input_ids=torch.tensor([full[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                          use_cache=True, cache_position=torch.arange(k, len(full), device=model.device))
                states.append(rec.states(len(full) - 1)[KEEP].numpy())
                rec.reset([])
                position = x["position"]
                if position is None:                       # the opening: its position, as the update shows it
                    position = float(re.findall(r"Your position: ([+-][\d,]+) oz", c1["history"][x["history_index"]]["content"])[-1].replace(",", ""))
                orders, probs, cover = order_dist(model, tok, full, cache, NEUTRAL_LEAD, WIDE_GRID)
                rows.append({"experiment": "A", "history": v0, "run": career["run"], "career_file": cf,
                             "kind": x["kind"], "history_index": x["history_index"], "chat": x.get("chat"),
                             "wants": x["wants"], "position": position, "saved_joined": x.get("saved_joined"),
                             "priming": v1, "p_order_along": None,
                             **summarise_orders(orders, probs, position, x["wants"]),
                             "coverage": cover, "probs": probs, "tokens": len(full)})
        arr = np.stack(states).astype(np.float32)
        assert np.isfinite(arr).all(), f"{path}: a state is not finite"
        with open(path + ".tmp", "wb") as fh:                # written whole, then renamed: a crash cannot leave a
            np.savez_compressed(fh, states=arr, layers=np.array(KEEP), meta=np.array(json.dumps(rows)))
        os.replace(path + ".tmp", path)                     # half-written file that a retry would skip
        states_vol.commit()
        print(f"A part {part}: {n + 1}/{len(files)} careers | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"A part {part}: {len(files)} careers"


@app.function(cpu=8, memory=65536, timeout=4 * 3600, secrets=SECRETS, volumes=VOLUMES)
def analyse(exp="B"):
    import subprocess
    repo = setup()
    states_vol.reload()
    script = "matched_history.py" if exp == "B" else "matched_memo.py"
    subprocess.run(f"python designs/rd2/analysis/{script} /states/v2 results/matched", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/matched && git -C {repo} commit -q -m 'Same moment, different frame'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "matched-history results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=12 * 3600)
def dispatch(parts, analysis_only, exp="B"):
    """Starts the parts inside Modal and waits for them there, then the analysis (survives the laptop closing)."""
    done = []
    if not analysis_only:
        calls = [(k, (run_part if exp == "B" else run_part_memo).spawn(k, parts)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(analyse.remote(exp))
    return done


@app.local_entrypoint()
def main(exp: str = "B", parts: int = 4, analysis_only: bool = False):
    assert exp in ("A", "B"), "exp: B (UBS's framing) or A (management's priming)"
    print(f"same moment, different {'frame' if exp == 'B' else 'priming'} ({exp}): {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only, exp):
        print(line)
