"""Mapping the decision features on our own episodes, and the dictionary's misconduct features at the requests
(the author, 13 Nov: what kind of thing are the decision features; is there another way to map them?). CPU only.

    python map_features.py <states dir> <dir with L24/L31/L41.safetensors> <decision_features.json> <concepts.json> <repo results dir> <out json>

A. Every decision feature at every saved update of A, B, D, E, F (the last token before each trading-day reply), joined
   to what the agent then did (the day files' `traded`):
   - its mean at ordinary updates (no UBS line yet that day), at UBS lines that are not one of the six requests, and at
     the requests;
   - ordinary trades: at updates before the day's first UBS line, the agent then traded vs did not, within experiment,
     framing and date (spread units; 95% interval from resampling careers; also each experiment on its own);
   - UBS on the line: updates with a UBS line (not a request) vs the day's other updates, the same way.
B. The features Neuronpedia labels as misconduct (concept_search.py; every hit), at the 1,740 request states: how often
   each is on; A's neutral request vs the same moment with no request (within request, reshuffled 1,000 times); went
   along vs held (within request, experiment and framing).
C. Families: the replicating decision features' correlations across the asked moments, within cell.
"""
import glob, json, os, sys
import numpy as np
from safetensors.numpy import load_file

STATES, SAEDIR, DEC, CONCEPTS, RESULTS, OUT = sys.argv[1:7]
LAYERS, BOOT, PERMS = [24, 31, 41], 500, 1000
FOLDERS = {"A": "career_book_neutral_lines_v2", "B": "ubs_framing_v2", "D": "memo_and_ubs_framing_v2",
           "E": "memo_ubs_bank_c_v2", "F": "peer_same_frame_v2"}
PAPER = {"E": "F", "F": "E"}
rng = np.random.default_rng(20261113)
dec, con = json.load(open(DEC)), json.load(open(CONCEPTS))

# ---- request states
META, X = [], []
for d in sorted(glob.glob(os.path.join(STATES, "*_bf16"))):
    for f in sorted(glob.glob(os.path.join(d, "*.npz"))):
        z = np.load(f)
        META += json.loads(str(z["meta"]))
        X.append(z["states"][:, LAYERS].astype(np.float32))
X = np.concatenate(X)
EXP = np.array([m["experiment"] for m in META]); VER = np.array([m["version"] for m in META])
REQ = np.array([m["chat"] for m in META]); JOINED = np.array([bool(m["joined"]) for m in META])
ASKED = np.array([m.get("asked", True) for m in META])
CELL = np.array([f"{m['chat']}|{m['experiment']}|{m['version']}" for m in META])

# ---- every-update states, joined to the day files
rows, US = [], []
for exp, folder in FOLDERS.items():
    asked_at = {(m["version"], m["run"], m["history_index"]) for m in META if m["experiment"] == exp and m.get("asked", True)}
    for f in sorted(glob.glob(os.path.join(STATES, f"{exp}_bf16_steps", "*.npz"))):
        name = os.path.basename(f)[:-4]
        z = np.load(f)
        lay = [int(v) for v in z["layers"]]
        ms = json.loads(str(z["meta"]))
        US.append(z["states"][:, [lay.index(L) for L in LAYERS]].astype(np.float32))
        day = {}
        for dp in glob.glob(os.path.join(RESULTS, "full_career_gemma-3-12b-it_4bit_" + folder, "days", name + "_2011-*.json")):
            dj = json.load(open(dp))
            prev = 0.0
            for s in dj["steps"]:
                day[(dj["date"], s["time"])] = {"traded": float(s["traded"] or 0), "before": prev}
                prev = float(s["position"] or 0)
        spoken = set()
        for m in ms:
            s = day[(m["date"], m["time"])]
            rows.append({"exp": exp, "ver": m["version"], "run": m["run"], "date": m["date"], "ubs": bool(m["ubs"]),
                         "pre": (m["date"] not in spoken) and not m["ubs"],
                         "request": (m["version"], m["run"], m["history_index"]) in asked_at,
                         "traded": s["traded"] != 0, "before": s["before"]})
            if m["ubs"]:
                spoken.add(m["date"])
US = np.concatenate(US)
col = lambda k: np.array([r[k] for r in rows])
uEXP, uUBS, uPRE, uREQ, uTR = col("exp"), col("ubs"), col("pre"), col("request"), col("traded")
uCAR = np.unique(np.array([f"{r['exp']}|{r['ver']}|{r['run']}" for r in rows]), return_inverse=True)[1]
uCELL = np.unique(np.array([f"{r['exp']}|{r['ver']}|{r['date']}" for r in rows]), return_inverse=True)[1]
print(len(rows), "updates;", int(uREQ.sum()), "requests;", int((uUBS & ~uREQ).sum()), "other UBS lines;", int(uPRE.sum()),
      "before the day's first UBS line, of which the agent then traded at", int((uPRE & uTR).sum()), flush=True)
out = {"updates": len(rows), "requests": int(uREQ.sum()), "other_ubs_lines": int((uUBS & ~uREQ).sum()),
       "ordinary_updates": int(uPRE.sum()), "ordinary_trades": int((uPRE & uTR).sum()),
       "ordinary_trades_by_experiment": {PAPER.get(e, e): [int((uPRE & uTR & (uEXP == e)).sum()), int((uPRE & (uEXP == e)).sum())] for e in FOLDERS},
       "decision": {}, "concepts": {}, "families": {}}


def gap(V, lab, strata, r):
    s, l = strata[r], lab[r]
    num, var, wsum = 0.0, 0.0, 0.0
    for c in np.unique(s):
        m = s == c
        a, b = r[m & l], r[m & ~l]
        if len(a) < 2 or len(b) < 2:
            continue
        w = min(len(a), len(b))
        num = num + w * (V[a].mean(0) - V[b].mean(0))
        var = var + w * np.concatenate([V[a] - V[a].mean(0), V[b] - V[b].mean(0)]).var(0)
        wsum += w
    if not wsum:
        return np.full(V.shape[1], np.nan)
    return num / wsum / np.sqrt(var / wsum + 1e-6)


def boot(V, lab, strata, r, car):
    cs = np.unique(car[r])
    idx = {c: r[car[r] == c] for c in cs}
    zs = np.array([gap(V, lab, strata, np.concatenate([idx[c] for c in rng.choice(cs, len(cs))])) for _ in range(BOOT)])
    return np.nanpercentile(zs, 2.5, axis=0), np.nanpercentile(zs, 97.5, axis=0)


def perm(V, a, b, S):
    r = np.where(a | b)[0]
    lab = a.copy()
    obs = gap(V, lab, S, r)
    hits = np.zeros(V.shape[1])
    groups = [(r[S[r] == c], int(lab[r[S[r] == c]].sum())) for c in np.unique(S[r])]
    for _ in range(PERMS):
        l2 = np.zeros(len(a), bool)
        for g, k in groups:
            l2[rng.permutation(g)[:k]] = True
        hits += np.abs(np.nan_to_num(gap(V, l2, S, r))) >= np.abs(np.nan_to_num(obs)) - 1e-12
    return obs, (hits + 1) / (PERMS + 1)


sREQ = np.unique(REQ, return_inverse=True)[1]
sCELL = np.unique(CELL, return_inverse=True)[1]
fam_cols, fam_names = [], []
for li, L in enumerate(LAYERS):
    p = {k.lower().replace(".", "_"): v.astype(np.float32) for k, v in load_file(os.path.join(SAEDIR, f"L{L}.safetensors")).items()}
    We, be, th = p["w_enc"], p["b_enc"], p["threshold"]
    We = We if We.shape[0] == 3840 else We.T
    d_rows = dec["layers"][str(L)]["rows"]
    d_ids = [r["feature"] for r in d_rows]
    c_ids = sorted({v["feature"] for v in con.values() if v["layer"] == L})
    cols = d_ids + c_ids

    def enc(S):
        outp = []
        for s in range(0, len(S), 4000):
            pre = S[s:s + 4000] @ We[:, cols] + be[cols]
            outp.append(np.where(pre > th[cols], pre, 0.0))
        return np.concatenate(outp).astype(np.float64)

    Fr, Fu = enc(X[:, li]), enc(US[:, li])
    nd = len(d_ids)
    # ---- A. the decision features across the episode
    r_pre, r_non = np.where(uPRE)[0], np.where(~uREQ)[0]
    z_tr = gap(Fu[:, :nd], uTR, uCELL, r_pre)
    lo_tr, hi_tr = boot(Fu[:, :nd], uTR, uCELL, r_pre, uCAR)
    z_ub = gap(Fu[:, :nd], uUBS, uCELL, r_non)
    lo_ub, hi_ub = boot(Fu[:, :nd], uUBS, uCELL, r_non, uCAR)
    z_by = {PAPER.get(e, e): gap(Fu[:, :nd], uTR, uCELL, np.where(uPRE & (uEXP == e))[0]) for e in FOLDERS}
    for j, r in enumerate(d_rows):
        out["decision"][f"{L}:{r['feature']}"] = {
            "ordinary_trade_gap_by_experiment": {e: float(v[j]) for e, v in z_by.items()},
            "replicates": r["replicates"], "went_along_gap": r["effect_spread_units"],
            "mean_ordinary": float(Fu[uPRE, j].mean()), "mean_other_ubs_line": float(Fu[uUBS & ~uREQ, j].mean()),
            "mean_request": float(Fu[uREQ, j].mean()),
            "on_ordinary": float((Fu[uPRE, j] > 0).mean()), "on_request": float((Fu[uREQ, j] > 0).mean()),
            "ordinary_trade_gap": float(z_tr[j]), "ordinary_trade_ci": [float(lo_tr[j]), float(hi_tr[j])],
            "ubs_line_gap": float(z_ub[j]), "ubs_line_ci": [float(lo_ub[j]), float(hi_ub[j])]}
    # ---- B. the misconduct features at the requests
    C = Fr[:, nd:]
    a_ask, a_no = (EXP == "A") & (VER == "neutral") & ASKED, (EXP == "A") & ~ASKED
    z_ask, p_ask = perm(C, a_ask, a_no, sREQ)
    z_go, p_go = perm(C, ASKED & JOINED, ASKED & ~JOINED, sCELL)
    Cu = Fu[:, nd:]
    for j, f in enumerate(c_ids):
        v = con[f"{L}:{f}"]
        out["concepts"][f"{L}:{f}"] = {
            "label": v["label"], "best_similarity": max(v["queries"].values()),
            "best_query": max(v["queries"], key=v["queries"].get), "promotes": v["promotes"][:6],
            "on_at_requests": float((C[ASKED, j] > 0).mean()), "mean_at_requests": float(C[ASKED, j].mean()),
            "on_at_ordinary_updates": float((Cu[uPRE, j] > 0).mean()), "on_at_request_updates": float((Cu[uREQ, j] > 0).mean()),
            "A_request_on": float((C[a_ask, j] > 0).mean()), "A_no_request_on": float((C[a_no, j] > 0).mean()),
            "A_request_mean": float(C[a_ask, j].mean()), "A_no_request_mean": float(C[a_no, j].mean()),
            "request_vs_none_gap": None if np.isnan(z_ask[j]) else float(z_ask[j]), "request_vs_none_p": float(p_ask[j]),
            "went_along_on": float((C[ASKED & JOINED, j] > 0).mean()), "held_on": float((C[ASKED & ~JOINED, j] > 0).mean()),
            "went_along_gap": None if np.isnan(z_go[j]) else float(z_go[j]), "went_along_p": float(p_go[j])}
    # ---- C. families (the replicating ones)
    for j, r in enumerate(d_rows):
        if r["replicates"]:
            v = Fr[ASKED, j].copy()
            for c in np.unique(sCELL[ASKED]):
                m = sCELL[ASKED] == c
                v[m] -= v[m].mean()
            fam_cols.append(v)
            fam_names.append(f"{L}/{r['feature']}")
    print(L, "done", flush=True)
    json.dump(out, open(OUT, "w"), indent=1)
R = np.corrcoef(np.array(fam_cols))
sign = np.array([1 if out["decision"][n.replace("/", ":")]["went_along_gap"] > 0 else -1 for n in fam_names])
same, opp = (sign[:, None] == sign[None, :]) & ~np.eye(len(sign), dtype=bool), sign[:, None] != sign[None, :]
ev = np.linalg.eigvalsh(R)[::-1]
out["families"] = {"names": fam_names, "correlations": np.round(R, 3).tolist(),
                   "mean_correlation_same_side": float(R[same].mean()), "mean_correlation_opposite_sides": float(R[opp].mean()),
                   "first_components_share": [float(x) for x in (ev[:3] / ev.sum())]}
json.dump(out, open(OUT, "w"), indent=1)
print("families", out["families"]["mean_correlation_same_side"], out["families"]["mean_correlation_opposite_sides"], out["families"]["first_components_share"])
