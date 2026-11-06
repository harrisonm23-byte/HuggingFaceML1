"""The author's emotion lists, read by the model, on Modal (exploratory; the user, 21 Oct). One GPU reads each document
(designs/rd2/emotion_lists/*.txt, one document per line, frozen) and keeps, at every layer, the mean state over its
tokens and its last token; then `designs/rd2/analysis/emotion_lists.py` compares the emotion directions with the frame
directions from UBS's lines (the matched rereads) and pushes results/emotion_lists/EMOTION.md.

    modal run --detach scripts/modal_emotion.py
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
LISTS = "designs/rd2/emotion_lists"
FROZEN = {"loss.txt": "ad106b2c76d2075adf38f3efc01a3c7c551e84a663b43255ac73ca8e95d8a5e6",
          "blame.txt": "448e76cae16ceb96d01cd11288b32fbaaf7c1f567c16b9a3896dc26b953feb32",
          "gain.txt": "e9aa8b85169dff39d11706ab75d2efdb4cf664b4cf5cd31ea591a0b44d718d16",
          "credit.txt": "28e16297b8c5fb9053da680fc1116ccac549b3c047b5235e234ee63665eb056f",
          "neutral.txt": "d6952221565fb8d8854e35ce3f609ef9ee89894540ea659577b15a48087b9019"}
OUT = "/states/v2/emotion/states.npz"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-emotion", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def setup():
    import os, subprocess, sys
    repo = "/root/HuggingFaceML1"
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    for c in ("git config --global credential.helper store", 'git config --global user.name "Modal job"',
              'git config --global user.email "harrisonm23-byte@users.noreply.github.com"'):
        subprocess.run(c, shell=True, check=True)
    if not os.path.exists(repo):
        subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH}", shell=True)
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "sim"))
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    return repo


@app.function(gpu="H100", timeout=2 * 3600, secrets=SECRETS, volumes=VOLUMES)
def read_and_analyse():
    import hashlib, json, os, subprocess
    import numpy as np, torch
    repo = setup()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    files = {f: os.path.join(LISTS, f) for f in FROZEN}
    if os.path.exists(os.path.join(LISTS, "neutral.txt")):
        files["neutral.txt"] = os.path.join(LISTS, "neutral.txt")
    for f, path in files.items():                       # the author's files, unchanged since they were frozen
        if f in FROZEN:
            assert hashlib.sha256(open(path, "rb").read()).hexdigest() == FROZEN[f], f"{f} changed since it was frozen"
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
    got = {}

    def hook(k):
        def h(module, inputs, output):
            x = (output[0] if isinstance(output, tuple) else output)[0].float()
            got[k] = (x[1:].mean(0).cpu().numpy(), x[-1].cpu().numpy())   # the mean leaves out the first (BOS) token
        return h

    for k, layer in enumerate(layers):
        layer.register_forward_hook(hook(k))
    means, lasts, meta = [], [], []
    for f, path in files.items():
        docs = [d.strip() for d in open(path, encoding="utf-8") if d.strip()]
        for i, d in enumerate(docs):
            ids = tok(d, return_tensors="pt")["input_ids"].to(model.device)
            with torch.no_grad():
                model(input_ids=ids)
            means.append(np.stack([got[k][0] for k in range(len(layers))]))
            lasts.append(np.stack([got[k][1] for k in range(len(layers))]))
            meta.append({"theme": f[:-4], "doc": i, "tokens": int(ids.shape[1])})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    np.savez_compressed(OUT, states_mean=np.stack(means).astype(np.float32), states_last=np.stack(lasts).astype(np.float32),
                        meta=np.array(json.dumps(meta)))
    states_vol.commit()
    subprocess.run(f"python designs/rd2/analysis/emotion_lists.py {OUT} /states/v2/matched/B_bf16 /states/v2/B_bf16 "
                   "results/emotion_lists", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/emotion_lists && git -C {repo} commit -q -m 'Emotion lists against the frame'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "emotion results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.local_entrypoint()
def main():
    print(read_and_analyse.remote())
