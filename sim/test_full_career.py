"""Checks for the full career (sim/full_career.py), with scripted agents (no model). Run: python sim/test_full_career.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from career import Career, career_opening, chat_text, speaker
from framing_set import frame, is_ubs, match, read_set
from full_career import HANDOFFS, TRADING_DAYS, FullCareer, chat_days, plan, restore, run, seen_chats, state
from mountain import ME, load_chat_setups

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
TAC = {c["id"]: c for c in json.load(open("data/silver/tac_chats.json"))["conversations"]}
SETUPS = load_chat_setups()
AGENT = "Deutsche Bank [Agent B]"
ok = True


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


def hold(turns):
    return "Watching the market.\nHOLD"


P = plan(FRAMED, TAC)
dates = [x["date"] if k == "chat" else x for k, x in P]
seat_ids = {r["id"] for r in FRAMED if r["model_role"].startswith("Deutsche Bank") and TAC[r["id"]]["date"]}
SEEN = seen_chats("neutral", FRAMED, TAC, SETUPS)
ok &= check(f"the plan: 34 chat-only days and the 5 trading days, in date order ({sum(k == 'chat' for k, _ in P)} + "
            f"{sum(k == 'trade' for k, _ in P)}, {dates[0]} to {dates[-1]})",
            sum(k == "chat" for k, _ in P) == 34 and [x for k, x in P if k == "trade"] == TRADING_DAYS
            and dates == sorted(dates))
ok &= check(f"every dated chat in Deutsche Bank's seat appears exactly once, the undated p310 not at all "
            f"({len(SEEN)} of {len(seat_ids)})", set(SEEN) == seat_ids and len(seat_ids) == 46
            and "p310_smash_it_together" not in SEEN)
ok &= check("clean career: nothing is shown under the agent's own name (no words put in its mouth)",
            all(speaker(s) != AGENT and not s.startswith("Deutsche Bank [Trader B]") for d, L in SEEN.values() for s, t in L))

# A whole career with an agent that always holds: it runs, and the conversation is complete
c = FullCareer(hold, career_opening())
for kind, x in P:
    if kind == "chat":
        c.chat(x)
    else:
        c.trade_day(x, "neutral", FRAMED, SETUPS, briefing="BRIEFING " + x)
roles = [t["role"] for t in c.history]
chars = sum(len(t["content"]) for t in c.turns("next"))
ok &= check(f"a whole career runs: {len([r for r in c.records if r['kind'] == 'chat'])} chats, "
            f"{len([r for r in c.records if r['kind'] == 'trading day'])} trading days, {len(c.history) // 2} replies, "
            f"about {chars // 4:,} tokens of conversation at the end",
            len(c.records) == 39 and roles == ["user", "assistant"] * (len(roles) // 2))
users = [t["content"] for t in c.history if t["role"] == "user"]
ok &= check("each trading day's text (A's memo or morning book) comes before that day's first update, once",
            all(sum(u.startswith("BRIEFING " + d) or ("\n\nBRIEFING " + d) in u for u in users) == 1 for d in TRADING_DAYS))
ok &= check("each trading day's close is told at the start of the next update",
            all(any(u.startswith(f"End of {d}:") for u in users) for d in TRADING_DAYS[:-1]))

# The same as the career pilot where they overlap: the early chats and 7 Jan, update for update
old, new = Career(hold, career_opening()), FullCareer(hold, career_opening())
for kind, x in P:
    if kind == "trade" and x > "2011-01-07":
        break
    for k in (old, new):
        k.chat(x) if kind == "chat" else k.trade_day(x, "loss", FRAMED, SETUPS, briefing="MEMO")
ok &= check("up to the end of 7 Jan, the clean full career gives the agent exactly the pilot's updates (notebooks 16/17)",
            old.history == new.history)

# Experiment B: every UBS line the agent sees is the user's line for the version
T = match(SEEN, read_set())
for v in ("loss", "gain + you"):
    b = FullCareer(hold, career_opening(), edit=lambda cid, lines, v=v: frame(lines, v, T[cid]) if cid in T else lines)
    for kind, x in P:
        b.chat(x) if kind == "chat" else b.trade_day(x, "neutral", FRAMED, SETUPS)
    text = "\n".join(t["content"] for t in b.history if t["role"] == "user")
    want = [l["text"][v] for cid in T for l in T[cid]]
    real = [t for d, L in SEEN.values() for s, t in L if is_ubs(s)]
    # A record line may still be read only inside the user's line for it (form A keeps the line and adds a sentence)
    left = [r for r in real if len(r) > 12 and text.count(r) > sum(r in w for w in want)]
    ok &= check(f"B, {v}: all 58 of the user's lines reach the agent ({sum(w in text for w in want)} found); "
                f"no record line of UBS's is left outside them ({len(left)})", all(w in text for w in want) and not left)

# Experiment C: exactly one inherited line, under the agent's own name, where the record has it
for h, (cid, line) in HANDOFFS.items():
    k = FullCareer(hold, career_opening(), handoff=h)
    for kind, x in P:
        k.chat(x) if kind == "chat" else k.trade_day(x, "neutral", FRAMED, SETUPS)
    users = [t["content"] for t in k.history if t["role"] == "user"]
    mine = [u for u in users if f"{AGENT}: " in u]
    where = mine[0] if mine else ""
    nxt = [t for s, t in next(r for r in FRAMED if r["id"] == cid)["real_history"] if s != "***" and t != line][0]
    ok &= check(f"C, {h}: one inherited line, under the agent's name, before the record's next line",
                len(mine) == 1 and where.count(f"{AGENT}: ") == 1 and f"{AGENT}: {line}" in where
                and where.index(f"{AGENT}: {line}") < where.index(nxt))

# The run loop, and continuing after a disconnect: a career stopped after 12 Jan and continued from its saved state ends
# with the same conversation as one run straight through (with an agent whose replies do not depend on chance)
whole = run(FullCareer(hold, career_opening()), P, "neutral", FRAMED, SETUPS, before_day=lambda d: "BOOK " + d)
saved = {}


class Stopped(Exception):
    pass


def save_then_stop_after_12_jan(i, date, day, finishes):
    saved.update(json.loads(json.dumps(state(part, i + 1))))     # as written to and read back from a file
    if date == "2011-01-12":
        raise Stopped


part = FullCareer(hold, career_opening())
try:
    run(part, P, "neutral", FRAMED, SETUPS, before_day=lambda d: "BOOK " + d, after_day=save_then_stop_after_12_jan)
except Stopped:
    pass
again = FullCareer(hold, career_opening())
start = restore(again, saved)
run(again, P, "neutral", FRAMED, SETUPS, before_day=lambda d: "BOOK " + d, start=start)
ok &= check(f"a career stopped after 12 Jan and continued from its save (step {start} of {len(P)}) ends exactly like "
            "one run straight through", again.history == whole.history and again.records == whole.records)

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
