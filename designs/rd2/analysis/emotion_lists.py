"""The author's emotion lists against the frame UBS's lines produce (exploratory; the user, 21 Oct).

    python designs/rd2/analysis/emotion_lists.py <emotion states .npz> <matched B dir> <Run 1 B dir> <output dir>

The lists (designs/rd2/emotion_lists/, written by the author, frozen): Loss and Gain (no "you"), Blame and Credit (aimed
at "you"), and Neutral if present; 16 documents each, about 150 words, nothing about silver or trading. Each document is
read on its own; its state is the mean over its tokens (and, as a check, its last token) at each layer.

Emotion directions (mean of one theme's documents minus another's) against the frame directions from UBS's lines with the
history held fixed (the matched rereads, 300 B moments):
- Loss - Gain                   against UBS's loss and loss + you request minus gain and gain + you;
- Blame - Loss (the "you" in a loss)   against loss + you minus loss;
- Credit - Gain (the "you" in a gain)  against gain + you minus gain;
- Loss - Neutral (if Neutral is given) against loss and loss + you minus neutral.
Reported: the cosine; a null from reshuffling which documents belong to which theme (1,000 times); each direction's
ceiling (its cosine with itself built on two halves); and a held-out check (built on half the documents, does it sort
the other half?). Then the drift: Run 1's B states at the six requests projected on the Loss - Gain direction, loss-framed
careers minus gain-framed, request by request.
"""
import glob, json, os, sys
import numpy as np

EMO, MATCHED, RUN1, OUT = sys.argv[1:5]
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
KEEP = [6, 12, 18, 24, 31, 36, 41, 47]
RNG = np.random.default_rng(20261021)
SHUFFLES = 1000
os.makedirs(OUT, exist_ok=True)

z = np.load(EMO)
meta = json.loads(str(z["meta"]))
THEME = np.array([m["theme"] for m in meta])
STATES = {"mean": z["states_mean"].astype(np.float64), "last": z["states_last"].astype(np.float64)}
themes = sorted(set(THEME))
cos = lambda a, b: float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

# UBS's frame directions, the history held fixed
idx = {(v, b): 2 * i + int(b) for i, v in enumerate(FRAMINGS) for b in (False, True)}
shifts = {k: [] for k in ("loss_gain", "you_loss", "you_gain", "loss_neutral")}
runs = []
for p in sorted(glob.glob(os.path.join(MATCHED, "*.npz"))):
    m = np.load(p)
    S = m["states"].astype(np.float64)                           # 10 versions x layers x width
    g = lambda v: S[idx[(v, False)]]
    shifts["loss_gain"].append((g("loss") + g("loss + you")) / 2 - (g("gain") + g("gain + you")) / 2)
    shifts["you_loss"].append(g("loss + you") - g("loss"))
    shifts["you_gain"].append(g("gain + you") - g("gain"))
    shifts["loss_neutral"].append((g("loss") + g("loss + you")) / 2 - g("neutral"))
    runs.append(int(json.loads(str(m["meta"]))[0]["run"]))
runs = np.array(runs)
UBS = {k: np.stack(v) for k, v in shifts.items()}                 # moments x layers x width
PAIRS = [("Loss - Gain", "loss", "gain", "loss_gain", "UBS: loss - gain request"),
         ("Blame - Loss (the \"you\" in a loss)", "blame", "loss", "you_loss", "UBS: loss + you - loss"),
         ("Credit - Gain (the \"you\" in a gain)", "credit", "gain", "you_gain", "UBS: gain + you - gain"),
         ("Loss - Neutral", "loss", "neutral", "loss_neutral", "UBS: loss - neutral request")]
PAIRS = [p for p in PAIRS if p[1] in themes and p[2] in themes]

report = ["# The author's emotion lists against the frame UBS's lines produce (exploratory)\n",
          f"Documents: {', '.join(f'{t} {int((THEME == t).sum())}' for t in themes)}. Each read on its own by Gemma 3 12B "
          "(bfloat16); its state is the mean over its tokens. UBS's directions come from the matched rereads (the history "
          "held fixed). Cosine: 1 = the same direction, 0 = unrelated (two random directions in this space: about "
          "+/-0.03). The null reshuffles which documents belong to which theme. Produced by "
          "`designs/rd2/analysis/emotion_lists.py`.\n"]
summary = {}
half = np.arange(len(THEME)) % 2 == 0
for name, a, b, key, ubs_name in PAIRS:
    report.append(f"\n## {name}, against {ubs_name}\n")
    report.append("| Layer | Cosine | Null, 95% range | Emotion direction, two halves of the documents | UBS direction, two "
                  "halves of the careers | Held out: documents sorted right |\n|---|---|---|---|---|---|")
    summary[name] = {}
    ab = np.isin(THEME, [a, b])
    for j, L in enumerate(KEEP):
        X = STATES["mean"][:, L]
        e = X[THEME == a].mean(0) - X[THEME == b].mean(0)
        u = UBS[key][:, j].mean(0)
        c = cos(e, u)
        lab = THEME[ab]
        null = []
        for _ in range(SHUFFLES):
            sh = RNG.permutation(lab)
            null.append(cos(X[ab][sh == a].mean(0) - X[ab][sh == b].mean(0), u))
        lo, hi = np.percentile(null, [2.5, 97.5])
        e_ceiling = cos(X[(THEME == a) & half].mean(0) - X[(THEME == b) & half].mean(0),
                        X[(THEME == a) & ~half].mean(0) - X[(THEME == b) & ~half].mean(0))
        u_ceiling = cos(UBS[key][runs < 5, j].mean(0), UBS[key][runs >= 5, j].mean(0))
        right = []                                                # built on one half, sort the other (both ways)
        for h in (half, ~half):
            d = X[(THEME == a) & h].mean(0) - X[(THEME == b) & h].mean(0)
            mid = (X[(THEME == a) & h].mean(0) + X[(THEME == b) & h].mean(0)) / 2
            test = ab & ~h
            right += list(((X[test] - mid) @ d > 0) == (THEME[test] == a))
        report.append(f"| {L} | {c:+.3f} | {lo:+.3f} to {hi:+.3f} | {e_ceiling:+.3f} | {u_ceiling:+.3f} | "
                      f"{100 * np.mean(right):.0f}% |")
        summary[name][L] = {"cosine": c, "null": [float(lo), float(hi)], "emotion_ceiling": e_ceiling,
                            "ubs_ceiling": u_ceiling, "held_out_right": float(np.mean(right))}

# The drift: do loss-framed careers sit further along the Loss - Gain emotion direction, request by request?
if "loss" in themes and "gain" in themes:
    rows, X1 = [], []
    for p in sorted(glob.glob(os.path.join(RUN1, "*.npz"))):
        r = np.load(p)
        for mm, x in zip(json.loads(str(r["meta"])), r["states"]):
            rows.append(mm)
            X1.append(x[KEEP].astype(np.float64))
    if rows:
        X1 = np.stack(X1)
        ver = np.array([m["version"] for m in rows])
        req = np.array([f"{m['date']} ({m['chat']})" for m in rows])
        report.append("\n## The drift: B's loss-framed careers minus its gain-framed careers along the Loss - Gain emotion "
                      "direction, request by request (in units of the documents' own Loss - Gain gap along it)\n")
        report.append("| Request | " + " | ".join(f"Layer {L}" for L in KEEP) + " |\n" + "|---" * (len(KEEP) + 1) + "|")
        summary["drift"] = {}
        for q in sorted(set(req)):
            cells = []
            for j, L in enumerate(KEEP):
                X = STATES["mean"][:, L]
                e = X[THEME == "loss"].mean(0) - X[THEME == "gain"].mean(0)
                unit, gap = e / np.linalg.norm(e), np.linalg.norm(e)
                lo_ = X1[(req == q) & np.isin(ver, ["loss", "loss + you"]), j] @ unit
                ga_ = X1[(req == q) & np.isin(ver, ["gain", "gain + you"]), j] @ unit
                cells.append((lo_.mean() - ga_.mean()) / gap)
            report.append(f"| {q} | " + " | ".join(f"{c:+.3f}" for c in cells) + " |")
            summary["drift"][q] = dict(zip(KEEP, cells))

open(os.path.join(OUT, "EMOTION.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "emotion.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "EMOTION.md"))
