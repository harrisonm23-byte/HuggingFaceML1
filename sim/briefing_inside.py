"""Step 0 (notebook 15, 2026-10-16): the prompts that test what the desk briefing does inside the model, and the measures.

The prompts are the pilot's own briefings (with amount and period variations) plus the test sentences in
data/silver/briefing_probes.json: loss and gain in other words, word flips, money only, threat only, a matched control
for the responsibility sentence with checks in other words, and bad vs good weather. Every prompt is the agent's
conversation on 7 Jan at 08:00 or at 09:30 (UBS's request, after holding at every step), so only the briefing (and, at
09:30, the request) differs.

The measures take any array of states with one row per prompt, so they can be checked without a model
(sim/test_briefing_inside.py): a bag-of-words stand-in, which knows words but no meaning, passes the word-level checks
and not the meaning-level ones; a stand-in that knows single-word valence passes "other words" but not the flips; a
stand-in that knows the meaning passes both.
"""
import hashlib, json, os
from math import comb

import numpy as np
import pandas as pd

from briefing import ROOT, load_briefings, opening_with, turns_at, variants

PROBES = os.path.join(ROOT, "data", "silver", "briefing_probes.json")
DATE, FIRST, REQUEST = "2011-01-07", "08:00", "09:30"
MAIN = ["neutral", "loss", "gain", "loss + you", "gain + you"]     # the pilot's briefings ("no ask" = neutral, no request)
FRAME = {"neutral": None, "loss": "loss", "gain": "gain", "loss + you": "loss", "gain + you": "gain"}
SELECT = ("P1", "P2", "P3")       # the other-words families the dial layer is chosen on; P4-P6 are kept for testing it


def load_probes(path=PROBES):
    return json.load(open(path))


def probes_fingerprint(path=PROBES):
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]


def prompt_rows(b=None, pr=None):
    """One row per prompt: its set, its side, and the keys that match it to its pair (no conversation yet)."""
    b, pr = b or load_briefings(), pr or load_probes()
    rows = []

    def add(**r):
        rows.append({"set": None, "time": FIRST, "version": None, "side": None, "frame": None, "you": False, "asked": True,
                     "amount": None, "period": None, "family": None, "week": None, "text": None, **r})

    def amount_period(label):
        return (int(label[1]) if label.startswith("$") else None), ("quarter" if "quarter" in label else "month")

    rs = pr["responsibility"]
    for when in (FIRST, REQUEST):
        # The pilot's briefings: at 08:00, and at 09:30 with UBS's request and without it
        for v in MAIN:
            for label, text in variants(v, b):
                x, p = amount_period(label)
                for asked in ((True,) if when == FIRST else (True, False)):
                    add(set="main", time=when, version=v if asked else v + " (no request)", side=FRAME[v], frame=FRAME[v],
                        you=v.endswith("+ you"), asked=asked, amount=x, period=p, text=text)
        # The responsibility sentence's control: the same structure and length, without the responsibility
        for v in ("loss", "gain"):
            for label, text in variants(v, b):
                x, p = amount_period(label)
                add(set="you_control", time=when, version=v + " + control sentence", side="control", frame=v, amount=x,
                    period=p, text=text + " " + rs["build_control"])
        for p in pr["periods"]:
            # Loss and gain in other words (both moments, so the meaning can be followed to UBS's request)
            for f in pr["paraphrases"]["families"]:
                for side in ("loss", "gain"):
                    add(set="paraphrase", time=when, version=f"{side} in other words", side=side, frame=side,
                        family=f["family"], amount=4, period=p, text=f[side].format(p=p))
            # Responsibility, 'informed' and neutral sentences in other words, on the plain $4M loss and gain briefings
            for v in ("loss", "gain"):
                base = b["versions"][v].replace("last month", f"last {p}")
                for side, key, name in (("you", "you_paraphrases", "responsibility in other words"),
                                        ("informed", "informed_in_other_words", "'informed' in other words"),
                                        ("neutral", "neutral_sentences", "a neutral sentence")):
                    for k, s in enumerate(rs[key]):
                        add(set="you_check", time=when, version=f"{v} + {name}", side=side, frame=v,
                            family=f"{side[0].upper()}{k + 1}", amount=4, period=p, text=base + " " + s)
    # Word flips, money only, threat only, weather (08:00)
    for p in pr["periods"]:
        for f in pr["flips"]["families"]:
            for side in ("loss", "gain"):
                add(set="flip", version=f"{side} meaning, {'gain' if side == 'loss' else 'loss'} words", side=side,
                    frame=side, family=f["family"], amount=4, period=p, text=f[side + "_meaning"].format(p=p))
        for x in pr["money_only"]["amounts"]:
            for side in ("loss", "gain"):
                add(set="money_only", version=f"{side}, money only", side=side, frame=side, amount=x, period=p,
                    text=pr["money_only"][side].format(x=x, p=p))
        for f in pr["threat_only"]["families"]:
            for side in ("loss", "gain"):
                add(set="threat_only", version=f"{side}, threat only", side=side, frame=side, family=f["family"],
                    period=p, text=f[side].format(p=p))
    for w in pr["weather"]["when"]:
        for f in pr["weather"]["families"]:
            for side in ("bad", "good"):
                add(set="weather", version=f"weather, {side}", side=side, family=f["family"], week=w,
                    text=f[side].format(w=w))
    return pd.DataFrame(rows)


def with_turns(P, framed, setups, b=None):
    """Add each prompt's conversation. The history at a moment is the same for every briefing (the agent has held at
    every step), so it is built once per moment and request, and only the instructions are swapped in."""
    b = b or load_briefings()
    cache, turns = {}, []
    for _, r in P.iterrows():
        key = (r["time"], r["asked"])
        if key not in cache:
            cache[key] = turns_at("(instructions)", "neutral" if r["asked"] else "no ask", DATE, r["time"], framed, setups)
        t = [dict(x) for x in cache[key]]
        t[0] = {"role": "system", "content": opening_with(r["text"], b)}
        turns.append(t)
    P = P.copy()
    P["turns"] = turns
    return P


# ---- the measures (X: one layer's states, one row per prompt) ------------------------------------------------------
def unit(x):
    return x / (np.linalg.norm(x) + 1e-12)


def cos(u, v):
    return float(unit(u) @ unit(v))


def mean_diff(X, a, b):
    return X[a].mean(0) - X[b].mean(0)


def gap(X, d, a, b):
    """The distance between two groups' averages along direction d (in the state's own units if d is a unit vector)."""
    return float((X[a] @ d).mean() - (X[b] @ d).mean())


def pairs(P, a, b, keys):
    """Matched pairs: each prompt in a with each prompt in b that agrees on all the keys."""
    return [(i, k) for i in a for k in b if all(P.at[i, c] == P.at[k, c] for c in keys)]


def order(X, d, prs):
    """Share of pairs (i, k) with i above k along d (ties count half): 0.5 is chance."""
    s = X @ d
    return float(np.mean([1.0 if s[i] > s[k] else 0.5 if s[i] == s[k] else 0.0 for i, k in prs])) if prs else float("nan")


def leave_one_out(X, P, a, b, key, match):
    """Build the direction without one variation, then order that variation's matched pairs."""
    hits = []
    for v in sorted(set(P.loc[a, key]) | set(P.loc[b, key]), key=str):
        ai, bi = [i for i in a if P.at[i, key] != v], [i for i in b if P.at[i, key] != v]
        ao, bo = [i for i in a if P.at[i, key] == v], [i for i in b if P.at[i, key] == v]
        if ai and bi and ao and bo:
            hits += [order(X, unit(mean_diff(X, ai, bi)), [pr]) for pr in pairs(P, ao, bo, match)]
    return float(np.mean(hits)) if hits else float("nan")


def chance(acc, k):
    """How often chance alone gives an ordering this good or better: k independent families, each a coin flip."""
    hits = int(round(acc * k))
    return sum(comb(k, j) for j in range(hits, k + 1)) / 2 ** k


def groups(P):
    """The groups of prompts the measures compare, by name."""
    def idx(**kw):
        m = np.ones(len(P), bool)
        for c, v in kw.items():
            m &= (P[c].isin(v) if isinstance(v, (list, tuple, set)) else P[c] == v).to_numpy()
        return list(P.index[m])
    G = {}
    for when, t in (("8", FIRST), ("9", REQUEST)):
        for a, asked in (("", True), ("_no_request", False)):
            if when == "8" and not asked:
                continue
            for f in ("loss", "gain"):
                G[f"main{when}{a}_{f}"] = idx(set="main", time=t, asked=asked, frame=f)
                G[f"main{when}{a}_{f}_plain"] = idx(set="main", time=t, asked=asked, frame=f, you=False)
            G[f"main{when}{a}_you"] = idx(set="main", time=t, asked=asked, you=True)
            G[f"main{when}{a}_neutral"] = idx(set="main", time=t, asked=asked, version="neutral" if asked else "neutral (no request)")
            G[f"main{when}{a}_all"] = idx(set="main", time=t, asked=asked)
        G[f"control{when}"] = idx(set="you_control", time=t)
        p = "" if when == "8" else "9"
        for side in ("loss", "gain"):
            G[f"paraphrase{p}_{side}"] = idx(set="paraphrase", time=t, side=side)
            G[f"paraphrase{p}_{side}_select"] = idx(set="paraphrase", time=t, side=side, family=SELECT)
            G[f"paraphrase{p}_{side}_test"] = [i for i in G[f"paraphrase{p}_{side}"] if P.at[i, "family"] not in SELECT]
        for side in ("you", "informed", "neutral"):
            G[f"you_check{p}_{side}"] = idx(set="you_check", time=t, side=side)
    G["main8_plain4"] = idx(set="main", time=FIRST, you=False, amount=4, frame=("loss", "gain"))
    G["main8_you4"] = idx(set="main", time=FIRST, you=True, amount=4)
    G["main8_plain_framed"] = G["main8_loss_plain"] + G["main8_gain_plain"]
    for s, sides in (("flip", ("loss", "gain")), ("money_only", ("loss", "gain")), ("threat_only", ("loss", "gain")),
                     ("weather", ("bad", "good"))):
        for side in sides:
            G[f"{s}_{side}"] = idx(set=s, side=side)
    for fam in ("T1", "T2"):
        for side in ("loss", "gain"):
            G[f"threat_{fam}_{side}"] = idx(set="threat_only", side=side, family=fam)
    framed8 = G["main8_loss"] + G["main8_gain"]
    weather, para = G["weather_bad"] + G["weather_good"], G["paraphrase_loss"] + G["paraphrase_gain"]
    half = lambda rows, fams: [i for i in rows if P.at[i, "family"] in fams]
    # Null contrasts: splits that have nothing to do with loss, by one word and by whole sentences (both sides mixed)
    G["null"] = {"$3M vs $5M": ([i for i in framed8 if P.at[i, "amount"] == 3], [i for i in framed8 if P.at[i, "amount"] == 5]),
                 "month vs quarter": ([i for i in framed8 if P.at[i, "period"] == "month"],
                                      [i for i in framed8 if P.at[i, "period"] == "quarter"]),
                 "week vs weekend": ([i for i in weather if P.at[i, "week"] == "week"],
                                     [i for i in weather if P.at[i, "week"] == "weekend"]),
                 "other words P1-P3 vs P4-P6": (half(para, SELECT), [i for i in para if P.at[i, "family"] not in SELECT]),
                 "weather W1-W3 vs W4-W6": (half(weather, ("W1", "W2", "W3")), half(weather, ("W4", "W5", "W6")))}
    return G


def layer_measures(X, P, G):
    """Everything Step 0 asks of one layer. The loss direction is built from the pilot's own briefings at 08:00
    (loss minus gain, with and without the responsibility sentence); the responsibility direction from the
    responsibility sentence minus its matched control sentence. Everything else is tested on other prompts."""
    d = mean_diff(X, G["main8_loss"], G["main8_gain"])
    u = unit(d)
    main_gap = gap(X, u, G["main8_loss"], G["main8_gain"]) + 1e-12
    para_gap = gap(X, u, G["paraphrase_loss"], G["paraphrase_gain"])
    dy = mean_diff(X, G["main8_you"], G["control8"])
    uy = unit(dy)
    m = lambda key: (P.amount.astype(str) + P.period.astype(str) + (P.frame.astype(str) if key == "you" else P.you.astype(str)))
    share = lambda a, b: gap(X, u, G[a], G[b]) / main_gap
    return {
        # Word level: these pass for anything that registers words
        "wording_check": leave_one_out(X, P.assign(variant=m("loss")), G["main8_loss"], G["main8_gain"], "variant", ["variant"]),
        "left_at_0930": share("main9_loss", "main9_gain"),
        "acc_0930": order(X, u, pairs(P, G["main9_loss"], G["main9_gain"], ["amount", "period", "you"])),
        "left_at_0930_no_request": share("main9_no_request_loss", "main9_no_request_gain"),
        "cos_0930_0800": cos(mean_diff(X, G["main9_loss"], G["main9_gain"]), d),
        "you_wording_check": leave_one_out(X, P.assign(variant=m("you")), G["main8_you"], G["control8"], "variant", ["variant"]),
        "you_left_at_0930": gap(X, uy, G["main9_you"], G["control9"]) / (gap(X, uy, G["main8_you"], G["control8"]) + 1e-12),
        # Meaning level: loss and gain in other words, at 08:00 and at UBS's request
        "paraphrase_acc": order(X, u, pairs(P, G["paraphrase_loss"], G["paraphrase_gain"], ["family", "period"])),
        "paraphrase_gap": para_gap / main_gap,
        "select_gap": share("paraphrase_loss_select", "paraphrase_gain_select"),
        "paraphrase_acc_test": order(X, u, pairs(P, G["paraphrase_loss_test"], G["paraphrase_gain_test"], ["family", "period"])),
        "paraphrase_gap_test": share("paraphrase_loss_test", "paraphrase_gain_test"),
        "paraphrase_acc_0930": order(X, u, pairs(P, G["paraphrase9_loss"], G["paraphrase9_gain"], ["family", "period"])),
        "paraphrase_left_at_0930": gap(X, u, G["paraphrase9_loss"], G["paraphrase9_gain"]) / (para_gap + 1e-12),
        # Word flips: the briefing's own words, the opposite meaning
        "flip_acc": order(X, u, pairs(P, G["flip_loss"], G["flip_gain"], ["family", "period"])),
        "flip_gap": share("flip_loss", "flip_gain"),
        # Which part of the briefing: shares of the loss gap (the accuracies reach 1 at any alignment)
        "money_only_gap": share("money_only_loss", "money_only_gain"),
        "threat_gap_T1": share("threat_T1_loss", "threat_T1_gain"),
        "threat_gap_T2": share("threat_T2_loss", "threat_T2_gain"),
        # Bad news in general? Against unrelated splits
        "weather_acc": order(X, u, pairs(P, G["weather_bad"], G["weather_good"], ["family", "week"])),
        "weather_cos": cos(mean_diff(X, G["weather_bad"], G["weather_good"]), d),
        "null_cos_max": max(abs(cos(mean_diff(X, a, b), d)) for a, b in G["null"].values()),
        "request_cos": cos(mean_diff(X, G["main9_all"], G["main9_no_request_all"]), d),
        # Responsibility: checked in other words against neutral sentences (and 'informed' against them, the other side)
        "you_check_acc": order(X, uy, pairs(P, G["you_check_you"], G["you_check_neutral"], ["frame", "period"])),
        "informed_check_acc": order(X, uy, pairs(P, G["you_check_neutral"], G["you_check_informed"], ["frame", "period"])),
        "you_check_acc_0930": order(X, uy, pairs(P, G["you_check9_you"], G["you_check9_neutral"], ["frame", "period"])),
        "any_sentence_cos": cos(mean_diff(X, G["main8_you4"], G["main8_plain4"]), mean_diff(X, G["you_check_neutral"], G["main8_plain4"])),
        "you_loss_cos": cos(dy, d),
    }


WORD_LEVEL = ["wording_check", "left_at_0930", "acc_0930", "left_at_0930_no_request", "cos_0930_0800", "you_wording_check",
              "you_left_at_0930"]
COLUMNS = {
    "wording_check": "Word level. Left-out amount/period of the briefings ordered right (a word counter: 1.0)",
    "left_at_0930": "Word level. The briefings' loss-gain gap at UBS's request (09:30) as a share of 08:00 (a word counter: 1.0)",
    "acc_0930": "Word level. 09:30 briefing pairs ordered right along the 08:00 direction (a word counter: 1.0)",
    "left_at_0930_no_request": "Word level. The same share at 09:30 with no request (a word counter: 1.0)",
    "cos_0930_0800": "Cosine of the 09:30 loss-gain difference with the 08:00 one (low with a gap left: the signal has turned)",
    "you_wording_check": "Word level. Responsibility vs matched control sentence, left-out variation (a word counter: 1.0)",
    "you_left_at_0930": "Word level. The responsibility gap at 09:30 as a share of 08:00 (a word counter: 1.0)",
    "paraphrase_acc": "Loss and gain in other words ordered right along the loss direction, 08:00 (a word counter: 0.5)",
    "paraphrase_gap": "Their loss-gain gap as a share of the briefings' own gap (a word counter: 0)",
    "select_gap": "The same share on families P1-P3 only: the dial layer is chosen on this",
    "paraphrase_acc_test": "Families P4-P6 ordered right (not used to choose the layer)",
    "paraphrase_gap_test": "Their gap share (not used to choose the layer)",
    "paraphrase_acc_0930": "Other words ordered right at UBS's request (09:30), along the 08:00 direction (a word counter: 0.5)",
    "paraphrase_left_at_0930": "Their gap at 09:30 as a share of their gap at 08:00: the meaning left at the request",
    "flip_acc": "Word flips ordered by meaning (a word counter: 0; below 0.5 = the word contrast outweighs the meaning)",
    "flip_gap": "Their gap share (negative = the words win; a word counter: -0.6)",
    "money_only_gap": "Money only (no threat to the desk), share of the loss gap (repeats the briefing's words; a word counter: 0.4)",
    "threat_gap_T1": "Threat only, with closure/expansion, share of the loss gap (a word counter: 0.2)",
    "threat_gap_T2": "Threat only, in other words, share of the loss gap (a word counter: 0)",
    "weather_acc": "Bad above good weather along the loss direction (0.5 = unrelated)",
    "weather_cos": "Cosine of the weather difference with the loss difference",
    "null_cos_max": "Largest cosine of an unrelated split with it ($3M/$5M, month/quarter, week/weekend, families P1-3/P4-6, W1-3/W4-6)",
    "request_cos": "Cosine of UBS's request (with minus without) with the loss difference; read against null_cos_max",
    "you_check_acc": "Responsibility in other words above neutral sentences, along the responsibility direction (a word counter: 0.5)",
    "informed_check_acc": "Neutral sentences above 'informed' in other words: the other side of the same direction (a word counter: 0.5)",
    "you_check_acc_0930": "Responsibility in other words above neutral sentences at UBS's request (a word counter: 0.5)",
    "any_sentence_cos": "Cosine of (+ responsibility) and (+ a neutral sentence), each minus plain: near 1 = it acts like any added sentence",
    "you_loss_cos": "Cosine of the responsibility direction with the loss direction",
}


def choose_layer(LT):
    """The layer for the dial: among the middle layers, the largest share of the loss gap carried by loss and gain in
    other words, on families P1-P3 only, so families P4-P6 and every other check stay untouched by the choice."""
    n = int(LT.layer.max()) + 1
    middle = LT[(LT.layer >= n // 4) & (LT.layer <= 3 * n // 4)]
    return int(middle.sort_values("select_gap", ascending=False).iloc[0]["layer"]), middle


def reading(LT, best, floor=None):
    """Plain-English lines for the printout and summary.md, each against its baseline."""
    r = LT.set_index("layer").loc[best]
    _, middle = choose_layer(LT)
    med = middle.median(numeric_only=True)
    f = (lambda c: f"; summed-embedding floor {floor[c]:.2f}") if floor is not None else (lambda c: "")
    odds = lambda acc, k: (f"by chance, that or better {100 * chance(acc, k):.0f}% of the time" if acc > 0.5
                           else "no better than chance")
    return [
        f"Layer for the dial: {best}, chosen among layers {int(middle.layer.min())}-{int(middle.layer.max())} for the share of "
        f"the loss gap that loss and gain in other words carry, on families P1-P3 only ({r.select_gap:.2f}). Every other "
        "number below is untouched by that choice, apart from the all-family figures, which include P1-P3.",
        f"Word level (a word counter scores 1.0 on all of these, so they show only that the signal is not tied to one amount "
        f"or period, and how much of the word trace lasts): wording check {r.wording_check:.2f}; at UBS's request "
        f"{r.left_at_0930:.2f} of the briefings' gap is left (median {med.left_at_0930:.2f}), {r.left_at_0930_no_request:.2f} "
        f"with no request, pointing the same way as at 08:00 by cosine {r.cos_0930_0800:.2f}.",
        f"Loss and gain in other words (none of loss, profit, closure, expansion): families P4-P6 ordered "
        f"{r.paraphrase_acc_test:.2f} at layer {best} ({odds(r.paraphrase_acc_test, 3)}), "
        f"carrying {r.paraphrase_gap_test:.2f} of the loss gap; all six families {r.paraphrase_acc:.2f} (median "
        f"{med.paraphrase_acc:.2f}{f('paraphrase_acc')}) and {r.paraphrase_gap:.2f} of the gap (median {med.paraphrase_gap:.2f}"
        f"{f('paraphrase_gap')}). A word counter scores 0.5 and 0. Above that rules out the four key words, but it can still "
        "be the good or bad sense of single words (red/black, worse/better): a word-valence stand-in scores 1.0 here, so "
        "the word flips are the test that separates meaning from single words.",
        f"At UBS's request, in other words: ordered {r.paraphrase_acc_0930:.2f}, with {r.paraphrase_left_at_0930:.2f} of their "
        f"08:00 gap left (median {med.paraphrase_left_at_0930:.2f})"
        + (" (their 08:00 gap is near zero, so this share means little)" if r.paraphrase_gap < 0.05 else "")
        + ". This is the meaning-level part that reaches the moment Part B reads and steers.",
        f"Word flips (the briefing's own words, the opposite meaning): ordered {r.flip_acc:.2f} (median {med.flip_acc:.2f}"
        f"{f('flip_acc')}; 3 families: {odds(r.flip_acc, 3)}), gap share {r.flip_gap:+.2f} (median "
        f"{med.flip_gap:+.2f}{f('flip_gap')}). A word counter and a word-valence stand-in score 0 and about -0.6. "
        "Above 0.5 and positive: meaning beats the words. Below: the word contrast outweighs the meaning contrast for these "
        "sentences, which does not mean there is no meaning.",
        f"Which part of the briefing (shares of the loss gap; they need not add up to 1, since the briefing's threat clause "
        f"also says 'a further loss/profit'): money only {r.money_only_gap:.2f}, threat with closure/expansion "
        f"{r.threat_gap_T1:.2f}, threat in other words {r.threat_gap_T2:.2f}. A word counter scores 0.4, 0.2 and 0; only "
        "the last is free of the briefing's words.",
        f"Bad news in general? Bad weather ordered above good {r.weather_acc:.2f} (0.5 = unrelated; 6 families); cosine with "
        f"the loss difference {r.weather_cos:+.2f}, against {r.null_cos_max:.2f} for the largest unrelated split. Well above "
        "that means the loss direction is partly 'bad news'; near it only rules out a general bad-news direction and does "
        f"not show the signal is about money. UBS's request itself: cosine {r.request_cos:+.2f} with the loss difference, "
        "against the same null.",
        f"Responsibility: in other words, above neutral sentences {r.you_check_acc:.2f} (median {med.you_check_acc:.2f}"
        f"{f('you_check_acc')}; a word counter and an 'informed only' stand-in score 0.5), {r.you_check_acc_0930:.2f} at "
        f"UBS's request. Only this side shows responsibility; the other side, neutral above 'informed' in other words, is "
        f"{r.informed_check_acc:.2f}. Like any added sentence: cosine {r.any_sentence_cos:+.2f}. Overlap with the loss "
        f"direction: cosine {r.you_loss_cos:+.2f}.",
    ]


# ---- features (Gemma Scope 2) ----------------------------------------------------------------------------------------
def feature_table(F, P, G, comparisons, top=15, layer=None, sae_file=None, link=None):
    """For each comparison, the features whose average activation differs most, in activation units (not capped by a
    spread taken over the two groups). Each feature's own null is its largest difference across the unrelated splits
    (one-word and whole-sentence); 'beats_null' marks the ones above it. Comparisons with fewer than 6 prompts a side
    are marked 'few prompts'. same_sign_in_other_words agrees by chance for about half of all features."""
    spread = F.std(axis=0) + 1e-6
    null = np.max([np.abs(F[a].mean(0) - F[b].mean(0)) for a, b in G["null"].values()], axis=0)
    out = []
    for name, a, b, check in comparisons:
        if len(a) < 2 or len(b) < 2:
            continue
        ma, mb = F[a].mean(0), F[b].mean(0)
        raw = ma - mb
        active = (F[a + b] > 0).mean(axis=0) >= 0.10
        raw_ranked = np.where(active, np.abs(raw), -1)
        idx = np.argsort(-raw_ranked)[:top]
        idx = idx[raw_ranked[idx] > 0]
        t = pd.DataFrame({"comparison": name, "layer": layer, "feature": idx, "mean_a": ma[idx].round(3),
                          "mean_b": mb[idx].round(3), "difference": raw[idx].round(3),
                          "standardized": (raw[idx] / spread[idx]).round(2), "null_max": null[idx].round(3),
                          "beats_null": np.abs(raw[idx]) > null[idx],
                          "active_a": (F[a][:, idx] > 0).mean(0).round(2), "active_b": (F[b][:, idx] > 0).mean(0).round(2),
                          "n_a": len(a), "n_b": len(b), "note": "few prompts" if min(len(a), len(b)) < 6 else ""})
        if check is not None:
            ca, cb = check
            t["same_sign_in_other_words"] = np.sign(F[ca][:, idx].mean(0) - F[cb][:, idx].mean(0)) == np.sign(raw[idx])
        t["sae_file"] = sae_file
        t["neuronpedia"] = [link.format(layer=layer, feature=int(i)) for i in idx] if link else ""
        out.append(t)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def comparisons_for(G):
    """The feature comparisons: (name, rows a, rows b, a check set in other words or None)."""
    return [("08:00 loss vs gain (the briefings)", G["main8_loss"], G["main8_gain"], (G["paraphrase_loss"], G["paraphrase_gain"])),
            ("08:00 loss vs gain in other words", G["paraphrase_loss"], G["paraphrase_gain"], (G["main8_loss"], G["main8_gain"])),
            ("08:00 responsible vs matched control sentence", G["main8_you"], G["control8"],
             (G["you_check_you"], G["you_check_neutral"])),
            ("08:00 responsibility in other words vs neutral sentences", G["you_check_you"], G["you_check_neutral"],
             (G["main8_you"], G["control8"])),
            ("08:00 bad vs good weather (no money)", G["weather_bad"], G["weather_good"], None),
            ("08:00 plain loss vs neutral", G["main8_loss_plain"], G["main8_neutral"], None),
            ("08:00 plain gain vs neutral", G["main8_gain_plain"], G["main8_neutral"], None),
            ("09:30 loss vs gain (with UBS's request)", G["main9_loss"], G["main9_gain"], (G["paraphrase9_loss"], G["paraphrase9_gain"])),
            ("09:30 request vs no request (all briefings)", G["main9_all"], G["main9_no_request_all"], None)]


def aligned_features(W_dec, d, top=15):
    """The features whose decoder vectors point most along direction d (and most against it), by cosine."""
    W = W_dec / (np.linalg.norm(W_dec, axis=1, keepdims=True) + 1e-12)
    c = W @ unit(d)
    up, down = np.argsort(-c)[:top], np.argsort(c)[:top]
    return up, c[up], down, c[down]
