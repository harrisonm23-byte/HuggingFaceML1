"""Phase II, Section 5.1.3: name the decision features (the author, 13 Nov). CPU, saved states only.

    python decision_features.py <states dir: v2 mirror with {A..F}_bf16 and *_bf16_steps> <dir with L24/L31/L41.safetensors> <out dir>

A. Every Gemma Scope 2 feature (16k, residual stream) with q < 0.05 for went along vs held, within request, experiment
   and framing (the comparison of results/inside_full_career, same code, same seeds), at layers 24, 31, 41. For each:
   raw means, the within-cell difference in spread units, the half split (found on half the careers, confirmed on the
   other: same sign and p < 0.05), whether it separates UBS's loss from gain frame in B (q < 0.05, within request), and
   the went-along difference inside each request date on its own.
B. The four features that differ between the financial loss and gain documents (layer 24): the same columns.
C. For features that replicate: the same comparison at the update states 15 and 30 minutes before the request
   (history index - 2, - 4) and at the request update itself (A, B, D, E, F: the experiments with every-update states).
Top moments: the three request moments with the highest activation, with the agent's reply as the snippet.
Experiment letters are the paper's (repo E = paper F, repo F = paper E).
"""
import glob, json, os, sys
import numpy as np
from safetensors.numpy import load_file

STATES, SAEDIR, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
LAYERS = [24, 31, 41]
FIN = {24: [11564, 9245, 4376, 2367]}
PERMS = 1000
PAPER = {"E": "F", "F": "E"}
NP = "https://www.neuronpedia.org/gemma-3-12b-it/{}-gemmascope-2-res-16k/{}"


def load_sae(path, width=3840):
    p = {k.lower().replace(".", "_"): v.astype(np.float32) for k, v in load_file(path).items()}
    We, b, t, Wd = p["w_enc"], p["b_enc"], p["threshold"], p["w_dec"]
    We = We if We.shape[0] == width else We.T
    Wd = Wd if Wd.shape[1] == width else Wd.T
    return We, b, t, Wd


def encode(x, sae):
    pre = x @ sae[0] + sae[1]
    return np.where(pre > sae[2], pre, 0.0).astype(np.float32)


# ---- request states (all experiments), layers 24/31/41 only
META, X = [], []
for d in sorted(glob.glob(os.path.join(STATES, "*_bf16"))):
    for f in sorted(glob.glob(os.path.join(d, "*.npz"))):
        z = np.load(f)
        META += json.loads(str(z["meta"]))
        X.append(z["states"][:, LAYERS].astype(np.float32))
X = np.concatenate(X)
N = len(META)
REQ = np.array([m["chat"] for m in META]); EXP = np.array([m["experiment"] for m in META])
VER = np.array([m["version"] for m in META]); JOINED = np.array([m["joined"] for m in META])
ASKED = np.array([m.get("asked", True) for m in META])
CAREER = np.array([f"{m['experiment']}|{m['version']}|{m['run']}" for m in META])
CELL = np.array([f"{m['chat']}|{m['experiment']}|{m['version']}" for m in META])
HALF1 = np.isin(CAREER, np.random.default_rng(5).permutation(np.unique(CAREER))[::2])
print(N, "moments", flush=True)


def strat_diff(F, a, b, S):
    num, wsum, var = np.zeros(F.shape[1]), 0.0, np.zeros(F.shape[1])
    for r in np.unique(S[a | b]):
        ia, ib = a & (S == r), b & (S == r)
        if ia.sum() < 2 or ib.sum() < 2:
            continue
        w = min(ia.sum(), ib.sum())
        num += w * (F[ia].mean(0) - F[ib].mean(0))
        var += w * np.concatenate([F[ia] - F[ia].mean(0), F[ib] - F[ib].mean(0)]).var(0)
        wsum += w
    if wsum == 0:
        return np.full(F.shape[1], np.nan), np.full(F.shape[1], np.nan)
    return num / wsum, num / wsum / np.sqrt(var / wsum + 1e-6)


def strat_perm(F, a, b, S, rng):
    _, obs = strat_diff(F, a, b, S)
    both, hits = a | b, np.zeros(F.shape[1])
    groups = [(np.where(both & (S == r))[0], int((a & (S == r)).sum())) for r in np.unique(S[both])]
    for _ in range(PERMS):
        a2 = np.zeros(len(a), bool)
        for idx, k in groups:
            a2[rng.permutation(idx)[:k]] = True
        _, s = strat_diff(F, a2, both & ~a2, S)
        hits += np.abs(s) >= np.abs(obs) - 1e-12
    return obs, (hits + 1) / (PERMS + 1)


def fdr(p):
    order, q, run = np.argsort(p), np.empty_like(p), 1.0
    for i in range(len(p) - 1, -1, -1):
        run = min(run, p[order[i]] * len(p) / (i + 1))
        q[order[i]] = run
    return q


a_all, b_all = ASKED & JOINED, ASKED & ~JOINED
isB = EXP == "B"
LOSS, GAIN = isB & np.isin(VER, ["loss", "loss + you"]), isB & np.isin(VER, ["gain", "gain + you"])
DATES = sorted(set(REQ), key=lambda c: min(m["history_index"] for m in META if m["chat"] == c))
DATE_OF = {c: next(m["date"] for m in META if m["chat"] == c) for c in DATES}

# ---- every-update states (for C)
STEP = {}
for d in sorted(glob.glob(os.path.join(STATES, "*_bf16_steps"))):
    for f in sorted(glob.glob(os.path.join(d, "*.npz"))):
        z = np.load(f)
        lay = list(z["layers"])
        ms = json.loads(str(z["meta"]))
        st = z["states"][:, [lay.index(L) for L in LAYERS]].astype(np.float32)
        for i, m in enumerate(ms):
            STEP[(m["experiment"], m["version"], m["run"], m["history_index"])] = st[i]

out = {"moments": N, "layers": {}, "financial": {}, "timing": {}}
for li, L in enumerate(LAYERS):
    sae = load_sae(os.path.join(SAEDIR, f"L{L}.safetensors"))
    F = encode(X[:, li], sae)
    rng = np.random.default_rng(20261019 + L)
    live = (F[a_all | b_all] > 0).mean(0) >= 0.05
    ids = np.where(live)[0]
    _, p = strat_perm(F[:, live], a_all, b_all, CELL, rng)
    q = fdr(p)
    # framing: B loss vs gain, within request, on the features live in B
    liveB = (F[LOSS | GAIN] > 0).mean(0) >= 0.05
    _, pB = strat_perm(F[:, liveB], LOSS, GAIN, REQ, rng)
    qB_full = np.full(F.shape[1], np.nan); qB_full[liveB] = fdr(pB)
    zB_full = np.full(F.shape[1], np.nan); zB_full[liveB] = strat_diff(F[:, liveB], LOSS, GAIN, REQ)[1]
    pick = list(ids[q < 0.05]) + [f for f in FIN.get(L, []) if f not in ids[q < 0.05]]
    G = F[:, pick]
    raw, z = strat_diff(G, a_all, b_all, CELL)
    _, z1 = strat_diff(G, a_all & HALF1, b_all & HALF1, CELL)
    _, z2 = strat_diff(G, a_all & ~HALF1, b_all & ~HALF1, CELL)
    _, p2 = strat_perm(G, a_all & ~HALF1, b_all & ~HALF1, CELL, rng)
    per_date = {}
    for c in DATES:
        inc = REQ == c
        _, zd = strat_diff(G, a_all & inc, b_all & inc, CELL)
        _, pd = strat_perm(G, a_all & inc, b_all & inc, CELL, rng)
        per_date[f"{DATE_OF[c]} {c.split('_')[0]}"] = (zd, pd, int((a_all & inc).sum()), int((b_all & inc).sum()))
    rows = []
    for j, f in enumerate(pick):
        top = np.argsort(-G[:, j])[:3]
        k = np.where(ids == f)[0]
        rows.append({
            "layer": L, "feature": int(f), "neuronpedia": NP.format(L, f),
            "decision_q": float(q[k[0]]) if len(k) else None, "decision_p": float(p[k[0]]) if len(k) else None,
            "mean_went_along": float(G[a_all, j].mean()), "mean_held": float(G[b_all, j].mean()),
            "share_on_went_along": float((G[a_all, j] > 0).mean()), "share_on_held": float((G[b_all, j] > 0).mean()),
            "within_cell_difference": float(raw[j]), "effect_spread_units": float(z[j]),
            "half1": float(z1[j]), "half2": float(z2[j]), "half2_p": float(p2[j]),
            "replicates": bool(np.sign(z1[j]) == np.sign(z2[j]) and p2[j] < 0.05),
            "framing_loss_vs_gain_q": None if np.isnan(qB_full[f]) else float(qB_full[f]),
            "framing_loss_vs_gain_z": None if np.isnan(zB_full[f]) else float(zB_full[f]),
            "by_date": {d: {"z": None if np.isnan(v[0][j]) else float(v[0][j]),
                            "p": None if np.isnan(v[0][j]) else float(v[1][j]),
                            "n": [v[2], v[3]]} for d, v in per_date.items()},
            "top_moments": [{"activation": float(G[i, j]), "date": META[i]["date"],
                             "experiment": PAPER.get(EXP[i], EXP[i]), "framing": VER[i], "went_along": bool(JOINED[i]),
                             "asked": bool(ASKED[i]), "reply": META[i]["reply"][:220]} for i in top],
        })
    out["layers"][str(L)] = {"features_tested": int(live.sum()), "q_below_0.05": int((q < 0.05).sum()),
                             "framing_features_tested": int(liveB.sum()), "framing_q_below_0.05": int((qB_full < 0.05).sum()),
                             "rows": [r for r in rows if r["decision_q"] is not None and r["decision_q"] < 0.05]}
    if FIN.get(L):                                        # the financial features at every saved update, not only requests
        allst = np.stack([v[li] for v in STEP.values()])
        Fa = encode(allst, sae)[:, FIN[L]]
        fin_steps = {"updates": int(len(allst)), "share_on": {str(f): float((Fa[:, k] > 0).mean()) for k, f in enumerate(FIN[L])},
                     "max": {str(f): float(Fa[:, k].max()) for k, f in enumerate(FIN[L])}}
        del allst, Fa
    for r in rows:
        if r["feature"] in FIN.get(L, []):
            r["every_update"] = {"updates": fin_steps["updates"], "share_on": fin_steps["share_on"][str(r["feature"])],
                                 "max": fin_steps["max"][str(r["feature"])]}
            out["financial"][str(r["feature"])] = r
    # ---- C: timing, replicating decision features + financial ones
    tf = [j for j, r in enumerate(rows) if r["replicates"] or r["feature"] in FIN.get(L, [])]
    keep = [i for i, m in enumerate(META) if m.get("asked", True) and
            all((m["experiment"], m["version"], m["run"], m["history_index"] - s) in STEP for s in (0, 2, 4))]
    keep = np.array(keep)
    if len(keep):
        lab_a, lab_b = JOINED[keep], ~JOINED[keep]
        cos = []
        timing = {}
        for s, name in ((4, "30 min before"), (2, "15 min before"), (0, "request update")):
            Xs = np.stack([STEP[(META[i]["experiment"], META[i]["version"], META[i]["run"], META[i]["history_index"] - s)][li] for i in keep])
            if s == 0:
                u, v = Xs, X[keep, li]
                cos = (u * v).sum(1) / (np.linalg.norm(u, axis=1) * np.linalg.norm(v, axis=1))
            Gs = encode(Xs, sae)[:, [pick[j] for j in tf]]
            _, zs = strat_diff(Gs, lab_a, lab_b, CELL[keep])
            _, ps = strat_perm(Gs, lab_a, lab_b, CELL[keep], rng)
            timing[name] = {str(pick[j]): {"z": float(zs[t]), "p": float(ps[t]), "mean_went_along": float(Gs[lab_a, t].mean()),
                                            "mean_held": float(Gs[lab_b, t].mean())} for t, j in enumerate(tf)}
        _, zr = strat_diff(F[keep][:, [pick[j] for j in tf]], lab_a, lab_b, CELL[keep])
        timing["request moment (same moments)"] = {str(pick[j]): {"z": float(zr[t])} for t, j in enumerate(tf)}
        out["timing"][str(L)] = {"moments": int(len(keep)), "went_along": int(lab_a.sum()),
                                 "experiments": sorted({PAPER.get(EXP[i], EXP[i]) for i in keep}),
                                 "request_update_vs_request_state_cosine_median": float(np.median(cos)),
                                 "request_update_vs_request_state_cosine_min": float(np.min(cos)), "features": timing}
    print(L, out["layers"][str(L)]["q_below_0.05"], "decision features;", sum(r["replicates"] for r in out["layers"][str(L)]["rows"]), "replicate", flush=True)
    json.dump(out, open(os.path.join(OUT, "decision_features.json"), "w"), indent=1)
    del F, G
print("done")
