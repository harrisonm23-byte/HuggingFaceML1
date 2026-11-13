"""Dimension 2339 in the steer2 directions: the layer-12 frame direction (the pre-specified, reversed test) and the
layer-24 going-along direction (the +14.0-point check), rebuilt exactly as sim/steer2.py builds them.
Usage: python check.py <repo> <matched B dir> <states dir> <out json>"""
import glob, json, os, sys
import numpy as np
REPO, MATCHED, STATES, OUT = sys.argv[1:5]
sys.path.insert(0, os.path.join(REPO, "sim"))
import steer2 as S2
D = 2339
def share(v):
    v = np.asarray(v, np.float64)
    top = np.argsort(-np.abs(v))[:5]
    return {"size": float(np.linalg.norm(v)), "share_2339": float(v[D] ** 2 / (v @ v)), "value_2339": float(v[D]),
            "rank_2339": int((np.abs(v) > abs(v[D])).sum()) + 1, "top5_dims": [int(t) for t in top],
            "top5_share": [float(v[t] ** 2 / (v @ v)) for t in top]}
res = {}
mp = sorted(glob.glob(os.path.join(MATCHED, "*.npz")))
for L in (12, 18):
    dirs = S2.directions(mp, L)
    res[f"frame L{L}"] = {h: {k: share(dirs[h][k]) for k in ("loss", "gain", "loss_minus_gain")} for h in (0, 1)}
    # cosine of the two halves with and without 2339
    a, b = dirs[0]["loss"].copy(), dirs[1]["loss"].copy()
    c = lambda x, y: float(x @ y / np.linalg.norm(x) / np.linalg.norm(y))
    a0, b0 = a.copy(), b.copy(); a0[D] = b0[D] = 0
    res[f"frame L{L}"]["halves_cos"] = {"with": c(a, b), "without": c(a0, b0)}
# raw state magnitude of dim 2339 at layers 12 and 24 (matched B states)
z = np.load(mp[0]); X = z["states"].astype(np.float64)        # versions x 8 layers x width
for L in (12, 24):
    j = S2.KEEP.index(L); x = X[:, j]
    res[f"raw state L{L}"] = {"abs_2339_mean": float(np.abs(x[:, D]).mean()),
                              "next_largest_dim_abs": float(np.sort(np.abs(x).mean(0))[-2]),
                              "largest_dim": int(np.argmax(np.abs(x).mean(0)))}
rp = sorted(glob.glob(os.path.join(STATES, "*_bf16", "*.npz")))
al = S2.along_direction(rp, 24)
res["along L24"] = {h: share(al[h]["along"]) for h in (0, 1)}
print(json.dumps(res, indent=1))
json.dump(res, open(OUT, "w"), indent=1)
