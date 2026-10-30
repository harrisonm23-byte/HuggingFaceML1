"""Attention onto "you" (sim/attention_you.py, scripts/modal_attention_you.py): results/attention_you/ATTENTION_YOU.md.

    python designs/rd2/analysis/attention_you.py /states/v2 results/attention_you
    python designs/rd2/analysis/attention_you.py /states/v2 results/attention_you_chat --chat     # the chat-only days

Masses are shares of a head's attention (each head's masses over the key groups sum to 1), averaged over heads and
layers unless a layer or a layer type is named. Same moment, different frame: every comparison between framings is
paired within the moment. p: sign flips of each career's mean difference (20,000 flips). The link to the decision uses
the matched run's P(order goes along) at the same moments (/states/v2/matched/B_bf16, UBS's line alone, no Bank C).
On the chat-only days there is no order: the link is to the blind words labels (results/words_b) of the reply each
career actually wrote, in the framing it actually saw.
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


def load(root, folder="attention_you"):
    files = sorted(glob.glob(os.path.join(root, folder, "*.npz")))
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


def words_labels(root_results):
    """{(career_file, history_index): AGREES / REFUSES / NONCOMMITTAL / NO_ASK / None (no chat message)}."""
    key = json.load(open(os.path.join(root_results, "words_b", "key.json")))
    lab = {}
    for p in sorted(glob.glob(os.path.join(root_results, "words_b", "labels_batch_*.json"))):
        lab.update({k: v.strip().upper() for k, v in json.load(open(p)).items()})
    return {(m["career_file"], m["turn"]): lab.get(k) for k, m in key.items()}


def main(root, out, chat=False):
    dec, into, rows, groups, igroups, types = load(root, "attention_you_chat" if chat else "attention_you")
    M, F, L, H, G = dec.shape
    glob_l = np.array([t == "full_attention" for t in types])
    P = {} if chat else matched_p(root)
    what = "chat-only-day updates with a UBS line" if chat else "saved requests"
    md = ["# Attention onto \"you\"" + (", the chat-only days" if chat else "") + " (exploratory)", "",
          f"B's {M} {what} ({len({r[0]['career_file'] for r in rows})} careers), each read with UBS's lines in the "
          f"five framings and the history held fixed. {L} layers ({int(glob_l.sum())} global, {int((~glob_l).sum())} local "
          f"with a sliding window), {H} heads. A cell is the share of a head's attention on that group of tokens, averaged "
          "over heads, layers and moments. Levels, neutral first; comparisons between framings are paired within the moment."]
    g = {name: groups.index(name) for name in groups}
    extra_all = dec[:, :, :, :, g["extra_other"]] + dec[:, :, :, :, g["you_extra"]]
    # ---- 0. the framed sentence, 2 x 2: negative or positive, with "you" or without; per token, so length does not count
    md += ["", "## The framed sentence: negative or positive, \"you\" or not (all layers)", "",
           "Each framing adds a sentence to UBS's line (or rewrites part of it). Attention on the whole sentence, and per "
           "token (the sentences differ in length). p: per-token difference, sign flips by career.", "",
           "| Framed sentence | Tokens | Attention on the sentence | Per token |", "|---|---|---|---|"]
    ntok = {v: np.array([r[i]["n_extra_other"] + r[i]["n_you_extra"] for r in rows], float) for i, v in enumerate(FRAMINGS)}
    per_tok = {}
    for i, v in enumerate(FRAMINGS[1:], 1):
        a = extra_all[:, i].mean((1, 2))
        per_tok[v] = np.where(ntok[v] > 0, a / np.maximum(ntok[v], 1), np.nan)
        md.append(f"| {NAME[v]} | {ntok[v].mean():.1f} | {pct(a.mean())} | {100 * a.sum() / ntok[v].sum():.3f}% |")
    nc = np.array([r[0]["n_core_other"] + r[0]["n_you_core"] for r in rows], float)
    cm = (dec[:, 0, :, :, g["core_other"]] + dec[:, 0, :, :, g["you_core"]]).mean((1, 2))
    md.append(f"| (UBS's neutral line, for scale) | {nc.mean():.1f} | {pct(cm.mean())} | {100 * cm.sum() / nc.sum():.3f}% |")
    md += ["", "| Comparison, per token | Difference | p |", "|---|---|---|"]
    for a_, b_, what_ in (("loss", "gain", "negative vs positive, no \"you\""), ("loss + you", "gain + you", "negative vs positive, with \"you\""),
                          ("loss + you", "loss", "\"you\" vs not, negative"), ("gain + you", "gain", "\"you\" vs not, positive")):
        d = per_tok[a_] - per_tok[b_]
        keep = np.isfinite(d)
        md.append(f"| {NAME[a_]} minus {NAME[b_]} ({what_}) | {100 * np.nanmean(d):+.3f} points per token | "
                  f"{flip_p(by_career(d[keep], [r for r, k in zip(rows, keep) if k])):.3f} |")
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
    elif chat:
        here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        W = words_labels(os.path.join(here, "results"))
        md += ["The reply each career actually wrote (its own framing), labelled blind from its chat message: does the "
               "attention on the framed sentence, per token, differ where it agreed in words? p: labels reshuffled across "
               "moments within the framing (20,000 times). The history's length is reported, since a longer history "
               "takes attention from everything in the update.", "",
               "| Career's framing | Replies with UBS asking | Agreed | Per token, agreed | Per token, did not | p | "
               "History tokens, agreed | did not |", "|---|---|---|---|---|---|---|---|"]
        for v in FRAMINGS[1:]:
            i = FRAMINGS.index(v)
            sel = [(k, r) for k, r in enumerate(rows) if r[0]["history"] == v]
            lab = [W.get((r[0]["career_file"], r[0]["history_index"])) for _, r in sel]
            asked = [(k, r, l) for (k, r), l in zip(sel, lab) if l != "NO_ASK"]
            if not asked:
                continue
            x = np.array([per_tok[v][k] for k, _, _ in asked])
            y = np.array([l == "AGREES" for _, _, l in asked])
            hist = np.array([r[i]["update_start"] for _, r, _ in asked], float)
            keep = np.isfinite(x)
            x, y, hist = x[keep], y[keep], hist[keep]
            if y.sum() == 0 or (~y).sum() == 0:
                md.append(f"| {NAME[v]} | {len(y)} | {int(y.sum())} | - | - | - | - | - |")
                continue
            obs = x[y].mean() - x[~y].mean()
            perm = np.array([(lambda z: x[z].mean() - x[~z].mean())(RNG.permutation(y)) for _ in range(20_000)])
            pv = (np.sum(np.abs(perm) >= abs(obs) - 1e-12) + 1) / 20_001
            md.append(f"| {NAME[v]} | {len(y)} | {int(y.sum())} | {100 * x[y].mean():.3f}% | {100 * x[~y].mean():.3f}% | "
                      f"{pv:.3f} | {hist[y].mean():,.0f} | {hist[~y].mean():,.0f} |")
            summary[f"words_{v}"] = {"n": int(len(y)), "agreed": int(y.sum()), "per_token_agreed": float(x[y].mean()),
                                    "per_token_not": float(x[~y].mean()), "p": float(pv)}
    else:
        md.append("The matched run's readings were not found under /states/v2/matched/B_bf16; the link to the decision is left out.")
    os.makedirs(out, exist_ok=True)
    summary["decision_mean"] = {NAME[v]: {x: float(dec[:, i, :, :, g[x]].mean()) for x in groups} for i, v in enumerate(FRAMINGS)}
    json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=1)
    open(os.path.join(out, "ATTENTION_YOU.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:14]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], chat="--chat" in sys.argv[3:])
