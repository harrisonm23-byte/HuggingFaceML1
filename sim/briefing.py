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
UBS_FRAMES = os.path.join(ROOT, "data", "silver", "ubs_frames.json")
BRIEFING_VERSIONS = ["neutral", "loss", "gain", "loss + you", "gain + you", "no ask"]
# The "both" versions (the user, 2026-10-16): the same management briefing, and UBS's request also carries the matching
# frame, one line from data/silver/ubs_frames.json right after its last real line
BOTH = ["both loss", "both gain", "both loss + you", "both gain + you"]
VERSIONS = BRIEFING_VERSIONS + BOTH
MODE = "takeover 0 days"
# The paragraph of the opening the briefing follows (the description of the agent and its job)
_AFTER = "Your own messages in the chats appear under your name, Deutsche Bank [Agent B].\n"
# Bare replies to a Deutsche Bank line the agent never sees, dropped along with the line they answer (the user,
# 2026-10-16: an answer to no question reads as nonsense). On 12 Jan UBS's "yup" answered "we still good with the
# silver stop?". Nothing else of UBS's is changed, and nothing is added.
BARE_REPLIES = {("p316_bust_through_it", "yup")}


def load_briefings(path=BRIEFINGS):
    b = json.load(open(path))
    assert list(b["versions"]) == BRIEFING_VERSIONS, "desk_briefings.json must hold exactly the six versions, in order"
    return b


def base_version(version):
    """The management briefing a version gets: a "both" version gets the briefing of the same name."""
    return version[len("both "):] if version.startswith("both ") else version


def load_frames(path=UBS_FRAMES):
    f = json.load(open(path))
    assert all(set(c) >= {"loss", "gain", "loss + you", "gain + you"} for c in f["chats"].values()), "ubs_frames.json: a frame is missing"
    return f


def briefing_opening(version, b=None):
    """The instructions for one version: the final round's opening with the desk briefing after the job paragraph."""
    b = b or load_briefings()
    base = opening()
    assert base.count(_AFTER) == 1, "the opening changed: update _AFTER"
    return base.replace(_AFTER, _AFTER + b["prefix"] + b["versions"][base_version(version)] + "\n")


def briefing_day(date, version, framed, setups, frames=None):
    """One day of the briefing design: the final round's day in mode "takeover 0 days" (no Deutsche Bank line in the
    agent's mouth), with UBS's real lines for a version with a request and none for no ask, and the bare replies to
    the removed Deutsche Bank lines dropped. In a "both" version UBS also sends the matching frame as its own line
    right after its last real line. The chats are read from cfg.events at each step, so this is the day the agent gets."""
    from mountain import make_day
    day = make_day(date, chats_version(version), framed, setups, mode=MODE)
    for e in day.cfg.events:
        e["lines"] = [(sp, t) for sp, t in e["lines"] if (e["id"], t) not in BARE_REPLIES]
    if version.startswith("both "):
        frames = frames or load_frames()
        for e in day.cfg.events:
            ubs = [sp for sp, t in e["lines"] if sp.startswith("UBS")]
            if e["id"] in frames["chats"] and ubs:
                e["lines"] = e["lines"] + [(ubs[-1], frames["chats"][e["id"]][base_version(version)])]
    return day


def chats_version(version):
    """Which chats a version gets: UBS's real words for every version with a request, none for no ask."""
    return "no ask" if version == "no ask" else "real"


def briefing_fingerprint(path=BRIEFINGS, frames=UBS_FRAMES):
    """The wording of the briefings and of UBS's frames, so days run with different wording are never pooled."""
    return hashlib.md5(open(path, "rb").read() + open(frames, "rb").read()).hexdigest()[:8]


def opening_with(text, b=None):
    """The instructions with any briefing text (used for the matched variations in notebook 15)."""
    b = b or load_briefings()
    base = opening()
    assert base.count(_AFTER) == 1, "the opening changed: update _AFTER"
    return base.replace(_AFTER, _AFTER + b["prefix"] + text + "\n")


def variants(version, b=None, amounts=(3, 4, 5), periods=("last month", "last quarter")):
    """Matched variations of a version's briefing: the same sentence with the amount and the period changed. They show
    only that a difference is not tied to one dollar figure or period: loss and gain still differ in the same few words
    in every variation, so the tests of meaning use other wordings (sim/briefing_inside.py). The approved wording
    ($4 million, last month) is always one of them."""
    b = b or load_briefings()
    text = b["versions"][base_version(version)]
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
    day = briefing_day(date, version, framed, setups)
    got = {}

    def agent(obs, d):
        if d.now() == when:
            got["turns"] = build_turns(opening_text, [], d.log, obs, d.corrections)
        return reply
    while not day.done and "turns" not in got:
        day.step(agent)
    assert "turns" in got, f"{when} is not a step of {date}"
    return got["turns"]
