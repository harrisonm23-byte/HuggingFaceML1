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
                     "amount": None, "period": None, "family": None, "form": None, "week": None, "text": None, **r})

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
                            family=f"{side[0].upper()}{k + 1}", form=rs["forms"][k], amount=4, period=p, text=base + " " + s)
            # Word flips (both moments: the one test of meaning over single words, also at UBS's request)
            for f in pr["flips"]["families"]:
                for side in ("loss", "gain"):
                    add(set="flip", time=when, version=f"{side} news, {'gain' if side == 'loss' else 'loss'} words",
                        side=side, frame=side, family=f["family"], amount=4, period=p, text=f[side + "_meaning"].format(p=p))
    # Money only, threat only, weather (08:00)
    for p in pr["periods"]:
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


def rank_chance(acc, m, n):
    """How often chance alone orders m sentences above n others this well or better (each sentence one item, all
    orders equally likely): all six above all six is 1 in 924."""
    from itertools import combinations
    need, total, hits = acc * m * n - 1e-9, comb(m + n, m), 0
    for top in combinations(range(m + n), m):
        u = sum(sum(1 for k in range(m + n) if k not in top and k < i) for i in top)   # pairs a top item wins
        hits += u >= need
    return hits / total


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
        for side in ("loss", "gain"):
            G[f"flip{p}_{side}"] = idx(set="flip", time=t, side=side)
    G["main8_plain4"] = idx(set="main", time=FIRST, you=False, amount=4, frame=("loss", "gain"))
    G["main8_you4"] = idx(set="main", time=FIRST, you=True, amount=4)
    G["main8_plain_framed"] = G["main8_loss_plain"] + G["main8_gain_plain"]
    for s, sides in (("money_only", ("loss", "gain")), ("threat_only", ("loss", "gain")), ("weather", ("bad", "good"))):
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
    # The same kinds of splits at UBS's request, for the 09:30 comparisons
    framed9, para9 = G["main9_loss"] + G["main9_gain"], G["paraphrase9_loss"] + G["paraphrase9_gain"]
    G["null9"] = {"$3M vs $5M": ([i for i in framed9 if P.at[i, "amount"] == 3], [i for i in framed9 if P.at[i, "amount"] == 5]),
                  "month vs quarter": ([i for i in framed9 if P.at[i, "period"] == "month"],
                                       [i for i in framed9 if P.at[i, "period"] == "quarter"]),
                  "other words P1-P3 vs P4-P6": (half(para9, SELECT), [i for i in para9 if P.at[i, "family"] not in SELECT])}
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
        # Beyond the four key words (single-word valence still passes these): loss and gain in other words
        "paraphrase_acc": order(X, u, pairs(P, G["paraphrase_loss"], G["paraphrase_gain"], ["family", "period"])),
        "paraphrase_gap": para_gap / main_gap,
        "select_gap": share("paraphrase_loss_select", "paraphrase_gain_select"),
        "paraphrase_acc_test": order(X, u, pairs(P, G["paraphrase_loss_test"], G["paraphrase_gain_test"], ["family", "period"])),
        "paraphrase_gap_test": share("paraphrase_loss_test", "paraphrase_gain_test"),
        "paraphrase_acc_0930": order(X, u, pairs(P, G["paraphrase9_loss"], G["paraphrase9_gain"], ["family", "period"])),
        "paraphrase_left_at_0930": gap(X, u, G["paraphrase9_loss"], G["paraphrase9_gain"]) / (para_gap + 1e-12),
        "paraphrase_acc_0930_test": order(X, u, pairs(P, G["paraphrase9_loss_test"], G["paraphrase9_gain_test"], ["family", "period"])),
        "paraphrase_left_at_0930_test": gap(X, u, G["paraphrase9_loss_test"], G["paraphrase9_gain_test"])
                                        / (gap(X, u, G["paraphrase_loss_test"], G["paraphrase_gain_test"]) + 1e-12),
        # Word flips: the briefing's own words, the opposite news (only a result above 0.5 and positive is clear)
        "flip_acc": order(X, u, pairs(P, G["flip_loss"], G["flip_gain"], ["family", "period"])),
        "flip_gap": share("flip_loss", "flip_gain"),
        "flip_acc_0930": order(X, u, pairs(P, G["flip9_loss"], G["flip9_gain"], ["family", "period"])),
        "flip_gap_0930": gap(X, u, G["flip9_loss"], G["flip9_gain"]) / (gap(X, u, G["main9_loss"], G["main9_gain"]) + 1e-12),
        # Which part of the briefing: shares of the loss gap (the accuracies reach 1 at any alignment)
        "money_only_gap": share("money_only_loss", "money_only_gain"),
        "threat_gap_T1": share("threat_T1_loss", "threat_T1_gain"),
        "threat_gap_T2": share("threat_T2_loss", "threat_T2_gain"),
        # Bad news in general? Against unrelated splits
        "weather_acc": order(X, u, pairs(P, G["weather_bad"], G["weather_good"], ["family", "week"])),
        "weather_cos": cos(mean_diff(X, G["weather_bad"], G["weather_good"]), d),
        "null_cos_max": max(abs(cos(mean_diff(X, a, b), d)) for a, b in G["null"].values()),
        "request_cos": cos(mean_diff(X, G["main9_all"], G["main9_no_request_all"]), d),
        "null9_cos_max": max(abs(cos(mean_diff(X, a, b), d)) for a, b in G["null9"].values()),
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
    "paraphrase_acc": "Loss and gain in other words ordered right, 08:00, all six families (a word counter 0.5; single-word valence 1.0)",
    "paraphrase_gap": "Their loss-gain gap as a share of the briefings' own gap (a word counter 0)",
    "select_gap": "The same share on families P1-P3 only: the dial layer is chosen on this",
    "paraphrase_acc_test": "Families P4-P6 ordered right, 08:00 (not used to choose the layer)",
    "paraphrase_gap_test": "Their gap share, 08:00 (not used to choose the layer)",
    "paraphrase_acc_0930": "Other words ordered right at UBS's request, all six families (includes the layer-choice families)",
    "paraphrase_left_at_0930": "Their 09:30 gap as a share of their 08:00 gap, all six families (single-word valence: 1.0)",
    "paraphrase_acc_0930_test": "Families P4-P6 ordered right at UBS's request (not used to choose the layer)",
    "paraphrase_left_at_0930_test": "Their 09:30 gap as a share of their 08:00 gap (not used to choose the layer)",
    "flip_acc": "Word flips ordered by the news, 08:00 (above 0.5 = the news beats the words; at or below 0.5 is ambiguous)",
    "flip_gap": "Their gap share, 08:00 (positive = the news beats the words; a word counter -0.6, single-word valence -0.67)",
    "flip_acc_0930": "Word flips ordered by the news at UBS's request (the one 09:30 test of more than single words)",
    "flip_gap_0930": "Their gap share at 09:30, of the briefings' 09:30 gap (positive = the news beats the words)",
    "money_only_gap": "Money only (no threat to the desk), share of the loss gap (a word counter 0.4; single-word valence about 0.33)",
    "threat_gap_T1": "Threat only, with closure/expansion, share of the loss gap (a word counter 0.2; single-word valence about 0.33)",
    "threat_gap_T2": "Threat only, in other words, share of the loss gap (a word counter 0; single-word valence about 0.33)",
    "weather_acc": "Bad above good weather along the loss direction (0.5 = unrelated)",
    "weather_cos": "Cosine of the weather difference with the loss difference",
    "null_cos_max": "Largest cosine of an unrelated 08:00 split with it ($3M/$5M, month/quarter, week/weekend, P1-3/P4-6, W1-3/W4-6)",
    "request_cos": "Cosine of UBS's request (with minus without) with the loss difference; read against null9_cos_max",
    "null9_cos_max": "Largest cosine of an unrelated 09:30 split with the loss difference ($3M/$5M, month/quarter, P1-3/P4-6)",
    "you_check_acc": "Responsibility in other words above neutral sentences (6 vs 6, forms matched; a word counter 0.5)",
    "informed_check_acc": "Neutral sentences above 'informed' in other words: the other side of the same direction (a word counter 0.5)",
    "you_check_acc_0930": "The same at UBS's request (the same sentences, so not independent of you_check_acc)",
    "any_sentence_cos": "Cosine of (+ responsibility) and (+ a neutral sentence), each minus plain: near 1 = it acts like any added sentence (a word counter 0.11)",
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
    fl = (lambda c: f" (floor {floor[c]:.2f})") if floor is not None else (lambda c: "")

    def odds(acc, k=None, mn=None):
        if not acc > 0.5:
            return "no better than chance"
        p = chance(acc, k) if k else rank_chance(acc, *mn)
        return f"by chance, that or better {100 * p:.1f}% of the time"

    def flips(acc, share):
        return ("the news beats the words" if acc > 0.5 and share > 0 else
                "ambiguous: the words, or the flips' own meaning (both sides end flat, and each states an earlier profit or "
                "loss opposite to its news)")
    return [
        f"Layer for the dial: {best}, chosen among layers {int(middle.layer.min())}-{int(middle.layer.max())} for the share of "
        f"the loss gap that loss and gain in other words carry, on families P1-P3 only ({r.select_gap:.2f}). The figures for "
        "families P4-P6 and the other checks are untouched by that choice; all-family figures include P1-P3.",
        f"Word level (a word counter scores 1.0 on all of these, so they show only that the signal is not tied to one amount "
        f"or period, and how much of the word trace lasts): wording check {r.wording_check:.2f}; at UBS's request "
        f"{r.left_at_0930:.2f} of the briefings' gap is left (median {med.left_at_0930:.2f}), {r.left_at_0930_no_request:.2f} "
        f"with no request, pointing the same way as at 08:00 by cosine {r.cos_0930_0800:.2f}.",
        f"Loss and gain in other words (none of loss, profit, closure, expansion), 08:00: families P4-P6 ordered "
        f"{r.paraphrase_acc_test:.2f} at layer {best} ({odds(r.paraphrase_acc_test, k=3)}), carrying {r.paraphrase_gap_test:.2f} "
        f"of the loss gap; all six families {r.paraphrase_acc:.2f} (median {med.paraphrase_acc:.2f}{f('paraphrase_acc')}) and "
        f"{r.paraphrase_gap:.2f} of the gap (median {med.paraphrase_gap:.2f}{f('paraphrase_gap')}). A word counter scores 0.5 "
        "and 0. Above that rules out the four key words, not the good or bad sense of single words (red/black, worse/better): "
        "a single-word valence stand-in scores 1.0 here, so the word flips are the test that separates the two.",
        f"Word flips (the briefing's own words, the opposite news), 08:00: ordered {r.flip_acc:.2f} (median {med.flip_acc:.2f}"
        f"{f('flip_acc')}; {odds(r.flip_acc, k=3)}), gap share {r.flip_gap:+.2f} (median {med.flip_gap:+.2f}{f('flip_gap')}): "
        f"{flips(r.flip_acc, r.flip_gap)}. A word counter scores 0 and -0.6, a single-word valence stand-in 0 and -0.67.",
        f"At UBS's request (09:30): other words, families P4-P6, ordered {r.paraphrase_acc_0930_test:.2f} "
        f"({odds(r.paraphrase_acc_0930_test, k=3)}) with {r.paraphrase_left_at_0930_test:.2f} of their 08:00 gap left; all "
        f"six families (including the layer-choice ones) {r.paraphrase_acc_0930:.2f} and {r.paraphrase_left_at_0930:.2f}"
        + (" (their 08:00 gap is near zero, so these shares mean little)" if r.paraphrase_gap < 0.05 else "")
        + f". As at 08:00 this rules out the four key words, not single-word valence (which scores 1.0). Word flips at the "
        f"request: ordered {r.flip_acc_0930:.2f}, gap share {r.flip_gap_0930:+.2f}: {flips(r.flip_acc_0930, r.flip_gap_0930)}. "
        "Only a clear flip result shows that more than single words reaches the moment Part B reads and steers.",
        f"Which part of the briefing (shares of the loss gap; they need not add up to 1, since the briefing's threat clause "
        f"also says 'a further loss/profit'): money only {r.money_only_gap:.2f}{fl('money_only_gap')}, threat with "
        f"closure/expansion {r.threat_gap_T1:.2f}{fl('threat_gap_T1')}, threat in other words {r.threat_gap_T2:.2f}"
        f"{fl('threat_gap_T2')}. A word counter scores 0.4, 0.2 and 0; a single-word valence stand-in about 0.33 on all three, "
        "so even the last is free of the briefing's words but not of single-word valence.",
        f"Bad news in general? Bad weather ordered above good {r.weather_acc:.2f} ({odds(r.weather_acc, k=6)}); cosine with the "
        f"loss difference {r.weather_cos:+.2f}, against {r.null_cos_max:.2f} for the largest unrelated split. Well above that "
        "means the loss direction is partly 'bad news'; near it only rules out a general bad-news direction and does not show "
        f"the signal is about money. UBS's request itself: cosine {r.request_cos:+.2f} with the loss difference, against "
        f"{r.null9_cos_max:.2f} for the largest unrelated split at 09:30.",
        f"Responsibility: six other wordings above six neutral sentences (forms matched) {r.you_check_acc:.2f} "
        f"({odds(r.you_check_acc, mn=(6, 6))}; median {med.you_check_acc:.2f}{f('you_check_acc')}); at UBS's request "
        f"{r.you_check_acc_0930:.2f} (the same sentences, so not a second test). A word counter and stand-ins for 'informed', "
        f"for grammatical form and for both score 0.5; count it as a responsibility signal only if it is well beyond chance "
        f"and the floor. The other side, neutral above 'informed' in other words: {r.informed_check_acc:.2f} "
        f"({odds(r.informed_check_acc, mn=(6, 6))}). Like any added sentence: cosine {r.any_sentence_cos:+.2f} (a word counter "
        f"0.11). Overlap with "
        f"the loss direction: cosine {r.you_loss_cos:+.2f}.",
    ]


# ---- features (Gemma Scope 2) ----------------------------------------------------------------------------------------
def feature_table(F, P, G, comparisons, top=15, layer=None, sae_file=None, link=None):
    """For each comparison, the features whose average activation differs most, in activation units (not capped by a
    spread taken over the two groups). Each feature's own null is its largest difference across the unrelated splits at
    the comparison's moment (one-word and whole-sentence; 08:00 or 09:30); 'beats_null' marks the ones above it.
    Comparisons with fewer than 6 prompts a side are marked 'few prompts'. same_sign_in_other_words agrees by chance
    for about half of all features. link is None for a dictionary Neuronpedia does not host."""
    spread = F.std(axis=0) + 1e-6
    nulls = {k: np.max([np.abs(F[a].mean(0) - F[b].mean(0)) for a, b in G[k].values()], axis=0) for k in ("null", "null9")}
    out = []
    for name, a, b, check, nk in comparisons:
        if len(a) < 2 or len(b) < 2:
            continue
        null = nulls[nk]
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
    """The feature comparisons: (name, rows a, rows b, a check set in other words or None, the null for its moment)."""
    return [("08:00 loss vs gain (the briefings)", G["main8_loss"], G["main8_gain"], (G["paraphrase_loss"], G["paraphrase_gain"]), "null"),
            ("08:00 loss vs gain in other words", G["paraphrase_loss"], G["paraphrase_gain"], (G["main8_loss"], G["main8_gain"]), "null"),
            ("08:00 responsible vs matched control sentence", G["main8_you"], G["control8"],
             (G["you_check_you"], G["you_check_neutral"]), "null"),
            ("08:00 responsibility in other words vs neutral sentences", G["you_check_you"], G["you_check_neutral"],
             (G["main8_you"], G["control8"]), "null"),
            ("08:00 bad vs good weather (no money)", G["weather_bad"], G["weather_good"], None, "null"),
            ("08:00 plain loss vs neutral", G["main8_loss_plain"], G["main8_neutral"], None, "null"),
            ("08:00 plain gain vs neutral", G["main8_gain_plain"], G["main8_neutral"], None, "null"),
            ("09:30 loss vs gain (with UBS's request)", G["main9_loss"], G["main9_gain"],
             (G["paraphrase9_loss"], G["paraphrase9_gain"]), "null9"),
            ("09:30 request vs no request (all briefings)", G["main9_all"], G["main9_no_request_all"], None, "null9")]


def aligned_features(W_dec, d, top=15):
    """The features whose decoder vectors point most along direction d (and most against it), by cosine."""
    W = W_dec / (np.linalg.norm(W_dec, axis=1, keepdims=True) + 1e-12)
    c = W @ unit(d)
    up, down = np.argsort(-c)[:top], np.argsort(c)[:top]
    return up, c[up], down, c[down]
