"""Dimension 2339 on unrelated prompts (the author, 13 Nov, Phase II D). 20 short prompts with nothing to do with
trading (weather, recipes, code, ...), read once by Gemma 3 12B (bf16, the pinned revision) in the chat template; the
residual stream after decoder layers 12 and 24 (the layers our episode states use) at every token. Reports dimension
2339 at the last token (the position our episode states are read at), at the first token and over the rest, and the
next-largest dimension, for comparison with the episodes (layer 12 about 8,500, layer 24 about 72,000 at the decision
token). No generation. H100, 20-minute timeout, no retries.

    modal run results/features_13nov/modal_dim2339_unrelated.py
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
image = (modal.Image.debian_slim(python_version="3.13").apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-dim2339-unrelated", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
DIM, LAYERS = 2339, (12, 24)
PROMPTS = [
    "What will the weather be like in Seattle this weekend?",
    "Is it going to rain in London tomorrow afternoon?",
    "Give me a simple recipe for banana bread.",
    "How long should I boil an egg for a soft yolk?",
    "What can I cook with chickpeas, spinach and garlic?",
    "Write a Python function that reverses a string.",
    "Explain what a for loop does in JavaScript.",
    "Fix this code: def add(a, b) return a + b",
    "How do I center a div in CSS?",
    "What is the capital of Australia?",
    "Tell me a short story about a cat who learns to swim.",
    "Write a haiku about autumn leaves.",
    "How many planets are in the solar system?",
    "What are some good exercises for lower back pain?",
    "Translate 'good morning, how are you?' into Spanish.",
    "Recommend three classic novels for a long flight.",
    "How does photosynthesis work, in two sentences?",
    "What is the difference between a violin and a viola?",
    "Plan a one-day itinerary for visiting Kyoto.",
    "Why is the sky blue?",
]


@app.function(gpu="H100", timeout=20 * 60, retries=0, secrets=SECRETS, volumes={"/root/.cache/huggingface": weights})
def run():
    import json, os, subprocess
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} /root/r", shell=True, check=True)
    pin = json.load(open("/root/r/results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
    assert len(layers) == 48
    got = {}
    hooks = [layers[L].register_forward_hook(lambda m, i, o, L=L: got.__setitem__(L, (o[0] if isinstance(o, tuple) else o)[0].float().cpu()))
             for L in LAYERS]
    rows = []
    for p in PROMPTS:
        ids = tok.apply_chat_template([{"role": "user", "content": p}], add_generation_prompt=True, return_tensors="pt")
        ids = ids["input_ids"] if hasattr(ids, "keys") else ids
        with torch.no_grad():
            model(input_ids=ids.to(model.device))
        r = {"prompt": p, "tokens": int(ids.shape[1])}
        for L in LAYERS:
            h = got[L]                                       # tokens x width
            last = h[-1]
            other = last.abs().clone(); other[DIM] = 0
            r[str(L)] = {"last": float(last[DIM]), "first": float(h[0, DIM]),
                         "rest_median": float(h[1:, DIM].median()), "rest_max": float(h[1:, DIM].abs().max()),
                         "next_largest_last": float(other.max()), "next_largest_dim": int(other.argmax())}
        rows.append(r)
        print(json.dumps(r), flush=True)
    for hk in hooks:
        hk.remove()
    return rows


@app.local_entrypoint()
def main():
    import json, os
    rows = run.remote()
    os.makedirs("results/features_13nov", exist_ok=True)
    json.dump(rows, open("results/features_13nov/dim2339_unrelated.json", "w"), indent=1)
    print("saved results/features_13nov/dim2339_unrelated.json")
