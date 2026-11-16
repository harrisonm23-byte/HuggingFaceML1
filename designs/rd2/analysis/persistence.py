"""The persistence check's summary (sim/persistence.py, scripts/modal_persistence.py; for B, designs/rd2/PREREG_JOLT.md).

    python designs/rd2/analysis/persistence.py results/persistence/<folder>

Writes PERSISTENCE.md there: for each state pushed once at the top, how much of its imprint is left at the agent's later
decisions (at the first layer above the push that sees the whole conversation and at the last layer), and how far it
moves the agent's order at the key moments: at UBS's requests, P(the order goes along); at the trading mornings,
P(the agent changes its position). Each against no push and against a random push of the same size and layer, with the
career as the unit (sign flips by career, 10,000; intervals by resampling careers).
"""
import glob, json, os, re, sys
import numpy as np

d = sys.argv[1]
runs = [json.load(open(p)) for p in sorted(glob.glob(f"{d}/*.json"))]
assert runs, f"no careers in {d}"
arms = [a for a in runs[0]["arms"] if a != "none"]
full = runs[0]["full_attention_layers"]
last = max(runs[0]["layers"])
rng = np.random.default_rng(20261022)
key = lambda m: (m["date"], m["time"])
moments = [key(m) for m in runs[0]["moments"]]
keys = [key(m) for m in runs[0]["moments"] if m["key"]]
requests = [key(m) for m in runs[0]["moments"] if m.get("request")]
mornings = [k for k in keys if k not in requests]
EMOTIONS = ("loss", "gain", "blame", "credit")


def random_of(a):
    """The random push at the same layer and strength."""
    return re.sub(r"^(fin )?\w+ ", lambda m: (m.group(1) or "") + "random ", a)


def at(r, k):
    return next((m for m in r["moments"] if key(m) == k), None)


def delta(r, a, k, field):
    """An arm's order measure at a key moment minus no push's, in one career (None if missing)."""
    m = at(r, k)
    if not m or "orders" not in m["arms"].get(a, {}) or "orders_none" not in m:
        return None
    return m["arms"][a]["orders"].get(field, 0.0) - m["orders_none"].get(field, 0.0)


def test(x):
    """Mean, 95% interval (resampling careers) and two-sided sign-flip p over careers."""
    x = np.asarray([v for v in x if v is not None], float)
    if len(x) == 0:
        return None
    boot = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(10000)]
    flips = (rng.choice([-1, 1], (10000, len(x))) * x).mean(1)
    p = (np.sum(np.abs(flips) >= abs(x.mean()) - 1e-12) + 1) / 10001
    return x.mean(), np.percentile(boot, 2.5), np.percentile(boot, 97.5), p, len(x)


def fmt(t, scale=100, unit=""):
    if t is None:
        return "–"
    m, lo, hi, p, n = t
    return f"{scale * m:+.1f}{unit} ({scale * lo:+.1f} to {scale * hi:+.1f}; p = {p:.3f})"


def imprint(a, k, layer, field):
    xs = [at(r, k)["arms"][a][str(layer)][field] for r in runs if at(r, k) and str(layer) in at(r, k)["arms"].get(a, {})]
    return np.mean(xs) if xs else None


md = ["# Persistence check: does a state pushed once at the top reach later decisions?\n",
      f"{len(runs)} careers from `{runs[0]['folder']}`, reread at bfloat16 with the text unchanged. Each state is added at "
      f"{', '.join(f'{s:g}' for s in runs[0].get('strengths', [runs[0]['strength']]))} x its natural size at one layer to the "
      "pushed moment (the first 7 January update, with the memo, and the reply under it: about "
      f"{int(np.median([r['region'][1] - r['region'][0] for r in runs])):,} tokens) at every read, as the jolt is kept. "
      f"Layers that see the whole conversation: {', '.join(map(str, full))}. Produced by `designs/rd2/analysis/persistence.py`.\n"]

# ---- the preregistered tests (B; designs/rd2/PREREG_JOLT.md)
primary = [a for a in arms if re.match(r"^(loss|gain|blame|credit) x4 L14$", a)]
if requests and primary:
    later = [k for k in requests if k[0] != "2011-01-07"]
    rnd = "random x4 L14"
    h1 = [np.mean([delta(r, a, k, "p_order_along") for a in primary for k in later]) -
          np.mean([delta(r, rnd, k, "p_order_along") for k in later]) for r in runs]
    morning = ("2011-01-12", "08:00")
    h2 = [np.mean([delta(r, a, morning, "p_change") for a in primary]) - delta(r, rnd, morning, "p_change") for r in runs]
    t1, t2 = test(h1), test(h2)
    md += ["## The preregistered tests (designs/rd2/PREREG_JOLT.md)\n",
           "The four emotional states at layer 14, 4 x, averaged, against the random push at layer 14, 4 x; career by career.\n",
           f"- **H1, the push does not roll to UBS's later requests** (12 Jan to 5 Aug, P(the order goes along), averaged over "
           f"the five): difference {fmt(t1, unit=' points')}. Holds if the interval lies within ±5 points: "
           f"**{'yes' if t1 and -0.05 <= t1[1] and t1[2] <= 0.05 else 'no'}**.",
           f"- **H2, it comes back at the next trading morning** (12 Jan 08:00, P(the agent changes its position)): difference "
           f"{fmt(t2, unit=' points')}. Holds if positive with one-sided p < 0.05: "
           f"**{'yes' if t2 and t2[0] > 0 and t2[3] / 2 < 0.05 else 'no'}**.\n"]

# ---- the orders at the key moments
if requests:
    md += ["## Going along at UBS's requests\n",
           "Change from no push in P(the order goes along), points, mean over careers. Last column: the five later requests "
           "averaged, the state minus the random push at the same layer and strength (interval, p).\n",
           "| Push | " + " | ".join(f"{k[0][5:]} {k[1]}" for k in requests) + " | Later requests, minus random |",
           "|---|" + "---|" * (len(requests) + 1)]
    later = [k for k in requests if k[0] != "2011-01-07"]
    for a in arms:
        cells = [test([delta(r, a, k, "p_order_along") for r in runs]) for k in requests]
        vs = None if a.startswith("random") or random_of(a) not in arms else test(
            [np.mean([delta(r, a, k, "p_order_along") for k in later]) - np.mean([delta(r, random_of(a), k, "p_order_along") for k in later])
             for r in runs])
        md.append(f"| {a} | " + " | ".join("–" if c is None else f"{100 * c[0]:+.1f}" for c in cells) + f" | {fmt(vs)} |")
    md += ["\nFor scale, the framing in words at the same requests (matched rereads of B, Section 5.2.1): the framed request "
           "+25 points at 7 January; the framed history +62 at 12 January and +48 at 1 April; the framed request +9 at the "
           "second 8 June request.\n"]
if mornings or not requests:
    ks = mornings if requests else keys
    md += ["## Opening a position at the trading mornings\n" if requests else "## The agent's order at the key moments\n"]
    kx = ("2011-01-12", "08:00") if ("2011-01-12", "08:00") in ks else ks[0]     # the next trading morning
    md += ["Change from no push in P(the agent changes its position), points, mean over careers"
           + (" (in brackets, toward the stops)" if not requests else "") + f". Last column: {kx[0][5:]} {kx[1]}, the "
           "state minus the random push at the same layer and strength (interval, p).\n",
           "| Push | " + " | ".join(f"{k[0][5:]} {k[1]}" for k in ks) + f" | {kx[0][5:]} {kx[1]}, minus random |",
           "|---|" + "---|" * (len(ks) + 1)]
    for a in arms:
        cells = []
        for k in ks:
            c, t = test([delta(r, a, k, "p_change") for r in runs]), test([delta(r, a, k, "p_order_along") for r in runs])
            cells.append("–" if c is None else f"{100 * c[0]:+.1f}" + ("" if requests or t is None else f" ({100 * t[0]:+.1f})"))
        vs = None if a.startswith("random") or random_of(a) not in arms else test(
            [delta(r, a, kx, "p_change") - delta(r, random_of(a), kx, "p_change") for r in runs if delta(r, a, kx, "p_change") is not None])
        md.append(f"| {a} | " + " | ".join(cells) + f" | {fmt(vs)} |")

# ---- the imprint
by_layer = {}
for a in arms:
    by_layer.setdefault(runs[0]["arms"][a]["layer"], []).append(a)
show = []
for date in dict.fromkeys(k[0] for k in moments):
    ks = [k for k in moments if k[0] == date]
    show += [k for k in ks if k in (ks[0], ks[-1]) or k in keys]
for L, names in sorted(by_layer.items()):
    first = min([x for x in full if x > L] or [last])
    for layer in dict.fromkeys([first, last]):
        md += [f"\n## Pushed at layer {L}: what is left at layer {layer}\n",
               "Share of the push's change at the pushed moment that is left at the later decision (cosine: whether it "
               "still points the same way), mean over careers.\n",
               "| Moment | Tokens after the push | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
        for k in dict.fromkeys(show):
            ta = int(np.median([at(r, k)["tokens_after_push"] for r in runs if at(r, k)]))
            md.append(f"| {k[0]} {k[1]} | {ta:,} | " + " | ".join(
                "–" if imprint(a, k, layer, "left") is None else f"{100 * imprint(a, k, layer, 'left'):.0f}% (cos {imprint(a, k, layer, 'cos'):+.2f})"
                for a in names) + " |")
open(f"{d}/PERSISTENCE.md", "w").write("\n".join(md) + "\n")
print("\n".join(md))
