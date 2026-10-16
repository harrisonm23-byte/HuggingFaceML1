"""Step 0 (notebook 15, 2026-10-16): the prompts that test what the desk briefing does inside the model, and the measures.

The prompts are the pilot's own briefings (with amount and period variations) plus the test sentences in
data/silver/briefing_probes.json: loss and gain in other words, word flips, money only, threat only, a matched control
for the responsibility sentence, and bad vs good weather. Every prompt is the agent's conversation on 7 Jan at 08:00 or
at 09:30 (UBS's request, after holding at every step), so only the briefing (and, at 09:30, the request) differs.

The measures take any array of states with one row per prompt, so they can be checked without a model: on a
bag-of-words stand-in, which knows words but no meaning, the word-level checks pass and the meaning-level ones do not
(sim/test_briefing_inside.py).
"""
import hashlib, json, os

import numpy as np
import pandas as pd

from briefing import ROOT, load_briefings, opening_with, turns_at, variants

PROBES = os.path.join(ROOT, "data", "silver", "briefing_probes.json")
DATE, FIRST, REQUEST = "2011-01-07", "08:00", "09:30"
MAIN = ["neutral", "loss", "gain", "loss + you", "gain + you"]     # the pilot's briefings ("no ask" = neutral, no request)
FRAME = {"neutral": None, "loss": "loss", "gain": "gain", "loss + you": "loss", "gain + you": "gain"}


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
        period = "quarter" if "quarter" in label else "month"
        return (int(label[1]) if label.startswith("$") else None), period

    # The pilot's briefings: at 08:00, and at 09:30 with UBS's request and without it
    for when in (FIRST, REQUEST):
        for v in MAIN:
            for label, text in variants(v, b):
                x, p = amount_period(label)
                for asked in ((True,) if when == FIRST else (True, False)):
                    add(set="main", time=when, version=v if asked else v + " (no request)", side=FRAME[v], frame=FRAME[v],
                        you=v.endswith("+ you"), asked=asked, amount=x, period=p, text=text)
    # The responsibility sentence's control: the same structure and length, without the responsibility
    rs = pr["responsibility"]
    for when in (FIRST, REQUEST):
        for v in ("loss", "gain"):
            for label, text in variants(v, b):
                x, p = amount_period(label)
                add(set="you_control", time=when, version=v + " + control sentence", side="control", frame=v, amount=x,
                    period=p, text=text + " " + rs["build_control"])
    # Loss and gain in other words, word flips, money only, threat only (all at 08:00)
    for p in pr["periods"]:
        for f in pr["paraphrases"]["families"]:
            for side in ("loss", "gain"):
                add(set="paraphrase", version=f"{side} in other words", side=side, frame=side, family=f["family"],
                    amount=4, period=p, text=f[side].format(p=p))
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
        # Responsibility in other words vs other neutral sentences, on the plain $4M loss and gain briefings
        for v in ("loss", "gain"):
            base = b["versions"][v].replace("last month", f"last {p}")
            for k, s in enumerate(rs["you_paraphrases"]):
                add(set="you_check", version=v + " + responsibility in other words", side="you", frame=v,
                    family=f"Y{k + 1}", amount=4, period=p, text=base + " " + s)
            for k, s in enumerate(rs["control_sentences"]):
                add(set="you_check", version=v + " + other neutral sentence", side="control", frame=v,
                    family=f"C{k + 1}", amount=4, period=p, text=base + " " + s)
    # Bad vs good news with no money in it
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
    cache = {}
    turns = []
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


def groups(P):
    """The groups of prompts the measures compare, by name."""
    def idx(**kw):
        m = np.ones(len(P), bool)
        for c, v in kw.items():
            m &= (P[c] == v).to_numpy() if v is not None else P[c].isna().to_numpy()
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
    G["main8_plain_framed"] = G["main8_loss_plain"] + G["main8_gain_plain"]
    G["main9_you_asked"] = G["main9_you"]
    for s, sides in (("paraphrase", ("loss", "gain")), ("flip", ("loss", "gain")), ("money_only", ("loss", "gain")),
                     ("threat_only", ("loss", "gain")), ("you_check", ("you", "control")), ("weather", ("bad", "good"))):
        for side in sides:
            G[f"{s}_{side}"] = idx(set=s, side=side)
    framed8 = G["main8_loss"] + G["main8_gain"]
    weather = G["weather_bad"] + G["weather_good"]
    # Null contrasts: splits that should have nothing to do with loss (the same prompts, another difference)
    G["null"] = {"$3M vs $5M": ([i for i in framed8 if P.at[i, "amount"] == 3], [i for i in framed8 if P.at[i, "amount"] == 5]),
                 "month vs quarter": ([i for i in framed8 if P.at[i, "period"] == "month"],
                                      [i for i in framed8 if P.at[i, "period"] == "quarter"]),
                 "week vs weekend": ([i for i in weather if P.at[i, "week"] == "week"],
                                     [i for i in weather if P.at[i, "week"] == "weekend"])}
    return G


def layer_measures(X, P, G):
    """Everything Step 0 asks of one layer. The loss direction is built from the pilot's own briefings at 08:00
    (loss minus gain, with and without the responsibility sentence); the responsibility direction from the
    responsibility sentence minus its matched control sentence."""
    d = mean_diff(X, G["main8_loss"], G["main8_gain"])
    u = unit(d)
    main_gap = gap(X, u, G["main8_loss"], G["main8_gain"])
    dy = mean_diff(X, G["main8_you"], G["control8"])
    uy = unit(dy)
    out = {
        # Passes for anything that registers words: the left-out variation differs in the same words
        "wording_check": leave_one_out(X, P.assign(variant=P.amount.astype(str) + P.period.astype(str) + P.you.astype(str)),
                                       G["main8_loss"], G["main8_gain"], "variant", ["variant"]),
        "paraphrase_acc": order(X, u, pairs(P, G["paraphrase_loss"], G["paraphrase_gain"], ["family", "period"])),
        "paraphrase_gap": gap(X, u, G["paraphrase_loss"], G["paraphrase_gain"]) / (main_gap + 1e-12),
        "flip_acc": order(X, u, pairs(P, G["flip_loss"], G["flip_gain"], ["family", "period"])),
        "money_only_acc": order(X, u, pairs(P, G["money_only_loss"], G["money_only_gain"], ["amount", "period"])),
        "threat_only_acc": order(X, u, pairs(P, G["threat_only_loss"], G["threat_only_gain"], ["family", "period"])),
        "weather_acc": order(X, u, pairs(P, G["weather_bad"], G["weather_good"], ["family", "week"])),
        "weather_cos": cos(mean_diff(X, G["weather_bad"], G["weather_good"]), d),
        "null_cos_max": max(abs(cos(mean_diff(X, a, b), d)) for a, b in G["null"].values()),
        "left_at_0930": gap(X, u, G["main9_loss"], G["main9_gain"]) / (main_gap + 1e-12),
        "acc_0930": order(X, u, pairs(P, G["main9_loss"], G["main9_gain"], ["amount", "period", "you"])),
        "left_at_0930_no_request": gap(X, u, G["main9_no_request_loss"], G["main9_no_request_gain"]) / (main_gap + 1e-12),
        "request_along_loss": gap(X, u, G["main9_all"], G["main9_no_request_all"]) / (main_gap + 1e-12),
        "you_wording_check": leave_one_out(X, P.assign(variant=P.frame.astype(str) + P.amount.astype(str) + P.period.astype(str)),
                                           G["main8_you"], G["control8"], "variant", ["variant"]),
        "you_check_acc": order(X, uy, pairs(P, G["you_check_you"], G["you_check_control"], ["frame", "period"])),
        "you_left_at_0930": gap(X, uy, G["main9_you"], G["control9"]) / (gap(X, uy, G["main8_you"], G["control8"]) + 1e-12),
        "one_more_sentence_cos": cos(mean_diff(X, G["main8_you"], G["main8_plain_framed"]),
                                     mean_diff(X, G["control8"], G["main8_plain_framed"])),
    }
    return out


COLUMNS = {
    "wording_check": "Left-out amount/period ordered right (passes even for a word counter; 0.5 = chance)",
    "paraphrase_acc": "Loss and gain in other words ordered right along the loss direction (0.5 = chance)",
    "paraphrase_gap": "Their loss-gain gap as a share of the briefings' own gap",
    "flip_acc": "Word flips ordered by meaning (1 = follows meaning, 0 = follows words)",
    "money_only_acc": "Money only (no threat to the desk) ordered right",
    "threat_only_acc": "Threat to the desk only (no money) ordered right",
    "weather_acc": "Bad above good weather along the loss direction (0.5 = unrelated)",
    "weather_cos": "Cosine of the weather difference with the loss difference",
    "null_cos_max": "Largest cosine of an unrelated split ($3M vs $5M, month vs quarter, week vs weekend) with it",
    "left_at_0930": "The loss-gain gap at UBS's request (09:30) as a share of 08:00",
    "acc_0930": "09:30 loss/gain pairs ordered right along the 08:00 direction",
    "left_at_0930_no_request": "The same share at 09:30 with no request",
    "request_along_loss": "How far UBS's request moves the state along the loss direction (share of the loss gap)",
    "you_wording_check": "Responsibility vs matched control sentence, left-out variation (passes for a word counter)",
    "you_check_acc": "Responsibility in other words above other neutral sentences (0.5 = chance)",
    "you_left_at_0930": "The responsibility gap at 09:30 as a share of 08:00",
    "one_more_sentence_cos": "Cosine of (+ responsibility) and (+ control sentence), each minus plain: how much is just 'one more sentence'",
}


def choose_layer(LT):
    """The layer for the dial: among the middle layers, the best at loss and gain in other words, then word flips."""
    n = int(LT.layer.max()) + 1
    middle = LT[(LT.layer >= n // 4) & (LT.layer <= 3 * n // 4)]
    return int(middle.sort_values(["paraphrase_acc", "flip_acc", "paraphrase_gap"], ascending=False).iloc[0]["layer"]), middle


def reading(LT, best, floor=None):
    """Plain-English lines for the printout and summary.md, each against its baseline."""
    r = LT.set_index("layer").loc[best]
    _, middle = choose_layer(LT)
    med = middle.median(numeric_only=True)
    f = (lambda c: f"; words-only floor {floor[c]:.2f}") if floor is not None else (lambda c: "")   # floor: no context
    lines = [
        f"Layer for the dial: {best} (chosen among layers {int(middle.layer.min())}-{int(middle.layer.max())} for loss and gain "
        f"in other words, so its number there is the best of those layers; their median is given too).",
        f"Wording check: {r.wording_check:.2f}. Expected near 1.0 even for a word counter, so it shows only that the "
        "signal is not tied to one amount or period.",
        f"Loss and gain in other words: ordered {r.paraphrase_acc:.2f} at layer {best} (median {med.paraphrase_acc:.2f}"
        f"{f('paraphrase_acc')}; 0.5 = chance), and {r.paraphrase_gap:.2f} of the briefings' loss gap carries over to them "
        f"(median {med.paraphrase_gap:.2f}{f('paraphrase_gap')}). Above chance means the loss direction is not just the words "
        "loss/profit and closure/expansion; above the floor means more than the meanings of single words.",
        f"Word flips: {r.flip_acc:.2f} (median {med.flip_acc:.2f}{f('flip_acc')}). 1 = follows the meaning, 0 = follows the "
        "words. This is the hardest test; below 0.5 means the words win.",
        f"Money only: {r.money_only_acc:.2f}; threat to the desk only: {r.threat_only_acc:.2f}. Which part of the briefing the "
        "loss direction picks up.",
        f"Weather (no money): ordered {r.weather_acc:.2f} (0.5 = unrelated); cosine with the loss difference "
        f"{r.weather_cos:+.2f}, against {r.null_cos_max:.2f} for the largest unrelated split. A weather cosine well above that "
        "means the loss direction is partly 'bad news in general'. Near the null only rules out a general good-or-bad-news "
        "direction; it does not show the signal is about money.",
        f"At UBS's request (09:30): {r.left_at_0930:.2f} of the 08:00 gap is left (median {med.left_at_0930:.2f}, range "
        f"{middle.left_at_0930.min():.2f} to {middle.left_at_0930.max():.2f}); pairs ordered {r.acc_0930:.2f}. With no request: "
        f"{r.left_at_0930_no_request:.2f}. The request itself moves the state {r.request_along_loss:+.2f} of the loss gap "
        "along the loss direction.",
        f"Responsibility: in other words, ordered {r.you_check_acc:.2f} (median {med.you_check_acc:.2f}{f('you_check_acc')}; "
        f"0.5 = chance); {r.you_left_at_0930:.2f} of it is left at 09:30. 'Just one more sentence' cosine "
        f"{r.one_more_sentence_cos:+.2f} (near 1 = the responsibility sentence acts mostly like any added sentence; the "
        "responsibility direction itself is built against the matched control sentence).",
    ]
    return lines


# ---- features (Gemma Scope 2) ----------------------------------------------------------------------------------------
def feature_table(F, P, G, comparisons, top=15, layer=None, sae_file=None, link=None):
    """For each comparison, the features whose average activation differs most, in activation units (not capped by a
    spread taken over the two groups). Each feature's own null is its largest difference across the unrelated splits;
    'beats_null' marks the ones above it. Comparisons with fewer than 6 prompts a side are marked 'few prompts'."""
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
            ("08:00 responsible vs matched control sentence", G["main8_you"], G["control8"], (G["you_check_you"], G["you_check_control"])),
            ("08:00 bad vs good weather (no money)", G["weather_bad"], G["weather_good"], None),
            ("08:00 plain loss vs neutral", G["main8_loss_plain"], G["main8_neutral"], None),
            ("08:00 plain gain vs neutral", G["main8_gain_plain"], G["main8_neutral"], None),
            ("09:30 loss vs gain (with UBS's request)", G["main9_loss"], G["main9_gain"], None),
            ("09:30 request vs no request (all briefings)", G["main9_all"], G["main9_no_request_all"], None)]


def aligned_features(W_dec, d, top=15):
    """The features whose decoder vectors point most along direction d (and most against it), by cosine."""
    W = W_dec / (np.linalg.norm(W_dec, axis=1, keepdims=True) + 1e-12)
    c = W @ unit(d)
    up, down = np.argsort(-c)[:top], np.argsort(c)[:top]
    return up, c[up], down, c[down]
