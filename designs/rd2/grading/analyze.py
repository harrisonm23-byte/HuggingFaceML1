# Usage: run in the folder holding key.json and the graders' labels_*.json files.
import json, glob
import pandas as pd
from scipy.stats import binomtest

key = pd.DataFrame(json.load(open("key.json")))
labels = {}
for f in sorted(glob.glob("labels_[0-9]*.json")):     # first grader (labels_sN.json = second grader)
    labels.update(json.load(open(f)))
key["label"] = key.code.map(labels)
missing = key.label.isna().sum()
print(f"labelled {key.label.notna().sum()} of {len(key)} ({missing} missing)\n")
key = key[key.label.notna()]
key["went"] = (key.label == "WENT_ALONG").astype(float)

hum = key[key.version == "human"]
print(f"Grader check: real traders' own replies labelled WENT_ALONG: {int(hum.went.sum())} of {len(hum)}\n")

m = key[key.version != "human"]
order = ["real", "loss", "gain", "loss + you", "gain + you"]
print("Label share (%) by condition and version")
tab = pd.crosstab([m.condition, m.version], m.label, normalize="index").mul(100).round(0)
print(tab.reindex(pd.MultiIndex.from_product([["extra party", "takeover"], order])).fillna(0).to_string(), "\n")

print("Went-along rate (%) by version x condition")
pv = m.pivot_table(index="version", columns="condition", values="went", aggfunc="mean").mul(100).round(0).reindex(order)
print(pv.to_string(), "\n")

def report(name, d):
    d = d.dropna()
    up, down = int((d > 0).sum()), int((d < 0).sum())
    p = binomtest(up, up + down).pvalue if up + down else float("nan")
    print(f"  {name:38s} {d.mean()*100:+5.0f} points | up in {up:2d} chats, down in {down:2d}, same in {len(d)-up-down:2d} | sign test p = {p:.3f}")

for cond in ["extra party", "takeover"]:
    p = m[m.condition == cond].pivot_table(index="id", columns="version", values="went", aggfunc="mean")
    print(f"[{cond}]  (per chat, on the went-along rate)")
    report("loss - gain, no 'you'", p["loss"] - p["gain"])
    report("loss - gain, with 'you'", p["loss + you"] - p["gain + you"])
    report("interaction (you - no you)", (p["loss + you"] - p["gain + you"]) - (p["loss"] - p["gain"]))
    report("'you' - no 'you' (both frames)", (p["loss + you"] + p["gain + you"] - p["loss"] - p["gain"]) / 2)
    report("framed (all 4) - real chat", p[["loss", "gain", "loss + you", "gain + you"]].mean(axis=1) - p["real"])
    print()
pc = m.pivot_table(index=["id", "version"], columns="condition", values="went", aggfunc="mean")
print("[takeover - extra party]")
report("all versions", (pc["takeover"] - pc["extra party"]).groupby("id").mean())
report("real chats only", (pc["takeover"] - pc["extra party"]).xs("real", level="version"))

# per chat table for the record
pt = m.pivot_table(index="id", columns=["condition", "version"], values="went", aggfunc="sum")
pt.to_csv("per_chat_went_along_counts.csv")
key.to_csv("graded_replies.csv", index=False)

# Second grader on a random sample: agreement with the first grader
import os
if os.path.exists("key_second.json"):
    second = {}
    for f in sorted(glob.glob("labels_s*.json")):
        second.update(json.load(open(f)))
    pairs = pd.DataFrame([{"first": labels.get(first), "second": second.get(code)}
                          for code, first in json.load(open("key_second.json")).items()]).dropna()
    agree = (pairs["first"] == pairs["second"]).mean()
    chance = sum(pairs["first"].value_counts(normalize=True).get(l, 0) * pairs["second"].value_counts(normalize=True).get(l, 0)
                 for l in set(pairs["first"]) | set(pairs["second"]))
    kappa = (agree - chance) / (1 - chance)
    went = ((pairs["first"] == "WENT_ALONG") == (pairs["second"] == "WENT_ALONG")).mean()
    print(f"\n[second grader] {len(pairs)} replies graded twice: same label {agree*100:.0f}% "
          f"(Cohen's kappa {kappa:.2f}); same went-along yes/no {went*100:.0f}%")
    print(pd.crosstab(pairs["first"], pairs["second"]).to_string())
