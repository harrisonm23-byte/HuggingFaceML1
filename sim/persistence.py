"""The persistence check (the user, 22 Oct): does a state pushed once at the top (the jolt) still reach the agent's later
decisions, or does it fade?

On saved careers, nothing generated: the text stays exactly as the agent wrote it, and the only change is the state,
added at one layer to the pushed moment (the first 7 January update, with the memo, and the reply under it) at every
read, as notebook 32 does with --when once --span kept. Each reply's prompt is the start of the career's whole text, so
one reading of the whole career gives the agent's internal state at every later decision (the last token of each
update's prompt), with and without the push. The push changes the layer's output only on the pushed tokens; a later
decision can carry it only through the layers above, looking back across the conversation (in Gemma 3 most layers see
only the last 1,024 tokens; the full-attention ones see everything, and the reading records which they are).

Measures, at each later update, for each layer above the push: the change the push makes to the state at the decision,
as a share of the change it makes at the pushed moment itself (how much of its imprint is left, and in the same
direction: the cosine), against a random push of the same size. At a few key moments (after UBS's stop, the next
morning, the invitation) also the agent's order: P(it goes toward the stops), the expected position and P(it changes
its position), after the fixed neutral reasoning line, as in the layer scan.
"""
import glob, json, os
import numpy as np

KEY_TIMES = {"2011-01-07": ["09:45"], "2011-01-12": ["08:00", "09:30"]}
PUSH_DATE = "2011-01-07"


def pushed_turn(career):
    """The history index of the first 7 January update (the pushed moment) and of the reply under it."""
    p = next(i for i, t in enumerate(career["history"]) if t["role"] == "user" and PUSH_DATE in t["content"])
    assert career["history"][p + 1]["role"] == "assistant", "the pushed update has no reply after it"
    return p, p + 1


def region(tok, career, opening):
    """[start, end) tokens of the pushed moment: from the start of that update to the end of the reply under it."""
    from inside_careers import turns_at
    from state_careers import kept_end, update_start
    p, a = pushed_turn(career)
    start = update_start(tok, turns_at(career, p, opening))[0]
    last = max(i for i, t in enumerate(career["history"]) if t["role"] == "user")
    end = kept_end(tok, turns_at(career, last, opening), a + 1)          # turns_at puts the instructions first
    return start, end


def moments(career, days):
    """Every trading-day update after the pushed one, in order: its history index, date, time, the position held before
    it, the direction toward the nearest stops (wants), and whether it is a key moment (orders read there too)."""
    users = [i for i, t in enumerate(career["history"]) if t["role"] == "user"]
    p, _ = pushed_turn(career)
    out = []
    for d in days:
        msg = (d["summary"].get("slope") or {}).get("message")
        sides = {s[3] for s in d["summary"]["book_stops"]}
        wants = msg["wants"] if msg else ("down" if sides == {"sell"} else "up" if sides == {"buy"} else None)
        for i, s in enumerate(d["steps"]):
            hits = [k for k in users if s["observation"] in career["history"][k]["content"]]
            assert len(hits) == 1, f"{d['date']} {s['time']}: the update is found {len(hits)} times"
            if hits[0] <= p:
                continue
            out.append({"history_index": hits[0], "date": d["date"], "time": s["time"], "wants": wants,
                        "position": float(d["steps"][i - 1]["position"]) if i else 0.0,
                        "key": s["time"] in KEY_TIMES.get(d["date"], [])})
    return out


def load_career(folder, name):
    """A saved career and its main trading days (not the control days), in date order."""
    career = json.load(open(f"{folder}/careers/{name}.json"))
    days = [json.load(open(p)) for p in sorted(glob.glob(f"{folder}/days/{name}_2011-*.json")) if not p.endswith("_control.json")]
    return career, days


def opening_for(career):
    """The instructions the career was run with: the slope's (stops as other traders' orders) or the pilot's."""
    from career import career_opening
    from slope import slope_opening
    new = any("Stop-loss orders resting in the market" in t["content"] for t in career["history"] if t["role"] == "user")
    return slope_opening(career_opening()) if new else career_opening()


def imprint(h, h0, ref, ref0):
    """At one layer: the push's change at a later decision (h - h0) against its change at the pushed moment (ref - ref0):
    the share of its size that is left, the cosine, and its size relative to the state itself."""
    d, r = h - h0, ref - ref0
    nd, nr = float(np.linalg.norm(d)), float(np.linalg.norm(r))
    return {"left": nd / nr if nr else 0.0, "cos": float(d @ r / (nd * nr)) if nd and nr else 0.0,
            "relative": nd / float(np.linalg.norm(h0)) if np.linalg.norm(h0) else 0.0}


def run_career(model, tok, career, days, opening, arms, steers, rec, layers, lead=None, grid=None, orders=True):
    """Every arm on one saved career. arms: {name: None, or (push layer, vec)}, "none" first. steers: {layer: ArmSteer},
    registered before rec (an inside_careers.Recorder) so the recording sees the push. layers: the layers to measure;
    an arm is measured only above its own layer (below it nothing can change). Returns a JSON-able dict."""
    import torch
    from inside_careers import positions, read
    from interventions import order_dist, prefill, summarise_orders
    assert next(iter(arms)) == "none" and arms["none"] is None, "the first arm is none (the baseline)"
    ms = moments(career, days)
    full, pos, prompts = positions(tok, career, [m["history_index"] for m in ms], opening)
    r0, r1 = region(tok, career, opening)
    assert all(p is None or p >= r1 for p in pos), "a later decision falls inside the pushed moment"
    want = sorted({p for p in pos if p is not None} | {r1 - 1})
    at = [p if p is not None else ("alone", k) for k, p in enumerate(pos)]
    rows = [{**m, "tokens_after_push": (pos[k] if pos[k] is not None else len(prompts[k]) - 1) - (r1 - 1), "arms": {}}
            for k, m in enumerate(ms)]
    base = None
    for name, arm in arms.items():
        L, vec = arm if arm else (None, None)
        if arm:
            steers[L].set(torch.tensor(vec, dtype=torch.float32, device=model.device), r0, r1)
        try:
            got = read(model, full, want, rec)
            for k, p in enumerate(pos):          # a moment that is not an exact prefix: read on its own
                if p is None:
                    got[("alone", k)] = read(model, prompts[k], [len(prompts[k]) - 1], rec)[len(prompts[k]) - 1]
            got = {key: v[layers].numpy() for key, v in got.items()}
            got_orders = {}
            if orders and lead is not None:
                for k, m in enumerate(ms):
                    if m["key"]:
                        cache = prefill(model, prompts[k][:-1])
                        o, pr, cover = order_dist(model, tok, prompts[k], cache, lead, grid)
                        got_orders[k] = {"coverage": cover, **summarise_orders(o, pr, m["position"], m["wants"])}
        finally:
            for st in steers.values():
                st.set(None)
        if base is None:                         # none: the baseline the others are measured against
            base = got
            for k in got_orders:
                rows[k]["orders_none"] = got_orders[k]
            continue
        for k in range(len(ms)):
            rows[k]["arms"][name] = {str(Lm): imprint(got[at[k]][j], base[at[k]][j], got[r1 - 1][j], base[r1 - 1][j])
                                     for j, Lm in enumerate(layers) if Lm > L}
            if k in got_orders:
                rows[k]["arms"][name]["orders"] = got_orders[k]
    full_attention = [i for i, t in enumerate(getattr(getattr(model.config, "text_config", model.config), "layer_types", []) or [])
                      if t == "full_attention"]
    return {"region": [r0, r1], "tokens": len(full), "layers": list(layers), "full_attention_layers": full_attention,
            "arms": {n: (None if a is None else {"layer": a[0], "size": float(np.linalg.norm(a[1]))}) for n, a in arms.items()},
            "moments": rows}
