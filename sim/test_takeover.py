"""Checks for Experiment C's ladder (sim/takeover.py), with scripted agents (no model). Run: python sim/test_takeover.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from career import EARLY_BARE, career_opening
from briefing import BARE_REPLIES
from framing_set import frame, match, read_set
from full_career import TRADING_DAYS, FullCareer, plan, seen_chats
from mountain import ME, load_chat_setups
from takeover import ALL, LadderCareer, with_own_lines

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
TAC = {c["id"]: c for c in json.load(open("data/silver/tac_chats.json"))["conversations"]}
SETUPS = load_chat_setups()
P = plan(FRAMED, TAC)
AGENT = "Deutsche Bank [Agent B]"
ok = True


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


def hold(turns):
    return "Watching the market.\nHOLD"


def run(c):
    for kind, x in P:
        c.chat(x) if kind == "chat" else c.trade_day(x, "neutral", FRAMED, SETUPS)
    return [t["content"] for t in c.history if t["role"] == "user"]


def others(lines):
    return [(s, t) for s, t in lines if s != ME and s != "***"]


# The inherited lines are the seat's real lines; everything else is exactly what a clean career shows
clean = seen_chats("neutral", FRAMED, TAC, SETUPS)
rows = {r["id"]: r for r in FRAMED}
good, n_own = True, 0
for cid, (date, lines) in clean.items():
    seat = ME if date in TRADING_DAYS else rows[cid]["model_role"]
    own = with_own_lines(cid, seat, FRAMED, BARE_REPLIES if date in TRADING_DAYS else EARLY_BARE)
    good &= others(own) == others(lines)
    record = [t for s, t in rows[cid]["real_history"] if s == seat]
    good &= [t for s, t in own if s == ME] == record
    n_own += len(record)
ok &= check(f"with the takeover, every chat shows the seat's real lines under the agent's name ({n_own} lines in all) and "
            "the other side's lines exactly as in a clean career", good)

clean_users = run(FullCareer(hold, career_opening()))
all_users = run(LadderCareer(hold, career_opening(), own_until=ALL))
jan_users = run(LadderCareer(hold, career_opening(), own_until="2011-01-07"))
mine = lambda users: sum(u.count(f"{AGENT}: ") for u in users)
ok &= check(f"a whole career runs in each arm: clean {mine(clean_users)}, up to 7 Jan {mine(jan_users)}, whole career "
            f"{mine(all_users)} lines under the agent's name", mine(clean_users) == 0 < mine(jan_users) < mine(all_users))
# up to 7 Jan: nothing inherited after the first trading day
idx_12jan = next(i for i, u in enumerate(jan_users) if "2011-01-12" in u)
ok &= check("up to 7 Jan: no inherited line after 7 Jan", mine(jan_users[idx_12jan:]) == 0 and mine(jan_users[:idx_12jan]) > 0)

# With UBS's lines reframed (E: everything combined), the framing still lands on every UBS line
T = match(clean, read_set())
both = LadderCareer(hold, career_opening(), own_until=ALL,
                    edit=lambda cid, lines: frame(lines, "loss + you", T[cid]) if cid in T and lines else lines)
text = "\n".join(run(both))
want = [l["text"]["loss + you"] for cid in T for l in T[cid]]
ok &= check(f"takeover with UBS's framing: all 58 framed UBS lines reach the agent ({sum(w in text for w in want)} found)",
            all(w in text for w in want))

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
