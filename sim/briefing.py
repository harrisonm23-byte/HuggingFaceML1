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
