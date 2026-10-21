"""Layer scan for the after-reading state: the analysis (`sim/layer_scan.py`; exploratory).

    python designs/rd2/analysis/layer_scan.py <rows dir, e.g. /states/v2/layer_scan> <output dir>

The loss-specific direction (loss document's after-reading change minus the neutral document's), added with no document at
one layer, at 1-8 times its natural size. Each condition minus no injection at the same moment (paired; p by flipping
signs by career, 10,000 times; 95% intervals by resampling careers), and against a random direction of the same size. A
moment counts only if the scored orders cover at least half of the model's probability with no injection. The
showcase: one fixed moment, one greedy reply per condition.
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
LAYERS, STRENGTHS, RSTR = [12, 14, 16, 18, 20, 22, 24], [1, 2, 4, 8], [4, 8]
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


cell = lambda r: "–" if r is None else (f"{100 * r['change']:+.1f} (p < 0.001)" if r["p"] < 0.001
                                              else f"{100 * r['change']:+.1f} (p {r['p']:.3f})")
cover = lambda c: np.median([m[c]["coverage"] for m in M.values() if c in m]) if M else float("nan")
report = ["# Layer scan: the loss-specific after-reading state, injected without the document (exploratory)\n",
          f"{len(M)} moments (B's neutral careers at their requests; {len(low)} more left out because the scored orders "
          "cover less than half of the model's probability with no injection). The direction is the loss document's "
          "after-reading change over the request's update minus the neutral document's, built on the other half of the "
          "careers; it is added with no document at one layer, from the start of the request's update, at 1 to 8 times its "
          "natural size. P(the order goes along) after the fixed neutral reasoning line, change from no injection in points. "
          "Produced by `designs/rd2/analysis/layer_scan.py`.\n",
          "## Change from no injection\n",
          "| Layer | " + " | ".join(f"x{s}" for s in STRENGTHS) + " | " + " | ".join(f"random x{s}" for s in RSTR) + " |\n"
          + "|---" * (1 + len(STRENGTHS) + len(RSTR)) + "|"]
summary = {}
for L in LAYERS:
    res = {s: test(f"loss-specific x{s} at layer {L}") for s in STRENGTHS}
    rnd = {s: test(f"random x{s} at layer {L}") for s in RSTR}
    report.append(f"| {L} | " + " | ".join(cell(res[s]) for s in STRENGTHS) + " | "
                  + " | ".join(cell(rnd[s]) for s in RSTR) + " |")
    summary[L] = {"push": res, "random": rnd}
report.append("\n## Against the random direction of the same size\n")
report.append("| Layer | " + " | ".join(f"x{s}" for s in RSTR) + " |\n" + "|---" * (1 + len(RSTR)) + "|")
for L in LAYERS:
    vs = {s: test(f"loss-specific x{s} at layer {L}", f"random x{s} at layer {L}") for s in RSTR}
    report.append(f"| {L} | " + " | ".join(cell(vs[s]) for s in RSTR) + " |")
    summary[L]["vs_random"] = vs
report.append("\n## Coverage (median share of the model's probability on the scored orders)\n")
report.append("| Layer | " + " | ".join(f"x{s}" for s in STRENGTHS) + " |\n" + "|---" * (1 + len(STRENGTHS)) + "|")
for L in LAYERS:
    report.append(f"| {L} | " + " | ".join(f"{cover(f'loss-specific x{s} at layer {L}'):.2f}" for s in STRENGTHS) + " |")

show = sorted((r for r in rows.values() if r.get("showcase")), key=lambda r: (r["layer"] or 0, r["kind"], r["strength"]))
if show:
    s0 = show[0]
    report.append(f"\n## The showcase: one moment, one reply per condition\n")
    report.append(f"{s0['career_file']}, {s0['date']} ({s0['chat']}): UBS's request in its neutral wording; UBS wants the "
                  f"price {s0['wants']}. Greedy replies (no sampling), so every difference comes from the injection.\n")
    for r in show:
        text = (r["reply"] or "").strip().replace("\n", " / ")
        report.append(f"**{r['condition']}** (P(along) {100 * r['p_order_along']:.0f}%, reply read as: {r['reply_status']})"
                      f"\n> {text}\n")
open(os.path.join(OUT, "LAYER_SCAN.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "layer_scan.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "LAYER_SCAN.md"))
