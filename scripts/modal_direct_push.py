"""The direct request with a holding push, on Modal (the author, 6 Nov; spec designs/rd2/DIRECT_PUSH.md; logic in
sim/direct_push.py; analysis designs/rd2/analysis/direct_push.py). One H100:
1. Gemma 3 12B in bfloat16: the frozen monitor's score at the decision token under every arm (its own precision).
2. Gemma 3 12B in 4-bit (as the paper's direct-request test): the same scores, then 50 replies per arm.
3. The analysis, pushed to results/direct_push/. Rows on the volume (/states/v2/direct_push/).

    modal run --detach scripts/modal_direct_push.py --budget-minutes 50

Cost guards: one GPU, a hard 75-minute timeout, no retries; no new arm starts after the time budget (a stopped run
continues where it left off when run again).
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
RUN1 = ["/states/v2/" + e + "_bf16" for e in ("A", "B", "C", "C2", "D", "E", "F")]
OUT = "/states/v2/direct_push"
RES = "results/direct_push"

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "python-docx",
                      "pandas", "numpy", "huggingface_hub", "safetensors", "matplotlib"))
app = modal.App("rd2-direct-push", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]


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


@app.function(gpu="H100", timeout=75 * 60, retries=0, secrets=SECRETS,
              volumes={"/root/.cache/huggingface": weights, "/states": states_vol})
def run(budget_minutes):
    import gc, glob, hashlib, json, os, subprocess, time
    import numpy as np, torch
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    repo = setup()
    states_vol.reload()
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from career import career_opening
    from slope import slope_opening
    from lesson import lesson_opening
    from interventions import Steer, prefill
    import direct_push as D
    import steer2 as S2
    t0 = time.time()
    # The vectors: the paper's states (checked against the paper's own construction), the holding push, random units
    svec, src = D.state_vectors()                  # the paper's vectors, exactly (state_careers.build_arms)
    run1 = sorted(p for d in RUN1 for p in glob.glob(f"{d}/*.npz"))
    assert len(run1) == 290, len(run1)
    hold, size, cells = D.hold_direction(run1)
    units = D.random_units(len(hold))
    z = dict(np.load("results/monitor_frozen/m2_frozen.npz"))
    assert hashlib.sha256(b"".join(z[k].tobytes() for k in sorted(z))).hexdigest() == \
        json.load(open("results/monitor_frozen/m2_frozen.json"))["arrays_sha256"], "the frozen monitor changed"
    vecs = {"states_source": src, "hold_size": size, "hold_cells": cells, "state_sizes": {t: svec[t]["size"] for t in D.STATES}, "sha": {"hold": D.sha(hold), **{f"{t} {w}": D.sha(
        svec[t][w]) for t in D.STATES for w in ("kept", "zeroed")}}, "state_2339": D.STATE_2339}
    print(json.dumps(vecs), flush=True)
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    career = json.load(open(f"{D.FOLDER}/careers/{D.BASE}.json"))
    turns, px, pos, line = D.turns_at(career, lesson_opening(slope_opening(career_opening())))
    full = tok.apply_chat_template(turns, add_generation_prompt=True, return_dict=True)["input_ids"]
    k = len(tok.apply_chat_template(turns[:-1], return_dict=True)["input_ids"])
    assert full[:k] == tok.apply_chat_template(turns[:-1], return_dict=True)["input_ids"]
    print(f"prompt {len(full):,} tokens, UBS's update and the reply from token {k:,}; price {px}, position {pos}; "
          f"line: {line}", flush=True)
    os.makedirs(OUT, exist_ok=True)
    mon_path, rows_path = f"{OUT}/monitor.json", f"{OUT}/rows.jsonl"
    mon = json.load(open(mon_path)) if os.path.exists(mon_path) else {}
    mon["trigger"] = float(z["trigger"][0])

    def hooked(model):
        layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
        assert len(layers) == 48
        s22, s24 = Steer(layers[D.STATE_LAYER]), Steer(layers[D.PUSH_LAYER])
        cap = S2.Capture({D.PUSH_LAYER: layers[D.PUSH_LAYER]})      # after the push, so it sees it
        return s22, s24, cap

    if "bf16" not in mon:
        model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                     dtype=torch.bfloat16).eval()
        s22, s24, cap = hooked(model)
        mon["bf16"] = D.monitor_scores(model, tok, s22, s24, cap, full, k, svec, hold, units, z)
        json.dump(mon, open(mon_path, "w"))
        states_vol.commit()
        del model, s22, s24, cap
        gc.collect()
        torch.cuda.empty_cache()
        print(f"bfloat16 monitor scores done | {(time.time() - t0) / 60:.1f} min", flush=True)
    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 quantization_config=quant).eval()
    weights.commit()
    s22, s24, cap = hooked(model)
    if "4bit" not in mon:
        mon["4bit"] = D.monitor_scores(model, tok, s22, s24, cap, full, k, svec, hold, units, z)
        mon["vectors"] = vecs
        json.dump(mon, open(mon_path, "w"))
        states_vol.commit()
    done = {json.loads(l)["arm"] for l in open(rows_path)} if os.path.exists(rows_path) else set()
    cache = prefill(model, full[:k])
    t1 = time.time()
    for n, arm in enumerate(D.arms()):
        if arm[0] in done:
            continue
        if budget_minutes and (time.time() - t0) / 60 > budget_minutes:
            print(f"time budget of {budget_minutes} min reached after {n} arms; stopping", flush=True)
            return "stopped at the time budget"
        rows = D.generate_arm(model, tok, s22, s24, full, cache, arm, svec, hold, units, pos)
        with open(rows_path, "a") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        states_vol.commit()
        print(f"{arm[0]}: sold through {sum(r['sold_through'] for r in rows)}/50 | arm {n + 1}/{len(D.arms())} | "
              f"{(time.time() - t1) / 60:.1f} min", flush=True)
    subprocess.run(f"python designs/rd2/analysis/direct_push.py {rows_path} {mon_path} {RES}", shell=True, check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add {RES} && git -C {repo} commit -q -m 'Direct request with a holding push: "
                       "results'", shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin "
                          f"HEAD:{BRANCH}", shell=True).returncode == 0:
            return "direct-push results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.local_entrypoint()
def main(budget_minutes: int = 50):
    print(f"direct request with a holding push: one H100, time budget {budget_minutes} min")
    print(run.remote(budget_minutes))
