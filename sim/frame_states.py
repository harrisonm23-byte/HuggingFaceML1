"""UBS's framed messages' own states, put into the direct request (the author, 29 Oct; run by
scripts/modal_frame_states.py).

The direct request (results/lesson_lesson/ASKED_SAME_HISTORY.md): one saved no-state lesson career at 5 August 10:00,
UBS's plain line "I found a stop at {x}, when you see it, sell through...", and each emotional document's state switched
on at layer 22, 2 x, for that reply only. Every document state made the agent sell through the stop in 9 or 10 of 10
replies (no state 1, random 0). Here the same request gets the state of UBS's own framed messages instead.

The framed states are measured the way the document states were (sim/layer_scan.py), at the same 20 moments (B's ten
neutral careers at the 7 and 12 January requests), in bfloat16: UBS's request in each framing against the neutral
request at the same moment, everything before it unchanged (sim/matched.py). Two ways:
- "after": the change on the tokens that follow the framed words, framed minus neutral at the same tokens. This is the
  document states' construction, where the change was read on the tokens after the document. UBS's line ends the update,
  so these are only the few tokens that close UBS's turn and open the reply (the last of them is where the decision is
  read); the document states were read over the whole request that followed the document.
- "whole": the framed update's average state minus the neutral update's, over every token of the update (the framed
  words included; the whole-message transplant of scripts/modal_steer3.py).
Each is averaged over the 20 moments; its natural size is its length. A framed sentence is far shorter than a document,
so its state can be much smaller: each framed state is also used at the size of its document twin (loss, gain, blame,
credit), so that direction and dose can be told apart.
"""
import copy
import math

import numpy as np

FRAMES = ["loss", "gain", "loss + you", "gain + you"]
DOC_TWIN = {"loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit"}
KINDS = ["after", "whole"]


def common_suffix(a, b):
    """How many tokens a and b share at their ends, counting only tokens after the first place they differ."""
    d = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    n = 0
    while n < min(len(a), len(b)) - d and a[-1 - n] == b[-1 - n]:
        n += 1
    return n


def frame_shifts_at(model, tok, capture, career, item, chats, opening, layers):
    """{framing: {"after": {layer: vector}, "whole": {layer: vector}, "after_tokens", "extra_tokens"}} at one moment."""
    import torch
    from inside_careers import encode, turns_at
    from interventions import prefill, split_point
    from matched import matched
    idx = item["history_index"]
    base = matched(career, idx, item["date"], "neutral", "neutral", chats)
    plain = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    cache = prefill(model, plain[:k])

    def read(seq):
        capture.on, capture.got = True, {}
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([seq[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(seq), device=model.device))
        finally:
            capture.on = False
        return dict(capture.got)

    b = read(plain)
    out = {}
    for f in FRAMES:
        seq = encode(tok, turns_at(matched(career, idx, item["date"], "neutral", f, chats), idx, opening))
        assert seq[:k] == plain[:k], "the history before the update changed"
        assert seq != plain, f"{f}: the request is the same as the neutral one"
        s = common_suffix(seq, plain)
        assert s >= 1, f"{f}: no tokens after the framed words"
        a = read(seq)
        out[f] = {"after": {L: (a[L][len(seq) - k - s:] - b[L][len(plain) - k - s:]).mean(0).cpu().numpy() for L in layers},
                  "whole": {L: (a[L].mean(0) - b[L].mean(0)).cpu().numpy() for L in layers},
                  "after_tokens": s, "extra_tokens": len(seq) - len(plain)}
    return out


def pooled(shifts, frames, kinds, layers):
    """shifts: moments x frames x kinds x layers x width -> {(frame, kind, layer): mean vector over the moments}."""
    m = np.asarray(shifts, np.float64).mean(0)
    return {(f, kd, L): m[a, b, c] for a, f in enumerate(frames) for b, kd in enumerate(kinds) for c, L in enumerate(layers)}


def unit(v):
    return np.asarray(v, np.float64) / np.linalg.norm(v)


def cosine(a, b):
    return float(np.dot(unit(a), unit(b)))


def conditions(frame_states, doc_arms, layer=22, strength=2.0):
    """[(name, vector or None, note)] for the direct request: no state, the random direction and the loss document's
    state from the earlier run (the same vectors, as a bridge), then for each framing its "after" state at `strength`
    times its own size and at its document twin's size, and its "whole" state at the twin's size.
    frame_states: pooled(); doc_arms: sim/state_careers.build_arms() for loss, gain, blame, credit and random at `layer`."""
    doc = lambda theme: doc_arms[f"{theme} x{strength:g} L{layer}"]["vec"]
    out = [("none", None, "nothing added"),
           (f"random x{strength:g} L{layer}", doc("random"), "the earlier run's random direction"),
           (f"loss document x{strength:g} L{layer}", doc("loss"), "the earlier run's loss document state")]
    for f in FRAMES:
        twin = np.linalg.norm(doc(DOC_TWIN[f]))
        after, whole = frame_states[(f, "after", layer)], frame_states[(f, "whole", layer)]
        out += [(f"frame {f}, after, x{strength:g} own size", np.asarray(after * strength, np.float32),
                 f"UBS's {f} framing, its own size"),
                (f"frame {f}, after, {DOC_TWIN[f]} document size", np.asarray(unit(after) * twin, np.float32),
                 f"UBS's {f} framing, as large as the {DOC_TWIN[f]} document state"),
                (f"frame {f}, whole, {DOC_TWIN[f]} document size", np.asarray(unit(whole) * twin, np.float32),
                 f"UBS's {f} framing over the whole update, as large as the {DOC_TWIN[f]} document state")]
    return out


def fisher(a, n1, b, n2):
    """Two-sided Fisher's exact test for a of n1 against b of n2."""
    total, col = n1 + n2, a + b
    p = lambda x: math.comb(n1, x) * math.comb(n2, col - x) / math.comb(total, col)
    obs = p(a)
    return min(1.0, sum(p(x) for x in range(max(0, col - n2), min(n1, col) + 1) if p(x) <= obs * (1 + 1e-9)))
