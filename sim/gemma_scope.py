"""Gemma Scope 2's residual-stream SAEs (16k) for Gemma 3 12B: find the files, load them, encode states into features,
and decode features back (to measure how well a dictionary rebuilds our own states). INSIDE_FAKE_SAE=1 gives random
dictionaries for dry runs (no download)."""
import os, re
import numpy as np

SAE_REPO, SAE_WIDTH = "google/gemma-scope-2-12b-it", "16k"
WANT_LAYERS = [12, 24, 31, 41]
NEURONPEDIA = "https://www.neuronpedia.org/gemma-3-12b-it/{layer}-gemmascope-2-res-16k/{feature}"
FAKE = os.environ.get("INSIDE_FAKE_SAE") == "1"


def sae_layers(n_layers):
    """{layer: file in the repo} for the layers in WANT_LAYERS that have a residual-stream SAE."""
    if FAKE:
        return {l: f"fake_layer_{l}" for l in WANT_LAYERS if l < n_layers}
    from huggingface_hub import list_repo_files
    files = list_repo_files(SAE_REPO)
    found = {}
    for layer in WANT_LAYERS:
        hit = [f for f in files if re.search(rf"(^|[/_-])layer[_-]?{layer}([/_-]|$)", f) and SAE_WIDTH in f
               and re.search(r"res", f) and not re.search(r"mlp|att|transcoder|crosscoder|clt", f)
               and f.endswith((".safetensors", ".npz"))]
        hit.sort(key=lambda f: (("medium" not in f), len(f)))
        if hit:
            found[layer] = hit[0]
    return found


def load_sae(path_in_repo, width):
    """(encoder, encoder bias, threshold, decoder, decoder bias), with the encoder as width x features."""
    if FAKE:
        g = np.random.default_rng(len(path_in_repo))
        We = g.normal(size=(width, 256)).astype(np.float32)
        return We, np.zeros(256, np.float32), np.full(256, 1.0, np.float32), We.T / width, np.zeros(width, np.float32)
    from huggingface_hub import hf_hub_download
    from safetensors.numpy import load_file
    path = hf_hub_download(SAE_REPO, path_in_repo)
    p = load_file(path) if path.endswith(".safetensors") else dict(np.load(path))
    p = {k.lower().replace(".", "_"): v.astype(np.float32) for k, v in p.items()}
    pick = lambda *names: next((p[n] for n in names if n in p), None)
    We, b, t = pick("w_enc", "encoder_weight"), pick("b_enc", "encoder_bias"), pick("threshold", "log_threshold")
    Wd, bd = pick("w_dec", "decoder_weight"), pick("b_dec", "decoder_bias")
    if "log_threshold" in p and "threshold" not in p:
        t = np.exp(t)
    if We.shape[0] != width:
        We = We.T
    if Wd is not None and Wd.shape[1] != width:
        Wd = Wd.T
    return We, b, t, Wd, bd


def encode(x, sae):
    We, b, t = sae[:3]
    pre = x @ We + b
    return np.where(pre > (t if t is not None else 0), pre, 0.0)


def explained(x, sae):
    """The share of the states' variance the dictionary rebuilds (1 = perfect), or None without a decoder."""
    Wd, bd = sae[3], sae[4]
    if Wd is None:
        return None
    rebuilt = encode(x, sae) @ Wd + (bd if bd is not None else 0)
    return float(1 - ((x - rebuilt) ** 2).sum() / ((x - x.mean(0)) ** 2).sum())


def relative_error(x, sae):
    """The dictionary's squared error as a share of the states' squared size (0 = perfect). Unlike explained(), it does
    not depend on how much the states differ from each other, which is little when every state is the same token."""
    Wd, bd = sae[3], sae[4]
    if Wd is None:
        return None
    rebuilt = encode(x, sae) @ Wd + (bd if bd is not None else 0)
    return float(((x - rebuilt) ** 2).sum() / (x ** 2).sum())
