"""Needs torch and transformers (CPU is enough): python sim/test_state_careers.py

Checks for the careers with a document's state switched on (sim/state_careers.py, notebook 31), with no download:
1. the arms: names, sizes, random sizing, fingerprints, which scan a layer comes from, unscanned layers refused;
2. the hook on a tiny random Gemma 3: chunked reading plus token-by-token writing with the state added from the newest
   update on gives the same reply and the same final logits as one full read with the state added there by hand;
3. where the newest update starts, from the chat template;
4. notebook 31's own cells, run over a whole career per arm with a stand-in agent (no git, no GPU), then the analysis.
"""
import glob, json, os, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
import state_careers as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. the arms, from fake scan files shaped like the real ones (moments x themes x layers x width)
tmp = tempfile.mkdtemp()
W = 64
rng = np.random.default_rng(0)


def fake_scan(path, themes, layers, scale=1.0):
    os.makedirs(path, exist_ok=True)
    np.savez(f"{path}/shifts.npz", shifts=(rng.normal(size=(20, len(themes), len(layers), W)) * scale).astype(np.float32),
             runs=np.repeat(np.arange(10), 2), layers=np.array(layers), themes=np.array(themes), meta=np.array("[]"))


src = {"emotion": [f"{tmp}/e", f"{tmp}/e_sweep"], "financial": [f"{tmp}/f", f"{tmp}/f_sweep"]}
fake_scan(src["emotion"][0], ["loss", "blame", "gain", "credit"], [1, 2, 3, 4])
fake_scan(src["emotion"][1], ["loss", "blame", "gain", "credit"], [2, 4], scale=5.0)
fake_scan(src["financial"][0], ["loss", "gain"], [1, 2, 3, 4], scale=2.0)
arms = S.build_arms("loss@3,blame@3,random@3,fin:loss@3,fin:random@3,gain@4,none", 2, src)
check("arm names: " + ", ".join(arms), list(arms) == ["loss x2 L3", "blame x2 L3", "random x2 L3", "fin loss x2 L3",
                                                       "fin random x2 L3", "gain x2 L4", "none"])
z = np.load(f"{src['emotion'][0]}/shifts.npz")
pooled = z["shifts"].astype(np.float64).mean(0)[0, 2]          # loss, layer 3: the mean over all 20 moments
check("a state is the mean over every scanned moment, at 2 x its own length",
      np.allclose(arms["loss x2 L3"]["vec"], 2 * pooled, atol=1e-5) and abs(arms["loss x2 L3"]["size"] - np.linalg.norm(pooled)) < 1e-6)
e_sizes = [np.linalg.norm(z["shifts"].astype(np.float64).mean(0)[a, 2]) for a in range(4)]
check("random: as long as the set's states at that layer on average (x2), sized on its own document set",
      abs(np.linalg.norm(arms["random x2 L3"]["vec"]) - 2 * np.mean(e_sizes)) < 1e-4
      and arms["fin random x2 L3"]["source"].startswith(src["financial"][0]))
check("the same arm gives the same vector and fingerprint every time",
      S.build_arms("random@3", 2, src)["random x2 L3"]["sha"] == arms["random x2 L3"]["sha"]
      and S.build_arms("loss@3", 2, src)["loss x2 L3"]["sha"] == arms["loss x2 L3"]["sha"])
check("a layer in both scans comes from the confirmation scan", arms["gain x2 L4"]["source"].startswith(src["emotion"][0] + "/"))
for bad, why in (("loss@5", "unscanned layer"), ("fin:blame@3", "no financial blame"), ("loss21", "bad spelling"),
                 ("loss@3,loss@3", "listed twice")):
    try:
        S.build_arms(bad, 2, src)
        check(f"refused: {why}", False)
    except (AssertionError, ValueError):
        check(f"refused: {why}", True)
check("none adds nothing", arms["none"]["vec"] is None and arms["none"]["sha"] == "none")
check("on every reply, or trading days only",
      S.steer_on("every", "2007-08-22", ["2011-01-07"]) and S.steer_on("trading", "2011-01-07", ["2011-01-07"])
      and not S.steer_on("trading", "2007-08-22", ["2011-01-07"]) and not S.steer_on("trading", None, ["2011-01-07"]))

# ---- 2. the hook on a tiny Gemma 3: chunked reading + writing == one full read with the state added by hand
torch.manual_seed(0)
cfg = Gemma3TextConfig(vocab_size=97, hidden_size=W, intermediate_size=128, num_hidden_layers=6, num_attention_heads=2,
                       num_key_value_heads=1, head_dim=32, sliding_window=16, max_position_embeddings=4096)
model = Gemma3ForCausalLM(cfg).eval()
layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
ids = torch.randint(0, 97, (1, 90))
start, L, new = 61, 3, 12
vec = torch.tensor(arms["loss x2 L3"]["vec"])
hook = S.ArmSteer(layers[L])
hook.set(vec, start)
with torch.no_grad():
    g = model.generate(input_ids=ids, attention_mask=torch.ones_like(ids), max_new_tokens=new, do_sample=False,
                       prefill_chunk_size=16, disable_compile=True, output_scores=True, return_dict_in_generate=True)
steered = hook.steered
hook.set(None)
hook.handle.remove()
seq = g.sequences


def by_hand(module, args, output):
    h = output[0] if isinstance(output, tuple) else output
    add = torch.zeros_like(h)
    add[:, start:] = vec
    return (h + add,) + tuple(output[1:]) if isinstance(output, tuple) else h + add


hh = layers[L].register_forward_hook(by_hand)
with torch.no_grad():
    ref = model(input_ids=seq[:, :-1]).logits[0]
hh.remove()
check(f"the reply written with the hook equals the one-pass reference ({new} tokens)",
      torch.equal(ref[89:].argmax(-1), seq[0, 90:]))
gap = (g.scores[-1][0] - ref[-1]).abs().max().item()
check(f"the last token's logits match the one-pass reference (largest gap {gap:.1e})", gap < 1e-3)
check(f"the state was added to exactly the tokens from the update on ({steered} = {90 - start} read + {new - 1} written)",
      steered == 90 - start + new - 1)
with torch.no_grad():
    plain = model.generate(input_ids=ids, attention_mask=torch.ones_like(ids), max_new_tokens=new, do_sample=False,
                           disable_compile=True)
check("with the hook off the model is untouched, and on it changes the reply", not torch.equal(plain, seq))


# ---- 3. where the newest update starts (a Gemma-like template, one character per token)
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
        return {"input_ids": [ord(ch) for ch in text]}

    def __call__(self, text, **k):
        return {"input_ids": [ord(ch) for ch in text]}


tk = Tok()
turns = [{"role": "system", "content": "RULES"}, {"role": "user", "content": "update one"},
         {"role": "assistant", "content": "HOLD"}, {"role": "user", "content": "update two"}]
n, total = S.update_start(tk, turns)
text = "".join(map(chr, tk.apply_chat_template(turns, add_generation_prompt=True)["input_ids"]))
check(f"the newest update starts where the conversation without it ends: {text[n:]!r}", text[n:] == "<user>\nupdate two<end>\n<model>\n")
check("the first update (instructions alone do not render): from the start", S.update_start(tk, turns[:2])[0] == 0)

# ---- 4. notebook 31's own cells over whole careers, with a stand-in agent (holds; sometimes rambles), then the analysis
nb = json.load(open(f"{ROOT}/notebooks/31_state_careers.ipynb"))
setup_cell, settings_cell, model_cell, memory_cell, agent_cell, run_cell, glance = \
    ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
repo = tempfile.mkdtemp()
for d in ("sim", "data", "designs", "notebooks"):
    os.symlink(f"{ROOT}/{d}", f"{repo}/{d}")
os.makedirs(f"{repo}/results")
shutil.copy(f"{ROOT}/results/full_career_pin.json", f"{repo}/results/")
os.symlink(f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2", f"{repo}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
real_system, real_sleep = os.system, __import__("time").sleep
os.system = lambda cmd: 0 if cmd.startswith("git ") else real_system(cmd)     # no git in the check
__import__("time").sleep = lambda s: None
torch.cuda.get_device_name = lambda i=0: "CPU (check)"
cwd = os.getcwd()
os.chdir(repo)
info = S.build_arms("loss@3,random@3,none", 2, src)
calls = {"on": 0, "off": 0, "added": 0}


class Hidden:                                          # what the hook sees: (1, tokens, width)
    shape = (1, 0, W)


def chat(turns, **k):
    # stand-in for the pipeline: the hook is called the way a chunked read and a short reply call it
    full = tk.apply_chat_template(turns, add_generation_prompt=True)["input_ids"]
    for h in HOOKS.values():
        if h.vec is not None:
            for s in range(0, len(full) + 3, 4096):
                e = min(s + 4096, len(full) + 3)
                out = h._hook(None, (), {"position_ids": torch.arange(s, e)[None]}, torch.zeros(1, e - s, W))
                calls["added"] += int((out.abs().sum(-1) > 0).sum())
    on = any(h.vec is not None for h in HOOKS.values())
    calls["on" if on else "off"] += 1
    return [{"generated_text": turns + [{"role": "assistant", "content": "Watching the market.\nHOLD"}]}]


g = {"__name__": "__main__", "REPO": repo, "BRANCH": "check", "PIN": json.load(open("results/full_career_pin.json")),
     "ARM_INFO": info, "WHEN": "every", "SPAN": "update"}
exec("import os, sys, json, glob, hashlib, time, datetime, torch", g)
exec(setup_cell[setup_cell.index("from mountain import"):], g)
exec(settings_cell, g)
g["ROUNDS_HERE"] = [0, 1]
import transformers
mod = Gemma3ForCausalLM(Gemma3TextConfig(vocab_size=97, hidden_size=W, intermediate_size=128, num_hidden_layers=6,
                                         num_attention_heads=2, num_key_value_heads=1, head_dim=32, sliding_window=16))
g.update(mod=mod, tok=tk, chat=chat, transformers=transformers)
exec(agent_cell, g)
HOOKS = g["HOOKS"]
check("one hook, at the arms' layer (3)", list(HOOKS) == [3])
exec(run_cell, g)
out = g["OUT"]
cs = {os.path.basename(p): json.load(open(p)) for p in glob.glob(f"{out}/careers/*.json")}
check(f"two careers per arm saved ({len(cs)}), 5 trading days each",
      len(cs) == 6 and len(glob.glob(f"{out}/days/*.json")) == 30)
check("every arm's round k has B's neutral seed for round k",
      all(c["seed"] == int(__import__("hashlib").md5(f"B|neutral|{c['run']}".encode()).hexdigest()[:8], 16) for c in cs.values()))
replies = {v: [c["steered_replies"] for c in cs.values() if c["version"] == v] for v in info}
n_replies = sum(1 for t in cs["none_r0.json"]["history"] if t["role"] == "assistant")
check(f"the state was on for every reply of the state and random careers ({replies['loss x2 L3']}, {replies['random x2 L3']}"
      f" of {n_replies}) and never for none ({replies['none']})",
      replies["loss x2 L3"] == [n_replies] * 2 and replies["random x2 L3"] == [n_replies] * 2 and replies["none"] == [0, 0])
day = json.load(open(glob.glob(f"{out}/days/loss_x2_L3_r0_2011-01-07.json")[0]))
check("each saved day records the arm, layer, strength, size and fingerprint",
      day["arm"] == "loss x2 L3" and day["layer"] == 3 and day["strength"] == 2 and day["arm_sha"] == info["loss x2 L3"]["sha"])
check("the hooks are off after every reply", all(h.vec is None for h in HOOKS.values()))
# a saved career with a different state for the same arm stops the run
bad = dict(info)
bad["loss x2 L3"] = dict(info["loss x2 L3"], sha="different")
g["ARM_INFO"] = bad
try:
    exec(run_cell, g)
    check("a career saved with another state for the same arm stops the run", False)
except AssertionError:
    check("a career saved with another state for the same arm stops the run", True)
os.chdir(cwd)
os.system = real_system
r = subprocess.run([sys.executable, f"{ROOT}/designs/rd2/analysis/state_careers.py", out, f"{tmp}/res"], capture_output=True, text=True)
md = open(f"{tmp}/res/STATE_CAREERS.md").read() if r.returncode == 0 else r.stderr
check("the analysis runs on them (arms, request by request, breakage, B's yardstick)",
      r.returncode == 0 and all(s in md for s in ("| loss x2 L3 | 2 |", "| none |", "Request by request", "yardstick")))
print(md[:1500])
shutil.rmtree(tmp)
shutil.rmtree(repo)
print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
