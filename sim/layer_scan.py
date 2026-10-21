"""Layer scan for the after-reading state (the user, 22 Oct): where along the forward pass does the loss document's state
push the decision, and how strongly?

Stage A (directions): at each of B's 60 neutral-career requests, the agent reads a loss document and, separately, a
neutral document just before UBS's request (sim/prime.py; the same document indices as the injection run). At each
scanned layer, the change each reading makes to the state over the request's update is averaged over the update's tokens;
the loss change minus the neutral change is the loss-specific part. Averaged over the moments of the other half of the
careers (runs 5-9 for careers 0-4 and the other way round), it is one fixed direction per layer and half; its natural
size is its length.
Stage B (the scan): with no document, that direction is added at one layer to every token from the start of the request's
update, at 1, 2, 4 and 8 times its natural size, against a random direction of the same size (at 4 and 8 times).
Outcome: P(the order goes along) after the fixed neutral reasoning line. At one fixed moment (the showcase), one greedy
reply is also written under every condition, to see what the injected state does to the agent's words.
"""
import copy
import numpy as np

LAYERS = [18, 19, 20, 21]          # the confirmation scan: where the showcase and the injection run put the effect
ALL_LAYERS = list(range(48))
STRENGTHS = [1, 2]
RANDOM_STRENGTH = 2
SAMPLES = 2                         # sampled replies per moment, with no injection and at 1x (the agent's own words)
SWEEP_LAYERS, SWEEP_STRENGTH = list(range(4, 44, 2)), 2   # the sweep: every second layer, read-out only


def conditions(themes):
    """[(name, theme, layer, kind, strength, sampled)]."""
    c = [("none", None, None, "none", 0, True)]
    for L in LAYERS:
        for t in themes:
            c += [(f"{t} x{s} at layer {L}", t, L, "push", s, s == 1) for s in STRENGTHS]
        c.append((f"random x{RANDOM_STRENGTH} at layer {L}", None, L, "random", RANDOM_STRENGTH, False))
    return c


def base_and_docs(career, item, docs, chats, opening, tok, themes=("loss", "neutral")):
    from inside_careers import encode, turns_at
    from interventions import split_point
    from matched import matched
    from prime import primed
    idx = item["history_index"]
    base = matched(career, idx, item["date"], "neutral", "neutral", chats)
    plain = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    reads = {}
    for t in themes:
        doc = docs[t][item["doc"] % len(docs[t])]
        seq = encode(tok, turns_at(primed(base, idx, doc), idx, opening))
        assert seq[:k] == plain[:k], "the history before the update changed"
        extra = len(seq) - len(plain)
        start = next(i for i in range(k, len(plain)) if seq[i] != plain[i])
        assert seq[start + extra:] == plain[start:], "the update after the document does not line up"
        reads[t] = (seq, start, extra)
    return plain, k, reads


def shifts_at(model, tok, capture, career, item, docs, chats, opening, layers=LAYERS, theme="loss", all_themes=False,
              only=None):
    """{layer: the `theme` reading's mean change over the update minus the neutral reading's} at one moment; with
    all_themes, {theme: {layer: ...}} for every document type but neutral."""
    import torch
    from interventions import prefill
    themes = [t for t in docs if t != "neutral" and (not only or t in only)] if all_themes else [theme]
    plain, k, reads = base_and_docs(career, item, docs, chats, opening, tok, tuple(themes) + ("neutral",))
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
    means = {}
    for t, (seq, start, extra) in reads.items():
        a = read(seq)
        means[t] = {L: (a[L][start - k + extra:] - b[L][start - k:]).mean(0).cpu().numpy() for L in layers}
    if all_themes:
        return {t: {L: means[t][L] - means["neutral"][L] for L in layers} for t in themes}
    for L in layers:
        out[L] = means[theme][L] - means["neutral"][L]
    return out


def conditions_sweep(themes):
    """The sweep: each state at 2x and a random direction at every second layer (read-out only, except no injection)."""
    c = [("none", None, None, "none", 0, True)]
    for L in SWEEP_LAYERS:
        c += [(f"{t} x{SWEEP_STRENGTH} at layer {L}", t, L, "push", SWEEP_STRENGTH, False) for t in themes]
        c.append((f"random x{SWEEP_STRENGTH} at layer {L}", None, L, "random", SWEEP_STRENGTH, False))
    return c


def build_directions(rows, layers=None):
    """rows: [(run, {theme: {layer: vector}})] -> {half: {theme: {layer: (direction, size)}}}; half 0 is applied to runs
    0-4 and built on runs 5-9, half 1 the other way."""
    out = {}
    themes = list(rows[0][1])
    for half in (0, 1):
        use = [d for run, d in rows if (run >= 5) == (half == 0)]
        out[half] = {t: {} for t in themes}
        for t in themes:
            for L in (layers or LAYERS):
                v = np.mean([d[t][L] for d in use], 0)
                out[half][t][L] = (v, float(np.linalg.norm(v)))
    return out


def run_item(model, tok, steers, career, item, dirs, chats, opening, lead, grid, themes, done=(), samples=SAMPLES,
             conds=None):
    """Every condition at one request (no document). One row per condition."""
    import torch
    from inside_careers import encode, turns_at
    from interventions import goes_along, order_dist, prefill, sample, split_point, summarise_orders
    from matched import matched
    from steer2 import half_for
    idx = item["history_index"]
    base = matched(career, idx, item["date"], "neutral", "neutral", chats)
    full = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    cache = None
    h = half_for(int(item["run"]))
    rng = np.random.default_rng(20261022 + idx)
    for name, t, L, kind, s, sampled in (conds or conditions(themes)):
        key = f"{item['career_file']}|{idx}|{name}"
        r = rng.normal(size=4096)                         # drawn every time, so a resumed run gets the same vectors
        if key in done:
            continue
        if cache is None:
            cache = prefill(model, full[:k])
        vec = None
        if kind == "push":
            d, _ = dirs[h][t][L]
            vec = d * s
        elif kind == "random":
            size = np.mean([dirs[h][tt][L][1] for tt in themes])
            r = r[:dirs[h][themes[0]][L][0].shape[0]]
            vec = r / np.linalg.norm(r) * size * s
        try:
            for st in steers.values():
                st.vec = None
            if vec is not None:
                steers[L].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            replies = sample(model, full, cache, samples, tok=tok) if sampled else []
        finally:
            for st in steers.values():
                st.vec = None
        judged = [goes_along(x, item["position"], item["wants"]) for x in replies]
        yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": idx,
               "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
               "condition": name, "theme": t, "layer": L, "kind": kind, "strength": s,
               "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "coverage": cover,
               "orders": orders, "probs": probs, **summarise_orders(orders, probs, item["position"], item["wants"]),
               "replies": replies, "along": [a for a, _ in judged], "status": [st_ for _, st_ in judged]}


def showcase(model, tok, steers, capture, career, item, docs, chats, opening, lead, grid, strength=1, max_new=300,
             only=None):
    """One moment: the loss-specific change measured there, then, with no document, added at each layer in turn (one
    greedy reply each), plus no injection. One row per layer."""
    import torch
    from inside_careers import encode, turns_at
    from interventions import order_dist, prefill, split_point, summarise_orders
    from matched import matched
    from mountain import parse_reply
    D = shifts_at(model, tok, capture, career, item, docs, chats, opening, ALL_LAYERS, all_themes=True, only=only)
    idx = item["history_index"]
    base = matched(career, idx, item["date"], "neutral", "neutral", chats)
    full = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    cache = prefill(model, full[:k])
    for t, L in [(None, None)] + [(t, L) for t in D for L in ALL_LAYERS]:
        d = D.get(t)
        try:
            for st in steers.values():
                st.vec = None
            if L is not None:
                steers[L].vec = torch.tensor(d[L] * strength, dtype=torch.float32, device=model.device)
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            x = torch.tensor([full], device=model.device)
            with torch.no_grad():
                g = model.generate(input_ids=x, attention_mask=torch.ones_like(x), past_key_values=copy.deepcopy(cache),
                                   max_new_tokens=max_new, do_sample=False, disable_compile=True)
            reply = tok.decode(g[0, len(full):], skip_special_tokens=True)
        finally:
            for st in steers.values():
                st.vec = None
        yield {"theme": t, "layer": L, "strength": strength if L is not None else 0,
               "shift_size": float(np.linalg.norm(d[L])) * strength if L is not None else 0.0,
               "career_file": item["career_file"], "date": item["date"], "chat": item["chat"], "wants": item["wants"],
               "coverage": cover, **summarise_orders(orders, probs, item["position"], item["wants"]),
               "reply": reply, "reply_status": parse_reply(reply)["status"]}


FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
FRAMED_LAYERS, FRAMED_STRENGTH = [19, 21], 2
FRAMED_SAMPLED = ("loss", "blame")


def conditions_framed(themes, layers=None):
    """[(name, theme, layer, kind, strength, sampled)] for one framing of UBS's request."""
    c = [("none", None, None, "none", 0, True)]
    for L in (layers or FRAMED_LAYERS):
        c += [(f"{t} x{FRAMED_STRENGTH} at layer {L}", t, L, "push", FRAMED_STRENGTH, t in FRAMED_SAMPLED) for t in themes]
        c.append((f"random x{FRAMED_STRENGTH} at layer {L}", None, L, "random", FRAMED_STRENGTH, False))
    return c


def run_item_framed(model, tok, steers, career, item, dirs, chats, opening, lead, grid, themes, done=(), samples=SAMPLES,
                    layers=None, sampled_themes=FRAMED_SAMPLED):
    """The states injected with UBS's request in each of its five framings (the same neutral career, the same moment).
    One row per framing and condition."""
    import torch
    from inside_careers import encode, turns_at
    from interventions import goes_along, order_dist, prefill, sample, split_point, summarise_orders
    from matched import matched
    from steer2 import half_for
    idx = item["history_index"]
    h = half_for(int(item["run"]))
    _, k = split_point(tok, career, idx, opening)
    cache = None
    for v in FRAMINGS:
        full = encode(tok, turns_at(matched(career, idx, item["date"], "neutral", v, chats), idx, opening))
        rng = np.random.default_rng(20261022 + idx)
        for name, t, L, kind, s, sampled in conditions_framed(themes, layers):
            sampled = kind == "none" or (kind == "push" and t in sampled_themes)
            key = f"{item['career_file']}|{idx}|{v}|{name}"
            r = rng.normal(size=4096)
            if key in done:
                continue
            if cache is None:
                cache = prefill(model, full[:k])
            vec = None
            if kind == "push":
                vec = dirs[h][t][L][0] * s
            elif kind == "random":
                size = np.mean([dirs[h][tt][L][1] for tt in themes])
                r = r[:dirs[h][themes[0]][L][0].shape[0]]
                vec = r / np.linalg.norm(r) * size * s
            try:
                for st in steers.values():
                    st.vec = None
                if vec is not None:
                    steers[L].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
                orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
                replies = sample(model, full, cache, samples, tok=tok) if sampled else []
            finally:
                for st in steers.values():
                    st.vec = None
            judged = [goes_along(x, item["position"], item["wants"]) for x in replies]
            yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": idx,
                   "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
                   "framing": v, "condition": name, "theme": t, "layer": L, "kind": kind, "strength": s,
                   "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "coverage": cover,
                   "orders": orders, "probs": probs, **summarise_orders(orders, probs, item["position"], item["wants"]),
                   "replies": replies, "along": [a for a, _ in judged], "status": [st_ for _, st_ in judged]}
