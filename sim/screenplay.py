"""The screenplay history and the injected end state (the user, 21 Oct; designs/rd2/DESIGN_IDEAL_HISTORY.md).

The screenplay: in each of F's framed careers, the agent's reply to every chat (45 of the 46; the one with no scripted
reply keeps Gemma's own) is replaced by the user's scripted reply for that framing (designs/rd2/screenplay/, written
elsewhere, wired in as written): it goes along and takes on the framing every time. Only the CHAT line changes hands: the
reply keeps its original TARGET/HOLD/QUOTE lines, because the positions and P&L in later updates follow the original
trades; the original reasoning is dropped; a reply sent back for correction keeps only its accepted version.

At each request after the first (the same moments as the ideal history):
1. Screenplay against real: UBS's request in each of its five framings after the screenplay history; the real history
   with the request in the career's own framing.
2. The injection: the screenplay's state at the request (each layer's output averaged over the request update's tokens)
   minus the real history's, added to every token of the request update in the real history, at layer 12, 18 or 24;
   control: a random vector of the same size at layer 18.
Outcome: P(the order goes along) after the fixed neutral reasoning line.
"""
import hashlib, json, os
import numpy as np

REPLIES = "designs/rd2/screenplay/F_replies.jsonl"
FROZEN = "491370d5aee499d99de644a7ca5bd250e566cdef72811fc7763ab1d5c8afcb97"
CONDITION = {"Loss": "loss", "Gain": "gain", "Loss_Blame": "loss + you", "Gain_Credit": "gain + you"}
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
INJECT_LAYERS, RANDOM_LAYER = [12, 18, 24], 18
CORRECTION = "Your reply was not accepted"


def read_replies():
    """{version: [(first incoming line, reply)]} in chat order, after checking the file is the frozen one."""
    raw = open(REPLIES, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == FROZEN, "the screenplay replies changed"
    out = {}
    for line in raw.decode().splitlines():
        r = json.loads(line)
        out.setdefault(CONDITION[r["condition"]], []).append((r["incoming_messages"][0].strip(), r["gemma_reply"]))
    return out


def _incoming(text):
    if "New chat messages:" not in text:
        return []
    return [l.strip() for l in text.split("New chat messages:")[1].split("\n") if l.startswith("  ")]


def screenplay(career, upto, scripted):
    """The career up to and including the update at `upto`, with each earlier chat's reply replaced (see above).
    Returns (career, new index of that update, replies replaced)."""
    h, out, i, j, n = career["history"], [], 0, 0, 0
    while i < upto:
        t = h[i]
        inc = _incoming(t["content"]) if t["role"] == "user" else []
        if inc and j < len(scripted) and inc[0] == scripted[j][0]:
            # the accepted reply: the last one before the next update (corrections skipped)
            e = i + 1
            while e + 2 < upto and h[e + 1]["role"] == "user" and h[e + 1]["content"].startswith(CORRECTION):
                e += 2
            assert h[e]["role"] == "assistant"
            from mountain import parse_reply
            p = parse_reply(h[e]["content"])
            acts = [f"TARGET {p['target']}" if p["target"] is not None else "HOLD"]
            if p["quote"] is not None:
                acts.append(f"QUOTE {p['quote']:g}")
            out += [t, {**h[e], "content": "\n".join(acts + [f"CHAT: {scripted[j][1]}"])}]
            i, j, n = e + 1, j + 1, n + 1
        else:
            out.append(t)
            i += 1
    out.append(h[upto])
    return {**career, "history": out}, len(out) - 1, n


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


def run_item(model, tok, steers, mean_capture, career, item, scripted, chats, opening, lead, grid, done=()):
    """One request: the screenplay in five framings, the real history, and the injections. One row per condition."""
    import copy
    import torch
    from inside_careers import encode, turns_at
    from interventions import order_dist, prefill, split_point, summarise_orders
    from matched import matched
    idx, own = item["history_index"], item["version"]
    play, pidx, replaced = screenplay(career, idx, scripted)

    def read(c0, i, framing):
        _, k = split_point(tok, c0, i, opening)
        full = encode(tok, turns_at(matched(c0, i, item["date"], own, framing, chats), i, opening))
        return full, k

    def mean_of(full, k, cache):
        mean_capture.on, mean_capture.got = True, {}
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([full[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(full), device=model.device))
        finally:
            mean_capture.on = False
        return dict(mean_capture.got)

    conds = [("screenplay", f, None) for f in FRAMINGS] + [("real", own, None)]
    conds += [(f"inject at layer {L}", own, L) for L in INJECT_LAYERS] + [(f"random at layer {RANDOM_LAYER}", own, RANDOM_LAYER)]
    todo = [c for c in conds if f"{item['career_file']}|{idx}|{c[0]}|{c[1]}" not in done]
    if not todo:
        return
    for s in steers.values():
        s.vec = None
    pfull, pk = read(play, pidx, own)
    rfull, rk = read(career, idx, own)
    pcache, rcache = prefill(model, pfull[:pk]), prefill(model, rfull[:rk])
    shift = None
    if any(c[2] is not None for c in todo):
        a, b = mean_of(pfull, pk, pcache), mean_of(rfull, rk, rcache)
        shift = {L: a[L] - b[L] for L in INJECT_LAYERS}
    rng = np.random.default_rng(20261021 + idx)
    for name, framing, layer in todo:
        if name == "screenplay":
            full, cache = (pfull, pcache) if framing == own else (read(play, pidx, framing)[0], pcache)
        else:
            full, cache = rfull, rcache
        vec = None
        if name.startswith("inject"):
            vec = shift[layer]
        elif name.startswith("random"):
            r = rng.normal(size=shift[layer].shape[0])
            vec = r / np.linalg.norm(r) * np.linalg.norm(shift[layer])
        try:
            if vec is not None:
                steers[layer].vec = torch.tensor(vec, dtype=torch.float32, device=model.device)
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
        finally:
            for s in steers.values():
                s.vec = None
        yield {"key": f"{item['career_file']}|{idx}|{name}|{framing}", "career_file": item["career_file"],
               "version": own, "run": item["run"], "history_index": idx, "date": item["date"], "chat": item["chat"],
               "wants": item["wants"], "position": item["position"], "saved_joined": item["joined"], "condition": name,
               "framing": framing, "layer": layer, "replaced": replaced,
               "shift_size": float(np.linalg.norm(vec)) if vec is not None else 0.0, "coverage": cover,
               "orders": orders, "probs": probs, **summarise_orders(orders, probs, item["position"], item["wants"])}
