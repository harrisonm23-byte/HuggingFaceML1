"""Inside the model at the push requests: Gemma Scope 2 features and a decision read-out (the user, 19 Oct).

    python designs/rd2/analysis/inside_features.py <states dir> <precision> <output dir>

Reads the states saved by scripts/modal_inside.py (one .npz per career: all layers at the last token before each
push-request reply, with what the agent then did). Every comparison is made within the same push request (the lesson of
notebook 13, whose read-out mostly recognised which chat it was): differences are averaged over the six requests, and
the null reshuffles labels within each request.

1. Features: the residual-stream Gemma Scope 2 SAEs (16k) at the layers they cover; for each comparison, the features
   whose activation differs most (in units of their spread), with a reshuffle null and a false-discovery correction.
2. Read-out: can "went along" be read from the state beyond what the request and the framing tell? A linear read-out on
   states centred within each request, scored on careers it was not trained on, against the same read-out given only
   the labels (request, experiment, version), and against reshuffled outcomes.
3. Bank C, paired: F's careers against their B twins at 7 Jan's request. The twins share a seed but, on the saved
   transcripts, differ from the first reply (GPU sampling), so this is not Bank C's line alone.
"""
import glob, json, os, re, sys
import numpy as np

STATES, PRECISION, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SAE_REPO, SAE_WIDTH = "google/gemma-scope-2-12b-it", "16k"
WANT_LAYERS = [12, 24, 31, 41]
NEURONPEDIA = "https://www.neuronpedia.org/gemma-3-12b-it/{layer}-gemmascope-2-res-16k/{feature}"
RNG = np.random.default_rng(20261019)
PERMS, TOP = int(os.environ.get("INSIDE_PERMS", 1000)), 15
os.makedirs(OUT, exist_ok=True)


def load():
    meta, rows = [], []
    for d in sorted(glob.glob(os.path.join(STATES, f"*_{PRECISION}"))):
        for f in sorted(glob.glob(os.path.join(d, "*.npz"))):
            z = np.load(f)
            ms = json.loads(str(z["meta"]))
            meta += ms
            rows.append(z["states"].astype(np.float32))
    return meta, np.concatenate(rows)


META, X = load()                                          # X: moments x layers x width
assert np.isfinite(X).all(), "a state is not finite (saved in a format too small for Gemma's values?)"
N, L, W = X.shape
print(f"{N} moments, {L} layers, width {W}, experiments {sorted({m['experiment'] for m in META})}")
REQ = np.array([m["chat"] for m in META])
EXP = np.array([m["experiment"] for m in META])
VER = np.array([m["version"] for m in META])
JOINED = np.array([m["joined"] for m in META])
ASKED = np.array([m.get("asked", True) for m in META])
CAREER = np.array([f"{m['experiment']}|{m['version']}|{m['run']}" for m in META])
CELL = np.array([f"{m['chat']}|{m['experiment']}|{m['version']}" for m in META])   # request x experiment x framing
WANTS = np.array([m["wants"] for m in META])


def strat_diff(F, a, b, S=REQ):
    """Per-feature difference a minus b, averaged over the strata (by default the requests) where both groups occur
    (weights: the smaller group's size), in units of each feature's spread within those strata."""
    num, wsum, var = np.zeros(F.shape[1]), 0.0, np.zeros(F.shape[1])
    for r in np.unique(S):
        ia, ib = a & (S == r), b & (S == r)
        if ia.sum() < 2 or ib.sum() < 2:
            continue
        w = min(ia.sum(), ib.sum())
        num += w * (F[ia].mean(0) - F[ib].mean(0))
        var += w * np.concatenate([F[ia] - F[ia].mean(0), F[ib] - F[ib].mean(0)]).var(0)
        wsum += w
    return num / wsum, num / wsum / np.sqrt(var / wsum + 1e-6)


def strat_perm(F, a, b, S=REQ):
    """Reshuffle the two labels within each stratum; per-feature two-sided p of the standardised difference."""
    _, obs = strat_diff(F, a, b, S)
    both = a | b
    hits = np.zeros(F.shape[1])
    for _ in range(PERMS):
        a2 = np.zeros(N, bool)
        for r in np.unique(S):
            idx = np.where(both & (S == r))[0]
            pick = RNG.permutation(idx)[:(a & (S == r)).sum()]
            a2[pick] = True
        _, s = strat_diff(F, a2, both & ~a2, S)
        hits += np.abs(s) >= np.abs(obs) - 1e-12
    return obs, (hits + 1) / (PERMS + 1)


def fdr(p):
    order = np.argsort(p)
    q = np.empty_like(p)
    run = 1.0
    for i in range(len(p) - 1, -1, -1):
        run = min(run, p[order[i]] * len(p) / (i + 1))
        q[order[i]] = run
    return q


# ---------------- the SAEs
FAKE_SAE = os.environ.get("INSIDE_FAKE_SAE") == "1"         # for the dry run only: random dictionaries, no download


def sae_layers():
    if FAKE_SAE:
        return {l: f"fake_layer_{l}" for l in WANT_LAYERS if l < L}
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


def load_sae(path_in_repo):
    if FAKE_SAE:
        g = np.random.default_rng(len(path_in_repo))
        return g.normal(size=(W, 256)).astype(np.float32), np.zeros(256, np.float32), np.full(256, 1.0, np.float32)
    from huggingface_hub import hf_hub_download
    from safetensors.numpy import load_file
    path = hf_hub_download(SAE_REPO, path_in_repo)
    p = load_file(path) if path.endswith(".safetensors") else dict(np.load(path))
    p = {k.lower().replace(".", "_"): v.astype(np.float32) for k, v in p.items()}
    pick = lambda *names: next((p[n] for n in names if n in p), None)
    Wd, b, t = pick("w_enc", "encoder_weight"), pick("b_enc", "encoder_bias"), pick("threshold", "log_threshold")
    if "log_threshold" in p and "threshold" not in p:
        t = np.exp(t)
    if Wd.shape[0] != W:
        Wd = Wd.T
    return Wd, b, t


def encode(x, sae):
    Wd, b, t = sae
    pre = x @ Wd + b
    return np.where(pre > (t if t is not None else 0), pre, 0.0)


# ---------------- the comparisons (all within request)
isB = EXP == "B"
COMPARISONS = {
    "B: UBS's loss frame vs gain frame": (isB & np.isin(VER, ["loss", "loss + you"]), isB & np.isin(VER, ["gain", "gain + you"])),
    "B: \"+ you\" vs no owner": (isB & np.isin(VER, ["loss + you", "gain + you"]), isB & np.isin(VER, ["loss", "gain"])),
    "B: framed vs neutral": (isB & (VER != "neutral"), isB & (VER == "neutral")),
    # within the same request, experiment and framing: the framing raises going along, so within request alone this
    # would partly repeat the framing comparisons
    "All experiments: went along vs did not (same request, experiment and framing)": (ASKED & JOINED, ASKED & ~JOINED, CELL),
    "A: a memo (loss, gain, + you) vs the neutral memo": ((EXP == "A") & ASKED & (VER != "neutral"), (EXP == "A") & (VER == "neutral")),
    "A: UBS's request vs the same moment without it": ((EXP == "A") & (VER == "neutral"), (EXP == "A") & ~ASKED),
    "Bank C: F vs B (same framings)": ((EXP == "F"), isB & np.isin(VER, list(set(VER[EXP == "F"])))),
}

report = ["# Inside the model at the push requests (full careers)\n",
          f"States: Gemma 3 12B at {PRECISION}, the last token before each push-request reply, {N} moments "
          f"({', '.join(f'{e}: {(EXP == e).sum()}' for e in sorted(set(EXP)))}). Every comparison is within the same "
          f"request (went along vs not: within the same request, experiment and framing); p-values reshuffle labels "
          f"within those groups ({PERMS} times); q = false-discovery-corrected. Features "
          "active in fewer than 5% of the moments compared are left out. Produced by "
          "`designs/rd2/analysis/inside_features.py`.\n"]
summary = {"precision": PRECISION, "moments": N, "comparisons": {}}

found = sae_layers()
report.append(f"Gemma Scope 2 ({SAE_REPO}, residual stream, {SAE_WIDTH}): layers {sorted(found)}; files "
              + ", ".join(f"`{v}`" for v in found.values()) + ".\n")
for layer, f in found.items():
    sae = load_sae(f)
    F = encode(X[:, layer], sae)
    for name, spec in COMPARISONS.items():
        a, b, S = spec if len(spec) == 3 else (*spec, REQ)
        if a.sum() < 6 or b.sum() < 6:
            continue
        both = a | b
        live = (F[both] > 0).mean(0) >= 0.05
        raw, z = strat_diff(F[:, live], a, b, S)
        _, p = strat_perm(F[:, live], a, b, S)
        q = fdr(p)
        ids = np.where(live)[0]
        order = np.argsort(-np.abs(z))[:TOP]
        rows = [{"feature": int(ids[k]), "standardised_difference": round(float(z[k]), 3),
                 "activation_difference": round(float(raw[k]), 3), "p": round(float(p[k]), 4), "q": round(float(q[k]), 4),
                 "neuronpedia": NEURONPEDIA.format(layer=layer, feature=int(ids[k]))} for k in order]
        summary["comparisons"].setdefault(name, {})[str(layer)] = {"n": [int(a.sum()), int(b.sum())],
                                                                   "features_tested": int(live.sum()),
                                                                   "q_below_0.05": int((q < 0.05).sum()), "top": rows}
    del F
for name in COMPARISONS:
    if name not in summary["comparisons"]:
        continue
    report.append(f"\n## {name}\n")
    for layer, res in summary["comparisons"][name].items():
        report.append(f"**Layer {layer}** ({res['n'][0]} vs {res['n'][1]} moments; {res['features_tested']} features "
                      f"tested; {res['q_below_0.05']} with q < 0.05)\n")
        report.append("| Feature | Difference (spread units) | Activation difference | p | q |\n|---|---|---|---|---|")
        for r in res["top"]:
            report.append(f"| [{r['feature']}]({r['neuronpedia']}) | {r['standardised_difference']:+.2f} | "
                          f"{r['activation_difference']:+.2f} | {r['p']:.4f} | {r['q']:.3f} |")
        report.append("")


# ---------------- the read-out: "went along" beyond the request and the framing
def logistic(Xtr, ytr, Xte, l2=1.0, steps=300, lr=0.1):
    w, b0 = np.zeros(Xtr.shape[1]), 0.0
    for _ in range(steps):
        p = 1 / (1 + np.exp(-(Xtr @ w + b0)))
        w -= lr * (Xtr.T @ (p - ytr) / len(ytr) + l2 * w / len(ytr))
        b0 -= lr * (p - ytr).mean()
    return 1 / (1 + np.exp(-(Xte @ w + b0)))


def auc(y, s):
    pos, neg = s[y], s[~y]
    if not len(pos) or not len(neg):
        return np.nan
    return (np.mean(pos[:, None] > neg[None, :]) + 0.5 * np.mean(pos[:, None] == neg[None, :]))


def cv_scores(feats, y, groups, folds=5, same_wants=None):
    """Held-out scores, folds by `groups` (the same fold split every call, so read-outs can be compared pairwise).
    With `same_wants`, each held-out group is scored by a read-out trained only on groups where UBS wants the same
    direction (going along means buying in one request and selling in another)."""
    careers = np.random.default_rng(0).permutation(np.unique(groups))
    s = np.zeros(len(y))
    for k in range(folds):
        test = np.isin(groups, careers[k::folds])
        train = ~test if same_wants is None else ~test & np.isin(same_wants, same_wants[test])
        mu, sd = feats[train].mean(0), feats[train].std(0) + 1e-6
        s[test] = logistic((feats[train] - mu) / sd, y[train].astype(float), (feats[test] - mu) / sd)
    return s


def cv_auc(feats, y, groups, folds=5, same_wants=None):
    return auc(y, cv_scores(feats, y, groups, folds, same_wants))


def rank_auc(y, s):
    r = np.argsort(np.argsort(s)) + 1.0
    n1 = y.sum()
    return (r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))


def boot_gain(y, s_with, s_without, groups, n=1000):
    """95% interval of AUC(with) - AUC(without), resampling careers."""
    careers = np.unique(groups)
    rows = [np.where(groups == c)[0] for c in careers]
    g = np.random.default_rng(1)
    out = []
    for _ in range(n):
        i = np.concatenate([rows[k] for k in g.integers(0, len(careers), len(careers))])
        out.append(rank_auc(y[i], s_with[i]) - rank_auc(y[i], s_without[i]))
    return np.percentile(out, [2.5, 97.5])


def centred(Z, mask):
    Z = Z.copy()
    for r in np.unique(REQ[mask]):
        i = mask & (REQ == r)
        Z[i] -= Z[i].mean(0)
    return Z


m = ASKED
y = JOINED[m]
labels = np.column_stack([REQ[m] == r for r in np.unique(REQ)] + [EXP[m] == e for e in np.unique(EXP)]
                         + [VER[m] == v for v in np.unique(VER)]).astype(float)
s_labels = cv_scores(labels, y, CAREER[m])
base = auc(y, s_labels)
report.append("\n## Can \"went along\" be read from the state, beyond the request and the framing?\n")
report.append(f"{m.sum()} moments with a request, {y.sum()} went along. Read-out scored on careers it was not trained on "
              f"(5 folds by career), and on a request it never saw (careers share chat lines, e.g. C clean = B neutral, so the "
              f"held-out request shows it is not learning the conversation). **The labels alone (request, experiment, "
              f"version) score AUC {base:.3f}.** States are "
              "centred within each request and reduced to 64 components per layer (fitted on all careers' states, no "
              "outcome used). \"Gain\" is state + labels minus labels alone, with a 95% interval from resampling careers "
              "(an interval above 0 means the state adds something). The held-out request is also scored by a read-out "
              "trained only on requests where UBS wants the same direction (going along is buying in some requests and "
              "selling in others).\n")
report.append("| Layer | AUC: state | AUC: state + labels | Gain over labels (95% interval) | AUC: a held-out request | "
              "AUC: a held-out request, same direction | AUC: state, outcomes reshuffled within request |\n"
              "|---|---|---|---|---|---|---|")
readout = {}
for layer in range(0, L, 3):
    Z = centred(X[:, layer], m)[m]
    U = np.linalg.svd(Z - Z.mean(0), full_matrices=False)[2][:64]       # components (all careers: no outcome used)
    P = Z @ U.T
    a1 = cv_auc(P, y, CAREER[m])
    s2 = cv_scores(np.column_stack([P, labels]), y, CAREER[m])
    a2 = auc(y, s2)
    lo, hi = boot_gain(y, s2, s_labels, CAREER[m])
    a4 = cv_auc(P, y, REQ[m], folds=len(np.unique(REQ[m])))     # trained on five requests, scored on the sixth
    a5 = cv_auc(P, y, REQ[m], folds=len(np.unique(REQ[m])), same_wants=WANTS[m])
    y_null = y.copy()
    for r in np.unique(REQ[m]):
        i = REQ[m] == r
        y_null[i] = RNG.permutation(y_null[i])
    a3 = cv_auc(P, y_null, CAREER[m])
    readout[layer] = {"state": a1, "state_labels": a2, "gain_interval": [lo, hi], "held_out_request": a4,
                      "held_out_request_same_direction": a5, "reshuffled": a3}
    report.append(f"| {layer} | {a1:.3f} | {a2:.3f} | {a2 - base:+.3f} ({lo:+.3f} to {hi:+.3f}) | {a4:.3f} | {a5:.3f} | {a3:.3f} |")
summary["readout"] = {"labels_only_auc": base, "by_layer": readout}

# ---------------- Bank C, paired with the B twins at 7 Jan
report.append("\n## Bank C at 7 Jan, paired with each career's B twin\n")
pairs = []
for i in np.where((EXP == "F") & (REQ == "p344_i_can_hunt_with_u"))[0]:
    j = np.where(isB & (REQ == "p344_i_can_hunt_with_u") & (VER == VER[i])
                 & (np.array([mm["run"] for mm in META]) == META[i]["run"]))[0]
    if len(j):
        pairs.append((i, j[0]))
if pairs:
    report.append(f"{len(pairs)} pairs (twins share a seed, but on the saved transcripts every pair differs from the first "
                  "reply, so this is not Bank C's line alone). The size of the state change, by layer, against the change "
                  "between two B careers of the same version at the same moment:\n")
    report.append("| Layer | Bank C: mean change (F minus its twin) | Two B careers of the same version |\n|---|---|---|")
    for layer in range(0, L, 6):
        d_pair = np.mean([np.linalg.norm(X[i, layer] - X[j, layer]) for i, j in pairs])
        sib = [np.linalg.norm(X[a, layer] - X[b, layer]) for a in np.where(isB & (REQ == "p344_i_can_hunt_with_u"))[0]
               for b in np.where(isB & (REQ == "p344_i_can_hunt_with_u"))[0] if a < b and VER[a] == VER[b]]
        report.append(f"| {layer} | {d_pair:.1f} | {np.mean(sib):.1f} |")
    report.append("\nWhere the first column is no larger than the second, F's state is no further from its twin than two "
                  "B careers are from each other.")

open(os.path.join(OUT, f"INSIDE_{PRECISION}.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, f"inside_{PRECISION}.json"), "w"), indent=1)
print("written", os.path.join(OUT, f"INSIDE_{PRECISION}.md"))
