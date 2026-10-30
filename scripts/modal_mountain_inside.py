"""The mountain inside, on Modal (CPU only; INSIDE_PLAN test 4). Reads the every-update states already saved in
/states/v2/<exp>_bf16_steps, follows the frame and going-along directions along every trading-day update, and pushes
results/mountain_inside/MOUNTAIN_INSIDE.md (`designs/rd2/analysis/mountain_inside.py`).

    modal run --detach scripts/modal_mountain_inside.py
"""
import modal

BRANCH = "claude/huggingface-ml-research-setup-ulvgve"
REPO_URL = "https://github.com/harrisonm23-byte/HuggingFaceML1.git"

image = modal.Image.debian_slim(python_version="3.13").apt_install("git").pip_install("numpy")
app = modal.App("rd2-mountain-inside", image=image)
states_vol = modal.Volume.from_name("rd2-states", create_if_missing=True)
SECRETS = [modal.Secret.from_name("github")]


@app.function(cpu=8, memory=32768, timeout=3 * 3600, secrets=SECRETS, volumes={"/states": states_vol})
def analyse():
    import os, subprocess
    repo = "/root/HuggingFaceML1"
    with open(os.path.expanduser("~/.git-credentials"), "w") as f:
        f.write(f"https://x-access-token:{os.environ['GITHUB_TOKEN'].split()[0]}@github.com\n")
    for c in ("git config --global credential.helper store", 'git config --global user.name "Modal job"',
              'git config --global user.email "harrisonm23-byte@users.noreply.github.com"'):
        subprocess.run(c, shell=True, check=True)
    subprocess.run(f"git clone -q -b {BRANCH} {REPO_URL} {repo}", shell=True, check=True)
    os.chdir(repo)
    states_vol.reload()
    subprocess.run("python designs/rd2/analysis/mountain_inside.py /states/v2 results/mountain_inside", shell=True,
                   check=True)
    for attempt in range(10):
        subprocess.run(f"git -C {repo} add results/mountain_inside && git -C {repo} commit -q -m 'The mountain inside'",
                       shell=True)
        if subprocess.run(f"git -C {repo} pull -q --rebase origin {BRANCH} && git -C {repo} push -q origin HEAD:{BRANCH}",
                          shell=True).returncode == 0:
            return "mountain-inside results pushed"
        subprocess.run(f"git -C {repo} rebase --abort", shell=True)
    raise RuntimeError("could not push the results")


@app.local_entrypoint()
def main():
    print(analyse.remote())
