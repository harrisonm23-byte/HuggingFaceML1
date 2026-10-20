"""Same moment, different frame: the analysis of scripts/modal_matched.py (the user, 20 Oct).

    python designs/rd2/analysis/matched_history.py <states root, e.g. /states/v2> <output dir>

Every B moment (50 careers x 6 push requests) was read in 10 versions that differ only in UBS's current request (five
framings) and whether Bank C's line follows it. Within a moment the history is identical, so a difference between
versions is the request's own effect; between careers (same request version, different histories) it is the history's.

1. What it would do: P(the order goes along) by history and by request; the request's effect (paired within moments),
   the history's (between careers), and Bank C's line alone. p: signs flipped by career (paired) or careers reshuffled
   between groups (unpaired), 10,000 times; 95% intervals from resampling careers.
2. The state: the size of each change by layer; the frame direction measured with the history held fixed, against
   the one measured across careers (Run 1, which the steering used); Bank C's change along it.
3. Gemma Scope features: loss vs gain request, "you" after loss and after gain, and Bank C's line, paired within
   moments (signs flipped by career, false-discovery corrected), with the overlap with Run 1's loss-vs-gain features.
"You" after loss and after gain (the user, 20 Oct): after loss, "you" may read as blame; after gain, as credit. So the
change "+ you" makes is measured separately in each frame, in what the agent would do, in the state (are the two changes
alike?) and in the features, and the two are compared (B's preregistered H3, here with the history held fixed).
Check: the "as saved" version (the career's own framing, no Bank C) against Run 1's state for the same moment.
"""
import glob, json, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "sim"))
from gemma_scope import NEURONPEDIA, encode, load_sae, sae_layers

ROOT, OUT = sys.argv[1], sys.argv[2]
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
LOSS, GAIN, YOU, NOYOU = ["loss", "loss + you"], ["gain", "gain + you"], ["loss + you", "gain + you"], ["loss", "gain"]
PERMS, BOOT, FEATURE_PERMS, TOP = 10000, 2000, 1000, 15
RNG = np.random.default_rng(20261020)
os.makedirs(OUT, exist_ok=True)

# ---------------- load: moments x framing x Bank C (x layers x width for the states)
rows, S, layers = [], [], None
for f in sorted(glob.glob(os.path.join(ROOT, "matched", "B_bf16", "*.npz"))):
    z = np.load(f)
    r = json.loads(str(z["meta"]))
    assert [(x["framing"], x["bank_c"]) for x in r] == [(v, b) for v in FRAMINGS for b in (False, True)]
    rows.append(r)
    S.append(z["states"].reshape(len(FRAMINGS), 2, *z["states"].shape[1:]))
    layers = [int(l) for l in z["layers"]]
assert rows, "no matched-history states: run scripts/modal_matched.py first"
S = np.stack(S)                                                  # M x 5 x 2 x layers x width
assert np.isfinite(S).all()
M = len(rows)
P = np.array([[[x["p_order_along"] for x in r[2 * i:2 * i + 2]] for i in range(len(FRAMINGS))] for r in rows])
COV = np.array([[x["coverage"] for x in r] for r in rows])
HIST = np.array([r[0]["history"] for r in rows])
CAREER = np.array([r[0]["career_file"] for r in rows])
CHAT = np.array([r[0]["chat"] for r in rows])
fi = {v: i for i, v in enumerate(FRAMINGS)}
cols = lambda vs: [fi[v] for v in vs]
careers = np.unique(CAREER)
report = ["# Same moment, different frame (B's moments, history held fixed)\n",
          f"{M} moments ({len(careers)} careers x their push requests), each read in 10 versions: UBS's request in the "
          "five framings, each with and without Bank C's line; everything before the request is the saved career, "
          "unchanged. Gemma 3 12B at bfloat16. Produced by `designs/rd2/analysis/matched_history.py`.\n"]
summary = {"moments": M}


# ---------------- tests
def by_career(d):
    return np.array([d[CAREER == c].mean() for c in careers])


def paired(d):
    """Mean of a per-moment difference; p by flipping signs by career; 95% interval by resampling careers."""
    c = by_career(d)
    obs = c.mean()
    flips = RNG.choice([-1, 1], (PERMS, len(c)))
    p = (np.sum(np.abs((flips * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    boot = [c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)]
    return obs, p, np.percentile(boot, [2.5, 97.5])


def unpaired(value, group_a, group_b):
    """Careers in group a minus group b (each career's mean over its moments); careers reshuffled between the groups."""
    va = np.array([value[CAREER == c].mean() for c in careers if HIST[CAREER == c][0] in group_a])
    vb = np.array([value[CAREER == c].mean() for c in careers if HIST[CAREER == c][0] in group_b])
    obs, both = va.mean() - vb.mean(), np.concatenate([va, vb])
    hits = 0
    for _ in range(PERMS):
        x = RNG.permutation(both)
        hits += abs(x[:len(va)].mean() - x[len(va):].mean()) >= abs(obs) - 1e-12
    boot = [va[RNG.integers(0, len(va), len(va))].mean() - vb[RNG.integers(0, len(vb), len(vb))].mean() for _ in range(BOOT)]
    return obs, (hits + 1) / (PERMS + 1), np.percentile(boot, [2.5, 97.5])


line = lambda name, r: f"| {name} | {100 * r[0]:+.1f} points | {100 * r[2][0]:+.1f} to {100 * r[2][1]:+.1f} | {r[1]:.4f} |"

# ---------------- 1. what it would do
report.append("\n## 1. What it would do: P(the order goes along)\n")
report.append(f"After a fixed neutral reasoning line, the probability of HOLD and of every order size the agents "
              f"used (both signs), and the share of it on orders that go along. Coverage, the share of all probability "
              f"those orders take: median {np.median(COV):.2f}, lowest {COV.min():.2f}.\n")
for bc in (False, True):
    report.append(f"\n**{'With' if bc else 'Without'} Bank C's line.** Rows: the career's own framing (its history); "
                  "columns: the framing of UBS's request at this moment. The diagonal is the career as saved"
                  + (" plus Bank C" if bc else "") + ".\n")
    report.append("| History \\ request | " + " | ".join(FRAMINGS) + " |\n" + "|---" * (len(FRAMINGS) + 1) + "|")
    for h in FRAMINGS:
        report.append(f"| {h} | " + " | ".join(f"{100 * P[HIST == h, fi[v], int(bc)].mean():.1f}%" for v in FRAMINGS) + " |")
    summary.setdefault("p_order_along", {})["bank_c" if bc else "no_bank_c"] = \
        {h: {v: float(P[HIST == h, fi[v], int(bc)].mean()) for v in FRAMINGS} for h in FRAMINGS}

req = P[:, :, 0]
tests = {
    "Request: loss frame vs gain frame": req[:, cols(LOSS)].mean(1) - req[:, cols(GAIN)].mean(1),
    "Request: loss vs neutral": req[:, fi["loss"]] - req[:, fi["neutral"]],
    "Request: loss + you vs neutral": req[:, fi["loss + you"]] - req[:, fi["neutral"]],
    "Request: gain vs neutral": req[:, fi["gain"]] - req[:, fi["neutral"]],
    "Request: gain + you vs neutral": req[:, fi["gain + you"]] - req[:, fi["neutral"]],
    "Request: \"+ you\" vs none": req[:, cols(YOU)].mean(1) - req[:, cols(NOYOU)].mean(1),
    "Bank C's line (all framings)": (P[:, :, 1] - P[:, :, 0]).mean(1),
}
for bc, tag in ((0, ""), (1, ", with Bank C")):                    # "you" after loss and after gain (F: with Bank C)
    you_loss = P[:, fi["loss + you"], bc] - P[:, fi["loss"], bc]
    you_gain = P[:, fi["gain + you"], bc] - P[:, fi["gain"], bc]
    tests[f"\"You\" after loss: loss + you vs loss{tag}"] = you_loss
    tests[f"\"You\" after gain: gain + you vs gain{tag}"] = you_gain
    tests[f"\"You\" after loss minus after gain{tag}"] = you_loss - you_gain
tests.update({f"Bank C's line ({v})": P[:, fi[v], 1] - P[:, fi[v], 0] for v in FRAMINGS})
report.append(f"\n**The request's own effect** (the same moments, all {len(careers)} histories; paired, signs flipped "
              "by career):\n")
report.append("| Contrast | Change in P(order goes along) | 95% interval | p |\n|---|---|---|---|")
summary["tests"] = {}
for name, d in tests.items():
    r = paired(d)
    report.append(line(name, r))
    summary["tests"][name] = {"change": r[0], "p": r[1], "interval": list(r[2])}

neutral_req = req[:, fi["neutral"]]
as_saved = np.array([req[i, fi[HIST[i]]] for i in range(M)])
hist_tests = {
    "History: loss frame vs gain frame (request neutral)": unpaired(neutral_req, LOSS, GAIN),
    "History: framed vs neutral (request neutral)": unpaired(neutral_req, LOSS + GAIN, ["neutral"]),
    "As saved: loss frame vs gain frame (history and request)": unpaired(as_saved, LOSS, GAIN),
    "As saved: framed vs neutral (history and request)": unpaired(as_saved, LOSS + GAIN, ["neutral"]),
}
report.append("\n**The history's effect** (different careers, the request held neutral; careers reshuffled between the "
              "groups), next to the whole effect as saved:\n")
report.append("| Contrast | Change in P(order goes along) | 95% interval | p |\n|---|---|---|---|")
for name, r in hist_tests.items():
    report.append(line(name, r))
    summary["tests"][name] = {"change": r[0], "p": r[1], "interval": list(r[2])}

# ---------------- 2. the state
run1 = {}
for f in sorted(glob.glob(os.path.join(ROOT, "B_bf16", "*.npz"))):
    z = np.load(f)
    for mm, x in zip(json.loads(str(z["meta"])), z["states"]):
        run1[(mm["career_file"], mm["chat"])] = (mm["version"], x[layers].astype(np.float32))
report.append("\n## 2. The state\n")
check = [(i, run1[(CAREER[i], CHAT[i])][1]) for i in range(M) if (CAREER[i], CHAT[i]) in run1]
if check:
    report.append("**Check:** the as-saved version against Run 1's reading of the same moment (cosine; Run 1 read the "
                  "career in one pass, this run from a saved cache, so tiny differences are expected):\n")
    report.append("| Layer | Median | Lowest |\n|---|---|---|")
    for j, l in enumerate(layers):
        cs = [float(S[i, fi[HIST[i]], 0, j] @ r[j] / (np.linalg.norm(S[i, fi[HIST[i]], 0, j]) * np.linalg.norm(r[j])))
              for i, r in check]
        report.append(f"| {l} | {np.median(cs):.4f} | {min(cs):.4f} |")
        summary.setdefault("check_cosine", {})[l] = [float(np.median(cs)), float(min(cs))]

# Sizes: how far each change moves the state, against two careers of the same framing at the same request (Run 1)
report.append("\n**How far each change moves the state** (mean distance, by layer), against two different B careers of "
              "the same framing at the same request (Run 1: different histories):\n")
report.append("| Layer | Request loss vs gain (same moment) | Request framed vs neutral | Bank C's line | Two careers, "
              "same framing |\n|---|---|---|---|---|")
for j, l in enumerate(layers):
    lg = np.linalg.norm(S[:, cols(LOSS), 0, j] - S[:, cols(GAIN), 0, j], axis=-1).mean()
    fn = np.linalg.norm(S[:, cols(LOSS + GAIN), 0, j] - S[:, [fi["neutral"]], 0, j], axis=-1).mean()
    bc = np.linalg.norm(S[:, :, 1, j] - S[:, :, 0, j], axis=-1).mean()
    sib = [np.linalg.norm(a[1][j] - b[1][j]) for (ka, a) in run1.items() for (kb, b) in run1.items()
           if ka < kb and ka[1] == kb[1] and a[0] == b[0]] if run1 else [np.nan]
    report.append(f"| {l} | {lg:.1f} | {fn:.1f} | {bc:.1f} | {np.mean(sib):.1f} |")

# "You" after loss and after gain: the change "+ you" makes at the same moment, in each frame
report.append("\n**\"You\" after loss and after gain** (the change \"+ you\" makes to the state at the same moment): its "
              "size in each frame, and how alike the two changes are (cosine of the average changes: 1 = the same "
              "change, 0 = unrelated). The last column is the ceiling: the change after loss compared with itself, "
              "measured on two halves of the careers. A cosine between the frames well below that ceiling means \"you\" "
              "registers differently after loss than after gain.\n")
report.append("| Layer | Size after loss | Size after gain | Cosine, after loss vs after gain | Median cosine, moment by "
              "moment | Ceiling: after loss vs itself (two halves) |\n|---|---|---|---|---|---|")
half = np.isin(CAREER, careers[::2])
ucos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
for j, l in enumerate(layers):
    dL = S[:, fi["loss + you"], 0, j] - S[:, fi["loss"], 0, j]
    dG = S[:, fi["gain + you"], 0, j] - S[:, fi["gain"], 0, j]
    per = np.median([ucos(a, b) for a, b in zip(dL, dG)])
    row = {"size_loss": float(np.linalg.norm(dL, axis=1).mean()), "size_gain": float(np.linalg.norm(dG, axis=1).mean()),
           "cosine": ucos(dL.mean(0), dG.mean(0)), "median_cosine": float(per),
           "ceiling": ucos(dL[half].mean(0), dL[~half].mean(0))}
    report.append(f"| {l} | {row['size_loss']:.1f} | {row['size_gain']:.1f} | {row['cosine']:.3f} | {row['median_cosine']:.3f} "
                  f"| {row['ceiling']:.3f} |")
    summary.setdefault("you_loss_vs_gain", {})[l] = row

# The frame direction: loss-framed minus neutral request, the history held fixed, against Run 1's (across careers)
report.append("\n**The frame direction** (loss and loss + you minus neutral, averaged over requests). Held fixed: from "
              "this run, at the same moments. Across careers: from Run 1, B's loss careers minus its neutral careers at "
              "the same request (the direction the steering used). Bank C's change along the held-fixed direction is in "
              "units of the loss - neutral gap along it (1 = as far as the loss frame itself moves the state).\n")
report.append("| Layer | Cosine: held fixed vs across careers | Bank C's change along it (all framings) | Bank C, neutral "
              "request | Bank C, loss + you request |\n|---|---|---|---|---|")
for j, l in enumerate(layers):
    u = np.mean([(S[CHAT == c][:, cols(LOSS), 0, j].mean(1) - S[CHAT == c][:, fi["neutral"], 0, j]).mean(0)
                 for c in np.unique(CHAT)], 0)
    gap = np.linalg.norm(u)
    u = u / gap
    if l == 24:
        os.makedirs(os.path.join(ROOT, "matched"), exist_ok=True)
        np.save(os.path.join(ROOT, "matched", "frame_direction_held_fixed_L24.npy"), u)
    cos = np.nan
    if run1:
        ver = np.array([v[0] for v in run1.values()])
        ch = np.array([k[1] for k in run1])
        X1 = np.stack([v[1][j] for v in run1.values()])
        w = np.mean([X1[(ch == c) & np.isin(ver, LOSS)].mean(0) - X1[(ch == c) & (ver == "neutral")].mean(0)
                     for c in np.unique(ch)], 0)
        cos = float(u @ w / np.linalg.norm(w))
    along = lambda vs: float(((S[:, cols(vs), 1, j] - S[:, cols(vs), 0, j]) @ u).mean() / gap)
    report.append(f"| {l} | {cos:.3f} | {along(FRAMINGS):+.2f} | {along(['neutral']):+.2f} | {along(['loss + you']):+.2f} |")
    summary.setdefault("direction", {})[l] = {"cosine_with_run1": cos, "bank_c_along_all": along(FRAMINGS)}

# ---------------- 3. Gemma Scope features, paired within moments
run1_top = {}
try:
    j1 = json.load(open("results/inside_full_career/inside_bf16.json"))["comparisons"]["B: UBS's loss frame vs gain frame"]
    run1_top = {int(l): {r["feature"] for r in v["top"]} for l, v in j1.items()}
except (FileNotFoundError, KeyError):
    pass


def feature_test(D):
    """D: moments x features (paired differences). Per-feature mean in spread units, p by flipping signs by career."""
    C = np.stack([D[CAREER == c].mean(0) for c in careers])
    obs = C.mean(0)
    hits = np.zeros(D.shape[1])
    for _ in range(FEATURE_PERMS):
        hits += np.abs(RNG.choice([-1, 1], len(careers)) @ C / len(careers)) >= np.abs(obs) - 1e-12
    p = (hits + 1) / (FEATURE_PERMS + 1)
    order = np.argsort(p)
    q, run = np.empty_like(p), 1.0
    for i in range(len(p) - 1, -1, -1):
        run = min(run, p[order[i]] * len(p) / (i + 1))
        q[order[i]] = run
    return obs, obs / (D.std(0) + 1e-6), p, q


report.append("\n## 3. Gemma Scope features, the history held fixed\n")
report.append("\n**Note:** a difference between \"you\" after loss and after gain in the features can come from the features' on/off thresholds alone (the same change, starting from different levels). The cosine table in section 2, which is linear, is the cleaner test of whether \"you\" registers differently.\n")
W = S.shape[-1]
for l, path in sae_layers(max(layers) + 1).items():
    if l not in layers:
        continue
    j, sae = layers.index(l), load_sae(path, W)
    Fz = encode(S[:, :, :, j].reshape(-1, W), sae).reshape(M, len(FRAMINGS), 2, -1)
    fyL = Fz[:, fi["loss + you"], 0] - Fz[:, fi["loss"], 0]
    fyG = Fz[:, fi["gain + you"], 0] - Fz[:, fi["gain"], 0]
    tops = {}
    for name, D, live_from in [
            ("Request: loss frame vs gain frame", Fz[:, cols(LOSS), 0].mean(1) - Fz[:, cols(GAIN), 0].mean(1),
             Fz[:, cols(LOSS + GAIN), 0]),
            ("\"You\" after loss: loss + you vs loss", fyL, Fz[:, cols(LOSS), 0]),
            ("\"You\" after gain: gain + you vs gain", fyG, Fz[:, cols(GAIN), 0]),
            ("\"You\" after loss minus after gain", fyL - fyG, Fz[:, cols(LOSS + GAIN), 0]),
            ("Bank C's line (all framings)", (Fz[:, :, 1] - Fz[:, :, 0]).mean(1), Fz[:, :, :])]:
        live = (live_from.reshape(-1, Fz.shape[-1]) > 0).mean(0) >= 0.05
        raw, z, p, q = feature_test(D[:, live])
        ids = np.where(live)[0]
        order = np.argsort(-np.abs(z))[:TOP]
        shared = ""
        tops[name] = {int(ids[o]) for o in order}
        if name.startswith("Request") and l in run1_top:
            k = len(run1_top[l] & tops[name])
            shared = f"; {k} of the top {TOP} are also in Run 1's top {TOP} (loss vs gain across careers)"
        if name.startswith("\"You\" after gain"):
            k = len(tops[name] & tops["\"You\" after loss: loss + you vs loss"])
            shared = f"; {k} of its top {TOP} are also in the top {TOP} after loss"
        report.append(f"**{name}, layer {l}** ({int(live.sum())} features tested; {int((q < 0.05).sum())} with q < 0.05"
                      f"{shared})\n")
        report.append("| Feature | Difference (spread units) | Activation difference | p | q |\n|---|---|---|---|---|")
        for o in order:
            report.append(f"| [{ids[o]}]({NEURONPEDIA.format(layer=l, feature=int(ids[o]))}) | {z[o]:+.2f} | "
                          f"{raw[o]:+.2f} | {p[o]:.4f} | {q[o]:.3f} |")
        report.append("")
        summary.setdefault("features", {}).setdefault(name, {})[l] = {
            "tested": int(live.sum()), "q_below_0.05": int((q < 0.05).sum()),
            "top": [{"feature": int(ids[o]), "standardised_difference": float(z[o]), "q": float(q[o])} for o in order]}
    del Fz, fyL, fyG

open(os.path.join(OUT, "MATCHED.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "matched.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "MATCHED.md"))
