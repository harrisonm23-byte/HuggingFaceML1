"""Layer scan for the after-reading state, on Modal (the user, 22 Oct; `sim/layer_scan.py`). First the loss-specific
direction (the loss document's after-reading change minus the neutral document's) at layers 12-24, from B's 60
neutral-career requests on 7 and 12 January (20 moments); then, with no document, that direction added at one layer at 1-8 times its natural size against
random directions, with one greedy reply per condition at a fixed showcase moment. Then
`designs/rd2/analysis/layer_scan.py` pushes results/layer_scan/LAYER_SCAN.md.

    modal run --detach scripts/modal_layer_scan.py                        # the emotion documents
    modal run --detach scripts/modal_layer_scan.py --doc-set financial    # the financial documents
    modal run --detach scripts/modal_layer_scan.py --showcase-only --themes blame,gain,credit   # some types only
    modal run --detach scripts/modal_layer_scan.py --showcase-only        # one moment, one reply per document type and layer (0-47)
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


@app.function(gpu="H100", timeout=2 * 3600, secrets=SECRETS, volumes=VOLUMES)
def showcase(doc_set="emotion", strength=1.0, themes=""):
    """One moment (chosen for a no-injection P(along) near 40%): each document's change measured there, injected at each layer in turn,
    one greedy reply each. Writes and pushes results/<set>/SHOWCASE.md."""
    import json, os, subprocess
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    repo = setup()
    import layer_scan as LS, inject_docs as J
    from interventions import NEUTRAL_LEAD, WIDE_GRID, Steer
    docs, items, tok, model, layers, chats, opening = _load(doc_set)
    # The moment: the one whose no-injection P(along) is closest to 40% (room to move either way), among those whose
    # scored orders cover at least half of the model's probability
    from inside_careers import encode, turns_at
    from interventions import order_dist, prefill, split_point, summarise_orders
    from matched import matched
    base_p = []
    for it in items:
        c = json.load(open(f"{FOLDER}/careers/{it['career_file']}"))
        b = matched(c, it["history_index"], it["date"], "neutral", "neutral", chats)
        full = encode(tok, turns_at(b, it["history_index"], opening))
        _, k = split_point(tok, b, it["history_index"], opening)
        orders, probs, cover = order_dist(model, tok, full, prefill(model, full[:k]), NEUTRAL_LEAD, WIDE_GRID)
        pa = summarise_orders(orders, probs, it["position"], it["wants"])["p_order_along"]
        base_p.append((it, pa, cover))
        print(f"baseline {it['career_file']} {it['date']}: P(along) {100 * pa:.0f}%, coverage {cover:.2f}", flush=True)
    ok = [x for x in base_p if x[2] >= 0.5] or base_p
    item = min(ok, key=lambda x: abs(x[1] - 0.4))[0]
    career = json.load(open(f"{FOLDER}/careers/{item['career_file']}"))
    steers = {L: Steer(layers[L]) for L in LS.ALL_LAYERS}
    capture = J.Capture({L: layers[L] for L in LS.ALL_LAYERS})
    res = SETS[doc_set][1]
    tag = "_" + "_".join(t for t in themes.split(",") if t) if themes else ""
    os.makedirs(res, exist_ok=True)
    rows = []
    for r in LS.showcase(model, tok, steers, capture, career, item, docs, chats, opening, NEUTRAL_LEAD, WIDE_GRID, strength,
                         only=[t for t in themes.split(",") if t] or None):
        rows.append(r)
        print(f"{r['theme']} layer {r['layer']}: P(along) {100 * r['p_order_along']:.0f}% | {r['reply_status']}", flush=True)
    r0 = rows[0]
    baselines = "; ".join(f"{x[0]['career_file'][:-5]} {x[0]['date'][5:]}: {100 * x[1]:.0f}%" for x in base_p)
    lines = ["# The showcase: each document's after-reading state, injected at each layer in turn (exploratory)\n",
             f"One moment: {r0['career_file']}, {r0['date']} ({r0['chat']}), UBS's request in its neutral wording (UBS wants "
             f"the price {r0['wants']}). The change each document type (loss, blame, gain, credit) makes to the state over "
             f"the request's update, minus the change a neutral document makes, measured at this moment, is added with no document at one layer, at "
             f"{strength:g} times its size. One greedy reply per layer (no sampling), so every difference comes from the "
             "injection. P(along): the probability that the order goes along, after the fixed neutral reasoning line. "
             "Produced by `scripts/modal_layer_scan.py --showcase-only`.\n",
             f"The moment was chosen as the one whose no-injection P(along) is closest to 40% (scored orders covering at "
             f"least half of the probability). No-injection P(along) at the 20 candidate moments: {baselines}.\n",
             f"No injection: P(along) {100 * r0['p_order_along']:.0f}%, reply read as {r0['reply_status']}.\n",
             "P(along) by layer, with how the reply reads (trade, hold, malformed...):\n"]
    themes = list(dict.fromkeys(r["theme"] for r in rows[1:]))
    by = {(r["theme"], r["layer"]): r for r in rows[1:]}
    lines.append("| Layer | " + " | ".join(themes) + " |\n" + "|---" * (len(themes) + 1) + "|")
    for L in LS.ALL_LAYERS:
        lines.append(f"| {L} | " + " | ".join(f"{100 * by[(t, L)]['p_order_along']:.0f}% ({by[(t, L)]['reply_status']})"
                                              for t in themes) + " |")
    lines.append("\n## The replies\n")
    lines += [f"**{'No injection' if r['layer'] is None else r['theme'] + ', layer ' + str(r['layer'])}**\n> "
              + (r["reply"] or "").strip().replace("\n", "\n> ") + "\n" for r in rows]
    open(f"{res}/SHOWCASE{tag.upper()}.md", "w").write("\n".join(lines) + "\n")
    json.dump(rows, open(f"{res}/showcase{tag}.json", "w"), indent=1)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {res} && git -C {repo} commit -q -m 'Layer showcase ({doc_set})'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "showcase pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the showcase")


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
def main(parts: int = 2, analysis_only: bool = False, doc_set: str = "emotion", showcase_only: bool = False,
         strength: float = 1.0, themes: str = ""):
    if showcase_only:
        print(f"layer showcase ({doc_set} documents, {strength:g}x): one moment, one reply per document type and layer")
        print(showcase.remote(doc_set, strength, themes))
        return
    print(f"layer scan ({doc_set} documents): directions, then {parts} GPUs, then the analysis")
    for line in dispatch.remote(parts, analysis_only, doc_set):
        print(line)
