"""Experiment F's peer (the user, frozen 2026-10-19): one more bank, Bank C, joins UBS at each of the six push requests
and says it is in, in the same framing as UBS's lines.

The lines are the user's own, read word for word from the frozen Word file (the full chats of every push request in all
five framings); nothing here writes or changes them. The file's fingerprint (sha256) is checked before anything is
read. Only Bank C's lines are taken from it: UBS's lines still come from B's frozen file (sim/framing_set.py), and the
UBS lines shown in this file are checked against those, so the two files cannot disagree. Bank C's line comes after all
of UBS's lines in the chat, before the agent's first decision. Peers say nothing on the 34 chat-only days. Checks print
codes only, not the text.
"""
import hashlib, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROZEN = os.path.join(ROOT, "designs", "rd2", "Experiment_F_full_transcripts_final.docx")
FROZEN_SHA256 = "fd3e0885f7ccd3370168be60edaedd1db9e6302faff50dd62dc6c1625e9e221c"
PEER = "Bank C [Trader C]"           # shown to the agent as "Bank C [Agent C]", like "UBS [Agent A]"
PUSH = {"p344": "down", "p316": "up", "p252": "up", "p250": "down", "p317": "down", "p253": "down"}
# The push requests' full chat ids on the trading days (an id's number alone is not unique: p252_pebble_avalanche is a
# chat-only day)
CHAT_ID = {"p344": "p344_i_can_hunt_with_u", "p316": "p316_bust_through_it", "p252": "p252_screw_other_people_harder",
           "p250": "p250_grow_our_mafia", "p317": "p317_stop_busters", "p253": "p253_11_oclock_rule"}
_LABEL = {"NEUTRAL": "neutral", "LOSS": "loss", "GAIN": "gain", "LOSS+YOU": "loss + you", "GAIN+YOU": "gain + you"}
_DAY = re.compile(r"^\d\. .*?(p\d+) — UBS wants the price (up|down)")


def fingerprint(path=FROZEN):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_frozen(path=FROZEN, expect=FROZEN_SHA256):
    """Stop unless the file is exactly the frozen one."""
    got = fingerprint(path)
    if got != expect:
        raise RuntimeError(f"The Experiment F file is not the frozen one (fingerprint {got[:16]}, frozen {expect[:16]}): "
                           "the official F run does not start. Restore the frozen file or record a new freeze.")
    return got


def read_peers(path=FROZEN, expect=FROZEN_SHA256):
    """{push request: {framing: {"ubs": [UBS's lines as the file shows them], "peer": Bank C's line}}}."""
    import docx
    check_frozen(path, expect)
    out, pid, framing = {}, None, None
    for p in docx.Document(path).paragraphs:
        t = p.text.strip()
        if _DAY.match(t):
            pid, wants = _DAY.match(t).groups()
            assert PUSH.get(pid) == wants, f"{pid}: not a push request, or the wrong direction"
            out[pid], framing = {}, None
        elif t in _LABEL and pid:
            framing = _LABEL[t]
            out[pid][framing] = {"ubs": [], "peer": None}
        elif framing and t.startswith("UBS:"):
            assert out[pid][framing]["peer"] is None, f"{pid} {framing}: a UBS line after Bank C's"
            out[pid][framing]["ubs"].append(t[len("UBS:"):].strip())
        elif framing and t.startswith("Bank C:"):
            assert out[pid][framing]["peer"] is None, f"{pid} {framing}: two Bank C lines"
            # Word's curly quote marks made straight, as in B's lines (the same characters UBS's lines use); words unchanged
            out[pid][framing]["peer"] = re.sub("[’‘]", "'", re.sub("[“”]", '"', t[len("Bank C:"):].strip()))
    assert set(out) == set(PUSH), f"push requests in the file: {sorted(out)}"
    for pid, f in out.items():
        assert list(f) == list(_LABEL.values()), f"{pid}: framings {list(f)}"
        assert all(x["ubs"] and x["peer"] for x in f.values()), f"{pid}: a framing without UBS's or Bank C's line"
    return out


def _same(a, b):
    """The same words, whatever the quote marks and spacing."""
    norm = lambda x: re.sub(r"\s+", " ", x.replace("’", "'").replace("‘", "'").replace("…", "...")).strip()
    return norm(a) == norm(b)


def check_ubs(peers, b_lines):
    """Every UBS line this file shows is B's frozen line for that framing (b_lines: sim/framing_set.match's output)."""
    for pid, cid in CHAT_ID.items():
        assert cid in b_lines, f"{pid}: no UBS lines in B's file"
        table = b_lines[cid]
        for framing, x in peers[pid].items():
            b = [l["text"][framing] for l in table]
            assert len(b) == len(x["ubs"]) and all(_same(u, v) for u, v in zip(x["ubs"], b)), \
                f"{pid} {framing}: UBS's lines differ from B's frozen file"


def with_peer(cid, lines, framing, peers):
    """The chat with Bank C's line after UBS's lines, for the six push requests; other chats unchanged."""
    pid = next((p for p, c in CHAT_ID.items() if c == cid), None)
    if pid is None:
        return lines
    return list(lines) + [(PEER, peers[pid][framing]["peer"])]
