"""The frame's state at every layer: the read-out that picks the layer and the construction before careers are spent
(the user, 29 Oct: "we have to do that probability test again"). Run by scripts/modal_transplant_sweep.py.

At B's neutral-career moments of 7 and 12 January (the document sweep's moments), UBS's request is read as it is and in
the blame framing (FROM) after the same history, and the two readings are compared at every even layer from 4 to 42,
two ways:
- "whole": the framed update's average state minus the neutral update's (the whole-message transplant of sim/steer3.py
  and of notebook 35's careers);
- "after": framed minus neutral on the tokens after the framed words only (the tokens that close UBS's turn and open
  the reply; the document states' construction, as in sim/frame_states.py).
Each is added to every token of the neutral update and of the reply, at its natural size ("whole" x1, "after" x1) and
"after" at two and four times its size, against a random direction of the same size at the same layer. Outcome: P(the order goes
along) after the fixed neutral reasoning line (sim/interventions.order_dist), as in the steering runs; the framed words
read as written are the yardstick. Each moment's "whole" and "after" vectors at every layer are saved, for the careers.

The same for the other frames (the user, 29 Oct: "What about gain, loss and credit?"): `framing` picks UBS's wording,
`whole=False` drops the "whole" conditions, and the layers can be the band where blame's state carried (BAND).
"""
import numpy as np

LAYERS = list(range(4, 44, 2))
BAND = [16, 20, 22, 24]                      # where the blame frame's "after" state carried (results/transplant_sweep)
FROM = "loss + you"
FRAMES = ["loss", "gain", "loss + you", "gain + you"]
NAME = {"loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit"}
RANDOM_SEED = 20261029
DATES = ("2011-01-07", "2011-01-12")


class Capture:
    """While on, keeps each watched layer's output over the positions of the pass ([positions, width], float32, CPU)."""

    def __init__(self, layer_modules):
        self.on, self.got = False, {}
        self.handles = [m.register_forward_hook(self._hook(L)) for L, m in layer_modules.items()]

    def _hook(self, L):
        def hook(module, inputs, output):
            if self.on:
                h = output[0] if isinstance(output, tuple) else output
                self.got[L] = h[0].float().cpu().numpy()
        return hook


def common_suffix(a, b):
    """How many tokens a and b share at their ends, counting only tokens after the first place they differ."""
    d = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    n = 0
    while n < min(len(a), len(b)) - d and a[-1 - n] == b[-1 - n]:
        n += 1
    return n


def conditions(layers=LAYERS, framing=FROM, whole=True):
    """[(name, kind, layer, strength)]: none and the framed words first, then seven conditions per layer (five without
    the "whole" ones)."""
    c = [("none", "none", None, 0), (f"framed ({framing}), as read", "framed", None, 0)]
    for L in layers:
        c += [(f"whole x1 L{L}", "whole", L, 1)] if whole else []
        c += [(f"after x1 L{L}", "after", L, 1), (f"after x2 L{L}", "after", L, 2), (f"after x4 L{L}", "after", L, 4)]
        c += [(f"random, whole size, L{L}", "random_whole", L, 1)] if whole else []
        c += [(f"random, after x2 size, L{L}", "random_after", L, 2), (f"random, after x4 size, L{L}", "random_after", L, 4)]
    return c


def framing_of(rows):
    """The frame a run's rows were measured with (from the framed-words condition's name)."""
    name = next(r["condition"] for r in rows if r["kind"] == "framed")
    return name[len("framed ("):-len("), as read")]


def random_units(width, layers=LAYERS, seed=RANDOM_SEED):
    """One random unit direction per layer, the same in every moment."""
    out = {}
    for L in layers:
        r = np.random.default_rng(seed + L).normal(size=width)
        out[L] = (r / np.linalg.norm(r)).astype(np.float32)
    return out


def shifts(neutral, framed, s, layers=LAYERS):
    """{"whole": {layer: vec}, "after": {layer: vec}} from the two readings' captured states ({layer: [positions,
    width]}) and the number of shared tokens after the framed words."""
    assert s >= 1, "no tokens after the framed words"
    return {"whole": {L: (framed[L].mean(0) - neutral[L].mean(0)).astype(np.float32) for L in layers},
            "after": {L: (framed[L][-s:].mean(0) - neutral[L][-s:].mean(0)).astype(np.float32) for L in layers}}


def vector(kind, layer, strength, sh, units):
    """The vector a condition adds (None for none and framed)."""
    if kind in ("none", "framed"):
        return None
    if kind == "whole":
        return strength * sh["whole"][layer]
    if kind == "after":
        return strength * sh["after"][layer]
    size = np.linalg.norm(sh["whole"][layer]) if kind == "random_whole" else strength * np.linalg.norm(sh["after"][layer])
    return size * units[layer]


def run_item(model, tok, steers, capture, units, item, career, chats, opening, lead, grid, done=(), layers=LAYERS,
             save=None, framing=FROM, whole=True):
    """Every condition at one neutral-career moment; one row per condition. `save(shifts, meta)` keeps the vectors."""
    import copy
    import torch
    from inside_careers import encode, turns_at
    from interventions import order_dist, prefill, split_point, summarise_orders
    from matched import matched
    idx = item["history_index"]
    full, k = split_point(tok, career, idx, opening)
    framed_full = encode(tok, turns_at(matched(career, idx, item["date"], "neutral", framing, chats), idx, opening))
    assert framed_full[:k] == full[:k] and framed_full != full, "the framed request must differ after the same history"
    s = common_suffix(framed_full, full)
    for st in steers.values():
        st.vec = None
    cache, sh = None, None

    def read(seq):
        capture.on, capture.got = True, {}
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([seq[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(seq), device=model.device))
        finally:
            capture.on = False
        return dict(capture.got)

    for name, kind, layer, strength in conditions(layers, framing, whole):
        key = f"{item['career_file']}|{idx}|{name}"
        if key in done:
            continue
        if cache is None:
            cache = prefill(model, full[:k])
        if sh is None and kind not in ("none", "framed"):
            sh = shifts(read(full), read(framed_full), s, layers)
            if save:
                save(sh, {"career_file": item["career_file"], "history_index": idx, "date": item["date"],
                          "framing": framing, "after_tokens": s, "extra_tokens": len(framed_full) - len(full)})
        vec = vector(kind, layer, strength, sh, units) if sh is not None else None
        seq = framed_full if kind == "framed" else full
        try:
            if vec is not None:
                steers[layer].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
            orders, probs, cover = order_dist(model, tok, seq, cache, lead, grid)
        finally:
            for st in steers.values():
                st.vec = None
        yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": idx,
               "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
               "condition": name, "kind": kind, "layer": layer, "strength": strength, "framing": framing,
               "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "after_tokens": s,
               "coverage": cover, "orders": orders, "probs": probs,
               **summarise_orders(orders, probs, item["position"], item["wants"])}
