"""The layer scan with framed requests: the analysis (`sim/layer_scan.py`, run_item_framed; exploratory).

    python designs/rd2/analysis/layer_scan_framed.py <rows dir, e.g. /states/v2/layer_scan_18_21_framed> <output dir>

B's 10 neutral careers at the 7 and 12 January requests, with UBS's request in each of its five framings. Each document
type's after-reading state (minus the neutral document's) added at layer 19 or 21 at 2 times its size, against a random
direction of the same size. For each framing: each condition minus no injection under that framing (paired; p by
flipping signs by career, 10,000 times). Also the framing's own effect (each framed request minus the neutral one, no
injection) as the yardstick, and the agent's own sampled replies. A moment counts only if the scored orders cover at
least half of the model's probability with the neutral request and no injection.
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
LAYERS, S = [19, 21], 2
MIN_COVER, PERMS = 0.5, 10000
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
    M.setdefault((r["career_file"], r["history_index"]), {})[(r["framing"], r["condition"])] = r
low = {k for k, m in M.items() if ("neutral", "none") not in m or m[("neutral", "none")]["coverage"] < MIN_COVER}
M = {k: m for k, m in M.items() if k not in low}
themes = [t for t in dict.fromkeys(r["theme"] for r in rows.values()) if t]


def test(a, b):
    per = {}
    for (cf, _), m in M.items():
        if a in m and b in m:
            per.setdefault(cf, []).append(m[a]["p_order_along"] - m[b]["p_order_along"])
    if len(per) < 2:
        return None
    c = np.array([np.mean(v) for v in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    return {"change": float(obs), "p": float(p)}


cell = lambda r: "–" if r is None else (f"{100 * r['change']:+.1f} (p < 0.001)" if r["p"] < 0.001
                                              else f"{100 * r['change']:+.1f} (p {r['p']:.3f})")
level = lambda v, c: 100 * np.mean([m[(v, c)]["p_order_along"] for m in M.values() if (v, c) in m])
report = ["# The layer scan with framed requests (exploratory)\n",
          f"{len(M)} moments (B's 10 neutral careers at the 7 and 12 January requests; {len(low)} more left out because the "
          "scored orders cover less than half of the model's probability with the neutral request). UBS's request in each "
          "of its five framings; each document type's after-reading state (minus the neutral document's) added at layer 19 "
          f"or 21 at {S} times its size. P(the order goes along) after the fixed neutral reasoning line. Produced by "
          "`designs/rd2/analysis/layer_scan_framed.py`.\n",
          "## No injection: the framing's own effect\n",
          "| Request | P(along) | Against the neutral request |\n|---|---|---|"]
for v in FRAMINGS:
    report.append(f"| {v} | {level(v, 'none'):.1f}% | "
                  + ("–" if v == "neutral" else cell(test((v, "none"), ("neutral", "none")))) + " |")
summary = {}
for L in LAYERS:
    report.append(f"\n## Layer {L}: each state's change from no injection, under each framing (points)\n")
    report.append("| Request | " + " | ".join(themes) + " | random |\n" + "|---" * (len(themes) + 2) + "|")
    for v in FRAMINGS:
        cells = [cell(test((v, f"{t} x{S} at layer {L}"), (v, "none"))) for t in themes]
        report.append(f"| {v} | " + " | ".join(cells) + f" | {cell(test((v, f'random x{S} at layer {L}'), (v, 'none')))} |")
        summary[f"{L} {v}"] = {t: test((v, f"{t} x{S} at layer {L}"), (v, "none")) for t in themes}
    report.append(f"\nAgainst random at layer {L}: " + "; ".join(
        f"{v}: " + ", ".join(f"{t} {cell(test((v, f'{t} x{S} at layer {L}'), (v, f'random x{S} at layer {L}')))}"
                             for t in themes) for v in FRAMINGS) + ".")

samp = [r for r in rows.values() if r["replies"] and (r["career_file"], r["history_index"]) in M]
if samp:
    report.append("\n## The agent's own replies (two sampled per moment): share that went along\n")
    conds = sorted({r["condition"] for r in samp}, key=lambda c: (c != "none", c))
    report.append("| Request | " + " | ".join(conds) + " |\n" + "|---" * (len(conds) + 1) + "|")
    for v in FRAMINGS:
        cells = []
        for c in conds:
            al = [a for r in samp if r["framing"] == v and r["condition"] == c for a in r["along"]]
            cells.append(f"{100 * np.mean(al):.0f}% ({len(al)})" if al else "–")
        report.append(f"| {v} | " + " | ".join(cells) + " |")
    st = [s for r in samp for s in r["status"]]
    report.append(f"\nUnreadable replies overall: {100 * np.mean([s not in ('trade', 'hold') for s in st]):.0f}%.")
open(os.path.join(OUT, "LAYER_SCAN_FRAMED.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "layer_scan_framed.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "LAYER_SCAN_FRAMED.md"))
