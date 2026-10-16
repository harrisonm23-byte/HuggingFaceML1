"""The briefing design (2026-10-16): the loss or gain frame comes from the agent's own side, as a short desk briefing in
its instructions from the start of the run; UBS's requests are its real 2011 words, the same in every version.

The final round's code is untouched: the briefing is inserted into the text mountain.opening() returns, and the chats
are the real ones ("real") or none ("no ask"). With mode "takeover 0 days" no Deutsche Bank line is put in the agent's
mouth, so every word it writes is its own.
"""
import hashlib, json, os

from mountain import opening

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIEFINGS = os.path.join(ROOT, "data", "silver", "desk_briefings.json")
VERSIONS = ["neutral", "loss", "gain", "loss + you", "gain + you", "no ask"]
MODE = "takeover 0 days"
# The paragraph of the opening the briefing follows (the description of the agent and its job)
_AFTER = "Your own messages in the chats appear under your name, Deutsche Bank [Agent B].\n"


def load_briefings(path=BRIEFINGS):
    b = json.load(open(path))
    assert list(b["versions"]) == VERSIONS, "desk_briefings.json must hold exactly the six versions, in order"
    return b


def briefing_opening(version, b=None):
    """The instructions for one version: the final round's opening with the desk briefing after the job paragraph."""
    b = b or load_briefings()
    base = opening()
    assert base.count(_AFTER) == 1, "the opening changed: update _AFTER"
    return base.replace(_AFTER, _AFTER + b["prefix"] + b["versions"][version] + "\n")


def chats_version(version):
    """Which chats a version gets: UBS's real words for every version with a request, none for no ask."""
    return "no ask" if version == "no ask" else "real"


def briefing_fingerprint(path=BRIEFINGS):
    """Part of the setup ID, so days run with different wording are never pooled."""
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]


def opening_with(text, b=None):
    """The instructions with any briefing text (used for the matched variations in notebook 15)."""
    b = b or load_briefings()
    base = opening()
    assert base.count(_AFTER) == 1, "the opening changed: update _AFTER"
    return base.replace(_AFTER, _AFTER + b["prefix"] + text + "\n")


def variants(version, b=None, amounts=(3, 4, 5), periods=("last month", "last quarter")):
    """Matched variations of a version's briefing: the same sentence with the amount and the period changed, so a
    difference found between versions comes from loss vs gain (or the responsibility sentence), not one wording.
    The approved wording ($4 million, last month) is always one of them."""
    b = b or load_briefings()
    text = b["versions"][version]
    out = []
    for period in periods:
        if "$4 million" in text:
            for x in amounts:
                out.append((f"${x}M, {period}", text.replace("$4 million", f"${x} million").replace("last month", period)))
        else:
            out.append((period, text.replace("last month", period)))
    return out


def build_turns(opening_text, diary, log, observation, corrections=(), recent=4):
    """The conversation the agent is given at a step, exactly as notebook 14's agent builds it: the instructions, the
    desk diary and one line per older step today, the last `recent` steps in full, the new update, and any send-backs."""
    from mountain import one_line
    turns = [{"role": "system", "content": opening_text}]
    older, rec = (log[:-recent] if len(log) > recent else []), log[-recent:]
    memory = (["Desk diary (your earlier days):\n" + "\n".join(diary)] if diary else []) + \
             (["Earlier today:\n" + "\n".join(one_line(r) for r in older)] if older else [])
    if memory:
        turns += [{"role": "user", "content": "\n\n".join(memory)}, {"role": "assistant", "content": "Noted."}]
    for r in rec:
        turns += [{"role": "user", "content": r["observation"]}, {"role": "assistant", "content": r["reply"] or "(no reply)"}]
    turns.append({"role": "user", "content": observation})
    for bad, note in corrections:
        turns += [{"role": "assistant", "content": bad or "(no reply)"}, {"role": "user", "content": note}]
    return turns


def turns_at(opening_text, version, date, when, framed, setups, reply="Watching the market for now.\nHOLD"):
    """The conversation at time `when` on `date` (the first day of a run, no diary), after the agent has held at every
    earlier step: the same history for every version, so only the briefing (and the chat, for no ask) differs."""
    from mountain import make_day
    day = make_day(date, chats_version(version), framed, setups, mode=MODE)
    got = {}

    def agent(obs, d):
        if d.now() == when:
            got["turns"] = build_turns(opening_text, [], d.log, obs, d.corrections)
        return reply
    while not day.done and "turns" not in got:
        day.step(agent)
    assert "turns" in got, f"{when} is not a step of {date}"
    return got["turns"]
