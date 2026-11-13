"""State monitor, Phase 1, Steps 1-4, as preregistered (designs/rd2/PREREG_MONITOR.md, committed before this ran).

    python designs/rd2/analysis/monitor_phase1.py <folder holding the downloaded <exp>_bf16 state folders>

Read point 1 (the last token before the reply, saved at all 48 layers in rd2-states v2/<exp>_bf16). Unit: the request;
label: the paper's trade measure ("joined"). Monitors built on training careers only:
  M1  difference of means, within cell (experiment x condition x request), harmonic-weighted, on one scale;
  M2  L2 logistic regression on one scale, strength by inner cross-validation.
Baselines: framing-only, request-only, history-only, combined no-state (logistic on the three), words (the existing
blind chat-only labels: AGREES 2, NONCOMMITTAL 1, else 0). Controls: 100 random directions, 100 label shuffles.
Split 1: five folds grouped by career, balanced by going-along requests per experiment (seed 20261105). Split 2: built
on B, tested on each other experiment; each experiment left out in turn. Layer: 12, 18, 22, 24, 30, 36, chosen by inner
cross-validation on the training careers of each outer fold. AUROC on pooled out-of-fold scores, 95% intervals by
resampling careers (2,000). Thresholds for catch and false-alarm rates come from the inner cross-validation scores of
the training careers (never the test fold).
Writes results/monitor_heldout/: SUMMARY.md, summary.json, one CSV per experiment, roc.png, scores.png.
"""
import collections, csv, glob, json, os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul")   # numpy 2.0 on macOS Accelerate: spurious (checked: results match a plain sum)
from sklearn.linear_model import LogisticRegression

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STATES = sys.argv[1]
OUT = os.path.join(ROOT, "results", "monitor_heldout")
LAYERS = [12, 18, 22, 24, 30, 36]
EXPS = ["A", "B", "C", "C2", "D", "E", "F"]
SEED, BOOT, N_RANDOM, N_SHUFFLE = 20261105, 2000, 100, 100
CS = [1e-4, 1e-3, 1e-2, 1e-1]
JAN7 = "2011-01-07"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(SEED)

# ---------------- the data: every request UBS made, its state at the six layers, its labels
meta, X = [], {L: [] for L in LAYERS}
for e in EXPS:
    for p in sorted(glob.glob(os.path.join(STATES, f"{e}_bf16", "*.npz"))):
        z = np.load(p)
        S = z["states"]
        for i, m in enumerate(json.loads(str(z["meta"]))):
            if not m["asked"]:
                continue
            meta.append({**m, "exp": e})
            for L in LAYERS:
                X[L].append(S[i, L].astype(np.float32))
X = {L: np.stack(v) for L, v in X.items()}
N, W = len(meta), X[LAYERS[0]].shape[1]
y = np.array([int(m["joined"]) for m in meta])
EXP = np.array([m["exp"] for m in meta])
CAREER = np.array([f"{m['exp']}|{m['version']}|{m['run']}" for m in meta])
CELL = np.array([f"{m['exp']}|{m['version']}|{m['chat']}" for m in meta])
FRAME = np.array([f"{m['exp']}|{m['version']}" for m in meta])
REQ = np.array([m["chat"] for m in meta])
DATE = np.array([m["date"] for m in meta])
HIST = np.zeros(N, int)                                   # went along at an earlier request of the same career
for c in np.unique(CAREER):
    idx = sorted(np.where(CAREER == c)[0], key=lambda i: (meta[i]["date"], meta[i]["history_index"]))
    seen = False
    for i in idx:
        HIST[i] = int(seen)
        seen = seen or bool(y[i])
assert N == 1710 and y.sum() == 286, (N, y.sum())


def label_files(folder):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, "labels_batch_*.json"))):
        out.update({k: v.strip().upper() for k, v in json.load(open(p)).items()})
    return out


SCORE = lambda lab: {"AGREES": 2, "NONCOMMITTAL": 1}.get(lab, 0)
words = {}
key, lab = json.load(open(os.path.join(ROOT, "results/words_all/key.json"))), label_files(os.path.join(ROOT, "results/words_all"))
for k, m in key.items():
    if m["push_request"] and m["experiment"] in EXPS and m["experiment"] != "B":
        words[(m["experiment"], m["version"], m["career_file"], m["push_request"])] = (
            SCORE(lab.get(k) if m["has_chat"] else None), m["traded_along"])
regraded = {m["b_item"]: lab[k] for k, m in key.items() if m["experiment"] == "B" and m["b_item"] and m["has_chat"]}
bkey, blab = json.load(open(os.path.join(ROOT, "results/words_b/key.json"))), label_files(os.path.join(ROOT, "results/words_b"))
for k, m in bkey.items():
    if m.get("push_request"):
        words[("B", m["version"], m["career_file"], m["push_request"])] = (
            SCORE(regraded.get(k, blab.get(k) if m["has_chat"] else None)), m["traded_along"])
WORDS = np.full(N, np.nan)
agree_label = 0
for i, m in enumerate(meta):
    w = words.get((m["exp"], m["version"], m["career_file"], m["chat"]))
    if w is not None:
        WORDS[i] = w[0]
        agree_label += int(bool(w[1]) == bool(y[i]))
HAS_WORDS = ~np.isnan(WORDS)

# ---------------- AUROC (weighted, ties as half) and the career bootstrap
def auc(s, yy, w=None):
    w = np.ones(len(s)) if w is None else w
    o = np.argsort(s, kind="mergesort")
    s, yy, w = s[o], yy[o], w[o]
    _, start = np.unique(s, return_index=True)
    wp, wn = np.add.reduceat(w * yy, start), np.add.reduceat(w * (1 - yy), start)
    below = np.cumsum(wn) - wn
    den = wp.sum() * wn.sum()
    return float((wp * (below + 0.5 * wn)).sum() / den) if den > 0 else float("nan")


def boot_weights(mask, n=BOOT, seed=SEED):
    """Row weights for n career resamples within the rows in `mask`."""
    g = np.random.default_rng(seed)
    cars = np.unique(CAREER[mask])
    pos = {c: i for i, c in enumerate(cars)}
    rows = np.where(mask)[0]
    ci = np.array([pos[c] for c in CAREER[rows]])
    for _ in range(n):
        counts = np.bincount(g.integers(0, len(cars), len(cars)), minlength=len(cars))
        yield rows, counts[ci].astype(float)


def interval(scores, mask, base=None):
    """AUROC (or the difference with `base`) and its 95% career-resampling interval, on the rows in `mask`."""
    yy = y[mask]
    pt = auc(scores[mask], yy) - (auc(base[mask], yy) if base is not None else 0)
    bs = []
    for rows, w in boot_weights(mask):
        v = auc(scores[rows], y[rows], w)
        if base is not None:
            v -= auc(base[rows], y[rows], w)
        bs.append(v)
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return pt, lo, hi


# ---------------- folds, scale, the monitors
def folds_for(rows, k=5, seed=SEED):
    """{row: fold} grouping careers, balanced by going-along requests within each experiment."""
    g = np.random.default_rng(seed)
    out, offset = {}, 0
    for e in EXPS:
        cars = sorted({CAREER[i] for i in rows if EXP[i] == e})
        if not cars:
            continue
        g.shuffle(cars)
        npos = {c: sum(y[i] for i in rows if CAREER[i] == c) for c in cars}
        cars.sort(key=lambda c: -npos[c])                    # stable: the shuffle breaks ties
        for j, c in enumerate(cars):
            for i in rows:
                if CAREER[i] == c:
                    out[i] = (j + offset) % k
        offset += len(cars)
    return np.array([out[i] for i in rows])


def cell_centred(Z, cells):
    _, inv = np.unique(cells, return_inverse=True)
    o = np.argsort(inv, kind="mergesort")
    _, start, counts = np.unique(inv[o], return_index=True, return_counts=True)
    means = np.add.reduceat(Z[o], start, axis=0) / counts[:, None]
    return Z - means[inv]


_scale_cache = {}


def fit_scale(tr, L, raw=False):
    key = (hash(tr.tobytes()), L, raw)
    if key not in _scale_cache:
        mu = X[L][tr].mean(0)
        sc = np.ones(W) if raw else np.sqrt((cell_centred(X[L][tr].astype(np.float64), CELL[tr]) ** 2).mean(0)) + 1e-6
        _scale_cache[key] = (mu, sc)
    return _scale_cache[key]


def fit_m1(tr, L, raw=False, labels=None):
    yy = y if labels is None else labels
    mu, sc = fit_scale(tr, L, raw)
    Z = (X[L][tr] - mu) / sc
    diffs, wts = [], []
    for c in np.unique(CELL[tr]):
        m = CELL[tr] == c
        p, q = m & (yy[tr] == 1), m & (yy[tr] == 0)
        if p.any() and q.any():
            diffs.append(Z[p].mean(0) - Z[q].mean(0))
            wts.append(2 / (1 / p.sum() + 1 / q.sum()))
    d = np.average(np.stack(diffs), axis=0, weights=wts)
    s = Z @ d
    a, b = s[yy[tr] == 0].mean(), s[yy[tr] == 1].mean()
    return {"L": L, "mu": mu, "sc": sc, "d": d, "a": a, "b": b}


def score_m1(f, te):
    return (((X[f["L"]][te] - f["mu"]) / f["sc"]) @ f["d"] - f["a"]) / (f["b"] - f["a"])


def fit_m2(tr, L, C):
    mu, sc = fit_scale(tr, L)
    clf = LogisticRegression(C=C, max_iter=3000)
    clf.fit((X[L][tr] - mu) / sc, y[tr])
    return {"L": L, "mu": mu, "sc": sc, "clf": clf}


def score_m2(f, te):
    return f["clf"].decision_function((X[f["L"]][te] - f["mu"]) / f["sc"])


def inner(tr, with_m2=True):
    """Inner cross-validation on the training careers: M1's AUROC per layer, M2's per layer and strength, and the inner
    out-of-fold scores at the chosen settings (for thresholds)."""
    fo = folds_for(tr, seed=SEED + 1)
    m1 = {L: np.zeros(len(tr)) for L in LAYERS}
    m2 = {(L, C): np.zeros(len(tr)) for L in LAYERS for C in CS} if with_m2 else {}
    for k in range(5):
        a, b = tr[fo != k], tr[fo == k]
        for L in LAYERS:
            m1[L][fo == k] = score_m1(fit_m1(a, L), b)
            for C in (CS if with_m2 else []):
                m2[(L, C)][fo == k] = score_m2(fit_m2(a, L, C), b)
    a1 = {L: auc(m1[L], y[tr]) for L in LAYERS}
    a2 = {key: auc(v, y[tr]) for key, v in m2.items()}
    L1 = max(a1, key=a1.get)
    best2 = max(a2, key=a2.get) if a2 else None
    return {"L1": L1, "auc1": a1, "oof1": m1[L1], "best2": best2, "auc2": a2, "oof2": m2.get(best2)}


def baselines(tr, te):
    rate = lambda groups: {g: y[tr][groups[tr] == g].mean() for g in np.unique(groups[tr])}
    overall = y[tr].mean()
    fr, rq = rate(FRAME), rate(REQ)
    out = {"framing-only": np.array([fr.get(g, overall) for g in FRAME[te]]),
           "request-only": np.array([rq.get(g, overall) for g in REQ[te]]),
           "history-only": HIST[te].astype(float)}
    cols = [("f", g) for g in np.unique(FRAME[tr])] + [("r", g) for g in np.unique(REQ[tr])]
    design = lambda rows: np.column_stack([(FRAME[rows] == g) if t == "f" else (REQ[rows] == g) for t, g in cols]
                                          + [HIST[rows]]).astype(float)
    clf = LogisticRegression(C=1.0, max_iter=3000).fit(design(tr), y[tr])
    out["no-state (combined)"] = clf.decision_function(design(te))
    out["_combined_train"] = clf.decision_function(design(tr))
    return out


# ---------------- Split 1
ALL = np.arange(N)
FOLD = folds_for(ALL)
S1 = {name: np.zeros(N) for name in ["M1", "M2", "M1 raw", "framing-only", "request-only", "history-only",
                                     "no-state (combined)"]}
S1_layer = {L: np.zeros(N) for L in LAYERS}               # M1 at each fixed layer (exploratory)
RND = rng.normal(size=(N_RANDOM, W))
RND /= np.linalg.norm(RND, axis=1, keepdims=True)
S1_rnd = np.zeros((N_RANDOM, N))
S1_shuf = np.zeros((N_SHUFFLE, N))
chosen, thr = [], {"M1": [], "M2": [], "no-state (combined)": []}
flag = {name: {t: np.zeros(N, bool) for t in ("catch 80%", "false alarm 10%")} for name in thr}
for k in range(5):
    tr, te = ALL[FOLD != k], ALL[FOLD == k]
    inn = inner(tr)
    L1, (L2, C2) = inn["L1"], inn["best2"]
    chosen.append({"fold": k, "M1 layer": L1, "M2 layer": L2, "M2 C": C2, "inner M1 AUROC": inn["auc1"][L1],
                   "inner M2 AUROC": inn["auc2"][(L2, C2)], "test careers": len(np.unique(CAREER[te])),
                   "test went along": int(y[te].sum())})
    f1 = fit_m1(tr, L1)
    S1["M1"][te] = score_m1(f1, te)
    S1["M1 raw"][te] = score_m1(fit_m1(tr, L1, raw=True), te)
    S1["M2"][te] = score_m2(fit_m2(tr, L2, C2), te)
    for L in LAYERS:
        S1_layer[L][te] = score_m1(fit_m1(tr, L), te)
    b = baselines(tr, te)
    for name in ("framing-only", "request-only", "history-only", "no-state (combined)"):
        S1[name][te] = b[name]
    # thresholds from the training careers only
    train_scores = {"M1": inn["oof1"], "M2": inn["oof2"], "no-state (combined)": b["_combined_train"]}
    for name, ts in train_scores.items():
        t80 = np.quantile(ts[y[tr] == 1], 0.20)              # 80% of training going-along requests at or above
        t10 = np.quantile(ts[y[tr] == 0], 0.90)              # 10% of training not-going-along requests above
        thr[name].append((float(t80), float(t10)))
        flag[name]["catch 80%"][te] = S1[name][te] >= t80
        flag[name]["false alarm 10%"][te] = S1[name][te] > t10
    # controls at the fold's M1 layer and scale
    Zte = (X[L1][te] - f1["mu"]) / f1["sc"]
    Ztr = (X[L1][tr] - f1["mu"]) / f1["sc"]
    pr, pt = Ztr @ RND.T, Zte @ RND.T
    for r in range(N_RANDOM):
        sign = 1.0 if auc(pr[:, r], y[tr]) >= 0.5 else -1.0
        S1_rnd[r, te] = sign * (pt[:, r] - pr[:, r].mean()) / (pr[:, r].std() + 1e-12)
    g = np.random.default_rng(SEED + 100 + k)
    for r in range(N_SHUFFLE):
        yy = y.copy()
        for c in np.unique(CELL[tr]):
            idx = tr[CELL[tr] == c]
            yy[idx] = g.permutation(yy[idx])
        S1_shuf[r, te] = score_m1(fit_m1(tr, L1, labels=yy), te)
    print(f"fold {k}: M1 layer {L1}, M2 layer {L2} C {C2}", flush=True)
S1["words"] = np.where(HAS_WORDS, WORDS, np.nan)

# ---------------- Split 2
def transfer(train_mask, test_mask):
    tr, te = np.where(train_mask)[0], np.where(test_mask)[0]
    inn = inner(tr, with_m2=False)
    f1 = fit_m1(tr, inn["L1"])
    s = {"M1": score_m1(f1, te)}
    fo = folds_for(tr, seed=SEED + 2)
    Cbest = max(CS, key=lambda C: auc(np.concatenate([score_m2(fit_m2(tr[fo != j], inn["L1"], C), tr[fo == j])
                                                       for j in range(5)]),
                                       np.concatenate([y[tr[fo == j]] for j in range(5)])))
    s["M2"] = score_m2(fit_m2(tr, inn["L1"], Cbest), te)
    b = baselines(tr, te)
    for name in ("request-only", "history-only", "no-state (combined)"):
        s[name] = b[name]
    res = {"layer": inn["L1"], "M2 C": Cbest, "requests": len(te), "went along": int(y[te].sum()),
           "careers": len(np.unique(CAREER[te]))}
    full = {name: np.full(N, np.nan) for name in s}
    for name, v in s.items():
        full[name][te] = v
    mask = np.zeros(N, bool)
    mask[te] = True
    for name in s:
        res[name] = interval(full[name], mask)
    j7 = mask & (DATE == JAN7)
    res["M1, 7 Jan"] = interval(full["M1"], j7)
    return res


eligible = {e: (y[EXP == e].sum() >= 10 and len(np.unique(CAREER[(EXP == e) & (y == 1)])) >= 5) for e in EXPS}
S2 = {}
for e in EXPS:
    if e != "B" and eligible[e]:
        S2[f"built on B, tested on {e}"] = transfer(EXP == "B", EXP == e)
        print("split 2:", e, "from B", flush=True)
for e in EXPS:
    if eligible[e]:
        S2[f"built on all but {e}, tested on {e}"] = transfer(EXP != e, EXP == e)
        print("split 2: leave out", e, flush=True)

# ---------------- the report
everything = np.ones(N, bool)
fmt = lambda t: f"{t[0]:.3f} ({t[1]:.3f} to {t[2]:.3f})"
fmtd = lambda t: f"{t[0]:+.3f} ({t[1]:+.3f} to {t[2]:+.3f})"
pooled = {name: interval(S1[name], everything) for name in S1 if name != "words"}
pooled["words"] = interval(np.nan_to_num(S1["words"]), HAS_WORDS)
m1_on_words = interval(S1["M1"], HAS_WORDS)
diffs = {name: interval(S1["M1"], everything, S1[name]) for name in
         ("framing-only", "request-only", "history-only", "no-state (combined)")}
diff_words = interval(S1["M1"], HAS_WORDS, np.nan_to_num(S1["words"]))
rnd_auc = np.array([auc(S1_rnd[r], y) for r in range(N_RANDOM)])
shuf_auc = np.array([auc(S1_shuf[r], y) for r in range(N_SHUFFLE)])
crit = {
    "1. AUROC at least 0.75": pooled["M1"][0] >= 0.75,
    "2. beats framing-only, request-only, history-only and combined no-state (interval above 0)":
        all(d[1] > 0 for d in diffs.values()),
    "3. above every random direction": pooled["M1"][0] > rnd_auc.max(),
    "4. matches or beats words (lower bound above -0.05)": diff_words[1] > -0.05,
}


def within_request(s, mask=everything):
    num = den = 0.0
    for r in np.unique(REQ):
        m = mask & (REQ == r)
        npos, nneg = y[m].sum(), (1 - y[m]).sum()
        if npos and nneg:
            num += auc(s[m], y[m]) * npos * nneg
            den += npos * nneg
    return num / den


def within_request_interval(s, base=None, mask=everything):
    pt = within_request(s, mask) - (within_request(base, mask) if base is not None else 0)
    bs = []
    for rows, w in boot_weights(mask, n=500):
        v = []
        for sc in ([s] if base is None else [s, base]):
            num = den = 0.0
            for r in np.unique(REQ):
                m = REQ[rows] == r
                yy, ww = y[rows][m], w[m]
                npos, nneg = (ww * yy).sum(), (ww * (1 - yy)).sum()
                if npos and nneg:
                    num += auc(sc[rows][m], yy, ww) * npos * nneg
                    den += npos * nneg
            v.append(num / den)
        bs.append(v[0] - (v[1] if base is not None else 0))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return pt, lo, hi


rep = ["# State monitor, Phase 1: held-out results (read point 1)\n",
       "Produced by `designs/rd2/analysis/monitor_phase1.py`, as preregistered in `designs/rd2/PREREG_MONITOR.md` "
       "(committed before any score was computed). 1,710 requests in 285 careers (A to F with C2), 286 went along. Read "
       "point: the last token before the reply. AUROC: the chance a going-along request scores above one that did not "
       "(0.5 = no better than chance); 95% intervals by resampling careers. Split 1: five folds by career; every "
       "monitor, threshold and layer was built on the training careers only.\n",
       "## Success criteria (Split 1, M1)\n", "| Criterion | Result | Met |", "|---|---|---|",
       f"| 1. AUROC at least 0.75 | {fmt(pooled['M1'])} | {'yes' if crit['1. AUROC at least 0.75'] else 'no'} |"]
for name, d in diffs.items():
    rep.append(f"| 2. M1 minus {name} | {fmtd(d)} | {'yes' if d[1] > 0 else 'no'} |")
rep += [f"| 3. above every random direction | M1 {pooled['M1'][0]:.3f}; random: highest {rnd_auc.max():.3f}, median "
        f"{np.median(rnd_auc):.3f} | {'yes' if crit['3. above every random direction'] else 'no'} |",
        f"| 4. M1 minus words (C2 left out) | {fmtd(diff_words)} | {'yes' if diff_words[1] > -0.05 else 'no'} |",
        f"\n**All four met: {'yes' if all(crit.values()) else 'no'}.**\n",
        "## Every monitor and baseline (Split 1, pooled)\n",
        "| Monitor | AUROC | Within request | 7 January only |", "|---|---|---|---|"]
j7 = DATE == JAN7
for name in ["M1", "M1 raw", "M2", "framing-only", "request-only", "history-only", "no-state (combined)", "words"]:
    s = S1[name] if name != "words" else np.nan_to_num(S1["words"])
    m = HAS_WORDS if name == "words" else everything
    wr = within_request_interval(s) if name in ("M1", "M2", "no-state (combined)") else (within_request(s, m), None, None)
    rep.append(f"| {name} | {fmt(pooled[name])} | {fmt(wr) if wr[1] is not None else f'{wr[0]:.3f}'} | "
               f"{fmt(interval(s, m & j7))} |")
rep += [f"\nM1 on the requests with words labels (for criterion 4): {fmt(m1_on_words)}. The words labels agree with the "
        f"trade label's source on {agree_label} of {int(HAS_WORDS.sum())} requests' \"traded along\" field (a join check).",
        f"Label shuffles (direction rebuilt on shuffled labels, 100 times): AUROC median {np.median(shuf_auc):.3f}, "
        f"highest {shuf_auc.max():.3f}.\n",
        "## Catching and false alarms (thresholds from the training careers only)\n",
        "| Monitor | Threshold | Caught (of 286 that went along) | False alarms (of 1,424 that did not) | Flags per career | "
        "Flags per career that never went along |", "|---|---|---|---|---|---|"]
never = np.array([y[CAREER == c].sum() == 0 for c in CAREER])
ncar, nnever = len(np.unique(CAREER)), len(np.unique(CAREER[never]))
for name in flag:
    for t, f in flag[name].items():
        rep.append(f"| {name} | {t} | {int(f[y == 1].sum())} ({100 * f[y == 1].mean():.0f}%) | {int(f[y == 0].sum())} "
                   f"({100 * f[y == 0].mean():.0f}%) | {f.sum() / ncar:.2f} | {f[never].sum() / max(nnever, 1):.2f} |")
for t, cut in (("words: AGREES", 2), ("words: AGREES or NONCOMMITTAL", 1)):
    f = HAS_WORDS & (np.nan_to_num(S1["words"]) >= cut)
    rep.append(f"| {t} | (after the reply) | {int(f[y == 1].sum())} ({100 * f[HAS_WORDS & (y == 1)].sum() / (HAS_WORDS & (y == 1)).sum():.0f}%) | "
               f"{int(f[y == 0].sum())} ({100 * f[HAS_WORDS & (y == 0)].sum() / (HAS_WORDS & (y == 0)).sum():.0f}%) | | |")
rep += ["\n## By experiment (Split 1, pooled out-of-fold scores)\n",
        "| Experiment | Requests | Went along | M1 | M2 | No-state (combined) | Words | M1, 7 January |", "|---|---|---|---|---|---|---|---|"]
per_exp = {}
for e in EXPS:
    m = EXP == e
    row = {k: interval(S1[k], m) for k in ("M1", "M2", "no-state (combined)")}
    row["words"] = interval(np.nan_to_num(S1["words"]), m & HAS_WORDS) if (m & HAS_WORDS).any() else None
    row["M1, 7 Jan"] = interval(S1["M1"], m & j7)
    per_exp[e] = row
    rep.append(f"| {e} | {m.sum()} | {y[m].sum()} | {fmt(row['M1'])} | {fmt(row['M2'])} | {fmt(row['no-state (combined)'])} | "
               f"{fmt(row['words']) if row['words'] else '-'} | {fmt(row['M1, 7 Jan'])} |")
rep += ["\n## The layer chosen in each fold (inner cross-validation on the training careers)\n",
        "| Fold | Test careers | Test went along | M1 layer | Inner AUROC | M2 layer | M2 strength (C) | Inner AUROC |",
        "|---|---|---|---|---|---|---|---|"]
for c in chosen:
    rep.append(f"| {c['fold']} | {c['test careers']} | {c['test went along']} | {c['M1 layer']} | {c['inner M1 AUROC']:.3f} | "
               f"{c['M2 layer']} | {c['M2 C']:g} | {c['inner M2 AUROC']:.3f} |")
rep += ["\n## Every layer, M1 at a fixed layer (exploratory)\n", "| Layer | AUROC | Within request | 7 January |", "|---|---|---|---|"]
for L in LAYERS:
    rep.append(f"| {L} | {fmt(interval(S1_layer[L], everything))} | {within_request(S1_layer[L]):.3f} | "
               f"{fmt(interval(S1_layer[L], j7))} |")
rep += ["\n## Split 2: transfer across experiments (reported, not pass/fail)\n",
        "Only experiments with at least 10 going-along requests from at least 5 careers are tested (all qualify: " +
        ", ".join(f"{e} {'yes' if v else 'no'}" for e, v in eligible.items()) + ").\n",
        "| Built on, tested on | Requests | Went along | M1 layer | M1 | M2 | Request-only | History-only | No-state | M1, 7 January |",
        "|---|---|---|---|---|---|---|---|---|---|"]
for name, r in S2.items():
    rep.append(f"| {name} | {r['requests']} | {r['went along']} | {r['layer']} | {fmt(r['M1'])} | {fmt(r['M2'])} | "
               f"{fmt(r['request-only'])} | {fmt(r['history-only'])} | {fmt(r['no-state (combined)'])} | {fmt(r['M1, 7 Jan'])} |")
rep.append("\nRead point 2 (before the order line) is not in this report: it needs a GPU pass, run only after the author's yes.")

# ---------------- exploratory, not preregistered (added after the preregistered results above were read)
rnd_wr = np.array([within_request(S1_rnd[r]) for r in range(N_RANDOM)])
shuf_wr = np.array([within_request(S1_shuf[r]) for r in range(N_SHUFFLE)])
rnd_j7 = np.array([auc(S1_rnd[r][j7], y[j7]) for r in range(N_RANDOM)])
rep += ["\n## Exploratory (not preregistered; added after the results above were read)\n",
        "Going along falls from 51% of the 7 January requests to 1% of the 5 August ones, so any direction that encodes "
        "where in the career a request falls separates going along on the pooled AUROC. Within each request, and on "
        "7 January alone, the request cannot do that.\n",
        "| Comparison | Pooled | Within request | 7 January only |", "|---|---|---|---|",
        f"| M1 | {pooled['M1'][0]:.3f} | {within_request(S1['M1']):.3f} | {auc(S1['M1'][j7], y[j7]):.3f} |",
        f"| M2 | {pooled['M2'][0]:.3f} | {within_request(S1['M2']):.3f} | {auc(S1['M2'][j7], y[j7]):.3f} |",
        f"| 100 random directions: median | {np.median(rnd_auc):.3f} | {np.median(rnd_wr):.3f} | {np.median(rnd_j7):.3f} |",
        f"| 100 random directions: highest | {rnd_auc.max():.3f} | {rnd_wr.max():.3f} | {rnd_j7.max():.3f} |",
        f"| 100 label shuffles: median | {np.median(shuf_auc):.3f} | {np.median(shuf_wr):.3f} | |",
        f"| 100 label shuffles: highest | {shuf_auc.max():.3f} | {shuf_wr.max():.3f} | |",
        "", "| Difference (95% interval, careers resampled) | Pooled | Within request | 7 January only |", "|---|---|---|---|"]
for a_name, b_name in [("M2", "no-state (combined)"), ("M2", "framing-only"), ("M1", "no-state (combined)"),
                       ("M1", "framing-only"), ("M2", "M1")]:
    rep.append(f"| {a_name} minus {b_name} | {fmtd(interval(S1[a_name], everything, S1[b_name]))} | "
               f"{fmtd(within_request_interval(S1[a_name], S1[b_name]))} | {fmtd(interval(S1[a_name], j7, S1[b_name]))} |")

# ---------------- figures and per-request CSVs
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def roc(s, yy):
        o = np.argsort(-s)
        tp, fp = np.cumsum(yy[o]) / yy.sum(), np.cumsum(1 - yy[o]) / (1 - yy).sum()
        return np.r_[0, fp], np.r_[0, tp]
    fig, ax = plt.subplots(figsize=(6, 5.5))
    for name, style in [("M1", "-"), ("M2", "-"), ("no-state (combined)", "--"), ("request-only", ":"), ("history-only", ":")]:
        fx, ty = roc(S1[name], y)
        ax.plot(fx, ty, style, label=f"{name} ({pooled[name][0]:.2f})")
    fx, ty = roc(np.nan_to_num(S1["words"])[HAS_WORDS], y[HAS_WORDS])
    ax.plot(fx, ty, "-.", label=f"words, after the reply ({pooled['words'][0]:.2f})")
    ax.plot([0, 1], [0, 1], color="#bbb", lw=0.8)
    ax.set_xlabel("False alarms (share of requests that did not go along)")
    ax.set_ylabel("Caught (share of requests that went along)")
    ax.set_title("Held-out monitors, read point 1 (Split 1)")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "roc.png"), dpi=150)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    bins = np.linspace(np.percentile(S1["M1"], 1), np.percentile(S1["M1"], 99), 40)
    ax.hist(S1["M1"][y == 0], bins=bins, alpha=0.6, density=True, label="did not go along")
    ax.hist(S1["M1"][y == 1], bins=bins, alpha=0.6, density=True, label="went along")
    ax.set_xlabel("M1 score (0 = training mean of did not, 1 = of went along)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "scores.png"), dpi=150)
    rep.append("\n![ROC](roc.png)\n\n![scores](scores.png)")
except ImportError:
    pass
for e in EXPS:
    with open(os.path.join(OUT, f"requests_{e}.csv"), "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["request", "career", "condition", "date", "request_id", "went_along", "words", "earlier_went_along",
                     "fold", "M1", "M2", "M1_raw"] + [f"M1_L{L}" for L in LAYERS] +
                    ["framing_only", "request_only", "no_state"])
        for i in np.where(EXP == e)[0]:
            m = meta[i]
            wr.writerow([f"{CAREER[i]}|{m['chat']}", CAREER[i], m["version"], m["date"], m["chat"], y[i],
                         "" if np.isnan(WORDS[i]) else int(WORDS[i]), HIST[i], FOLD[i]] +
                        [f"{S1[k][i]:.4f}" for k in ("M1", "M2", "M1 raw")] + [f"{S1_layer[L][i]:.4f}" for L in LAYERS] +
                        [f"{S1[k][i]:.4f}" for k in ("framing-only", "request-only", "no-state (combined)")])
open(os.path.join(OUT, "SUMMARY.md"), "w").write("\n".join(rep) + "\n")
json.dump({"exploratory": {"random_within_request": rnd_wr.tolist(), "shuffle_within_request": shuf_wr.tolist(),
                           "random_jan7": rnd_j7.tolist()}, "criteria": {k: bool(v) for k, v in crit.items()}, "pooled": pooled, "diffs": diffs, "diff_words": diff_words,
           "random_auc": rnd_auc.tolist(), "shuffle_auc": shuf_auc.tolist(), "folds": chosen, "split2": S2,
           "thresholds": thr}, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=float)
print("\n".join(rep))
