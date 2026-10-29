"""Needs torch and transformers (CPU is enough): python sim/test_frame_state.py

Checks for the careers with the frame's state carried in (sim/frame_state.py, notebook 35), with no download:
1. the framed update: every UBS line of B's neutral career in the blame wording, nothing else changed;
2. the hook on a tiny random Gemma 3: chunked reading plus token-by-token writing with a kept segment and an open one
   gives the same reply and logits as one full read with both added by hand;
3. the measured state: the framed update's average minus the neutral one's, read in chunks after a steered history,
   equals a brute-force full read;
4. notebook 35's own cells over whole careers with a stand-in agent (no git, no GPU): 29 moments per career, each kept
   from its update to the next update, the random arm the same sizes in one direction, a career stopped partway and
   continued equal to one run straight through; then the analysis.
"""
import glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
import frame_state as F
from framing_set import read_set

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. the framed update, on B's neutral career 0
table = F.framed_lines(read_set(), "loss + you")
hist = json.load(open(f"{B}/careers/neutral_r0.json"))["history"]
blame_lines = {m.group(2) for p in glob.glob(f"{B}/careers/loss_plus_you_r*.json")
               for t in json.load(open(p))["history"] if t["role"] == "user" for m in F.UBS.finditer(t["content"])}
n_upd, n_lines, same_rest, in_blame = 0, 0, True, True
for t in hist:
    if t["role"] != "user":
        continue
    framed, n = F.framed_update(t["content"], table)
    if n:
        n_upd, n_lines = n_upd + 1, n_lines + n
        same_rest &= F.UBS.sub("", framed) == F.UBS.sub("", t["content"])
        in_blame &= all(m.group(2) in blame_lines for m in F.UBS.finditer(framed))
check(f"B's neutral career: {n_upd} updates with a UBS line, {n_lines} lines framed", (n_upd, n_lines) == (29, 58))
check("only UBS's lines change, and each framed line is one B's blame careers saw", same_rest and in_blame)
try:
    F.framed_update("New chat messages:\n  UBS [Agent A]: not a line of the file", table)
    check("a UBS line missing from the file stops the run", False)
except AssertionError:
    check("a UBS line missing from the file stops the run", True)

# ---- 2. the hook: a kept segment and an open one, chunked reading + writing == one full read by hand
torch.manual_seed(0)
W, L = 64, 3
cfg = Gemma3TextConfig(vocab_size=97, hidden_size=W, intermediate_size=128, num_hidden_layers=6, num_attention_heads=2,
                       num_key_value_heads=1, head_dim=32, sliding_window=16, max_position_embeddings=4096)
model = Gemma3ForCausalLM(cfg).eval()
layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
ids = torch.randint(0, 97, (1, 90))
segs = [(20, 41, torch.randn(W)), (61, None, torch.randn(W))]
new = 12
hook = F.Segments(layers[L])
hook.set(segs)
with torch.no_grad():
    g = model.generate(input_ids=ids, attention_mask=torch.ones_like(ids), max_new_tokens=new, do_sample=False,
                       prefill_chunk_size=16, disable_compile=True, output_scores=True, return_dict_in_generate=True)
steered = hook.steered
hook.set()
seq = g.sequences


def by_hand(module, args, output):
    h = output[0] if isinstance(output, tuple) else output
    add = torch.zeros_like(h)
    add[:, 20:41] += segs[0][2]
    add[:, 61:] += segs[1][2]
    return (h + add,) + tuple(output[1:]) if isinstance(output, tuple) else h + add


hh = layers[L].register_forward_hook(by_hand)
with torch.no_grad():
    ref = model(input_ids=seq[:, :-1]).logits[0]
hh.remove()
check(f"the reply written with the hook equals the one-pass reference ({new} tokens)", torch.equal(ref[89:].argmax(-1), seq[0, 90:]))
gap = (g.scores[-1][0] - ref[-1]).abs().max().item()
check(f"the last token's logits match the one-pass reference (largest gap {gap:.1e})", gap < 1e-3)
check(f"added at exactly the kept and open positions ({steered} = 21 + {90 - 61} read + {new - 1} written)",
      steered == 21 + (90 - 61) + new - 1)


# ---- 3. the measured state, against brute force (a Gemma-like template, one character per token)
class Tok:
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


tk = Tok()
turns = [{"role": "system", "content": "RULES"}, {"role": "user", "content": "first update"},
         {"role": "assistant", "content": "HOLD"}, {"role": "user", "content": "New chat messages:\n  UBS [Agent A]: hi"}]
framed = [dict(t) for t in turns]
framed[-1]["content"] = "New chat messages:\n  UBS [Agent A]: hi, and that is on you"
start = F.turn_start(tk, turns, 3)
check("the update starts where the conversation before it ends", start == len(tk.apply_chat_template(turns[:3])["input_ids"]))
kept = F.Segments(layers[L])
cap = F.Capture(layers[L])
vec0 = torch.randn(W)
kept.set([(3, 12, vec0)])                      # an earlier moment, kept while the history is read
got, s_after = F.frame_shift(model, tk, turns, framed, start, cap, chunk=8)
got_a, s_after2 = F.frame_shift(model, tk, turns, framed, start, cap, chunk=8, construction="after")


def brute_all(ts):
    x = torch.tensor([tk.apply_chat_template(ts, add_generation_prompt=True)["input_ids"]])
    keep = {}
    hh = layers[L].register_forward_hook(lambda m, a, o: keep.__setitem__("h", (o[0] if isinstance(o, tuple) else o)[0]))
    with torch.no_grad():
        model(input_ids=x)
    hh.remove()
    return keep["h"][start:].float().numpy()


def brute(ts):
    return brute_all(ts).mean(0)


want = brute(framed) - brute(turns)
kept.set()
check(f"the whole state equals a brute-force full read (largest gap {np.abs(got - want).max():.1e}, size {np.linalg.norm(want):.2f})",
      np.abs(got - want).max() < 1e-4 and np.linalg.norm(want) > 0)
ids_n = tk.apply_chat_template(turns, add_generation_prompt=True)["input_ids"]
ids_f = tk.apply_chat_template(framed, add_generation_prompt=True)["input_ids"]
s_want = F.common_suffix(ids_f, ids_n)
kept.set([(3, 12, vec0)])
want_a = brute_all(framed)[-s_want:].mean(0) - brute_all(turns)[-s_want:].mean(0)
kept.set()
check(f"the after state equals a brute-force read of the {s_want} shared tail tokens (largest gap {np.abs(got_a - want_a).max():.1e})",
      s_after == s_after2 == s_want and s_want >= 1 and np.abs(got_a - want_a).max() < 1e-4)
kept.handle.remove()
cap.handle.remove()
hook.handle.remove()

# ---- 4. notebook 35's own cells over whole careers, with a stand-in agent and a stand-in measurement
nb = json.load(open(f"{ROOT}/notebooks/35_frame_state_careers.ipynb"))
setup_cell, settings_cell, model_cell, memory_cell, agent_cell, run_cell, glance = \
    ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
repo = tempfile.mkdtemp()
for d in ("sim", "data", "designs", "notebooks"):
    os.symlink(f"{ROOT}/{d}", f"{repo}/{d}")
os.makedirs(f"{repo}/results")
shutil.copy(f"{ROOT}/results/full_career_pin.json", f"{repo}/results/")
real_system, real_sleep = os.system, __import__("time").sleep
os.system = lambda cmd: 0 if cmd.startswith("git ") else real_system(cmd)     # no git in the check
__import__("time").sleep = lambda s: None
torch.cuda.get_device_name = lambda i=0: "CPU (check)"
cwd = os.getcwd()
os.chdir(repo)
measured = []


def fake_shift(model, tok, turns, framed_turns, start, capture, chunk=4096, construction="whole"):
    # stand-in: a fixed vector for each framed update, so careers run twice give the same states
    measured.append(start)
    seed = int(hashlib.md5(framed_turns[-1]["content"].encode()).hexdigest()[:8], 16)
    return np.random.default_rng(seed).normal(size=W).astype(np.float32), 3


F.frame_shift = fake_shift
stop = {"at": None}
added = {"bad": 0, "calls": 0}


def chat(turns, **k):
    # stand-in for the pipeline: the hook is called the way a chunked read and a short reply call it
    full = tk.apply_chat_template(turns, add_generation_prompt=True)["input_ids"]
    if stop["at"] and stop["at"] in turns[-1]["content"] and g["CURRENT_ARM"] == VB:
        stop["at"] = None
        raise RuntimeError("stopped partway (the check)")
    segs = g["STEER"].segs
    if segs:
        end = len(full) + 3
        want = sum(max(0, min(e if e is not None else end, end) - s) for s, e, _ in segs)
        g["STEER"].steered = 0
        for s in range(0, end, 16384):
            e = min(s + 16384, end)
            g["STEER"]._hook(None, (), {"position_ids": torch.arange(s, e)[None]}, torch.zeros(1, e - s, W))
        added["bad"] += g["STEER"].steered != want
        added["calls"] += 1
    return [{"generated_text": turns + [{"role": "assistant", "content": "Watching the market.\nHOLD"}]}]


g = {"__name__": "__main__", "REPO": repo, "BRANCH": "check", "PIN": json.load(open("results/full_career_pin.json"))}
exec("import os, sys, json, glob, hashlib, time, datetime, torch", g)
exec(setup_cell[setup_cell.index("from mountain import"):], g)
exec(settings_cell, g)
VB, VR = g["VERSIONS"]                                 # the blame and random arms, as the settings name them
g2 = dict(g)
os.environ["RD2_SETTINGS"] = "L22x2"
try:
    exec(settings_cell, g2)
finally:
    del os.environ["RD2_SETTINGS"]
check("a Modal job's override: L22x2 sets the layer and the size, keeps the construction, names the folder and arms",
      (g2["LAYER"], g2["STRENGTH"], g2["CONSTRUCTION"]) == (22, 2.0, g["CONSTRUCTION"]) and g2["NAME"] == f"frame_state_{g['CONSTRUCTION']}_x2_L22"
      and all("x2 L22" in v for v in g2["VERSIONS"]) and 22 in g2["EXTRA_HASH"] and 2.0 in g2["EXTRA_HASH"])
slug = lambda v: v.replace(" + ", "_plus_").replace(" ", "_")
import transformers
mod = Gemma3ForCausalLM(Gemma3TextConfig(vocab_size=97, hidden_size=W, intermediate_size=128, num_hidden_layers=44,
                                         num_attention_heads=2, num_key_value_heads=1, head_dim=32, sliding_window=16))
g.update(mod=mod, tok=tk, chat=chat, transformers=transformers, np=np)
exec(agent_cell, g)
check(f"the hook and the capture sit on layer {g['LAYER']} ({g['CONSTRUCTION']}, x{g['STRENGTH']:g})",
      g["STEER"].handle is not None and g["CAPTURE"].handle is not None)
g["ROUNDS_HERE"] = [0]
stop["at"] = "2011-06-08"                       # the blame career stops on 8 June, after 1 April was saved
try:
    exec(run_cell, g)
    check("the career stopped partway", False)
except RuntimeError:
    out = g["OUT"]
    check("the career stopped partway, its last trading day and states saved",
          os.path.exists(f"{out}/partial/{slug(VB)}_r0.json") and os.path.exists(f"{out}/partial/{slug(VB)}_r0_moments.npz"))
before = len(measured)
saved_n = len(json.load(open(f"{out}/partial/{slug(VB)}_r0.json"))["frame_state"]["moments"])
g["ROUNDS_HERE"] = [0, 1]
exec(run_cell, g)
cs = {os.path.basename(p)[:-5]: json.load(open(p)) for p in glob.glob(f"{out}/careers/*.json")}
vs = {k: np.load(f"{out}/careers/{k}_moments.npz")["vecs"] for k in cs}
B0, B1, R0 = f"{slug(VB)}_r0", f"{slug(VB)}_r1", f"{slug(VR)}_r0"
check(f"four careers saved ({sorted(cs)}), 5 trading days each, no partial left",
      len(cs) == 4 and len(glob.glob(f"{out}/days/*.json")) == 20 and not os.listdir(f"{out}/partial"))
check("the stopped career, continued, equals the one run straight through (history, moments, states)",
      cs[B0]["history"] == cs[B1]["history"] and cs[B0]["frame_state"] == cs[B1]["frame_state"]
      and np.array_equal(vs[B0], vs[B1]))
c = cs[B1]
ms = c["frame_state"]["moments"]
check(f"29 moments, 58 UBS lines ({len(ms)}, {sum(m['lines'] for m in ms)})", len(ms) == 29 and sum(m["lines"] for m in ms) == 58)
opening = g["OPENING"]
ts = [{"role": "system", "content": opening}] + c["history"]
ups = [i for i, t in enumerate(ts) if t["role"] == "user" and not t["content"].startswith(F.NOTE)]
starts = [F.turn_start(tk, ts[:i + 1], i) for i in ups]
ok_spans = True
for m in ms:
    k = starts.index(m["start"])
    ok_spans &= bool(F.UBS.search(ts[ups[k]]["content"])) and m["end"] == (starts[k + 1] if k + 1 < len(starts) else None)
check("each moment starts at an update with a UBS line and is kept up to the next update", ok_spans)
check(f"the hook added exactly the kept and open positions at every steered reply ({added['calls']} replies checked)",
      added["bad"] == 0 and added["calls"] > 0)
n_rep = sum(t["role"] == "assistant" for t in c["history"])
first = next(i for i, t in enumerate(c["history"]) if t["role"] == "user" and F.UBS.search(t["content"]))
check(f"steered from the first UBS update on ({c['steered_replies']} of {n_rep} replies)",
      c["steered_replies"] == sum(t["role"] == "assistant" for t in c["history"][first:]))
r = vs[R0]
units = r / np.linalg.norm(r, axis=1, keepdims=True)
check("random: the blame state's sizes, moment by moment, in one direction",
      np.allclose(np.linalg.norm(r, axis=1), np.linalg.norm(vs[B0], axis=1), rtol=1e-5)
      and np.allclose(units, units[0], atol=1e-6))
check(f"the vectors added are {g['STRENGTH']:g} x the natural size, which each moment records",
      np.allclose(np.linalg.norm(vs[B0], axis=1), g["STRENGTH"] * np.array([m["size"] for m in ms]), rtol=1e-5)
      and all(m["after_tokens"] == 3 for m in ms) and c["frame_state"]["construction"] == g["CONSTRUCTION"])
check(f"each moment measured once; continued, only the moments after the last saved day again ({len(measured)} = "
      f"{before} before the stop + {29 - saved_n} + 3 x 29)", len(measured) == before + (29 - saved_n) + 3 * 29)
check("every arm's round k has B's neutral seed for round k",
      all(x["seed"] == int(hashlib.md5(f"B|neutral|{x['run']}".encode()).hexdigest()[:8], 16) for x in cs.values()))
day = json.load(open(f"{out}/days/{B0}_2011-08-05.json"))
check(f"each saved day records the arm, layer, construction, strength and the moments so far ({day['moments']} by 5 Aug; "
      "UBS's last chats come after it)", day["arm"] == VB and day["layer"] == g["LAYER"] and day["kind"] == "frame"
      and day["construction"] == g["CONSTRUCTION"] and day["strength"] == g["STRENGTH"]
      and 0 < day["moments"] < 29 and day["moment_sizes"] == [m["size"] for m in ms[:day["moments"]]])
check("the hooks are off after every reply", not g["STEER"].segs and not g["CAPTURE"].on)
os.chdir(cwd)
os.system = real_system
res = tempfile.mkdtemp()
r = subprocess.run([sys.executable, f"{ROOT}/designs/rd2/analysis/frame_state.py", out, res], capture_output=True, text=True)
md = open(f"{res}/FRAME_STATE.md").read() if r.returncode == 0 else r.stderr
check("the analysis runs on them (base, both arms, the yardstick, the states)",
      r.returncode == 0 and all(s in md for s in ("| B neutral", f"| {VB}", f"| {VR}", "| B blame", "| 29 |", g["CONSTRUCTION"])))
print(md[:2500])
shutil.rmtree(repo)
shutil.rmtree(res)
print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
