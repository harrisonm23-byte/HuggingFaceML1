"""Needs torch and transformers (CPU is enough; downloads the two models' tokenizers, a few MB, no weights):
python sim/test_other_models.py [folder with qwen/ and nemo/ tokenizer files, to skip the download]

Checks for sim/other_models.py and the "model=" path of scripts/modal_careers.py:
1. the settings and the pins (same libraries as Gemma's pin, a full revision);
2. the templates on a real career's conversation: Nemo's instructions at the start of the first message as Gemma lays
   them out (not before the newest message), Qwen's think block closed in the prompt, the adaptation idempotent;
3. the pipeline the notebooks use (text-generation, chat turns) reaches the model with the adapted prompt, on tiny
   random copies of both architectures with the real tokenizers;
4. notebook 19's setup and settings cells as the Modal job runs them: the pin swapped, the versions filtered, the setup
   ID's extra inputs extended, Gemma's path unchanged.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
import transformers
from transformers import AutoTokenizer, pipeline
import other_models as O
from career import career_opening

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
LOCAL = sys.argv[1] if len(sys.argv) > 1 else None
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. settings and pins
check("parse: model and versions", O.parse("model=qwen3.5-9b&versions=neutral;loss_plus_you")
      == {"model": "qwen3.5-9b", "versions": ["neutral", "loss + you"]})
check("parse: notebook 35's settings are left alone", O.parse("L16x2-loss") == {})
base = json.load(open(f"{ROOT}/results/full_career_pin.json"))
for key in O.MODELS:
    p = O.pin(key)
    check(f"{key}: pin has a full revision and Gemma's library versions",
          len(p["model_revision"]) == 40 and all(p[k] == base[k] for k in ("transformers", "accelerate", "bitsandbytes")))

# ---- 2. templates on a real career
repo = {"qwen3.5-9b": O.pin("qwen3.5-9b")["model"], "mistral-nemo-12b": O.pin("mistral-nemo-12b")["model"]}
local = {"qwen3.5-9b": "qwen", "mistral-nemo-12b": "nemo"}
toks = {k: AutoTokenizer.from_pretrained(os.path.join(LOCAL, local[k]) if LOCAL else repo[k],
                                         revision=None if LOCAL else O.pin(k)["model_revision"]) for k in O.MODELS}
career = json.load(open(f"{B}/careers/neutral_r0.json"))
OPEN = career_opening()
turns = [{"role": "system", "content": OPEN}] + career["history"][:9]
raw_nemo = toks["mistral-nemo-12b"].apply_chat_template(turns, add_generation_prompt=True, tokenize=False)
check("Nemo's own template puts the instructions late (the reason for merge_system)", raw_nemo.find(OPEN[:60]) > 1000)
for k in O.MODELS:
    O.adapt(toks[k], k)
    O.adapt(toks[k], k)                                   # twice: no double wrapping
nemo = toks["mistral-nemo-12b"].apply_chat_template(turns, add_generation_prompt=True, tokenize=False)
check("Nemo adapted: the instructions open the first message, a blank line, then its first update",
      nemo.startswith("<s>[INST]" + OPEN + "\n\n" + career["history"][0]["content"]) and nemo.count(OPEN[:60]) == 1)
qwen = toks["qwen3.5-9b"].apply_chat_template(turns, add_generation_prompt=True, tokenize=False)
check("Qwen adapted: the instructions (trimmed, as Gemma's template also trims) as the system message at the top, the think block closed",
      qwen.startswith("<|im_start|>system\n" + OPEN.strip() + "<|im_end|>") and qwen.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"))
check("a caller's own keyword still wins", toks["qwen3.5-9b"].apply_chat_template(
      turns, add_generation_prompt=True, tokenize=False, enable_thinking=True).endswith("<think>\n"))
check("the caller's turns are not changed", turns[0]["role"] == "system" and turns[1] == career["history"][0])

# ---- 3. the notebooks' pipeline reaches the model with the adapted prompt (tiny random models, real tokenizers)
from transformers import MistralConfig, MistralForCausalLM
from transformers.models.qwen3_5.configuration_qwen3_5 import Qwen3_5TextConfig
from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5ForCausalLM
torch.manual_seed(0)
tiny = {
    "mistral-nemo-12b": MistralForCausalLM(MistralConfig(vocab_size=len(toks["mistral-nemo-12b"]), hidden_size=32,
                                                         intermediate_size=64, num_hidden_layers=2, num_attention_heads=2,
                                                         num_key_value_heads=1, head_dim=16, max_position_embeddings=8192)),
    "qwen3.5-9b": Qwen3_5ForCausalLM(Qwen3_5TextConfig(vocab_size=len(toks["qwen3.5-9b"]), hidden_size=32, intermediate_size=64,
                                                       num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=1,
                                                       head_dim=16, layer_types=["linear_attention", "full_attention"],
                                                       linear_num_value_heads=2, linear_num_key_heads=1, linear_key_head_dim=16,
                                                       linear_value_head_dim=16, max_position_embeddings=8192)),
}
short = [{"role": "system", "content": OPEN}] + career["history"][:3]
for k, model in tiny.items():
    model.eval()
    seen = []
    h = model.get_input_embeddings().register_forward_hook(lambda m, i, o: seen.append(i[0][0].tolist()))
    chat = pipeline("text-generation", model=model, tokenizer=toks[k])
    out = chat(short, max_new_tokens=3, do_sample=False, prefill_chunk_size=256, disable_compile=True)
    h.remove()
    want = toks[k].apply_chat_template(short, add_generation_prompt=True, return_dict=True)["input_ids"]
    prompt = [t for ids in seen for t in ids][:len(want)]
    check(f"{k}: the pipeline's prompt is the adapted template, read in chunks", prompt == list(want) and len(seen) > 2)
    check(f"{k}: the reply comes back as the notebooks read it", out[0]["generated_text"][-1]["role"] == "assistant")

# ---- 4. notebook 19's cells as the Modal job runs them
nb = json.load(open(f"{ROOT}/notebooks/19_ubs_framing_careers.ipynb"))
setup_cell, settings_cell = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"][:2]


def job_globals(settings):
    other = O.parse(settings)
    cwd = os.getcwd()
    os.chdir(ROOT)
    g = {"__name__": "__main__"}
    exec("import os, sys, json, glob, hashlib, time, datetime, torch", g)
    g.update(REPO=ROOT, BRANCH="x", PIN=O.pin(other["model"]) if other else json.load(open("results/full_career_pin.json")))
    exec(setup_cell[setup_cell.index("from mountain import"):], g)
    exec(settings_cell, g)
    if other:
        if "versions" in other:
            g["VERSIONS"] = other["versions"]
        g["EXTRA_HASH"] = g["EXTRA_HASH"] + O.setup_hash(other["model"])
    os.chdir(cwd)
    return g


gem = job_globals("")
nem = job_globals("model=mistral-nemo-12b&versions=neutral")
check("Gemma's path: its pin, all five versions, the setup inputs as before",
      gem["MODEL"] == "google/gemma-3-12b-it" and len(gem["VERSIONS"]) == 5 and len(gem["EXTRA_HASH"]) == 2)
check("Nemo's job: its model and revision, only the neutral version, its pin and adaptation in the setup inputs",
      nem["MODEL"] == "mistralai/Mistral-Nemo-Instruct-2407" and nem["REVISION"] == O.pin("mistral-nemo-12b")["model_revision"]
      and nem["VERSIONS"] == ["neutral"] and nem["EXTRA_HASH"][2:] == O.setup_hash("mistral-nemo-12b"))
folder = lambda g: "full_career_" + g["MODEL"].split("/")[-1] + "_4bit_" + g["NAME"] + "_v2"
check(f"its own results folder ({folder(nem)})", folder(nem) != folder(gem) and folder(gem) ==
      "full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
