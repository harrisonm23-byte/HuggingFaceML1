"""Where going along comes from, and whether the agent knows it is misconduct (exploratory; the user, 21 Oct).

    python designs/rd2/analysis/trace.py <states root, e.g. /states/v2> <output dir>

1. The misconduct question (`sim/misconduct.py`): at B's 300 requests, UBS's request in each framing, P(Yes: it is market
   manipulation). Does the agent recognise it; does it go along knowingly (recognition where it went along against where it
   did not); does a framing lower recognition (paired within moment against the neutral request)?
2. The going-along direction at layer 24 (Run 1's states, all experiments: went along minus not, within request,
   experiment and framing): its cosine with every other direction measured (UBS's framings and "you" with the history
   held fixed, Bank C's line, the author's emotion documents, the position already held, and a "misconduct words"
   direction from the agent's own replies), raw and with every dimension on one scale; a reference for unrelated
   directions is +/-2/sqrt(width).
3. Naming it: the Gemma Scope 2 features (layer 24) whose decoder directions align most with it, with Neuronpedia links.
"""
import glob, json, os, re, sys
import numpy as np

ROOT, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "sim"))
sys.path.insert(0, os.path.join(os.getcwd(), "sim"))
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]
L = 24
RNG = np.random.default_rng(20261021)
PERMS, BOOT = 10000, 2000
os.makedirs(OUT, exist_ok=True)
report = ["# Where going along comes from, and whether the agent knows it is misconduct (exploratory)\n",
          "Produced by `designs/rd2/analysis/trace.py` (`scripts/modal_trace.py`).\n"]
summary = {}
cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def career_test(pairs):
    """[(career, value)] -> mean over careers, p by flipping signs, interval by resampling careers."""
    per = {}
    for c, x in pairs:
        per.setdefault(c, []).append(x)
    c = np.array([np.mean(v) for v in per.values()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    lo, hi = np.percentile([c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)], [2.5, 97.5])
    return obs, p, lo, hi


# ---------------- 1. the misconduct question
rows = {}
for p in sorted(glob.glob(os.path.join(ROOT, "trace", "part*.jsonl"))):
    for line in open(p):
        r = json.loads(line)
        rows[r["key"]] = r
if rows:
    R = list(rows.values())
    by = {}
    for r in R:
        by.setdefault((r["career_file"], r["history_index"]), {})[r["framing"]] = r
    full = {k: v for k, v in by.items() if len(v) == len(FRAMINGS)}
    own = [v[v["neutral"]["version"]] for v in full.values()]          # the request as the career saw it
    report.append("## 1. Does it know? P(Yes, it is market manipulation), asked at each request\n")
    report.append(f"{len(full)} moments; the Yes/No answers take a median {np.median([r['yes_no_mass'] for r in R]):.2f} "
                  "of the model's probability.\n")
    report.append("| | P(Yes) |\n|---|---|")
    report.append(f"| All moments, the request as the career saw it | {100 * np.mean([r['p_yes'] for r in own]):.1f}% |")
    report.append(f"| Where it went along | {100 * np.mean([r['p_yes'] for r in own if r['saved_joined']]):.1f}% "
                  f"({sum(r['saved_joined'] for r in own)} moments) |")
    report.append(f"| Where it did not | {100 * np.mean([r['p_yes'] for r in own if not r['saved_joined']]):.1f}% |")
    for f in FRAMINGS:
        report.append(f"| UBS's request {f} (all moments) | {100 * np.mean([v[f]['p_yes'] for v in full.values()]):.1f}% |")
    report.append("\n**Does a framing lower recognition?** Each framing minus the neutral request, the same moment (points):\n")
    report.append("| Framing | Change | 95% interval | p |\n|---|---|---|---|")
    summary["misconduct"] = {"overall": float(np.mean([r["p_yes"] for r in own]))}
    for f in FRAMINGS[1:]:
        o, p, lo, hi = career_test([(k[0], v[f]["p_yes"] - v["neutral"]["p_yes"]) for k, v in full.items()])
        report.append(f"| {f} | {100 * o:+.1f} | {100 * lo:+.1f} to {100 * hi:+.1f} | {p:.4f} |")
        summary["misconduct"][f] = {"change": o, "p": p}
    report.append("\n**By request** (the request as the career saw it):\n")
    report.append("| Request | P(Yes) | Went along |\n|---|---|---|")
    for q in sorted({(r["date"], r["chat"]) for r in own}):
        rr = [r for r in own if (r["date"], r["chat"]) == q]
        report.append(f"| {q[0]} ({q[1]}) | {100 * np.mean([r['p_yes'] for r in rr]):.1f}% | "
                      f"{100 * np.mean([r['saved_joined'] for r in rr]):.0f}% |")

# ---------------- 2. the going-along direction and what it lines up with
import steer2
run1 = sorted(p for e in ("A", "B", "C", "C2", "D", "E", "F") for p in glob.glob(os.path.join(ROOT, f"{e}_bf16", "*.npz")))
dirs, ref_states = {}, []
if run1:
    a = steer2.along_direction(run1, L)
    along = (a[0]["along"] + a[1]["along"]) / 2
    # Position already held (B), and "misconduct words" in the agent's own reply (all experiments): within request,
    # experiment and framing, like the going-along direction
    WORDS = re.compile(r"manipulat|illegal|unethical|improper|collu|complian|regulat|front.?run|spoof", re.I)
    cells_pos, cells_words = {}, {}
    for p in run1:
        z = np.load(p)
        for m, x in zip(json.loads(str(z["meta"])), z["states"][:, L].astype(np.float64)):
            key = (m["experiment"], m["version"], m["chat"])
            ref_states.append(x)
            if m["experiment"] == "B":
                side = np.sign(m.get("held_their_way", 0))
                if side != 0:
                    cells_pos.setdefault(key, {True: [], False: []})[side > 0].append(x)
            cells_words.setdefault(key, {True: [], False: []})[bool(WORDS.search(m.get("reply") or ""))].append(x)

    def cell_dir(cells):
        d = [np.mean(g[True], 0) - np.mean(g[False], 0) for g in cells.values() if g[True] and g[False]]
        return np.mean(d, 0) if d else None
    dirs["position already on UBS's side (against the other side)"] = cell_dir(cells_pos)
    dirs["misconduct words in its own reply"] = cell_dir(cells_words)
    idx = {(v, b): 2 * i + int(b) for i, v in enumerate(FRAMINGS) for b in (False, True)}
    j = KEEP.index(L)
    sh = {"UBS: loss - neutral request": [], "UBS: gain - neutral request": [], "UBS: loss - gain request": [],
          "UBS: \"you\" after loss": [], "UBS: \"you\" after gain": [], "Bank C's line": []}
    for p in sorted(glob.glob(os.path.join(ROOT, "matched", "B_bf16", "*.npz"))):
        S = np.load(p)["states"][:, j].astype(np.float64)
        g = lambda v, b=False: S[idx[(v, b)]]
        sh["UBS: loss - neutral request"].append((g("loss") + g("loss + you")) / 2 - g("neutral"))
        sh["UBS: gain - neutral request"].append((g("gain") + g("gain + you")) / 2 - g("neutral"))
        sh["UBS: loss - gain request"].append((g("loss") + g("loss + you") - g("gain") - g("gain + you")) / 2)
        sh["UBS: \"you\" after loss"].append(g("loss + you") - g("loss"))
        sh["UBS: \"you\" after gain"].append(g("gain + you") - g("gain"))
        sh["Bank C's line"].append(np.mean([g(v, True) - g(v) for v in FRAMINGS], 0))
    for k, v in sh.items():
        if v:
            dirs[k] = np.mean(v, 0)
    emo = os.path.join(ROOT, "emotion", "states.npz")
    if os.path.exists(emo):
        z = np.load(emo)
        th = np.array([m["theme"] for m in json.loads(str(z["meta"]))])
        X = z["states_mean"][:, L].astype(np.float64)
        mean = lambda t: X[th == t].mean(0)
        dirs["Documents: loss - gain"] = mean("loss") - mean("gain")
        dirs["Documents: blame - credit"] = mean("blame") - mean("credit")
        if "neutral" in th:
            for t in ("loss", "blame", "gain", "credit"):
                dirs[f"Documents: {t} - neutral"] = mean(t) - mean("neutral")
    R0 = np.stack(ref_states)
    scale = R0.std(0) + 1e-6
    ref = 2 / np.sqrt(len(along))
    report.append(f"\n## 2. The going-along direction (layer {L}) against everything else measured\n")
    report.append(f"Cosine: 1 = the same direction, -1 = opposite; unrelated directions fall within about +/-{ref:.3f}. "
                  "\"One scale\": every dimension divided by its spread over all decision moments first.\n")
    report.append("| Direction | Cosine | Cosine, one scale |\n|---|---|---|")
    summary["cosines"] = {}
    for k, d in dirs.items():
        if d is None:
            continue
        c1, c2 = cos(along, d), cos(along / scale, d / scale)
        report.append(f"| {k} | {c1:+.3f} | {c2:+.3f} |")
        summary["cosines"][k] = {"raw": c1, "scaled": c2}

    # ---------------- 3. naming it: Gemma Scope features whose decoder directions align with it
    try:
        from gemma_scope import NEURONPEDIA, load_sae, sae_layers
        files = sae_layers(48)
        if L in files:
            We, b, t, Wd, bd = load_sae(files[L], len(along))
            D = Wd / np.linalg.norm(Wd, axis=1, keepdims=True)
            sc = D @ (along / np.linalg.norm(along))
            report.append(f"\n## 3. Gemma Scope 2 features (layer {L}) most aligned with going along\n")
            report.append("| Toward going along | Cosine | Away from it | Cosine |\n|---|---|---|---|")
            top, bot = np.argsort(-sc)[:15], np.argsort(sc)[:15]
            for i, k in zip(top, bot):
                report.append(f"| [{i}]({NEURONPEDIA.format(layer=L, feature=int(i))}) | {sc[i]:+.3f} | "
                              f"[{k}]({NEURONPEDIA.format(layer=L, feature=int(k))}) | {sc[k]:+.3f} |")
            summary["features"] = {"toward": [int(i) for i in top], "away": [int(k) for k in bot]}
    except Exception as err:                                  # the features are a bonus; the rest stands without them
        report.append(f"\n(Gemma Scope features not read: {type(err).__name__})")

open(os.path.join(OUT, "TRACE.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "trace.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "TRACE.md"))
