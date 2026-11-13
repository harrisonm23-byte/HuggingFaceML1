"""FEATURES.md from decision_features.json, neuronpedia.json and (if present) dim2339_unrelated.json.

    python make_report.py <dir with the json files>
"""
import json, os, sys

D = sys.argv[1]
d = json.load(open(os.path.join(D, "decision_features.json")))
n = json.load(open(os.path.join(D, "neuronpedia.json")))
ORDER = ["2011-01-07", "2011-01-12", "2011-04-01", "2011-06-08", "2011-08-05"]


def lab(L, f):
    v = n.get(f"{L}:{f}", {})
    return f'"{v["label"]}"' if v.get("label") else "no label on Neuronpedia"


def dates(r):
    out = []
    for k, v in r["by_date"].items():
        if k.startswith(("2011-01-07", "2011-01-12")):
            out.append(f"{'7 Jan' if k.startswith('2011-01-07') else '12 Jan'} {v['z']:+.2f} (p {v['p']:.3f})")
    return "; ".join(out)


def framing(r):
    q = r["framing_loss_vs_gain_q"]
    if q is None:
        return "not active enough in B to test"
    return f"yes (q {q:.3f}, {'loss' if r['framing_loss_vs_gain_z'] > 0 else 'gain'} higher)" if q < 0.05 else f"no (q {q:.2f})"


def row(r):
    L, f = r["layer"], r["feature"]
    return (f"| {L} | [{f}]({r['neuronpedia']}) | {lab(L, f)} | {r['mean_went_along']:.1f} / {r['mean_held']:.1f} | "
            f"{r['within_cell_difference']:+.1f} ({r['effect_spread_units']:+.2f}) | {'yes' if r['replicates'] else 'no'} ({r['half1']:+.2f} / {r['half2']:+.2f}, p {r['half2_p']:.3f}) | "
            f"{framing(r)} | {dates(r)} |")


HEAD = ("| Layer | Feature | Neuronpedia label | Mean activation, went along / held (all moments) | Effect: within-cell "
        "difference, activation (spread units) | Replicates (half 1 / half 2, p) | Framing feature (B loss vs gain) | "
        "Within one request alone (7 Jan; 12 Jan) |\n|---|---|---|---|---|---|---|---|")


def examples(r):
    L, f = r["layer"], r["feature"]
    v = n.get(f"{L}:{f}", {})
    out = [f"**{L}/{f}** ({lab(L, f)})", "", "Neuronpedia top examples (peak token in [[ ]]):"]
    out += [f"- {e['max']}: `{e['text'][:160]}`" for e in v.get("examples", [])] or ["- none stored"]
    out += ["", "Top moments in our episodes (the agent's reply at that request):"]
    for m in r["top_moments"]:
        out.append(f"- {m['activation']:.0f}: {m['date']}, {m['experiment']}, {m['framing']}, "
                   f"{'went along' if m['went_along'] else 'held' if m['asked'] else 'no request'}: "
                   f"\"{m['reply'][:160].replace(chr(10), ' ')}...\"")
    return "\n".join(out) + "\n"


rep = ["# Decision features, named (13 Nov; exploratory)\n",
       "Gemma Scope 2 (16k, residual stream) on Run 1's saved request states (1,740 moments, all experiments; 286 went "
       "along). Decision features: q < 0.05 for went along vs held within request, experiment and framing (1,000 "
       "within-cell reshuffles; the comparison of `results/inside_full_career`, which reported 24 / 17 / 18 with its "
       "own reshuffles; this run finds the counts below). Replicates: found on half the careers, same sign and p < 0.05 "
       "on the other half. Framing feature: q < 0.05 for UBS's loss vs gain frame in B, within request. Within one "
       "request alone: the went-along difference inside 7 Jan's request (145 went along, 140 held) and 12 Jan's (99, "
       "186), the only requests with enough going along (the later four have 4 to 18 went along; their values are in "
       "the json). The pooled means mix cells that go along at different rates, so they can differ in sign from the "
       "within-cell effect. Experiment letters are the paper's. Labels are Neuronpedia's automatic explanations; where it has none, "
       "that is said. Produced by `decision_features.py`, `neuronpedia.py`, `make_report.py`.\n"]
rep.append("## A. Decision features\n")
for L, v in d["layers"].items():
    rep.append(f"**Layer {L}**: {v['features_tested']} features tested, {v['q_below_0.05']} decision features, "
               f"{sum(r['replicates'] for r in v['rows'])} replicate; {v['framing_q_below_0.05']} framing features at this layer.\n")
    rep += [HEAD] + [row(r) for r in sorted(v["rows"], key=lambda r: -abs(r["effect_spread_units"]))] + [""]
rep.append("## B. Financial loss-vs-gain features (layer 24) at the decisions\n")
rep += [HEAD] + [row(r) for r in d["financial"].values()] + [""]
rep.append("At every saved update (" + str(next(iter(d["financial"].values()))["every_update"]["updates"]) + " update states, A, B, D, E, F): "
           + "; ".join(f"{k} on at {v['every_update']['share_on']:.1%} (max {v['every_update']['max']:.0f})" for k, v in d["financial"].items()) + ".\n")
rep.append("## C. Timing: before UBS's request vs at it\n")
for L, t in d["timing"].items():
    rep.append(f"**Layer {L}** ({t['moments']} request moments with every-update states, {t['went_along']} went along; "
               f"experiments {', '.join(t['experiments'])}; the saved request-update state vs the request state: cosine "
               f"median {t['request_update_vs_request_state_cosine_median']:.3f}). Within-cell went-along difference, spread units (p):\n")
    rep.append("| Feature | 30 min before | 15 min before | Request update |\n|---|---|---|---|")
    fs = t["features"]
    for f in fs["request update"]:
        c = [f"{fs[k][f]['z']:+.2f} ({fs[k][f]['p']:.3f})" for k in ("30 min before", "15 min before", "request update")]
        rep.append(f"| {L}/{f} | " + " | ".join(c) + " |")
    rep.append("")
p = os.path.join(D, "dim2339_unrelated.json")
if os.path.exists(p):
    u = json.load(open(p))
    rep.append("## D. Dimension 2339 on unrelated prompts\n\n| Prompt | Layer 12 (last token) | Layer 24 (last token) | Next largest, layer 12 |\n|---|---|---|---|")
    rep += [f"| {x['prompt']} | {x['12']['last']:.0f} | {x['24']['last']:.0f} | {x['12']['next_largest_last']:.0f} |" for x in u]
p = os.path.join(D, "features_vs_state.json")
if os.path.exists(p):
    v = json.load(open(p))
    rep.append("\n## E. Are the decision features the whole difference between going along and holding?\n")
    rep.append(f"`features_vs_state.py`, the {v['moments']} moments with a request ({v['went_along']} went along). Reading "
               "going along with the frozen monitor's recipe (logistic, inputs scaled by their within-cell spread, 5 folds "
               "by career), scored within request (within request, experiment and framing in brackets). The decision "
               "features are chosen again inside each training fold. Last column: the whole state's within-request score "
               "minus the decision features', 95% interval over careers.\n")
    rep.append("| Layer | Whole state | Every dictionary feature on in 5%+ of moments | Decision features only | What the dictionary leaves out | Whole state minus decision features |\n|---|---|---|---|---|---|")
    names = ["whole state", "all dictionary features on in 5%+", "decision features, chosen in each training fold", "what the dictionary leaves out"]
    for L, r in v["layers"].items():
        c = [f"{r['readout'][n]['within_request']:.2f} ({r['readout'][n]['within_cell']:.2f})" for n in names]
        lo, hi = r["readout"][names[2]]["whole_state_minus_this_within_request_ci"]
        rep.append(f"| {L} | " + " | ".join(c) + f" | {lo:.2f} to {hi:.2f} |")
    rep.append("\nThe difference itself (the state where the agent went along minus where it held, within cell, dimension "
               "2339 left out), measured on two halves of the careers: how alike the two halves' differences are, and the "
               "share of the repeating difference carried by the dictionary's rebuild, by the decision features and by "
               "the ones that replicate (one half's difference projected on the other half's rebuilt difference).\n")
    rep.append("| Layer | Cosine between the halves | Whole dictionary | Decision features | Replicating decision features |\n|---|---|---|---|---|")
    for L, r in v["layers"].items():
        h = r["difference_split_half"]
        rep.append(f"| {L} | {h['cosine_between_halves']:.2f} | {h['whole dictionary']:.0%} | {h['decision features']:.0%} | {h['replicating decision features']:.0%} |")
rep.append("\n## Examples\n")
for L, v in d["layers"].items():
    rep += [examples(r) for r in v["rows"]]
rep += [examples(r) for r in d["financial"].values()]
open(os.path.join(D, "FEATURES.md"), "w").write("\n".join(rep))
print("written")
