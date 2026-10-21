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

LAYERS = [12, 14, 16, 18, 20, 22, 24]
ALL_LAYERS = list(range(48))
STRENGTHS = [1, 2, 4, 8]
RANDOM_STRENGTHS = [4, 8]


def conditions():
    """[(name, layer, kind, strength)]."""
    c = [("none", None, "none", 0)]
    for L in LAYERS:
        c += [(f"loss-specific x{s} at layer {L}", L, "push", s) for s in STRENGTHS]
        c += [(f"random x{s} at layer {L}", L, "random", s) for s in RANDOM_STRENGTHS]
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


def build_directions(rows):
    """rows: [(run, {layer: vector})] -> {half: {layer: (direction, size)}}; half 0 is applied to runs 0-4 and built on
    runs 5-9, half 1 the other way."""
    out = {}
    for half in (0, 1):
        use = [d for run, d in rows if (run >= 5) == (half == 0)]
        out[half] = {}
        for L in LAYERS:
            v = np.mean([d[L] for d in use], 0)
            out[half][L] = (v, float(np.linalg.norm(v)))
    return out


def run_item(model, tok, steers, career, item, dirs, chats, opening, lead, grid, done=(), showcase=False, max_new=300):
    """Every condition at one request (no document). One row per condition."""
    import torch
    from inside_careers import encode, turns_at
    from interventions import order_dist, prefill, split_point, summarise_orders
    from matched import matched
    from mountain import parse_reply
    from steer2 import half_for
    idx = item["history_index"]
    base = matched(career, idx, item["date"], "neutral", "neutral", chats)
    full = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    cache = None
    h = half_for(int(item["run"]))
    rng = np.random.default_rng(20261022 + idx)
    for name, L, kind, s in conditions():
        key = f"{item['career_file']}|{idx}|{name}"
        if key in done:
            continue
        if cache is None:
            cache = prefill(model, full[:k])
        vec = None
        if kind != "none":
            d, size = dirs[h][L]
            if kind == "push":
                vec = d * s
            else:
                r = rng.normal(size=d.shape[0])
                vec = r / np.linalg.norm(r) * size * s
        reply = None
        try:
            for st in steers.values():
                st.vec = None
            if vec is not None:
                steers[L].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            if showcase:
                x = torch.tensor([full], device=model.device)
                with torch.no_grad():
                    g = model.generate(input_ids=x, attention_mask=torch.ones_like(x), past_key_values=copy.deepcopy(cache),
                                       max_new_tokens=max_new, do_sample=False, disable_compile=True)
                reply = tok.decode(g[0, len(full):], skip_special_tokens=True)
        finally:
            for st in steers.values():
                st.vec = None
        yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": idx,
               "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
               "condition": name, "layer": L, "kind": kind, "strength": s,
               "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "coverage": cover,
               "orders": orders, "probs": probs, **summarise_orders(orders, probs, item["position"], item["wants"]),
               "showcase": showcase, "reply": reply, "reply_status": parse_reply(reply)["status"] if reply else None}


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
