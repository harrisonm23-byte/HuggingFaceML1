"""Push and cue (the user, 28 Oct; designs/rd2/PLAN_PUSH_CUE.md): what carries B's framing from 7 to 12 January.

In B, UBS says nothing between its 7 January request and its 12 January request, and the framed lines before 7 January
(28 Nov 2007, 15 Oct 2010) left no detectable effect at 7 January. So at 12 January a framed career carries, in the
main, one framed request and the agent's own reaction to it. Here a saved framed career is reread at its 12 January
request with UBS's earlier words set back to the author's neutral wording and everything the agent wrote and did kept:
- "as saved": the career as it was;
- "7 Jan neutral": only UBS's 7 January request in the neutral wording;
- "UBS neutral": every UBS line before the moment in the neutral wording (2007, 2010 and 7 January).
Each with UBS's 12 January request as saved and in the neutral wording. A neutral career is read once (nothing
changes). The lines come from the frozen file (sim/framing_set.py); nothing here writes or changes one.
"""
import re

UBS_LINE = re.compile(r"^(  UBS \[Agent [AB]\]: )(.*)$", re.M)     # 2007's UBS trader is Agent B, the rest Agent A
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                          "September", "October", "November", "December"])}
PUSH_DATE, CUE_CHAT = "2011-01-07", "p316_bust_through_it"
PUSH_CHAT = "p344_i_can_hunt_with_u"
CONDITIONS = ["as saved", "7 Jan neutral", "UBS neutral"]
REQUESTS = ["as saved", "neutral"]


def turn_date(text):
    """The date of an update ("Time: 09:30 UTC (09:30 London), 2011-01-07.") or of a chat-only day ("Wednesday
    28 November 2007.")."""
    m = re.search(r"Time: \d\d:\d\d UTC \([^)]*\), (\d{4}-\d{2}-\d{2})\.", text)
    if m:
        return m.group(1)
    m = re.match(r"\w+day (\d{1,2}) (\w+) (\d{4})\.", text)
    return f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}" if m else None


def swap_ubs(text, date, v0, v1, chats):
    """The turn with every UBS line (framing v0) replaced by the same line in framing v1, and how many were swapped.
    chats: read_set()."""
    table = {}
    for c in chats:
        if c["date"] == date:
            for l in c["lines"]:
                table.setdefault(l["text"][v0], set()).add(l["text"][v1])

    def sub(m):
        alts = table.get(m.group(2))
        assert alts is not None, "a UBS line is not in the file for its framing on its date"
        assert len(alts) == 1, "a UBS line matches file lines with different framings"
        return m.group(1) + next(iter(alts))
    return UBS_LINE.subn(sub, text)


def reread_versions(career, idx, chats):
    """{(history version, request version): (career copy, [(turn, date, lines swapped)])} for the moment at history
    index idx (UBS's 12 January request). Only UBS's lines change; the agent's turns are never touched."""
    v0, h = career["version"], career["history"]
    out = {}
    for cond in CONDITIONS:
        new, changed = list(h), []
        if cond != "as saved":
            for i in range(idx):
                t = h[i]
                if t["role"] != "user" or not UBS_LINE.search(t["content"]):
                    continue
                d = turn_date(t["content"])
                assert d, "a turn with UBS lines has no date"
                if cond == "7 Jan neutral" and d != PUSH_DATE:
                    continue
                text, n = swap_ubs(t["content"], d, v0, "neutral", chats)
                if text != t["content"]:                     # a neutral career's lines are already neutral
                    new[i] = {**t, "content": text}
                    changed.append((i, d, n))
        for req in REQUESTS:
            hh = list(new)
            if req == "neutral":
                text, n = swap_ubs(hh[idx]["content"], turn_date(hh[idx]["content"]), v0, "neutral", chats)
                assert n >= 1, "no UBS line in the request's update"
                hh[idx] = {**hh[idx], "content": text}
            out[(cond, req)] = ({**career, "history": hh}, changed)
    return out


def cue_row(z12, z7, career_file):
    """One career's cue, from its two matched-reread files (scripts/modal_matched.py: states, layers, meta) at
    12 January and 7 January: P(the order goes along) with each framing of the 12 January request (no Bank C), and the
    change the blame line makes to the state (blame minus neutral line) at each kept layer, at 12 January against
    7 January."""
    import json
    import numpy as np
    r12, r7 = json.loads(str(z12["meta"])), json.loads(str(z7["meta"]))
    at = lambda r, v: next(i for i, x in enumerate(r) if x["framing"] == v and not x["bank_c"])
    d12 = z12["states"][at(r12, "loss + you")] - z12["states"][at(r12, "neutral")]
    d7 = z7["states"][at(r7, "loss + you")] - z7["states"][at(r7, "neutral")]
    return {"career_file": career_file, "history": r12[0]["history"], "run": r12[0]["run"],
            "p": {x["framing"]: x["p_order_along"] for x in r12 if not x["bank_c"]},
            "coverage": r12[at(r12, "neutral")]["coverage"], "layers": [int(l) for l in z12["layers"]],
            "cosine_12_vs_7": [float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))) for a, b in zip(d12, d7)],
            "size_12": [float(np.linalg.norm(a)) for a in d12], "size_7": [float(np.linalg.norm(b)) for b in d7]}


def score_moment(model, tok, career, m, chats, opening):
    """Rows for one saved career at its 12 January request: P(the order goes along) after the fixed neutral reasoning
    line, over HOLD and every size the agents used, in each history version x request version. m: the moment, from
    inside_careers.moments()."""
    from interventions import NEUTRAL_LEAD, SIGN, WIDE_GRID, order_dist, prefill, split_point, summarise_orders
    idx, position = m["history_index"], m["held_their_way"] * SIGN[m["wants"]]
    versions = reread_versions(career, idx, chats)
    framed = career["version"] != "neutral"
    rows = []
    for cond in (CONDITIONS if framed else ["as saved"]):
        cache = prefix = None
        for req in (REQUESTS if framed else ["neutral"]):     # a neutral career's request is already neutral
            c, changed = versions[(cond, req)]
            full, k = split_point(tok, c, idx, opening)
            if cache is None:                                # the history before the request: the same for both
                prefix, cache = full[:k], prefill(model, full[:k])
            assert full[:k] == prefix, "the history before the request differs between the request versions"
            orders, probs, cover = order_dist(model, tok, full, cache, NEUTRAL_LEAD, WIDE_GRID)
            rows.append({"history": career["version"], "run": career["run"], "career_file": m["career_file"],
                         "chat": m["chat"], "date": m["date"], "wants": m["wants"], "position": position,
                         "saved_joined": m["joined"], "condition": cond, "request": req,
                         "swapped": [[i, d, n] for i, d, n in changed],
                         **summarise_orders(orders, probs, position, m["wants"]), "coverage": cover, "probs": probs,
                         "tokens": len(full)})
    return rows
