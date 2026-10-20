"""Checks for sim/matched.py on the saved careers (prints counts only, never a line's text).

    python sim/test_matched.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framing_set import FRAMINGS, read_set
from inside_careers import moments
from matched import SHOWN_PEER, add_peer, matched, swap_update
from peer_lines import CHAT_ID, read_peers

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "results", "full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
F = os.path.join(ROOT, "results", "full_career_gemma-3-12b-it_4bit_peer_same_frame_v2")
chats, peers = read_set(), read_peers()
pid_of = {c: p for p, c in CHAT_ID.items()}

# 1. B: every swap finds every UBS line; a swap and back is the original; to its own framing is no change
n, changed = 0, 0
for m in moments(B, "B"):
    career = json.load(open(os.path.join(B, "careers", m["career_file"])))
    upd = career["history"][m["history_index"]]["content"]
    for v1 in FRAMINGS:
        s = swap_update(upd, m["date"], m["version"], v1, chats)
        assert swap_update(s, m["date"], v1, m["version"], chats) == upd, "a swap and back is not the original"
        changed += s != upd
        n += 1
    assert swap_update(upd, m["date"], m["version"], m["version"], chats) == upd
    c2 = matched(career, m["history_index"], m["date"], m["version"], "loss", chats)
    assert c2["history"][:m["history_index"]] == career["history"][:m["history_index"]], "the history before changed"
print(f"B: {n} swaps checked, {changed} changed the update; every swap and back gives the original")

# 2. F: B's construction rebuilds F's own updates exactly (F's update without Bank C's line, plus Bank C's line)
k = 0
for m in moments(F, "F"):
    upd = json.load(open(os.path.join(F, "careers", m["career_file"])))["history"][m["history_index"]]["content"]
    assert upd.count(SHOWN_PEER) == 1, "an F update without exactly one Bank C line"
    without = re.sub(rf"\n  {re.escape(SHOWN_PEER)}: [^\n]*", "", upd)
    assert add_peer(without, peers[pid_of[m["chat"]]][m["version"]]["peer"]) == upd, "Bank C's line placed differently"
    k += 1
print(f"F: {k} updates rebuilt exactly from UBS's lines plus Bank C's line")
# 3. A swap to framing v1 shows the same UBS lines as B's own v1 careers at that request
ubs = lambda t: re.findall(r"^  UBS \[Agent A\]: .*$", t, re.M)
real, k = {}, 0
for m in moments(B, "B"):
    upd = json.load(open(os.path.join(B, "careers", m["career_file"])))["history"][m["history_index"]]["content"]
    real.setdefault((m["chat"], m["version"]), set()).add(tuple(ubs(upd)))
for m in moments(B, "B"):
    upd = json.load(open(os.path.join(B, "careers", m["career_file"])))["history"][m["history_index"]]["content"]
    for v1 in FRAMINGS:
        assert tuple(ubs(swap_update(upd, m["date"], m["version"], v1, chats))) in real[(m["chat"], v1)], \
            "a swapped update differs from B's own careers in that framing"
        k += 1
print(f"B: {k} swapped updates show UBS's lines exactly as B's careers in that framing do")
print("all matched-history checks OK")
