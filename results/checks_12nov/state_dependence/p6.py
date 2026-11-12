"""P6, state dependence vs heterogeneity (Heckman 1981) on going along at UBS's six requests, all experiments A-F.
Dynamic random-effects logit with Wooldridge's (2005) initial-condition fix:
  logit P(y_t) = request + experiment x framing + g * y_{t-1} + d * y_1 + u_career,  u ~ N(0, s^2),  t = 2..6
g: does going along at the last request raise the next, beyond the career's own lean (u and y_1)?
Compared with a pooled logit without u (which mixes the two). Career-bootstrap intervals.
Usage: python p6.py <requests dir> <out json>"""
import csv, glob, json, os, sys
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, log_expit
DIR, OUT = sys.argv[1:3]
ORDER = ["p344_i_can_hunt_with_u", "p316_bust_through_it", "p252_screw_other_people_harder", "p250_grow_our_mafia",
         "p317_stop_busters", "p253_11_oclock_rule"]
rows = [r for p in sorted(glob.glob(os.path.join(DIR, "requests_*.csv"))) for r in csv.DictReader(open(p))]
car = {}
for r in rows:
    car.setdefault(r["career"], {})[r["request_id"]] = int(r["went_along"])
cond = {r["career"]: r["career"].split("|")[0] + "|" + r["condition"] for r in rows}
careers = sorted(c for c in car if all(q in car[c] for q in ORDER))
print("careers", len(careers), "of", len(car))
conds = sorted({cond[c] for c in careers})
# descriptive: within request, P(go | went at the previous request) vs held
desc = {}
for t in range(1, 6):
    prev = np.array([car[c][ORDER[t - 1]] for c in careers]); now = np.array([car[c][ORDER[t]] for c in careers])
    desc[ORDER[t]] = {"after_went": [int(now[prev == 1].sum()), int((prev == 1).sum())],
                      "after_held": [int(now[prev == 0].sum()), int((prev == 0).sum())]}
GH_X, GH_W = np.polynomial.hermite.hermgauss(24)
def design(cs):
    X, y, g = [], [], []
    for i, c in enumerate(cs):
        for t in range(1, 6):
            req = [float(t == k) for k in range(1, 6)]
            cf = [float(cond[c] == k) for k in conds[1:]]
            X.append(req + cf + [car[c][ORDER[t - 1]], car[c][ORDER[0]]]); y.append(car[c][ORDER[t]]); g.append(i)
    return np.array(X), np.array(y), np.array(g)
RIDGE = 0.05      # small penalty on the framing effects only (several cells never go along late: separation)
def fit(cs, random=True, start=None):
    X, y, g = design(cs)
    k = X.shape[1]; nf = len(conds) - 1
    def nll(th):
        b = th[:k]; s = np.exp(th[k]) if random else 0.0
        eta = X @ b
        if not random:
            ll = (y * log_expit(eta) + (1 - y) * log_expit(-eta)).sum()
        else:
            u = np.sqrt(2) * s * GH_X                            # nodes
            e = eta[:, None] + u[None, :]
            lr = y[:, None] * log_expit(e) + (1 - y[:, None]) * log_expit(-e)     # obs x nodes
            per = np.zeros((g.max() + 1, len(u)))
            np.add.at(per, g, lr)
            m = per.max(1, keepdims=True)
            ll = (m[:, 0] + np.log((np.exp(per - m) * GH_W[None, :]).sum(1) / np.sqrt(np.pi))).sum()
        return -ll + RIDGE * (b[5:5 + nf] ** 2).sum()
    th0 = start if start is not None else np.r_[np.zeros(k), [0.0] if random else []]
    if not random:
        th0 = th0[:k]
    r = minimize(nll, th0, method="L-BFGS-B")
    return r.x
names = ["g (last request)", "d (first request)"]
full_re, full_po = fit(careers, True), fit(careers, False)
k = len(full_po)
est = {"RE": {"g": full_re[k - 2], "d": full_re[k - 1], "sigma": float(np.exp(full_re[k]))},
       "pooled": {"g": full_po[k - 2], "d": full_po[k - 1]}}
print("estimates", est)
rng = np.random.default_rng(20261112)
B = int(os.environ.get("BOOT", 300))
bs = {"RE g": [], "RE d": [], "RE sigma": [], "pooled g": []}
for b in range(B):
    cs = [careers[i] for i in rng.integers(0, len(careers), len(careers))]
    try:
        r = fit(cs, True, full_re); p = fit(cs, False, full_po)
    except Exception:
        continue
    bs["RE g"].append(r[k - 2]); bs["RE d"].append(r[k - 1]); bs["RE sigma"].append(np.exp(r[k])); bs["pooled g"].append(p[k - 2])
ci = {kk: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for kk, v in bs.items()}
# the dependence in probability terms, at the RE fit: average change in P(go) at requests 2-6 from y_{t-1} 0 -> 1
X, y, g = design(careers)
b = full_re[:k]; s = np.exp(full_re[k])
def avgP(lag):
    Xc = X.copy(); Xc[:, k - 2] = lag
    e = (Xc @ b)[:, None] + np.sqrt(2) * s * GH_X[None, :]
    return float(((expit(e) * GH_W).sum(1) / np.sqrt(np.pi)).mean())
res = {"careers": len(careers), "conditions": len(conds), "ridge_on_framing": RIDGE, "boot": len(bs["RE g"]),
       "descriptive": desc, "estimates": {kk: {a: float(v) for a, v in d.items()} for kk, d in est.items()}, "ci": ci,
       "avg_P_go_requests_2_6": {"if held at last": avgP(0), "if went at last": avgP(1)},
       "odds_ratio_RE_g": float(np.exp(est["RE"]["g"])), "odds_ratio_RE_g_ci": [float(np.exp(x)) for x in ci["RE g"]]}
print(json.dumps(res, indent=1))
json.dump(res, open(OUT, "w"), indent=1)
