"""Needs torch and transformers (CPU is enough), from the repo root: python sim/test_persistence.py

Checks for the persistence check (sim/persistence.py) on a tiny random Gemma 3 (layers 0-4 see 16 tokens back, layer 5
sees everything, as Gemma 3 mixes them) and a short made-up career:
1. the pushed moment is found: the first 7 January update and the reply under it, exactly;
2. one reading of the whole career gives the same state at each decision as reading that moment's prompt alone, with
   and without the push;
3. the push changes nothing before the pushed moment, nothing at or below its own layer after it, and, far from it,
   reaches a later decision only through the layer that sees the whole conversation;
4. run_career end to end: an imprint per later update above the push's layer, orders at the key moments, the
   full-attention layers recorded.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
import persistence as P
from inside_careers import Recorder, encode, positions, read, turns_at
from state_careers import ArmSteer

ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


class Tok:                                               # a Gemma-like template, one character per token (mod 97)
    def apply_chat_template(self, turns, add_generation_prompt=False, return_dict=False, tokenize=True):
        sys_ = turns[0]["content"] if turns and turns[0]["role"] == "system" else None
        rest = turns[1:] if sys_ is not None else turns
        if sys_ is not None and not rest:
            raise ValueError("instructions alone")
        text = "^"
        for i, t in enumerate(rest):
            c = (sys_ + "\n\n" + t["content"]) if i == 0 and sys_ else t["content"]
            text += f"<{'model' if t['role'] == 'assistant' else 'user'}>\n{c}<end>\n"
        text += "<model>\n" if add_generation_prompt else ""
        return {"input_ids": [ord(ch) % 97 for ch in text]}

    def __call__(self, text, **k):
        return {"input_ids": [ord(ch) % 97 for ch in text]}

    def get_vocab(self):
        return {chr(c): c % 97 for c in range(32, 127)}


tok = Tok()
torch.manual_seed(0)
model = Gemma3ForCausalLM(Gemma3TextConfig(vocab_size=97, hidden_size=64, intermediate_size=128, num_hidden_layers=6,
                                           num_attention_heads=2, num_key_value_heads=1, head_dim=32, sliding_window=16,
                                           max_position_embeddings=8192)).eval()
check(f"tiny model: layer types {model.config.layer_types}", model.config.layer_types[-1] == "full_attention")

# a short career: one chat day, then 7 Jan (pushed at 08:00) and 12 Jan, with long enough updates that later ones sit
# far beyond the 16-token window of every short-range layer below the full-attention one
pad = "market quiet; " * 6
obs = {("2011-01-07", t): f"Time: {t} UTC, 2011-01-07. Silver 28.{i}0. {pad}" for i, t in enumerate(["08:00", "08:15", "09:45"])}
obs.update({("2011-01-12", t): f"Time: {t} UTC, 2011-01-12. Silver 29.{i}0. {pad}" for i, t in enumerate(["08:00", "09:30"])})
history = [{"role": "user", "content": "2010-11-02 chat: UBS [Agent A]: morning"}, {"role": "assistant", "content": "Noted."}]
for (d, t), o in obs.items():
    history += [{"role": "user", "content": ("MEMO: neutral.\n\n" if t == "08:00" and d == "2011-01-07" else "") + o},
                {"role": "assistant", "content": f"Watching {t}.\nHOLD"}]
career = {"history": history}
day = lambda d, times, msg: {"date": d, "summary": {"slope": {"message": msg}, "book_stops": [["Client A", 1.0, 1, "sell"]]},
                             "steps": [{"time": t, "observation": obs[(d, t)], "position": 0} for t in times]}
days = [day("2011-01-07", ["08:00", "08:15", "09:45"], None), day("2011-01-12", ["08:00", "09:30"], {"wants": "up"})]
opening = "You are a trading agent."

# ---- 1. the pushed moment
r0, r1 = P.region(tok, career, opening)
text = "".join(chr(c) for c in encode(tok, turns_at(career, len(history) - 2, opening)))   # chars mod 97: compare by ids
ids = encode(tok, turns_at(career, len(history) - 2, opening))
seg_expected = tok.apply_chat_template([{"role": "system", "content": "x"}, {"role": "user", "content": "y"}])["input_ids"]
pushed_user = [ord(ch) % 97 for ch in "<user>\n" + history[2]["content"] + "<end>\n<model>\nWatching 08:00.\nHOLD<end>\n"]
check(f"the pushed moment is the first 7 January update with the memo and the reply under it ({r1 - r0} tokens)",
      ids[r0:r1] == pushed_user)
ms = P.moments(career, days)
check(f"later updates: {[(m['date'], m['time'], m['key']) for m in ms]}",
      [(m["date"], m["time"]) for m in ms] == [("2011-01-07", "08:15"), ("2011-01-07", "09:45"), ("2011-01-12", "08:00"),
                                               ("2011-01-12", "09:30")] and [m["key"] for m in ms] == [False, True, True, True]
      and [m["wants"] for m in ms] == ["down", "down", "up", "up"])

# ---- 2 and 3. one reading against each prompt alone; where the push can show
L = 1
steers = {L: ArmSteer([m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")][L])}
rec = Recorder(model)
full, pos, prompts = positions(tok, career, [m["history_index"] for m in ms], opening)
vec = torch.randn(64) * 8
res = {}
for name, v in (("none", None), ("push", vec)):
    steers[L].set(v, r0, r1)
    res[name] = read(model, full, sorted(set(pos) | {r0 - 1, r1 - 1}), rec)
    alone = [read(model, prompts[k], [len(prompts[k]) - 1], rec)[len(prompts[k]) - 1] for k in range(len(ms))]
    steers[L].set(None)
    check(f"{name}: one reading of the whole career gives each decision's state as its prompt alone does",
          all(torch.allclose(res[name][p], a, atol=1e-4) for p, a in zip(pos, alone)))
d = {p: (res["push"][p] - res["none"][p]).abs().amax(-1) for p in res["none"]}
check("nothing changes before the pushed moment", float(d[r0 - 1].max()) == 0.0)
check(f"at the pushed moment the push shows from its own layer up ({[round(float(x), 2) for x in d[r1 - 1]]})",
      float(d[r1 - 1][:L].max()) == 0.0 and float(d[r1 - 1][L:].min()) > 0)
far = [p for p in pos if p - r1 > 16 * 4]
check(f"far later ({[p - r1 for p in far]} tokens on), nothing at or below the push's layer, nothing in the short-range layers "
      f"above it, and a change at the full-attention layer: {[[round(float(x), 3) for x in d[p]] for p in far]}",
      far and all(float(d[p][:5].max()) == 0.0 and float(d[p][5]) > 0 for p in far))

# ---- 4. run_career end to end
from interventions import NEUTRAL_LEAD
out = P.run_career(model, tok, career, days, opening, {"none": None, "push x8 L1": (L, vec.numpy()), "random L1": (L, (torch.randn(64) * 8).numpy())},
                   steers, rec, layers=list(range(6)), lead=NEUTRAL_LEAD, grid=[0, 10, -10])
row = out["moments"][-1]
check(f"run_career: imprints above the push's layer only ({sorted(row['arms']['push x8 L1'])}), orders at the key moments, "
      f"full-attention layers {out['full_attention_layers']}",
      sorted(k for k in row["arms"]["push x8 L1"] if k != "orders") == ["2", "3", "4", "5"]
      and "orders" in row["arms"]["push x8 L1"] and "orders_none" in row and "orders" not in out["moments"][0]["arms"]["push x8 L1"]
      and out["full_attention_layers"] == [5] and out["region"] == [r0, r1])
far_row = row["arms"]["push x8 L1"]
check(f"at the invitation, far from the push: share of the imprint left by layer {[(k, round(v['left'], 3)) for k, v in far_row.items() if k != 'orders']}",
      far_row["4"]["left"] == 0.0 and far_row["5"]["left"] > 0)
import json, subprocess, tempfile
tmp = tempfile.mkdtemp()
for k in range(2):                                      # two "careers" for the summary
    json.dump({**out, "folder": "results/check", "strength": 8, "career": f"none_r{k}"}, open(f"{tmp}/none_r{k}.json", "w"))
r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                  "designs/rd2/analysis/persistence.py"), tmp], capture_output=True, text=True)
md = open(f"{tmp}/PERSISTENCE.md").read() if r.returncode == 0 else r.stderr
check("the summary runs: imprint tables by push layer, and the orders at the key moments",
      r.returncode == 0 and "## Pushed at layer 1: what is left at layer 5" in md and "| 2011-01-12 09:30 | push x8 L1 |" in md)
print(md[:1500])
print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
