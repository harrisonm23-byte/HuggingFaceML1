"""Which saved requests the frozen monitor flags: fixed before any Phase 2 steering runs (MONITOR.md, "Decisions, 5 Nov").

    python designs/rd2/analysis/phase2_flags.py <folder holding the downloaded <exp>_bf16 state folders>

Phase 2's single moments are the saved careers' own requests, and the frozen M2 (results/monitor_frozen/) was fitted on
all of them, so its score there is in-sample. The flag used for the conditional arm is therefore each request's
out-of-fold score from the freeze's own cross-validation (layer 24, C = 0.001, five folds grouped by career, seed
20261106; the career's fold left out), against the frozen trigger, which was set on exactly these scores. The in-sample
score of the frozen file is kept alongside, as a check. At a single moment, conditional steering is the steered reply
where the request is flagged and the unsteered reply where it is not, so it needs no GPU arm of its own: it is put
together from these flags and the paired runs. Writes results/conditional_steering/flags.csv and FLAGS.md.
"""
import csv, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from monitor_common import REQUESTS, ROOT, SEED, Data, fit_m2, folds_for, score_m2

FROZEN = os.path.join(ROOT, "results", "monitor_frozen")
OUT = os.path.join(ROOT, "results", "conditional_steering")
z = np.load(os.path.join(FROZEN, "m2_frozen.npz"))
L, C, trigger = int(z["layer"][0]), float(z["C"][0]), float(z["trigger"][0])
D = Data(sys.argv[1], layers=[L])
ALL = np.arange(D.N)
fo = folds_for(D, ALL, seed=SEED + 1)                      # the freeze's folds (monitor_freeze.py)
oof = np.zeros(D.N)
for k in range(5):
    oof[fo == k] = score_m2(D, fit_m2(D, L, C, ALL[fo != k]), ALL[fo == k])
again = float(np.quantile(oof[D.y == 1], 0.20))
assert abs(again - trigger) < 1e-9, f"out-of-fold scores do not reproduce the frozen trigger: {again} vs {trigger}"
frozen = ((D.X[L] - z["mu"]) / z["sc"]) @ z["coef"] + z["intercept"][0]
flag, flag_in = oof >= trigger, frozen >= trigger

os.makedirs(OUT, exist_ok=True)
cols = ["experiment", "version", "run", "career_file", "chat", "date", "history_index", "joined", "score_oof", "flag",
        "score_frozen_in_sample", "flag_in_sample", "fold"]
with open(os.path.join(OUT, "flags.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for i, m in enumerate(D.meta):
        w.writerow([m["exp"], m["version"], m["run"], m["career_file"], m["chat"], m["date"], m["history_index"],
                    int(D.y[i]), f"{oof[i]:.6f}", int(flag[i]), f"{frozen[i]:.6f}", int(flag_in[i]), int(fo[i])])

rows = ["| Request | Requests | Went along | Flagged | Caught | False alarms | Precision | Flagged by the frozen file "
        "(in-sample) |", "|---|---|---|---|---|---|---|---|"]
summary = {}
for r, lab in REQUESTS + [(None, "All")]:
    m = np.ones(D.N, bool) if r is None else D.REQ == r
    pos, neg = m & (D.y == 1), m & (D.y == 0)
    tp, fp = int((flag & pos).sum()), int((flag & neg).sum())
    summary[lab] = {"requests": int(m.sum()), "went_along": int(pos.sum()), "flagged": int((flag & m).sum()),
                    "caught": tp, "false_alarms": fp, "flagged_in_sample": int((flag_in & m).sum())}
    prec = f"{100 * tp / (tp + fp):.0f}% ({tp} of {tp + fp})" if tp + fp else "-"
    rows.append(f"| {lab} | {m.sum()} | {pos.sum()} | {100 * (flag & m).sum() / m.sum():.0f}% ({(flag & m).sum()}) | "
                f"{100 * tp / max(pos.sum(), 1):.0f}% ({tp} of {pos.sum()}) | "
                f"{100 * fp / max(neg.sum(), 1):.0f}% ({fp} of {neg.sum()}) | {prec} | "
                f"{100 * (flag_in & m).sum() / m.sum():.0f}% ({(flag_in & m).sum()}) |")
json.dump({"layer": L, "C": C, "trigger": trigger, "by_request": summary}, open(os.path.join(OUT, "flags.json"), "w"),
          indent=1)
open(os.path.join(OUT, "FLAGS.md"), "w").write(
    "# The frozen monitor's flags at the saved requests\n\n"
    "Fixed before any Phase 2 steering ran (`designs/rd2/analysis/phase2_flags.py`). Each request's score is its "
    f"out-of-fold score from the freeze's cross-validation (layer {L}, C = {C:g}, the career's fold left out); a request "
    f"is flagged when the score is at or above the frozen trigger ({trigger:.4f}). The frozen file itself was fitted on "
    "these requests, so its own (in-sample) flags are shown only as a check. At a single moment, the conditional arm is "
    "the steered reply where the request is flagged and the unsteered reply where it is not.\n\n" + "\n".join(rows) + "\n")
print("\n".join(rows))
