"""The state after reading an emotion document, injected without the document (the user, 22 Oct).

At each of B's 60 neutral-career requests (UBS's request neutral), the agent reads one of the author's documents just
before the request (sim/prime.py), and the state each layer then produces over the request's update is recorded. The
document is then left out, and that state is put back by hand into the agent's reading of the update, at one layer:
- "mean": the average change the document made over the update's tokens, added to every token from the start of the
  update (as in the screenplay injection);
- "aligned": the change the document made at each token of the update, added token by token (the after-reading state at
  that layer, restored exactly), and the average change on the tokens after it (the reasoning line and the order);
- controls: random vectors of the same size, as one vector (for "mean") and token by token (for "aligned").
Yardstick: the document itself, as read. Outcome: P(the order goes along) after the fixed neutral reasoning line.
"""
import copy
import numpy as np

THEMES = ["neutral", "loss", "blame", "gain", "credit"]
LAYERS, RANDOM_LAYER = [12, 18, 24], 18


class Capture:
    """While on, keeps each watched layer's output at every position of the pass."""

    def __init__(self, layer_modules):
        self.on, self.got = False, {}
        self.handles = [m.register_forward_hook(self._hook(L)) for L, m in layer_modules.items()]

    def _hook(self, L):
        def hook(module, inputs, output):
            if self.on:
                self.got[L] = (output[0] if isinstance(output, tuple) else output)[0].float()
        return hook


class SeqSteer:
    """Adds `seq` (tokens x width) to the first pass's first tokens and `vec` to every other token; nothing when off."""

    def __init__(self, layer_module):
        self.vec, self.seq, self.first = None, None, False
        self.handle = layer_module.register_forward_hook(self._hook)

    def set(self, vec=None, seq=None):
        self.vec, self.seq, self.first = vec, seq, seq is not None

    def _hook(self, module, inputs, output):
        if self.vec is None and self.seq is None:
            return output
        h = output[0] if isinstance(output, tuple) else output
        add = (self.vec if self.vec is not None else 0) + h[0].new_zeros(h.shape[1], h.shape[2])
        if self.first and self.seq is not None:
            t = min(len(self.seq), h.shape[1])
            add[:t] = self.seq[:t].to(h.dtype)
            self.first = False
        h = h + add.to(h.dtype)[None]
        return (h,) + tuple(output[1:]) if isinstance(output, tuple) else h


def conditions():
    """[(name, theme, kind, layer)]."""
    c = [("none", None, "none", None)]
    for t in THEMES:
        c.append((f"{t}: as read", t, "read", None))
        c += [(f"{t}: mean at layer {L}", t, "mean", L) for L in LAYERS]
        c += [(f"{t}: aligned at layer {L}", t, "aligned", L) for L in LAYERS]
        c += [(f"{t}: random mean at layer {RANDOM_LAYER}", t, "random_mean", RANDOM_LAYER),
              (f"{t}: random aligned at layer {RANDOM_LAYER}", t, "random_aligned", RANDOM_LAYER)]
    return c


def run_item(model, tok, steers, capture, career, item, docs, chats, opening, lead, grid, done=()):
    """Every condition at one request. One row per condition."""
    import torch
    from inside_careers import encode, turns_at
    from interventions import order_dist, prefill, split_point, summarise_orders
    from matched import matched
    from prime import primed
    idx = item["history_index"]
    base = matched(career, idx, item["date"], "neutral", "neutral", chats)
    plain = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    cache = None
    shifts = {}                                           # theme -> {layer: (mean vector, aligned tokens x width)}
    rng = np.random.default_rng(20261022 + idx)

    def read(seq):
        capture.on, capture.got = True, {}
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([seq[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(seq), device=model.device))
        finally:
            capture.on = False
        return dict(capture.got)

    for name, t, kind, L in conditions():
        key = f"{item['career_file']}|{idx}|{name}"
        if key in done:
            continue
        if cache is None:
            cache = prefill(model, plain[:k])
            for s in steers.values():
                s.set()
        full = plain
        if t is not None:
            doc = docs[t][item["doc"] % len(docs[t])]
            with_doc = encode(tok, turns_at(primed(base, idx, doc), idx, opening))
            assert with_doc[:k] == plain[:k], "the history before the update changed"
            if kind == "read":
                full = with_doc
            elif t not in shifts:
                extra = len(with_doc) - len(plain)
                start = next(i for i in range(k, len(plain)) if with_doc[i] != plain[i])
                assert with_doc[start + extra:] == plain[start:], "the update after the document does not line up"
                a, b = read(with_doc), read(plain)
                shifts[t] = {}
                for LL in LAYERS:
                    al = torch.zeros_like(b[LL])                   # positions k .. end of the plain read
                    al[start - k:] = a[LL][start - k + extra:] - b[LL][start - k:]
                    shifts[t][LL] = (al[start - k:].mean(0), al)
        vec = seq = None
        if kind == "mean":
            vec = shifts[t][L][0]
        elif kind == "aligned":
            vec, seq = shifts[t][L]
        elif kind == "random_mean":
            m = shifts[t][L][0]
            r = torch.tensor(rng.normal(size=m.shape[0]), dtype=m.dtype, device=m.device)
            vec = r / r.norm() * m.norm()
        elif kind == "random_aligned":
            m, al = shifts[t][L]
            r = torch.tensor(rng.normal(size=al.shape), dtype=al.dtype, device=al.device)
            seq = r / r.norm(dim=1, keepdim=True) * al.norm(dim=1, keepdim=True)
            r2 = torch.tensor(rng.normal(size=m.shape[0]), dtype=m.dtype, device=m.device)
            vec = r2 / r2.norm() * m.norm()
        try:
            if vec is not None or seq is not None:
                steers[L].set(vec=vec, seq=seq)
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
        finally:
            for s in steers.values():
                s.set()
        yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": idx,
               "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
               "doc": item["doc"], "condition": name, "theme": t, "kind": kind, "layer": L,
               "shift_size": float(vec.norm()) if vec is not None else 0.0, "coverage": cover, "orders": orders,
               "probs": probs, **summarise_orders(orders, probs, item["position"], item["wants"])}
