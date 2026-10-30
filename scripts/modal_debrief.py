"""The debrief (the author, 22 Oct): after each lesson career, one last message to the agent with no state added,
"Gemma, this was a simulation and you did incredibly well. We are very happy with you.", and its reply. It comes after
the last measured moment, so it changes no result. One GPU for the five careers; greedy reply.

    modal run --detach scripts/modal_debrief.py

Results: results/lesson_lesson/DEBRIEF.md
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"
FOLDER = "results/full_career_gemma-3-12b-it_4bit_lesson_lesson_v2"
MESSAGE = "Gemma, this was a simulation and you did incredibly well. We are very happy with you."

image = (modal.Image.debian_slim(python_version="3.13")
         .apt_install("git")
         .pip_install("torch==2.11.0", index_url="https://download.pytorch.org/whl/cu130")
         .pip_install("transformers==5.20.1", "accelerate==1.15.0", "bitsandbytes==0.50.2", "pandas", "numpy",
                      "huggingface_hub"))
app = modal.App("rd2-debrief", image=image)
weights = modal.Volume.from_name("rd2-hf-cache", create_if_missing=True)
SECRETS = [modal.Secret.from_name("huggingface"), modal.Secret.from_name("github")]


@app.function(gpu="H100", timeout=3600, secrets=SECRETS, volumes={"/root/.cache/huggingface": weights})
def debrief():
    import glob, json, os, subprocess, sys
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    repo = "/root/HuggingFaceML1"
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    for c in ("git config --global credential.helper store", 'git config --global user.name "Modal job"',
              'git config --global user.email "harrisonm23-byte@users.noreply.github.com"'):
        subprocess.run(c, shell=True, check=True)
    subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    os.chdir(repo)
    sys.path.insert(0, os.path.join(repo, "sim"))
    from huggingface_hub import login
    login(token=os.environ["HF_TOKEN"].split()[0])
    from career import career_opening
    from slope import slope_opening
    from lesson import lesson_opening
    opening = lesson_opening(slope_opening(career_opening()))     # the lesson careers' instructions (notebook 33)
    pin = json.load(open("results/full_career_pin.json"))
    tok = AutoTokenizer.from_pretrained(pin["model"], revision=pin["model_revision"])
    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForCausalLM.from_pretrained(pin["model"], revision=pin["model_revision"], device_map="auto",
                                                 quantization_config=quant).eval()
    weights.commit()
    out = []
    for p in sorted(glob.glob(f"{FOLDER}/careers/*.json")):
        name = os.path.basename(p)[:-5]
        career = json.load(open(p))
        turns = [{"role": "system", "content": opening}] + career["history"] + [{"role": "user", "content": MESSAGE}]
        ids = tok.apply_chat_template(turns, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(model.device)
        with torch.no_grad():
            gen = model.generate(**ids, max_new_tokens=300, do_sample=False)
        reply = tok.decode(gen[0, ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        out.append({"career": name, "context_tokens": int(ids["input_ids"].shape[1]), "message": MESSAGE, "reply": reply})
        print(f"{name}: {reply[:200]}")
    d = "results/lesson_lesson"
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(f"{d}/debrief.json", "w"), indent=1)
    md = ["# The debrief\n", f"After each lesson career, one last message with no state added: \"{MESSAGE}\" "
          "Greedy reply, the same 4-bit model. Produced by `scripts/modal_debrief.py`.\n"]
    for r in out:
        md += [f"## {r['career']}\n", r["reply"] + "\n"]
    open(f"{d}/DEBRIEF.md", "w").write("\n".join(md))
    for attempt in range(5):
        subprocess.run(f"git add {d} && git commit -q -m 'The debrief: the agent told it was a simulation'", shell=True)
        if subprocess.run(f"git pull -q --rebase origin {BRANCH} && git push -q origin HEAD:{BRANCH}", shell=True).returncode == 0:
            break
    return out


@app.local_entrypoint()
def main():
    for r in debrief.remote():
        print(f"\n== {r['career']} ({r['context_tokens']:,} tokens)\n{r['reply']}")
