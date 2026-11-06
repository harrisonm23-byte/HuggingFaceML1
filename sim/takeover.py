"""Experiment C's ladder (the user, 2026-10-19): how much of Deutsche Bank's real history the agent inherits as its own.

A new module, so sim/full_career.py (part of the setup IDs of A and B, which are running) is not changed. A career here
is a FullCareer with one more option, `own_until`: in every chat up to that date the seat's own lines from the record
are put back under the agent's own name (Deutsche Bank [Agent B]); "9999-12-31" means the whole career. The bare
replies that are dropped in a clean career stay dropped in every arm, so the other side's lines are the same in every
arm and only the agent's inherited lines differ. The single-line takeovers stay as they are (FullCareer's `handoff`).
"""
from briefing import BARE_REPLIES
from career import EARLY_BARE
from full_career import FullCareer, load
from mountain import ME

ALL = "9999-12-31"


def with_own_lines(cid, seat, framed, drop):
    """The chat as the record has it, with the seat's own lines under the agent's name and the bare replies in `drop`
    left out, gaps at the start, doubled or at the end dropped."""
    real = next(r for r in framed if r["id"] == cid)["real_history"]
    out = []
    for s, t in real:
        if (cid, t) in drop or (s == "***" and (not out or out[-1][0] == "***")):
            continue
        out.append((ME if s == seat else s, t))
    while out and out[-1][0] == "***":
        out.pop()
    return out


class LadderCareer(FullCareer):
    """A full career where the agent inherits its seat's real lines in every chat up to `own_until`."""

    def __init__(self, generate, opening_text=None, edit=None, own_until=None):
        super().__init__(generate, opening_text, edit=edit)
        self.own_until = own_until

    def chat(self, event):
        if self.own_until and event["date"] <= self.own_until:
            event = {**event, "lines": with_own_lines(event["id"], event["seat"], load()[0], EARLY_BARE)}
        return super().chat(event)

    def day(self, date, version, framed, setups):
        if self.own_until and date <= self.own_until:
            edit, self.edit = self.edit, None          # the inherited lines first, then the framing (if any)
            day = super().day(date, version, framed, setups)
            self.edit = edit
            for e in day.cfg.events:
                e["lines"] = with_own_lines(e["id"], ME, framed, BARE_REPLIES)
                if self.edit:
                    e["lines"] = self.edit(e["id"], e["lines"])
            return day
        return super().day(date, version, framed, setups)

    def fork(self):
        c = LadderCareer(self.generate, self.opening, self.edit, self.own_until)
        c.history, c.records, c.pending = [dict(t) for t in self.history], [dict(r) for r in self.records], self.pending
        return c
