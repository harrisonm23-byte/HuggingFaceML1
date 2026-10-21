"""The confirmation scan: the analysis (`sim/layer_scan.py`; exploratory).

    python designs/rd2/analysis/layer_scan.py <rows dir, e.g. /states/v2/layer_scan_18_21> <output dir>

Each document type's after-reading state (minus the neutral document's), added with no document at layer 18, 19, 20 or
21, at 1 and 2 times its natural size, against a random direction of the same size at 2 times. B's 10 neutral careers
at the 7 and 12 January requests. Each condition minus no injection at the same moment (paired; p by flipping signs by
career, 10,000 times; 95% intervals by resampling careers). Two outcomes: P(the order goes along) after the fixed
neutral reasoning line (every condition), and the agent's own sampled replies (no injection and 1x): how often they go
along, and how often they are unreadable. A moment counts only if the scored orders cover at least half of the model's
probability with no injection.
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
SWEEP = len(sys.argv) > 3 and sys.argv[3] == "SWEEP"
MIN_COVER, PERMS, BOOT = 0.5, 10000, 2000
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
themes = [t for t in dict.fromkeys(r["theme"] for r in rows.values()) if t]
LAYERS = sorted({r["layer"] for r in rows.values() if r["layer"] is not None})
STRENGTHS = sorted({r["strength"] for r in rows.values() if r["kind"] == "push"})
RS = max(r["strength"] for r in rows.values() if r["kind"] == "random")


def test(a, b="none", field="p_order_along"):
    per = {}
    for (cf, _), m in M.items():
        if a in m and b in m:
            per.setdefault(cf, []).append(m[a][field] - m[b][field])
    if len(per) < 2:
        return None
    c = np.array([np.mean(v) for v in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return {"change": float(obs), "p": float(p), "interval": [float(lo), float(hi)]}


cell = lambda r: "–" if r is None else (f"{100 * r['change']:+.1f} (p < 0.001)" if r["p"] < 0.001
                                              else f"{100 * r['change']:+.1f} (p {r['p']:.3f})")
base = 100 * np.mean([m["none"]["p_order_along"] for m in M.values()]) if M else float("nan")
report = [f"# {'Layer sweep' if SWEEP else 'Confirmation scan'}: each document's after-reading state at layers "
          f"{LAYERS[0]}-{LAYERS[-1]} (exploratory)\n",
          f"{len(M)} moments (B's 10 neutral careers at the 7 and 12 January requests; {len(low)} more left out because the "
          "scored orders cover less than half of the model's probability with no injection). Each document type's "
          "after-reading change over the request's update, minus the neutral document's, built on the other half of the "
          "careers and added with no document at one layer. With no injection, P(the order goes along) averages "
          f"{base:.1f}%. Produced by `designs/rd2/analysis/layer_scan.py`.\n",
          "## The read-out: P(the order goes along), change from no injection (points)\n",
          "| Layer | " + " | ".join(f"{t} x{s}" for t in themes for s in STRENGTHS) + f" | random x{RS} |\n"
          + "|---" * (2 + len(themes) * len(STRENGTHS)) + "|"]
summary = {}
for L in LAYERS:
    cells = [cell(test(f"{t} x{s} at layer {L}")) for t in themes for s in STRENGTHS]
    report.append(f"| {L} | " + " | ".join(cells) + f" | {cell(test(f'random x{RS} at layer {L}'))} |")
    summary[L] = {f"{t} x{s}": test(f"{t} x{s} at layer {L}") for t in themes for s in STRENGTHS}
report.append(f"\n**Against the random direction of the same size (x{RS})**\n")
report.append("| Layer | " + " | ".join(themes) + " |\n" + "|---" * (1 + len(themes)) + "|")
for L in LAYERS:
    report.append(f"| {L} | " + " | ".join(cell(test(f"{t} x{RS} at layer {L}", f"random x{RS} at layer {L}"))
                                          for t in themes) + " |")
if "loss" in themes and "gain" in themes and 1 in STRENGTHS:      # (the sweep runs at 2x only)
    report.append("\n**Loss against gain (x1)**: " + "; ".join(
        f"layer {L} {cell(test(f'loss x1 at layer {L}', f'gain x1 at layer {L}'))}" for L in LAYERS) + ".")

# the agent's own words
samp = [r for r in rows.values() if r["replies"] and (r["career_file"], r["history_index"]) in M]
if samp:
    report.append("\n## The agent's own replies (two sampled per moment)\n")
    report.append("| Condition | Replies | Went along | Unreadable |\n|---|---|---|---|")
    for c in sorted({r["condition"] for r in samp}, key=lambda c: (c != "none", c)):
        al = [a for r in samp if r["condition"] == c for a in r["along"]]
        st = [s for r in samp if r["condition"] == c for s in r["status"]]
        report.append(f"| {c} | {len(al)} | {100 * np.mean(al):.0f}% | "
                      f"{100 * np.mean([s not in ('trade', 'hold') for s in st]):.0f}% |")
cov = [m[c]["coverage"] for m in M.values() for c in m]
report.append(f"\nCoverage over the included moments, every condition: median {np.median(cov):.2f}, "
              f"10th percentile {np.percentile(cov, 10):.2f}.")
open(os.path.join(OUT, "LAYER_SWEEP.md" if SWEEP else "LAYER_SCAN.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "layer_sweep.json" if SWEEP else "layer_scan.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "LAYER_SWEEP.md" if SWEEP else "LAYER_SCAN.md"))
