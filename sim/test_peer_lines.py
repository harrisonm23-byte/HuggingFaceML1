"""Checks for Experiment F's peer (sim/peer_lines.py), with scripted agents (no model). Run: python sim/test_peer_lines.py
Checks print codes and counts only, not the lines."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from career import career_opening
from framing_set import FRAMINGS, frame, match, read_set
from full_career import FullCareer, plan, seen_chats
from mountain import load_chat_setups
from peer_lines import CHAT_ID, PEER, check_ubs, read_peers, with_peer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
TAC = {c["id"]: c for c in json.load(open("data/silver/tac_chats.json"))["conversations"]}
SETUPS = load_chat_setups()
P = plan(FRAMED, TAC)
ok = True


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


def hold(turns):
    return "Watching the market.\nHOLD"


PEERS = read_peers()
LINES = match(seen_chats("neutral", FRAMED, TAC, SETUPS), read_set())
ok &= check("the file holds all 6 push requests in all 5 framings",
            sorted(PEERS) == sorted(CHAT_ID) and all(list(f) == FRAMINGS for f in PEERS.values()))
check_ubs(PEERS, LINES)
ok &= check("every UBS line shown in the F file is B's frozen line for that framing", True)

# The user's design rules, within each push request
lead = all(PEERS[p][f]["peer"].startswith(PEERS[p]["neutral"]["peer"]) for p in PEERS for f in FRAMINGS)
ok &= check("every framed Bank C line starts with that day's neutral line", lead)
you = re.compile(r"\b(you|you're|your|deutsche)\b", re.I)
ok &= check("no 'you' or 'Deutsche' in neutral, loss or gain",
            not any(you.search(PEERS[p][f]["peer"]) for p in PEERS for f in ("neutral", "loss", "gain")))
ok &= check("every +you line names Deutsche",
            all(re.search(r"\bDeutsche\b", PEERS[p][f]["peer"]) for p in PEERS for f in ("loss + you", "gain + you")))
neutral = [PEERS[p]["neutral"]["peer"] for p in PEERS]
ok &= check("no neutral line repeats across the career", len(set(neutral)) == len(neutral))

# Only the six push requests get Bank C; the chat-only day that shares p252's number does not
ok &= check("p252_pebble_avalanche (a chat-only day) is unchanged",
            with_peer("p252_pebble_avalanche", [("UBS [Trader A]", "x")], "loss", PEERS) == [("UBS [Trader A]", "x")])


def run(c, version):
    for kind, x in P:
        c.chat(x) if kind == "chat" else c.trade_day(x, "neutral", FRAMED, SETUPS)
    return [t["content"] for t in c.history if t["role"] == "user"]


# A whole career per framing: Bank C's line reaches the agent once at each push request, after UBS's lines, in the
# same framing; B's framed UBS lines are all still there; nothing else changes
base = "\n".join(run(FullCareer(hold, career_opening()), "neutral"))
for v in FRAMINGS:
    edit = (lambda v: lambda cid, lines: with_peer(cid, frame(lines, v, LINES[cid]) if cid in LINES else lines, v, PEERS))(v)
    text = "\n".join(run(FullCareer(hold, career_opening(), edit=edit), v))
    mine = [PEERS[p][v]["peer"] for p in PEERS]
    once = all(text.count(m) == 1 for m in mine)
    other = [PEERS[p][f]["peer"] for p in PEERS for f in FRAMINGS if f != v
             and not any(PEERS[p][f]["peer"] in m for m in mine)]   # (the neutral line is the start of every framed one)
    ubs = [l["text"][v] for cid in LINES for l in LINES[cid]]
    order = all(text.index(PEERS[p][v]["peer"]) > text.index(LINES[CHAT_ID[p]][-1]["text"][v]) for p in PEERS)
    ok &= check(f"{v}: Bank C's 6 lines reach the agent once each, after UBS's, none from another framing; "
                f"all {len(ubs)} framed UBS lines there; shown as 'Bank C [Agent C]' ({text.count('Bank C [Agent C]')} times)",
                once and not any(o in text for o in other) and all(u in text for u in ubs) and order
                and text.count("Bank C [Agent C]") == 6 and "Bank C" not in base)

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
