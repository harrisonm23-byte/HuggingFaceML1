"""Steering, third run (the user, 21 Oct): two ways to capture the frame better than Stage 1 did.

1. The whole-message transplant. Stage 1 copied the framed state of one position only (the decision token) and nothing
   moved, while the framed words themselves raised going along. Here, at each of B's neutral-career requests, the
   loss + you version of the update is read, and its state averaged over all of the update's tokens (minus the neutral
   update's average, at the same moment) is added to every token of the neutral update, at one layer (6, 12, 18 or 24).
   Control: a random vector of the same size at the same layer.
2. Layer 18, pushed harder. Stage 1's loss direction at layer 18 moved the decision's state toward going along (and
   P(along) by +1.4 points at 4x, p = 0.08). Here at 8x and 16x its natural size, against random directions of the same
   size, with sampled replies to check they stay readable.
Outcome: P(the order goes along) after the fixed neutral reasoning line (and sampled replies where marked).
"""
import numpy as np

TRANSPLANT_LAYERS, RANDOM_LAYERS = [6, 12, 18, 24], [12, 18]
PUSH_LAYER, PUSH_STRENGTHS, N_RANDOM = 18, [8, 16], 3
FROM = "loss + you"
SAMPLES = 2


class MeanCapture:
    """While on, keeps each watched layer's output averaged over the positions of the pass."""

    def __init__(self, layer_modules):
        self.on, self.got = False, {}
        self.handles = [m.register_forward_hook(self._hook(L)) for L, m in layer_modules.items()]

    def _hook(self, L):
        def hook(module, inputs, output):
            if self.on:
                h = output[0] if isinstance(output, tuple) else output
                self.got[L] = h[0].float().mean(0).cpu().numpy()
        return hook


def conditions():
    """[(name, kind, layer, strength, sampled)]."""
    c = [("none", "none", None, 0, True), (f"framed ({FROM}), as read", "framed", None, 0, True)]
    c += [(f"message transplant at layer {L}", "transplant", L, 1, L == 18) for L in TRANSPLANT_LAYERS]
    c += [(f"random, transplant size, at layer {L}", "random_transplant", L, 1, False) for L in RANDOM_LAYERS]
    c += [(f"+loss x{s} at layer {PUSH_LAYER}", "push", PUSH_LAYER, s, True) for s in PUSH_STRENGTHS]
    c += [(f"random{k} x{s} at layer {PUSH_LAYER}", "random_push", PUSH_LAYER, s, k == 0)
          for s in PUSH_STRENGTHS for k in range(N_RANDOM)]
    return c


def run_item(model, tok, steers, mean_capture, dirs18, item, career, framed_full, opening, lead, grid, done=(),
             samples=SAMPLES):
    """Every condition at one neutral-career request. One row per condition."""
    import copy
    import torch
    from interventions import goes_along, order_dist, prefill, sample, split_point, summarise_orders
    from steer2 import half_for
    full, k = split_point(tok, career, item["history_index"], opening)
    assert framed_full[:k] == full[:k], "the history before the request differs in the framed version"
    for s in steers.values():
        s.vec = None
    cache, means = None, None

    def mean_of(seq):
        mean_capture.on, mean_capture.got = True, {}
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([seq[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(seq), device=model.device))
        finally:
            mean_capture.on = False
        return dict(mean_capture.got)

    d = dirs18[half_for(item["run"])]
    rng = np.random.default_rng(20261025 + item["history_index"])
    for name, kind, layer, strength, sampled in conditions():
        key = f"{item['career_file']}|{item['history_index']}|{name}"
        if key in done:
            continue
        if cache is None:
            cache = prefill(model, full[:k])
        if kind in ("transplant", "random_transplant") and means is None:
            f, n = mean_of(framed_full), mean_of(full)
            means = {L: f[L] - n[L] for L in TRANSPLANT_LAYERS}
        vec = None
        if kind == "transplant":
            vec = means[layer]
        elif kind == "random_transplant":
            r = rng.normal(size=means[layer].shape[0])
            vec = r / np.linalg.norm(r) * np.linalg.norm(means[layer])
        elif kind == "push":
            vec = strength * d["loss"]
        elif kind == "random_push":
            vec = strength * d["size"] * d["random"][int(name[6])]
        seq = framed_full if kind == "framed" else full
        try:
            if vec is not None:
                steers[layer].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
            orders, probs, cover = order_dist(model, tok, seq, cache, lead, grid)
            summary = summarise_orders(orders, probs, item["position"], item["wants"])
            replies = sample(model, seq, cache, samples, tok=tok) if sampled else []
        finally:
            for s in steers.values():
                s.vec = None
        judged = [goes_along(r, item["position"], item["wants"]) for r in replies]
        yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": item["history_index"],
               "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
               "condition": name, "kind": kind, "layer": layer, "strength": strength,
               "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "coverage": cover,
               "orders": orders, "probs": probs, **summary, "along": [a for a, _ in judged],
               "status": [s for _, s in judged], "replies": replies}
