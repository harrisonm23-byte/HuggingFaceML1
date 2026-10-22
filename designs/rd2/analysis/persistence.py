"""The persistence check's summary (sim/persistence.py, scripts/modal_persistence.py).

    python designs/rd2/analysis/persistence.py results/persistence/<folder>

Writes PERSISTENCE.md there: for each state pushed once at the top (at each layer), how much of its imprint is left at
the agent's later decisions, by moment, at the first layer above the push that sees the whole conversation and at the
last layer; and how far it moves the agent's order at the key moments, each against a random push of the same size.
"""
import glob, json, os, sys
import numpy as np

d = sys.argv[1]
runs = [json.load(open(p)) for p in sorted(glob.glob(f"{d}/*.json"))]
assert runs, f"no careers in {d}"
arms = [a for a in runs[0]["arms"] if a != "none"]
full = runs[0]["full_attention_layers"]
last = max(runs[0]["layers"])                      # the model's last layer
by_layer = {}
for a in arms:
    by_layer.setdefault(runs[0]["arms"][a]["layer"], []).append(a)
moments = [(m["date"], m["time"]) for m in runs[0]["moments"]]


def cell(a, key, layer, field):
    xs = []
    for r in runs:
        m = next((m for m in r["moments"] if (m["date"], m["time"]) == key), None)
        if m and a in m["arms"] and str(layer) in m["arms"][a]:
            xs.append(m["arms"][a][str(layer)][field])
    return np.mean(xs) if xs else None


def tokens_after(key):
    return int(np.median([m["tokens_after_push"] for r in runs for m in r["moments"] if (m["date"], m["time"]) == key]))


def show(keys):
    """The moments shown in the imprint tables: the first and last update of each day and the key moments."""
    out = []
    for date in dict.fromkeys(k[0] for k in keys):
        ks = [k for k in keys if k[0] == date]
        out += [k for k in ks if k in (ks[0], ks[-1]) or any(m["key"] for m in runs[0]["moments"] if (m["date"], m["time"]) == k)]
    return list(dict.fromkeys(out))


md = [f"# Persistence check: does a state pushed once at the top reach later decisions?\n",
      f"{len(runs)} careers from `{runs[0]['folder']}`, reread at bfloat16 with the text unchanged. Each state is added at "
      f"{runs[0]['strength']:g} x its natural size at one layer to the pushed moment (the first 7 January update, with "
      "the memo, and the reply under it: about {:,} tokens) at every read, as the jolt is kept. \"Left\" is the push's change "
      "to the agent's state at a later decision as a share of its change at the pushed moment itself, at the same layer "
      "(1 = all of it); \"cos\" whether it still points the same way. Layers that see the whole conversation: {}. Means "
      "over careers. Produced by `designs/rd2/analysis/persistence.py`.\n".format(
          int(np.median([r["region"][1] - r["region"][0] for r in runs])), ", ".join(map(str, full)))]
for L, names in sorted(by_layer.items()):
    first = min([x for x in full if x > L] or [last])
    for layer in dict.fromkeys([first, last]):
        md += [f"\n## Pushed at layer {L}: what is left at layer {layer}\n",
               "| Moment | Tokens after the push | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names)]
        for k in show(moments):
            vals = [(cell(a, k, layer, "left"), cell(a, k, layer, "cos")) for a in names]
            md.append(f"| {k[0]} {k[1]} | {tokens_after(k):,} | " + " | ".join(
                "–" if l is None else f"{100 * l:.0f}% (cos {c:+.2f})" for l, c in vals) + " |")
md += ["\n## The agent's order at the key moments\n",
       "Change from no push: P(the order goes toward the stops) in points, the expected position it sets (oz), and "
       "P(it changes its position) in points; in brackets, the careers where it moved toward the stops.\n",
       "| Moment | Push | Toward the stops | Expected position | Changes position |", "|---|---|---|---|---|"]
for k in [k for k in moments if any(m["key"] for m in runs[0]["moments"] if (m["date"], m["time"]) == k)]:
    for a in arms:
        dd = []
        for r in runs:
            m = next((m for m in r["moments"] if (m["date"], m["time"]) == k), None)
            if m and "orders" in m["arms"].get(a, {}) and "orders_none" in m:
                o, n = m["arms"][a]["orders"], m["orders_none"]
                dd.append((o.get("p_order_along", 0) - n.get("p_order_along", 0), o["expected_size"] - n["expected_size"],
                           o["p_change"] - n["p_change"]))
        if dd:
            x = np.array(dd)
            md.append(f"| {k[0]} {k[1]} | {a} | {100 * x[:, 0].mean():+.1f} ({int((x[:, 0] > 0).sum())}/{len(x)}) | "
                      f"{x[:, 1].mean():+,.0f} | {100 * x[:, 2].mean():+.1f} |")
open(f"{d}/PERSISTENCE.md", "w").write("\n".join(md) + "\n")
print("\n".join(md))
