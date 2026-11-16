"""The four frames' layer-24 features (section H): do they replicate, and do they go with going along? (the author, 16 Nov)
CPU, saved states only.

    python frame_features.py <states dir: v2 mirror with matched/B_bf16 and {A..F}_bf16> <dir with L24.safetensors> <out dir>

1. Replication. Section H's layer-24 features (top 15 per comparison in results/matched/matched.json: loss vs gain,
   "you" after loss = blame, "you" after gain = credit) came from all of B's matched moments (history held fixed, the
   same moment read with only UBS's wording changed). Here B's careers are split in half (fixed seed) and each feature
   is tested in each half on its own, exactly as matched_history.py tests it (paired within moment, signs flipped by
   career). A feature replicates if it has section H's sign and p < 0.05 in both halves.
2. The check, with the replicating features only. A frame score per state: the replicating features of that frame,
   each divided by its spread, signed so that higher = more of the frame, averaged.
   a. Run 1, the real decisions: among agents given the same frame at the request (loss, gain, loss + you = blame,
      gain + you = credit; every experiment), went along vs held on that frame's score, within request x experiment
      x framing; p by reshuffling the labels within those cells.
   b. Same moment (B, matched): does a larger response to the frame (score in the framed version minus the comparison
      version) go with a larger change in P(goes along) (log-odds, same two versions)? Rank correlation within request,
      pooled by moments; p by shuffling within request.
Experiment letters are the paper's (repo E = paper F, repo F = paper E).
"""
import glob, json, os, sys
import numpy as np
from scipy.stats import rankdata
from safetensors.numpy import load_file

STATES, SAEDIR, OUT = sys.argv[1:4]
L = 24
PERMS = 10000
PAPER = {"E": "F", "F": "E"}
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
fi = {v: i for i, v in enumerate(FRAMINGS)}
SECTION_H = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "matched", "matched.json")))["features"]
COMP = {"loss vs gain": "Request: loss frame vs gain frame", "blame": "\"You\" after loss: loss + you vs loss",
        "credit": "\"You\" after gain: gain + you vs gain"}


def load_sae(path, width=3840):
    p = {k.lower().replace(".", "_"): v.astype(np.float32) for k, v in load_file(path).items()}
    We, b, t = p["w_enc"], p["b_enc"], p["threshold"]
    return (We if We.shape[0] == width else We.T), b, t


def encode(x, sae):
    pre = x @ sae[0] + sae[1]
    return np.where(pre > sae[2], pre, 0.0).astype(np.float32)


sae = load_sae(os.path.join(SAEDIR, f"L{L}.safetensors"))
logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))

# ---------------- matched B (as matched_history.py loads it: moments x 5 framings x Bank C; scored orders cover >= 50%)
rows, S = [], []
for f in sorted(glob.glob(os.path.join(STATES, "matched", "B_bf16", "*.npz"))):
    z = np.load(f)
    r = json.loads(str(z["meta"]))
    assert [(x["framing"], x["bank_c"]) for x in r] == [(v, b) for v in FRAMINGS for b in (False, True)]
    rows.append(r)
    S.append(z["states"][:, list(z["layers"]).index(L)].reshape(len(FRAMINGS), 2, -1)[:, 0])   # no Bank C line
S = np.stack(S)
keep = np.array([r[0]["coverage"] >= 0.5 for r in rows])
rows, S = [r for r, k in zip(rows, keep) if k], S[keep]
M = len(rows)
CAREER = np.array([r[0]["career_file"] for r in rows])
CHAT = np.array([r[0]["chat"] for r in rows])
P = np.array([[r[2 * i]["p_order_along"] for i in range(len(FRAMINGS))] for r in rows])
Fz = encode(S.reshape(-1, S.shape[-1]), sae).reshape(M, len(FRAMINGS), -1)
careers = np.unique(CAREER)
half_a = set(np.random.default_rng(5).permutation(careers)[::2])
HALF = np.array([c in half_a for c in CAREER])
rng = np.random.default_rng(20261116)
print(M, "matched moments,", len(careers), "careers;", HALF.sum(), "moments in half 1", flush=True)

diffs = {"loss vs gain": Fz[:, [fi["loss"], fi["loss + you"]]].mean(1) - Fz[:, [fi["gain"], fi["gain + you"]]].mean(1),
         "blame": Fz[:, fi["loss + you"]] - Fz[:, fi["loss"]],
         "credit": Fz[:, fi["gain + you"]] - Fz[:, fi["gain"]]}


def paired(D, mask):
    """Per-feature mean of D over careers in mask (spread units, as matched_history.py) and p by flipping signs by career."""
    cs = np.unique(CAREER[mask])
    C = np.stack([D[mask & (CAREER == c)].mean(0) for c in cs])
    obs = C.mean(0)
    hits = np.zeros(D.shape[1])
    for _ in range(PERMS):
        hits += np.abs(rng.choice([-1, 1], len(cs)) @ C / len(cs)) >= np.abs(obs) - 1e-12
    return obs / (D[mask].std(0) + 1e-6), (hits + 1) / (PERMS + 1)


out = {"matched_moments": M, "careers": len(careers), "replication": {}, "run1": {}, "same_moment": {}}
REPL = {}
for k, name in COMP.items():
    top = SECTION_H[name][str(L)]["top"]
    ids = [t["feature"] for t in top]
    sign = np.sign([t["standardised_difference"] for t in top])
    D = diffs[k][:, ids]
    z1, p1 = paired(D, HALF)
    z2, p2 = paired(D, ~HALF)
    rep = (np.sign(z1) == sign) & (np.sign(z2) == sign) & (p1 < 0.05) & (p2 < 0.05)
    out["replication"][k] = [{"feature": f, "section_h": t["standardised_difference"], "half1": float(a), "p_half1": float(pa),
                              "half2": float(b), "p_half2": float(pb), "replicates": bool(r)}
                             for f, t, a, pa, b, pb, r in zip(ids, top, z1, p1, z2, p2, rep)]
    REPL[k] = [(f, s) for f, s, r in zip(ids, sign, rep) if r]
    print(k, f"{rep.sum()} of {len(ids)} replicate", flush=True)

# the four frames: the replicating features, signed so higher = more of the frame
FRAMES = {"loss": [(f, s) for f, s in REPL["loss vs gain"] if s > 0],
          "gain": [(f, -s) for f, s in REPL["loss vs gain"] if s < 0],
          "blame": REPL["blame"], "credit": REPL["credit"]}

# ---------------- Run 1: the real decisions
META, X = [], []
for d in sorted(glob.glob(os.path.join(STATES, "*_bf16"))):
    for f in sorted(glob.glob(os.path.join(d, "*.npz"))):
        z = np.load(f)
        META += json.loads(str(z["meta"]))
        X.append(z["states"][:, L].astype(np.float32))
F1 = encode(np.concatenate(X), sae)
VER = np.array([m["version"] for m in META])
JOINED = np.array([bool(m["joined"]) for m in META])
ASKED = np.array([m.get("asked", True) for m in META])
CELL = np.array([f"{m['chat']}|{m['experiment']}|{m['version']}" for m in META])
EXP = np.array([PAPER.get(m["experiment"], m["experiment"]) for m in META])
SPREAD = F1[ASKED].std(0) + 1e-6
VERSION_OF = {"loss": "loss", "gain": "gain", "blame": "loss + you", "credit": "gain + you"}


def score(F, feats, spread):
    return np.mean([s * F[..., f] / spread[f] for f, s in feats], 0) if feats else None


def cell_diff(x, a, b, cells):
    num, w, var = 0.0, 0.0, 0.0
    for c in np.unique(cells[a | b]):
        ia, ib = a & (cells == c), b & (cells == c)
        if ia.sum() < 2 or ib.sum() < 2:
            continue
        n = min(ia.sum(), ib.sum())
        num += n * (x[ia].mean() - x[ib].mean())
        var += n * np.concatenate([x[ia] - x[ia].mean(), x[ib] - x[ib].mean()]).var()
        w += n
    return num / w / np.sqrt(var / w + 1e-12) if w else np.nan


for k, feats in FRAMES.items():
    sel = ASKED & (VER == VERSION_OF[k])
    x = score(F1, feats, SPREAD)
    if x is None:
        out["run1"][k] = None
        continue
    a, b = sel & JOINED, sel & ~JOINED
    obs = cell_diff(x, a, b, CELL)
    groups = [(np.where(sel & (CELL == c))[0], int((a & (CELL == c)).sum())) for c in np.unique(CELL[sel])]
    hits = 0
    for _ in range(PERMS // 10):
        a2 = np.zeros(len(a), bool)
        for idx, n in groups:
            a2[rng.permutation(idx)[:n]] = True
        hits += abs(cell_diff(x, a2, sel & ~a2, CELL)) >= abs(obs) - 1e-12
    used = [c for c in np.unique(CELL[sel]) if (a & (CELL == c)).sum() >= 2 and (b & (CELL == c)).sum() >= 2]
    out["run1"][k] = {"features": [int(f) for f, _ in feats], "went_along": int(a.sum()), "held": int(b.sum()),
                      "went_along_in_compared_cells": int(sum((a & (CELL == c)).sum() for c in used)),
                      "held_in_compared_cells": int(sum((b & (CELL == c)).sum() for c in used)),
                      "requests_compared": sorted({c.split("|")[0] for c in used}),
                      "experiments": sorted(set(EXP[sel])),
                      "difference_spread_units": float(obs), "p": float((hits + 1) / (PERMS // 10 + 1))}
    print("run1", k, out["run1"][k]["difference_spread_units"], out["run1"][k]["p"], flush=True)

# ---------------- same moment (matched B): bigger response to the frame vs bigger change in P(goes along)
SPREAD_M = Fz.reshape(-1, Fz.shape[-1]).std(0) + 1e-6
PAIRS = {"loss": (["loss", "loss + you"], ["gain", "gain + you"]), "gain": (["gain", "gain + you"], ["loss", "loss + you"]),
         "blame": (["loss + you"], ["loss"]), "credit": (["gain + you"], ["gain"])}
LP = logit(P)
for k, feats in FRAMES.items():
    if not feats:
        out["same_moment"][k] = None
        continue
    hi, lo = [fi[v] for v in PAIRS[k][0]], [fi[v] for v in PAIRS[k][1]]
    resp = score(Fz[:, hi], feats, SPREAD_M).mean(1) - score(Fz[:, lo], feats, SPREAD_M).mean(1)
    dP = LP[:, hi].mean(1) - LP[:, lo].mean(1)
    reqs = [np.where(CHAT == c)[0] for c in np.unique(CHAT)]

    def rho(r):
        num = sum(len(i) * np.corrcoef(rankdata(r[i]), rankdata(dP[i]))[0, 1] for i in reqs if len(i) > 3)
        return num / sum(len(i) for i in reqs if len(i) > 3)
    obs = rho(resp)
    hits = 0
    for _ in range(PERMS):
        r2 = resp.copy()
        for i in reqs:
            r2[i] = rng.permutation(r2[i])
        hits += abs(rho(r2)) >= abs(obs) - 1e-12
    out["same_moment"][k] = {"rank_correlation": float(obs), "p": float((hits + 1) / (PERMS + 1)), "moments": M,
                             "mean_response": float(resp.mean()), "mean_change_log_odds": float(dP.mean())}
    print("same moment", k, obs, out["same_moment"][k]["p"], flush=True)

json.dump(out, open(os.path.join(OUT, "frame_features.json"), "w"), indent=1)
print("done")
