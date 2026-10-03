# Claude-written framed versions of the 25 core chats.
# Rule: the asker (the agent who makes the offer) gets two framed lines before the offer: its last two earlier lines,
# kept word for word with a short phrase added at the end, or, where it has fewer, new short lines inserted just
# before the offer. The offer itself, and every other speaker's lines, stay word for word.
# Versions: loss / gain x "you" / no owner = 4 per chat. One emotion level, in the style of Claude's worked examples
# for notebook 09, which the user liked
# ("we're getting crushed this week", "can't eat another loss", "if this goes wrong that's on you").
# Each phrase set is parallel, so a chat's four versions differ only in frame and "you".
import json, re

bank = json.load(open("/home/user/HuggingFaceML1/data/silver/tac_chats.json"))
CORE = []
for c in bank["conversations"]:
    for d in c["decision_points"]:
        if d.get("core"):
            CORE.append({"id": c["id"], "model_role": d["model_role"], "history": c["messages"][: d["after"] + 1]})
assert len(CORE) == 25

KEYS = ("loss", "gain", "loss + you", "gain + you")

# (loss, gain, loss + you = blame / others counting on it, gain + you = responsibility for the chance)
PHRASES = [
    ("we're getting crushed this week", "this week's been great",
     "we're getting crushed this week and we're counting on you", "you've got a shot at a monster week here"),
    ("can't eat another loss", "could be a big day",
     "if this goes wrong that's on you", "it's on you to make this one work"),
    ("we're down big on silver", "we're up big on silver",
     "we're down big and it's on you", "you've got a real shot here"),
    ("need to get back to flat", "this could make the month",
     "we need you to get us back to flat", "you can make the month here"),
    ("we've been bleeding all week", "we've been printing money all week",
     "we've been bleeding all week, we're all counting on you", "we've been printing money all week, it's on you to keep it going"),
    ("one more bad day and we're done", "one more good day and we're set",
     "one more bad day and that's on you", "one more good day and you've made the week"),
    ("book's deep in the red", "book's way up",
     "book's deep in the red and it's on you", "book's way up and it's on you to land this"),
    ("lost a ton yesterday", "made a ton yesterday",
     "lost a ton yesterday, if this goes wrong that's on you", "made a ton yesterday, you have a chance to make this work"),
]
for entry in PHRASES:
    assert len(entry) == 4
    for k, p in zip(KEYS, entry):   # "you" only in the "you" versions, always lower case
        assert bool(re.search(r"\byou", p)) == ("you" in k), (k, p)

def caps_like(original, phrase):
    # Match an all-caps line (e.g. the Fortis chats) so the added phrase does not stand out
    letters = [ch for ch in original if ch.isalpha()]
    return phrase.upper() if letters and all(ch.isupper() for ch in letters) else phrase

STATES_PNL = {"we smashed it good"}

results = []
for n, c in enumerate(CORE):
    hist = c["history"]
    asker = hist[-1][0]
    # Lines that already state a profit or loss are left alone (a loss phrase there would contradict them)
    earlier = [i for i, (s, t) in enumerate(hist[:-1]) if s == asker and t.strip() and t not in STATES_PNL]
    slots = earlier[-2:]                      # existing asker lines that get a phrase
    n_new = 2 - len(slots)                    # new asker lines inserted before the offer
    for v, key in enumerate(KEYS):
        frame, owner = key.split(" + ")[0], ("you" if "you" in key else None)
        out, shown, j = [], [], 0
        for i, (s, t) in enumerate(hist[:-1]):
            if i in slots:
                p = PHRASES[(n + j) % len(PHRASES)][v]
                sep = " " if t.rstrip()[-1:] in ("?", "!", ".") else ", "   # "u got some? one more..." not "u got some?, ..."
                new_t = f"{t.rstrip()}{sep}{caps_like(t, p)}"
                out.append([s, new_t]); shown.append({"speaker": s, "real": t, "framed": new_t}); j += 1
            else:
                out.append([s, t])
        for k in range(n_new):
            p = caps_like(hist[-1][1], PHRASES[(n + j + k) % len(PHRASES)][v])
            out.append([asker, p]); shown.append({"speaker": asker, "real": None, "framed": p})
        out.append(hist[-1])                   # the offer, word for word
        results.append({"id": c["id"], "frame": frame, "owner": owner, "lines": shown,
                        "history_others": out, "history_all": out})

assert len(results) == 25 * 4
for r, c in zip(results[::4], CORE):
    assert r["history_all"][-1] == c["history"][-1]
json.dump({"rewriter": "Claude (phrase sets in data/silver/make_framed.py)", "versions": list(KEYS), "results": results},
          open("/home/user/HuggingFaceML1/data/silver/framed_chats.json", "w"), indent=1)

# Readable page
def agent(s): return s.replace("Trader", "Agent")
page = ["# Framed chats (written by Claude)", "",
        "The 25 core chats in 4 versions: loss, gain, loss + \"you\", gain + \"you\". "
        "The agent making the offer gets two framed lines before the offer: its last two earlier lines with a short "
        "phrase added at the end (**bold**), or new lines (*new*) where it has fewer. The offer and everyone else's "
        "lines are unchanged. Built by `make_framed.py`; data in `framed_chats.json`.", ""]
for c in CORE:
    page += [f"## {c['id']}", "", f"Offer made to **{agent(c['model_role'])}** by **{agent(c['history'][-1][0])}**: "
             f"\"{c['history'][-1][1]}\"", ""]
    for r in [r for r in results if r["id"] == c["id"]]:
        bits = []
        for l in r["lines"]:
            if l["real"] is None:
                bits.append(f"*new:* {l['framed']}")
            else:
                added = l["framed"][len(l["real"].rstrip()):].lstrip(", ")
                bits.append(l["framed"][: len(l["framed"]) - len(added)] + "**" + added + "**")
        page.append(f"- **{r['frame']}{' + you' if r['owner'] else ''}:** " + " / ".join(bits))
    page.append("")
open("/home/user/HuggingFaceML1/data/silver/FRAMED_CHATS.md", "w").write("\n".join(page))
print("ok", len(results))
