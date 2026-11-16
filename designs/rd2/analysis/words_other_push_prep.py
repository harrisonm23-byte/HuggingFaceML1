"""Blind items for the push-request replies of other models' B careers (as designs/rd2/analysis/words_prep.py, push requests only)."""
import glob, json, os, random, re, sys
ROOT = "/Users/harrisonmargolin/HuggingFaceML1"
sys.path.insert(0, os.path.join(ROOT, "sim"))
os.chdir(ROOT)
from framing_set import read_set
from inside_careers import moments
from mountain import parse_reply
UBS = re.compile(r"^(  UBS \[Agent [AB]\]: )(.*)$", re.M)
NOTE = "Your reply was not accepted"
NEUTRAL_OF = {l["text"][v]: l["text"]["neutral"] for c in read_set() for l in c["lines"] for v in l["text"]}
OUT = "/private/tmp/claude-501/-Users-harrisonmargolin/bc46a6bc-aadf-4947-b759-66fb23667e75/scratchpad/push_words"
os.makedirs(OUT, exist_ok=True)
def received(update):
    block = update.split("New chat messages:\n", 1)[1].split("\nReply as usual", 1)[0]
    return UBS.sub(lambda m: m.group(1) + NEUTRAL_OF.get(m.group(2), m.group(2)), block).strip("\n")
items, key = [], {}
for model, folder in (("qwen", "results/full_career_Qwen3.5-9B_4bit_ubs_framing_v2"),
                      ("ministral", "results/full_career_Ministral-3-14B-Instruct-2512-BF16_4bit_ubs_framing_v2")):
    for m in moments(folder, "B"):
        if not m["asked"]:
            continue
        h = json.load(open(f"{folder}/careers/{m['career_file']}"))["history"]
        i = m["history_index"]; j = i + 1
        while j + 2 < len(h) and h[j + 1]["role"] == "user" and h[j + 1]["content"].startswith(NOTE):
            j += 2
        chat = (parse_reply(h[j]["content"]).get("chat") or "").strip()
        items.append(({"model": model, "career_file": m["career_file"], "version": m["version"], "push_request": m["chat"],
                       "traded_along": m["joined"], "has_chat": bool(chat)}, received(h[i]["content"]), chat))
random.Random(20261030).shuffle(items)
batch = []
for n, (meta, got, chat) in enumerate(items):
    iid = f"x{n:04d}"; key[iid] = meta
    if chat:
        batch.append(f"### {iid}\nMessages the agent received:\n" + "\n".join("> " + x.strip() for x in got.splitlines())
                     + f"\n\nThe agent's chat message:\n> {chat}\n")
json.dump(key, open(f"{OUT}/key.json", "w"), indent=0)
half = (len(batch) + 1) // 2
open(f"{OUT}/batch_0.md", "w").write("\n".join(batch[:half])); open(f"{OUT}/batch_1.md", "w").write("\n".join(batch[half:]))
print(len(items), "push-request replies;", len(batch), "with a chat message;", {m: sum(k["model"] == m for k in key.values()) for m in ("qwen", "ministral")})
