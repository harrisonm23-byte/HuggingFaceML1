"""Incidental emotion before UBS's request: the analysis (exploratory; the user, 21 Oct).

    python designs/rd2/analysis/prime.py <rows dir, e.g. /states/v2/prime> <output dir>

B's neutral careers at their six requests (60 moments), each read 25 ways: no document or one of the author's emotion
documents (loss, blame, gain, credit) just before UBS's request, times the request's five framings. Outcome: P(the order
goes along) after the fixed neutral reasoning line. Paired within moment; p by flipping signs by career (10,000 times);
95% intervals by resampling careers.
Tested: each document against none (UBS neutral); and the user's two crossed predictions: after blame, a credit-framed
request (gain + you) lands harder than without a document (relief); after credit, a blame-framed request (loss + you)
lands harder than without a document (avoiding blame). "Lands harder" = the framing's effect over the neutral request,
with the document minus without it.
"""
import glob, json, os, sys
import numpy as np

ROWS, OUT = sys.argv[1], sys.argv[2]
PRIMES = ["none", "neutral", "loss", "blame", "gain", "credit"]
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
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
       if r["prime"] == "none" and r["framing"] == "neutral" and r["coverage"] < MIN_COVER}
rows = {k: r for k, r in rows.items() if (r["career_file"], r["history_index"]) not in LOW}
M = {}
for r in rows.values():
    M.setdefault((r["career_file"], r["history_index"]), {})[(r["prime"], r["framing"])] = r["p_order_along"]
moments = {k: v for k, v in M.items() if len(v) == len(PRIMES) * len(FRAMINGS)}
if not moments:                                       # before the neutral documents ran: the four emotion documents only
    PRIMES = [p for p in PRIMES if p != "neutral"]
    moments = {k: v for k, v in M.items() if all((p, f) in v for p in PRIMES for f in FRAMINGS)}


def test(f):
    """f(moment's 25 values) -> a number; mean over careers, p by sign flips, interval by resampling careers."""
    per = {}
    for (cf, _), v in moments.items():
        per.setdefault(cf, []).append(f(v))
    c = np.array([np.mean(x) for x in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return {"change": float(obs), "p": float(p), "interval": [float(lo), float(hi)], "careers": len(c)}


pts = lambda r: f"{100 * r['change']:+.1f} | {100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f} | {r['p']:.4f}"
report = ["# Incidental emotion before UBS's request (exploratory)\n",
          f"{len(moments)} moments (B's neutral careers at their requests), each read in 25 versions: no document or one of "
          "the author's emotion documents just before UBS's request (a different document per moment), times the "
          "request's five framings. P(the order goes along) after the fixed neutral reasoning line, in percent. Produced "
          "by `designs/rd2/analysis/prime.py` from `scripts/modal_prime.py`.\n",
          "## P(the order goes along): document read (rows) x UBS's framing (columns)\n",
          "| Document \\ request | " + " | ".join(FRAMINGS) + " |\n" + "|---" * (len(FRAMINGS) + 1) + "|"]
summary = {"table": {}}
for p in PRIMES:
    vals = [100 * np.mean([v[(p, f)] for v in moments.values()]) for f in FRAMINGS]
    report.append(f"| {p} | " + " | ".join(f"{x:.1f}%" for x in vals) + " |")
    summary["table"][p] = dict(zip(FRAMINGS, vals))

report.append("\n## Each document against none, UBS's request neutral (points)\n")
report.append("| Document | Change | 95% interval | p |\n|---|---|---|---|")
summary["document_vs_none"] = {}
for p in PRIMES[1:]:
    r = test(lambda v, p=p: v[(p, "neutral")] - v[("none", "neutral")])
    report.append(f"| {p} | {pts(r)} |")
    summary["document_vs_none"][p] = r

if "neutral" in PRIMES:
    report.append("\n## Each emotion document against the neutral document, UBS's request neutral (points): emotion "
                  "itself, beyond reading any document\n")
    report.append("| Document | Change | 95% interval | p |\n|---|---|---|---|")
    summary["document_vs_neutral_document"] = {}
    for p in [x for x in PRIMES if x not in ("none", "neutral")]:
        r = test(lambda v, p=p: v[(p, "neutral")] - v[("neutral", "neutral")])
        report.append(f"| {p} | {pts(r)} |")
        summary["document_vs_neutral_document"][p] = r
    report.append("\nPooled over all five framings:\n")
    report.append("| Document | Change | 95% interval | p |\n|---|---|---|---|")
    for p in [x for x in PRIMES if x not in ("none", "neutral")]:
        r = test(lambda v, p=p: np.mean([v[(p, f)] - v[("neutral", f)] for f in FRAMINGS]))
        report.append(f"| {p} | {pts(r)} |")
        summary["document_vs_neutral_document"][p + " (all framings)"] = r

report.append("\n## The two crossed predictions (points): the framing's effect over the neutral request, with the "
              "document minus without it\n")
report.append("| Prediction | Change | 95% interval | p |\n|---|---|---|---|")
lands = lambda p, f: (lambda v: (v[(p, f)] - v[(p, "neutral")]) - (v[("none", f)] - v[("none", "neutral")]))
preds = [("After blame, a credit-framed request (gain + you) lands harder (relief)", "blame", "gain + you"),
         ("After credit, a blame-framed request (loss + you) lands harder (avoiding blame)", "credit", "loss + you")]
summary["predictions"] = {}
for name, p, f in preds:
    r = test(lands(p, f))
    report.append(f"| {name} | {pts(r)} |")
    summary["predictions"][name] = r

report.append("\n## Every document x framing: how the document changes the framing's effect (points, against no "
              "document)\n")
report.append("| Document | " + " | ".join(FRAMINGS[1:]) + " |\n" + "|---" * len(FRAMINGS) + "|")
summary["interaction"] = {}
for p in PRIMES[1:]:
    cells = []
    for f in FRAMINGS[1:]:
        r = test(lands(p, f))
        cells.append(f"{100 * r['change']:+.1f} ({100 * r['interval'][0]:+.1f} to {100 * r['interval'][1]:+.1f})")
        summary["interaction"][f"{p} x {f}"] = r
    report.append(f"| {p} | " + " | ".join(cells) + " |")

cov = [r["coverage"] for r in rows.values()]
report.append(f"\nCoverage (the share of the model's probability on the orders scored): median {np.median(cov):.2f}, "
              f"lowest {min(cov):.2f}.")
open(os.path.join(OUT, "PRIME.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "prime.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "PRIME.md"))
