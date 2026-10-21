"""Steering, third run: the analysis (exploratory; `sim/steer3.py`).

    python designs/rd2/analysis/steer3.py <rows dir, e.g. /states/v2/steer3> <output dir>

B's neutral-career requests. Each condition against none at the same moment (paired; p by flipping signs by career,
10,000 times; 95% intervals by resampling careers): the framed words themselves (the yardstick), the whole-message
transplant at each layer (also as a share of the framed words' effect) against a random vector of the same size, and the
layer-18 loss direction at 8x and 16x against random directions of the same size; sampled replies (going along,
unreadable).
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
PERMS, BOOT = 10000, 2000
RNG = np.random.default_rng(20261025)
os.makedirs(OUT, exist_ok=True)
rows = {}
for p in sorted(glob.glob(os.path.join(ROWS, "part*.jsonl"))):
    for line in open(p):
        r = json.loads(line)
        rows[r["key"]] = r
assert rows, f"no rows in {ROWS}"
M = {}
for r in rows.values():
    M.setdefault((r["career_file"], r["history_index"]), {})[r["condition"]] = r


def test(a, b="none"):
    per = {}
    for (cf, _), m in M.items():
        if a in m and b in m:
            per.setdefault(cf, []).append(m[a]["p_order_along"] - m[b]["p_order_along"])
    if len(per) < 2:
        return None
    c = np.array([np.mean(v) for v in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return {"change": float(obs), "p": float(p), "interval": [float(lo), float(hi)]}


pts = lambda r: "– | – | –" if r is None else \
    f"{100 * r['change']:+.1f} | {100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f} | {r['p']:.4f}"
conds = sorted({c for m in M.values() for c in m})
framed = next(c for c in conds if c.startswith("framed"))
fr = test(framed)
report = ["# Steering, third run (exploratory)\n",
          f"{len(M)} moments (B's neutral careers at their requests). P(the order goes along) after the fixed neutral "
          "reasoning line, each condition minus none at the same moment, in points. Produced by "
          "`designs/rd2/analysis/steer3.py`.\n",
          "## The yardstick: the framed words themselves\n",
          "| Condition | Change | 95% interval | p |\n|---|---|---|---|", f"| {framed} | {pts(fr)} |",
          "\n## The whole-message transplant (the framed update's average state added to every token of the neutral "
          "update)\n",
          "| Layer | Transplant | 95% interval | p | Share of the framed words' effect | Random vector, same size |"
          "\n|---|---|---|---|---|---|"]
summary = {"framed": fr, "transplant": {}, "push": {}}
for L in (6, 12, 18, 24):
    r = test(f"message transplant at layer {L}")
    rr = test(f"random, transplant size, at layer {L}") if f"random, transplant size, at layer {L}" in conds else None
    share = f"{100 * r['change'] / fr['change']:.0f}%" if r and fr and abs(fr["change"]) > 1e-9 else "–"
    rand = "–" if rr is None else f"{100 * rr['change']:+.1f} (p {rr['p']:.3f})"
    report.append(f"| {L} | {pts(r)} | {share} | {rand} |")
    summary["transplant"][L] = {"test": r, "random": rr}

report.append("\n## The layer-18 loss direction, pushed harder\n")
report.append("| Condition | Change | 95% interval | p | Random directions, same size (mean) |\n|---|---|---|---|---|")
for s in (8, 16):
    r = test(f"+loss x{s} at layer 18")
    rnd = [test(c) for c in conds if c.startswith("random") and c.endswith(f"x{s} at layer 18")]
    rnd = [x["change"] for x in rnd if x]
    report.append(f"| +loss x{s} at layer 18 | {pts(r)} | {100 * np.mean(rnd):+.1f} |" if rnd else
                  f"| +loss x{s} at layer 18 | {pts(r)} | – |")
    summary["push"][s] = {"test": r, "random_mean": float(np.mean(rnd)) if rnd else None}

samp = [r for r in rows.values() if r["replies"]]
if samp:
    report.append("\n## Sampled replies (two per moment)\n")
    report.append("| Condition | Replies | Went along | Unreadable |\n|---|---|---|---|")
    for c in sorted({r["condition"] for r in samp}, key=lambda c: (c != "none", c)):
        st = [s for r in samp if r["condition"] == c for s in r["status"]]
        al = [a for r in samp if r["condition"] == c for a in r["along"]]
        report.append(f"| {c} | {len(st)} | {100 * np.mean(al):.0f}% | {100 * np.mean([s not in ('trade', 'hold') for s in st]):.0f}% |")
open(os.path.join(OUT, "STEER3.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "steer3.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "STEER3.md"))
