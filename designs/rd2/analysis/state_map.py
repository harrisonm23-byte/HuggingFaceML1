"""Where the injected states sit at layer 22: the emotion documents, the financial documents and UBS's framed lines on
one map, and the Gemma Scope 2 features each direction points along.

    python designs/rd2/analysis/state_map.py <folder of downloaded vectors> <folder with the layer-22 dictionary>

Vectors (from the rd2-states volume, v2/): layer_scan_18_21_sweep/shifts.npz (the emotion document states, the ones
notebook 31 injected; 20 moments x 4 themes x 20 layers), layer_scan_18_21_fin_sweep/shifts.npz (the financial
documents), frame_states/shifts.npz (UBS's framed request minus the neutral one at the same 20 moments, "after" and
"whole"; layers 12, 22, 24). Each direction is the mean over the 20 moments, exactly as it was injected (state_careers
.build_arms, frame_states.pooled). The random direction is build_arms's (seed 20261022 + layer).

Cosine: 1 = the same direction, 0 = unrelated, -1 = opposite. "One scale": every dimension divided by its spread over
the per-moment vectors of all sources first (a few huge dimensions dominate Gemma's residual stream and can make raw
cosines misleading). Each source's ceiling is its cosine with itself built on two halves of the careers. The picture is
classical MDS of the one-scale cosines. Features: the Gemma Scope 2 layer-22 residual dictionary (16k, l0 small)'s
decoder directions most aligned with each unit direction, as trace.py did at layer 24; Neuronpedia does not host this
layer, so each feature is labelled here from the dictionary's own examples (its top-activating texts and the output
tokens it boosts).
"""
import json, os, sys
import numpy as np

VEC, SAE_DIR = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..",
                                                         "results", "state_map")
TOKENIZER = sys.argv[4] if len(sys.argv) > 4 else os.path.join(SAE_DIR, "tokenizer.json")   # Gemma 3's tokenizer.json
L = 22
RANDOM_SEED = 20261022
os.makedirs(OUT, exist_ok=True)
cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
unit = lambda v: v / np.linalg.norm(v)


def career_of(meta):
    return np.array([int(m["career_file"].split("_r")[1].split(".")[0]) for m in meta])


# ---------------- the per-moment vectors at layer 22
per = {}                                           # name -> (moments x width), careers
z = np.load(os.path.join(VEC, "layer_scan_18_21_sweep.npz"))
j = list(z["layers"]).index(L)
cars = career_of(json.loads(str(z["meta"])))
for a, t in enumerate(z["themes"]):
    per[f"{t} document"] = (z["shifts"][:, a, j].astype(np.float64), cars)
z = np.load(os.path.join(VEC, "layer_scan_18_21_fin_sweep.npz"))
j = list(z["layers"]).index(L)
cars = career_of(json.loads(str(z["meta"])))
for a, t in enumerate(z["themes"]):
    per[f"financial {t} document"] = (z["shifts"][:, a, j].astype(np.float64), cars)
z = np.load(os.path.join(VEC, "frame_states_shifts.npz"))
j = list(z["layers"]).index(L)
FRAME_NAME = {"loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit"}
for a, f in enumerate(z["frames"]):
    for b, kind in enumerate(z["kinds"]):
        per[f"UBS {FRAME_NAME[str(f)]} line, {kind}"] = (z["shifts"][:, a, b, j].astype(np.float64), np.asarray(z["runs"]))
ORDER = [f"{t} document" for t in ("loss", "blame", "gain", "credit")] + \
        [f"financial {t} document" for t in ("loss", "gain")] + \
        [f"UBS {t} line, after" for t in ("loss", "blame", "gain", "credit")] + \
        [f"UBS {t} line, whole" for t in ("loss", "blame", "gain", "credit")]
assert set(ORDER) == set(per), sorted(per)
vec = {k: per[k][0].mean(0) for k in ORDER}
size = {k: float(np.linalg.norm(vec[k])) for k in ORDER}
width = len(next(iter(vec.values())))
r = np.random.default_rng(RANDOM_SEED + L).normal(size=width)
vec["random direction"] = r / np.linalg.norm(r) * np.mean([size[k] for k in ORDER if k.endswith("document")])
ALL = ORDER + ["random direction"]

# the dimensions' spread, pooled over every source's per-moment vectors (each source centred)
scale = np.sqrt(np.concatenate([x - x.mean(0) for x, _ in per.values()]).__pow__(2).mean(0)) + 1e-6
ceiling = {}
for k in ORDER:
    x, c = per[k]
    half = (c % 2) == 0
    ceiling[k] = (cos(x[half].mean(0), x[~half].mean(0)),
                  cos(x[half].mean(0) / scale, x[~half].mean(0) / scale))

# ---------------- the report
report = [f"# Where the states sit: layer {L} (exploratory)\n",
          "Produced by `designs/rd2/analysis/state_map.py`. Each direction is exactly the vector the runs injected "
          "(the mean over B's 20 neutral-career moments at the 7 and 12 January requests): the four emotion documents "
          "(notebook 31 and the direct request), the two financial documents, and UBS's framed line minus the neutral "
          "line at the same moment (\"after\": read on the tokens after the framed words, the construction that "
          "worked; \"whole\": the update's average, which did nothing). Cosine: 1 = the same direction, 0 = unrelated, "
          f"-1 = opposite; unrelated directions fall within about +/-{2 / np.sqrt(width):.3f}. \"One scale\": every "
          "dimension divided by its spread over the per-moment vectors first. \"Ceiling\": the direction built on "
          "two halves of the careers, against itself (how stable it is; cosines between two sources cannot be read "
          "above their ceilings).\n",
          "## Sizes and stability\n", "| Direction | Size (x1) | Ceiling | Ceiling, one scale |", "|---|---|---|---|"]
for k in ORDER:
    report.append(f"| {k} | {size[k]:.1f} | {ceiling[k][0]:+.3f} | {ceiling[k][1]:+.3f} |")
SHORT = {k: k.replace(" document", " doc").replace("UBS ", "").replace(" line, ", " ").replace("financial", "fin")
         for k in ALL}
SHORT["random direction"] = "random"
for title, f in [("Cosines (raw)", lambda a, b: cos(vec[a], vec[b])),
                 ("Cosines, one scale", lambda a, b: cos(vec[a] / scale, vec[b] / scale))]:
    report += [f"\n## {title}\n", "| | " + " | ".join(SHORT[k] for k in ALL) + " |", "|---|" + "---|" * len(ALL)]
    for a in ALL:
        report.append(f"| {SHORT[a]} | " + " | ".join("" if a == b else f"{f(a, b):+.2f}" for b in ALL) + " |")
C = np.array([[cos(vec[a] / scale, vec[b] / scale) for b in ALL] for a in ALL])
summary = {"sizes": size, "ceiling": ceiling, "cosine_raw": {a: {b: cos(vec[a], vec[b]) for b in ALL} for a in ALL},
           "cosine_one_scale": {a: {b: float(C[i, j]) for j, b in enumerate(ALL)} for i, a in enumerate(ALL)}}

# the twin pairs, side by side
TWINS = [("loss", "loss"), ("blame", "blame"), ("gain", "gain"), ("credit", "credit")]
report += ["\n## Each UBS line against its document twin, and against the other documents (one scale)\n",
           "| UBS line (after) | Its twin document | Nearest document | Nearest of anything | Farthest |", "|---|---|---|---|---|"]
for f, d in TWINS:
    a = f"UBS {f} line, after"
    i = ALL.index(a)
    docs = [k for k in ORDER if k.endswith("document")]
    near_doc = max(docs, key=lambda k: C[i, ALL.index(k)])
    others = [k for k in ALL if k != a]
    near, far = max(others, key=lambda k: C[i, ALL.index(k)]), min(others, key=lambda k: C[i, ALL.index(k)])
    report.append(f"| {f} | {d} document: {C[i, ALL.index(d + ' document')]:+.2f} | {SHORT[near_doc]} "
                  f"{C[i, ALL.index(near_doc)]:+.2f} | {SHORT[near]} {C[i, ALL.index(near)]:+.2f} | {SHORT[far]} "
                  f"{C[i, ALL.index(far)]:+.2f} |")

# robustness: the same picture with the largest dimensions simply dropped
rows = []
for n_drop in (8, 32):
    keep = np.ones(width, bool)
    keep[np.argsort(-np.abs(vec["loss document"]))[:n_drop]] = False
    ck = lambda a, b: cos(vec[a][keep], vec[b][keep])
    rows.append(f"dropping {n_drop}: loss document vs UBS loss line (after) {ck('loss document', 'UBS loss line, after'):+.2f}, "
                f"blame document vs UBS blame line {ck('blame document', 'UBS blame line, after'):+.2f}, loss vs gain "
                f"document {ck('loss document', 'gain document'):+.2f}, UBS loss vs gain line "
                f"{ck('UBS loss line, after', 'UBS gain line, after'):+.2f}")
report.append("\nThe same picture when the largest dimensions are dropped instead of every dimension rescaled: "
              + "; ".join(rows) + ".")

# the emotion with the kind of input removed: contrasts within each family, compared across families
CONTRASTS = [("loss - gain", ("loss", "gain")), ("blame - credit", ("blame", "credit")),
             ("blame - loss (the \"you\" in a loss)", ("blame", "loss")),
             ("credit - gain (the \"you\" in a gain)", ("credit", "gain"))]
FAMILY = {"documents": "{} document", "financial documents": "financial {} document", "UBS lines, after": "UBS {} line, after",
          "UBS lines, whole": "UBS {} line, whole"}
report += ["\n## The emotion alone: contrasts within each family, compared across families (one scale)\n",
           "Within a family the four directions are nearly the same (the kind of input sets the direction), so the "
           "emotion is what is left when one is subtracted from another. Each contrast is built per moment and "
           "averaged; its ceiling is the contrast on two halves of the careers against itself. A cosine between two "
           "families well below both ceilings means they do not share the emotion's direction either.\n",
           "| Contrast | Documents, ceiling | UBS after, ceiling | Documents vs UBS after | Documents vs financial "
           "documents | UBS after vs UBS whole |", "|---|---|---|---|---|---|"]
summary["contrasts"] = {}


def contrast(fam, a, b):
    ka, kb = FAMILY[fam].format(a), FAMILY[fam].format(b)
    if ka not in per or kb not in per:
        return None
    x, c = per[ka][0] - per[kb][0], per[ka][1]
    assert (per[kb][1] == c).all()
    return x, c


for name, (a, b) in CONTRASTS:
    d, u, fin, w = contrast("documents", a, b), contrast("UBS lines, after", a, b), \
        contrast("financial documents", a, b), contrast("UBS lines, whole", a, b)
    ceil = lambda x: cos(x[0][(x[1] % 2) == 0].mean(0) / scale, x[0][(x[1] % 2) == 1].mean(0) / scale)
    cc = lambda x, y: "" if x is None or y is None else f"{cos(x[0].mean(0) / scale, y[0].mean(0) / scale):+.3f}"
    report.append(f"| {name} | {ceil(d):+.2f} | {ceil(u):+.2f} | {cc(d, u)} | {cc(d, fin)} | {cc(u, w)} |")
    summary["contrasts"][name] = {"doc_ceiling": ceil(d), "ubs_ceiling": ceil(u), "doc_vs_ubs": cc(d, u),
                                  "doc_vs_fin": cc(d, fin), "after_vs_whole": cc(u, w)}

# ---------------- the picture: classical MDS of the one-scale cosines
D2 = (1 - C) ** 2
n = len(ALL)
J = np.eye(n) - 1 / n
B = -0.5 * J @ D2 @ J
w, V = np.linalg.eigh(B)
idx = np.argsort(-w)[:2]
XY = V[:, idx] * np.sqrt(np.maximum(w[idx], 0))
share = np.maximum(w, 0)[idx] / np.maximum(w, 0).sum()
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 6))
    COL = {"document": "#1f77b4", "financial": "#2ca02c", "after": "#d62728", "whole": "#ff9896", "random": "#7f7f7f"}
    for i, k in enumerate(ALL):
        kind = "financial" if k.startswith("financial") else "document" if k.endswith("document") else \
            "after" if k.endswith("after") else "whole" if k.endswith("whole") else "random"
        ax.scatter(XY[i, 0], XY[i, 1], s=60, color=COL[kind], zorder=3)
        ax.annotate(SHORT[k], (XY[i, 0], XY[i, 1]), xytext=(5, 4), textcoords="offset points", fontsize=9)
    ax.set_title(f"Injected directions at layer {L}, by angle (MDS of one-scale cosines; "
                 f"{100 * share.sum():.0f}% of the spread shown)")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks([])
    ax.set_yticks([])
    for kind, lab in [("document", "emotion documents"), ("financial", "financial documents"),
                      ("after", "UBS's lines (after)"), ("whole", "UBS's lines (whole)"), ("random", "random")]:
        ax.scatter([], [], color=COL[kind], label=lab)
    ax.legend(loc="best", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, f"state_map_L{L}.png"), dpi=150)
    report.append(f"\n![map](state_map_L{L}.png)\n")
except ImportError:
    report.append("\n(matplotlib not available: no picture)\n")
summary["mds"] = {k: [float(XY[i, 0]), float(XY[i, 1])] for i, k in enumerate(ALL)}

# ---------------- the features: Gemma Scope 2, layer 22, decoder directions
from safetensors import safe_open
with safe_open(os.path.join(SAE_DIR, "params.safetensors"), "np") as f:
    Wd = f.get_tensor("w_dec")                          # features x width
Dn = Wd / np.linalg.norm(Wd, axis=1, keepdims=True)
Ds = Wd / scale
Ds /= np.linalg.norm(Ds, axis=1, keepdims=True)
# how much a few dimensions carry: the raw alignment names the features that live on them, whatever the direction
big = np.argsort(-np.abs(vec["loss document"]))[:8]
big_share = {k: float((vec[k][big] ** 2).sum() / (vec[k] ** 2).sum()) for k in ORDER}
feat_on_big = float(((Dn[:, big] ** 2).sum(1) > 0.5).mean())
ex = safe_open(os.path.join(SAE_DIR, "examples.safetensors"), "np")
tok = None
try:
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(TOKENIZER)
except Exception as err:
    print("no tokenizer, labels will be token ids:", err)
_tokens = ex.get_slice("tokens")
_top = ex.get_tensor("top_tokens")
_acts, _seq, _pos = ex.get_tensor("activations"), ex.get_tensor("seq_ids"), ex.get_tensor("positions")
freq = ex.get_tensor("feature_frequencies")
dec = lambda ids: tok.decode([int(i) for i in ids]).replace("\n", " ") if tok else " ".join(str(i) for i in ids)


def label(i, n_ex=3, ctx=8):
    """The feature's top-activating texts (the activating token in [brackets]) and the output tokens it boosts."""
    order = np.argsort(-_acts[i])[:n_ex]
    seen, texts = set(), []
    for o in order:
        s, p = int(_seq[i, o]), int(_pos[i, o])
        if s < 0 or _acts[i, o] <= 0:
            continue
        row = _tokens[s:s + 1][0]
        lo = max(0, p - ctx)
        t = dec(row[lo:p]) + "[" + dec(row[p:p + 1]) + "]"
        if t not in seen:
            seen.add(t)
            texts.append(t.strip())
    boosts = dec(_top[i][:6]) if tok else ""
    return " / ".join(f"“{t}”" for t in texts) + (f"; boosts: {boosts}" if boosts else "")


def features(v, k=10, scaled=True):
    sc = (Ds @ unit(v / scale)) if scaled else (Dn @ unit(v))
    top, bot = np.argsort(-sc)[:k], np.argsort(sc)[:k]
    return [(int(i), float(sc[i])) for i in top], [(int(i), float(sc[i])) for i in bot]


raw_top = {k: {i for i, _ in features(vec[k], 10, scaled=False)[0]} | {i for i, _ in features(vec[k], 10, scaled=False)[1]}
           for k in ORDER}
raw_common = set.intersection(*[raw_top[k] for k in ORDER if k.endswith("document") or k.endswith("after")])
report += [f"\n## Gemma Scope 2 features (layer {L}, 16k) most aligned with each direction\n",
           "The dictionary's decoder directions against each unit direction (cosine, one scale as above); the "
           "direction is a change, not a state, so this names what it points along, not what fires. Labels are the "
           "feature's top-activating texts from the dictionary's own examples (activating token in [brackets]) and "
           "the output tokens it boosts; `freq` is how often the feature fires in ordinary text. Raw cosines are not "
           f"used here: {len(big)} of the {width} dimensions carry {100 * min(big_share.values()):.0f}-"
           f"{100 * max(big_share.values()):.0f}% of each direction's squared length, {100 * feat_on_big:.0f}% of the "
           f"dictionary's features sit mostly on those dimensions, and the raw alignment returns the same features "
           f"for every direction ({len(raw_common)} of the top 20 shared by all documents and UBS lines, with the sign "
           "flipped between the families).\n"]
summary["features"] = {}
for k in ORDER + ["random direction"]:
    top, bot = features(vec[k])
    report += [f"\n### {k}\n", "| Along it | Cosine | freq | What the feature responds to |", "|---|---|---|---|"]
    for i, s in top:
        report.append(f"| {i} | {s:+.3f} | {freq[i]:.1e} | {label(i)} |")
    report += ["", "| Against it | Cosine | freq | What the feature responds to |", "|---|---|---|---|"]
    for i, s in bot:
        report.append(f"| {i} | {s:+.3f} | {freq[i]:.1e} | {label(i)} |")
    summary["features"][k] = {"along": top, "against": bot}
    # overlap of the top-20 feature sets between a UBS line and its twin document
report += ["\n## Shared features: each UBS line (after) and its document twin\n",
           "Of each one's 20 most aligned features (along and against, 10 each), how many the other shares, with the "
           "sign kept; and the features of their difference (the line's unit direction minus the document's).\n"]
for f, d in TWINS:
    a, b = f"UBS {f} line, after", f"{d} document"
    ta, tb = features(vec[a], 20), features(vec[b], 20)
    along_a, along_b = {i for i, _ in ta[0]}, {i for i, _ in tb[0]}
    against_a, against_b = {i for i, _ in ta[1]}, {i for i, _ in tb[1]}
    shared = (along_a & along_b) | (against_a & against_b)
    crossed = (along_a & against_b) | (against_a & along_b)
    report.append(f"- **{f}**: shared {len(shared)} of 20 ({sorted(shared)}); with the opposite sign {len(crossed)} "
                  f"({sorted(crossed)}).")
    diff = unit(vec[a]) - unit(vec[b])
    top, bot = features(diff, 6)
    report.append(f"  - the line has, the document lacks: " + "; ".join(f"{i} ({s:+.2f}) {label(i, 2, 6)}" for i, s in top))
    report.append(f"  - the document has, the line lacks: " + "; ".join(f"{i} ({s:+.2f}) {label(i, 2, 6)}" for i, s in bot))
    summary["features"][f"{f}: line minus document"] = {"shared": sorted(shared), "crossed": sorted(crossed),
                                                       "along": top, "against": bot}

open(os.path.join(OUT, "STATE_MAP.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "state_map.json"), "w"), indent=1, default=float)
print("\n".join(report[:60]))
print("written", os.path.join(OUT, "STATE_MAP.md"))
