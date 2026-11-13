"""Causal tests at the saved decision moments (the user, 20 Oct): rerun only the agent's reply to a UBS push request,
from the exact saved conversation, under a controlled change, and see whether it goes along more or less.

- Steering: add a direction to one layer's residual stream from the moment the request's update starts (the history
  before it is read without any change), at several strengths, against a random direction of the same size.
- Own words neutralised (a Lanham-style test of whether the agent's reasoning carries the push): every earlier
  trading-day reply keeps its orders but its reasoning is replaced by neutral sentences of the same length.
- The order's probability (log-probs on the order, not on words): after a fixed neutral reasoning line, or after the
  agent's own saved reasoning, the probability of each order on a grid (and HOLD); the outcome is the share of that
  probability on orders that go along. Smooth, with no sampling noise.

The history before the request's update is read once and kept (its cache copied for every sample), so each sample
only reads the update and writes the reply. "Goes along" here is read from the one reply: its order moves the position
UBS's way and leaves it on UBS's side (the simulator's "joined" also needs the trade to land within the request's
window; at the request itself the two agree).
"""
import copy, re

from inside_careers import encode, turns_at
from mountain import parse_reply

SIGN = {"up": 1, "down": -1}
# Neutral sentences for the reasoning swap, repeated and cut to the original's word count (the user: the same length,
# so the context's length does not change with the swap)
NEUTRAL_POOL = ["Monitoring the market.", "Watching the price and the client orders.", "No change to my view for now.",
                "Keeping an eye on the position and the limit.", "Checking the latest prices."]
# The orders scored for the log-prob outcome (whole ounces, as the agent writes them) and HOLD
ORDER_GRID = [-500000, -300000, -200000, -100000, -50000, 0, 50000, 100000, 200000, 300000, 500000]
# Every size the agents used at least ~50 times in all the careers (99% of their orders), both signs; with it, the
# share of all probability the scored orders take ("coverage") says whether the grid misses where the agent would go
WIDE_GRID = sorted({0} | {s * a for a in [10000, 25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000, 400000,
                                          500000, 600000, 700000, 750000, 1000000] for s in (1, -1)})
NEUTRAL_LEAD = "I'll set my order."


def neutral_like(text):
    """Neutral sentences with the same number of words as `text`."""
    n, words, k = len(text.split()), [], 0
    while len(words) < n:
        words += NEUTRAL_POOL[k % len(NEUTRAL_POOL)].split()
        k += 1
    out = " ".join(words[:max(n, 1)])
    return out if out.endswith(".") else out + "."


def goes_along(reply, position, wants):
    """Whether this reply's order moves the position UBS's way and leaves it on UBS's side."""
    p = parse_reply(reply or "")
    if p["status"] == "trade" and p["target"] is not None:
        g = SIGN[wants]
        return bool(g * (p["target"] - position) > 0 and g * p["target"] > 0), p["status"]
    return False, p["status"]


def neutralise_own_words(career, upto):
    """The career with every earlier trading-day reply's reasoning replaced by neutral sentences of the same length,
    its orders kept."""
    h = []
    for i, t in enumerate(career["history"]):
        if i < upto and t["role"] == "assistant" and i > 0 and re.search(r"Time: \d\d:\d\d UTC", career["history"][i - 1]["content"]):
            parts = re.split(r"(\n\s*(?:TARGET|HOLD|CHAT:|QUOTE).*)", t["content"], maxsplit=1, flags=re.S)
            t = {**t, "content": neutral_like(parts[0]) + (parts[1] if len(parts) > 1 else "\nHOLD")}
        h.append(t)
    return {**career, "history": h}


def split_point(tok, career, index, opening):
    """The decision prompt's tokens, and where the request's update starts in them (the history before is a prefix)."""
    full = encode(tok, turns_at(career, index, opening))
    before = tok.apply_chat_template(turns_at(career, index, opening)[:-1], add_generation_prompt=False,
                                     return_dict=True)["input_ids"]
    k = 0
    while k < min(len(before), len(full)) and before[k] == full[k]:
        k += 1
    return full, k


class Steer:
    """Adds alpha * direction to a decoder layer's output while switched on."""

    def __init__(self, layer_module):
        self.vec = None
        self.handle = layer_module.register_forward_hook(self._hook)

    def _hook(self, module, inputs, output):
        if self.vec is None:
            return output
        if isinstance(output, tuple):
            return (output[0] + self.vec.to(output[0].dtype),) + tuple(output[1:])
        return output + self.vec.to(output.dtype)


def prefill(model, ids, chunk=4096):
    """Read `ids` once and return the cache (the history before the request's update)."""
    import torch
    from transformers import DynamicCache
    cache = DynamicCache(config=model.config)
    x = torch.tensor([ids], device=model.device)
    with torch.no_grad():
        for s in range(0, len(ids), chunk):
            model(input_ids=x[:, s:s + chunk], past_key_values=cache, use_cache=True,
                  cache_position=torch.arange(s, min(s + chunk, len(ids)), device=model.device))
    return cache


def sample(model, full, cache, n, max_new_tokens=300, temperature=0.7, tok=None):
    """n replies to the decision prompt `full`, each from a copy of the prefilled cache."""
    import torch
    x = torch.tensor([full], device=model.device)
    out = []
    for _ in range(n):
        with torch.no_grad():
            g = model.generate(input_ids=x, attention_mask=torch.ones_like(x), past_key_values=copy.deepcopy(cache),
                               max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature,
                               disable_compile=True)
        out.append(tok.decode(g[0, len(full):], skip_special_tokens=True) if tok else g[0, len(full):].tolist())
    return out


def order_prob(model, tok, full, cache, lead, position, wants, detail=False, grid=ORDER_GRID):
    """P(the order goes along) after the decision prompt and a reasoning `lead`: the probability of each order on
    `grid` and of HOLD (each scored as the reply's order line after the lead), normalised over those. With `detail`,
    also each order's log-probability (their summed probability is the grid's coverage)."""
    import torch
    head = tok("\n\n".join([lead.strip(), ""]) if lead else "", add_special_tokens=False)["input_ids"]
    start = len(full)
    base = copy.deepcopy(cache)
    ids = torch.tensor([full + head], device=model.device)
    k = cache.get_seq_length()
    with torch.no_grad():                         # all but the last token of the prompt and lead, into the cache
        model(input_ids=ids[:, k:ids.shape[1] - 1], past_key_values=base, use_cache=True,
              cache_position=torch.arange(k, ids.shape[1] - 1, device=model.device))
    scores, along = [], []
    for order in ["HOLD"] + [f"TARGET {t}" for t in grid]:
        c = tok(order, add_special_tokens=False)["input_ids"]
        x = torch.tensor([full + head + c], device=model.device)
        n0 = start + len(head)
        with torch.no_grad():
            logits = model(input_ids=x[:, n0 - 1:], past_key_values=copy.deepcopy(base), use_cache=True,
                           cache_position=torch.arange(n0 - 1, x.shape[1], device=model.device)).logits[0]
        # the input starts at the prompt's last token, so logits[j] predicts the order's token j
        lp = torch.log_softmax(logits[:-1].float(), -1)
        scores.append(float(sum(lp[j, c[j]] for j in range(len(c)))))
        along.append(goes_along(order, position, wants)[0])
    import math
    m = max(scores)
    w = [math.exp(v - m) for v in scores]
    p = sum(wi for wi, a in zip(w, along) if a) / sum(w)
    return (p, scores) if detail else p


_CONT = {}


def _continuations(tok):
    """Token ids that would continue a number: those starting with a digit (no space before it). The agents never
    write commas or decimal points in an order, and a full stop can end one ("TARGET -200000."), so those end it."""
    if id(tok) not in _CONT:
        _CONT[id(tok)] = [i for t, i in tok.get_vocab().items() if t[:1] in set("0123456789")]
    return _CONT[id(tok)]


def order_dist(model, tok, full, cache, lead, grid):
    """The agent's order after the decision prompt and a reasoning `lead`, as a distribution over HOLD and each size in
    `grid` (the review of 20 Oct fixed two faults of order_prob, kept as it was for the first steering run):
    - a positive size is scored in both ways the agents write it, "TARGET n" and "TARGET +n", summed;
    - each "TARGET n" is scored as a whole number: its probability times the chance the number ends there (the next
      token is not a digit), so "TARGET 50000" no longer also counts "TARGET 500000".
    Returns (orders, probabilities normalised over them, coverage = their summed probability before normalising)."""
    import math
    import torch
    head = tok("\n\n".join([lead.strip(), ""]) if lead else "", add_special_tokens=False)["input_ids"]
    base = copy.deepcopy(cache)
    ids = torch.tensor([full + head], device=model.device)
    k = cache.get_seq_length()
    with torch.no_grad():
        model(input_ids=ids[:, k:ids.shape[1] - 1], past_key_values=base, use_cache=True,
              cache_position=torch.arange(k, ids.shape[1] - 1, device=model.device))
    n0, cont = len(full) + len(head), _continuations(tok)

    def logp(text, whole_number):
        c = tok(text, add_special_tokens=False)["input_ids"]
        x = torch.tensor([full + head + c], device=model.device)
        with torch.no_grad():
            logits = model(input_ids=x[:, n0 - 1:], past_key_values=copy.deepcopy(base), use_cache=True,
                           cache_position=torch.arange(n0 - 1, x.shape[1], device=model.device)).logits[0].float()
        lp = torch.log_softmax(logits, -1)            # lp[j] predicts token j of the order; the last row, what follows
        total = float(sum(lp[j, c[j]] for j in range(len(c))))
        if whole_number:
            total += math.log(max(1e-12, 1 - float(lp[len(c), cont].exp().sum())))
        return total

    orders, mass = ["HOLD"] + list(grid), [math.exp(logp("HOLD", False))]
    for t in grid:
        forms = [f"TARGET {t}"] + ([f"TARGET +{t}"] if t > 0 else [])
        mass.append(sum(math.exp(logp(f, True)) for f in forms))
    total = sum(mass)
    return orders, [m / total for m in mass], total


def summarise_orders(orders, probs, position, wants=None):
    """From order_dist: P(the order goes along) (if `wants`), the expected size of the position it sets, and the chance
    it changes its position."""
    size = [abs(position) if o == "HOLD" else abs(o) for o in orders]
    change = [0.0 if o == "HOLD" else float(o != position) for o in orders]
    out = {"expected_size": sum(p * s for p, s in zip(probs, size)), "p_change": sum(p * c for p, c in zip(probs, change))}
    if wants:
        out["p_order_along"] = sum(p for o, p in zip(orders, probs)
                                   if goes_along("HOLD" if o == "HOLD" else f"TARGET {o}", position, wants)[0])
    return out
