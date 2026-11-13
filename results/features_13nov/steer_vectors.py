"""The vectors for single-feature steering (Part 2; built on CPU, used by scripts/modal_feature_steer.py).

    python steer_vectors.py <states dir> <dir with L24/L31/L41.safetensors> <decision_features.json> <out .npz>

Targets: the decision features that replicate (decision_features.json) and the four financial loss-vs-gain features
(layer 24). Each vector = the feature's decoder direction with dimension 2339 set to zero, times the feature's typical
activation (its mean when on, over Run 1's 1,740 request moments), so x1 adds one typical activation. The financial
features are never on at the request moments, so they take the median length of the layer-24 targets' vectors.
Controls: per layer, 5 random features (not decision features) whose share of request moments with the feature on is
within a factor of 2 of the median share of that layer's targets; decoder direction (2339 zeroed) scaled to the median
target length of the layer. Doses (x1, x2, x4) are applied on the GPU."""
import glob, json, os, sys
import numpy as np
from safetensors.numpy import load_file

STATES, SAEDIR, DEC, OUT = sys.argv[1:5]
DROP, LAYERS, N_CTRL = 2339, [24, 31, 41], 5
FIN = [11564, 9245, 4376, 2367]
X = np.concatenate([np.load(f)["states"][:, LAYERS].astype(np.float32)
                    for d in sorted(glob.glob(os.path.join(STATES, "*_bf16"))) for f in sorted(glob.glob(os.path.join(d, "*.npz")))])
d = json.load(open(DEC))
rng = np.random.default_rng(20261113)
vecs, conds, info = {}, [], []
for li, L in enumerate(LAYERS):
    p = load_file(os.path.join(SAEDIR, f"L{L}.safetensors"))
    We, b, t, Wd = p["w_enc"], p["b_enc"], p["threshold"], p["w_dec"]
    We = We if We.shape[0] == 3840 else We.T
    Wd = Wd if Wd.shape[1] == 3840 else Wd.T
    pre = X[:, li] @ We + b
    F = np.where(pre > t, pre, 0.0)
    share = (F > 0).mean(0)
    typical = np.where(share > 0, F.sum(0) / np.maximum((F > 0).sum(0), 1), 0.0)
    decision = {r["feature"] for r in d["layers"][str(L)]["rows"]}
    targets = [r["feature"] for r in d["layers"][str(L)]["rows"] if r["replicates"]]
    lengths = []
    for f in targets:
        v = Wd[f].astype(np.float64).copy(); v[DROP] = 0.0
        v *= typical[f]
        lengths.append(np.linalg.norm(v))
        key = f"L{L}_f{f}"; vecs[key] = v; conds.append([f"feature {L}/{f}", L, key])
        info.append({"key": key, "layer": L, "feature": f, "kind": "decision", "typical_activation": float(typical[f]),
                     "share_on": float(share[f]), "length": float(np.linalg.norm(v)),
                     "dim2339_share_of_decoder": float(Wd[f][DROP] ** 2 / (Wd[f] ** 2).sum())})
    med = float(np.median(lengths))
    if L == 24:
        for f in FIN:
            v = Wd[f].astype(np.float64).copy(); v[DROP] = 0.0
            v *= med / np.linalg.norm(v)
            key = f"L{L}_fin{f}"; vecs[key] = v; conds.append([f"financial {L}/{f}", L, key])
            info.append({"key": key, "layer": L, "feature": f, "kind": "financial", "share_on": float(share[f]),
                         "length": med, "dim2339_share_of_decoder": float(Wd[f][DROP] ** 2 / (Wd[f] ** 2).sum())})
    m = np.median([share[f] for f in targets])
    pool = [k for k in np.where((share >= m / 2) & (share <= m * 2))[0] if k not in decision and k not in FIN]
    for f in rng.choice(pool, N_CTRL, replace=False):
        v = Wd[f].astype(np.float64).copy(); v[DROP] = 0.0
        v *= med / np.linalg.norm(v)
        key = f"L{L}_ctrl{f}"; vecs[key] = v; conds.append([f"control {L}/{f}", L, key])
        info.append({"key": key, "layer": L, "feature": int(f), "kind": "control", "share_on": float(share[f]),
                     "length": med, "pool_size": len(pool), "target_median_share": float(m)})
    print(L, len(targets), "targets; median length", round(med, 1), "; median share on", round(float(m), 3), "; control pool", len(pool))
np.savez(OUT, conditions=json.dumps(conds), info=json.dumps(info), **vecs)
json.dump(info, open(OUT.replace(".npz", ".json"), "w"), indent=1)
print(len(conds), "vectors")
