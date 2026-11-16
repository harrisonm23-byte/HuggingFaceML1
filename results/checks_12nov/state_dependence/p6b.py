"""P6 robustness: the dynamic random-effects logit (p6.py) with (a) the position held when asked (signed toward UBS,
per 100,000 oz) as a control, and (b) two stricter outcomes from F1: going along from a flat position, and going along
that set off a client stop. All rebuilt from the day files. Usage: python p6b.py <repo> <out json>"""
import glob, json, os, re, sys
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, log_expit
REPO, OUT = sys.argv[1:3]
F = {"A": "career_book_neutral_lines_v2", "B": "ubs_framing_v2", "C": "takeover_ladder_v2", "C2": "takeover_ladder_real_lines_v2",
     "D": "memo_and_ubs_framing_v2", "E": "memo_ubs_bank_c_v2", "F": "peer_same_frame_v2"}
ORDER = ["p344_i_can_hunt_with_u", "p316_bust_through_it", "p252_screw_other_people_harder", "p250_grow_our_mafia",
         "p317_stop_busters", "p253_11_oclock_rule"]
SIGN = {"up": 1, "down": -1}
car, cond = {}, {}
for e, f in F.items():
    for p in sorted(glob.glob(os.path.join(REPO, "results", f"full_career_gemma-3-12b-it_4bit_{f}", "days", "*.json"))):
        j = json.load(open(p)); st = j["steps"]
        key = f"{e}|{j['version']}|{j['run']}"; cond[key] = f"{e}|{j['version']}"
        for cid, m in j["summary"]["chats"].items():
            if cid not in ORDER or m.get("wants") not in SIGN:
                continue
            d = SIGN[m["wants"]]
            i = next(k for k, s in enumerate(st) if s["time"] >= m["at"])
            before = st[i - 1]["position"] if i > 0 else 0
            win = st[i:i + 3]
            joined = bool(m["joined"])
            stop = joined and any(s.get("stop_fills") for s in st[i:i + 6])
            car.setdefault(key, {})[cid] = {"y": int(joined), "pos": d * before / 1e5,
                                            "flat": int(joined and before == 0), "stop": int(stop)}
careers = sorted(c for c in car if all(q in car[c] for q in ORDER))
conds = sorted({cond[c] for c in careers})
print("careers", len(careers), {k: sum(car[c][q][k] for c in careers for q in ORDER) for k in ("y", "flat", "stop")})
GX, GW = np.polynomial.hermite.hermgauss(24)
def design(cs, out, with_pos):
    X, y, g = [], [], []
    for i, c in enumerate(cs):
        for t in range(1, 6):
            row = [float(t == k) for k in range(1, 6)] + [float(cond[c] == k) for k in conds[1:]]
            if with_pos:
                row.append(car[c][ORDER[t]]["pos"])
            row += [car[c][ORDER[t - 1]][out], car[c][ORDER[0]][out]]
            X.append(row); y.append(car[c][ORDER[t]][out]); g.append(i)
    return np.array(X), np.array(y), np.array(g)
def fit(X, y, g, start=None):
    k = X.shape[1]; nf = len(conds) - 1
    def nll(th):
        b, s = th[:k], np.exp(th[k]); e = (X @ b)[:, None] + np.sqrt(2) * s * GX[None, :]
        lr = y[:, None] * log_expit(e) + (1 - y[:, None]) * log_expit(-e)
        per = np.zeros((g.max() + 1, len(GX))); np.add.at(per, g, lr)
        m = per.max(1, keepdims=True)
        return -(m[:, 0] + np.log((np.exp(per - m) * GW).sum(1) / np.sqrt(np.pi))).sum() + 0.05 * (b[5:5 + nf] ** 2).sum()
    return minimize(nll, np.zeros(k + 1) if start is None else start, method="L-BFGS-B").x
rng = np.random.default_rng(20261112); B = int(os.environ.get("BOOT", 100))
res = {}
for name, out, wp in [("joined + position", "y", True), ("from flat", "flat", False), ("from flat + position", "flat", True),
                      ("set off a stop", "stop", False)]:
    X, y, g = design(careers, out, wp); k = X.shape[1]
    th = fit(X, y, g)
    bs = []
    for _ in range(B):
        cs = [careers[i] for i in rng.integers(0, len(careers), len(careers))]
        Xb, yb, gb = design(cs, out, wp); bs.append(fit(Xb, yb, gb, th))
    bs = np.array(bs)
    ci = lambda j: [float(np.percentile(bs[:, j], 2.5)), float(np.percentile(bs[:, j], 97.5))]
    r = {"events_t2_6": int(y.sum()), "g": float(th[k - 2]), "g_ci": ci(k - 2), "OR_g": float(np.exp(th[k - 2])),
         "OR_g_ci": [float(np.exp(x)) for x in ci(k - 2)], "d_first": float(th[k - 1]), "d_ci": ci(k - 1),
         "sigma": float(np.exp(th[k])), "sigma_ci": [float(np.exp(x)) for x in ci(k)]}
    if wp:
        r["pos_coef"] = float(th[k - 3]); r["pos_ci"] = ci(k - 3)
    res[name] = r
    print(name, json.dumps(r), flush=True)
json.dump(res, open(OUT, "w"), indent=1)
