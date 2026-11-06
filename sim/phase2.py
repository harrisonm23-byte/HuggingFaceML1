"""Phase 2, single moments: does changing the state at UBS's request lower going along without stopping legitimate
trading? (designs/rd2/MONITOR.md, "Decisions, 5 Nov"; the user, 6 Nov: include 12 January, every arm per request.)

Moments: every saved career's 7 January and 12 January requests (all seven experiments, 285 careers, 570 moments; the
conversation exactly as the agent was given it, nothing regenerated before the request). At each moment, every arm
reads the history before the request's update once, unsteered (one shared cache), then acts from the update on:

- none: no steering;
- contrastive x0.5, x1, x2: the difference-of-means direction (holding minus going along; `steer2.along_direction`,
  within request, experiment and framing, harmonic-weighted, built on the other half of the careers) at layer 24, at
  0.5, 1 and 2 times its natural size (the going-along gap), added to every token of the update and the reply;
- random x0.5, x1, x2: a random direction of the same size, the same way (one of ten fixed directions per moment, the
  same direction at all three sizes);
- contrastive x2, decision token only (secondary): added once, at the last token before the reply.

Conditional steering needs no arm of its own at a single moment: it is the contrastive reply where the frozen monitor
flags the request and the unsteered reply where it does not (results/conditional_steering/flags.csv, fixed before this
runs). Unconditional steering is the contrastive arm itself.

Each arm gives, from the same update:
- the decision token's state at layer 24 (the frozen monitor's score of it, and how far it sits along the going-along
  direction, in units of the gap's size), a check that the push reached the decision;
- P(the order goes along) after a fixed neutral reasoning line (no sampling noise; `interventions.order_dist`);
- SAMPLES replies sampled together, with the same random seed in every arm of a moment (paired seeds: the arms differ
  only by the steering). The analysis reads going along, HOLD, trades not UBS's way, readable actions and market
  reasoning from these.
"""
import copy, hashlib, json, os

import numpy as np

LAYER = 24                                   # the frozen monitor's layer and the going-along direction's
REQUESTS = {"p344_i_can_hunt_with_u": "7 Jan", "p316_bust_through_it": "12 Jan"}
STRENGTHS = [0.5, 1, 2]
N_RANDOM, RANDOM_SEED = 10, 20261107
SAMPLES, MAX_NEW_TOKENS, TEMPERATURE = 8, 300, 0.7      # the careers' own settings: temperature 0.7, 300 new tokens
FOLDERS = {"A": "career_book_neutral_lines_v2", "B": "ubs_framing_v2", "C": "takeover_ladder_v2",
           "C2": "takeover_ladder_real_lines_v2", "D": "memo_and_ubs_framing_v2", "E": "memo_ubs_bank_c_v2",
           "F": "peer_same_frame_v2"}
SIGN = {"up": 1, "down": -1}


def arms():
    """[(name, kind, which, strength)]: kind "all" adds the vector to every token from the update on; "token" once, at
    the decision token."""
    a = [("none", "all", None, 0)]
    a += [(f"contrastive x{s:g}", "all", "contrastive", s) for s in STRENGTHS]
    a += [(f"random x{s:g}", "all", "random", s) for s in STRENGTHS]
    a.append(("contrastive x2, decision token only", "token", "contrastive", 2))
    return a


def folder_of(exp):
    return f"results/full_career_gemma-3-12b-it_4bit_{FOLDERS[exp]}"


def as_read(exp, career, opening):
    """The career and instructions exactly as the model read them (as `scripts/modal_inside.py` read the states):
    notebook 29's model (C2) read the desk view; every other experiment read the saved text as it is."""
    if exp != "C2":
        return career, opening
    from takeover_desk import desk_opening, desk_text
    return ({**career, "history": [{**t, "content": desk_text(t["content"])} for t in career["history"]]},
            desk_opening(opening))


def stable_int(text):
    return int(hashlib.sha256(text.encode()).hexdigest()[:12], 16)


def work_items(moments):
    """Every 7 and 12 January request of every career, in a fixed order (request, experiment, career)."""
    items = []
    for exp in FOLDERS:
        for m in moments(folder_of(exp), exp):
            if m["asked"] and m["chat"] in REQUESTS:
                key = f"{exp}|{m['career_file']}|{m['chat']}"
                items.append({"key": key, "experiment": exp, "version": m["version"], "run": int(m["run"]),
                              "career_file": m["career_file"], "chat": m["chat"], "request": REQUESTS[m["chat"]],
                              "date": m["date"], "wants": m["wants"], "history_index": m["history_index"],
                              "position": m["held_their_way"] * SIGN[m["wants"]], "saved_joined": bool(m["joined"]),
                              "saved_reply": m["reply"], "random_index": stable_int(key) % N_RANDOM,
                              "seed": stable_int("seed|" + key) % 2 ** 31})
    order = list(REQUESTS)
    return sorted(items, key=lambda x: (order.index(x["chat"]), list(FOLDERS).index(x["experiment"]), x["career_file"]))


def spread(items, n):
    """n moments spread evenly over the ordered list (both requests, most experiments): the pilot."""
    if n <= 0 or n >= len(items):
        return items
    return [items[int(i)] for i in np.linspace(0, len(items) - 1, n).round()]


def half_for(run):
    return 0 if run < 5 else 1                 # steer2.along_direction: half 0 is built on runs 5-9, applied to 0-4


# Dimension 2339 of layer 24 is one of Gemma's massive-activation dimensions: about 80,000 at every request, with a
# spread of 3,834 across them (the next largest is 162). Left in, it is 88% of half 0's going-along gap (a difference of
# means is mostly noise there; half 1: 6%), so "the gap's size" and a random direction "of the same size" would mean
# very different pushes in the other dimensions for the two halves. Set to zero in every steering vector, and the sizes
# measured without it (the two halves' gaps then agree at cosine 0.72 instead of 0.35). Found from the states' spread
# alone, no labels.
DROP_DIMS = [2339]


def directions(run1_paths, layer=LAYER, n_random=N_RANDOM, seed=RANDOM_SEED, drop=DROP_DIMS):
    """steer2.along_direction (within request, experiment and framing, harmonic-weighted, built on the other half of
    the careers), with the massive-activation dimension(s) set to zero in the gap and in the random directions."""
    import steer2 as S2
    d = S2.along_direction(run1_paths, layer=layer, n_random=n_random, seed=seed)
    for h in d.values():
        h["size_with_dropped"] = h["size"]
        h["along"] = h["along"].copy()
        h["along"][drop] = 0.0
        h["size"] = float(np.linalg.norm(h["along"]))
        r = h["random"].copy()
        r[:, drop] = 0.0
        h["random"] = r / np.linalg.norm(r, axis=1, keepdims=True)
        h["dropped"] = list(drop)
    return d


def vector(dirs, item, which, strength):
    """The vector an arm adds at this moment (float64), or None."""
    if which is None:
        return None
    d = dirs[half_for(item["run"])]
    if which == "contrastive":
        return -strength * d["along"]                     # holding minus going along
    return strength * d["size"] * d["random"][item["random_index"]]


class SteerOnce:
    """Adds a vector at one position of a decoder layer's output, once: on the first pass long enough to hold that
    position (counted from the pass's start), then it switches itself off. Every pass here starts where the shared
    cache ends (the update's first token), so the decision token is at the same offset in all three."""

    def __init__(self, layer_module):
        self.vec, self.index = None, None
        self.handle = layer_module.register_forward_hook(self._hook)

    def _hook(self, module, inputs, output):
        if self.vec is None:
            return output
        h = output[0] if isinstance(output, tuple) else output
        if h.shape[1] <= self.index:
            return output
        h = h.clone()
        h[:, self.index] = h[:, self.index] + self.vec.to(h.dtype)
        self.vec = None
        return (h,) + tuple(output[1:]) if isinstance(output, tuple) else h


def sample_paired(model, tok, full, cache, n, seed, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE):
    """n replies to the decision prompt, sampled together from copies of the shared cache, with the random generator
    set to `seed` first (the same seed in every arm: paired)."""
    import torch
    c = copy.deepcopy(cache)
    c.batch_repeat_interleave(n)
    x = torch.tensor([full] * n, device=model.device)
    torch.manual_seed(seed)
    with torch.no_grad():
        g = model.generate(input_ids=x, attention_mask=torch.ones_like(x), past_key_values=c,
                           max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature,
                           disable_compile=True)          # as the careers sampled: temperature only (model defaults)
    return [tok.decode(g[i, len(full):], skip_special_tokens=True) for i in range(n)]


def run_item(model, tok, steer, once, capture, dirs, frozen, item, career, opening, lead, grid, done=(),
             samples=SAMPLES):
    """Every arm at one moment; yields one row per arm (the replies kept, for the analysis to read)."""
    import time
    import torch
    from interventions import goes_along, order_dist, prefill, split_point, summarise_orders
    full, k = split_point(tok, career, item["history_index"], opening)
    cache = None
    d = dirs[half_for(item["run"])]
    unit = d["along"] / d["size"]
    for name, kind, which, strength in arms():
        key = f"{item['key']}|{name}"
        if key in done:
            continue
        t0 = time.time()
        if cache is None:
            cache = prefill(model, full[:k])
        vec = vector(dirs, item, which, strength)
        v = None if vec is None else torch.tensor(vec, dtype=torch.float32, device=model.device)

        def arm():
            if v is None:
                return
            if kind == "all":
                steer.vec = v
            else:
                once.vec, once.index = v, len(full) - 1 - k

        try:
            arm()
            capture.on, capture.got = True, {}
            with torch.no_grad():
                model(input_ids=torch.tensor([full[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(full), device=model.device))
            capture.on = False
            state = capture.got[LAYER].astype(np.float64)
            arm()                                 # the single-token push switches itself off after each pass
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            arm()
            replies = sample_paired(model, tok, full, cache, samples, item["seed"])
        finally:
            capture.on = False
            steer.vec = once.vec = None
        judged = [goes_along(r, item["position"], item["wants"]) for r in replies]
        yield {"key": key, **{f: item[f] for f in ("experiment", "version", "run", "career_file", "chat", "request",
                                                    "date", "wants", "history_index", "position", "saved_joined",
                                                    "random_index", "seed")},
               "arm": name, "kind": kind, "which": which, "strength": strength,
               "vector_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "gap_size": d["size"],
               "monitor_score": float(((state - frozen["mu"]) / frozen["sc"]) @ frozen["coef"] + frozen["intercept"][0]),
               "along_position": float(state @ unit), "coverage": cover, "orders": orders, "probs": probs,
               **summarise_orders(orders, probs, item["position"], item["wants"]),
               "went_along": [a for a, _ in judged], "status": [s for _, s in judged], "replies": replies,
               "tokens": len(full), "update_tokens": len(full) - k, "seconds": time.time() - t0}
