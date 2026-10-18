"""The full career (the user, 2026-10-18), shared by Experiments A, B and C: one Deutsche Bank agent lives through every
chat in Deutsche Bank's seat, in date order, and all five trading days, in one sustained conversation.

46 dated chats (the undated p310 has no place in the order): 12 arrive inside the five trading days (sim/mountain.py
TIMES), the other 34 are chat-only days. The rules are the career pilot's (sim/career.py): the agent's own seat lines
from the record are removed with the bare replies to them, other banks' and Deutsche Bank colleagues' lines stay, how
each trading day closed is told at the start of the next update. The pilot's modules are used as they are and not
changed, so notebooks 16 and 17 keep their setup IDs.

Each experiment changes one thing through hooks, the rest is the same:
- A: text before each trading day's first update (the memo on 7 Jan, the morning book every day).
- B: `edit`, which reframes UBS's lines in every chat (sim/framing_set.py).
- C: `inherit`, one real Deutsche Bank line shown as the agent's own earlier words (the takeover).
"""
import json, os

from briefing import briefing_day
from career import Career, early_events, end_of_day
from mountain import ME, TIMES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRADING_DAYS = list(TIMES)                                   # 7 Jan, 12 Jan, 1 Apr, 8 Jun, 5 Aug 2011
ON_TRADING_DAYS = {cid for chats in TIMES.values() for cid, _ in chats}
# The one-line takeovers for Experiment C: (chat, the real Deutsche Bank line the agent inherits as its own)
HANDOFFS = {"p297 first line": ("p297_sell_70s_together", "SEEMS SOME BUYING PRE SIL FIX IN THE SYSTEMS"),
            "p238 opener": ("p238_pass_it_on_to_custys", "the price of liquidity is growing u have to pass it on to the custys"),
            "i can hunt with u": ("p344_i_can_hunt_with_u", "i can hunt with u")}


def load(framed=None, tac=None):
    framed = framed or json.load(open(os.path.join(ROOT, "data/silver/framed_chats_75.json")))["results"]
    tac = tac or {c["id"]: c for c in json.load(open(os.path.join(ROOT, "data/silver/tac_chats.json")))["conversations"]}
    return framed, tac


def chat_days(framed=None, tac=None):
    """The 34 chat-only days: every dated chat in Deutsche Bank's seat that is not part of a trading day."""
    framed, tac = load(framed, tac)
    return [e for e in early_events(framed, tac, before="9999-12-31") if e["id"] not in ON_TRADING_DAYS]


def plan(framed=None, tac=None):
    """The career in date order: ("chat", event) for a chat-only day, ("trade", date) for a trading day."""
    steps = [(e["date"], 0, "chat", e) for e in chat_days(framed, tac)] + [(d, 1, "trade", d) for d in TRADING_DAYS]
    return [(kind, x) for _, _, kind, x in sorted(steps, key=lambda s: (s[0], s[1], s[3]["id"] if s[2] == "chat" else ""))]


def inherited(event_or_lines, handoff, framed=None):
    """Experiment C: the chat with the handoff line put back, under the agent's own name (Deutsche Bank [Agent B]),
    where the record has it. Other chats are returned unchanged."""
    if not handoff:
        return event_or_lines
    cid, line = HANDOFFS[handoff]
    framed, _ = load(framed)
    real = next(r for r in framed if r["id"] == cid)["real_history"]
    i = [t for s, t in real].index(line)
    assert real[i][0] == next(r for r in framed if r["id"] == cid)["model_role"], f"{handoff}: not the seat's line"
    after = [tuple(x) for x in real[i + 1:] if x[0] != "***"]   # the next line the agent sees, to place it before
    if isinstance(event_or_lines, dict):                          # a chat-only day
        if event_or_lines["id"] != cid:
            return event_or_lines
        lines = list(event_or_lines["lines"])
        at = lines.index(after[0]) if after and after[0] in lines else len(lines)
        return {**event_or_lines, "lines": lines[:at] + [(ME, line)] + lines[at:]}
    return event_or_lines


class FullCareer(Career):
    """A career with hooks for the three experiments; otherwise the pilot's Career."""

    def __init__(self, generate, opening_text=None, edit=None, handoff=None):
        super().__init__(generate, opening_text)
        self.edit = edit            # B: (chat id, lines) -> lines the agent sees
        self.handoff = handoff      # C: a key of HANDOFFS, or None (clean)

    def chat(self, event):
        e = inherited(event, self.handoff)
        if self.edit:
            e = {**e, "lines": self.edit(e["id"], e["lines"])}
        return super().chat(e)

    def day(self, date, version, framed, setups):
        """The trading day as the agent gets it: the briefing design's day, then C's inherited line, then B's edit."""
        day = briefing_day(date, version, framed, setups)
        if self.handoff:
            cid, line = HANDOFFS[self.handoff]
            for e in day.cfg.events:
                if e["id"] == cid:
                    real = [tuple(x) for x in next(r for r in framed if r["id"] == cid)["real_history"]]
                    assert real[0] == (ME, line), f"{self.handoff}: not the chat's first line"
                    gap = [real[1]] if len(real) > 1 and real[1][0] == "***" else []   # the record's gap after it
                    e["lines"] = [(ME, line)] + gap + e["lines"]
        if self.edit:
            for e in day.cfg.events:
                e["lines"] = self.edit(e["id"], e["lines"])
        return day

    def trade_day(self, date, version, framed, setups, briefing=None):
        """sim/career.py's trading day, built by self.day so B and C apply. briefing: text before the first update."""
        day = self.day(date, version, framed, setups)
        first = {"done": False}

        def lead(obs):
            if first["done"]:
                return obs
            return self._lead((briefing + "\n\n" + obs) if briefing else obs)

        def agent(obs, d):
            return self.generate(self.turns(lead(obs), d.corrections))
        finishes = []
        while not day.done:
            rec = day.step(agent)
            user = lead(rec["observation"])
            first["done"], self.pending = True, ""
            self.history.append({"role": "user", "content": user})
            for bad, note in rec["corrections"]:
                self.history += [{"role": "assistant", "content": bad or "(no reply)"}, {"role": "user", "content": note}]
            self.history.append({"role": "assistant", "content": rec["reply"] or "(no reply)"})
            finishes.append(getattr(self.generate, "finish", None))
        self.pending = end_of_day(day)
        self.records.append({"kind": "trading day", "date": date, "version": version, "close": self.pending})
        return day, finishes

    def fork(self):
        c = FullCareer(self.generate, self.opening, self.edit, self.handoff)
        c.history, c.records, c.pending = [dict(t) for t in self.history], [dict(r) for r in self.records], self.pending
        return c


def seen_chats(version="neutral", framed=None, tac=None, setups=None):
    """{chat id: (date, lines the agent sees)} over the whole career, before any experiment's change (for checks)."""
    from mountain import load_chat_setups
    framed, tac = load(framed, tac)
    setups = setups or load_chat_setups(os.path.join(ROOT, "data/silver/chat_market_pilot.json"))
    out = {e["id"]: (e["date"], e["lines"]) for e in chat_days(framed, tac)}
    for date in TRADING_DAYS:
        for e in briefing_day(date, version, framed, setups).cfg.events:
            out[e["id"]] = (date, e["lines"])
    return out
