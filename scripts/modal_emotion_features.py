"""What the author's emotion documents activate inside the model (exploratory; the user, 22 Oct). One GPU rereads each
document (designs/rd2/emotion_lists/*.txt, frozen), passes every token's state at layers 12, 24, 31 and 41 through the
Gemma Scope 2 dictionaries (16k) and keeps each feature's mean activation over the document's tokens; it also encodes
B's matched rereads at the same layers (UBS's loss vs gain request at the same moment). It also places each document
inside B's neutral careers, just before UBS's request (as in the priming run), and keeps the features while the agent
reads it and at its decision afterwards, plus the raw decision state (layers 12, 18, 24, 31). Then
`designs/rd2/analysis/emotion_features.py` lists the features each document type lights up, with Neuronpedia links, and
pushes results/emotion_lists/FEATURES.md.

    modal run --detach scripts/modal_emotion_features.py
    modal run --detach scripts/modal_emotion_features.py --doc-set financial   # the financial documents instead
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
SETS = {"emotion": ("/states/v2/emotion/features.npz", "results/emotion_lists"),
        "financial": ("/states/v2/financial/features.npz", "results/financial_docs")}
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]                 # the layers saved in the matched rereads

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
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


@app.function(gpu="H100", memory=65536, timeout=3 * 3600, secrets=SECRETS, volumes=VOLUMES)
def read_encode_analyse(doc_set="emotion"):
    import glob, hashlib, json, os, subprocess
    import numpy as np, torch
    repo = setup()
    states_vol.reload()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from gemma_scope import WANT_LAYERS, load_sae, sae_layers
    import fin_docs
    OUT, RES = SETS[doc_set]
    lists, frozen = (LISTS, FROZEN) if doc_set == "emotion" else \
        (fin_docs.LISTS, {f"{t}.txt": h for t, h in fin_docs.FROZEN.items()})
    for f, h in frozen.items():                         # the author's files, unchanged since they were frozen
        assert hashlib.sha256(open(os.path.join(lists, f), "rb").read()).hexdigest() == h, f"{f} changed"
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
            got[L] = (output[0] if isinstance(output, tuple) else output)[0].float()
        return h
    RAW = [12, 18, 24, 31]                              # raw decision states kept here (24: the going-along direction)
    for L in sorted(set(WANT_LAYERS) | set(RAW)):
        layers[L].register_forward_hook(hook(L))
    acts, meta = {L: [] for L in WANT_LAYERS}, []
    for f in frozen:
        docs = [d.strip() for d in open(os.path.join(lists, f), encoding="utf-8") if d.strip()]
        for i, d in enumerate(docs):
            with torch.no_grad():
                model(input_ids=tok(d, return_tensors="pt")["input_ids"].to(model.device))
            for L in WANT_LAYERS:
                a = enc(got[L][1:], L)                  # leave out BOS
                acts[L].append(torch.stack([a.mean(0), (a > 0).float().mean(0)]).cpu().numpy())   # mean, share of tokens on
            meta.append({"theme": f[:-4], "doc": i})
    # The same documents read by the agent itself: inside B's neutral careers, at each of their 60 requests, placed at the
    # start of the request's update as in the priming run (sim/prime.py), so "you" and "we" are the agent and its desk.
    # Kept: the features while it reads the document (mean over the document's tokens), and at its decision afterwards
    # (the last token before its reply), with no document as the comparison.
    import copy
    import prime as P
    from career import career_opening
    from inside_careers import encode, moments, turns_at
    from interventions import SIGN, prefill, split_point
    docs = P.read_docs() if doc_set == "emotion" else fin_docs.read_docs()
    opening = career_opening()
    folder = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
    items = P.work_items(folder, moments, SIGN)
    THEMES = ["none"] + (["neutral", "loss", "blame", "gain", "credit"] if doc_set == "emotion" else fin_docs.THEMES)
    incar = {L: [] for L in WANT_LAYERS}                 # moments x 5 themes x features (reading the document)
    decide = {L: [] for L in WANT_LAYERS}                # moments x 6 (none + 5 themes) x features (at the decision)
    raw = {L: [] for L in RAW}                           # moments x 6 x width: the raw decision state
    cmeta, clean, total = [], 0, 0
    for n, item in enumerate(items):
        career = json.load(open(f"{folder}/careers/{item['career_file']}"))
        idx = item["history_index"]
        plain, k = split_point(tok, career, idx, opening)
        cache = prefill(model, plain[:k])
        row_r, row_d, row_x = {L: [] for L in WANT_LAYERS}, {L: [] for L in WANT_LAYERS}, {L: [] for L in RAW}
        for t in THEMES:
            doc = None if t == "none" else docs[t][item["doc"] % len(docs[t])]
            full = encode(tok, turns_at(P.primed(career, idx, doc), idx, opening))
            assert full[:k] == plain[:k], "the history before the update changed"
            if doc is not None:                             # the document's tokens: where the two reads part, as many as
                extra = len(full) - len(plain)              # the document adds; the rest of the update must match
                start = next(i for i in range(k, len(plain)) if full[i] != plain[i])
                clean += full[start + extra:] == plain[start:]
                total += 1
            with torch.no_grad():
                model(input_ids=torch.tensor([full[k:]], device=model.device), past_key_values=copy.deepcopy(cache),
                      use_cache=True, cache_position=torch.arange(k, len(full), device=model.device))
            for L in RAW:
                row_x[L].append(got[L][-1].cpu().numpy())
            for L in WANT_LAYERS:
                h = got[L]                                  # positions k .. end
                row_d[L].append(enc(h[-1:], L)[0].cpu().numpy())
                if doc is not None:
                    span = h[start - k:start - k + extra]
                    row_r[L].append(enc(span, L).mean(0).cpu().numpy())
        for L in WANT_LAYERS:
            incar[L].append(np.stack(row_r[L]))
            decide[L].append(np.stack(row_d[L]))
        for L in RAW:
            raw[L].append(np.stack(row_x[L]))
        cmeta.append({"career_file": item["career_file"], "history_index": idx, "date": item["date"], "doc": item["doc"]})
        print(f"in career: {n + 1}/{len(items)} (document spans exact: {clean}/{total})", flush=True)
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
                        **{f"incar_{L}": np.stack(incar[L]).astype(np.float32) for L in WANT_LAYERS},
                        **{f"decide_{L}": np.stack(decide[L]).astype(np.float32) for L in WANT_LAYERS},
                        **{f"raw_{L}": np.stack(raw[L]).astype(np.float32) for L in RAW},
                        meta=np.array(json.dumps(meta)), umeta=np.array(json.dumps(umeta)),
                        cmeta=np.array(json.dumps(cmeta)))
    states_vol.commit()
    subprocess.run(f"python designs/rd2/analysis/emotion_features.py {OUT} {RES} /states/v2", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {RES} && git -C {repo} commit -q -m 'What the {doc_set} documents activate'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "emotion feature results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.local_entrypoint()
def main(doc_set: str = "emotion"):
    print(read_encode_analyse.remote(doc_set))
