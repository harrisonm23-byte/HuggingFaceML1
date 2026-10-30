"""Causal tests at the saved decision moments, on Modal (the user, 20 Oct). Needs the states from
scripts/modal_inside.py (the decision moments of B) on the volume `rd2-states`, to build the frame direction.

Moments: the first two push requests (7 Jan, 12 Jan, where going along happens) of B's neutral and loss + you careers
and F's gain + you careers. For each, 8 replies per condition, at bfloat16 (the precision the direction was read at):
- B neutral: as saved; + the loss-frame direction at two strengths; + a random direction (the larger strength);
  + the memo's loss direction (7b: built from A's memo, so not from framed UBS words).
- B loss + you: as saved; - the loss-frame direction at two strengths; - a random direction; - the memo's loss
  direction; its own earlier reasoning neutralised (length-matched; follow-up).
Each condition also gets the order's probability by log-probs (the share of probability on orders that go along,
after a fixed neutral reasoning line; as saved, also after its own saved reasoning).
- F gain + you: as saved; its own earlier reasoning neutralised.
The loss-frame direction (layer LAYER): B's loss and loss + you states minus its neutral states at the same requests,
built on the other half of the careers (rounds 0-4 for 5-9 and the reverse), so no career steers with a direction it
helped build. Strength: 2x and 4x the gap between B's loss and neutral moments along the direction (the random
and memo directions at 4x, the same size).

    modal run --detach scripts/modal_interventions.py                 # all parts, then the summary
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
LAYER, STRENGTHS, SAMPLES = 24, [2, 4], 8      # strengths: multiples of the loss - neutral gap along the direction
REQUESTS = ["p344_i_can_hunt_with_u", "p316_bust_through_it"]
GROUPS = [("B", "ubs_framing_v2", "neutral"), ("B", "ubs_framing_v2", "loss + you"), ("F", "peer_same_frame_v2", "gain + you")]

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-interventions", image=image)
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


def directions(width):
    """The loss-frame direction at LAYER for each half of the careers (built on the other half), the random direction,
    and the median residual size: from B's saved decision states."""
    import glob, json
    import numpy as np
    meta, X = [], []
    for f in sorted(glob.glob("/states/v2/B_bf16/*.npz")):
        z = np.load(f)
        meta += json.loads(str(z["meta"]))
        X.append(z["states"][:, LAYER].astype(np.float32))
    assert meta, "no B states in /states/v2: run scripts/modal_inside.py first"
    X = np.concatenate(X)
    assert np.isfinite(X).all(), "a B state is not finite"
    ver = np.array([m["version"] for m in meta])
    req = np.array([m["chat"] for m in meta])
    half = np.array([m["run"] >= 5 for m in meta])
    out = {}
    for h in (False, True):
        build = half == (not h)                              # built on the other half
        diffs = []
        for r in np.unique(req):
            a = build & (req == r) & np.isin(ver, ["loss", "loss + you"])
            b = build & (req == r) & (ver == "neutral")
            diffs.append(X[a].mean(0) - X[b].mean(0))
        u = np.mean(diffs, 0)
        out[h] = u / np.linalg.norm(u)
    # The size of a step: how far apart the loss and neutral moments sit along the direction (on all careers). Steering
    # by 2x and 4x that gap; not a share of the residual's length, which Gemma's few very large dimensions dominate.
    u_all = (out[False] + out[True]) / 2
    u_all = u_all / np.linalg.norm(u_all)
    proj = X @ u_all
    gap = float(np.mean([proj[(req == r) & np.isin(ver, ["loss", "loss + you"])].mean() - proj[(req == r) & (ver == "neutral")].mean()
                         for r in np.unique(req)]))
    rnd = np.random.default_rng(7).normal(size=width)
    # 7b: a loss direction built elsewhere, from A's memo (loss and loss + you memos minus the neutral memo at the same
    # requests; UBS's lines are the same neutral ones in all of them, so no framed UBS words are in it)
    memo = None
    ma, XA = [], []
    for f in sorted(glob.glob("/states/v2/A_bf16/*.npz")):
        z = np.load(f)
        ma += json.loads(str(z["meta"]))
        XA.append(z["states"][:, LAYER].astype(np.float32))
    if ma:
        XA = np.concatenate(XA)
        va, ra = np.array([m["version"] for m in ma]), np.array([m["chat"] for m in ma])
        asked = np.array([m.get("asked", True) for m in ma])
        d = [XA[asked & (ra == r) & np.isin(va, ["loss", "loss + you"])].mean(0) - XA[asked & (ra == r) & (va == "neutral")].mean(0)
             for r in np.unique(ra[asked])]
        memo = np.mean(d, 0)
        memo = memo / np.linalg.norm(memo)
    print(f"loss - neutral gap along the frame direction at layer {LAYER}: {gap:.2f} (residual length, median: "
          f"{float(np.median(np.linalg.norm(X, axis=1))):.1f})", flush=True)
    return out, rnd / np.linalg.norm(rnd), abs(gap), memo


@app.function(gpu="H100", timeout=8 * 3600, retries=modal.Retries(max_retries=2, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_part(part, parts):
    import json, os, re, time
    import numpy as np, torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    states_vol.reload()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from inside_careers import moments
    from interventions import NEUTRAL_LEAD, SIGN, Steer, goes_along, neutralise_own_words, order_prob, prefill, sample, split_point
    pin = json.load(open("results/full_career_pin.json"))
    todo = []
    for exp, folder, version in GROUPS:
        for m in moments("results/full_career_gemma-3-12b-it_4bit_" + folder, exp):
            if m["version"] == version and m["chat"] in REQUESTS:
                todo.append((folder, m))
    todo = todo[part::parts]
    out_path = f"/states/v2/interventions/part{part}.jsonl"
    os.makedirs("/states/v2/interventions", exist_ok=True)
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["key"] for l in open(out_path)}
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers = [mm for _, mm in model.named_modules() if type(mm).__name__.endswith("DecoderLayer")]
    width = model.config.get_text_config().hidden_size
    frame, rnd, size, memo = directions(width)
    steer = Steer(layers[LAYER])
    opening = career_opening()
    t0 = time.time()
    for n, (folder, m) in enumerate(todo):
        career = json.load(open(f"results/full_career_gemma-3-12b-it_4bit_{folder}/careers/{m['career_file']}"))
        position = m["held_their_way"] * SIGN[m["wants"]]
        u = torch.tensor(frame[m["run"] >= 5])
        r = torch.tensor(rnd)
        mm = torch.tensor(memo) if memo is not None else None
        conds = [("as saved", None, career)]
        if m["version"] == "neutral":
            conds += [(f"+ loss frame x{s}", u * s * size, career) for s in STRENGTHS] + \
                     [(f"+ random x{STRENGTHS[-1]}", r * STRENGTHS[-1] * size, career)]
            if mm is not None:
                conds.append((f"+ memo loss direction x{STRENGTHS[-1]}", mm * STRENGTHS[-1] * size, career))
        elif m["version"] == "loss + you":
            conds += [(f"- loss frame x{s}", -u * s * size, career) for s in STRENGTHS] + \
                     [(f"- random x{STRENGTHS[-1]}", -r * STRENGTHS[-1] * size, career)]
            if mm is not None:
                conds.append((f"- memo loss direction x{STRENGTHS[-1]}", -mm * STRENGTHS[-1] * size, career))
        if m["version"] != "neutral":
            conds.append(("own words neutralised", None, neutralise_own_words(career, m["history_index"])))
        caches = {}
        for name, vec, c in conds:
            key = f"{m['experiment']}|{m['version']}|{m['run']}|{m['chat']}|{name}"
            if key in done:
                continue
            full, k = split_point(tok, c, m["history_index"], opening)
            ck = id(c)
            if ck not in caches:
                steer.vec = None
                caches[ck] = prefill(model, full[:k])        # the history before the request's update, unsteered
            steer.vec = vec.to(model.device) if vec is not None else None
            replies = sample(model, full, caches[ck], SAMPLES, tok=tok)
            # The order's probability (log-probs on the order), under the same condition: after a fixed neutral
            # reasoning line, and (as saved only) after the agent's own saved reasoning
            p_lead = order_prob(model, tok, full, caches[ck], NEUTRAL_LEAD, position, m["wants"])
            own = re.split(r"\n\s*(?:TARGET|HOLD|CHAT:|QUOTE)", m["reply"] or "", maxsplit=1)[0]
            p_own = order_prob(model, tok, full, caches[ck], own, position, m["wants"]) if name == "as saved" else None
            steer.vec = None
            rows = [dict(zip(("along", "status"), goes_along(x, position, m["wants"]))) for x in replies]
            with open(out_path, "a") as f:
                f.write(json.dumps({"key": key, "experiment": m["experiment"], "version": m["version"], "run": m["run"],
                                    "chat": m["chat"], "condition": name, "saved_joined": m["joined"],
                                    "p_order_along": p_lead, "p_order_along_own_reasoning": p_own,
                                    "along": [x["along"] for x in rows], "status": [x["status"] for x in rows],
                                    "replies": replies}) + "\n")
            states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(cpu=2, timeout=3600, secrets=SECRETS, volumes=VOLUMES)
def summarise():
    import glob, json, os, subprocess
    import numpy as np
    repo = setup()
    states_vol.reload()
    rows = [json.loads(l) for f in sorted(glob.glob("/states/v2/interventions/*.jsonl")) for l in open(f)]
    rng = np.random.default_rng(1)
    rep = ["# Causal tests at the decision moments\n",
           f"Rerunning only the agent's reply to UBS's request on 7 and 12 Jan, {SAMPLES} replies per condition, Gemma 3 "
           f"12B at bfloat16, steering at layer {LAYER} from the start of the request's update (the history before is "
           "unchanged). Going along: the reply's order moves the position UBS's way and leaves it on UBS's side. "
           "p: the change against 'as saved' for the same moments, signs flipped by career (10,000 times). "
           "Produced by `scripts/modal_interventions.py`.\n"]
    out = {}
    for exp, _, version in GROUPS:
        sub = [r for r in rows if r["experiment"] == exp and r["version"] == version]
        if not sub:
            continue
        rep.append(f"\n## {exp} {version}\n")
        rep.append("| Condition | Moments | Replies going along | Readable replies | Change vs as saved | p | P(order goes along), log-probs | Change | p |\n|---|---|---|---|---|---|---|---|---|")
        base = {(r["run"], r["chat"]): np.mean(r["along"]) for r in sub if r["condition"] == "as saved"}
        base_lp = {(r["run"], r["chat"]): r["p_order_along"] for r in sub if r["condition"] == "as saved"}
        for cond in sorted({r["condition"] for r in sub}, key=lambda c: (c != "as saved", c)):
            cs = [r for r in sub if r["condition"] == cond]
            rate = np.mean([a for r in cs for a in r["along"]])
            readable = np.mean([s in ("trade", "hold") for r in cs for s in r["status"]])
            plp = np.mean([r["p_order_along"] for r in cs])
            line = f"| {cond} | {len(cs)} | {100 * rate:.0f}% | {100 * readable:.0f}% |"
            if cond == "as saved":
                own = [r["p_order_along_own_reasoning"] for r in cs if r.get("p_order_along_own_reasoning") is not None]
                rep.append(line + f" - | - | {100 * plp:.1f}% (after its own reasoning: {100 * np.mean(own):.1f}%) | - | - |")
                continue

            def flip_test(field, basemap):
                by_run = {}
                for r in cs:
                    if (r["run"], r["chat"]) in basemap:
                        by_run.setdefault(r["run"], []).append(field(r) - basemap[(r["run"], r["chat"])])
                d = np.array([np.mean(v) for v in by_run.values()])
                obs = d.mean() if len(d) else np.nan
                hits = sum(abs((d * rng.choice([-1, 1], len(d))).mean()) >= abs(obs) - 1e-12 for _ in range(10000))
                return obs, (hits + 1) / 10001

            o1, p1 = flip_test(lambda r: np.mean(r["along"]), base)
            o2, p2 = flip_test(lambda r: r["p_order_along"], base_lp)
            rep.append(line + f" {100 * o1:+.1f} points | {p1:.4f} | {100 * plp:.1f}% | {100 * o2:+.1f} points | {p2:.4f} |")
            out.setdefault(f"{exp} {version}", {})[cond] = {"rate": rate, "change": o1, "p_order": plp, "p_order_change": o2}
    os.makedirs(f"{repo}/results/interventions", exist_ok=True)
    open(f"{repo}/results/interventions/INTERVENTIONS.md", "w").write("\n".join(rep) + "\n")
    json.dump(out, open(f"{repo}/results/interventions/summary.json", "w"), indent=1)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/interventions && git -C {repo} commit -q -m 'Causal tests at the decision moments'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "summary pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the summary")


@app.function(timeout=12 * 3600)
def dispatch(parts, summary_only):
    done = []
    if not summary_only:
        calls = [(k, run_part.spawn(k, parts)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(summarise.remote())
    return done


@app.local_entrypoint()
def main(parts: int = 8, summary_only: bool = False):
    print(f"causal tests at the decision moments: {parts} GPUs, then the summary")
    for line in dispatch.remote(parts, summary_only):
        print(line)
