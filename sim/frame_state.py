"""Careers with the frame's state carried in (the user, 29 Oct; notebook 35): B's neutral career, the agent reading
UBS's neutral words throughout, with the state UBS's framed words would have produced added inside the model.

At each update with a UBS line (29 per career), the update is read twice from the same point of the career: as it is
(neutral) and with UBS's lines in the framing (FROM). The difference of the two readings' averages over the update's
tokens, at one layer, is added to every token of the neutral update and of the reply written under it: the
whole-message transplant of the third steering run (sim/steer3.py), which at single moments moved going along about a
third as much as the framed words did, at layers 18 and 24. Kept: at every later read the update and its reply keep
that moment's state, as a framed career keeps the framed words in its conversation (each reply re-reads the
conversation from its text, so otherwise the state would live on only in what the agent wrote). The control: the same
moments and sizes with one random direction for the whole career.
"""
import hashlib
import re

import numpy as np

UBS = re.compile(r"^(\s*UBS \[Agent [AB]\]: )(.*)$", re.M)
NOTE = "Your reply was not accepted"
KINDS = ("frame", "random")
RANDOM_SEED = 20261029


def framed_lines(chats, framing):
    """{UBS's neutral line: the same line in `framing`} over the frozen file (each neutral line has one)."""
    out = {}
    for c in chats:
        for l in c["lines"]:
            n, f = l["text"]["neutral"], l["text"][framing]
            assert out.get(n, f) == f, f"the neutral line {n!r} has two {framing} versions"
            out[n] = f
    return out


def framed_update(text, table):
    """(the update with every UBS line in the framing, how many lines changed). Every UBS line must be in the table."""
    seen = []

    def swap(m):
        assert m.group(2) in table, f"a UBS line not in the framing file: {m.group(2)!r}"
        seen.append(m.group(2))
        return m.group(1) + table[m.group(2)]
    return UBS.sub(swap, text), len(seen)


def update_index(turns):
    """The newest update: the last user turn that is not a request to correct a reply."""
    return max(i for i, t in enumerate(turns) if t["role"] == "user" and not t["content"].startswith(NOTE))


def turn_start(tok, turns, u):
    """The token where turn u starts: where the conversation up to it stops matching the whole one."""
    full = tok.apply_chat_template(turns, add_generation_prompt=True, return_dict=True)["input_ids"]
    try:                                   # (the instructions alone may not render on their own: then from 0)
        before = tok.apply_chat_template(turns[:u], return_dict=True)["input_ids"] if u > 1 else []
    except Exception:
        before = []
    n = 0
    for a, b in zip(full, before):
        if a != b:
            break
        n += 1
    return n


def random_unit(width, seed):
    r = np.random.default_rng(seed).normal(size=width)
    return (r / np.linalg.norm(r)).astype(np.float32)


class Segments:
    """Adds each segment's vector to a decoder layer's output at the positions from its start up to its end (None: to
    the end of the pass), positions as the model counts them (chunked reading and token-by-token writing both
    covered); nothing with no segments."""

    def __init__(self, layer_module):
        self.segs, self.steered = [], 0
        self.handle = layer_module.register_forward_hook(self._hook, with_kwargs=True)

    def set(self, segs=()):
        self.segs, self.steered = list(segs), 0

    def _hook(self, module, args, kwargs, output):
        if not self.segs:
            return output
        h = output[0] if isinstance(output, tuple) else output
        pos = kwargs.get("position_ids")
        assert pos is not None, "the decoder layer was called without position_ids"
        p = pos[0]
        for start, end, vec in self.segs:
            keep = p >= start
            if end is not None:
                keep = keep & (p < end)
            n = int(keep.sum())
            if n:
                self.steered += n
                h = h + keep.to(h.dtype)[None, :, None] * vec.to(h.device, h.dtype)
        return (h,) + tuple(output[1:]) if isinstance(output, tuple) else h


class SumCapture:
    """While on, sums a layer's output over the positions of every pass, and counts them."""

    def __init__(self, layer_module):
        self.on, self.sum, self.n = False, None, 0
        self.handle = layer_module.register_forward_hook(self._hook)

    def reset(self):
        self.sum, self.n = None, 0

    def _hook(self, module, inputs, output):
        if self.on:
            h = (output[0] if isinstance(output, tuple) else output)[0].float()
            s = h.sum(0)
            self.sum = s if self.sum is None else self.sum + s
            self.n += h.shape[0]

    def mean(self):
        return (self.sum / self.n).cpu().numpy()


def _read(model, ids, start, cache, chunk, capture=None):
    """Read ids[start:] into the cache (in chunks), the capture on if given."""
    import torch
    x = torch.tensor([ids], device=model.device)
    if capture is not None:
        capture.reset()
        capture.on = True
    try:
        with torch.no_grad():
            for s in range(start, len(ids), chunk):
                e = min(s + chunk, len(ids))
                model(input_ids=x[:, s:e], past_key_values=cache, use_cache=True, logits_to_keep=1,
                      cache_position=torch.arange(s, e, device=model.device))
    finally:
        if capture is not None:
            capture.on = False
    return capture.mean() if capture is not None else None


def frame_shift(model, tok, turns, framed_turns, start, capture, chunk=4096):
    """The framed update's average state minus the neutral update's, at the capture's layer, both read after the same
    history (turns end with the update; read with the reply's opening, as the third steering run did)."""
    import copy
    from transformers import DynamicCache
    a = tok.apply_chat_template(turns, add_generation_prompt=True, return_dict=True)["input_ids"]
    b = tok.apply_chat_template(framed_turns, add_generation_prompt=True, return_dict=True)["input_ids"]
    assert a[:start] == b[:start] and a != b, "the framed update must differ from the neutral one after the same history"
    cache = DynamicCache(config=model.config)
    _read(model, a[:start], 0, cache, chunk)
    framed = _read(model, b, start, copy.deepcopy(cache), chunk, capture)
    neutral = _read(model, a, start, cache, chunk, capture)
    return (framed - neutral).astype(np.float32)


class FrameState:
    """One career's moments: [{"start", "end" (None while open), "key", "size", "lines"}] and their vectors."""

    def __init__(self, kind, table, seed=RANDOM_SEED):
        assert kind in KINDS, kind
        self.kind, self.table, self.seed = kind, table, seed
        self.moments, self.vecs, self.unit = [], [], None

    def begin(self, model, tok, turns, capture, chunk=4096):
        """Before a reply: close the earlier update's moment where this update starts, add this update's moment if it
        has a UBS line, and return every segment to add while this reply is read and written."""
        u = update_index(turns)
        start, key = turn_start(tok, turns, u), hashlib.sha256(turns[u]["content"].encode()).hexdigest()[:16]
        last = self.moments[-1] if self.moments else None
        if last is not None and last["end"] is None and last["key"] != key:
            assert start >= last["start"], "an update starts before the open moment"
            last["end"] = start
        if last is None or last["key"] != key:
            framed, n = framed_update(turns[u]["content"], self.table)
            if n:
                ft = [dict(t) for t in turns[:u + 1]]
                ft[u]["content"] = framed
                vec = frame_shift(model, tok, turns[:u + 1], ft, start, capture, chunk)
                size = float(np.linalg.norm(vec))
                if self.kind == "random":
                    if self.unit is None:
                        self.unit = random_unit(len(vec), self.seed)
                    vec = self.unit * size
                self.moments.append({"start": start, "end": None, "key": key, "size": size, "lines": n})
                self.vecs.append(vec)
        return [(m["start"], m["end"], v) for m, v in zip(self.moments, self.vecs)]

    def saved(self):
        return {"kind": self.kind, "seed": self.seed, "moments": [dict(m) for m in self.moments]}

    def vectors(self):
        return np.stack(self.vecs) if self.vecs else np.zeros((0, 0), np.float32)

    def restore(self, saved, vecs):
        assert saved["kind"] == self.kind and saved["seed"] == self.seed, "saved with another arm"
        self.moments = [dict(m) for m in saved["moments"]]
        self.vecs = [np.asarray(v, np.float32) for v in vecs]
        assert len(self.vecs) == len(self.moments)
        if self.kind == "random" and self.vecs:
            self.unit = random_unit(self.vecs[0].shape[0], self.seed)
