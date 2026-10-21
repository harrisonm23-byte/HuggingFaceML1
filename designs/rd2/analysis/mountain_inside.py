"""The mountain inside (INSIDE_PLAN test 4; exploratory): the frame and the decision followed along every trading-day
update of every career.

    python designs/rd2/analysis/mountain_inside.py <states root, e.g. /states/v2> <output dir>

Data: /states/v2/<exp>_bf16_steps/*.npz (the state at the last token before every trading-day reply, about 120 per
career, layers 6-47; scripts/modal_inside.py --every-step). Two yardsticks, each built on the other half of the careers
(runs 5-9 for careers 0-4 and the other way round):
- the frame direction (B's matched rereads: UBS's loss and loss + you request minus the neutral request, the history held
  fixed), at layers 12 and 24; units: 1 = as far as UBS's loss request itself moves the state;
- the going-along direction (Run 1: agents that went along minus those that did not, within request, experiment and
  framing), at layer 24; units: 1 = the full gap between agents that went along and agents that did not.
Each career's projection is averaged over each trading day's updates; framed careers are compared with neutral ones, and
loss-framed with gain-framed, day by day (p reshuffles whole careers between the groups, 10,000 times). "Early minus
later" asks whether the difference is larger on 7 January than on the later days (fades) or smaller (builds).
"""
import glob, json, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.getcwd(), "sim"))
import steer2

ROOT, OUT = sys.argv[1], sys.argv[2]
PERMS = 10000
RNG = np.random.default_rng(20261022)
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]
EXPS = ["B", "F", "A", "D", "E"]
LOSS, GAIN = ("loss", "loss + you"), ("gain", "gain + you")
os.makedirs(OUT, exist_ok=True)

# ---------------- the yardsticks
matched = sorted(glob.glob(os.path.join(ROOT, "matched", "B_bf16", "*.npz")))
frame = {L: steer2.directions(matched, L) for L in (12, 24)}
run1 = sorted(p for e in ("A", "B", "C", "C2", "D", "E", "F") for p in glob.glob(os.path.join(ROOT, f"{e}_bf16", "*.npz")))
along = steer2.along_direction(run1, 24)
YARD = {"frame, layer 12": (12, lambda h: frame[12][h]["loss"], lambda h: frame[12][h]["size"]),
        "frame, layer 24": (24, lambda h: frame[24][h]["loss"], lambda h: frame[24][h]["size"]),
        "going along, layer 24": (24, lambda h: along[h]["along"], lambda h: along[h]["size"])}

# ---------------- every career: its projection, averaged per trading day
careers, counts = [], {}
for e in EXPS:
    files = sorted(glob.glob(os.path.join(ROOT, f"{e}_bf16_steps", "*.npz")))
    counts[e] = (len(files), [])
    for p in files:
        z = np.load(p)
        assert [int(l) for l in z["layers"]] == KEEP, p
        meta = json.loads(str(z["meta"]))
        S = z["states"].astype(np.float64)                         # updates x layers x width
        counts[e][1].append(len(meta))
        h = steer2.half_for(int(meta[0]["run"]))
        days = sorted({m["date"] for m in meta})
        row = {"experiment": e, "version": meta[0]["version"], "file": os.path.basename(p), "days": days, "proj": {}}
        for name, (L, vec, size) in YARD.items():
            pr = S[:, KEEP.index(L)] @ vec(h) / size(h) ** 2
            row["proj"][name] = {d: float(np.mean([v for v, m in zip(pr, meta) if m["date"] == d])) for d in days}
            first = [v for v, m, prev in zip(pr, meta, [None] + meta[:-1]) if prev is None or prev["date"] != m["date"]]
            row["proj"][name]["openings"] = float(np.mean(first))
        careers.append(row)


def compare(rows_a, rows_b, key, name):
    a = np.array([r["proj"][name][key] for r in rows_a if key in r["proj"][name]])
    b = np.array([r["proj"][name][key] for r in rows_b if key in r["proj"][name]])
    if len(a) < 2 or len(b) < 2:
        return None
    obs = a.mean() - b.mean()
    y = np.concatenate([a, b])
    null = np.array([(lambda o: y[o[:len(a)]].mean() - y[o[len(a):]].mean())(RNG.permutation(len(y))) for _ in range(PERMS)])
    return {"diff": float(obs), "p": float((np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)),
            "n": [int(len(a)), int(len(b))]}


def early_minus_later(rows_a, rows_b, name):
    """Each career's 7 January value minus its mean over the later days; group a minus group b."""
    f = lambda r: r["proj"][name][r["days"][0]] - np.mean([r["proj"][name][d] for d in r["days"][1:]])
    a, b = np.array([f(r) for r in rows_a]), np.array([f(r) for r in rows_b])
    if len(a) < 2 or len(b) < 2:
        return None
    obs = a.mean() - b.mean()
    y = np.concatenate([a, b])
    null = np.array([(lambda o: y[o[:len(a)]].mean() - y[o[len(a):]].mean())(RNG.permutation(len(y))) for _ in range(PERMS)])
    return {"diff": float(obs), "p": float((np.sum(np.abs(null) >= abs(obs) - 1e-12) + 1) / (PERMS + 1))}


fmt = lambda r: "–" if r is None else f"{r['diff']:+.2f} (p {r['p']:.3f})"
report = ["# The mountain inside: the frame and the decision along every trading-day update (exploratory)\n",
          "Every trading-day update of every career (about 120 per career; the state at the last token before each "
          "reply), projected on two yardsticks built on the other half of the careers: the **frame direction** (UBS's "
          "loss request minus the neutral request with the history held fixed; 1 = as far as UBS's loss request itself "
          "moves the state) and the **going-along direction** (agents that went along minus those that did not; 1 = the "
          "full gap between them). Each career is averaged per trading day; groups of careers are compared day by day; "
          "p reshuffles careers (10,000 times). Produced by `designs/rd2/analysis/mountain_inside.py`.\n",
          "Files read: " + ", ".join(f"{e} {counts[e][0]} careers (updates per career: "
                                       f"{min(counts[e][1]) if counts[e][1] else 0}–{max(counts[e][1]) if counts[e][1] else 0})"
                                       for e in EXPS) + ".\n"]
summary = {}
for e in EXPS:
    rows = [r for r in careers if r["experiment"] == e]
    if not rows:
        continue
    by = lambda vs: [r for r in rows if r["version"] in vs]
    framed, neutral = by(LOSS + GAIN), by(("neutral",))
    contrasts = [("Loss-framed minus gain-framed", by(LOSS), by(GAIN))]
    if neutral:
        contrasts.insert(0, ("Framed minus neutral", framed, neutral))
    days = rows[0]["days"]
    report.append(f"\n## Experiment {e}\n")
    summary[e] = {}
    for title, A, B in contrasts:
        report.append(f"**{title}** ({len(A)} against {len(B)} careers)\n")
        report.append("| Yardstick | " + " | ".join(days) + " | First update of each day | Early minus later |\n"
                      + "|---" * (len(days) + 3) + "|")
        for name in YARD:
            cells = [fmt(compare(A, B, d, name)) for d in days]
            report.append(f"| {name} | " + " | ".join(cells) + f" | {fmt(compare(A, B, 'openings', name))} | "
                          f"{fmt(early_minus_later(A, B, name))} |")
            summary[e][f"{title} | {name}"] = {d: compare(A, B, d, name) for d in days}
        report.append("")
    # the levels themselves, for the record
    report.append("Mean projection by version and day (frame, layer 12 / going along, layer 24):\n")
    report.append("| Version | " + " | ".join(days) + " |\n" + "|---" * (len(days) + 1) + "|")
    for v in sorted({r["version"] for r in rows}):
        rv = by((v,))
        report.append(f"| {v} ({len(rv)}) | " + " | ".join(
            f"{np.mean([r['proj']['frame, layer 12'][d] for r in rv]):+.2f} / "
            f"{np.mean([r['proj']['going along, layer 24'][d] for r in rv]):+.2f}" for d in days) + " |")
    report.append("")
open(os.path.join(OUT, "MOUNTAIN_INSIDE.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "mountain_inside.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "MOUNTAIN_INSIDE.md"))
