"""Same moment, different frame (the user, 20 Oct; from an outside review): a saved decision moment with only UBS's
current request changed, so the history, positions and P&L are held fixed.

At a push request, the agent's update lists the new chat messages ("  UBS [Agent A]: ..."). Every UBS line there is
one of the user's frozen lines (B's file, `sim/framing_set.py`) in the career's framing; it is swapped for the same
line in another framing. Bank C's line (F's file, `sim/peer_lines.py`) can be added after UBS's lines, as F's careers
show it. Nothing here writes or changes a line; the checks in `sim/test_matched.py` print counts, not text.
"""
import re

SHOWN_PEER = "Bank C [Agent C]"            # how F's careers show Bank C to the agent
_UBS = re.compile(r"^(  UBS \[Agent A\]: )(.*)$", re.M)


def swap_update(update, date, v0, v1, chats):
    """The update with every UBS line (framing v0) replaced by the same line in framing v1. chats: read_set()."""
    if v0 == v1:
        return update
    table = {}
    for c in chats:
        if c["date"] == date:
            for l in c["lines"]:
                table.setdefault(l["text"][v0], set()).add(l["text"][v1])

    def sub(m):
        alts = table.get(m.group(2))
        assert alts is not None, "a UBS line in the update is not in the file for its framing"
        assert len(alts) == 1, "a UBS line in the update matches file lines with different framings"
        return m.group(1) + next(iter(alts))
    new, n = _UBS.subn(sub, update)
    assert n >= 1, "no UBS line in the update"
    return new


def add_peer(update, line):
    """The update with Bank C's line after the last UBS line, as F's careers show it."""
    last = list(_UBS.finditer(update))[-1]
    return update[:last.end()] + f"\n  {SHOWN_PEER}: {line}" + update[last.end():]


def matched(career, idx, date, v0, v1, chats, peer_line=None):
    """A copy of the career whose update at `idx` carries UBS's request in framing v1 (and Bank C's line, if given);
    everything before it is untouched."""
    h = list(career["history"])
    text = swap_update(h[idx]["content"], date, v0, v1, chats)
    if peer_line is not None:
        text = add_peer(text, peer_line)
    h[idx] = {**h[idx], "content": text}
    return {**career, "history": h}
