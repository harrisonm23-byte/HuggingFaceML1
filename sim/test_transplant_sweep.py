"""Needs torch and transformers (CPU is enough; python-docx for the framing file): python sim/test_transplant_sweep.py

Checks for the frame's state at every layer (sim/transplant_sweep.py), with no download:
1. the conditions, the random directions and the vectors' sizes;
2. common_suffix and shifts() on made-up readings;
3. run_item on a tiny random Gemma 3 with a Gemma-like template (one character per token), at B's real 7 January
   request (the update alone, after short instructions): one row per condition, the "after" state against a brute-force
   full read, the steer on only for the condition's layer and off after, done rows skipped, and the saved vectors;
4. the analysis on those rows.
"""
import glob, json, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
import transplant_sweep as T
from framing_set import read_set
from inside_careers import moments
from interventions import ORDER_GRID, SIGN, Steer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. conditions and vectors
conds = T.conditions()
check(f"{len(conds)} conditions: none and the framed words first, seven per layer", len(conds) == 2 + 7 * len(T.LAYERS)
      and conds[0][1] == "none" and conds[1][1] == "framed")
W = 64
units = T.random_units(W, T.LAYERS)
check("one unit direction per layer, the same every time",
      all(abs(np.linalg.norm(u) - 1) < 1e-6 for u in units.values()) and np.allclose(T.random_units(W)[18], units[18]))
rng = np.random.default_rng(0)
sh = {"whole": {L: rng.normal(size=W).astype(np.float32) * 3 for L in T.LAYERS},
      "after": {L: rng.normal(size=W).astype(np.float32) for L in T.LAYERS}}
check("whole x1 is the whole state; after x2 twice the after state",
      np.allclose(T.vector("whole", 18, 1, sh, units), sh["whole"][18]) and np.allclose(T.vector("after", 18, 2, sh, units), 2 * sh["after"][18]))
check("the random controls are as long as what they stand in for, along the layer's direction",
      abs(np.linalg.norm(T.vector("random_whole", 18, 1, sh, units)) - np.linalg.norm(sh["whole"][18])) < 1e-4
      and abs(np.linalg.norm(T.vector("random_after", 18, 2, sh, units)) - 2 * np.linalg.norm(sh["after"][18])) < 1e-4
      and np.allclose(T.vector("random_after", 18, 2, sh, units) / np.linalg.norm(T.vector("random_after", 18, 2, sh, units)), units[18]))
check("none and framed add nothing", T.vector("none", None, 0, sh, units) is None and T.vector("framed", None, 0, sh, units) is None)

# ---- 2. common_suffix and shifts
check("common_suffix: an insertion in the middle keeps the shared tail", T.common_suffix([1, 2, 3, 9, 9, 4, 5], [1, 2, 3, 4, 5]) == 2)
check("common_suffix: a tail that matches by chance does not reach back before the first difference",
      T.common_suffix([1, 2, 3], [1, 7, 3]) == 1)
n = {L: rng.normal(size=(10, W)) for L in [4]}
f = {L: rng.normal(size=(13, W)) for L in [4]}
s4 = T.shifts(n, f, 3, [4])
check("shifts: whole is the difference of the two means; after, of the last s tokens' means",
      np.allclose(s4["whole"][4], f[4].mean(0) - n[4].mean(0), atol=1e-5)
      and np.allclose(s4["after"][4], f[4][-3:].mean(0) - n[4][-3:].mean(0), atol=1e-5))


# ---- 3. run_item on a tiny model, B's real 7 January request
class Tok:
    def apply_chat_template(self, turns, add_generation_prompt=False, return_dict=False, tokenize=True):
        text = "^"
        for t in turns:
            text += f"<{ {'system': 'sys', 'user': 'user', 'assistant': 'model'}[t['role']] }>\n{t['content']}<end>\n"
        text += "<model>\n" if add_generation_prompt else ""
        return {"input_ids": [ord(ch) % 97 for ch in text]}

    def __call__(self, text, **k):
        return {"input_ids": [ord(ch) % 97 for ch in text]}

    def get_vocab(self):
        return {chr(i): i for i in range(97)}


tk = Tok()
torch.manual_seed(0)
LAYERS = [4, 18, 42]
cfg = Gemma3TextConfig(vocab_size=97, hidden_size=W, intermediate_size=128, num_hidden_layers=44, num_attention_heads=2,
                       num_key_value_heads=1, head_dim=32, sliding_window=16, max_position_embeddings=8192)
model = Gemma3ForCausalLM(cfg).eval()
layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
steers = {L: Steer(layers[L]) for L in LAYERS}
capture = T.Capture({L: layers[L] for L in LAYERS})
units = T.random_units(W, LAYERS)
chats = read_set()
items = [{**m, "position": m["held_their_way"] * SIGN[m["wants"]]} for m in moments(B, "B")
         if m["version"] == "neutral" and m["date"] in T.DATES]
check(f"B's neutral careers at 7 and 12 January: {len(items)} moments", len(items) == 20)
item = sorted(items, key=lambda m: (m["career_file"], m["history_index"]))[0]
real = json.load(open(f"{B}/careers/{item['career_file']}"))
career = {**real, "history": [real["history"][item["history_index"]]]}      # the request's update alone, after RULES
item = {**item, "history_index": 0}
saved = []
rows = list(T.run_item(model, tk, steers, capture, units, item, career, chats, "RULES", "", ORDER_GRID, layers=LAYERS,
                       save=lambda sh, meta: saved.append((sh, meta))))
names = [c[0] for c in T.conditions(LAYERS)]
check(f"one row per condition ({len(rows)}), in order", [r["condition"] for r in rows] == names)
check("the vectors were measured and saved once, with tokens after the framed words",
      len(saved) == 1 and saved[0][1]["after_tokens"] >= 1 and saved[0][1]["extra_tokens"] > 0
      and all(r["after_tokens"] == saved[0][1]["after_tokens"] for r in rows))
sh, meta = saved[0]
# brute force: both prompts read whole, the layer's output kept, the shared tail compared
from inside_careers import encode, turns_at
from matched import matched
full = encode(tk, turns_at(career, 0, "RULES"))
framed = encode(tk, turns_at(matched(career, 0, item["date"], "neutral", T.FROM, chats), 0, "RULES"))
s = T.common_suffix(framed, full)
_, k = __import__("interventions").split_point(tk, career, 0, "RULES")


def states(seq, L):
    keep = {}
    hh = layers[L].register_forward_hook(lambda m, a, o: keep.__setitem__("h", (o[0] if isinstance(o, tuple) else o)[0]))
    with torch.no_grad():
        model(input_ids=torch.tensor([seq]))
    hh.remove()
    return keep["h"][k:].float().numpy()


a, b = states(framed, 18), states(full, 18)
gap_a = np.abs(sh["after"][18] - (a[-s:].mean(0) - b[-s:].mean(0))).max()
gap_w = np.abs(sh["whole"][18] - (a.mean(0) - b.mean(0))).max()
check(f"the saved states equal a brute-force full read (largest gaps {gap_w:.1e} whole, {gap_a:.1e} after; {s} tokens after)",
      gap_a < 1e-3 and gap_w < 1e-3)
by = {r["condition"]: r for r in rows}
check("shift sizes: whole x1 and random (whole size) equal; after x2 twice after x1",
      abs(by["whole x1 L18"]["shift_size"] - by["random, whole size, L18"]["shift_size"]) < 1e-3
      and abs(by["after x2 L18"]["shift_size"] - 2 * by["after x1 L18"]["shift_size"]) < 1e-3 and by["none"]["shift_size"] == 0)
check("every row has a distribution over the orders (coverage in (0, 1], probabilities summing to 1, P(along) in [0, 1])",
      all(0 < r["coverage"] <= 1 + 1e-6 and abs(sum(r["probs"]) - 1) < 1e-6 and 0 <= r["p_order_along"] <= 1 for r in rows))
check("adding a state changes the distribution; the framed words read differently from the neutral ones",
      by["whole x1 L18"]["probs"] != by["none"]["probs"] and by["framed (loss + you), as read"]["probs"] != by["none"]["probs"])
check("the steers are off after the run", all(st.vec is None for st in steers.values()) and not capture.on)
again = list(T.run_item(model, tk, steers, capture, units, item, career, chats, "RULES", "", ORDER_GRID,
                        done={r["key"] for r in rows}, layers=LAYERS))
check("rows already done are skipped", again == [])

# ---- 4. the analysis on these rows
tmp = tempfile.mkdtemp()
os.makedirs(f"{tmp}/src/shifts")
with open(f"{tmp}/src/part0.jsonl", "w") as fh:
    for r in rows:
        fh.write(json.dumps(r) + "\n")
    r2 = {**rows[0], "career_file": "neutral_r1.json", "key": "other|0|none"}
    fh.write(json.dumps(r2) + "\n")
np.savez(f"{tmp}/src/shifts/m.npz", layers=np.array(LAYERS), whole=np.stack([sh["whole"][L] for L in LAYERS]),
         after=np.stack([sh["after"][L] for L in LAYERS]), meta=np.array(json.dumps(meta)))
src = open(f"{ROOT}/designs/rd2/analysis/transplant_sweep.py").read().replace("from transplant_sweep import LAYERS, conditions",
                                                                                  f"LAYERS = {LAYERS}").replace(
    '["coverage"] >= 0.5', '["coverage"] >= 0.0')          # a tiny random model gives the orders little probability
open(f"{tmp}/analysis.py", "w").write(src)
r = subprocess.run([sys.executable, f"{tmp}/analysis.py", f"{tmp}/src", f"{tmp}/out"], capture_output=True, text=True)
md = open(f"{tmp}/out/TRANSPLANT_SWEEP.md").read() if r.returncode == 0 else r.stderr
check("the analysis runs: a row per layer, the sizes table, the base and the framed words",
      r.returncode == 0 and all(f"| {L} |" in md for L in LAYERS) and "cosine" in md and "Nothing added:" in md)
print(md[:1200])
shutil.rmtree(tmp)
print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
