"""Checks for sim/inside_careers.py: the chunked reading gives exactly the states of a plain full reading, at every
chosen position and layer (a tiny random Gemma 3, CPU). Run: python sim/test_inside_careers.py"""
import sys, torch
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
from inside_careers import Recorder, read
torch.manual_seed(0)
cfg = Gemma3TextConfig(vocab_size=300, hidden_size=64, intermediate_size=128, num_hidden_layers=6, num_attention_heads=4,
                       num_key_value_heads=2, head_dim=16, sliding_window=16, max_position_embeddings=4096)
m = Gemma3ForCausalLM(cfg).eval()
ids = torch.randint(5, 300, (1, 150)).tolist()[0]
want = [0, 7, 31, 32, 63, 100, 148, 149]
rec = Recorder(m)
got = read(m, ids, want, rec, chunk=32)
rec.remove()
full = []
hs = [m.model.layers]
outs = {}
hooks = [l.register_forward_hook(lambda mod, i, o, k=k: outs.__setitem__(k, (o[0] if isinstance(o, tuple) else o)[0].detach())) for k, l in enumerate(m.model.layers)]
with torch.no_grad():
    m(input_ids=torch.tensor([ids]))
worst = max((got[p][k] - outs[k][p]).abs().max().item() for p in want for k in range(len(m.model.layers)))
print("layers", len(m.model.layers), "| positions", want, "| largest difference chunked vs full:", worst)
assert worst < 1e-4
print("OK")
