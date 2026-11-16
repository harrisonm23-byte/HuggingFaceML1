"""Push and cue: the analysis of scripts/modal_push_carry.py (the user, 28 Oct; designs/rd2/PLAN_PUSH_CUE.md).

    python designs/rd2/analysis/push_carry.py results/push_carry      # reads carry_rows.json and cue_rows.json there

1. The carry: at UBS's 12 January request, P(the order goes along) in each framed career as saved, with UBS's
   7 January request set back to neutral, and with every earlier UBS line set back to neutral, the agent's own words and
   trades kept; against B's neutral careers. Within a career the versions differ only in UBS's words, so the
   differences are paired (signs flipped by career); against the neutral careers, careers are reshuffled.
2. The cue: at 12 January, P(the order goes along) with UBS's blame line ("I'm counting on you to deliver it", no loss
   in it) minus with the neutral line, in each career (the matched rereads). If the line calls back an earlier push, it
   should do more in the blame careers than in the neutral ones. Blame careers start high and neutral ones low, so the
   effect is also given in log-odds, which a ceiling or a floor bends less; a null may be saturation, not absence.
   Inside: whether the change the line makes to the state points the way the 7 January blame line's change did, more
   in the blame careers.
One moment per career; a career counts only if the scored orders cover at least half the model's probability with the
neutral request (as in the matched rereads). 10,000 reshuffles; 95% intervals from resampling careers. Exploratory.
"""
import json, os, sys
import numpy as np

DIR = sys.argv[1]
MIN_COVER, PERMS, BOOT = 0.5, 10000, 2000
RNG = np.random.default_rng(20261028)
NAME = {"neutral": "neutral", "loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit"}
FRAMED = ["loss + you", "loss", "gain + you", "gain"]
pts = lambda x: f"{100 * x:+.1f}"
lo = lambda x: f"{x:+.2f}"
logit = lambda p: float(np.log(np.clip(p, 1e-4, 1 - 1e-4) / (1 - np.clip(p, 1e-4, 1 - 1e-4))))
pct = lambda x: f"{100 * x:.1f}%"


def ci(x):
    x = np.asarray(x, float)
    return tuple(np.percentile([x[RNG.integers(0, len(x), len(x))].mean() for _ in range(BOOT)], [2.5, 97.5]))


def paired(d):
    """Mean of per-career differences; p by flipping signs; 95% interval."""
    d = np.asarray(d, float)
    obs = d.mean()
    null = (RNG.choice([-1, 1], (PERMS, len(d))) * d).mean(1)
    return obs, ci(d), float((np.abs(null) >= abs(obs) - 1e-12).mean())


def unpaired(a, b):
    """Mean of a minus mean of b; p by reshuffling careers between the groups; 95% interval."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs, pool = a.mean() - b.mean(), np.concatenate([a, b])
    null = []
    for _ in range(PERMS):
        s = RNG.permutation(pool)
        null.append(s[:len(a)].mean() - s[len(a):].mean())
    boot = [a[RNG.integers(0, len(a), len(a))].mean() - b[RNG.integers(0, len(b), len(b))].mean() for _ in range(BOOT)]
    return obs, tuple(np.percentile(boot, [2.5, 97.5])), float((np.abs(null) >= abs(obs) - 1e-12).mean())


def line(label, res, n, scale=pts):
    obs, (a, b), p = res
    return f"| {label} | {n} | {scale(obs)} | {scale(a)} to {scale(b)} | {p:.4f} |"


md = ["# Push and cue: what carries B's framing from 7 to 12 January (exploratory)\n",
      "Produced by `designs/rd2/analysis/push_carry.py` from rereads of B's saved careers at UBS's 12 January request "
      "(`scripts/modal_push_carry.py`). P(the order goes along): after the fixed neutral reasoning line, over HOLD and "
      "every order size the agents used. Blame = loss + you, credit = gain + you. In B, UBS says nothing between its "
      "7 January and 12 January requests.\n"]
summary = {}

# ---------------- 1. the carry
path = os.path.join(DIR, "carry_rows.json")
if os.path.exists(path):
    rows = json.load(open(path))
    P, cover, hist = {}, {}, {}
    for r in rows:
        P.setdefault(r["career_file"], {})[(r["condition"], r["request"])] = r["p_order_along"]
        hist[r["career_file"]] = r["history"]
        if (r["condition"], r["request"]) == ("as saved", "neutral"):
            cover[r["career_file"]] = r["coverage"]
    keep = sorted(c for c in P if cover.get(c, 0) >= MIN_COVER)
    dropped = len(P) - len(keep)
    neutral = [P[c][("as saved", "neutral")] for c in keep if hist[c] == "neutral"]
    groups = {NAME[v]: [c for c in keep if hist[c] == v] for v in FRAMED}
    groups["all framed"] = [c for c in keep if hist[c] in FRAMED]
    md += ["## 1. The carry: UBS's earlier words set back to neutral, the agent's own words and trades kept\n",
           f"{len(keep)} careers ({dropped} dropped: the scored orders cover less than half the probability). "
           f"B's neutral careers ({len(neutral)}): {pct(np.mean(neutral))} with the neutral request.\n",
           "| UBS's words before 12 January | 12 January request | " + " | ".join(groups) + " |",
           "|---|---|" + "---|" * len(groups)]
    for cond, label in [("as saved", "as saved (framed)"), ("7 Jan neutral", "7 January request neutral"),
                        ("UBS neutral", "every earlier UBS line neutral")]:
        for req in ["neutral", "as saved"]:
            md.append(f"| {label} | {req} | " + " | ".join(pct(np.mean([P[c][(cond, req)] for c in cs])) if cs else "–"
                                                           for cs in groups.values()) + " |")
    for g in ["blame", "all framed"]:
        cs = groups[g]
        if not cs:
            continue
        get = lambda cond, req="neutral": np.array([P[c][(cond, req)] for c in cs])
        whole = unpaired(get("as saved"), neutral)
        words7 = paired(get("as saved") - get("7 Jan neutral"))
        words = paired(get("as saved") - get("UBS neutral"))
        rest = unpaired(get("UBS neutral"), neutral)
        md += [f"\n**{g.capitalize()} careers ({len(cs)}), the 12 January request neutral** (points of P(the order "
               "goes along))\n", "| Part | Careers | Change | 95% interval | p |", "|---|---|---|---|---|",
               line("The whole history: as saved minus B's neutral careers", whole, f"{len(cs)} vs {len(neutral)}"),
               line("UBS's 7 January words: as saved minus that request neutral", words7, len(cs)),
               line("All UBS's earlier words: as saved minus every earlier UBS line neutral", words, len(cs)),
               line("What is left, the agent's own record: every UBS line neutral minus B's neutral careers", rest,
                    f"{len(cs)} vs {len(neutral)}")]
        if abs(whole[0]) > 1e-9:
            md.append(f"\nShare of the whole history carried by UBS's earlier words: {100 * words[0] / whole[0]:.0f}% "
                      f"(by the 7 January request alone: {100 * words7[0] / whole[0]:.0f}%).")
        summary[f"carry_{g}"] = {"whole": whole[0], "words_7jan": words7[0], "words_all": words[0], "rest": rest[0]}

# ---------------- 2. the cue
path = os.path.join(DIR, "cue_rows.json")
if os.path.exists(path):
    cue = [r for r in json.load(open(path)) if r["coverage"] >= MIN_COVER]
    d = {r["career_file"]: r["p"]["loss + you"] - r["p"]["neutral"] for r in cue}
    dl = {r["career_file"]: logit(r["p"]["loss + you"]) - logit(r["p"]["neutral"]) for r in cue}
    by = lambda vs: [r for r in cue if r["history"] in vs]
    md += ["\n## 2. The cue: UBS's 12 January blame line (\"I'm counting on you to deliver it\") against the neutral "
           "line, the same moment\n",
           f"{len(cue)} careers (the matched rereads). The cue's effect: P(the order goes along) with the blame line "
           "minus with the neutral line, the history unchanged.\n",
           "| Career's own framing | Careers | Neutral line | Blame line | The cue's effect (points) | (log-odds) |",
           "|---|---|---|---|---|---|"]
    for v in ["neutral"] + FRAMED:
        rs = by([v])
        if rs:
            md.append(f"| {NAME[v]} | {len(rs)} | {pct(np.mean([r['p']['neutral'] for r in rs]))} | "
                      f"{pct(np.mean([r['p']['loss + you'] for r in rs]))} | {pts(np.mean([d[r['career_file']] for r in rs]))} | "
                      f"{lo(np.mean([dl[r['career_file']] for r in rs]))} |")
    eff = lambda vs, dd=d: [dd[r["career_file"]] for r in by(vs)]
    md += ["\n**Does the cue do more after a framed history?** (the cue's effect, careers reshuffled between groups)\n",
           "| Comparison | Careers | Difference | 95% interval | p |", "|---|---|---|---|---|"]
    tests = [(f"{NAME[v].capitalize()} careers minus neutral careers", [v], ["neutral"]) for v in FRAMED] + [
             ("All framed careers minus neutral careers", FRAMED, ["neutral"]),
             ("Loss and blame careers minus gain and credit careers", ["loss", "loss + you"], ["gain", "gain + you"])]
    for label, a, b in tests:
        if eff(a) and eff(b):
            md.append(line(label + ", points", unpaired(eff(a), eff(b)), f"{len(eff(a))} vs {len(eff(b))}"))
            md.append(line(label + ", log-odds", unpaired(eff(a, dl), eff(b, dl)), f"{len(eff(a))} vs {len(eff(b))}", lo))
    if eff(["loss + you"]) and eff(["neutral"]):
        summary["cue_blame_minus_neutral"] = unpaired(eff(["loss + you"]), eff(["neutral"]))[0]
        summary["cue_blame_minus_neutral_logodds"] = unpaired(eff(["loss + you"], dl), eff(["neutral"], dl))[0]
    layers = cue[0]["layers"] if cue else []
    blame, neu = by(["loss + you"]), by(["neutral"])
    if blame and neu:
        md += ["\n**Inside: does the cue's change to the state point the way the 7 January blame line's did?** Cosine "
               "between the two changes (blame line minus neutral line, at the last token before the reply), by layer; "
               "1 = the same direction, 0 = unrelated.\n",
               "| Layer | Blame careers | Neutral careers | Difference | p |", "|---|---|---|---|---|"]
        for i, L in enumerate(layers):
            a = [r["cosine_12_vs_7"][i] for r in blame]
            b = [r["cosine_12_vs_7"][i] for r in neu]
            obs, _, p = unpaired(a, b)
            md.append(f"| {L} | {np.mean(a):+.3f} | {np.mean(b):+.3f} | {obs:+.3f} | {p:.4f} |")

if len(md) == 2:
    md.append("No rows yet: run `scripts/modal_push_carry.py`.")
open(os.path.join(DIR, "PUSH_CARRY.md"), "w").write("\n".join(md) + "\n")
json.dump(summary, open(os.path.join(DIR, "push_carry.json"), "w"), indent=1, default=float)
print("\n".join(md))
