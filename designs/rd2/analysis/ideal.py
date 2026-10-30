"""The ideal history: the analysis (designs/rd2/DESIGN_IDEAL_HISTORY.md; exploratory).

    python designs/rd2/analysis/ideal.py <rows dir, e.g. /states/v2/ideal> <output dir>

F's framed careers at each request after the first; the real history (the agent's own replies) and the ideal one (its
earlier refusals replaced by real Gemma replies that went along), with UBS's request in each of its five framings.
Outcome: P(the order goes along) after the fixed neutral reasoning line. Ideal minus real is paired within moment; p by
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
# 5 August's request asks for a price (QUOTE), not an order: a moment counts only if the scored orders cover at least
# half the model's probability in its plain read
MIN_COVER = 0.5
LOW = {(r["career_file"], r["history_index"]) for r in rows.values()
       if r["record"] == "real" and r["framing"] == r["version"] and r["coverage"] < MIN_COVER}
rows = {k: r for k, r in rows.items() if (r["career_file"], r["history_index"]) not in LOW}
M, meta = {}, {}
for r in rows.values():
    k = (r["career_file"], r["history_index"])
    M.setdefault(k, {})[(r["record"], r["framing"])] = r["p_order_along"]
    meta[k] = r
moments = {k: v for k, v in M.items() if len(v) == 2 * len(FRAMINGS)}


def test(f, where=lambda k: True):
    per = {}
    for k, v in moments.items():
        if where(k):
            per.setdefault(k[0], []).append(f(v, k))
    if len(per) < 2:
        return None
    c = np.array([np.mean(x) for x in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return {"change": float(obs), "p": float(p), "interval": [float(lo), float(hi)], "careers": len(c)}


pts = lambda r: "– | – | –" if r is None else \
    f"{100 * r['change']:+.1f} | {100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f} | {r['p']:.4f}"
own = lambda v, k: v[("ideal", meta[k]["version"])] - v[("real", meta[k]["version"])]      # the career's own framing
pooled = lambda v, k: np.mean([v[("ideal", f)] - v[("real", f)] for f in FRAMINGS])
swapped = [meta[k]["swapped"] for k in moments]
report = ["# The ideal history (exploratory)\n",
          f"{len(moments)} moments: F's framed careers (UBS's lines from B's file and Bank C, one framing) at each request "
          "after the first. Real: the agent's own replies. Ideal: its earlier refusals replaced by real Gemma replies that "
          f"went along at the same request in careers of the same framing (per moment: median {np.median(swapped):.0f} "
          f"replaced, {sum(meta[k]['missing'] for k in moments)} refusals with no replacement in all). P(the order goes "
          "along) after the fixed neutral reasoning line, in percent. Produced by `designs/rd2/analysis/ideal.py`.\n",
          "## Ideal minus real (points)\n",
          "| Contrast | Change | 95% interval | p |\n|---|---|---|---|",
          f"| UBS's request in the career's own framing | {pts(test(own))} |",
          f"| Pooled over UBS's five framings | {pts(test(pooled))} |",
          f"| Only moments where something was replaced | {pts(test(own, lambda k: meta[k]['swapped'] > 0))} |"]
summary = {"own_framing": test(own), "pooled": test(pooled)}

report.append("\n## By the career's framing (UBS's request in that framing)\n")
report.append("| Framing | Real | Ideal | Ideal minus real | 95% interval | p |\n|---|---|---|---|---|---|")
summary["by_version"] = {}
for ver in VERSIONS:
    w = lambda k, ver=ver: meta[k]["version"] == ver
    ks = [k for k in moments if w(k)]
    real = 100 * np.mean([moments[k][("real", ver)] for k in ks])
    ide = 100 * np.mean([moments[k][("ideal", ver)] for k in ks])
    r = test(own, w)
    report.append(f"| {ver} | {real:.1f}% | {ide:.1f}% | {pts(r)} |")
    summary["by_version"][ver] = {"real": real, "ideal": ide, "test": r}

report.append("\n## By request (UBS's request in the career's own framing)\n")
report.append("| Request | Real | Ideal | Ideal minus real | 95% interval | p |\n|---|---|---|---|---|---|")
summary["by_request"] = {}
for q in sorted({(meta[k]["date"], meta[k]["chat"]) for k in moments}):
    w = lambda k, q=q: (meta[k]["date"], meta[k]["chat"]) == q
    ks = [k for k in moments if w(k)]
    real = 100 * np.mean([moments[k][("real", meta[k]["version"])] for k in ks])
    ide = 100 * np.mean([moments[k][("ideal", meta[k]["version"])] for k in ks])
    r = test(own, w)
    report.append(f"| {q[0]} ({q[1]}) | {real:.1f}% | {ide:.1f}% | {pts(r)} |")
    summary["by_request"][f"{q[0]} {q[1]}"] = {"real": real, "ideal": ide, "test": r}

report.append("\n## The ideal history crossed with UBS's request (percent; rows: the career's framing)\n")
report.append("| History \\ request | " + " | ".join(FRAMINGS) + " |\n" + "|---" * (len(FRAMINGS) + 1) + "|")
summary["crossed"] = {}
for ver in VERSIONS:
    ks = [k for k in moments if meta[k]["version"] == ver]
    for rec in ("real", "ideal"):
        vals = [100 * np.mean([moments[k][(rec, f)] for k in ks]) for f in FRAMINGS]
        report.append(f"| {ver} ({rec}) | " + " | ".join(f"{x:.1f}%" for x in vals) + " |")
        summary["crossed"][f"{ver} {rec}"] = dict(zip(FRAMINGS, vals))

cov = [r["coverage"] for r in rows.values()]
report.append(f"\nCoverage: median {np.median(cov):.2f}, lowest {min(cov):.2f}.")
open(os.path.join(OUT, "IDEAL.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "ideal.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "IDEAL.md"))
