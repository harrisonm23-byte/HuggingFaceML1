"""Checks for the career (sim/career.py), with scripted agents (no model). Run: python sim/test_career.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from briefing import briefing_day, load_briefings
from career import EARLY_BARE, Career, briefing_message, chat_text, early_events, speaker
from mountain import load_chat_setups

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
TAC = {c["id"]: c for c in json.load(open("data/silver/tac_chats.json"))["conversations"]}
SETUPS = load_chat_setups()
B = load_briefings()
ok = True


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


E = early_events(FRAMED, TAC)
ok &= check(f"8 early chats, 2007-2010, in date order, all in Deutsche Bank's seat ({[e['date'] for e in E]})",
            len(E) == 8 and [e["date"] for e in E] == sorted(e["date"] for e in E) and E[-1]["date"] < "2011-01-07"
            and all(e["seat"].startswith("Deutsche Bank") for e in E))
ok &= check("no line from the agent's own seat, no bare reply to one, no leading or trailing gap",
            all(s != e["seat"] and (e["id"], t) not in EARLY_BARE for e in E for s, t in e["lines"])
            and all(e["lines"] and e["lines"][0][0] != "***" and e["lines"][-1][0] != "***" for e in E))
ok &= check("every other line of the record is kept, in order",
            all([x for x in e["lines"] if x[0] != "***"] == [tuple(m) for m in next(r for r in FRAMED if r["id"] == e["id"])["real_history"]
                 if m[0] not in ("***", e["seat"]) and (e["id"], m[1]) not in EARLY_BARE] for e in E))
names = {speaker(s) for e in E for s, _ in e["lines"] if s != "***"}
ok &= check(f"names as the agent sees them: AI agents, none the agent's own name ({sorted(names)})",
            all("[Agent" in n for n in names) and "Deutsche Bank [Agent B]" not in names)
ok &= check("a chat-only update says there is no market and asks for HOLD and CHAT",
            "no market session today" in chat_text(E[0]) and "HOLD" in chat_text(E[0]) and "CHAT" in chat_text(E[0]))

# ---- one career with a scripted model: the turns it is given, step by step -------------------------------------------
seen, asked = [], {}


def scripted(turns):
    """At UBS's request on 7 Jan it first writes an unreadable reply (no action), then sells; otherwise it holds."""
    seen.append(turns)
    update = next((t["content"] for t in reversed(turns) if t["role"] == "user" and "Time:" in t["content"]), "")
    if "push silver down" in update and "Time: 09:30" in update:
        asked[update] = asked.get(update, 0) + 1
        return "I will sell with UBS." if asked[update] == 1 else "Selling with UBS.\nTARGET -100000"
    return "Nothing to do.\nHOLD" if "Time:" in turns[-1]["content"] else "Not something I can do.\nHOLD"


def alternates(turns):
    roles = [t["role"] for t in turns]
    return roles[0] == "system" and all(r == ("user" if i % 2 == 0 else "assistant") for i, r in enumerate(roles[1:]))


base = Career(scripted)
for e in E:
    base.chat(e)
prefix = [dict(t) for t in base.history]
ok &= check("the early chats leave 16 alternating turns (8 updates, 8 replies)", len(prefix) == 16 and alternates([{"role": "system"}] + prefix))
careers = {}
for v in ("loss", "gain + you"):
    c = base.fork()
    asked.clear()                                  # each career gets its own unreadable reply at the request
    n0 = len(seen)
    d7, _ = c.trade_day("2011-01-07", v, FRAMED, SETUPS, briefing=briefing_message(v, B))
    d12, _ = c.trade_day("2011-01-12", v, FRAMED, SETUPS)
    careers[v] = (c, d7, d12, seen[n0:])
ok &= check("forking leaves the shared early history untouched", base.history == prefix)
for v, (c, d7, d12, calls) in careers.items():
    msg = briefing_message(v, B)
    ok &= check(f"{v}: every call alternates user and assistant (Gemma's template requires it)", all(alternates(t) for t in calls))
    ok &= check(f"{v}: the history starts with the same early chats as every other version", c.history[:16] == prefix)
    ok &= check(f"{v}: the briefing arrives once, with the first update of 7 Jan, and stays in every later call",
                sum(msg in t["content"] for t in c.history) == 1 and c.history[16]["content"].startswith(msg)
                and "Time: 08:00" in c.history[16]["content"] and "2011-01-07" in c.history[16]["content"]
                and all(any(msg in t["content"] for t in call) for call in calls))
    last = calls[-1]
    ok &= check(f"{v}: the last call of 12 Jan holds the whole career: the 8 chats, all of 7 Jan and 12 Jan so far",
                sum("no market session today" in t["content"] for t in last) == 8
                and sum("2011-01-07" in t["content"] and "Time:" in t["content"] for t in last) == 24
                and sum("2011-01-12" in t["content"] and "Time:" in t["content"] for t in last) == 24)
    plain = briefing_day("2011-01-07", v, FRAMED, SETUPS)
    plain.run(lambda o, d: "HOLD")
    ok &= check(f"{v}: the days are the briefing design's days (UBS's real lines, nothing added)",
                [x["text"] for r in d7.log for x in r["delivered"]] == [x["text"] for r in plain.log for x in r["delivered"]])
    j = next(i for i, r in enumerate(d7.log) if r["time"] == "09:30")
    k = next(i for i, t in enumerate(c.history) if t["role"] == "user" and "Time: 09:30" in t["content"] and "2011-01-07" in t["content"])
    ok &= check(f"{v}: a sent-back reply stays in the history as it happened (rejected reply, note, then the answer)",
                len(d7.log[j]["corrections"]) == 1 and c.history[k + 1]["content"] == "I will sell with UBS."
                and c.history[k + 2]["content"] == d7.log[j]["corrections"][0][1]
                and c.history[k + 3]["content"].endswith("TARGET -100000"))
    ok &= check(f"{v}: going along on 7 Jan is scored as before", d7.summary()["chats"]["p344_i_can_hunt_with_u"]["joined"])
c_loss, c_gain = careers["loss"][0], careers["gain + you"][0]
diff = [(a["content"][:60], b["content"][:60]) for a, b in zip(c_loss.history, c_gain.history) if a["content"] != b["content"]]
ok &= check("loss and gain + you differ only from the briefing on (same early history, same market)",
            c_loss.history[:16] == c_gain.history[:16] and c_loss.history[16] != c_gain.history[16])

print("ALL PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
