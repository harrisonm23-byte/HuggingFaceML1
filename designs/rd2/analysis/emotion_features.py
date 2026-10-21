"""What the author's emotion documents activate inside the model: the analysis (exploratory; the user, 22 Oct).

    python designs/rd2/analysis/emotion_features.py <features npz from scripts/modal_emotion_features.py> <output dir>

For each layer (12, 24, 31, 41) and each contrast (each emotion against the neutral documents; loss against gain; blame
against loss; credit against gain): the Gemma Scope 2 features whose mean activation over a document's tokens differs
most between the two document types; p by reshuffling which documents belong to which type (2,000 times), with a
false-discovery-rate correction over the features active in either type. Then, for loss against gain: do the features
that separate the documents also separate UBS's loss request from its gain request at the same moment (B's matched
rereads, the decision token)? Feature names come from Neuronpedia where it has one.
"""
import json, math, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "sim"))
sys.path.insert(0, os.path.join(os.getcwd(), "sim"))
from gemma_scope import NEURONPEDIA, WANT_LAYERS

NPZ, OUT = sys.argv[1], sys.argv[2]
PERMS, TOP, Q = 2000, 12, 0.05
RNG = np.random.default_rng(20261022)
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
CONTRASTS = [("loss", "neutral"), ("blame", "neutral"), ("gain", "neutral"), ("credit", "neutral"),
             ("loss", "gain"), ("blame", "loss"), ("credit", "gain")]
os.makedirs(OUT, exist_ok=True)
z = np.load(NPZ)
theme = np.array([m["theme"] for m in json.loads(str(z["meta"]))])
umeta = json.loads(str(z["umeta"]))


def bh(p):
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.minimum(q, 1)


def pq(obs, null):
    """Two-sided p from the reshuffled differences, read off a normal fitted to them (8,000 features need p-values
    smaller than a few thousand reshuffles can show), and the false-discovery q."""
    z = obs / (null.std(0) + 1e-12)
    p = np.array([math.erfc(abs(v) / math.sqrt(2)) for v in z])
    return p, bh(p)


def contrast(X, a, b):
    """(features tested, difference, p, q) for document type a minus b; X: documents x features."""
    A, B = X[theme == a], X[theme == b]
    live = np.where((A > 0).any(0) | (B > 0).any(0))[0]
    Y = np.concatenate([A[:, live], B[:, live]])
    n = len(A)
    obs = Y[:n].mean(0) - Y[n:].mean(0)
    null = np.stack([(lambda o: Y[o[:n]].mean(0) - Y[o[n:]].mean(0))(RNG.permutation(len(Y))) for _ in range(PERMS)])
    return live, obs, *pq(obs, null)


_names = {}


def name(L, f):
    if os.environ.get("NO_NAMES") == "1":
        return ""
    url = f"https://www.neuronpedia.org/api/feature/gemma-3-12b-it/{L}-gemmascope-2-res-16k/{f}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            d = json.load(r)
        ex = d.get("explanations") or []
        return (ex[0].get("description") or "").strip() if ex else ""
    except Exception:
        return ""


def names(pairs):
    todo = [p for p in pairs if p not in _names]
    with ThreadPoolExecutor(16) as ex:
        for p, n in zip(todo, ex.map(lambda p: name(*p), todo)):
            _names[p] = n


report = ["# What the emotion documents activate inside the model (exploratory)\n",
          f"{len(theme)} documents ({', '.join(f'{t} {int((theme == t).sum())}' for t in dict.fromkeys(theme))}), each "
          "read on its own by Gemma 3 12B (bfloat16). Every token's state passed through the Gemma Scope 2 dictionary "
          "(16k, residual stream); a document's activation of a feature is its mean over the document's tokens. "
          f"p reshuffles which documents belong to which type ({PERMS:,} times, read off a normal fitted to the reshuffled differences); q is false-discovery corrected over the "
          "features active in either type. Names are Neuronpedia's automatic descriptions where it has one; every "
          "feature links to its page. Produced by `designs/rd2/analysis/emotion_features.py`.\n"]
summary = {}
for L in WANT_LAYERS:
    X = z[f"doc_{L}"][:, 0]                                         # documents x features: mean activation
    on = z[f"doc_{L}"][:, 1]                                        # share of tokens on
    report.append(f"\n## Layer {L}\n")
    summary[L] = {}
    for a, b in CONTRASTS:
        live, d, p, q = contrast(X, a, b)
        sig = q < Q
        up = [i for i in np.argsort(-d) if sig[i] and d[i] > 0][:TOP]
        down = [i for i in np.argsort(d) if sig[i] and d[i] < 0][:TOP]
        names([(L, int(live[i])) for i in up + down])
        summary[L][f"{a} vs {b}"] = {"tested": int(len(live)), "q<0.05": int(sig.sum()),
                                     "up": [int(live[i]) for i in up], "down": [int(live[i]) for i in down]}
        report.append(f"**{a.capitalize()} documents against {b} documents** ({len(live)} features active; "
                      f"{int(sig.sum())} differ at q < {Q}; {int((sig & (d > 0)).sum())} more active in {a}, "
                      f"{int((sig & (d < 0)).sum())} in {b})\n")
        if up or down:
            report.append(f"| More active in {a} | Activation ({a} / {b}) | Share of {a} tokens on | Description |"
                          "\n|---|---|---|---|")
            for i in up:
                f = int(live[i])
                report.append(f"| [{f}]({NEURONPEDIA.format(layer=L, feature=f)}) | "
                              f"{X[theme == a, f].mean():.1f} / {X[theme == b, f].mean():.1f} | "
                              f"{100 * on[theme == a, f].mean():.0f}% | {_names.get((L, f), '')} |")
            report.append("")
            report.append(f"| More active in {b} | Activation ({a} / {b}) | Share of {b} tokens on | Description |"
                          "\n|---|---|---|---|")
            for i in down:
                f = int(live[i])
                report.append(f"| [{f}]({NEURONPEDIA.format(layer=L, feature=f)}) | "
                              f"{X[theme == a, f].mean():.1f} / {X[theme == b, f].mean():.1f} | "
                              f"{100 * on[theme == b, f].mean():.0f}% | {_names.get((L, f), '')} |")
            report.append("")

    # do the documents' loss-vs-gain features also separate UBS's loss request from its gain request?
    U = z[f"ubs_{L}"]                                               # moments x 10 versions x features
    idx = {(m["framing"], m["bank_c"]): k for k, m in enumerate(umeta[0])}
    g = lambda v: U[:, idx[(v, False)]]
    ud = (g("loss") + g("loss + you") - g("gain") - g("gain + you")) / 2  # moments x features
    careers = np.array([m[0]["career_file"] for m in umeta])
    cm = np.stack([ud[careers == c].mean(0) for c in np.unique(careers)])
    obs = cm.mean(0)
    live_u = np.where((U > 0).any((0, 1)))[0]
    null = np.stack([(RNG.choice([-1, 1], (len(cm), 1)) * cm[:, live_u]).mean(0) for _ in range(PERMS)])
    qu = pq(obs[live_u], null)[1]
    ubs_up = set(live_u[(qu < Q) & (obs[live_u] > 0)].tolist())
    ubs_down = set(live_u[(qu < Q) & (obs[live_u] < 0)].tolist())
    live, d, p, q = contrast(X, "loss", "gain")
    doc_up = set(live[(q < Q) & (d > 0)].tolist())
    doc_down = set(live[(q < Q) & (d < 0)].tolist())
    both = np.intersect1d(live, live_u)
    n = len(both)
    exp_same = (len(doc_up & set(both)) * len(ubs_up & set(both)) + len(doc_down & set(both)) * len(ubs_down & set(both))) / max(n, 1)
    same = len(doc_up & ubs_up) + len(doc_down & ubs_down)
    opposite = len(doc_up & ubs_down) + len(doc_down & ubs_up)
    pos = {f: i for i, f in enumerate(live)}
    r = np.corrcoef(d[[pos[f] for f in both]], obs[both])[0, 1] if n > 2 else float("nan")
    report.append(f"**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, "
                  f"{len(umeta)} moments, history held fixed; p flips signs by career): {len(ubs_up) + len(ubs_down)} "
                  f"features separate UBS's loss request from its gain request at q < {Q}. Of the features that separate "
                  f"both, {same} point the same way (about {exp_same:.1f} expected by chance) and {opposite} the opposite "
                  f"way. Correlation of the two differences over the {n} features active in both: {r:+.2f}.\n")
    shared = sorted(doc_up & ubs_up, key=lambda f: -obs[f])[:TOP]
    if shared:
        names([(L, f) for f in shared])
        report.append("| Shared: more active under loss in both | Description |\n|---|---|")
        report += [f"| [{f}]({NEURONPEDIA.format(layer=L, feature=f)}) | {_names.get((L, f), '')} |" for f in shared]
        report.append("")
    summary[L]["vs UBS"] = {"ubs_features": len(ubs_up) + len(ubs_down), "same": same, "opposite": opposite,
                            "expected_same": exp_same, "correlation": float(r), "shared_up": [int(f) for f in shared]}

open(os.path.join(OUT, "FEATURES.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "features.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "FEATURES.md"))
