"""Attention onto "you" (sim/attention_you.py, scripts/modal_attention_you.py): results/attention_you/ATTENTION_YOU.md.

    python designs/rd2/analysis/attention_you.py /states/v2 results/attention_you

Masses are shares of a head's attention (each head's masses over the key groups sum to 1), averaged over heads and
layers unless a layer or a layer type is named. Same moment, different frame: every comparison between framings is
paired within the moment. p: sign flips of each career's mean difference (20,000 flips). The link to the decision uses
the matched run's P(order goes along) at the same moments (/states/v2/matched/B_bf16, UBS's line alone, no Bank C).
"""
import glob, json, os, sys

import numpy as np

FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
NAME = {"neutral": "Neutral", "loss": "Loss", "gain": "Gain", "loss + you": "Blame", "gain + you": "Credit"}
GROUP_NAME = {"history": "History before the update", "update_rest": "Rest of the update", "core_other": "UBS's neutral core",
              "you_core": "\"you\" in the core", "extra_other": "The framed extra", "you_extra": "\"you\" in the extra",
              "tail": "Template tail", "core": "UBS's core", "extra_before_you": "The extra before \"you\"",
              "you_and_after": "Itself"}
RNG = np.random.default_rng(20261030)


def load(root):
    files = sorted(glob.glob(os.path.join(root, "attention_you", "*.npz")))
    dec, into, rows, groups, igroups, types = [], [], [], None, None, None
    for f in files:
        z = np.load(f)
        meta = json.loads(str(z["meta"]))
        assert [r["framing"] for r in meta] == FRAMINGS, f
        dec.append(z["decision"])
        into.append(z["into_you"])
        rows.append(meta)
        groups, igroups, types = list(z["decision_groups"]), list(z["into_you_groups"]), list(z["layer_types"])
    return np.stack(dec), np.stack(into), rows, groups, igroups, types     # dec: moments x F x L x H x G


def matched_p(root):
    """{(career_file, chat): {framing: P(order goes along)}} from the matched run (UBS's line alone)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(root, "matched", "B_bf16", "*.npz"))):
        for r in json.loads(str(np.load(f)["meta"])):
            if not r["bank_c"]:
                out.setdefault((r["career_file"], r["chat"]), {})[r["framing"]] = r["p_order_along"]
    return out


def flip_p(diffs, n=20_000):
    d = np.asarray(diffs, dtype=float)
    if len(d) == 0:
        return float("nan")
    obs = abs(d.mean())
    signs = RNG.choice([-1.0, 1.0], size=(n, len(d)))
    return (np.sum(np.abs((signs * d).mean(1)) >= obs - 1e-12) + 1) / (n + 1)


def by_career(values, rows):
    """Mean of a per-moment value within each career."""
    per = {}
    for v, r in zip(values, rows):
        per.setdefault(r[0]["career_file"], []).append(v)
    return [float(np.mean(v)) for v in per.values()]


def pct(x):
    return f"{100 * x:.1f}%"


def main(root, out):
    dec, into, rows, groups, igroups, types = load(root)
    M, F, L, H, G = dec.shape
    glob_l = np.array([t == "full_attention" for t in types])
    P = matched_p(root)
    md = ["# Attention onto \"you\" (exploratory)", "",
          f"B's {M} saved requests ({len({r[0]['career_file'] for r in rows})} careers), each read with UBS's request in the "
          f"five framings and the history held fixed. {L} layers ({int(glob_l.sum())} global, {int((~glob_l).sum())} local "
          f"with a sliding window), {H} heads. A cell is the share of a head's attention on that group of tokens, averaged "
          "over heads, layers and moments. Levels, neutral first; comparisons between framings are paired within the moment."]
    g = {name: groups.index(name) for name in groups}
    # ---- A. where the decision token looks
    for title, sel in (("all layers", np.ones(L, bool)), ("global layers only (the ones that can see the whole history)", glob_l)):
        md += ["", f"## Where the decision token looks, {title}", "",
               "| Framing | " + " | ".join(GROUP_NAME[x] for x in groups) + " |", "|---|" + "---|" * len(groups)]
        for i, v in enumerate(FRAMINGS):
            m = dec[:, i][:, sel].mean((0, 1, 2))
            md.append(f"| {NAME[v]} | " + " | ".join(pct(x) for x in m) + " |")
    # per-token attention: a "you" token against an average token of the extra
    md += ["", "## Attention per token: one \"you\" against one other token of the extra (all layers)", "",
           "| Framing | Per \"you\" token | Per other token of the extra | Ratio |", "|---|---|---|---|"]
    for v in ("loss + you", "gain + you"):
        i = FRAMINGS.index(v)
        ny = np.array([r[i]["n_you_extra"] for r in rows], float)
        ne = np.array([r[i]["n_extra_other"] for r in rows], float)
        py = (dec[:, i, :, :, g["you_extra"]].mean((1, 2)) / ny)
        pe = (dec[:, i, :, :, g["extra_other"]].mean((1, 2)) / ne)
        md.append(f"| {NAME[v]} | {100 * py.mean():.2f}% | {100 * pe.mean():.2f}% | {py.mean() / pe.mean():.2f} |")
    # ---- B. the "you" clause against the loss or gain clause: mass on the whole extra
    md += ["", "## Does the \"you\" clause draw more attention than the loss or gain clause? (mass on the whole framed extra)", "",
           "| Pair | Extra, first | Extra, second | Difference | p |", "|---|---|---|---|---|"]
    extra_all = dec[:, :, :, :, g["extra_other"]] + dec[:, :, :, :, g["you_extra"]]
    for a, b in (("loss + you", "loss"), ("gain + you", "gain"), ("loss", "gain"), ("loss + you", "gain + you")):
        ia, ib = FRAMINGS.index(a), FRAMINGS.index(b)
        xa, xb = extra_all[:, ia].mean((1, 2)), extra_all[:, ib].mean((1, 2))
        md.append(f"| {NAME[a]} vs {NAME[b]} | {pct(xa.mean())} | {pct(xb.mean())} | {100 * (xa - xb).mean():+.2f} points | "
                  f"{flip_p(by_career(xa - xb, rows)):.3f} |")
    # ---- C. the layer profile of "you" in the extra
    md += ["", "## By layer: share of a head's attention on \"you\" in the extra, and on the whole extra", "",
           "| Layer | Type | Blame: \"you\" | Credit: \"you\" | Blame: extra | Loss: extra | Credit: extra | Gain: extra |",
           "|---|---|---|---|---|---|---|---|"]
    for l in range(L):
        cells = [pct(dec[:, FRAMINGS.index(v), l, :, g["you_extra"]].mean()) for v in ("loss + you", "gain + you")]
        cells += [pct(extra_all[:, FRAMINGS.index(v), l].mean()) for v in ("loss + you", "loss", "gain + you", "gain")]
        md.append(f"| {l} | {'global' if glob_l[l] else 'local'} | " + " | ".join(cells) + " |")
    # ---- D. heads
    md += ["", "## The heads that look at \"you\" most (blame; mean share of the head's attention)", "",
           "| Layer | Head | Blame: \"you\" in the extra | Credit: \"you\" in the extra | Neutral: \"you\" in the core |",
           "|---|---|---|---|---|"]
    yb = dec[:, FRAMINGS.index("loss + you"), :, :, g["you_extra"]].mean(0)
    yc = dec[:, FRAMINGS.index("gain + you"), :, :, g["you_extra"]].mean(0)
    yn = dec[:, FRAMINGS.index("neutral"), :, :, g["you_core"]].mean(0)
    for l, h in sorted(np.ndindex(yb.shape), key=lambda lh: -yb[lh])[:10]:
        md.append(f"| {l} | {h} | {pct(yb[l, h])} | {pct(yc[l, h])} | {pct(yn[l, h])} |")
    # ---- E. into "you"
    ig = {name: igroups.index(name) for name in igroups}
    md += ["", "## Into \"you\": where the \"you\" token itself looks (blame and credit; all layers, then global layers)", "",
           "| Framing | Layers | " + " | ".join(GROUP_NAME[x] for x in igroups) + " |", "|---|---|" + "---|" * len(igroups)]
    for v in ("loss + you", "gain + you"):
        i = FRAMINGS.index(v)
        for title, sel in (("all", np.ones(L, bool)), ("global", glob_l)):
            m = np.nanmean(into[:, i][:, sel], axis=(0, 1, 2))
            md.append(f"| {NAME[v]} | {title} | " + " | ".join(pct(x) for x in m) + " |")
    # ---- F. the link to the decision
    summary = {"moments": M, "layers": L, "heads": H}
    md += ["", "## Does attention on \"you\" go with the decision?", ""]
    if P:
        p_of = lambda r, v: P.get((r[0]["career_file"], r[0]["chat"]), {}).get(v)
        md += ["P(order goes along) is the matched run's reading at the same moment (UBS's line alone). r is Pearson's, "
               "across moments; p by reshuffling P across moments (20,000 times).", "",
               "| Comparison | n | r | p |", "|---|---|---|---|"]

        def corr_row(name, x, y):
            x, y = np.asarray(x, float), np.asarray(y, float)
            keep = np.isfinite(x) & np.isfinite(y)
            x, y = x[keep], y[keep]
            if len(x) < 4 or x.std() == 0 or y.std() == 0:
                md.append(f"| {name} | {len(x)} | - | - |")
                return
            r = float(np.corrcoef(x, y)[0, 1])
            perm = np.array([np.corrcoef(x, RNG.permutation(y))[0, 1] for _ in range(20_000)])
            pv = (np.sum(np.abs(perm) >= abs(r) - 1e-12) + 1) / 20_001
            md.append(f"| {name} | {len(x)} | {r:+.3f} | {pv:.3f} |")
            summary[name] = {"n": int(len(x)), "r": r, "p": float(pv)}
        for v in ("loss + you", "gain + you"):
            i = FRAMINGS.index(v)
            you = dec[:, i, :, :, g["you_extra"]].mean((1, 2))
            you_g = dec[:, i][:, glob_l][:, :, :, g["you_extra"]].mean((1, 2))
            pv = [p_of(r, v) for r in rows]
            corr_row(f"{NAME[v]}: \"you\" mass (all layers) against P(goes along) under {NAME[v]}", you, pv)
            corr_row(f"{NAME[v]}: \"you\" mass (global layers) against P(goes along) under {NAME[v]}", you_g, pv)
            base = "loss" if v == "loss + you" else "gain"
            ib = FRAMINGS.index(base)
            dx = extra_all[:, i].mean((1, 2)) - extra_all[:, ib].mean((1, 2))
            dp = [None if p_of(r, v) is None or p_of(r, base) is None else p_of(r, v) - p_of(r, base) for r in rows]
            corr_row(f"{NAME[v]} minus {NAME[base]}: extra mass against P(goes along), same moment", dx,
                     [np.nan if d is None else d for d in dp])
    else:
        md.append("The matched run's readings were not found under /states/v2/matched/B_bf16; the link to the decision is left out.")
    os.makedirs(out, exist_ok=True)
    summary["decision_mean"] = {NAME[v]: {x: float(dec[:, i, :, :, g[x]].mean()) for x in groups} for i, v in enumerate(FRAMINGS)}
    json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=1)
    open(os.path.join(out, "ATTENTION_YOU.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:14]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
