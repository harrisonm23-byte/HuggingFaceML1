"""The ideal history (designs/rd2/DESIGN_IDEAL_HISTORY.md; the user, 21 Oct): every setting at maximum, and the agent's own
record turned from refusing to going along.

Base (the user's choice, 21 Oct): Experiment D's careers, which carry management's memo and five morning books and UBS's
framed lines (B's file), all in one framing. In the ideal history, the agent's own reply at every
earlier push request where it did not go along is replaced by a real Gemma reply that went along at that same request,
in a career of the same framing (E first, then F, D, B; replies in which the agent itself speaks of fault,
responsibility or credit preferred). Nothing is written here: the replies are Gemma's own, from other careers.

At each later request (12 January on), the ideal history and the real one (its own replies kept) are read up to the
request, and UBS's request comes in each of its five framings. The positions and P&L in later updates still follow the
original trades.
"""
import json, os, re

FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
DONOR_EXPERIMENTS = [("E", "memo_ubs_bank_c_v2"), ("F", "peer_same_frame_v2"), ("D", "memo_and_ubs_framing_v2"),
                     ("B", "ubs_framing_v2")]
BASES = {"D": "results/full_career_gemma-3-12b-it_4bit_memo_and_ubs_framing_v2"}   # management + UBS (B's lines)
FIRST_REQUEST = "p344_i_can_hunt_with_u"
OWN_WORDS = re.compile(r"\b(fault|responsib\w*|on me|my call|my decision|blame|credit|thank\w*|proud)\b", re.I)


def folder(name):
    return f"results/full_career_gemma-3-12b-it_4bit_{name}"


def donors(moments):
    """{(version, request): [replies that went along]}: E's first, then F, D, B; within each, replies with the agent's own
    words of fault, responsibility or credit first."""
    out = {}
    for exp, name in DONOR_EXPERIMENTS:
        by = {}
        for m in moments(folder(name), exp):
            if not m["joined"]:
                continue
            career = json.load(open(os.path.join(folder(name), "careers", m["career_file"])))
            reply = career["history"][m["history_index"] + 1]
            assert reply["role"] == "assistant"
            by.setdefault((m["version"], m["chat"]), []).append(reply["content"])
        for key, replies in by.items():
            out.setdefault(key, []).extend(sorted(replies, key=lambda r: not OWN_WORDS.search(r)))
    return out


def ideal(career, own_moments, upto, donor_replies, pick):
    """The career with the agent's reply at every earlier push request (history index below `upto`) where it did not go
    along replaced by a donor reply that went along. Returns (career, swapped, kept, missing)."""
    h = list(career["history"])
    swapped = kept = missing = 0
    for m in own_moments:
        if m["history_index"] >= upto:
            continue
        if m["joined"]:
            kept += 1
            continue
        pool = donor_replies.get((m["version"], m["chat"]), [])
        if not pool:
            missing += 1
            continue
        i = m["history_index"] + 1
        assert h[i]["role"] == "assistant"
        h[i] = {**h[i], "content": pool[pick % len(pool)]}
        swapped += 1
    return {**career, "history": h}, swapped, kept, missing


def work_items(moments, sign):
    """The base careers (framed) at every request after the first."""
    items = []
    for exp, base in BASES.items():
        ms = [m for m in moments(base, exp) if m["version"] != "neutral"]
        by = {}
        for m in ms:
            by.setdefault(m["career_file"], []).append(m)
        items += [{**m, "base": exp, "folder": base, "position": m["held_their_way"] * sign[m["wants"]],
                   "own": by[m["career_file"]]} for m in ms if m["chat"] != FIRST_REQUEST]
    return sorted(items, key=lambda m: (m["base"], m["career_file"], m["history_index"]))


def run_item(model, tok, career, item, donor_replies, chats, opening, lead, grid, done=()):
    """The real and the ideal history at one request, the request in each framing. One row per condition."""
    from interventions import order_dist, prefill, split_point, summarise_orders
    from inside_careers import encode, turns_at
    from matched import matched
    idx = item["history_index"]
    ideal_career, swapped, kept, missing = ideal(career, item["own"], idx, donor_replies, item["run"])
    for record, c0 in (("real", career), ("ideal", ideal_career)):
        cache, base, k = None, None, None
        for v in FRAMINGS:
            key = f"{item['base']}|{item['career_file']}|{idx}|{record}|{v}"
            if key in done:
                continue
            if cache is None:
                _, k = split_point(tok, c0, idx, opening)
            c = matched(c0, idx, item["date"], item["version"], v, chats)
            full = encode(tok, turns_at(c, idx, opening))
            if cache is None:
                base = full[:k]
                cache = prefill(model, base)
            assert full[:k] == base, "the history before the request changed"
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            yield {"key": key, "base": item["base"], "career_file": item["career_file"], "version": item["version"], "run": item["run"],
                   "history_index": idx, "date": item["date"], "chat": item["chat"], "wants": item["wants"],
                   "position": item["position"], "saved_joined": item["joined"], "record": record, "framing": v,
                   "swapped": swapped, "kept": kept, "missing": missing, "coverage": cover, "orders": orders,
                   "probs": probs, **summarise_orders(orders, probs, item["position"], item["wants"]), "tokens": len(full)}
