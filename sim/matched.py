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


def swap_update(update, date, v0, v1, chats, pattern=None):
    """The update with every UBS line (framing v0) replaced by the same line in framing v1. chats: read_set().
    pattern: which lines are UBS's (default: Agent A's, all a push request has; the chat-only days also have Agent B)."""
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
    new, n = (pattern or _UBS).subn(sub, update)
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


def priming_days(folder, career_file):
    """An A career's trading days, in date order (its days files hold each morning book exactly as the agent read it,
    and each day's P&L)."""
    import glob, json, os
    stem = career_file[:-len(".json")]
    return [json.load(open(p)) for p in sorted(glob.glob(os.path.join(folder, "days", f"{stem}_2011-*.json")))]


def swap_priming(career, v0, v1, days):
    """Experiment A's career with management's priming in version v1 instead of v0: the memo on the first trading
    morning and every morning book (whose 30-day P&L keeps carrying the agent's own P&L). Everything else, the agent's
    own words included, is untouched. days: priming_days()."""
    from briefing import load_briefings
    from career import briefing_message
    from morning_book import morning_book
    b, h, pnl = load_briefings(), list(career["history"]), 0.0
    turns = [i for i, t in enumerate(h) if t["role"] == "user" and "Morning book, " in t["content"]]
    assert len(turns) == len(days), "a morning book is missing from the conversation"
    for k, (i, d) in enumerate(zip(turns, days)):
        old, new = morning_book(d["date"], v0, pnl), morning_book(d["date"], v1, pnl)
        assert morning_book(d["date"], d["version"], pnl) == d["book"], "a book does not rebuild from its day's record"
        if k == 0:                                       # the memo comes just before the first book
            old = briefing_message(v0, b) + "\n\n" + old
            new = briefing_message(v1, b) + "\n\n" + new
        assert h[i]["content"].count(old) == 1, "the memo or book is not in its turn exactly once"
        h[i] = {**h[i], "content": h[i]["content"].replace(old, new)}
        pnl += d["summary"]["pnl"]
    return {**career, "history": h}
