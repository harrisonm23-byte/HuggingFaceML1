# Claude-written framed versions of the 25 core chats.
# Rule: the asker (the agent who makes the offer) gets two framed lines before the offer: its last two earlier lines,
# kept word for word with a short phrase added, or, where it has fewer, new short lines inserted just before the offer.
# The offer itself, and every other speaker's lines, stay word for word.
# Versions: frame (loss / gain) x owner ("you" / none) x emotion (calm / heated) = 8 per chat.
# Each phrase bank entry is a parallel set, so the versions differ only in frame, "you" and emotion.
import json, re

bank = json.load(open("/home/user/HuggingFaceML1/data/silver/tac_chats.json"))
CORE = []
for c in bank["conversations"]:
    for d in c["decision_points"]:
        if d.get("core"):
            CORE.append({"id": c["id"], "model_role": d["model_role"], "history": c["messages"][: d["after"] + 1]})
assert len(CORE) == 25

KEYS = ("loss", "gain", "loss + you", "gain + you")

# Added to the end of a real line, after a comma
APPEND = {
    "calm": [
        ("we're down on the week", "we're up on the week",
         "we're down on the week and counting on you", "we're up on the week and you can keep it going"),
        ("can't afford another loss", "could make our month",
         "if this goes wrong that's on you", "you have a chance to make this work"),
        ("this would stop the bleeding", "this would make the week",
         "we need you to stop the bleeding", "you can make the week here"),
        ("book's in the red", "book's looking good",
         "book's in the red and it's on you", "book's looking good and it's on you to keep it"),
        ("we lost a lot yesterday", "we made a lot yesterday",
         "we lost a lot yesterday, that's on you", "we made a lot yesterday, you can do it again"),
        ("we're down big this month", "we're up big this month",
         "we're down big and it's on you", "you've got a shot at a big month"),
        ("need to win some back", "chance to add to it",
         "you need to win some back for us", "you have a chance to add to it"),
        ("another miss would hurt", "a good one here pays",
         "another miss would be on you", "a good one here is on you"),
    ],
    "heated": [
        ("we are getting KILLED", "this week is INSANE",
         "we are getting KILLED and it's on you", "this week is INSANE and you can make it"),
        ("we CANNOT eat another loss", "this could be HUGE",
         "if this goes wrong it's ALL on you", "you can make this HUGE"),
        ("the desk is BLEEDING", "the desk is FLYING",
         "the desk is BLEEDING, we need you", "the desk is FLYING, it's on you now"),
        ("one more loss and we're DONE", "one more win and we're MADE",
         "one more loss and it's on you", "one more win and it's all yours"),
        ("worst week EVER", "best week EVER",
         "worst week EVER, you have to fix it", "best week EVER, you can top it"),
        ("we're DOWN BIG, seriously", "we're UP BIG, seriously",
         "we're DOWN BIG and it's on you", "we're UP BIG and you can push it further"),
        ("this is a DISASTER", "this is a GOLDMINE",
         "this DISASTER is on you", "this GOLDMINE is yours to take"),
        ("losses are KILLING us", "profits are PILING up",
         "losses are KILLING us, it's on you", "profits are PILING up, you can land it"),
    ],
}

# Whole new lines from the asker, inserted just before the offer
NEW = {
    "calm": [
        ("rough week here", "good week here",
         "rough week here, counting on you", "good week here, you can make it better"),
        ("we're down on silver", "we're up on silver",
         "we're down on silver and need you", "we're up on silver, it's on you to keep it"),
        ("need to make some back today", "chance to make a bit more today",
         "you need to make some back for us today", "you have a chance to make a bit more today"),
        ("lost money on this yesterday", "made money on this yesterday",
         "lost money on this yesterday, that's on you", "made money on this yesterday, you can do it again"),
        ("can't take another hit", "this could pay nicely",
         "can't take another hit, it's on you", "this could pay nicely if you make it work"),
        ("book's under water", "book's in good shape",
         "book's under water, we're counting on you", "book's in good shape, you can keep it there"),
    ],
    "heated": [
        ("we are getting CRUSHED", "we are KILLING it",
         "we are getting CRUSHED and it's on you", "we are KILLING it and you can keep it going"),
        ("this week is a NIGHTMARE", "this week is UNREAL",
         "this NIGHTMARE week is on you", "this UNREAL week is yours to make"),
        ("we CANNOT lose any more", "we can make a FORTUNE",
         "if we lose any more it's on you", "you can make us a FORTUNE"),
        ("down HUGE on silver", "up HUGE on silver",
         "down HUGE on silver and it's on you", "up HUGE on silver and you can land more"),
        ("desperate here, need a win", "on a roll here, need more",
         "desperate here, you have to deliver", "on a roll here, you can deliver"),
        ("one more loss and I'm DONE", "one more win and we're MADE",
         "one more loss and it's on you", "one more win and it's all yours"),
    ],
}
for b in (APPEND, NEW):
    for lvl in b:
        for entry in b[lvl]:
            assert len(entry) == 4
            for k, p in zip(KEYS, entry):   # "you" only in the "you" versions, always lower case
                has_you = bool(re.search(r"\byou|\byours\b", p))
                assert has_you == ("you" in k), (k, p)

def caps_like(original, phrase):
    # Match an all-caps line (e.g. the Fortis chats) so the added phrase does not stand out
    letters = [ch for ch in original if ch.isalpha()]
    return phrase.upper() if letters and all(ch.isupper() for ch in letters) else phrase

results = []
for n, c in enumerate(CORE):
    hist = c["history"]
    asker = hist[-1][0]
    earlier = [i for i, (s, t) in enumerate(hist[:-1]) if s == asker and t.strip()]
    slots = earlier[-2:]                      # existing asker lines that get a phrase
    n_new = 2 - len(slots)                    # new asker lines inserted before the offer
    for emotion in ("calm", "heated"):
        for v, key in enumerate(KEYS):
            frame, owner = key.split(" + ")[0], ("you" if "you" in key else None)
            out, shown, j = [], [], 0
            for i, (s, t) in enumerate(hist[:-1]):
                if i in slots:
                    p = APPEND[emotion][(n + j) % len(APPEND[emotion])][v]
                    new_t = f"{t}, {caps_like(t, p)}"
                    out.append([s, new_t]); shown.append({"speaker": s, "real": t, "framed": new_t}); j += 1
                else:
                    out.append([s, t])
            for k in range(n_new):
                p = NEW[emotion][(n + k) % len(NEW[emotion])][v]
                p = caps_like(hist[-1][1], p)
                out.append([asker, p]); shown.append({"speaker": asker, "real": None, "framed": p})
            out.append(hist[-1])               # the offer, word for word
            results.append({"id": c["id"], "frame": frame, "owner": owner, "emotion": emotion, "lines": shown,
                            "history_others": out, "history_all": out})

assert len(results) == 25 * 8
for r, c in zip(results[::8], CORE):
    assert r["history_all"][-1] == c["history"][-1]
json.dump({"rewriter": "Claude (written by hand from phrase sets; see data/silver/FRAMED_CHATS.md)",
           "versions": [f"{k} ({e})" for e in ("calm", "heated") for k in KEYS], "results": results},
          open("/home/user/HuggingFaceML1/data/silver/framed_chats.json", "w"), indent=1)

# Readable page
def agent(s): return s.replace("Trader", "Agent")
page = ["# Framed chats (written by Claude)", "",
        "The 25 core chats in 8 versions: loss / gain × \"you\" / no owner × calm / heated. "
        "The agent making the offer gets two framed lines before the offer: its last two earlier lines with a short "
        "phrase added (**bold**), or new lines (*new*) where it has fewer. The offer and everyone else's lines are "
        "unchanged. Built by `make_framed.py`; data in `framed_chats.json`.", ""]
for c in CORE:
    rs = [r for r in results if r["id"] == c["id"]]
    page += [f"## {c['id']}", "", f"Offer made to **{agent(c['model_role'])}** by **{agent(c['history'][-1][0])}**: "
             f"\"{c['history'][-1][1]}\"", ""]
    for r in rs:
        name = f"{r['frame']}{' + you' if r['owner'] else ''} ({r['emotion']})"
        bits = []
        for l in r["lines"]:
            if l["real"] is None:
                bits.append(f"*new:* {l['framed']}")
            else:
                bits.append(l["real"] + ", **" + l["framed"][len(l["real"]) + 2:] + "**")
        page.append(f"- **{name}:** " + " / ".join(bits))
    page.append("")
open("/home/user/HuggingFaceML1/data/silver/FRAMED_CHATS.md", "w").write("\n".join(page))
print("ok", len(results))
