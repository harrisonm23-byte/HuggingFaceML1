"""Steering, second run: Stage 1 of the "ideal acquiescence" plan (designs/rd2/PREREG_STEER2.md).

The frame direction is the change in the model's state when only the framing of UBS's request changes, everything before
it held fixed (the matched rereads, `scripts/modal_matched.py`). Here that direction is added to the residual stream at
saved decision moments, by hand and with no framed words, to see whether the decision follows:
- at UBS's requests: P(the order goes along) (log-probs after a fixed neutral reasoning line), and for some conditions
  two sampled replies (going along, and whether the reply is still readable);
- at each trading day's first update, before any chat: the expected size of the order and the chance it changes its
  position (the risk-taking that the loss frame kept raising all career).

The review of the first steering run (20 Oct) found four faults; each is fixed here:
- the direction and its size come from the other half of the careers (built on runs 0-4, applied to runs 5-9 and back);
- ten random directions of the same size, not one;
- both signs in both groups (adding to neutral careers and subtracting from them; the same for loss-framed careers);
- orders scored as whole numbers in both written forms (`order_dist`).
"""
import json, os, re
import numpy as np

FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]       # the layers the matched run saved
LAYER, CHECK_LAYER = 12, 18                   # 12: where the held-fixed and across-career directions agree (0.98)
STRENGTHS = [1, 2, 4]                         # multiples of the natural size: how far the framing itself moves the state
N_RANDOM, RANDOM_STRENGTH = 10, 2
SAMPLES = 2


def run_of(meta):
    if "run" in meta:
        return int(meta["run"])
    return int(re.search(r"_r(\d+)\.json$", meta["career_file"]).group(1))


def directions(npz_paths, layer, n_random=N_RANDOM, seed=20261021):
    """{half: {"loss", "gain", "loss_minus_gain": vectors at their natural size (the mean shift), "random": unit vectors,
    "size": the loss shift's length}}. Half 0 is applied to runs 0-4 and built on runs 5-9; half 1 the other way."""
    j = KEEP.index(layer)
    idx = {(v, b): 2 * i + int(b) for i, v in enumerate(FRAMINGS) for b in (False, True)}
    shifts = {"loss": [], "gain": [], "run": []}
    for p in npz_paths:
        z = np.load(p)
        assert [int(x) for x in z["layers"]] == KEEP, f"{p}: saved layers {list(z['layers'])}, expected {KEEP}"
        meta = json.loads(str(z["meta"]))
        S = z["states"][:, j].astype(np.float64)                      # 10 versions x width
        neutral = S[idx[("neutral", False)]]
        shifts["loss"].append((S[idx[("loss", False)]] + S[idx[("loss + you", False)]]) / 2 - neutral)
        shifts["gain"].append((S[idx[("gain", False)]] + S[idx[("gain + you", False)]]) / 2 - neutral)
        shifts["run"].append(run_of(meta[0]))
    run = np.array(shifts["run"])
    L, G = np.stack(shifts["loss"]), np.stack(shifts["gain"])
    width = L.shape[1]
    out = {}
    for half in (0, 1):
        built_on = run >= 5 if half == 0 else run < 5
        loss, gain = L[built_on].mean(0), G[built_on].mean(0)
        rng = np.random.default_rng(seed + half)
        rnd = rng.normal(size=(n_random, width))
        out[half] = {"loss": loss, "gain": gain, "loss_minus_gain": loss - gain,
                     "random": rnd / np.linalg.norm(rnd, axis=1, keepdims=True), "size": float(np.linalg.norm(loss)),
                     "moments_used": int(built_on.sum())}
    return out


def half_for(run):
    return 0 if run < 5 else 1


def conditions(group, kind):
    """[(name, layer, which, sign, strength, sampled)]. group: "neutral" (B's neutral careers) or "loss" (its loss and
    loss + you careers); kind: "request" or "opening". which: a direction's name or "random<k>"."""
    c = [("none", None, None, 0, 0, kind == "request" and group == "neutral")]
    strengths = STRENGTHS if group == "neutral" else STRENGTHS[:2]
    for s in strengths:
        c.append((f"+loss x{s}", LAYER, "loss", 1, s, kind == "request" and group == "neutral"))
        c.append((f"-loss x{s}", LAYER, "loss", -1, s, False))
    if group == "neutral":
        for s in STRENGTHS:
            c.append((f"+gain x{s}", LAYER, "gain", 1, s, kind == "request" and s == 2))
            c.append((f"+(loss - gain) x{s}", LAYER, "loss_minus_gain", 1, s, False))
        if kind == "request":
            c += [(f"+loss x{s} at layer {CHECK_LAYER}", CHECK_LAYER, "loss", 1, s, False) for s in STRENGTHS]
    n = N_RANDOM if group == "neutral" else N_RANDOM // 2
    c += [(f"random{k} x{RANDOM_STRENGTH}", LAYER, f"random{k}", 1, RANDOM_STRENGTH,
           kind == "request" and group == "neutral" and k < 3) for k in range(n)]
    return c


def vector(dirs, which, sign, strength):
    """The vector to add: a direction at `strength` times its natural size; a random one at the loss shift's size."""
    if which is None:
        return None
    if which.startswith("random"):
        return sign * strength * dirs["size"] * dirs["random"][int(which[6:])]
    return sign * strength * dirs[which]


def openings(career, days):
    """Each trading day's first update in the conversation (before any chat that day), with the position it shows."""
    users = [i for i, t in enumerate(career["history"]) if t["role"] == "user"]
    out = []
    for day in days:
        obs = day["steps"][0]["observation"]
        hits = [i for i in users if obs in career["history"][i]["content"]]
        assert len(hits) == 1, f"{day['date']}: the first update is found {len(hits)} times"
        pos = re.findall(r"Your position: ([+-]?[\d,]+) oz", career["history"][hits[0]]["content"])
        out.append({"kind": "opening", "date": day["date"], "history_index": hits[0], "wants": None, "chat": None,
                    "position": float(pos[-1].replace(",", "")) if pos else 0.0})
    return out


def work_items(folder, moments, sign):
    """Every moment to steer, sorted: B's neutral careers at their requests and trading-day openings, and its loss and
    loss + you careers at their requests."""
    import glob
    items = []
    for m in moments(folder, "B"):
        group = "neutral" if m["version"] == "neutral" else "loss" if m["version"] in ("loss", "loss + you") else None
        if group:
            items.append({"group": group, "kind": "request", "version": m["version"], "run": m["run"],
                          "career_file": m["career_file"], "history_index": m["history_index"], "date": m["date"],
                          "chat": m["chat"], "wants": m["wants"], "position": m["held_their_way"] * sign[m["wants"]],
                          "saved_joined": m["joined"]})
    for path in sorted(glob.glob(os.path.join(folder, "careers", "*.json"))):
        career = json.load(open(path))
        if career["version"] != "neutral":
            continue
        days = [json.load(open(d)) for d in sorted(glob.glob(path.replace("/careers/", "/days/")[:-5] + "_2011-*.json"))]
        for o in openings(career, days):
            items.append({**o, "group": "neutral", "version": "neutral", "run": career["run"],
                          "career_file": os.path.basename(path), "saved_joined": None})
    return sorted(items, key=lambda x: (x["career_file"], x["history_index"]))


def run_item(model, tok, steers, dirs, item, career, opening, lead, grid, done=(), samples=SAMPLES):
    """Every condition at one moment: the history before the moment's update is read once, unsteered; each condition then
    steers from the update on (the update, the fixed reasoning line and the order). Yields one row per condition."""
    import torch
    from interventions import goes_along, order_dist, prefill, sample, split_point, summarise_orders
    full, k = split_point(tok, career, item["history_index"], opening)
    for s in steers.values():
        s.vec = None
    cache = None
    for name, layer, which, sign, strength, sampled in conditions(item["group"], item["kind"]):
        key = f"{item['career_file']}|{item['history_index']}|{name}"
        if key in done:
            continue
        if cache is None:
            cache = prefill(model, full[:k])
        d = dirs[layer or LAYER][half_for(item["run"])]
        vec = vector(d, which, sign, strength)
        if vec is not None:
            steers[layer].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
        try:
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            summary = summarise_orders(orders, probs, item["position"], item["wants"])
            replies = sample(model, full, cache, samples, tok=tok) if sampled else []
        finally:
            for s in steers.values():
                s.vec = None
        judged = [goes_along(r, item["position"], item["wants"]) for r in replies]      # replies: requests only
        yield {"key": key, **{f: item[f] for f in ("group", "kind", "version", "run", "career_file", "history_index",
                                                    "date", "chat", "wants", "position", "saved_joined")},
               "condition": name, "layer": layer, "which": which, "sign": sign, "strength": strength,
               "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "coverage": cover,
               "orders": orders, "probs": probs, **summary, "along": [a for a, _ in judged],
               "status": [s for _, s in judged], "replies": replies, "tokens": len(full)}
