"""Careers with a document's after-reading state switched on (the injection series' last step; notebook 31, run by
scripts/modal_state_careers.py).

B's neutral careers are run again from the start, with UBS's neutral wording and the neutral memo, and one fixed state
added inside the model at one layer while the agent reads and writes. The states are the ones the layer scans tested:
each document type's after-reading change over UBS's request minus the neutral document's (sim/layer_scan.py), here
averaged over all 20 scanned moments (both halves of the careers, since the new careers are new runs). Arms:

    "loss@21"        the emotional loss state at layer 21
    "fin:loss@26"    the financial loss state at layer 26
    "random@21"      a random direction at layer 21, as large as the emotional states there (on average)
    "fin:random@26"  the same, sized on the financial states
    "none"           nothing added

Every state is used at STRENGTH times its natural size (its length). A layer must have been scanned: 18-21 (the
confirmation scan) or an even layer from 4 to 42 (the sweep).

When the state is on (WHEN): "every" reply of the career, or "trading" days only. Where (SPAN): "update", the newest
update and the reply, as in the layer scans (the history before it is read as it is); or "all", every token of the
conversation.
"""
import hashlib
import os
import re

import numpy as np

SOURCES = {"emotion": ["/states/v2/layer_scan_18_21", "/states/v2/layer_scan_18_21_sweep"],
           "financial": ["/states/v2/layer_scan_18_21_fin", "/states/v2/layer_scan_18_21_fin_sweep"]}
WHENS, SPANS = ("every", "trading"), ("update", "all")
RANDOM_SEED = 20261022


def parse_arms(spec):
    """"loss@21,fin:loss@26,random@21,none" -> [(doc_set, theme, layer)], none as (None, None, None)."""
    out = []
    for a in [x.strip() for x in spec.split(",") if x.strip()]:
        if a == "none":
            out.append((None, None, None))
            continue
        m = re.fullmatch(r"(?:(fin|emo):)?([a-z]+)@(\d+)", a)
        assert m, f"arm {a!r}: write it as theme@layer, e.g. loss@21 or fin:loss@26"
        out.append(("financial" if m.group(1) == "fin" else "emotion", m.group(2), int(m.group(3))))
    assert len(set(out)) == len(out), f"an arm is listed twice: {spec}"
    return out


def arm_name(doc_set, theme, layer, strength):
    """The career's version name, e.g. "loss x2 L21" or "fin loss x2 L26"."""
    if theme is None:
        return "none"
    s = f"{strength:g}"
    return ("fin " if doc_set == "financial" else "") + f"{theme} x{s} L{layer}"


def load_states(path):
    """{theme: {layer: pooled vector}} from a layer scan's shifts.npz (moments x themes x layers x width)."""
    z = np.load(path)
    layers, themes = [int(x) for x in z["layers"]], [str(t) for t in z["themes"]]
    pooled = z["shifts"].astype(np.float64).mean(0)
    return {t: {L: pooled[a, j] for j, L in enumerate(layers)} for a, t in enumerate(themes)}, int(len(z["runs"]))


def state_at(doc_set, layer, sources=None):
    """({theme: vector at `layer`}, the file it came from, moments): the confirmation scan if it has the layer, else
    the sweep."""
    for d in (sources or SOURCES)[doc_set]:
        p = os.path.join(d, "shifts.npz")
        if os.path.exists(p):
            states, n = load_states(p)
            if layer in next(iter(states.values())):
                return {t: v[layer] for t, v in states.items()}, p, n
    raise ValueError(f"layer {layer} was not scanned for the {doc_set} documents (18-21, or an even layer 4-42 once "
                     "the sweep has run)")


def sha(vec):
    return "none" if vec is None else hashlib.sha256(np.asarray(vec, np.float32).tobytes()).hexdigest()[:16]


def build_arms(spec, strength, sources=None):
    """{version name: {"doc_set", "theme", "layer", "strength", "size" (natural), "vec" (float32, or None), "sha",
    "source", "moments"}}."""
    out = {}
    for doc_set, theme, layer in parse_arms(spec):
        name = arm_name(doc_set, theme, layer, strength)
        if theme is None:
            out[name] = {"doc_set": None, "theme": None, "layer": None, "strength": 0.0, "size": 0.0, "vec": None,
                         "sha": "none", "source": None, "moments": 0}
            continue
        states, src, n = state_at(doc_set, layer, sources)
        if theme == "random":
            size = float(np.mean([np.linalg.norm(v) for v in states.values()]))
            r = np.random.default_rng(RANDOM_SEED + layer + (1000 if doc_set == "financial" else 0)).normal(
                size=len(next(iter(states.values()))))
            unit = r / np.linalg.norm(r)
        else:
            assert theme in states, f"no {theme} state in {src} (it has {', '.join(states)})"
            size = float(np.linalg.norm(states[theme]))
            unit = states[theme] / size
        vec = (unit * size * strength).astype(np.float32)
        out[name] = {"doc_set": doc_set, "theme": theme, "layer": layer, "strength": float(strength), "size": size,
                     "vec": vec, "sha": sha(vec), "source": src, "moments": n}
    return out


FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]    # B's five, as in its careers


def run_name(framing, when, span):
    """The run's name: state_careers, plus the framing if not neutral, plus when/span if not every/update."""
    assert framing in FRAMINGS, f"framing {framing!r}: one of {FRAMINGS}"
    assert when in WHENS and span in SPANS, (when, span)
    return ("state_careers" + ("" if framing == "neutral" else "_" + framing.replace(" + ", "_plus_"))
            + ("" if (when, span) == ("every", "update") else f"_{when}_{span}"))


def steer_on(when, date, trading_days):
    """Whether the state is on for an update on `date`."""
    assert when in WHENS, when
    return when == "every" or (date is not None and date in trading_days)


def update_start(tok, turns):
    """The token where the newest update starts: where the conversation without it stops matching the whole one."""
    full = tok.apply_chat_template(turns, add_generation_prompt=True, return_dict=True)["input_ids"]
    try:                                   # (the instructions alone may not render on their own: then steer from 0)
        before = tok.apply_chat_template(turns[:-1], return_dict=True)["input_ids"] if len(turns) > 1 else []
    except Exception:
        before = []
    n = 0
    for a, b in zip(full, before):
        if a != b:
            break
        n += 1
    return n, len(full)


class ArmSteer:
    """Adds `vec` to a decoder layer's output at every token from position `start` on (positions as the model counts
    them, so chunked reading and token-by-token writing are both covered); nothing when off."""

    def __init__(self, layer_module):
        self.vec, self.start, self.steered = None, 0, 0
        self.handle = layer_module.register_forward_hook(self._hook, with_kwargs=True)

    def set(self, vec=None, start=0):
        self.vec, self.start, self.steered = vec, start, 0

    def _hook(self, module, args, kwargs, output):
        if self.vec is None:
            return output
        h = output[0] if isinstance(output, tuple) else output
        pos = kwargs.get("position_ids")
        assert pos is not None, "the decoder layer was called without position_ids"
        mask = (pos[0] >= self.start).to(h.dtype)[None, :, None]
        self.steered += int(mask.sum())
        h = h + mask * self.vec.to(h.dtype)
        return (h,) + tuple(output[1:]) if isinstance(output, tuple) else h
