"""Are the decision features the whole difference between going along and holding, or the part the dictionary shows?
(the author's question, 13 Nov). CPU, Run 1's saved request states, asked moments only, layers 24 / 31 / 41.

    python features_vs_state.py <states dir> <dir with L24/L31/L41.safetensors> <decision_features.json> <out json>

1. The difference vector: the state where the agent went along minus where it held, averaged within request, experiment
   and framing (as the features were found). How much of that vector's squared size is reproduced by (a) the whole
   Gemma Scope dictionary (all 16k features, decoded), (b) the decision features alone (q < 0.05), (c) the ones that
   replicate. Share = 1 - |difference - reproduced difference|^2 / |difference|^2. With and without dimension 2339.
2. Reading going along: the frozen monitor's recipe (logistic, each input scaled by its within-cell spread on the
   training careers; 5 folds by career) on (a) the whole state, (b) every dictionary feature on in at least 5% of the
   moments, (c) the decision features only, chosen again inside each training fold (the k largest standardised
   differences, k = the number found at that layer), (d) what the dictionary leaves out (state minus its rebuild).
   Scored within cell and within request (AUROC pooled by pair count), careers resampled for intervals. C over
   0.001 / 0.01 / 0.1 / 1; every value is saved, the best per input is printed.
"""
import glob, json, os, sys
import numpy as np
from safetensors.numpy import load_file
from sklearn.linear_model import LogisticRegression

STATES, SAEDIR, DEC, OUT = sys.argv[1:5]
LAYERS, DROP, CS = [24, 31, 41], 2339, [0.001, 0.01, 0.1, 1.0]
dec = json.load(open(DEC))
META, X = [], []
for d in sorted(glob.glob(os.path.join(STATES, "*_bf16"))):
    for f in sorted(glob.glob(os.path.join(d, "*.npz"))):
        z = np.load(f)
        ms = json.loads(str(z["meta"]))
        keep = [i for i, m in enumerate(ms) if m.get("asked", True)]
        META += [ms[i] for i in keep]
        X.append(z["states"][keep][:, LAYERS].astype(np.float32))
X = np.concatenate(X)
y = np.array([int(m["joined"]) for m in META])
REQ = np.array([m["chat"] for m in META])
CELL = np.array([f"{m['chat']}|{m['experiment']}|{m['version']}" for m in META])
CAR = np.array([f"{m['experiment']}|{m['version']}|{m['run']}" for m in META])
print(len(y), "asked moments,", int(y.sum()), "went along", flush=True)
rng = np.random.default_rng(20261113)
cars = rng.permutation(np.unique(CAR))
FOLD = np.zeros(len(y), int)
for k in range(5):
    FOLD[np.isin(CAR, cars[k::5])] = k


def cell_diff(V, rows=None):
    """Went along minus held, averaged over cells with at least 2 of each (weights: the smaller group)."""
    rows = np.arange(len(y)) if rows is None else rows
    num, wsum, var = 0.0, 0.0, 0.0
    for c in np.unique(CELL[rows]):
        r = rows[CELL[rows] == c]
        a, b = r[y[r] == 1], r[y[r] == 0]
        if len(a) < 2 or len(b) < 2:
            continue
        w = min(len(a), len(b))
        num = num + w * (V[a].mean(0) - V[b].mean(0))
        var = var + w * np.concatenate([V[a] - V[a].mean(0), V[b] - V[b].mean(0)]).var(0)
        wsum += w
    return num / wsum, num / wsum / np.sqrt(var / wsum + 1e-6)


def auc(s, t):
    pos, neg = s[t == 1], s[t == 0]
    r = np.argsort(np.argsort(np.r_[pos, neg])) + 1.0
    return (r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / len(pos) / len(neg)


def within(s, t, g):
    num = den = 0.0
    for r in np.unique(g):
        m = g == r
        npos, nneg = t[m].sum(), (1 - t[m]).sum()
        if npos and nneg:
            num += auc(s[m], t[m]) * npos * nneg
            den += npos * nneg
    return num / den


def oof(V, C, k_select=None):
    """Out-of-fold scores; with k_select, the k features with the largest standardised difference on the training rows."""
    s = np.zeros(len(y))
    for k in range(5):
        tr, te = np.where(FOLD != k)[0], np.where(FOLD == k)[0]
        cols = np.arange(V.shape[1])
        if k_select:
            _, zz = cell_diff(V, tr)
            cols = np.argsort(-np.abs(np.nan_to_num(zz)))[:k_select]
        Z = V[tr][:, cols].astype(np.float64)
        mu = Z.mean(0)
        cc = Z.copy()
        for c in np.unique(CELL[tr]):
            m = CELL[tr] == c
            cc[m] -= Z[m].mean(0)
        sc = np.sqrt((cc ** 2).mean(0)) + 1e-6
        clf = LogisticRegression(C=C, max_iter=5000).fit((Z - mu) / sc, y[tr])
        s[te] = clf.decision_function((V[te][:, cols] - mu) / sc)
    return s


def ci(s, g, B=1000):
    u = np.unique(CAR)
    idx = {c: np.where(CAR == c)[0] for c in u}
    out = []
    for _ in range(B):
        p = np.concatenate([idx[c] for c in rng.choice(u, len(u))])
        out.append(within(s[p], y[p], g[p]))
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


out = {"moments": int(len(y)), "went_along": int(y.sum()), "layers": {}}
for li, L in enumerate(LAYERS):
    p = {k.lower().replace(".", "_"): v.astype(np.float32) for k, v in load_file(os.path.join(SAEDIR, f"L{L}.safetensors")).items()}
    We, be, th, Wd, bd = p["w_enc"], p["b_enc"], p["threshold"], p["w_dec"], p["b_dec"]
    We = We if We.shape[0] == 3840 else We.T
    Wd = Wd if Wd.shape[1] == 3840 else Wd.T
    S = X[:, li]
    pre = S @ We + be
    F = np.where(pre > th, pre, 0.0).astype(np.float32)
    rebuilt = F @ Wd + bd
    left = S - rebuilt
    rows = dec["layers"][str(L)]["rows"]
    d_ids = [r["feature"] for r in rows]
    r_ids = [r["feature"] for r in rows if r["replicates"]]
    res = {"decision_features": len(d_ids), "replicating": len(r_ids)}
    # 1. the difference vector
    d, _ = cell_diff(S.astype(np.float64))
    parts = {"whole dictionary": cell_diff(rebuilt.astype(np.float64))[0],
             "decision features": cell_diff((F[:, d_ids] @ Wd[d_ids]).astype(np.float64))[0],
             "replicating decision features": cell_diff((F[:, r_ids] @ Wd[r_ids]).astype(np.float64))[0]}
    res["difference"] = {}
    for tag, mask in (("without 2339", np.arange(3840) != DROP), ("with 2339", np.ones(3840, bool))):
        dd = d[mask]
        res["difference"][tag] = {"size": float(np.linalg.norm(dd)), **{
            k: {"share": float(1 - ((dd - v[mask]) ** 2).sum() / (dd ** 2).sum()),
                "cosine": float(dd @ v[mask] / (np.linalg.norm(dd) * np.linalg.norm(v[mask]) + 1e-12))} for k, v in parts.items()}}
    res["dim2339_share_of_difference"] = float(d[DROP] ** 2 / (d ** 2).sum())
    # the same on two halves of the careers: the part of the difference that repeats, and how much of it each set carries
    # (the difference on one half projected on the reproduced difference of the other, over half 1 x half 2; no 2339)
    keep = np.arange(3840) != DROP
    h = [np.where(np.isin(CAR, cars[0::2]))[0], np.where(np.isin(CAR, cars[1::2]))[0]]
    dh = [cell_diff(S.astype(np.float64), r)[0][keep] for r in h]
    base = float(dh[0] @ dh[1])
    res["difference_split_half"] = {"cosine_between_halves": float(base / (np.linalg.norm(dh[0]) * np.linalg.norm(dh[1])))}
    for k, V in (("whole dictionary", rebuilt), ("decision features", F[:, d_ids] @ Wd[d_ids]),
                 ("replicating decision features", F[:, r_ids] @ Wd[r_ids])):
        vh = [cell_diff(V.astype(np.float64), r)[0][keep] for r in h]
        res["difference_split_half"][k] = float((dh[0] @ vh[1] + dh[1] @ vh[0]) / (2 * base))
    # 2. reading going along
    live = (F > 0).mean(0) >= 0.05
    inputs = {"whole state": (S, None), "all dictionary features on in 5%+": (F[:, live], None),
              "decision features, chosen in each training fold": (F[:, live], len(d_ids)),
              "what the dictionary leaves out": (left, None)}
    res["live_features"] = int(live.sum())
    res["readout"] = {}
    scores = {}
    for name, (V, ksel) in inputs.items():
        best = None
        allc = {}
        for C in CS:
            s = oof(V, C, ksel)
            wc, wr = within(s, y, CELL), within(s, y, REQ)
            allc[str(C)] = {"within_cell": float(wc), "within_request": float(wr)}
            if best is None or wc > best[0]:
                best = (wc, wr, C, s)
        res["readout"][name] = {"by_C": allc, "best_C": best[2], "within_cell": float(best[0]),
                                "within_cell_ci": ci(best[3], CELL), "within_request": float(best[1]),
                                "within_request_ci": ci(best[3], REQ)}
        scores[name] = best[3]
        print(L, name, f"within cell {best[0]:.3f} {res['readout'][name]['within_cell_ci']}, within request {best[1]:.3f} (C {best[2]})", flush=True)
    u = np.unique(CAR)
    idx = {c: np.where(CAR == c)[0] for c in u}
    draws = {n: [] for n in scores if n != "whole state"}
    for _ in range(1000):
        pk = np.concatenate([idx[c] for c in rng.choice(u, len(u))])
        w0 = within(scores["whole state"][pk], y[pk], REQ[pk])
        for n in draws:
            draws[n].append(w0 - within(scores[n][pk], y[pk], REQ[pk]))
    for n, v in draws.items():
        res["readout"][n]["whole_state_minus_this_within_request_ci"] = [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
        print(L, "whole state minus", n, [round(x, 3) for x in res["readout"][n]["whole_state_minus_this_within_request_ci"]], flush=True)
    print(L, "split half", json.dumps(res["difference_split_half"]), flush=True)
    print(L, json.dumps(res["difference"]["without 2339"]), "2339 share", round(res["dim2339_share_of_difference"], 3), flush=True)
    out["layers"][str(L)] = res
    json.dump(out, open(OUT, "w"), indent=1)
print("done")
