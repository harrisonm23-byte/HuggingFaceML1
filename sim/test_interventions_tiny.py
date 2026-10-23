"""Needs torch and transformers (CPU is enough): python sim/test_interventions_tiny.py

CPU check of the GPU code paths on a tiny random Gemma 3 (no download): order_dist against brute force, and the
cached tail read (prefill + Recorder offset) against one full read."""
import copy, math, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
from inside_careers import Recorder
from interventions import NEUTRAL_LEAD, order_dist, prefill, summarise_orders, goes_along

torch.manual_seed(0)
CHARS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:+-'?\n")


class Tok:
    def __init__(self):
        self.v = {c: i for i, c in enumerate(CHARS)}

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [self.v[c] for c in text]}

    def get_vocab(self):
        return dict(self.v)


tok = Tok()
cfg = Gemma3TextConfig(vocab_size=len(CHARS), hidden_size=64, intermediate_size=128, num_hidden_layers=6,
                       num_attention_heads=2, num_key_value_heads=1, head_dim=32, sliding_window=16,
                       max_position_embeddings=4096)
model = Gemma3ForCausalLM(cfg).eval()
print("layer types:", getattr(model.config, "layer_types", None))
full = tok("Time: 09:30 UTC. Silver 28.4. Your position: +0 oz. UBS: we push it down now, are you in?\n")["input_ids"] * 2
k = 70
cache = prefill(model, full[:k], chunk=32)

# 1. order_dist against a brute-force full forward (no cache) for every candidate
grid = [-100000, -50000, 0, 50000, 500000]
orders, probs, cover = order_dist(model, tok, full, cache, NEUTRAL_LEAD, grid)
head = tok(NEUTRAL_LEAD.strip() + "\n\n")["input_ids"]
cont = [tok.v[d] for d in "0123456789"]


def brute(text, whole):
    c = tok(text)["input_ids"]
    x = torch.tensor([full + head + c])
    with torch.no_grad():
        lp = torch.log_softmax(model(input_ids=x).logits[0].float(), -1)
    n0 = len(full) + len(head)
    t = sum(float(lp[n0 - 1 + j, c[j]]) for j in range(len(c)))
    if whole:
        t += math.log(1 - float(lp[n0 - 1 + len(c), cont].exp().sum()))
    return t


mass = [math.exp(brute("HOLD", False))] + [sum(math.exp(brute(f, True)) for f in ([f"TARGET {t}"] + ([f"TARGET +{t}"] if t > 0 else []))) for t in grid]
want = [m / sum(mass) for m in mass]
gap = max(abs(a - b) for a, b in zip(probs, want))
print(f"order_dist vs brute force: largest gap in probabilities {gap:.2e}; coverage {cover:.3e} vs {sum(mass):.3e}")
assert gap < 1e-4 and abs(cover - sum(mass)) / sum(mass) < 1e-3
# whole numbers: 'TARGET 50000' must not include 'TARGET 500000'
assert all(abs(p) <= 1 for p in probs) and abs(sum(probs) - 1) < 1e-9
o = summarise_orders(orders, probs, 0.0, "down")
print("summarise_orders:", {k2: round(v, 4) for k2, v in o.items()})
assert abs(o["p_order_along"] - sum(p for od, p in zip(orders, probs) if od != "HOLD" and od < 0)) < 1e-12

# 2. the cached tail read (as in scripts/modal_matched.py) against one full read, every layer
rec = Recorder(model)
last = len(full) - 1
rec.reset([last])
with torch.no_grad():
    model(input_ids=torch.tensor([full]))
ref = rec.states(last)
rec.reset([last])
rec.seen = [k] * len(rec.layers)
with torch.no_grad():
    model(input_ids=torch.tensor([full[k:]]), past_key_values=copy.deepcopy(cache), use_cache=True,
          cache_position=torch.arange(k, len(full)))
got = rec.states(last)
d = float((got - ref).abs().max() / ref.abs().max())
print(f"cached tail read vs full read: largest relative gap {d:.2e} over {len(rec.layers)} layers")
assert d < 1e-4
# 3. the cache handed to order_dist is not changed by it (later versions reuse it)
before = cache.get_seq_length()
order_dist(model, tok, full, cache, NEUTRAL_LEAD, grid)
assert cache.get_seq_length() == before == k
# 4. summarise_orders on a hand-made distribution
o = summarise_orders(["HOLD", -100000, 0, 50000], [0.1, 0.2, 0.3, 0.4], 0.0, "down")
assert abs(o["p_order_along"] - 0.2) < 1e-12 and abs(o["expected_size"] - 40000) < 1e-6 and abs(o["p_change"] - 0.6) < 1e-12
o = summarise_orders(["HOLD", -100000, 0, 50000, 100000], [0.1, 0.2, 0.2, 0.3, 0.2], 50000.0, "up")
assert abs(o["p_order_along"] - 0.2) < 1e-12 and abs(o["expected_size"] - (0.1 * 50000 + 0.2 * 100000 + 0.3 * 50000 + 0.2 * 100000)) < 1e-6
# 5. the A run's path: a shared cache extended by one forward (memo to moment), then the tail read
k0 = 40
shared = prefill(model, full[:k0], chunk=32)
c2 = copy.deepcopy(shared)
with torch.no_grad():
    model(input_ids=torch.tensor([full[k0:k]]), past_key_values=c2, use_cache=True, cache_position=torch.arange(k0, k))
rec.reset([last])
rec.seen = [k] * len(rec.layers)
with torch.no_grad():
    model(input_ids=torch.tensor([full[k:]]), past_key_values=copy.deepcopy(c2), use_cache=True,
          cache_position=torch.arange(k, len(full)))
d2 = float((rec.states(last) - ref).abs().max() / ref.abs().max())
o1, p1, _ = order_dist(model, tok, full, c2, NEUTRAL_LEAD, grid)
print(f"extended cache: state gap {d2:.2e}; order gap {max(abs(a - b) for a, b in zip(p1, probs)):.2e}")
assert d2 < 1e-4 and max(abs(a - b) for a, b in zip(p1, probs)) < 1e-4
print("ALL OK")
