"""State monitor, exploratory checks on Phase 1's data (added after Phase 1's results were read; MONITOR.md,
"Decisions, 5 Nov"). Not part of Phase 1's evaluation; every number here is labelled exploratory.

    python designs/rd2/analysis/monitor_explore.py <folder holding the downloaded <exp>_bf16 state folders>

1. A prompt-only text baseline: a TF-IDF (hashed words and word pairs) logistic regression on the visible conversation up to the decision (every
   turn the agent had seen and written, no model activations), with Phase 1's career folds; word weights and strength
   from the training careers only. Compared with Phase 1's M2 on the same requests.
2. Each request held out in turn: the monitor built on the other five requests of the training careers, tested on the
   held-out request of the test careers (Phase 1's career folds, so no career is on both sides).
3. Transfer within request: M2 built on B (or on every experiment but one) and tested on the others, reported pooled,
   within request and on 7 January.
M2 here uses Phase 1's settings, fixed: layer 22, C = 0.001 (C in all five folds; layer 22 in three, 24 in two).
Thresholds catch 80% of the training careers' going-along requests (inner cross-validation); never from the test side.
Writes results/monitor_heldout/EXPLORATORY.md and exploratory.json.
"""
import csv, glob, json, os, sys
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from monitor_common import (EXPS, FOLDERS, JAN7, REQUESTS, ROOT, SEED, Data, auc, folds_for, interval,
                            m2_with_threshold, table, within_request)

D = Data(sys.argv[1], layers=[22])
OUT = os.path.join(ROOT, "results", "monitor_heldout")
L, C = 22, 1e-3
TEXT_CS = [0.1, 1.0, 10.0, 100.0]
fmt = lambda t: f"{t[0]:.3f} ({t[1]:.3f} to {t[2]:.3f})"
fmtd = lambda t: f"{t[0]:+.3f} ({t[1]:+.3f} to {t[2]:+.3f})"

# ---------------- Phase 1's own scores, folds and thresholds
rows = {}
for e in EXPS:
    for r in csv.DictReader(open(os.path.join(OUT, f"requests_{e}.csv"))):
        rows[r["request"]] = r
p1 = [rows[i] for i in D.ID]
assert all(int(r["went_along"]) == D.y[i] for i, r in enumerate(p1))
FOLD = np.array([int(r["fold"]) for r in p1])
summ = json.load(open(os.path.join(OUT, "summary.json")))
P1 = {"M2": np.array([float(r["M2"]) for r in p1]), "no-state (combined)": np.array([float(r["no_state"]) for r in p1])}
P1_FLAG = {k: np.array([P1[k][i] >= summ["thresholds"][k][FOLD[i]][0] for i in range(D.N)]) for k in P1}

# ---------------- the visible conversation at each decision
hist = {}
for e, f in FOLDERS.items():
    for p in glob.glob(os.path.join(ROOT, "results", f"full_career_gemma-3-12b-it_4bit_{f}", "careers", "*.json")):
        hist[(e, os.path.basename(p))] = json.load(open(p))["history"]
DOCS = []
for m in D.meta:
    h = hist[(m["exp"], m["career_file"])][:m["history_index"] + 1]
    assert h[-1]["role"] == "user" and "UBS [Agent A]" in h[-1]["content"], (m["exp"], m["career_file"], m["chat"])
    DOCS.append("\n".join(f"<{t['role']}> {t['content']}" for t in h))


def text_fit(Xm, tr, Cc):
    return LogisticRegression(C=Cc, max_iter=5000).fit(Xm[tr], D.y[tr])


def text_inner(Xm, tr, Cc):
    fo = folds_for(D, tr, seed=SEED + 1)
    oof = np.zeros(len(tr))
    for j in range(5):
        oof[fo == j] = text_fit(Xm, tr[fo != j], Cc).decision_function(Xm[tr[fo == j]])
    return oof


def text_with_threshold(Xm, tr, test, Cc):
    oof = text_inner(Xm, tr, Cc)
    return text_fit(Xm, tr, Cc).decision_function(Xm[test]), float(np.quantile(oof[D.y[tr] == 1], 0.20)), auc(oof, D.y[tr])


def nostate_with_threshold(tr, test, use_request=True):
    cols = [("f", g) for g in np.unique(D.FRAME[tr])] + ([("r", g) for g in np.unique(D.REQ[tr])] if use_request else [])
    design = lambda rr: np.column_stack([(D.FRAME[rr] == g) if t == "f" else (D.REQ[rr] == g) for t, g in cols]
                                        + [D.HIST[rr]]).astype(float)
    clf = LogisticRegression(C=1.0, max_iter=3000).fit(design(tr), D.y[tr])
    ts = clf.decision_function(design(tr))
    return clf.decision_function(design(test)), float(np.quantile(ts[D.y[tr] == 1], 0.20))


# words and word pairs, hashed (2^20 slots, no vocabulary to hold in memory); counts only, weights fitted per fold
COUNTS = HashingVectorizer(ngram_range=(1, 2), n_features=2 ** 20, alternate_sign=False, norm=None).transform(DOCS)
ALL = np.arange(D.N)
TEXT, TEXT_FLAG = np.zeros(D.N), np.zeros(D.N, bool)
HO = {k: np.zeros(D.N) for k in ("M2", "text", "no-state (framing + history)")}
HO_FLAG = {k: np.zeros(D.N, bool) for k in HO}
chosen = []
for k in range(5):
    tr, te = ALL[FOLD != k], ALL[FOLD == k]
    tfidf = TfidfTransformer(sublinear_tf=True).fit(COUNTS[tr])  # word weights from the training careers only
    Xm = tfidf.transform(COUNTS)
    best = max(TEXT_CS, key=lambda Cc: auc(text_inner(Xm, tr, Cc), D.y[tr]))
    s, t, a_in = text_with_threshold(Xm, tr, te, best)
    TEXT[te], TEXT_FLAG[te] = s, s >= t
    chosen.append({"fold": k, "text C": best, "text inner AUROC": a_in, "vocabulary": int((COUNTS[tr].getnnz(0) > 0).sum())})
    for r, _ in REQUESTS:                                      # 2. each request held out in turn
        trr, ter = ALL[(FOLD != k) & (D.REQ != r)], ALL[(FOLD == k) & (D.REQ == r)]
        s, t = m2_with_threshold(D, L, C, trr, ter)
        HO["M2"][ter], HO_FLAG["M2"][ter] = s, s >= t
        s, t, _ = text_with_threshold(Xm, trr, ter, best)
        HO["text"][ter], HO_FLAG["text"][ter] = s, s >= t
        s, t = nostate_with_threshold(trr, ter, use_request=False)
        HO["no-state (framing + history)"][ter], HO_FLAG["no-state (framing + history)"][ter] = s, s >= t
    print(f"fold {k}: text C {best}, inner AUROC {a_in:.3f}", flush=True)

rep = ["# State monitor: exploratory checks on Phase 1's data\n",
       "**Exploratory.** Added after Phase 1's results were read (MONITOR.md, \"Decisions, 5 Nov\"); not part of Phase "
       "1's evaluation. Produced by `designs/rd2/analysis/monitor_explore.py`. M2 here uses Phase 1's settings, fixed "
       "(layer 22, C = 0.001). Every threshold catches 80% of the training careers' going-along requests (set on the "
       "training side only). AUROC: the chance a going-along request scores above one that did not (0.5 = chance); "
       "intervals by resampling careers. Precision: of the requests flagged, the share that went along.\n",
       "## 1. Does the state know more than the visible conversation? (exploratory)\n",
       "The prompt-only text baseline reads every turn the agent had seen and written up to the decision (TF-IDF "
       "words and word pairs, logistic regression; vocabulary and strength from the training careers), with Phase 1's "
       "career folds. M2 and the no-state baseline are Phase 1's own held-out scores and thresholds."]
summary = {"folds": chosen, "tables": {}}
for name, s, f in [("M2 (Phase 1)", P1["M2"], P1_FLAG["M2"]), ("Prompt-only text baseline", TEXT, TEXT_FLAG),
                   ("No-state baseline (framing + request + history; Phase 1)", P1["no-state (combined)"],
                    P1_FLAG["no-state (combined)"])]:
    t, sm = table(D, name, s, f)
    rep += t
    summary["tables"][name] = sm
j7 = D.REQ == JAN7
every = np.ones(D.N, bool)
rep += ["", "| M2 minus the text baseline | Pooled | Within request | 7 January |", "|---|---|---|---|"]
d_pool = interval(D, lambda w: auc(P1["M2"][w > 0], D.y[w > 0], w[w > 0]) - auc(TEXT[w > 0], D.y[w > 0], w[w > 0]))
d_within = interval(D, lambda w: within_request(D, P1["M2"], w > 0, w) - within_request(D, TEXT, w > 0, w))
d_j7 = interval(D, lambda w: auc(P1["M2"][j7 & (w > 0)], D.y[j7 & (w > 0)], w[j7 & (w > 0)])
                - auc(TEXT[j7 & (w > 0)], D.y[j7 & (w > 0)], w[j7 & (w > 0)]))
rep.append(f"| AUROC difference | {fmtd(d_pool)} | {fmtd(d_within)} | {fmtd(d_j7)} |")
summary["m2_minus_text"] = {"pooled": d_pool, "within_request": d_within, "jan7": d_j7}
rep.append("\nText baseline settings per fold: " + "; ".join(
    f"fold {c['fold']}: C {c['text C']:g}, inner AUROC {c['text inner AUROC']:.3f}, {c['vocabulary']:,} hashed terms seen in training" for c in chosen) + ".")

rep += ["\n## 2. Each request held out in turn (exploratory)\n",
        "Built on the other five requests of the training careers, tested on the held-out request of the test careers "
        "(no career on both sides; the request itself never seen in training). The no-state baseline here has framing "
        "and history only, since the request is unseen. Each request's row is its own held-out test."]
for name in HO:
    t, sm = table(D, f"{name}, request held out", HO[name], HO_FLAG[name])
    rep += t
    summary["tables"][f"held out: {name}"] = sm

# ---------------- 3. transfer, within request
rep += ["\n## 3. Transfer across experiments, within request (exploratory)\n",
        "M2 (fixed settings) built on the named experiments' careers and tested on another experiment's; threshold from "
        "the training side.",
        "| Built on, tested on | n | Went along | AUROC, pooled | Within request | 7 January | Caught | False alarms | Precision |",
        "|---|---|---|---|---|---|---|---|---|"]
summary["transfer"] = {}
for name, trm, tem in ([(f"B, tested on {e}", D.EXP == "B", D.EXP == e) for e in EXPS if e != "B"] +
                       [(f"all but {e}, tested on {e}", D.EXP != e, D.EXP == e) for e in EXPS]):
    tr, te = ALL[trm], ALL[tem]
    s_te, t = m2_with_threshold(D, L, C, tr, te)
    s = np.full(D.N, np.nan)
    s[te] = s_te
    m = tem
    a = interval(D, lambda w: auc(s[m & (w > 0)], D.y[m & (w > 0)], w[m & (w > 0)]))
    wr = interval(D, lambda w: within_request(D, s, m & (w > 0), w))
    a7 = interval(D, lambda w: auc(s[m & j7 & (w > 0)], D.y[m & j7 & (w > 0)], w[m & j7 & (w > 0)]))
    fl = m & (np.nan_to_num(s, nan=-np.inf) >= t)
    tp, fp = int((fl & (D.y == 1)).sum()), int((fl & (D.y == 0)).sum())
    npos, nneg = int((m & (D.y == 1)).sum()), int((m & (D.y == 0)).sum())
    rep.append(f"| {name} | {m.sum()} | {npos} | {fmt(a)} | {fmt(wr)} | {fmt(a7)} | {100 * tp / npos:.0f}% | "
               f"{100 * fp / nneg:.0f}% | {100 * tp / max(tp + fp, 1):.0f}% ({tp} of {tp + fp}) |")
    summary["transfer"][name] = {"pooled": a, "within_request": wr, "jan7": a7, "caught": tp / npos, "false_alarms": fp / nneg}
    print("transfer", name, flush=True)

open(os.path.join(OUT, "EXPLORATORY.md"), "w").write("\n".join(rep) + "\n")
json.dump(summary, open(os.path.join(OUT, "exploratory.json"), "w"), indent=1, default=float)
print("\n".join(rep))
