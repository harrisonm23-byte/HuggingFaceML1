"""Attention onto "you" (the user, 30 Oct; the question notebook 04 was written for and never ran): at a saved decision
moment, how much of the agent's attention falls on UBS's framed words, and on the word "you" in them.

Same moment, different frame (sim/matched.py): the history, positions and P&L fixed, UBS's request in each of the five
framings. In each version the model reads the request's update once (the history from the cache, as the matched run
did) and every attention layer's weights are tapped (eager attention) for two kinds of query token:

- the decision token, the last token before the agent's reply: its attention mass on each disjoint group of keys:
  the history before the update; the rest of the update (prices, positions, Reply as usual...); UBS's neutral core
  (the line every framing shares) apart from any "you" in it; "you" in the core (it is there in every framing: "Can
  you help me..."); the framed extra apart from "you"; "you" in the extra (blame and credit only: the manipulation);
  and the template's tail after the update's text. The groups cover every key, so the masses sum to 1 per head.
- each "you" of the extra, as a query ("into you", notebook 04): its mass on the history, the rest of the update, the
  core, the extra before it (the loss or gain statement it closes), and itself with what follows it.

Masses are kept per layer and head. A local layer (sliding window) cannot see keys beyond its window; its mass on the
history is what it actually gives them. Nothing is sampled and nothing is steered.
"""
import copy
import difflib
import re

import numpy as np

YOU = re.compile(r"\b[Yy]ou(?:r|rs|'re|'ve|'ll|'d)?\b")
UBS_LINE = re.compile(r"^(  UBS \[Agent [AB]\]: )(.*)$", re.M)      # the chat-only days also have UBS's Agent B
WORD = re.compile(r"\w+(?:'\w+)?|[^\w\s]")
DECISION_GROUPS = ["history", "update_rest", "core_other", "you_core", "extra_other", "you_extra", "tail"]
INTO_YOU_GROUPS = ["history", "update_rest", "core", "extra_before_you", "you_and_after"]


def core_mask(core, line):
    """For each character of the framed line, whether it belongs to UBS's neutral line (the core): the words the two
    share in order (difflib on words and punctuation, runs of at least two, or one word at the very start), so a framing
    that rewrites the line ("Hallelujah." -> "We're not saved yet.") or drops its end ("-- it shouldn't hurt.") is
    split correctly. Where the core opens the line unchanged this is exactly that opening."""
    if line.startswith(core):
        return [True] * len(core) + [False] * (len(line) - len(core))
    cw, lw = [m for m in WORD.finditer(core)], [m for m in WORD.finditer(line)]
    sm = difflib.SequenceMatcher(None, [m.group(0) for m in cw], [m.group(0) for m in lw], autojunk=False)
    mask = [False] * len(line)
    for blk in sm.get_matching_blocks():
        if blk.size >= 2 or (blk.size == 1 and blk.b == 0):
            for m in lw[blk.b:blk.b + blk.size]:
                for i in range(m.start(), m.end()):
                    mask[i] = True
    return mask


def runs(mask, offset):
    """Character spans [a, b) where mask is True, shifted by offset."""
    out, start = [], None
    for i, x in enumerate(list(mask) + [False]):
        if x and start is None:
            start = i
        elif not x and start is not None:
            out.append((offset + start, offset + i))
            start = None
    return out


def line_spans(update, date, framing, chats):
    """Character spans in the update's text: for each UBS line, its neutral core and its framed extra (lists of spans),
    and every "you" in each. chats: framing_set.read_set()."""
    table = {}
    for c in chats:
        if c["date"] == date:
            for l in c["lines"]:
                table.setdefault(l["text"][framing], set()).add(l["text"]["neutral"])
    out = []
    for m in UBS_LINE.finditer(update):
        line, start = m.group(2), m.start(2)
        cores = table.get(line)
        assert cores is not None, "a UBS line in the update is not in the file for its framing"
        assert len(cores) == 1, "a UBS line matches file lines with different cores"
        core = next(iter(cores))
        mask = core_mask(core, line)
        core_spans = runs(mask, start)
        extra_spans = runs([not x and not line[i].isspace() for i, x in enumerate(mask)], start)
        you_core, you_extra = [], []
        for y in YOU.finditer(line):
            (you_core if mask[y.start()] else you_extra).append((start + y.start(), start + y.end()))
        out.append({"core": core_spans, "extra": extra_spans, "core_is_prefix": line.startswith(core),
                    "core_words_found": sum(all(mask[w.start():w.end()]) for w in WORD.finditer(line))
                    / max(1, len(WORD.findall(core))), "you_core": you_core, "you_extra": you_extra})
    return out


def token_groups(tok, turns, update_index, date, framing, chats):
    """The decision prompt's token ids and, for each group, the sorted key positions in it. Offsets come from tokenizing
    the chat-templated text; the ids must equal the template's own (asserted)."""
    text = tok.apply_chat_template(turns, add_generation_prompt=True, tokenize=False)
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    ids, offs = list(enc["input_ids"]), list(enc["offset_mapping"])
    from inside_careers import encode
    assert ids == list(encode(tok, turns)), "the templated text does not tokenize to the template's ids"
    update = turns[-1]["content"]                           # turns_at: the opening, the history, then the update
    assert turns[-1]["role"] == "user" and update == turns[update_index + 1]["content"], "the last turn is not the update"
    u0 = text.rfind(update)
    assert u0 >= 0, "the update's text is not in the templated prompt"
    u1 = u0 + len(update)

    def toks(a, b):
        return [i for i, (s, e) in enumerate(offs) if e > a and s < b and e > s]

    def toks_many(spans):
        return sorted({i for a, b in spans for i in toks(a, b)})
    spans = line_spans(update, date, framing, chats)
    shift = lambda sp: (u0 + sp[0], u0 + sp[1])
    you_core = toks_many([shift(y) for s in spans for y in s["you_core"]])
    you_extra = toks_many([shift(y) for s in spans for y in s["you_extra"]])
    core = toks_many([shift(sp) for s in spans for sp in s["core"]])
    extra = [i for i in toks_many([shift(sp) for s in spans for sp in s["extra"]]) if i not in set(core)]
    upd = set(toks(u0, u1))
    first_upd = min(upd)
    yous, ubs = set(you_core) | set(you_extra), set(core) | set(extra)
    groups = {"history": list(range(first_upd)), "you_core": you_core, "you_extra": you_extra,
              "core_other": [i for i in core if i not in yous],
              "extra_other": [i for i in extra if i not in yous and i not in core],
              "update_rest": [i for i in sorted(upd) if i not in ubs],
              "tail": [i for i in range(first_upd, len(ids)) if i not in upd and i not in ubs]}
    seen = sorted(i for g in groups.values() for i in g)
    assert seen == list(range(len(ids))), "the groups do not partition the prompt's tokens"
    # The extra before each "you" (the loss or gain statement), per "you" token
    before = {y: [i for i in extra if i < y] for y in you_extra}        # the loss or gain statement, any earlier "you" included
    return ids, groups, before


def framed(career, idx, date, v0, v1, chats):
    """A copy of the career whose update at `idx` carries UBS's lines (Agent A's and Agent B's) in framing v1."""
    from matched import swap_update
    h = list(career["history"])
    h[idx] = {**h[idx], "content": swap_update(h[idx]["content"], date, v0, v1, chats, pattern=UBS_LINE)}
    return {**career, "history": h}


MONTHS = {m: i for i, m in enumerate("January February March April May June July August September October November "
                                     "December".split(), 1)}


def chat_moments(folder):
    """Every chat-only-day update with a UBS line in every career of a results folder (B: 17 a career), in the same
    form as inside_careers.moments(): career_file, version, run, date (ISO, the chat's), history_index, chat (an id for
    the file name). The day's date is the update's "Wednesday 28 November 2007" line (some updates open with how the
    last trading day closed)."""
    import glob, json, os
    out = []
    for path in sorted(glob.glob(os.path.join(folder, "careers", "*.json"))):
        c = json.load(open(path))
        for i, t in enumerate(c["history"]):
            if t["role"] != "user" or "no market session today" not in t["content"] or not UBS_LINE.search(t["content"]):
                continue
            d = re.search(r"\b(\d{2}) (" + "|".join(MONTHS) + r") (\d{4})\. You have no market session today", t["content"])
            assert d, f"{path} turn {i}: no date"
            date = f"{d[3]}-{MONTHS[d[2]]:02d}-{d[1]}"
            out.append({"experiment": "B", "version": c["version"], "run": c["run"], "date": date, "history_index": i,
                        "chat": f"chatday_{date}_t{i}", "wants": None, "joined": None,
                        "career_file": os.path.basename(path)})
    return out


class Tap:
    """Keeps selected query rows of every attention layer's weights (eager attention) while switched on."""

    def __init__(self, model):
        import torch
        self.torch = torch
        # The language model's decoder layers (as inside_careers.Recorder picks them), each one's attention: the vision
        # tower's attention, if the checkpoint has one, is left alone
        layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
        self.attn = [layer.self_attn for layer in layers]
        assert self.attn, "no decoder layers found"
        self.handles = [a.register_forward_hook(self._hook(k)) for k, a in enumerate(self.attn)]
        self.off()

    def off(self):
        self.rows, self.offset, self.got = None, 0, {}

    def arm(self, rows, offset):
        """Keep these absolute query positions; the forward pass's first query token sits at `offset`."""
        self.rows, self.offset, self.got = list(rows), offset, {}

    def _hook(self, k):
        def hook(module, inputs, output):
            if self.rows is None:
                return
            w = output[1]
            assert w is not None, "no attention weights: load the model with attn_implementation='eager'"
            q_len, kv_len = w.shape[2], w.shape[3]
            local = [r - self.offset for r in self.rows]
            assert all(0 <= r < q_len for r in local), "a query row is outside this forward pass"
            # A sliding-window layer's cache keeps only its last keys, so its key axis starts later than position 0:
            # column j is absolute position j + shift. Keys before the shift are outside the window (weight 0).
            shift = self.offset + q_len - kv_len
            self.got[k] = (w[0][:, local, :].float().cpu(), shift)      # heads x rows x keys
        return hook

    def masses(self, groups_per_row):
        """[layers x heads x rows x groups]: for each kept row, the summed weight on each key group (a list of absolute
        key positions). groups_per_row: for each row, a list of key-position lists (one per group)."""
        L = len(self.attn)
        H, R = self.got[0][0].shape[0], self.got[0][0].shape[1]
        out = np.zeros((L, H, R, max(len(g) for g in groups_per_row)), dtype=np.float32)
        for k in range(L):
            w, shift = self.got[k]
            for r, groups in enumerate(groups_per_row):
                for g, keys in enumerate(groups):
                    cols = [p - shift for p in keys if p >= shift]
                    out[k, :, r, g] = w[:, r, cols].sum(-1).numpy() if cols else 0.0
        return out

    def remove(self):
        for h in self.handles:
            h.remove()


def run_moment(model, tok, tap, career, m, chats, opening, framings, prefill):
    """One saved moment in every framing: decision-token masses [framings x layers x heads x groups], "into you" masses
    averaged over the extra's "you" tokens [framings x layers x heads x groups] (NaN where the framing has none), and a
    row of counts per framing. prefill: interventions.prefill (the history read once into a cache)."""
    import torch
    from inside_careers import turns_at
    from interventions import split_point
    idx = m["history_index"]
    full0, k = split_point(tok, career, idx, opening)
    tap.off()
    cache = prefill(model, full0[:k])
    dec, into, rows = [], [], []
    for v1 in framings:
        c = framed(career, idx, m["date"], m["version"], v1, chats)
        turns = turns_at(c, idx, opening)
        ids, groups, before = token_groups(tok, turns, idx, m["date"], v1, chats)
        assert ids[:k] == full0[:k], "the history before the request changed"
        last = len(ids) - 1
        yous = groups["you_extra"]
        tap.arm([last] + yous, k)
        with torch.no_grad():
            model(input_ids=torch.tensor([ids[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                  use_cache=True, cache_position=torch.arange(k, len(ids), device=model.device))
        per_row = [[groups[g] for g in DECISION_GROUPS]]
        for y in yous:
            core = sorted(set(groups["core_other"]) | set(groups["you_core"]))
            after = [i for i in range(y, len(ids))]           # itself and what follows (causal: only itself counts)
            per_row.append([groups["history"], groups["update_rest"], core, before[y], after])
        mass = tap.masses(per_row)                            # layers x heads x rows x groups
        tap.off()
        dec.append(mass[:, :, 0, :len(DECISION_GROUPS)])
        into.append(mass[:, :, 1:, :len(INTO_YOU_GROUPS)].mean(2) if yous else
                    np.full(mass.shape[:2] + (len(INTO_YOU_GROUPS),), np.nan, dtype=np.float32))
        rows.append({"framing": v1, "tokens": len(ids), "update_start": k,
                     **{f"n_{g}": len(groups[g]) for g in DECISION_GROUPS}})
    return np.stack(dec), np.stack(into), rows

