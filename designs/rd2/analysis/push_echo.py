"""Push and cue, the echo check (from the review of 28 Oct): before reading the carry, did the agent restate UBS's
framed words in its own replies before 12 January? If it did, setting UBS's lines back to neutral does not take the
frame out of the conversation: it is still there in the agent's words.

    python designs/rd2/analysis/push_echo.py          # writes results/push_carry/ECHO.md

For each framed career of B, every UBS line before the 12 January request: the words its framing adds to the neutral
line (`sim/push_carry.py` added); then the agent's replies between that line and the request: shared runs of three
words, and added words of five letters or more. A word or run counts only if none of B's neutral careers used it in its
replies before its own 12 January request (so "price", "stops", "I need to" do not count). A pointer to replies worth
reading, not a measure of meaning: a paraphrase in other words is missed.
"""
import collections, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
import push_carry as PC
from framing_set import read_set
from inside_careers import moments

FOLDER = os.path.join(ROOT, "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
OUT = os.path.join(ROOT, "results/push_carry")
NAME = {"loss + you": "blame", "loss": "loss", "gain + you": "credit", "gain": "gain"}
chats = read_set()
M = {m["career_file"]: m for m in moments(FOLDER, "B") if m["chat"] == PC.CUE_CHAT}
careers = {f: json.load(open(f"{FOLDER}/careers/{f}")) for f in M}

# what B's neutral careers wrote anyway before 12 January
base_words, base_grams = set(), set()
for f, c in careers.items():
    if c["version"] == "neutral":
        for t in c["history"][:M[f]["history_index"]]:
            if t["role"] == "assistant":
                ws = PC.WORD.findall(t["content"].lower())
                base_words |= set(ws)
                base_grams |= {" ".join(ws[i:i + 3]) for i in range(len(ws) - 2)}

rows = {}
for f, c in sorted(careers.items()):
    if c["version"] == "neutral":
        continue
    hits = []
    for e in PC.echoes(c, M[f]["history_index"], chats):
        shared = [g for g in e["shared"] if g not in base_grams]
        words = [w for w in e["words"] if w not in base_words]
        if shared or words:
            hits.append({**e, "shared": shared, "words": words})
    rows[f] = (c["version"], c["run"], hits)

md = ["# The echo check: did the agent restate UBS's framed words before 12 January? (exploratory)\n",
      "Produced by `designs/rd2/analysis/push_echo.py` from B's saved careers. For each UBS line before the 12 January "
      "request, the words its framing adds to the neutral line; then the agent's replies between that line and the "
      "request: shared runs of three words, or added words of five letters or more, that none of B's neutral careers "
      "used before 12 January. A pointer, not a measure: a paraphrase in other words is missed.\n",
      "| Framing | Careers | Restated any framed words | ...of the 7 January request | ...in a reply on 7 January or later |",
      "|---|---|---|---|---|"]
summary = {}
for v in ["loss + you", "loss", "gain + you", "gain"]:
    rs = [(run, hits) for vv, run, hits in rows.values() if vv == v]
    anyh = sum(bool(h) for _, h in rs)
    of7 = sum(any(x["ubs_date"] == PC.PUSH_DATE for x in h) for _, h in rs)
    late = sum(any(x["reply_date"] >= PC.PUSH_DATE for x in h) for _, h in rs)
    md.append(f"| {NAME[v]} | {len(rs)} | {anyh}/{len(rs)} | {of7}/{len(rs)} | {late}/{len(rs)} |")
    summary[NAME[v]] = {"careers": len(rs), "any": anyh, "of_7jan": of7, "late": late}
md += ["\n## What was restated, career by career\n",
       "UBS's framed words the agent's reply repeated (UBS's words, not the reply), with the date of UBS's line and of "
       "the reply.\n", "| Framing | Run | UBS's line (date) | Reply (date) | Repeated |", "|---|---|---|---|---|"]
for f, (v, run, hits) in rows.items():
    seen = collections.OrderedDict()
    for x in hits:
        seen.setdefault((x["ubs_date"], x["reply_date"]), set()).update(x["shared"] + x["words"])
    for (ud, rd), ws in seen.items():
        md.append(f"| {NAME[v]} | {run} | {ud} | {rd} | {', '.join(sorted(ws))} |")
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ECHO.md"), "w").write("\n".join(md) + "\n")
json.dump(summary, open(os.path.join(OUT, "echo.json"), "w"), indent=1)
print("\n".join(md))
