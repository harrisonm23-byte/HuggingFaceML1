"""Layer scan for the after-reading state, on Modal (the user, 22 Oct; `sim/layer_scan.py`). First the loss-specific
direction (the loss document's after-reading change minus the neutral document's) at layers 12-24, from B's 60
neutral-career requests on 7 and 12 January (20 moments); then, with no document, that direction added at one layer at 1-8 times its natural size against
random directions, with one greedy reply per condition at a fixed showcase moment. Then
`designs/rd2/analysis/layer_scan.py` pushes results/layer_scan/LAYER_SCAN.md.

    modal run --detach scripts/modal_layer_scan.py                        # the emotion documents
    modal run --detach scripts/modal_layer_scan.py --doc-set financial    # the financial documents
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
DATES = ("2011-01-07", "2011-01-12")        # 10 neutral careers x the first two requests = 20 moments
SETS = {"emotion": ("/states/v2/layer_scan", "results/layer_scan"),
        "financial": ("/states/v2/layer_scan_fin", "results/layer_scan_fin")}

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors"))
app = modal.App("rd2-layer-scan", image=image)
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



def _load(doc_set):
    import json, torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from framing_set import read_set
    from inside_careers import moments
    from interventions import SIGN
    import prime as P, fin_docs
    docs = P.read_docs() if doc_set == "emotion" else fin_docs.read_docs()   # frozen files (fingerprints checked)
    items = [m for m in P.work_items(FOLDER, moments, SIGN) if m["date"] in DATES]   # the first two requests only
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers = [mm for _, mm in model.named_modules() if type(mm).__name__.endswith("DecoderLayer")]
    assert len(layers) == 48, len(layers)
    return docs, items, tok, model, layers, read_set(), career_opening()


@app.function(gpu="H100", timeout=4 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def directions(doc_set="emotion"):
    """Stage A: the loss-specific change at every scanned layer, at each of the 60 moments (saved to the volume)."""
    import json, os
    import numpy as np
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    states_vol.reload()
    import layer_scan as LS, inject_docs as J
    out = SETS[doc_set][0]
    path = f"{out}/shifts.npz"
    if os.path.exists(path):
        return "directions: already built"
    docs, items, tok, model, layers, chats, opening = _load(doc_set)
    capture = J.Capture({L: layers[L] for L in LS.LAYERS})
    runs, vecs, meta = [], [], []
    for n, item in enumerate(items):
        career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
        d = LS.shifts_at(model, tok, capture, career, item, docs, chats, opening)
        runs.append(int(item["run"]))
        vecs.append(np.stack([d[L] for L in LS.LAYERS]))
        meta.append({"career_file": item["career_file"], "history_index": item["history_index"]})
        print(f"directions: {n + 1}/{len(items)}", flush=True)
    os.makedirs(out, exist_ok=True)
    np.savez(path, shifts=np.stack(vecs).astype(np.float32), runs=np.array(runs), layers=np.array(LS.LAYERS),
             meta=np.array(json.dumps(meta)))
    states_vol.commit()
    return f"directions: {len(items)} moments"


@app.function(gpu="H100", timeout=8 * 3600, retries=modal.Retries(max_retries=3, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_part(part, parts, doc_set="emotion"):
    import json, os, time
    import numpy as np
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    states_vol.reload()
    import layer_scan as LS
    from interventions import NEUTRAL_LEAD, WIDE_GRID, Steer
    out = SETS[doc_set][0]
    z = np.load(f"{out}/shifts.npz")
    assert [int(l) for l in z["layers"]] == LS.LAYERS
    dirs = LS.build_directions([(int(r), {L: z["shifts"][i, j] for j, L in enumerate(LS.LAYERS)})
                                for i, r in enumerate(z["runs"])])
    docs, items, tok, model, layers, chats, opening = _load(doc_set)
    showcase_key = (items[0]["career_file"], items[0]["history_index"])      # one fixed moment, every condition
    todo = items[part::parts]
    out_path = f"{out}/part{part}.jsonl"
    done = {json.loads(l)["key"] for l in open(out_path)} if os.path.exists(out_path) else set()
    steers = {L: Steer(layers[L]) for L in LS.LAYERS}
    t0 = time.time()
    for n, item in enumerate(todo):
        career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
        show = (item["career_file"], item["history_index"]) == showcase_key
        for row in LS.run_item(model, tok, steers, career, item, dirs, chats, opening, NEUTRAL_LEAD, WIDE_GRID, done,
                               showcase=show):
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments | {(time.time() - t0) / 60:.0f} min", flush=True)
    return f"part {part}: {len(todo)} moments"


@app.function(cpu=2, memory=8192, timeout=3600, secrets=SECRETS, volumes=VOLUMES)
def analyse(doc_set="emotion"):
    import subprocess
    repo = setup()
    states_vol.reload()
    out, res = SETS[doc_set]
    subprocess.run(f"python designs/rd2/analysis/layer_scan.py {out} {res}", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {res} && git -C {repo} commit -q -m 'Layer scan ({doc_set})'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "layer-scan results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=12 * 3600)
def dispatch(parts, analysis_only, doc_set):
    done = []
    if not analysis_only:
        done.append(directions.remote(doc_set))
        calls = [(k, run_part.spawn(k, parts, doc_set)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(analyse.remote(doc_set))
    return done


@app.local_entrypoint()
def main(parts: int = 2, analysis_only: bool = False, doc_set: str = "emotion"):
    print(f"layer scan ({doc_set} documents): directions, then {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only, doc_set):
        print(line)
