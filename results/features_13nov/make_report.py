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
p = os.path.join(D, "map.json")
if os.path.exists(p):
    mp = json.load(open(p))
    con = json.load(open(os.path.join(D, "concepts.json")))

    def kind(v):
        lo, hi = v["ordinary_trade_ci"]
        if lo <= 0 <= hi:
            return "only at the request"
        return "about to trade" if (v["ordinary_trade_gap"] > 0) == (v["went_along_gap"] > 0) else "flips at the request"

    rep.append("\n## F. What kind of thing each decision feature is, on our own episodes\n")
    rep.append(f"`map_features.py`, the {mp['updates']:,} saved updates of A, B, D, E, F joined to what the agent then did. "
               f"Ordinary updates: before the day's first UBS line ({mp['ordinary_updates']:,}; the agent then traded at "
               f"{mp['ordinary_trades']:,}: " + ", ".join(f"{e} {a} of {b}" for e, (a, b) in sorted(mp["ordinary_trades_by_experiment"].items())) + "). "
               "Ordinary-trade gap: the feature where the agent then traded minus where it did not, within experiment, "
               "framing and date, in spread units, with a 95% interval from resampling careers. Kind: **about to trade** "
               "= the ordinary-trade gap has the went-along gap's sign and its interval excludes 0; **flips at the "
               "request** = the interval excludes 0 with the opposite sign; **only at the request** = the interval "
               "includes 0. Pushes toward: the next words the feature's direction raises most (Neuronpedia's "
               "projection of the feature on the output words; a rough guide at these layers). Last column: in how many of "
               "the five experiments, each on its own, the ordinary-trade gap has the pooled gap's sign. The 33 that replicate.\n")
    rep.append("| Feature | Neuronpedia label | Pushes the next word toward | Went-along gap | Ordinary-trade gap (95%) | Kind | Mean at ordinary updates / other UBS lines / requests | Same sign in |\n|---|---|---|---|---|---|---|---|")
    counts = {}
    for k, v in mp["decision"].items():
        if not v["replicates"]:
            continue
        L, f = k.split(":")
        kd = kind(v)
        counts[kd] = counts.get(kd, 0) + 1
        words = ", ".join(w.strip() for w in n.get(k, {}).get("promotes", [])[:5])
        rep.append(f"| {L}/{f} | {lab(L, f)} | {words} | {v['went_along_gap']:+.2f} | {v['ordinary_trade_gap']:+.2f} "
                   f"({v['ordinary_trade_ci'][0]:+.2f} to {v['ordinary_trade_ci'][1]:+.2f}) | {kd} | "
                   f"{v['mean_ordinary']:.0f} / {v['mean_other_ubs_line']:.0f} / {v['mean_request']:.0f} | "
                   f"{sum(1 for x in v['ordinary_trade_gap_by_experiment'].values() if x == x and (x > 0) == (v['ordinary_trade_gap'] > 0))} of 5 |")
    rep.append("\nCounts: " + "; ".join(f"{k} {c}" for k, c in sorted(counts.items())) + ".")
    fam = mp.get("families") or {}
    if fam:
        rep.append(f"Families: across the asked moments (within cell) two features on the same side of the decision "
                   f"correlate {fam['mean_correlation_same_side']:+.2f} on average and two on opposite sides "
                   f"{fam['mean_correlation_opposite_sides']:+.2f}; the first three components hold "
                   + ", ".join(f"{x:.0%}" for x in fam["first_components_share"]) + " of their variance.\n")
    rep.append("\n## G. The dictionary's misconduct features at the requests\n")
    rep.append("`concept_search.py`: Neuronpedia's labels at layers 24, 31 and 41 searched for eight concepts (20 hits "
               f"each; {len(con)} different features). Labelled = similarity of the label to the query of at least 0.55. "
               "On = active at the last token before the reply (the only token our saved states hold: what fires while "
               "the model reads UBS's words is not in them).\n")
    rep.append("| Concept searched | Features labelled | On at 5%+ of the 1,710 requests | On at any request |\n|---|---|---|---|")
    c = mp["concepts"]
    for q in sorted({q for v in con.values() for q in v["queries"]}):
        hits = [k for k, v in con.items() if v["queries"].get(q, 0) >= 0.55]
        rep.append(f"| {q} | {len(hits)} | {sum(c[k]['on_at_requests'] >= 0.05 for k in hits)} | {sum(c[k]['on_at_requests'] > 0 for k in hits)} |")
    rep.append(f"\nOf all {len(c)}, {sum(v['on_at_requests'] == 0 for v in c.values())} are never on at a request. The ones on at 5% or more "
               "(A, request against none: Experiment A's neutral request vs the same moment with no request, within "
               "request, 30 vs 30 moments; went along vs held: within request, experiment and framing):\n")
    rep.append("| Feature | Neuronpedia label | Similarity (concept) | On at requests | On at ordinary updates | A: on with the request / with none (p) | On when went along / held (within-cell gap, p) |\n|---|---|---|---|---|---|---|")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]["on_at_requests"]):
        if v["on_at_requests"] < 0.05:
            continue
        g = "n/a" if v["went_along_gap"] is None else f"{v['went_along_gap']:+.2f}"
        rep.append(f"| {k.replace(':', '/')} | \"{v['label']}\" | {v['best_similarity']:.2f} ({v['best_query']}) | {v['on_at_requests']:.0%} | "
                   f"{v['on_at_ordinary_updates']:.0%} | {v['A_request_on']:.0%} / {v['A_no_request_on']:.0%} ({v['request_vs_none_p']:.3f}) | "
                   f"{v['went_along_on']:.0%} / {v['held_on']:.0%} ({g}, p {v['went_along_p']:.3f}) |")
p = os.path.join(D, "neuronpedia_frames.json")
mj = os.path.join(D, "..", "matched", "matched.json")
if os.path.exists(p) and os.path.exists(mj):
    nf = json.load(open(p))
    mf = json.load(open(mj))["features"]
    rep.append("\n## H. The four frames' features, named (the same moment, only UBS's wording changed)\n")
    rep.append("From `results/matched` (B's saved moments read again with UBS's request in each framing, everything before "
               "it unchanged): the 15 features that differ most per layer, all q < 0.05 there, now with Neuronpedia's "
               "label and the words each pushes the output toward. Loss vs gain: + = higher under the loss frame. Blame "
               "= \"you\" added to the loss frame; credit = \"you\" added to the gain frame: + = higher with \"you\". "
               "Layers 24, 31 and 41 (at layer 12 the pushed-toward words are not readable).\n")
    for title, key in (("Loss frame vs gain frame", "Request: loss frame vs gain frame"),
                       ("Blame: loss + you vs loss", '"You" after loss: loss + you vs loss'),
                       ("Credit: gain + you vs gain", '"You" after gain: gain + you vs gain')):
        for L in ("24", "31", "41"):
            v = mf[key][L]
            rep.append(f"**{title}, layer {L}** ({v['tested']} features tested; {v['q_below_0.05']} with q < 0.05)\n")
            rep.append("| Feature | Difference (spread units) | Neuronpedia label | Pushes the next word toward |\n|---|---|---|---|")
            for r in v["top"]:
                x = nf.get(f"{L}:{r['feature']}", {})
                label = (x.get("label") or "no label on Neuronpedia")[:80]
                words = ", ".join(w.strip() for w in x.get("promotes", [])[:6] if w.strip())
                rep.append(f"| {L}/{r['feature']} | {r['standardised_difference']:+.2f} | {label} | {words} |")
            rep.append("")
rep.append("\n## Examples\n")
for L, v in d["layers"].items():
    rep += [examples(r) for r in v["rows"]]
rep += [examples(r) for r in d["financial"].values()]
open(os.path.join(D, "FEATURES.md"), "w").write("\n".join(rep))
print("written")
