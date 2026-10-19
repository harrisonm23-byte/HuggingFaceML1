"""Inside the model at each push request of the full careers (the user, 19 Oct): the decision moments, rebuilt from the
saved careers, and the model's state there.

A decision moment is the update in which UBS's push request arrives: the conversation exactly as the agent was given it
(the instructions, everything before, that update), at the last token before its reply. Nothing is regenerated. The
residual stream (each decoder layer's output) at that token is recorded for every layer.

One pass per career: the model is causal, so its state at a token depends only on the tokens before it, and the six
decision moments of a career are prefixes of its one conversation. The pass reads the conversation up to the last
moment, in chunks (as the careers did), and keeps the states at the six positions. Each moment is checked to be an exact
token prefix of the career's conversation; one that is not is read on its own.
"""
import glob, json, os

PUSH = ["p344_i_can_hunt_with_u", "p316_bust_through_it", "p252_screw_other_people_harder", "p250_grow_our_mafia",
        "p317_stop_busters", "p253_11_oclock_rule"]
SIGN = {"up": 1, "down": -1}


def moments(folder, experiment):
    """Every push request of every career in a results folder: where it sits in the career's conversation, and what the
    agent then did. Experiment A's "no ask" careers give the same moments with no request (asked = False)."""
    out = []
    for path in sorted(glob.glob(os.path.join(folder, "careers", "*.json"))):
        career = json.load(open(path))
        users = [i for i, t in enumerate(career["history"]) if t["role"] == "user"]
        for day_path in sorted(glob.glob(path.replace("/careers/", "/days/")[:-5] + "_2011-*.json")):
            day = json.load(open(day_path))
            s, steps = day["summary"], day["steps"]
            for cid in PUSH:
                c = s["chats"].get(cid)
                if not c or c["wants"] not in SIGN:
                    continue
                i = next(k for k, st in enumerate(steps) if st["time"] >= c["at"])
                obs = steps[i]["observation"]
                hits = [k for k in users if obs in career["history"][k]["content"]]
                assert len(hits) == 1, f"{path} {cid}: the update is found {len(hits)} times in the conversation"
                g = SIGN[c["wants"]]
                held = float(steps[i - 1]["position"]) if i > 0 else 0.0
                out.append({"experiment": experiment, "version": career["version"], "run": career["run"],
                            "date": day["date"], "chat": cid, "wants": c["wants"], "history_index": hits[0],
                            "asked": "UBS [Agent A]" in obs,          # False: "no ask", the same moment without the request
                            "joined": bool(c["joined"]), "their_way": c["window_their_way"] or 0,
                            "held_their_way": g * held, "reply": steps[i]["reply"], "career_file": os.path.basename(path)})
    return out


def turns_at(career, history_index, opening):
    """The conversation the agent was given at a moment: the instructions, the history before, and that update (its
    first reading; a reply sent back for correction came after it)."""
    return [{"role": "system", "content": opening}] + career["history"][:history_index + 1]


def encode(tok, turns):
    return tok.apply_chat_template(turns, add_generation_prompt=True, return_dict=True)["input_ids"]


def positions(tok, career, idx, opening):
    """Token ids of the career's conversation up to its last moment, and each moment's last-token position in them.
    A moment whose prompt is not an exact prefix gets None (read on its own)."""
    prompts = [encode(tok, turns_at(career, i, opening)) for i in idx]
    longest = prompts[max(range(len(prompts)), key=lambda k: len(prompts[k]))]
    pos = [len(p) - 1 if longest[:len(p)] == p else None for p in prompts]
    return longest, pos, prompts


class Recorder:
    """Keeps every decoder layer's output at chosen absolute token positions, while the model reads in chunks."""

    def __init__(self, model):
        import torch
        self.torch = torch
        self.layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
        self.handles = [layer.register_forward_hook(self._hook(k)) for k, layer in enumerate(self.layers)]
        self.reset([])

    def reset(self, want):
        self.want, self.seen = set(want), [0] * len(self.layers)
        self.got = {}                                     # (position, layer) -> state

    def _hook(self, k):
        def hook(module, inputs, output):
            h = output[0] if isinstance(output, tuple) else output
            start, n = self.seen[k], h.shape[1]
            for p in self.want:
                if start <= p < start + n:
                    self.got[(p, k)] = h[0, p - start].float().cpu()
            self.seen[k] += n
        return hook

    def states(self, p):
        return self.torch.stack([self.got[(p, k)] for k in range(len(self.layers))])

    def remove(self):
        for h in self.handles:
            h.remove()


def read(model, ids, want, rec, chunk=4096):
    """One reading of `ids` (no reply kept), returning {position: [layers x width]} for the positions in `want`."""
    import torch
    rec.reset(want)
    x = torch.tensor([ids], device=model.device)
    with torch.no_grad():
        model.generate(input_ids=x, attention_mask=torch.ones_like(x), max_new_tokens=1, do_sample=False,
                       prefill_chunk_size=chunk, disable_compile=True)
    missing = [p for p in want if any((p, k) not in rec.got for k in range(len(rec.layers)))]
    assert not missing, f"positions not read: {missing}"
    return {p: rec.states(p) for p in want}
