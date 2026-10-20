"""Steering, second run (Stage 1 of the "ideal acquiescence" plan): the analysis (designs/rd2/PREREG_STEER2.md).

    python designs/rd2/analysis/steer2.py <rows dir, e.g. /states/v2/steer2> <output dir>

Each condition is compared with no steering at the same moment (paired; p by flipping signs by career, 10,000 times; 95%
intervals by resampling careers). The four preregistered tests, Holm-corrected together:
- H1, joining (is the direction enough?): B's neutral careers at requests, P(the order goes along): adding the loss
  direction at twice its natural size, minus the mean of the ten random directions at the same size.
- H2, risk-taking: B's neutral careers at trading-day openings, the expected order size: the same contrast.
- H3, joining (is it needed?): B's loss-framed careers at requests: subtracting the loss direction at twice its size,
  minus the mean of the five random directions.
- H4, the direction's sign: B's neutral careers at requests: adding minus subtracting the loss direction (twice its size).
Also: every condition against none, the dose (1, 2 and 4 times), the random directions one by one, the effect request by
request, the sampled replies (going along, unreadable), and the strength Stage 2 would use. And three additions
(exploratory): the going-along direction at layer 24 against random directions at layer 24 (a check on the method), the
transplant of the loss + you version's decision state layer by layer, and how far each condition moves the decision
token's state at layer 24 along the going-along direction (in units of that direction's natural size).
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
PERMS, BOOT = 10000, 2000
RNG = np.random.default_rng(20261022)
VALUE = {"request": "p_order_along", "opening": "expected_size"}
READABLE = ("trade", "hold")
os.makedirs(OUT, exist_ok=True)

rows = {}
for p in sorted(glob.glob(os.path.join(ROWS, "part*.jsonl"))):
    for line in open(p):
        r = json.loads(line)
        rows[r["key"]] = r                                    # a retried part can repeat a row: keep one
rows = list(rows.values())
assert rows, f"no steering rows in {ROWS}: run scripts/modal_steer2.py first"
M = {}                                                        # (group, kind) -> moment -> condition -> row
for r in rows:
    M.setdefault((r["group"], r["kind"]), {}).setdefault((r["career_file"], r["history_index"]), {})[r["condition"]] = r


def val(m, kind, cond, field=None):
    field = field or VALUE[kind]
    if cond.startswith("random mean"):
        tail = cond[len("random mean"):]                  # "" (layer 12) or " at layer 24"
        v = [r[field] for c, r in m.items() if c.startswith("random")
             and (c.endswith(tail) if tail else " at layer" not in c)]
        return float(np.mean(v)) if v else None
    return m[cond][field] if cond in m else None


def contrast(group, kind, a, b="none", where=lambda m: True, field=None):
    """a minus b at each moment, averaged within career; p by flipping signs by career; interval by resampling careers."""
    per = {}
    for key, m in M.get((group, kind), {}).items():
        x, y = val(m, kind, a, field), val(m, kind, b, field)
        if x is None or y is None or not where(m):
            continue
        per.setdefault(key[0], []).append(x - y)
    if len(per) < 2:
        return None
    c = np.array([np.mean(v) for v in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return {"change": float(obs), "p": float(p), "interval": [float(lo), float(hi)], "careers": len(c),
            "moments": int(sum(len(v) for v in per.values()))}


def fmt(r, kind):
    if r is None:
        return "– | – | –"
    if kind == "request":
        return f"{100 * r['change']:+.1f} points | {100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f} | {r['p']:.4f}"
    return f"{r['change']:+,.0f} oz | {r['interval'][0]:+,.0f} to {r['interval'][1]:+,.0f} | {r['p']:.4f}"


def holm(ps):
    order = np.argsort(ps)
    adj, run = np.empty(len(ps)), 0.0
    for i, j in enumerate(order):
        run = max(run, min(1.0, (len(ps) - i) * ps[j]))
        adj[j] = run
    return adj


report = ["# Steering, second run (Stage 1): the frame direction added by hand at B's saved decisions\n",
          f"{len(rows)} rows from `scripts/modal_steer2.py`; analysis `designs/rd2/analysis/steer2.py`; design and "
          "hypotheses `designs/rd2/PREREG_STEER2.md`. The direction (loss and loss + you request minus the neutral "
          "request, the history held fixed) and its natural size come from the other half of the careers. Requests: "
          "P(the order goes along) after a fixed neutral reasoning line. Openings (each trading day's first update): "
          "the expected size of the order. Paired with no steering at the same moment.\n"]
summary = {}

# ---------------- the preregistered tests
tests = [("H1 joining: neutral careers, requests, +loss x2 minus random x2", "neutral", "request", "+loss x2", "random mean"),
         ("H2 risk-taking: neutral careers, openings, +loss x2 minus random x2", "neutral", "opening", "+loss x2", "random mean"),
         ("H3 joining: loss-framed careers, requests, -loss x2 minus random x2", "loss", "request", "-loss x2", "random mean"),
         ("H4 the sign: neutral careers, requests, +loss x2 minus -loss x2", "neutral", "request", "+loss x2", "-loss x2")]
res = [contrast(g, k, a, b) for _, g, k, a, b in tests]
ok = [r for r in res if r is not None]
adj = holm([r["p"] for r in ok]) if ok else []
report.append("## The four preregistered tests (Holm-corrected together)\n")
report.append("| Test | Change | 95% interval | p | Holm p | Careers |\n|---|---|---|---|---|---|")
summary["tests"] = {}
i = 0
for (name, g, k, a, b), r in zip(tests, res):
    if r is None:
        report.append(f"| {name} | – | – | – | – | – |")
        continue
    r["holm_p"] = float(adj[i]); i += 1
    report.append(f"| {name} | {fmt(r, k)} | {r['holm_p']:.4f} | {r['careers']} |")
    summary["tests"][name] = r

# ---------------- the additions (exploratory)
A24 = " at layer 24"
checks = [("Check: neutral careers, requests, +along x2 minus random x2, both at layer 24", "neutral", "request",
           "+along x2" + A24, "random mean" + A24),
          ("Check: loss-framed careers, requests, -along x2 minus random x2, both at layer 24", "loss", "request",
           "-along x2" + A24, "random mean" + A24)]
report.append("\n## The going-along direction at layer 24 (a check on the method; exploratory)\n")
report.append("| Contrast | Change | 95% interval | p | Careers |\n|---|---|---|---|---|")
summary["checks"] = {}
for name, g, k, a, b in checks:
    r = contrast(g, k, a, b)
    report.append(f"| {name} | {fmt(r, k)} | {r['careers'] if r else '–'} |")
    summary["checks"][name] = r

if ("neutral", "request") in M:
    report.append("\n## The transplant: the loss + you version's decision state copied into the neutral version of the "
                  "same moment (neutral careers, requests; exploratory)\n")
    report.append("| Condition | Change in P(along) | 95% interval | p |\n|---|---|---|---|")
    summary["transplant"] = {}
    tr = sorted({c for m in M[("neutral", "request")].values() for c in m if c.startswith(("framed", "transplant"))},
                key=lambda c: (not c.startswith("framed"), int(c.split()[-1]) if c[-1].isdigit() else 0))
    for c in tr:
        r = contrast("neutral", "request", c)
        report.append(f"| {c} | {fmt(r, 'request')} |")
        summary["transplant"][c] = r

    report.append("\n## Does the push reach the decision? The decision token's state at layer 24, moved along the "
                  "going-along direction (units of its natural size; neutral careers, requests; exploratory)\n")
    report.append("| Condition | Change | 95% interval | p |\n|---|---|---|---|")
    summary["reaches_decision"] = {}
    conds = sorted({c for m in M[("neutral", "request")].values() for c in m if c != "none"})
    for c in conds:
        r = contrast("neutral", "request", c, field="along_projection")
        if r is None:
            continue
        size = np.mean([m["none"]["along_size"] for m in M[("neutral", "request")].values() if "none" in m])
        r = {**r, "change": r["change"] / size, "interval": [x / size for x in r["interval"]]}
        report.append(f"| {c} | {r['change']:+.2f} | {r['interval'][0]:+.2f} to {r['interval'][1]:+.2f} | {r['p']:.4f} |")
        summary["reaches_decision"][c] = r

# ---------------- every condition against none
for (g, k) in [("neutral", "request"), ("neutral", "opening"), ("loss", "request")]:
    if (g, k) not in M:
        continue
    conds = sorted({c for m in M[(g, k)].values() for c in m if c != "none"},
                   key=lambda c: (c.startswith("random"), c.replace("-", "~")))
    label = {"neutral": "B's neutral careers", "loss": "B's loss and loss + you careers"}[g]
    report.append(f"\n## {label}, {'requests' if k == 'request' else 'trading-day openings'}: each condition against "
                  f"no steering\n")
    report.append("| Condition | Change | 95% interval | p | Moments |\n|---|---|---|---|---|")
    summary.setdefault("conditions", {})[f"{g} {k}"] = {}
    for c in conds:
        r = contrast(g, k, c)
        report.append(f"| {c} | {fmt(r, k)} | {r['moments'] if r else '–'} |")
        summary["conditions"][f"{g} {k}"][c] = r
    rnd = [summary["conditions"][f"{g} {k}"][c]["change"] for c in conds if c.startswith("random")
           and " at layer" not in c and summary["conditions"][f"{g} {k}"][c]]
    for c in ("+loss x2", "-loss x2"):
        rr = summary["conditions"][f"{g} {k}"].get(c)
        if rr and rnd:
            beyond = sum(abs(rr["change"]) > abs(x) for x in rnd)
            report.append(f"\n{c}: larger in size than {beyond} of the {len(rnd)} random directions at the same size.")

# ---------------- request by request (does steering still move the later requests?)
if ("neutral", "request") in M:
    dates = sorted({(m["none"]["date"], m["none"]["chat"]) for m in M[("neutral", "request")].values() if "none" in m})
    report.append("\n## Request by request: +loss x2 against no steering and against the random directions (neutral "
                  "careers)\n")
    report.append("| Request | P(along), no steering | +loss x2 vs none | +loss x2 vs random x2 |\n|---|---|---|---|")
    summary["by_request"] = {}
    for d, c in dates:
        w = lambda m, d=d, c=c: "none" in m and m["none"]["date"] == d and m["none"]["chat"] == c
        base = np.mean([m["none"]["p_order_along"] for m in M[("neutral", "request")].values() if w(m)])
        a, b = contrast("neutral", "request", "+loss x2", where=w), contrast("neutral", "request", "+loss x2", "random mean", where=w)
        short = lambda r: "–" if r is None else f"{100 * r['change']:+.1f} ({100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f})"
        report.append(f"| {d} ({c}) | {100 * base:.1f}% | {short(a)} | {short(b)} |")
        summary["by_request"][f"{d} {c}"] = {"base": float(base), "vs_none": a, "vs_random": b}

# ---------------- sampled replies, and the strength for Stage 2
sampled = [r for r in rows if r["replies"]]
if sampled:
    report.append("\n## Sampled replies (neutral careers, requests; two per moment)\n")
    report.append("| Condition | Replies | Went along | Unreadable |\n|---|---|---|---|")
    summary["sampled"] = {}
    for c in sorted({r["condition"] for r in sampled}, key=lambda c: (c != "none", c.startswith("random"), c)):
        st = [s for r in sampled if r["condition"] == c for s in r["status"]]
        al = [a for r in sampled if r["condition"] == c for a in r["along"]]
        unread = float(np.mean([s not in READABLE for s in st]))
        report.append(f"| {c} | {len(st)} | {100 * np.mean(al):.0f}% | {100 * unread:.0f}% |")
        summary["sampled"][c] = {"replies": len(st), "went_along": float(np.mean(al)), "unreadable": unread}
    base = summary["sampled"].get("none", {}).get("unreadable", 0.0)
    fine = [s for s in (1, 2, 4) if f"+loss x{s}" in summary["sampled"]
            and summary["sampled"][f"+loss x{s}"]["unreadable"] <= base + 0.10]
    pick = max(fine) if fine else None
    report.append(f"\n**Strength for Stage 2** (the largest of 1, 2 and 4 times whose sampled replies are unreadable no "
                  f"more than 10 points above no steering): {pick if pick else 'none qualifies'}.\n")
    summary["stage2_strength"] = pick

open(os.path.join(OUT, "STEER2.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "steer2.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "STEER2.md"))
