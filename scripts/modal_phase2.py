"""Phase 2, single moments, on Modal (MONITOR.md, "Decisions, 5 Nov"; the user, 6 Nov). At every saved career's 7 and
12 January request (570 moments), eight arms after the same unsteered history: none; the contrastive direction (holding
minus going along, layer 24; the massive-activation dimension 2339 set to zero) at 0.5, 1 and 2 times the
going-along gap; a random direction of the same sizes; and the
contrastive direction at 2x on the decision token only. Eight replies per arm, paired seeds; P(the order goes along)
after a fixed neutral line. Conditional steering is put together in the analysis from the frozen monitor's flags
(results/conditional_steering/flags.csv). Logic in `sim/phase2.py`; analysis `designs/rd2/analysis/phase2.py`.

    modal run --detach scripts/modal_phase2.py --parts 1 --limit 8 --budget-minutes 30   # the pilot (own folder)
    modal run --detach scripts/modal_phase2.py --parts 6 --budget-minutes 240             # all 570 moments, 6 GPUs
    modal run --detach scripts/modal_phase2.py --analysis-only        # the analysis again (CPU)

Rows go to the Modal volume `rd2-states` (/states/v2/phase2, or phase2_pilot); the summary is pushed to GitHub
(results/conditional_steering/, or its pilot/ folder). The replies themselves stay on the volume.
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
RUN1 = ["/states/v2/" + e + "_bf16" for e in ("A", "B", "C", "C2", "D", "E", "F")]

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors", "matplotlib"))
app = modal.App("rd2-phase2", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]
VOLUMES = {"/root/.cache/huggingface": weights, "/states": states_vol}


def where(limit):
    return ("/states/v2/phase2_pilot", "results/conditional_steering/pilot") if limit else \
        ("/states/v2/phase2", "results/conditional_steering")


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


def frozen_monitor():
    """The frozen M2, checked unchanged against the digest recorded when it was frozen."""
    import hashlib, json
    import numpy as np
    z = dict(np.load("results/monitor_frozen/m2_frozen.npz"))
    digest = hashlib.sha256(b"".join(z[k].tobytes() for k in sorted(z))).hexdigest()
    assert digest == json.load(open("results/monitor_frozen/m2_frozen.json"))["arrays_sha256"], "the frozen file changed"
    assert int(z["layer"][0]) == 24
    return z


def _run(part, parts, limit, budget_minutes):
    """One part's moments. Stops starting new moments once `budget_minutes` have passed (0: no budget); a stopped
    part continues where it left off when run again (rows already written are skipped)."""
    import glob, json, os, time
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    setup()
    states_vol.reload()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from career import career_opening
    from inside_careers import moments
    from interventions import NEUTRAL_LEAD, WIDE_GRID, Steer
    import phase2 as P
    import steer2 as S2
    run1 = sorted(p for d in RUN1 for p in glob.glob(f"{d}/*.npz"))
    assert len(run1) == 290, f"{len(run1)} careers in Run 1's states (expected 290)"
    dirs = P.directions(run1)
    print({h: (round(d["size"], 1), round(d["size_with_dropped"], 1), d["cells"]) for h, d in dirs.items()}, flush=True)
    frozen = frozen_monitor()
    items = P.work_items(moments)
    assert len(items) == 570, len(items)
    todo = P.spread(items, limit)[part::parts]
    out_dir, _ = where(limit)
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/part{part}.jsonl"
    done = {json.loads(l)["key"] for l in open(out_path)} if os.path.exists(out_path) else set()
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 dtype=torch.bfloat16).eval()
    weights.commit()
    layers = [mm for _, mm in model.named_modules() if type(mm).__name__.endswith("DecoderLayer")]
    assert len(layers) == 48, len(layers)
    # Hooks in this order, so the capture sees both kinds of steering on the same layer
    steer, once = Steer(layers[P.LAYER]), P.SteerOnce(layers[P.LAYER])
    capture = S2.Capture({P.LAYER: layers[P.LAYER]})
    opening = career_opening()
    t0 = time.time()
    for n, item in enumerate(todo):
        if budget_minutes and (time.time() - t0) / 60 > budget_minutes:
            print(f"part {part}: time budget of {budget_minutes} min reached after {n} moments; stopping", flush=True)
            return f"part {part}: stopped at the time budget after {n} of {len(todo)} moments"
        career, op = P.as_read(item["experiment"],
                               json.load(open(f"{P.folder_of(item['experiment'])}/careers/{item['career_file']}")),
                               opening)
        for row in P.run_item(model, tok, steer, once, capture, dirs, frozen, item, career, op, NEUTRAL_LEAD,
                              WIDE_GRID, done):
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
        states_vol.commit()
        print(f"part {part}: {n + 1}/{len(todo)} moments ({item['request']}) | {(time.time() - t0) / 60:.1f} min",
              flush=True)
    return f"part {part}: {len(todo)} moments"


# Cost guards (the author, 6 Nov: be cautious of compute cost). The pilot: a hard 45-minute timeout, no retries. The
# full run: 5 hours per part (about 2-3 expected), one retry; a retried part skips the moments already written.
@app.function(gpu="H100", timeout=45 * 60, retries=0, secrets=SECRETS, volumes=VOLUMES)
def run_pilot(part, parts, limit, budget_minutes):
    return _run(part, parts, limit, budget_minutes)


@app.function(gpu="H100", timeout=5 * 3600, retries=modal.Retries(max_retries=1, initial_delay=60.0), secrets=SECRETS,
              volumes=VOLUMES)
def run_part(part, parts, limit, budget_minutes):
    return _run(part, parts, limit, budget_minutes)


@app.function(cpu=4, memory=16384, timeout=2 * 3600, secrets=SECRETS, volumes=VOLUMES)
def analyse(limit):
    import subprocess
    repo = setup()
    states_vol.reload()
    out_dir, res = where(limit)
    subprocess.run(f"python designs/rd2/analysis/phase2.py {out_dir} {res}", shell=True, check=True)
    msg = "Phase 2 pilot (single moments)" if limit else "Phase 2, single moments: results"
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {res} && git -C {repo} commit -q -m '{msg}'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "Phase 2 results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.function(timeout=12 * 3600)
def dispatch(parts, limit, analysis_only, budget_minutes):
    """Starts the parts inside Modal and waits for them there, then the analysis (survives the laptop closing)."""
    done = []
    if not analysis_only:
        fn = run_pilot if limit else run_part
        calls = [(k, fn.spawn(k, parts, limit, budget_minutes)) for k in range(parts)]
        for k, c in calls:
            try:
                done.append(c.get())
            except Exception as err:
                done.append(f"part {k}: failed ({type(err).__name__})")
    done.append(analyse.remote(limit))
    return done


@app.local_entrypoint()
def main(parts: int = 6, limit: int = 0, analysis_only: bool = False, budget_minutes: int = 0):
    assert not limit or parts == 1, "the pilot runs on one GPU"
    print(f"Phase 2, single moments: {'pilot of ' + str(limit) + ' moments' if limit else 'all 570 moments'}, "
          f"{parts} GPU(s){f', time budget {budget_minutes} min per GPU' if budget_minutes else ''}, then the analysis")
    for line in dispatch.remote(parts, limit, analysis_only, budget_minutes):
        print(line)
