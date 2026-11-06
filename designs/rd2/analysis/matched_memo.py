"""Same moment, different priming: the analysis of scripts/modal_matched.py --exp A (the user, 20 Oct).

    python designs/rd2/analysis/matched_memo.py <states root, e.g. /states/v2> <output dir>

Every A career (25) was read with management's priming (the memo and all five morning books) in each of the five
versions, everything else as saved, the agent's own words included. Moments: the first update of each trading day
(where A's effect showed: it traded far bigger before any chat) and the six push requests.

1. What it would do: at the day's first update, the expected size of its order and the chance it changes its position;
   at the requests, P(the order goes along). Rows: the career's own version (its history and its own words); columns:
   the priming it is given. The priming's own effect is paired within moments (signs flipped by career); what the
   agent's own words carry is between careers (priming held neutral; careers reshuffled). Validity: the as-saved
   version against what the real careers did.
2. The state: the priming direction (loss and loss + you minus neutral priming, same moments), against Run 1's memo
   direction (across careers, used by the steering's memo check) and against UBS's loss direction with the history
   held fixed (from B's matched run): is management's loss the same thing inside as UBS's loss? "You" after loss and
   after gain, as in B.
3. Gemma Scope features: loss vs gain priming and "you" after loss and after gain, paired within moments, with the
   overlap with UBS's loss-vs-gain features (B's matched run).
"""
import glob, json, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "sim"))
from gemma_scope import NEURONPEDIA, encode, load_sae, sae_layers

ROOT, OUT = sys.argv[1], sys.argv[2]
FOLDER_A = "results/full_career_gemma-3-12b-it_4bit_career_book_neutral_lines_v2"
V = ["neutral", "loss", "gain", "loss + you", "gain + you"]
LOSS, GAIN = ["loss", "loss + you"], ["gain", "gain + you"]
PERMS, BOOT, FEATURE_PERMS, TOP = 10000, 2000, 1000, 15
RNG = np.random.default_rng(20261021)
os.makedirs(OUT, exist_ok=True)
vi = {v: i for i, v in enumerate(V)}
cols = lambda vs: [vi[v] for v in vs]

# ---------------- load: moments x priming (x layers x width)
meta, S, layers = [], [], None
for f in sorted(glob.glob(os.path.join(ROOT, "matched", "A_bf16", "*.npz"))):
    z = np.load(f)
    r = json.loads(str(z["meta"]))
    n = len(r) // len(V)
    assert [x["priming"] for x in r] == V * n
    meta += [r[k * len(V):(k + 1) * len(V)] for k in range(n)]
    S.append(z["states"].reshape(n, len(V), *z["states"].shape[1:]))
    layers = [int(l) for l in z["layers"]]
assert meta, "no A matched states: run scripts/modal_matched.py --exp A first"
S = np.concatenate(S)                                            # moments x 5 x layers x width
assert np.isfinite(S).all()
KIND = np.array([m[0]["kind"] for m in meta])
HIST = np.array([m[0]["history"] for m in meta])
CAREER = np.array([m[0]["career_file"] for m in meta])
SIZE = np.array([[x["expected_size"] for x in m] for m in meta])
CHANGE = np.array([[x["p_change"] for x in m] for m in meta])
ALONG = np.array([[x["p_order_along"] if x["p_order_along"] is not None else np.nan for x in m] for m in meta])
COV = np.array([[x["coverage"] for x in m] for m in meta])
OPEN, REQ = KIND == "opening", KIND == "request"
# 5 August's request asks for a price (QUOTE), not an order: a request counts only if the scored orders cover at least
# half the model's probability in its plain read (the neutral memo)
MIN_COVER = 0.5
REQ = REQ & (COV[:, 0] >= MIN_COVER)
careers = np.unique(CAREER)
report = ["# Same moment, different priming (A's careers, everything but management's memo and books held fixed)\n",
          f"{len(careers)} careers; {OPEN.sum()} trading-day openings and {REQ.sum()} push requests, each read with the "
          "memo and all five morning books in each of the five versions (the books' 30-day P&L still carries the "
          "agent's own; the agent's own words are as saved). Gemma 3 12B at bfloat16. Outcomes from the log-probs of "
          "HOLD and every order size the agents used, after a fixed neutral reasoning line; coverage (the share of all "
          f"probability those orders take): median {np.median(COV):.2f}, lowest {COV.min():.2f}. Produced by "
          "`designs/rd2/analysis/matched_memo.py`.\n"]
summary = {"careers": len(careers), "openings": int(OPEN.sum()), "requests": int(REQ.sum())}


def paired(d, mask):
    c = np.array([d[mask & (CAREER == k)].mean() for k in careers if (mask & (CAREER == k)).any()])
    obs = c.mean()
    p = (np.sum(np.abs((RNG.choice([-1, 1], (PERMS, len(c))) * c).mean(1)) >= abs(obs) - 1e-12) + 1) / (PERMS + 1)
    boot = [c[RNG.integers(0, len(c), len(c))].mean() for _ in range(BOOT)]
    return obs, p, np.percentile(boot, [2.5, 97.5])


def unpaired(value, mask, group_a, group_b):
    per = {k: value[mask & (CAREER == k)].mean() for k in careers if (mask & (CAREER == k)).any()}
    hist = {k: HIST[CAREER == k][0] for k in per}
    va = np.array([v for k, v in per.items() if hist[k] in group_a])
    vb = np.array([v for k, v in per.items() if hist[k] in group_b])
    obs, both = va.mean() - vb.mean(), np.concatenate([va, vb])
    hits = sum(abs((x := RNG.permutation(both))[:len(va)].mean() - x[len(va):].mean()) >= abs(obs) - 1e-12
               for _ in range(PERMS))
    boot = [va[RNG.integers(0, len(va), len(va))].mean() - vb[RNG.integers(0, len(vb), len(vb))].mean() for _ in range(BOOT)]
    return obs, (hits + 1) / (PERMS + 1), np.percentile(boot, [2.5, 97.5])


def contrasts(Y):
    return {
        "Priming: loss vs neutral": Y[:, vi["loss"]] - Y[:, vi["neutral"]],
        "Priming: gain vs neutral": Y[:, vi["gain"]] - Y[:, vi["neutral"]],
        "Priming: loss + you vs neutral": Y[:, vi["loss + you"]] - Y[:, vi["neutral"]],
        "Priming: gain + you vs neutral": Y[:, vi["gain + you"]] - Y[:, vi["neutral"]],
        "Priming: loss frame vs gain frame": Y[:, cols(LOSS)].mean(1) - Y[:, cols(GAIN)].mean(1),
        "\"You\" after loss: loss + you vs loss": Y[:, vi["loss + you"]] - Y[:, vi["loss"]],
        "\"You\" after gain: gain + you vs gain": Y[:, vi["gain + you"]] - Y[:, vi["gain"]],
        "\"You\" after loss minus after gain": (Y[:, vi["loss + you"]] - Y[:, vi["loss"]]) - (Y[:, vi["gain + you"]] - Y[:, vi["gain"]]),
    }


# ---------------- 1. what it would do
real = {}                                    # the real careers: traded before the first chat (oz/day), per version
for p in glob.glob(os.path.join(FOLDER_A, "days", "*.json")):
    d = json.load(open(p))
    real.setdefault(d["version"], []).append(d["summary"].get("before_first_chat_gross", np.nan))
outcomes = [("At the day's first update: expected order size (oz)", SIZE, OPEN, lambda x: f"{x:,.0f}", 1, " oz"),
            ("At the day's first update: chance it changes its position", CHANGE, OPEN, lambda x: f"{100 * x:.1f}%", 100, " points"),
            ("At UBS's requests: P(the order goes along)", ALONG, REQ, lambda x: f"{100 * x:.1f}%", 100, " points")]
report.append("\n## 1. What it would do\n")
summary["tables"], summary["tests"] = {}, {}
for title, Y, mask, fmt, scale, unit in outcomes:
    report.append(f"\n**{title}.** Rows: the career's own version (its history, its own words); columns: the priming it "
                  "is given. The diagonal is the career as saved.\n")
    report.append("| History \\ priming | " + " | ".join(V) + " |\n" + "|---" * (len(V) + 1) + "|")
    for h in V:
        report.append(f"| {h} | " + " | ".join(fmt(Y[mask & (HIST == h), vi[v]].mean()) for v in V) + " |")
    summary["tables"][title] = {h: {v: float(Y[mask & (HIST == h), vi[v]].mean()) for v in V} for h in V}
    report.append(f"\n| Contrast (all {len(careers)} histories; paired, signs flipped by career) | Change | 95% interval "
                  "| p |\n|---|---|---|---|")
    for name, d in contrasts(Y).items():
        o, p, ci = paired(d, mask)
        report.append(f"| {name} | {scale * o:+,.1f}{unit} | {scale * ci[0]:+,.1f} to {scale * ci[1]:+,.1f} | {p:.4f} |")
        summary["tests"][f"{title} | {name}"] = {"change": o, "p": p, "interval": list(ci)}
    neutral_priming = Y[:, vi["neutral"]]
    report.append(f"\n| What its own words carry (priming held neutral; different careers, 5 per version, so the "
                  "intervals are rough) | Change | 95% interval | p |\n|---|---|---|---|")
    for name, (a, b) in {"History: loss frame vs neutral": (LOSS, ["neutral"]),
                         "History: gain frame vs neutral": (GAIN, ["neutral"])}.items():
        o, p, ci = unpaired(neutral_priming, mask, a, b)
        report.append(f"| {name} | {scale * o:+,.1f}{unit} | {scale * ci[0]:+,.1f} to {scale * ci[1]:+,.1f} | {p:.4f} |")
        summary["tests"][f"{title} | {name}"] = {"change": o, "p": p, "interval": list(ci)}
report.append("\n**Validity check:** the as-saved expected order size at the day's first update, against what the real "
              "careers traded before the first chat (oz/day, mean over their trading days):\n")
report.append("| Version | As saved, expected order size (log-probs; one order) | Real careers, traded before the first "
              "chat (all orders that morning; comparable in scale, not the same quantity) |\n|---|---|---|")
for v in V:
    report.append(f"| {v} | {SIZE[OPEN & (HIST == v), vi[v]].mean():,.0f} | {np.nanmean(real.get(v, [np.nan])):,.0f} |")

# ---------------- 2. the state
def unit(x):
    return x / np.linalg.norm(x)


ucos = lambda a, b: float(unit(a) @ unit(b))
memo1 = {}                                   # Run 1: A's loss careers minus neutral careers at the same request
X1, m1 = [], []
for f in sorted(glob.glob(os.path.join(ROOT, "A_bf16", "*.npz"))):
    z = np.load(f)
    m1 += json.loads(str(z["meta"]))
    X1.append(z["states"][:, layers].astype(np.float32))
if m1:
    X1 = np.concatenate(X1)
    v1, r1 = np.array([m["version"] for m in m1]), np.array([m["chat"] for m in m1])
    a1 = np.array([m.get("asked", True) for m in m1])
    for j, l in enumerate(layers):
        memo1[l] = np.mean([X1[a1 & (r1 == c) & np.isin(v1, LOSS), j].mean(0) - X1[a1 & (r1 == c) & (v1 == "neutral"), j].mean(0)
                            for c in np.unique(r1[a1])], 0)
ubs = {}                                     # B's matched run: UBS's loss request minus neutral, the history held fixed
bfiles = sorted(glob.glob(os.path.join(ROOT, "matched", "B_bf16", "*.npz")))
if bfiles:
    acc, nb = None, 0
    for f in bfiles:
        z = np.load(f)
        s = z["states"].reshape(5, 2, *z["states"].shape[1:])[:, 0]          # without Bank C: framing x layers x width
        d = s[cols(LOSS)].mean(0) - s[vi["neutral"]]
        acc = d if acc is None else acc + d
        nb += 1
    for j, l in enumerate(layers):
        ubs[l] = acc[j] / nb
report.append("\n## 2. The state\n")
report.append("**The priming direction** (loss and loss + you priming minus neutral, the same moments). Cosines: 1 = the "
              "same direction, 0 = unrelated. Ceiling: the priming direction on two halves of the careers. Across "
              "careers: Run 1's memo direction (A's loss careers minus its neutral careers; the steering's memo check "
              "used it). UBS's loss: B's matched run, UBS's loss request minus neutral with the history held fixed: is "
              "management's loss the same thing inside as UBS's?\n")
report.append("Measured at UBS's requests (where Run 1's and UBS's directions were measured too); the last column compares "
              "it with the same priming direction at the day's first update.\n")
report.append("| Layer | Ceiling (two halves) | vs Run 1's memo direction | vs UBS's loss (history held fixed) | vs the "
              "priming direction at the day's first update |\n|---|---|---|---|---|")
half = np.isin(CAREER, careers[::2])
fmt = lambda x: "-" if x is None else f"{x:.3f}"
for j, l in enumerate(layers):
    d = S[REQ][:, cols(LOSS), j].mean(1) - S[REQ][:, vi["neutral"], j]
    u = d.mean(0)
    u_open = (S[OPEN][:, cols(LOSS), j].mean(1) - S[OPEN][:, vi["neutral"], j]).mean(0)
    if l == 24:
        np.save(os.path.join(ROOT, "matched", "memo_direction_held_fixed_L24.npy"), unit(u))
    row = {"ceiling": ucos(d[half[REQ]].mean(0), d[~half[REQ]].mean(0)),
           "run1_memo": ucos(u, memo1[l]) if l in memo1 else None, "ubs_loss": ucos(u, ubs[l]) if l in ubs else None,
           "openings": ucos(u, u_open)}
    report.append(f"| {l} | {row['ceiling']:.3f} | {fmt(row['run1_memo'])} | {fmt(row['ubs_loss'])} | {row['openings']:.3f} |")
    summary.setdefault("direction", {})[l] = row
report.append("\n**\"You\" after loss and after gain** (the change the \"+ you\" priming makes at the same moment): "
              "sizes, how alike (cosine), and the ceiling (after loss vs itself on two halves of the careers).\n")
report.append("| Layer | Size after loss | Size after gain | Cosine, after loss vs after gain | Ceiling |\n|---|---|---|---|---|")
for j, l in enumerate(layers):
    dL = S[:, vi["loss + you"], j] - S[:, vi["loss"], j]
    dG = S[:, vi["gain + you"], j] - S[:, vi["gain"], j]
    report.append(f"| {l} | {np.linalg.norm(dL, axis=1).mean():.1f} | {np.linalg.norm(dG, axis=1).mean():.1f} | "
                  f"{ucos(dL.mean(0), dG.mean(0)):.3f} | {ucos(dL[half].mean(0), dL[~half].mean(0)):.3f} |")

# ---------------- 3. Gemma Scope features, paired within moments
ubs_top = {}
try:
    j1 = json.load(open(os.path.join(OUT, "matched.json")))["features"]["Request: loss frame vs gain frame"]
    ubs_top = {int(l): {r["feature"] for r in v["top"]} for l, v in j1.items()}
except (FileNotFoundError, KeyError):
    pass


def feature_test(D):
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


YOU_LOSS = "\"You\" after loss: loss + you vs loss"
report.append("\n## 3. Gemma Scope features, everything but the priming held fixed\n")
report.append("\n**Note:** a difference between \"you\" after loss and after gain in the features can come from the features' on/off thresholds alone (the same change, starting from different levels). The cosine table in section 2, which is linear, is the cleaner test of whether \"you\" registers differently.\n")
W = S.shape[-1]
for l, path in sae_layers(max(layers) + 1).items():
    if l not in layers:
        continue
    j, sae = layers.index(l), load_sae(path, W)
    Fz = encode(S[:, :, j].reshape(-1, W), sae).reshape(len(meta), len(V), -1)
    fyL, fyG = Fz[:, vi["loss + you"]] - Fz[:, vi["loss"]], Fz[:, vi["gain + you"]] - Fz[:, vi["gain"]]
    tops = {}
    for name, D, live_from in [
            ("Priming: loss frame vs gain frame", Fz[:, cols(LOSS)].mean(1) - Fz[:, cols(GAIN)].mean(1), Fz[:, cols(LOSS + GAIN)]),
            (YOU_LOSS, fyL, Fz[:, cols(LOSS)]),
            ("\"You\" after gain: gain + you vs gain", fyG, Fz[:, cols(GAIN)]),
            ("\"You\" after loss minus after gain", fyL - fyG, Fz[:, cols(LOSS + GAIN)])]:
        live = (live_from.reshape(-1, Fz.shape[-1]) > 0).mean(0) >= 0.05
        raw, z, p, q = feature_test(D[:, live])
        ids = np.where(live)[0]
        order = np.argsort(-np.abs(z))[:TOP]
        tops[name] = {int(ids[o]) for o in order}
        shared = ""
        if name.startswith("Priming") and l in ubs_top:
            shared = f"; {len(tops[name] & ubs_top[l])} of the top {TOP} are also in UBS's top {TOP} (B's matched run)"
        if name.startswith("\"You\" after gain"):
            shared = f"; {len(tops[name] & tops[YOU_LOSS])} of its top {TOP} are also in the top {TOP} after loss"
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

open(os.path.join(OUT, "MATCHED_MEMO.md"), "w").write("\n".join(report) + "\n")
json.dump(summary, open(os.path.join(OUT, "matched_memo.json"), "w"), indent=1, default=float)
print("written", os.path.join(OUT, "MATCHED_MEMO.md"))
