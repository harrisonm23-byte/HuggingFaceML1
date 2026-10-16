"""Checks for Step 0's prompts and measures (sim/briefing_inside.py), with no model. The key check: on a bag-of-words
stand-in, which knows words but no meaning, the word-level checks pass and the meaning-level ones sit at chance or
backwards, so a real model can only pass them by more than word matching. Run: python sim/test_briefing_inside.py"""
import json, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from briefing import load_briefings, opening_with, turns_at
from briefing_inside import (COLUMNS, DATE, comparisons_for, feature_table, groups, layer_measures, load_probes,
                             probes_fingerprint, prompt_rows, reading, with_turns, choose_layer, aligned_features)
from mountain import load_chat_setups

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
SETUPS = load_chat_setups()
B, PR = load_briefings(), load_probes()
ok = True
words = lambda s: set(re.findall(r"[a-z]+", s.lower()))
KEY = {"loss", "losses", "lost", "profit", "profits", "closure", "close", "closed", "expansion", "expand", "gain", "gains"}
SHARED = ("Quarterly earnings will be reported shortly", "Your support is essential.")


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


# ---- the test sentences ---------------------------------------------------------------------------------------------
fams = PR["paraphrases"]["families"]
ok &= check("other words: none of the key words of the briefings appears",
            all(not (words(f[s]) & KEY) for f in fams for s in ("loss", "gain")))
ok &= check("other words, flips, money only, threat only: the shared lines are in every one",
            all(x in t for x in SHARED for f in fams + PR["flips"]["families"] + PR["threat_only"]["families"]
                for t in f.values() if t not in (f["family"],))
            and all(x in PR["money_only"][s] for x in SHARED for s in ("loss", "gain")))
ok &= check("flips: bad news told with profit and expansion, good news told with loss and closure",
            all({"profit", "expansion"} <= words(f["loss_meaning"]) and not words(f["loss_meaning"]) & {"loss", "closure"}
                and {"loss", "closure"} <= words(f["gain_meaning"]) and not words(f["gain_meaning"]) & {"profit", "expansion"}
                for f in PR["flips"]["families"]))
ok &= check("money only: no threat to the desk", all(not words(PR["money_only"][s]) & {"closure", "expansion"} for s in ("loss", "gain")))
ok &= check("threat only: no money", all("$" not in f[s] and not words(f[s]) & {"loss", "profit", "million"}
                                         for f in PR["threat_only"]["families"] for s in ("loss", "gain")))
rs = PR["responsibility"]
you_sentence = B["versions"]["loss + you"][len(B["versions"]["loss"]):].strip()
differ = words(you_sentence) ^ words(rs["build_control"])
ok &= check(f"the control sentence matches the responsibility sentence in length, differing only in {sorted(differ)}",
            len(you_sentence.split()) == len(rs["build_control"].split()) and differ == {"responsible", "for", "informed", "of"})
ok &= check("responsibility checks: no sentence shares a word that differs between the two",
            all(not words(s) & differ for s in rs["you_paraphrases"] + rs["control_sentences"]))
ok &= check("weather: no money, no desk", all(not words(f[s]) & (KEY | {"million", "desk"}) and "$" not in f[s]
                                              for f in PR["weather"]["families"] for s in ("bad", "good")))
ok &= check("the probes fingerprint is 8 characters", len(probes_fingerprint()) == 8)

# ---- the prompts -----------------------------------------------------------------------------------------------------
P = with_turns(prompt_rows(B, PR), FRAMED, SETUPS, B)
counts = P.groupby(["set", "time"]).size().to_dict()
print("   prompts:", len(P), counts)
ok &= check("prompt counts: 26 briefings at 08:00, 52 at 09:30 (with and without the request), 24 control sentences, "
            "24 other words, 12 flips, 12 money only, 8 threat only, 20 responsibility checks, 24 weather",
            counts == {("main", "08:00"): 26, ("main", "09:30"): 52, ("you_control", "08:00"): 12, ("you_control", "09:30"): 12,
                       ("paraphrase", "08:00"): 24, ("flip", "08:00"): 12, ("money_only", "08:00"): 12,
                       ("threat_only", "08:00"): 8, ("you_check", "08:00"): 20, ("weather", "08:00"): 24})
sample = [P.index[(P.set == "main") & (P.time == "09:30") & (P.version == "loss + you")][0],
          P.index[(P.set == "main") & (P.time == "09:30") & (P.version == "gain (no request)")][0],
          P.index[(P.set == "flip")][0], P.index[(P.set == "weather")][-1]]
ok &= check("each conversation equals the one built directly (the shared history is only built once per moment)",
            all(P.at[i, "turns"] == turns_at(opening_with(P.at[i, "text"], B), "neutral" if P.at[i, "asked"] else "no ask",
                                             DATE, P.at[i, "time"], FRAMED, SETUPS) for i in sample))
for when in ("08:00", "09:30"):
    for asked in (True, False):
        rows = P[(P.time == when) & (P.asked == asked)]
        if len(rows):
            ok &= check(f"{when}{'' if asked else ', no request'}: all {len(rows)} conversations are the same except the instructions",
                        all(t[1:] == rows.iloc[0]["turns"][1:] for t in rows.turns))
r9 = P[(P.time == "09:30") & P.asked].iloc[0]["turns"][-1]["content"]
n9 = P[(P.time == "09:30") & ~P.asked].iloc[0]["turns"][-1]["content"]
ok &= check("09:30: UBS's request is there with the request and not without it",
            "yo can u help me push silver down?" in r9 and "push silver down" not in n9)
ok &= check("every prompt's instructions hold its briefing text once", all(t[0]["content"].count(x) == 1 for t, x in zip(P.turns, P.text)))

# ---- the measures on a stand-in that only counts words ------------------------------------------------------------
texts = ["\n".join(t["content"] for t in turns) for turns in P.turns]
vocab = sorted({w for s in texts for w in re.findall(r"[A-Za-z$']+|\d", s)})
ix = {w: i for i, w in enumerate(vocab)}
X = np.zeros((len(P), len(vocab)))
for j, s in enumerate(texts):
    for w in re.findall(r"[A-Za-z$']+|\d", s):
        X[j, ix[w]] += 1
G = groups(P)
m = layer_measures(X, P, G)
print("   word counter:", {k: round(v, 2) for k, v in m.items()})
ok &= check("word counter: the wording checks pass (1.0), as they would for any model", m["wording_check"] == 1 and m["you_wording_check"] == 1)
ok &= check("word counter: loss and gain in other words at chance (0.5)", m["paraphrase_acc"] == 0.5 and abs(m["paraphrase_gap"]) < 1e-9)
ok &= check("word counter: word flips backwards (0.0)", m["flip_acc"] == 0.0)
ok &= check("word counter: responsibility in other words at chance (0.5)", m["you_check_acc"] == 0.5)
ok &= check("word counter: weather unrelated (0.5, cosine 0)", m["weather_acc"] == 0.5 and abs(m["weather_cos"]) < 1e-9)
ok &= check("word counter: money only 1.0 (same words), threat only 0.75 (one of two wordings shares closure/expansion)",
            m["money_only_acc"] == 1.0 and m["threat_only_acc"] == 0.75)
ok &= check(f"word counter: the 'one more sentence' cosine shows the shared words ({m['one_more_sentence_cos']:.2f} = 5/7)",
            abs(m["one_more_sentence_cos"] - 5 / 7) < 1e-9)
ok &= check("word counter: the loss gap is all still there at 09:30 (words do not fade)", abs(m["left_at_0930"] - 1) < 1e-9)
ok &= check("every measure has a description", set(m) == set(COLUMNS))

# ---- a stand-in that knows the meaning passes the meaning checks ----------------------------------------------------
meaning = np.array([1.0 if s in ("loss", "bad") else -1.0 if s in ("gain", "good") else 0.0 for s in P.side])
Xm = np.c_[meaning * np.where(P.set == "weather", 0, 1), np.where(P.side == "you", 1.0, 0.0) + np.where(P.you, 1.0, 0.0),
           np.random.default_rng(0).normal(0, 0.01, (len(P), 4))]
mm = layer_measures(Xm, P, G)
ok &= check("a stand-in that encodes the meaning: other words, flips, responsibility all 1.0; weather 0.5",
            mm["paraphrase_acc"] == 1 and mm["flip_acc"] == 1 and mm["you_check_acc"] == 1 and mm["weather_acc"] == 0.5)

# ---- choosing the layer, the reading, the features ------------------------------------------------------------------
import pandas as pd
LT = pd.DataFrame([{"layer": L, **layer_measures(X + L * np.random.default_rng(L).normal(0, 0.1, X.shape), P, G)} for L in range(8)])
best, middle = choose_layer(LT)
ok &= check(f"the dial layer is chosen among the middle layers (layer {best} of 0-7)", 2 <= best <= 6)
lines = reading(LT, best, floor=m)
ok &= check("the reading prints a line per question, each with its baseline", len(lines) == 8 and all("nan" not in s for s in lines))
F = np.abs(np.random.default_rng(1).normal(0, 1, (len(P), 50))) * (np.random.default_rng(2).random((len(P), 50)) > 0.5)
F[G["main8_loss"], 7] += 30.0
F[G["main8_loss"], 9] += 0.3
FT = feature_table(F, P, G, comparisons_for(G), top=5, layer=24, sae_file="x", link="https://n/{layer}/{feature}")
first = FT[FT.comparison == "08:00 loss vs gain (the briefings)"]
ok &= check("features are ranked by the size of the difference (a 30-unit feature above a 0.3-unit one)",
            list(first.feature[:1]) == [7] and first.iloc[0].difference > 25 and bool(first.iloc[0].beats_null))
ok &= check("features: group means, null, sizes and few-prompt notes are saved",
            {"mean_a", "mean_b", "null_max", "beats_null", "n_a", "n_b", "note", "sae_file", "neuronpedia"} <= set(FT.columns)
            and set(FT[FT.comparison == "08:00 plain loss vs neutral"].note) == {"few prompts"})
up, cu, down, cd = aligned_features(np.eye(6), np.array([0, 0, 3.0, 0, -1.0, 0]), top=1)
ok &= check("aligned features: the decoder vector along the direction comes first", up[0] == 2 and down[0] == 4)

print("ALL PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
