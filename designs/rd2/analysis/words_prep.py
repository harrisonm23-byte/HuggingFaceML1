"""Agreement in words (the user, 28 Oct): every chat message the agent sent in reply to UBS in B's 50 careers, prepared
for blind grading. The grader sees the chat messages the agent received, with UBS's lines in the neutral wording (the
framed extras would give the framing away), and the agent's chat message only (no reasoning, no order). Items are
shuffled across careers and split into batches; key.json (not shown to graders) holds where each came from.

    python designs/rd2/analysis/words_prep.py results/words_b
"""
import glob, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from framing_set import read_set
from inside_careers import moments
from mountain import parse_reply

FOLDER = os.path.join(ROOT, "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
OUT = sys.argv[1]
BATCHES, RECHECK, SEED = 8, 0.2, 20261028
UBS = re.compile(r"^(  UBS \[Agent [AB]\]: )(.*)$", re.M)
NOTE = "Your reply was not accepted"
NEUTRAL_OF = {l["text"][v]: l["text"]["neutral"] for c in read_set() for l in c["lines"] for v in l["text"]}
asks = {(m["career_file"], m["history_index"]): m for m in moments(FOLDER, "B")}


def received(update):
    """The chat block of an update, UBS's lines in the neutral wording."""
    block = update.split("New chat messages:\n", 1)[1].split("\nReply as usual", 1)[0]

    def neutral(m):
        assert m.group(2) in NEUTRAL_OF, "a UBS line is not in the file"
        return m.group(1) + NEUTRAL_OF[m.group(2)]
    return UBS.sub(neutral, block).strip("\n")


items, key = [], {}
for path in sorted(glob.glob(os.path.join(FOLDER, "careers", "*.json"))):
    c = json.load(open(path))
    f, h = os.path.basename(path), c["history"]
    for i, t in enumerate(h):
        if t["role"] != "user" or "New chat messages:\n" not in t["content"]:
            continue
        if not UBS.search(t["content"].split("New chat messages:\n", 1)[1]):
            continue
        j = i + 1                                         # the reply that counted: past any sent-back ones
        while j + 2 < len(h) and h[j + 1]["role"] == "user" and h[j + 1]["content"].startswith(NOTE):
            j += 2
        chat = (parse_reply(h[j]["content"]).get("chat") or "").strip()
        m = asks.get((f, i))
        meta = {"career_file": f, "version": c["version"], "run": c["run"], "turn": i,
                "day": "chat-only" if "no market session today" in t["content"] else "trading",
                "date": re.search(r"\d{4}-\d{2}-\d{2}", t["content"]).group(0) if "Time:" in t["content"] else
                t["content"].split(".", 1)[0], "push_request": m["chat"] if m else None,
                "traded_along": m["joined"] if m else None, "has_chat": bool(chat)}
        items.append((meta, received(t["content"]), chat))
rng = random.Random(SEED)
rng.shuffle(items)
os.makedirs(OUT, exist_ok=True)
graded = []
for n, (meta, got, chat) in enumerate(items):
    iid = f"w{n:04d}"
    key[iid] = meta
    if chat:
        graded.append((iid, got, chat))


def write_batch(name, rows):
    with open(os.path.join(OUT, f"{name}.md"), "w") as fh:
        for iid, got, chat in rows:
            quoted = "\n".join("> " + x.strip() for x in got.splitlines())
            fh.write(f"### {iid}\nMessages the agent received:\n{quoted}\n\nThe agent's chat message:\n> {chat}\n\n")


for k in range(BATCHES):
    write_batch(f"batch_{k}", graded[k::BATCHES])
check = rng.sample(graded, round(RECHECK * len(graded)))
for k in range(2):
    write_batch(f"recheck_{k}", check[k::2])
json.dump(key, open(os.path.join(OUT, "key.json"), "w"), indent=0)
print(f"{len(items)} replies to UBS; {len(graded)} with a chat message, in {BATCHES} batches of about "
      f"{len(graded) // BATCHES}; {len(check)} re-checked in 2 batches")
