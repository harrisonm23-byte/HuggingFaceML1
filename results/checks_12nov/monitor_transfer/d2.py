"""D2: does the state monitor learn going along, or something tied to the condition? M2 as frozen (layer 24, logistic,
C = 0.001, each dimension scaled by its within-cell spread on the training rows). Repo letters (repo E = paper F,
repo F = paper E). Transfer measured within request (AUROC inside each of the six requests, pooled by pair count), the
honest measure since the request date alone separates going along. Shuffled-label control: labels permuted within
request among the training rows, model refit, scored on the true test labels.
Usage: python d2.py <states dir> <out json>"""
import glob, json, os, sys
import numpy as np
from sklearn.linear_model import LogisticRegression
STATES, OUT = sys.argv[1:3]
L, C, NSHUF = 24, 0.001, int(os.environ.get("NSHUF", 50))
X, y, EXP, VER, REQ, CAR = [], [], [], [], [], []
for p in sorted(glob.glob(os.path.join(STATES, "*_bf16", "*.npz"))):
    e = os.path.basename(os.path.dirname(p))[:-5]
    z = np.load(p)
    for i, m in enumerate(json.loads(str(z["meta"]))):
        if m.get("asked", True):
            X.append(z["states"][i, L].astype(np.float32)); y.append(int(m["joined"])); EXP.append(e)
            VER.append(m["version"]); REQ.append(m["chat"]); CAR.append(f"{e}|{os.path.basename(p)}")
X, y, EXP, VER, REQ, CAR = map(np.array, (X, y, EXP, VER, REQ, CAR))
CELL = np.array([f"{a}|{b}|{c}" for a, b, c in zip(EXP, VER, REQ)])
print("requests", len(y), "went along", int(y.sum()), {e: int(y[EXP == e].sum()) for e in np.unique(EXP)})
def auc(s, t):
    pos, neg = s[t == 1], s[t == 0]
    if not len(pos) or not len(neg):
        return np.nan
    r = np.argsort(np.argsort(np.r_[pos, neg])) + 1.0
    return (r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / len(pos) / len(neg)
def within(s, t, req):
    num = den = 0.0
    for r in np.unique(req):
        m = req == r; npos, nneg = t[m].sum(), (1 - t[m]).sum()
        if npos and nneg:
            num += auc(s[m], t[m]) * npos * nneg; den += npos * nneg
    return num / den if den else np.nan
def fit(tr, labels):
    mu = X[tr].mean(0)
    Z = X[tr].astype(np.float64); c = CELL[tr]
    cc = Z.copy()
    for k in np.unique(c):
        m = c == k; cc[m] -= Z[m].mean(0)
    sc = np.sqrt((cc ** 2).mean(0)) + 1e-6
    clf = LogisticRegression(C=C, max_iter=3000).fit((Z - mu) / sc, labels)
    return lambda te: clf.decision_function((X[te] - mu) / sc)
rng = np.random.default_rng(20261112)
def career_ci(s, te, B=1000):
    cars = np.unique(CAR[te]); idx = {c: np.where(CAR[te] == c)[0] for c in cars}; out = []
    for _ in range(B):
        pick = np.concatenate([idx[c] for c in rng.choice(cars, len(cars))])
        out.append(within(s[pick], y[te][pick], REQ[te][pick]))
    return [float(np.nanpercentile(out, 2.5)), float(np.nanpercentile(out, 97.5))]
def test(name, trm, tem):
    tr, te = np.where(trm)[0], np.where(tem)[0]
    s = fit(tr, y[tr])(te)
    w = within(s, y[te], REQ[te]); pooled = auc(s, y[te])
    j7 = REQ[te] == "p344_i_can_hunt_with_u"; a7 = auc(s[j7], y[te][j7])
    null = []
    for k in range(NSHUF):
        lab = y[tr].copy()
        for r in np.unique(REQ[tr]):
            m = np.where(REQ[tr] == r)[0]; lab[m] = lab[rng.permutation(m)]
        null.append(within(fit(tr, lab)(te), y[te], REQ[te]))
    res = {"train": int(len(tr)), "test": int(len(te)), "test_went": int(y[te].sum()), "pooled_auc": float(pooled),
           "within_request_auc": float(w), "within_ci": career_ci(s, te), "auc_7jan": float(a7),
           "shuffled_within": [float(np.percentile(null, q)) for q in (50, 95)], "shuffled_max": float(np.max(null)),
           "p_vs_shuffled": float((np.sum(np.array(null) >= w) + 1) / (len(null) + 1))}
    print(f"{name}: within {w:.3f} {res['within_ci']}, 7 Jan {a7:.3f}, pooled {pooled:.3f}; shuffled median "
          f"{res['shuffled_within'][0]:.3f}, 95th {res['shuffled_within'][1]:.3f}", flush=True)
    return res
out = {}
for e in ["A", "C", "C2", "D", "E", "F"]:
    out[f"B -> {e}"] = test(f"B -> {e}", EXP == "B", EXP == e)
for ex in [("B",), ("B", "F")]:          # repo F = paper E, the same framings plus Bank C
    m = np.isin(EXP, ex)
    out[f"{'+'.join(ex)}: loss+neutral -> blame+credit"] = test(f"{'+'.join(ex)}: loss+neutral -> blame+credit",
        m & np.isin(VER, ["neutral", "loss"]), m & np.isin(VER, ["loss + you", "gain + you"]))
    out[f"{'+'.join(ex)}: neutral+loss+gain -> blame+credit"] = test(f"{'+'.join(ex)}: neutral+loss+gain -> blame+credit",
        m & np.isin(VER, ["neutral", "loss", "gain"]), m & np.isin(VER, ["loss + you", "gain + you"]))
json.dump(out, open(OUT, "w"), indent=1)
