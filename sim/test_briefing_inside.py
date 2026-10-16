"""Checks for Step 0's prompts and measures (sim/briefing_inside.py), with no model. The key checks are stand-ins that
know less than meaning: a bag-of-words stand-in passes only the word-level checks; one that knows how good or bad
single words sound also passes "other words" but not the word flips; one that knows only "being informed" does not pass
the responsibility check. A stand-in that knows the meaning passes them all. Run: python sim/test_briefing_inside.py"""
import json, os, re, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from briefing import load_briefings, opening_with, turns_at
from briefing_inside import (COLUMNS, DATE, WORD_LEVEL, aligned_features, chance, choose_layer, comparisons_for,
                             feature_table, groups, layer_measures, load_probes, probes_fingerprint, prompt_rows, reading,
                             with_turns)
from mountain import load_chat_setups

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
SETUPS = load_chat_setups()
B, PR = load_briefings(), load_probes()
ok = True
words = lambda s: set(re.findall(r"[a-z]+", s.lower()))
toks = lambda s: re.findall(r"[A-Za-z$']+|\d", s)
KEY = {"loss", "losses", "lost", "profit", "profits", "closure", "close", "closed", "expansion", "expand", "gain", "gains"}
SHARED = ("Quarterly earnings will be reported shortly", "Your support is essential.")


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


# ---- the test sentences ---------------------------------------------------------------------------------------------
fams, flips = PR["paraphrases"]["families"], PR["flips"]["families"]
ok &= check("other words: none of the key words of the briefings appears",
            all(not (words(f[s]) & KEY) for f in fams for s in ("loss", "gain")))
ok &= check("other words: each pair has the same number of words",
            all(len(f["loss"].split()) == len(f["gain"].split()) for f in fams))
ok &= check("other words, flips, money only, threat only: the shared lines are in every one",
            all(x in f[k] for x in SHARED for f in fams for k in ("loss", "gain"))
            and all(x in f[k] for x in SHARED for f in flips for k in ("loss_meaning", "gain_meaning"))
            and all(x in f[k] for x in SHARED for f in PR["threat_only"]["families"] for k in ("loss", "gain"))
            and all(x in PR["money_only"][s] for x in SHARED for s in ("loss", "gain")))
flip_diffs = [{(a, c) for a, c in zip(f["loss_meaning"].split(), f["gain_meaning"].split()) if a != c} for f in flips]
ok &= check("flips: within a pair only profit/loss and expansion/closure differ, exactly as in the briefings",
            all(len(f["loss_meaning"].split()) == len(f["gain_meaning"].split()) for f in flips)
            and all(d == {("profit", "loss"), ("expansion", "closure")} for d in flip_diffs))
ok &= check("money only: no threat to the desk", all(not words(PR["money_only"][s]) & {"closure", "expansion"} for s in ("loss", "gain")))
ok &= check("threat only: no money", all("$" not in f[s] and not words(f[s]) & {"loss", "profit", "million"}
                                         for f in PR["threat_only"]["families"] for s in ("loss", "gain")))
rs = PR["responsibility"]
you_sentence = B["versions"]["loss + you"][len(B["versions"]["loss"]):].strip()
differ = words(you_sentence) ^ words(rs["build_control"])
ok &= check(f"the control sentence matches the responsibility sentence in length, differing only in {sorted(differ)}",
            len(you_sentence.split()) == len(rs["build_control"].split()) and differ == {"responsible", "for", "informed", "of"})
checks = rs["you_paraphrases"] + rs["informed_in_other_words"] + rs["neutral_sentences"]
ok &= check("responsibility checks: no sentence shares a word that differs between the two",
            all(not words(s) & differ for s in checks))
ok &= check("neutral sentences: about neither results nor blame, and share no word with the responsibility sentence",
            all(not words(s) & (words(you_sentence) | {"results", "report", "blame", "accountable", "you", "your"})
                for s in rs["neutral_sentences"]))
ok &= check("weather: no money, no desk", all(not words(f[s]) & (KEY | {"million", "desk"}) and "$" not in f[s]
                                              for f in PR["weather"]["families"] for s in ("bad", "good")))
ok &= check("the probes fingerprint is 8 characters", len(probes_fingerprint()) == 8)
ok &= check("chance: 3 families all right 12.5% of the time, 6 families 1.6%, 5 of 6 or better 10.9%",
            chance(1.0, 3) == 0.125 and chance(1.0, 6) == 1 / 64 and abs(chance(5 / 6, 6) - 7 / 64) < 1e-12)

# ---- the prompts -----------------------------------------------------------------------------------------------------
P = with_turns(prompt_rows(B, PR), FRAMED, SETUPS, B)
counts = P.groupby(["set", "time"]).size().to_dict()
print("   prompts:", len(P), counts)
ok &= check("262 prompts: the briefings (26 at 08:00, 52 at 09:30 with and without the request), their control sentence "
            "(12 + 12), other words (24 + 24), the responsibility checks (28 + 28), and at 08:00 12 flips, 12 money only, "
            "8 threat only, 24 weather",
            counts == {("main", "08:00"): 26, ("main", "09:30"): 52, ("you_control", "08:00"): 12, ("you_control", "09:30"): 12,
                       ("paraphrase", "08:00"): 24, ("paraphrase", "09:30"): 24, ("you_check", "08:00"): 28,
                       ("you_check", "09:30"): 28, ("flip", "08:00"): 12, ("money_only", "08:00"): 12,
                       ("threat_only", "08:00"): 8, ("weather", "08:00"): 24})
sample = [P.index[(P.set == "main") & (P.time == "09:30") & (P.version == "loss + you")][0],
          P.index[(P.set == "main") & (P.time == "09:30") & (P.version == "gain (no request)")][0],
          P.index[(P.set == "paraphrase") & (P.time == "09:30")][0], P.index[(P.set == "flip")][0], P.index[(P.set == "weather")][-1]]
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
G = groups(P)
ok &= check("the 08:00 and 09:30 groups of other words and responsibility checks do not mix",
            all(P.loc[G[k], "time"].eq("08:00").all() for k in ("paraphrase_loss", "paraphrase_gain", "you_check_you", "you_check_neutral"))
            and all(P.loc[G[k], "time"].eq("09:30").all() for k in ("paraphrase9_loss", "paraphrase9_gain", "you_check9_you")))
ok &= check("families P1-P3 choose the layer, P4-P6 test it, and the two do not overlap",
            set(P.loc[G["paraphrase_loss_select"], "family"]) == {"P1", "P2", "P3"}
            and set(P.loc[G["paraphrase_loss_test"], "family"]) == {"P4", "P5", "P6"})

# ---- the measures on stand-ins that know less than meaning ------------------------------------------------------------
texts = ["\n".join(t["content"] for t in turns) for turns in P.turns]
vocab = sorted({w for s in texts for w in toks(s)})
ix = {w: i for i, w in enumerate(vocab)}
X = np.zeros((len(P), len(vocab)))
for j, s in enumerate(texts):
    for w in toks(s):
        X[j, ix[w]] += 1
m = layer_measures(X, P, G)
print("   word counter:", {k: round(v, 2) for k, v in m.items()})
ok &= check("word counter: every word-level check is passed (1.0)",
            all(abs(m[k] - 1) < 1e-9 for k in WORD_LEVEL))
ok &= check("word counter: loss and gain in other words at chance, at 08:00 and at the request (0.5, gap 0)",
            m["paraphrase_acc"] == m["paraphrase_acc_test"] == m["paraphrase_acc_0930"] == 0.5
            and abs(m["paraphrase_gap"]) < 1e-9 and abs(m["select_gap"]) < 1e-9)
ok &= check("word counter: word flips backwards (0.0, gap -0.6)", m["flip_acc"] == 0.0 and abs(m["flip_gap"] + 0.6) < 1e-9)
ok &= check("word counter: money only 0.4, threat with closure/expansion 0.2, threat in other words 0",
            abs(m["money_only_gap"] - 0.4) < 1e-9 and abs(m["threat_gap_T1"] - 0.2) < 1e-9 and abs(m["threat_gap_T2"]) < 1e-9)
ok &= check("word counter: weather and the request unrelated (0.5, cosines 0), and so is every unrelated split",
            m["weather_acc"] == 0.5 and abs(m["weather_cos"]) < 1e-9 and abs(m["request_cos"]) < 1e-9 and m["null_cos_max"] < 1e-9)
ok &= check("word counter: responsibility and 'informed' checks at chance (0.5), any-sentence cosine 0",
            m["you_check_acc"] == m["informed_check_acc"] == m["you_check_acc_0930"] == 0.5 and abs(m["any_sentence_cos"]) < 1e-9)
ok &= check("every measure has a description", set(m) == set(COLUMNS))

BAD = {"loss", "closure", "red", "below", "down", "back", "worse", "doubt", "missed", "wind", "wound", "shut", "poor", "under", "cut"}
GOOD = {"profit", "expansion", "black", "above", "up", "build", "built", "better", "secured", "exceeded", "strong", "over",
        "increased"}
valence = np.array([sum((w.lower() in BAD) - (w.lower() in GOOD) for w in toks(s)) for s in texts], float)
mv = layer_measures(np.c_[X, 10 * valence], P, G)
ok &= check(f"word valence (how good or bad single words sound, no context): passes other words "
            f"({mv['paraphrase_acc']:.2f}) and fails the flips ({mv['flip_acc']:.2f})",
            mv["paraphrase_acc"] == 1 and mv["paraphrase_acc_test"] == 1 and mv["flip_acc"] == 0 and mv["flip_gap"] < 0)

informed = np.array([float(any(x in t for x in [rs["build_control"]] + rs["informed_in_other_words"])) for t in P.text])
mi = layer_measures(np.c_[informed, np.zeros((len(P), 2))], P, G)
ok &= check(f"'informed only' stand-in: the responsibility check stays at chance ({mi['you_check_acc']:.2f}) and only "
            f"the 'informed' side moves ({mi['informed_check_acc']:.2f})", mi["you_check_acc"] == 0.5 and mi["informed_check_acc"] == 1)

# ---- a stand-in that knows the meaning passes the meaning checks ----------------------------------------------------
meaning = np.array([1.0 if s in ("loss", "bad") else -1.0 if s in ("gain", "good") else 0.0 for s in P.side])
resp = np.where(P.side == "you", 1.0, 0.0) + np.where(P.you, 1.0, 0.0)
Xm = np.c_[meaning * np.where(P.set == "weather", 0, 1), resp]
mm = layer_measures(Xm, P, G)
ok &= check("a stand-in that encodes the meaning: other words (also at the request), flips and responsibility 1.0; "
            "weather and 'informed' 0.5",
            mm["paraphrase_acc"] == mm["paraphrase_acc_test"] == mm["paraphrase_acc_0930"] == 1 and mm["flip_acc"] == 1
            and mm["flip_gap"] > 0 and mm["you_check_acc"] == mm["you_check_acc_0930"] == 1
            and mm["weather_acc"] == 0.5 and mm["informed_check_acc"] == 0.5)

# ---- choosing the layer, the reading, the features ------------------------------------------------------------------
LT = pd.DataFrame([{"layer": L, **layer_measures(np.c_[X, L * valence], P, G)} for L in range(8)])
best, middle = choose_layer(LT)
ok &= check(f"the dial layer is chosen among the middle layers on families P1-P3 (layer {best} of 0-7, the largest share)",
            2 <= best <= 6 and LT.at[best, "select_gap"] == middle.select_gap.max())
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
