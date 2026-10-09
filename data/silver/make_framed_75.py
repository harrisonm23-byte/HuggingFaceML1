# Framed versions of 75 chats: the 25 core chats and 50 more, each fitted to its own context (2026-10-09).
#
# Input: frames_75.json (a context note and the framed phrases per chat, written by Claude per FRAMING_RULES.md).
# Same rules as make_framed.py: every line another trader wrote before the offer keeps its words and gets a short
# added phrase; chats with fewer than two such lines get new lines from the offering trader just before the offer;
# four versions (loss, gain, loss + "you", gain + "you"); the offer and the model's trader's lines are word for word.
# Added rule: a phrase must not contradict the chat's context (the price that day/week, positions the chat reveals)
# or leak anything the model's trader has not been shown. The 25 core chats were audited against that rule; 5 had a
# phrase that did not fit and use the corrected phrases here (framed_chats.json, used by the earlier runs, is kept
# as it was).
#
# Writes framed_chats_75.json (300 entries: 75 chats x 4 versions) and FRAMED_CHATS_75.md (readable).
import json, re

D = "/home/user/HuggingFaceML1/data/silver"
KEYS = ("loss", "gain", "loss + you", "gain + you")
YOU = re.compile(r"\b(you|your|you're|youre|you've|you'll|yours|u|ur)\b", re.I)
bank = json.load(open(f"{D}/tac_chats.json"))
conv = {c["id"]: c for c in bank["conversations"]}
F = json.load(open(f"{D}/frames_75.json"))["chats"]


def join(t, p):
    # "u got some? one more..." and "accelerate it . . . we're...", otherwise "line, phrase"
    return f"{t.rstrip()} {p}" if t.rstrip()[-1:] in ("?", "!", ".") else f"{t.rstrip()}, {p}"


results = []
for ch in F:
    c = conv[ch["id"]]
    dp = next(d for d in c["decision_points"] if d["after"] == ch["decision_after"] and d["model_role"] == ch["model_role"])
    hist, me, slots = c["messages"][: dp["after"] + 1], dp["model_role"], ch["frames"]
    rival = [i for i, (s, t) in enumerate(hist[:-1]) if s not in (me, "***") and t.strip()]
    # Checks: every other trader's line before the offer is framed, in order; at least two framed lines; phrase rules
    assert [w for w, *_ in slots if w != "new"] == rival, ch["id"]
    assert all(w == "new" for w, *_ in slots[len(rival):]), ch["id"]
    assert len(slots) >= 2 and hist[-1][0] != me, ch["id"]
    for k, (w, *ph) in enumerate(slots):
        last = k == len(slots) - 1
        assert len(ph) == 4, ch["id"]
        for key, p in zip(KEYS, ph):
            assert 1 <= len(p.split()) <= 15 and not re.search(r"\d", p), (ch["id"], p)
            if "you" in key:
                plain = ph[KEYS.index(key.split(" + ")[0])]
                assert YOU.search(p) or (not last and p == plain), (ch["id"], key, p)
            else:
                assert not YOU.search(p), (ch["id"], key, p)
    asker = hist[-1][0]
    for v, key in enumerate(KEYS):
        frame, owner = key.split(" + ")[0], ("you" if "you" in key else None)
        by_line = {w: ph[v] for w, *ph in slots if w != "new"}
        out, shown = [], []
        for i, (s, t) in enumerate(hist[:-1]):
            if i in by_line:
                nt = join(t, by_line[i])
                out.append([s, nt]); shown.append({"speaker": s, "real": t, "framed": nt})
            else:
                out.append([s, t])
        for w, *ph in slots:
            if w == "new":
                out.append([asker, ph[v]]); shown.append({"speaker": asker, "real": None, "framed": ph[v]})
        out.append(hist[-1])                                         # the offer, word for word
        assert [t for s, t in out if s == me] == [t for s, t in hist if s == me]   # the model's own lines, word for word
        results.append({"id": ch["id"], "set": ch["set"], "frame": frame, "owner": owner,
                        "model_role": me, "decision_after": dp["after"], "kind": dp["kind"], "decision": dp["decision"],
                        "real_history": hist, "lines": shown, "history_all": out})

assert len(results) == 4 * len(F) == 300
json.dump({"rewriter": "Claude, chat by chat (data/silver/frames_75.json, data/silver/make_framed_75.py)",
           "versions": list(KEYS), "results": results}, open(f"{D}/framed_chats_75.json", "w"), indent=1)


def agent(s):
    return s.replace("Trader", "Agent")


page = ["# Framed chats, 75 chats (written by Claude)", "",
        "The 25 core chats and 50 more from the complaint, each in 4 versions: loss, gain, loss + \"you\", gain + "
        "\"you\". Each chat starts with its context note (the price that day, who holds what, what is being asked), "
        "which the framing has to fit. Every line another trader wrote before the offer keeps its words and gets a "
        "short added phrase (**bold**); chats with fewer than two such lines get new lines just before the offer. The "
        "offer and the model's own lines are unchanged. Rules: `FRAMING_RULES.md`; data: `frames_75.json`; built and "
        "checked by `make_framed_75.py`.", "",
        "## Core chats changed by the context audit", ""]
for ch in F:
    a = ch.get("audit") or {}
    if a.get("previous_frames"):
        page.append(f"- **{ch['id']}**: " + " ".join(a["problems"]))
page.append("")
for set_name, title in [("core", "The 25 core chats"), ("new", "The 50 added chats")]:
    page += [f"## {title}", ""]
    for ch in [x for x in F if x["set"] == set_name]:
        c = conv[ch["id"]]
        dp = next(d for d in c["decision_points"] if d["after"] == ch["decision_after"] and d["model_role"] == ch["model_role"])
        hist, me, slots = c["messages"][: dp["after"] + 1], dp["model_role"], ch["frames"]
        page += [f"### {ch['id']} ({c.get('date') or 'no date'})", "",
                 f"The model plays **{agent(me)}**. The offer comes from **{agent(hist[-1][0])}** ({dp['kind']}: {dp['decision']}).", "",
                 f"*Context:* {ch['context']}", ""]
        by_line = {w: ph for w, *ph in slots if w != "new"}
        for i, (s, t) in enumerate(hist[:-1]):
            if s == "***":
                page.append("- [... messages omitted ...]")
            elif i in by_line:
                page.append(f"- {agent(s)}: {t} + …")
                page += [f"    - *{key}:* **{p}**" for key, p in zip(KEYS, by_line[i])]
            else:
                page.append(f"- {agent(s)}: {t}" + ("  *(model's own line, unchanged)*" if s == me else ""))
        for w, *ph in slots:
            if w == "new":
                page.append(f"- {agent(hist[-1][0])}: *(new line)*")
                page += [f"    - *{key}:* **{p}**" for key, p in zip(KEYS, ph)]
        page += [f"- {agent(hist[-1][0])}: {hist[-1][1]}  *(the offer, unchanged)*",
                 f"- *What the real trader did:* {dp.get('human_choice') or 'not quoted'}", ""]
open(f"{D}/FRAMED_CHATS_75.md", "w").write("\n".join(page))
print("ok", len(results), "entries,", len(F), "chats")
