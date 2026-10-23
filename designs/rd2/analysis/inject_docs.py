"""The state after reading an emotion document, injected without the document: the analysis (`sim/inject_docs.py`;
exploratory).

    python designs/rd2/analysis/inject_docs.py <rows dir, e.g. /states/v2/inject_docs> <output dir>

B's neutral careers at their requests. Each condition against no document at the same moment (paired; p by flipping
signs by career, 10,000 times; 95% intervals by resampling careers): the document as read (the yardstick), its
after-reading state injected without it (mean and token by token, layers 12, 18, 24), and random vectors of the same
size. As in the priming analysis, a moment counts only if the scored orders cover at least half of the model's
probability in its plain read (no document).
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
THEMES = sys.argv[3].split(",") if len(sys.argv) > 3 else ["neutral", "loss", "blame", "gain", "credit"]
LAYERS, RL = [12, 18, 24], 18
MIN_COVER = 0.5
PERMS, BOOT = 10000, 2000
RNG = np.random.default_rng(20261022)
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
low = {k for k, m in M.items() if "none" not in m or m["none"]["coverage"] < MIN_COVER}
M = {k: m for k, m in M.items() if k not in low}


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
report = ["# The state after reading a document, injected without the document (exploratory)\n",
          f"{len(M)} moments (B's neutral careers at their requests; {len(low)} more left out because the scored orders "
          "cover less than half of the model's probability with no document). The agent reads the document just before "
          "UBS's (neutral) request; the change that reading makes to each layer's state over the request's update is then "
          "put back by hand with the document left out: **mean** (the average change, added to every token) or "
          "**aligned** (the change at each token of the update, restored token by token). P(the order goes along) after "
          "the fixed neutral reasoning line, each condition minus no document at the same moment, in points. Produced by "
          "`designs/rd2/analysis/inject_docs.py`.\n"]
summary = {}
for t in THEMES:
    read = test(f"{t}: as read")
    report.append(f"\n## {t.capitalize()} document\n")
    report.append("| Condition | Change from no document | 95% interval | p | Share of the document's own effect |\n"
                  "|---|---|---|---|---|")
    report.append(f"| the document, as read | {pts(read)} | 100% |")
    summary[t] = {"read": read}
    for kind in ("mean", "aligned"):
        for L in LAYERS:
            c = f"{t}: {kind} at layer {L}"
            r = test(c)
            share = f"{100 * r['change'] / read['change']:.0f}%" if r and read and abs(read["change"]) > 1e-9 else "–"
            report.append(f"| injected, {kind}, layer {L} | {pts(r)} | {share} |")
            summary[t][c] = r
        rc = f"{t}: random {kind} at layer {RL}"
        r = test(rc)
        report.append(f"| random, {kind}, layer {RL} | {pts(r)} | – |")
        summary[t][rc] = r
    report.append("")
    report.append(f"Injected against random at layer {RL}: mean {pts(test(f'{t}: mean at layer {RL}', f'{t}: random mean at layer {RL}'))}; "
                  f"aligned {pts(test(f'{t}: aligned at layer {RL}', f'{t}: random aligned at layer {RL}'))} "
                  "(change | interval | p).")
    if t != "neutral":
        report.append(f"Beyond the neutral document: as read {pts(test(f'{t}: as read', 'neutral: as read'))}; "
                      f"aligned at layer {RL} {pts(test(f'{t}: aligned at layer {RL}', f'neutral: aligned at layer {RL}'))}.")
cov = [r["coverage"] for r in rows.values()]
report.append(f"\nCoverage: median {np.median(cov):.2f}, lowest {min(cov):.2f}.")
open(os.path.join(OUT, "INJECT_DOCS.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "inject_docs.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "INJECT_DOCS.md"))
