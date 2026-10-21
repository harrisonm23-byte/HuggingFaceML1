"""What the author's emotion documents activate inside the model (exploratory; the user, 22 Oct). One GPU rereads each
document (designs/rd2/emotion_lists/*.txt, frozen), passes every token's state at layers 12, 24, 31 and 41 through the
Gemma Scope 2 dictionaries (16k) and keeps each feature's mean activation over the document's tokens; it also encodes
B's matched rereads at the same layers (UBS's loss vs gain request at the same moment). Then
`designs/rd2/analysis/emotion_features.py` lists the features each document type lights up, with Neuronpedia links, and
pushes results/emotion_lists/FEATURES.md.

    modal run --detach scripts/modal_emotion_features.py
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
OUT = "/states/v2/emotion/features.npz"
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]                 # the layers saved in the matched rereads

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-emotion-features", image=image)
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
def read_encode_analyse():
    import glob, hashlib, json, os, subprocess
    import numpy as np, torch
    repo = setup()
    states_vol.reload()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from gemma_scope import WANT_LAYERS, load_sae, sae_layers
    for f, h in FROZEN.items():                         # the author's files, unchanged since they were frozen
        assert hashlib.sha256(open(os.path.join(LISTS, f), "rb").read()).hexdigest() == h, f"{f} changed"
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
    files = sae_layers(len(layers))
    width = model.config.get_text_config().hidden_size
    saes = {}
    for L in WANT_LAYERS:
        We, b, t, _, _ = load_sae(files[L], width)
        t = np.zeros_like(b) if t is None else t
        saes[L] = [torch.tensor(a, device=model.device) for a in (We, b, t)]

    def enc(x, L):                                      # JumpReLU: a feature is on when it clears its threshold
        We, b, t = saes[L]
        pre = x @ We + b
        return torch.where(pre > t, pre, torch.zeros_like(pre))

    got = {}

    def hook(L):
        def h(module, inputs, output):
            got[L] = (output[0] if isinstance(output, tuple) else output)[0, 1:].float()   # leave out BOS
        return h
    for L in WANT_LAYERS:
        layers[L].register_forward_hook(hook(L))
    acts, meta = {L: [] for L in WANT_LAYERS}, []
    for f in FROZEN:
        docs = [d.strip() for d in open(os.path.join(LISTS, f), encoding="utf-8") if d.strip()]
        for i, d in enumerate(docs):
            with torch.no_grad():
                model(input_ids=tok(d, return_tensors="pt")["input_ids"].to(model.device))
            for L in WANT_LAYERS:
                a = enc(got[L], L)
                acts[L].append(torch.stack([a.mean(0), (a > 0).float().mean(0)]).cpu().numpy())   # mean, share of tokens on
            meta.append({"theme": f[:-4], "doc": i})
    # B's matched rereads (decision token; five framings x Bank C): encoded at the same layers
    ubs = {L: [] for L in WANT_LAYERS}
    umeta = []
    for p in sorted(glob.glob("/states/v2/matched/B_bf16/*.npz")):
        z = np.load(p)
        r = json.loads(str(z["meta"]))
        for L in WANT_LAYERS:
            x = torch.tensor(z["states"][:, KEEP.index(L)].astype(np.float32), device=model.device)
            ubs[L].append(enc(x, L).cpu().numpy())
        umeta.append([{"framing": m["framing"], "bank_c": m["bank_c"], "career_file": m["career_file"],
                       "coverage": m["coverage"]} for m in r])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    np.savez_compressed(OUT, **{f"doc_{L}": np.stack(acts[L]).astype(np.float32) for L in WANT_LAYERS},
                        **{f"ubs_{L}": np.stack(ubs[L]).astype(np.float32) for L in WANT_LAYERS},
                        meta=np.array(json.dumps(meta)), umeta=np.array(json.dumps(umeta)))
    states_vol.commit()
    subprocess.run(f"python designs/rd2/analysis/emotion_features.py {OUT} results/emotion_lists", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/emotion_lists && git -C {repo} commit -q -m 'What the emotion documents "
                       "activate'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "emotion feature results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.local_entrypoint()
def main():
    print(read_encode_analyse.remote())
