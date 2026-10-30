"""Needs torch and transformers (CPU is enough): python sim/test_attention_you.py

Checks for sim/attention_you.py, with no download:
1. the spans at B's 300 saved requests in all five framings: every UBS line found, its neutral core opening the framed
   line, "you" in the extra for blame and credit only;
2. the token groups with a one-character tokenizer on a real update: a partition of the prompt, the "you" tokens
   spelling "you";
3. the tap on a tiny random Gemma 3 (eager attention): masses sum to 1 per head and row, and the cached reading of the
   update gives the decision token the same masses as one full reading;
4. run_moment end to end on the tiny model: shapes, NaN for "into you" where the framing has no "you".
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
import attention_you as A
from framing_set import FRAMINGS, read_set
from inside_careers import moments, turns_at
from interventions import prefill, split_point
from matched import matched

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


chats = read_set()
# ---- 1. spans at every saved request, every framing
ms = moments(B, "B")
check(f"B's saved requests: {len(ms)}", len(ms) == 300)
counts = {v: {"lines": 0, "prefix": 0, "you_extra": 0, "moments_with_you": 0, "you_core": 0} for v in FRAMINGS}
for m in ms:
    career = json.load(open(f"{B}/careers/{m['career_file']}"))
    for v in FRAMINGS:
        upd = matched(career, m["history_index"], m["date"], m["version"], v, chats)["history"][m["history_index"]]["content"]
        sp = A.line_spans(upd, m["date"], v, chats)
        c = counts[v]
        c["lines"] += len(sp)
        c["prefix"] += sum(s["core_is_prefix"] for s in sp)
        c["you_extra"] += sum(len(s["you_extra"]) for s in sp)
        c["you_core"] += sum(len(s["you_core"]) for s in sp)
        c["moments_with_you"] += any(s["you_extra"] for s in sp)
for v in FRAMINGS:
    c = counts[v]
    print(f"     {v}: {c['lines']} UBS lines, core opens the line in {c['prefix']}; \"you\" in the extra {c['you_extra']} "
          f"({c['moments_with_you']} of 300 moments), in the core {c['you_core']}")
odd = sorted({(m["date"], v) for m in ms for v in FRAMINGS
              for s_ in A.line_spans(matched(json.load(open(f"{B}/careers/{m['career_file']}")), m["history_index"], m["date"],
                                             m["version"], v, chats)["history"][m["history_index"]]["content"], m["date"], v, chats)
              if not s_["core_is_prefix"]})
print("     lines whose framed text does not open with the neutral core (date, framing):", odd)
check("where the core does not open the line, the shared opening is still most of the core",
      all(counts[v]["prefix"] >= counts[v]["lines"] - 50 for v in FRAMINGS))
check("\"you\" in the extra at every blame and credit moment, never under neutral, loss or gain",
      counts["loss + you"]["moments_with_you"] == 300 and counts["gain + you"]["moments_with_you"] == 300
      and all(counts[v]["you_extra"] == 0 for v in ("neutral", "loss", "gain")))
check("the neutral core's own \"you\" is the same in every framing", len({counts[v]["you_core"] for v in FRAMINGS}) == 1)


# ---- 2. token groups with a one-character tokenizer, on a real update (the request's update alone, after RULES)
class Tok:
    def apply_chat_template(self, turns, add_generation_prompt=False, return_dict=False, tokenize=True):
        text = "^"
        for t in turns:
            text += f"<{ {'system': 'sys', 'user': 'user', 'assistant': 'model'}[t['role']] }>\n{t['content']}<end>\n"
        text += "<model>\n" if add_generation_prompt else ""
        if not tokenize:
            return text
        return {"input_ids": [ord(ch) % 97 for ch in text]}

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False, **k):
        out = {"input_ids": [ord(ch) % 97 for ch in text]}
        if return_offsets_mapping:
            out["offset_mapping"] = [(i, i + 1) for i in range(len(text))]
        return out


tk = Tok()
blame = [m for m in ms if m["version"] == "loss + you" and m["chat"] == "p344_i_can_hunt_with_u"][0]
real = json.load(open(f"{B}/careers/{blame['career_file']}"))
career = {**real, "history": real["history"][blame["history_index"] - 2:blame["history_index"] + 1]}  # a short history
m0 = {**blame, "history_index": 2}
turns = turns_at(career, 2, "RULES")
text = tk.apply_chat_template(turns, add_generation_prompt=True, tokenize=False)
ids, groups, before = A.token_groups(tk, turns, 2, m0["date"], "loss + you", chats)
check("groups partition the prompt", sorted(i for g in groups.values() for i in g) == list(range(len(ids))))
check("the \"you\" tokens spell you", all(text[i].lower() in "your'esvld" for i in groups["you_extra"] + groups["you_core"])
      and "".join(text[i] for i in groups["you_extra"]).lower().startswith("you"))
check("the history is everything before the update", "".join(text[i] for i in groups["history"]).endswith("<user>\n")
      and text[groups["update_rest"][0]:groups["update_rest"][0] + 5] == career["history"][2]["content"][:5])
check("the extra before \"you\" is the loss statement", all(before[y] and max(before[y]) < y for y in groups["you_extra"]))
print("     groups:", {g: len(v) for g, v in groups.items()})

# ---- 3 and 4. the tap on a tiny random Gemma 3 with eager attention
torch.manual_seed(0)
cfg = Gemma3TextConfig(vocab_size=97, hidden_size=32, intermediate_size=64, num_hidden_layers=6, num_attention_heads=2,
                       num_key_value_heads=1, head_dim=16, sliding_window=64, max_position_embeddings=8192,
                       attn_implementation="eager")
model = Gemma3ForCausalLM(cfg).eval()
tap = A.Tap(model)
check(f"one tap per layer ({len(tap.attn)})", len(tap.attn) == cfg.num_hidden_layers)
full, k = split_point(tk, career, 2, "RULES")
check("the templated ids equal the module's", full == ids)
last = len(ids) - 1
rows = [last] + groups["you_extra"]
per_row = [[groups[g] for g in A.DECISION_GROUPS]] + [[groups["history"], groups["update_rest"],
            sorted(set(groups["core_other"]) | set(groups["you_core"])), before[y], list(range(y, len(ids)))]
           for y in groups["you_extra"]]
tap.arm(rows, 0)
with torch.no_grad():
    model(input_ids=torch.tensor([ids]))
whole = tap.masses(per_row)
check("masses sum to 1 over the groups, every layer, head and row", np.allclose(whole.sum(-1), 1.0, atol=1e-3))
tap.off()
cache = prefill(model, ids[:k])
tap.arm(rows, k)
with torch.no_grad():
    model(input_ids=torch.tensor([ids[k:]]), past_key_values=cache, use_cache=True,
          cache_position=torch.arange(k, len(ids)))
cached = tap.masses(per_row)
check("the cached reading gives the same masses as one full reading", np.allclose(whole, cached, atol=2e-3))
hist = whole[:, :, 0, A.DECISION_GROUPS.index("history")]
check("a local layer's decision token gives the far history nothing (window 64) and a global layer gives it something",
      hist[0].max() < 1e-6 and hist[5].max() > 0.01)
dec, into, meta = A.run_moment(model, tk, tap, career, m0, chats, "RULES", FRAMINGS, prefill)
check("run_moment: one row per framing, masses [framings x layers x heads x groups]",
      dec.shape == (5, 6, 2, len(A.DECISION_GROUPS)) and into.shape == (5, 6, 2, len(A.INTO_YOU_GROUPS))
      and [r["framing"] for r in meta] == FRAMINGS)
check("decision masses sum to 1; \"into you\" is NaN only without a \"you\" in the extra",
      np.allclose(dec.sum(-1), 1.0, atol=1e-3) and np.isnan(into[[0, 1, 2]]).all() and np.isfinite(into[[3, 4]]).all()
      and np.allclose(np.nansum(into[[3, 4]], -1), 1.0, atol=1e-3))
check("the blame reading matches the direct tap", np.allclose(dec[3], whole[:, :, 0, :], atol=2e-3))
# ---- 5. the analysis on files shaped like the real ones
import subprocess, tempfile
tmp = tempfile.mkdtemp()
os.makedirs(f"{tmp}/attention_you"); os.makedirs(f"{tmp}/matched/B_bf16")
rng = np.random.default_rng(0)
for cf in ("neutral_r0.json", "loss_plus_you_r1.json"):
    for chat in ("p344_i_can_hunt_with_u", "p316_bust_through_it"):
        d = rng.random((5, 6, 2, len(A.DECISION_GROUPS))).astype(np.float32); d /= d.sum(-1, keepdims=True)
        iy = rng.random((5, 6, 2, len(A.INTO_YOU_GROUPS))).astype(np.float32); iy /= iy.sum(-1, keepdims=True)
        iy[:3] = np.nan
        meta = [{"framing": v, "tokens": 900, "update_start": 700, "career_file": cf, "chat": chat, "history_index": 9,
                 "history": "neutral" if cf.startswith("neutral") else "loss + you",
                 "saved_joined": False, **{f"n_{g}": 3 for g in A.DECISION_GROUPS}} for v in FRAMINGS]
        np.savez_compressed(f"{tmp}/attention_you/{cf[:-5]}__{chat}.npz", decision=d, into_you=iy,
                            decision_groups=np.array(A.DECISION_GROUPS), into_you_groups=np.array(A.INTO_YOU_GROUPS),
                            layer_types=np.array(cfg.layer_types), meta=np.array(json.dumps(meta)))
        mm = [{"framing": v, "bank_c": b, "career_file": cf, "chat": chat, "p_order_along": float(rng.random())}
              for v in FRAMINGS for b in (False, True)]
        np.savez_compressed(f"{tmp}/matched/B_bf16/{cf[:-5]}__{chat}.npz", states=np.zeros((10, 1, 4), np.float32),
                            meta=np.array(json.dumps(mm)))
r = subprocess.run([sys.executable, f"{ROOT}/designs/rd2/analysis/attention_you.py", tmp, f"{tmp}/out"], capture_output=True, text=True)
check("the analysis runs on files shaped like the real ones", r.returncode == 0 and os.path.exists(f"{tmp}/out/ATTENTION_YOU.md"))
if r.returncode:
    print(r.stderr[-1500:])
else:
    text = open(f"{tmp}/out/ATTENTION_YOU.md").read()
    line = [l for l in text.splitlines() if l.startswith("| Neutral |")][0]
    shares = [float(x.strip().rstrip("%")) for x in line.split("|")[2:-1]]
    check(f"a framing's shares sum to 100 ({sum(shares):.1f})", abs(sum(shares) - 100) < 0.3)
    check("the link to the decision is reported", "| Blame: \"you\" mass (all layers)" in text)

# ---- 6. the chat-only days
cms = A.chat_moments(B)
per = {}
for m in cms:
    per[m["career_file"]] = per.get(m["career_file"], 0) + 1
check(f"chat-only-day updates with a UBS line: {len(cms)}, 17 in every career", len(cms) == 850 and set(per.values()) == {17})
check("their dates are the chats' own dates in the file", {m["date"] for m in cms} <= {c["date"] for c in chats})
counts2 = {v: {"lines": 0, "you_extra": 0, "you_core": 0, "extra": 0, "core_found": 0} for v in FRAMINGS}
agent_b = 0
cache = {}
for m in cms:
    c = cache.setdefault(m["career_file"], json.load(open(f"{B}/careers/{m['career_file']}")))
    for v in FRAMINGS:
        upd = A.framed(c, m["history_index"], m["date"], m["version"], v, chats)["history"][m["history_index"]]["content"]
        agent_b += v == "neutral" and "UBS [Agent B]:" in upd
        for sp in A.line_spans(upd, m["date"], v, chats):
            k = counts2[v]
            k["lines"] += 1; k["you_extra"] += len(sp["you_extra"]); k["you_core"] += len(sp["you_core"])
            k["extra"] += bool(sp["extra"]); k["core_found"] += sp["core_words_found"] >= 0.6
for v in FRAMINGS:
    print(f"     chat days, {v}: {counts2[v]}")
check(f"UBS's Agent B lines are swapped too ({agent_b} neutral-framed updates hold one)", agent_b == 50)
check("every framed line has a framed part; the neutral lines none",
      counts2["neutral"]["extra"] == 0 and all(counts2[v]["extra"] == counts2[v]["lines"] for v in FRAMINGS[1:]))
check("\"you\" in the framed part only under blame and credit; UBS's own \"you\" the same in every framing",
      counts2["loss"]["you_extra"] == counts2["gain"]["you_extra"] == 0 and counts2["loss + you"]["you_extra"] > 0
      and counts2["gain + you"]["you_extra"] > 0 and len({counts2[v]["you_core"] for v in FRAMINGS}) == 1)
check("most of UBS's line is found in every framed line (a rewrite keeps at least 60% of it, except 11 May's)",
      all(counts2[v]["core_found"] >= counts2[v]["lines"] - 100 for v in FRAMINGS))
# a rewritten line split word by word
mask = A.core_mask("Hallelujah. Let's push it up.", "We're not saved yet. Let's push it up. If you ease off now, we both walk out with nothing.")
line = "We're not saved yet. Let's push it up. If you ease off now, we both walk out with nothing."
kept = "".join(ch if x else "_" for ch, x in zip(line, mask))
check(f"a rewritten line: the shared words are UBS's, the rest framed ({kept[:40]}...)",
      "Let's_push_it_up." in kept and "We're" not in kept and "saved" not in kept and "If you ease off" not in kept)
# run_moment on a chat-day moment, the tiny model, a short history
m = [x for x in cms if x["version"] == "loss + you" and x["date"] == "2011-03-31"][0]
real = json.load(open(f"{B}/careers/{m['career_file']}"))
short_c = {**real, "history": real["history"][m["history_index"] - 2:m["history_index"] + 1]}
dec2, into2, meta2 = A.run_moment(model, tk, tap, short_c, {**m, "history_index": 2}, chats, "RULES", FRAMINGS, prefill)
check("run_moment on a chat-only day: masses sum to 1, \"into you\" only under blame and credit",
      np.allclose(dec2.sum(-1), 1.0, atol=1e-3) and np.isnan(into2[[0, 1, 2]]).all() and np.isfinite(into2[[3, 4]]).all())
r = subprocess.run([sys.executable, f"{ROOT}/designs/rd2/analysis/attention_you.py", tmp, f"{tmp}/out_chat", "--chat"],
                   capture_output=True, text=True) if os.rename(f"{tmp}/attention_you", f"{tmp}/attention_you_chat") is None else None
check("the chat analysis runs and reports the words link", r.returncode == 0 and "agreed in words" in open(f"{tmp}/out_chat/ATTENTION_YOU.md").read()
      if r.returncode == 0 else print(r.stderr[-1200:]))

tap.remove()
print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
