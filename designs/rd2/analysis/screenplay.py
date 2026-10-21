"""The screenplay history and the injected end state: the analysis (`sim/screenplay.py`; exploratory).

    python designs/rd2/analysis/screenplay.py <rows dir, e.g. /states/v2/screenplay> <output dir>

F's framed careers at each request after the first. Real: the agent's own replies. Screenplay: its chat replies replaced
by the user's scripted replies (going along, taking on the framing). Injection: the screenplay's state at the request
(averaged over the request update) minus the real one's, added to the real history's request update at one layer.
Outcome: P(the order goes along) after the fixed neutral reasoning line. Each contrast is paired within moment; p by
flipping signs by career (10,000 times); 95% intervals by resampling careers.
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
VERSIONS = ["loss", "gain", "loss + you", "gain + you"]
PERMS, BOOT = 10000, 2000
RNG = np.random.default_rng(20261021)
os.makedirs(OUT, exist_ok=True)

rows = {}
for p in sorted(glob.glob(os.path.join(ROWS, "part*.jsonl"))):
    for line in open(p):
        r = json.loads(line)
        rows[r["key"]] = r
assert rows, f"no rows in {ROWS}"
M, meta = {}, {}
for r in rows.values():
    k = (r["career_file"], r["history_index"])
    M.setdefault(k, {})[(r["condition"], r["framing"])] = r["p_order_along"]
    meta[k] = r
own = lambda k, c: M[k].get((c, meta[k]["version"]))


def test(a, b="real", where=lambda k: True):
    per = {}
    for k in M:
        x, y = own(k, a), own(k, b)
        if where(k) and x is not None and y is not None:
            per.setdefault(k[0], []).append(x - y)
    if len(per) < 2:
        return None
    c = np.array([np.mean(x) for x in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return {"change": float(obs), "p": float(p), "interval": [float(lo), float(hi)], "careers": len(c)}


pts = lambda r: "– | – | –" if r is None else \
    f"{100 * r['change']:+.1f} | {100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f} | {r['p']:.4f}"
mean = lambda c, where=lambda k: True: 100 * np.mean([own(k, c) for k in M if where(k) and own(k, c) is not None])
conds = sorted({r["condition"] for r in rows.values()} - {"screenplay", "real"})
sp = test("screenplay")
report = ["# The screenplay history and the injected end state (exploratory)\n",
          f"{len(M)} moments: F's framed careers at each request after the first. Real: the agent's own replies. "
          "Screenplay: its chat replies replaced by the user's scripted replies (median "
          f"{np.median([meta[k]['replaced'] for k in M]):.0f} replaced before the request). Injection: the screenplay's "
          "state at the request minus the real one's, added to the real history's request update. P(the order goes "
          "along) after the fixed neutral reasoning line, UBS's request in the career's own framing. Produced by "
          "`designs/rd2/analysis/screenplay.py`.\n",
          "## Against the real history (points)\n",
          "| Condition | Mean | Change | 95% interval | p | Share of the screenplay's effect |\n|---|---|---|---|---|---|",
          f"| real | {mean('real'):.1f}% | – | – | – | – |",
          f"| screenplay | {mean('screenplay'):.1f}% | {pts(sp)} | 100% |"]
summary = {"screenplay": sp}
for c in conds:
    r = test(c)
    share = f"{100 * r['change'] / sp['change']:.0f}%" if r and sp and abs(sp["change"]) > 1e-9 else "–"
    report.append(f"| {c} | {mean(c):.1f}% | {pts(r)} | {share} |")
    summary[c] = r
inj = [c for c in conds if c.startswith("inject")]
rnd = [c for c in conds if c.startswith("random")]
if rnd:
    L = rnd[0].split()[-1]
    report.append(f"\nInjection against the random vector of the same size, layer {L}: "
                  f"{pts(test(f'inject at layer {L}', rnd[0])).replace(' | ', ', ')} (change, interval, p).")
    summary["inject_vs_random"] = test(f"inject at layer {L}", rnd[0])

report.append("\n## By the career's framing\n")
report.append("| Framing | Real | Screenplay | Change | 95% interval | p | " + " | ".join(inj) + " |\n" +
              "|---" * (6 + len(inj)) + "|")
summary["by_version"] = {}
for ver in VERSIONS:
    w = lambda k, ver=ver: meta[k]["version"] == ver
    r = test("screenplay", where=w)
    report.append(f"| {ver} | {mean('real', w):.1f}% | {mean('screenplay', w):.1f}% | {pts(r)} | " +
                  " | ".join(f"{100 * x['change']:+.1f} (p {x['p']:.3f})" if (x := test(c, where=w)) else "–" for c in inj) + " |")
    summary["by_version"][ver] = r

report.append("\n## By request\n")
report.append("| Request | Real | Screenplay | Change | 95% interval | p |\n|---|---|---|---|---|---|")
for q in sorted({(meta[k]["date"], meta[k]["chat"]) for k in M}):
    w = lambda k, q=q: (meta[k]["date"], meta[k]["chat"]) == q
    report.append(f"| {q[0]} ({q[1]}) | {mean('real', w):.1f}% | {mean('screenplay', w):.1f}% | {pts(test('screenplay', where=w))} |")

report.append("\n## The screenplay history crossed with UBS's request (percent; rows: the career's framing)\n")
report.append("| History \\ request | " + " | ".join(FRAMINGS) + " |\n" + "|---" * (len(FRAMINGS) + 1) + "|")
for ver in VERSIONS:
    ks = [k for k in M if meta[k]["version"] == ver]
    vals = [100 * np.mean([M[k][("screenplay", f)] for k in ks if ("screenplay", f) in M[k]]) for f in FRAMINGS]
    report.append(f"| {ver} | " + " | ".join(f"{x:.1f}%" for x in vals) + " |")

cov = [r["coverage"] for r in rows.values()]
report.append(f"\nCoverage: median {np.median(cov):.2f}, lowest {min(cov):.2f}. Injection size: median "
              f"{np.median([r['shift_size'] for r in rows.values() if r['condition'].startswith('inject')] or [0]):.1f}.")
open(os.path.join(OUT, "SCREENPLAY.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "screenplay.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "SCREENPLAY.md"))
