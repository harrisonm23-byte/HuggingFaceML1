"""Blind items: what each Ministral 3 career said in the chat before UBS's first push request (7 Jan 2011).

    python designs/rd2/analysis/history_words_prep.py      -> results/history_words_ministral/{key.json,packet.md}

Every chat-only day before 7 Jan 2011 (eight days, 2007-2010) in all 25 B careers: the messages the agent received
(UBS's lines in the neutral wording, so the framing is hidden) and the chat message it sent (its accepted reply when one
was sent back), shuffled across careers. Career, framing and trades are in the key only. history_words.py reads the labels.
"""
import json, os, random, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from framing_set import read_set
from mountain import parse_reply
FOLDER = os.path.join(ROOT, "results", "full_career_Ministral-3-14B-Instruct-2512-BF16_4bit_ubs_framing_v2")
OUT = os.path.join(ROOT, "results", "history_words_ministral")
UBS = re.compile(r"^(  UBS \[Agent [AB]\]: )(.*)$", re.M)
NOTE = "Your reply was not accepted"
NEUTRAL_OF = {l["text"][v]: l["text"]["neutral"] for c in read_set() for l in c["lines"] for v in l["text"]}


def received(update):
    block = update.split("New chat messages:\n", 1)[1].split("\nReply as usual", 1)[0]
    return UBS.sub(lambda m: m.group(1) + NEUTRAL_OF.get(m.group(2), m.group(2)), block).strip("\n")


items = []
for name in sorted(os.listdir(os.path.join(FOLDER, "careers"))):
    h = json.load(open(os.path.join(FOLDER, "careers", name)))["history"]
    days = [i for i, t in enumerate(h) if t["role"] == "user" and "You have no market session today" in t["content"]
            and int(re.search(r"\b(20\d\d)\b", t["content"]).group(1)) < 2011]
    assert len(days) == 8, (name, len(days))
    for n, i in enumerate(days):
        j = i + 1
        while j + 2 < len(h) and h[j + 1]["role"] == "user" and h[j + 1]["content"].startswith(NOTE):
            j += 2
        chat = (parse_reply(h[j]["content"]).get("chat") or "").strip()
        items.append(({"career_file": name, "day": n, "date": h[i]["content"].split(".")[0], "has_chat": bool(chat)},
                      received(h[i]["content"]), chat))
random.Random(20261030).shuffle(items)
key, packet = {}, []
for n, (meta, got, chat) in enumerate(items):
    iid = f"h{n:03d}"
    key[iid] = meta
    if chat:
        packet.append(f"### {iid}\nMessages the agent received:\n" + "\n".join("> " + x.strip() for x in got.splitlines())
                      + f"\n\nThe agent's chat message:\n> {chat}\n")
json.dump(key, open(os.path.join(OUT, "key.json"), "w"), indent=0)
open(os.path.join(OUT, "packet.md"), "w").write("\n".join(packet))
print(len(items), "replies;", len(packet), "with a chat message")
