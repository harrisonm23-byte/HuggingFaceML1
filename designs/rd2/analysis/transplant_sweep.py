"""The frame's state at every layer (sim/transplant_sweep.py): results/transplant_sweep/TRANSPLANT_SWEEP.md.

    python designs/rd2/analysis/transplant_sweep.py /states/v2/transplant_sweep results/transplant_sweep

Levels: P(the order goes along) after the fixed neutral reasoning line, averaged over the moments where the scored orders
cover at least half of the probability with nothing added. p against none at the same moments (sign flips by career,
20,000 times), and against the random direction of the same size at the same layer. Also each construction's size by
layer and the cosine between "whole" and "after" (from the saved vectors).
"""
import glob, json, os, random, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "sim"))
from transplant_sweep import LAYERS, conditions


def load(folder):
    rows = {}
    for p in sorted(glob.glob(os.path.join(folder, "part*.jsonl"))):
        for line in open(p):
            r = json.loads(line)
            rows[r["key"]] = r
    return list(rows.values())


def flip_p(diffs, n=20_000, seed=20261029):
    if not diffs:
        return None
    rng, obs = random.Random(seed), abs(sum(diffs) / len(diffs))
    hits = sum(abs(sum(d if rng.random() < 0.5 else -d for d in diffs) / len(diffs)) >= obs - 1e-12 for _ in range(n))
    return (hits + 1) / (n + 1)


def fmt_p(p):
    return "" if p is None else ("<0.001" if p < 0.001 else f"{p:.3f}")


def main(src, out):
    rows = load(src)
    by = {(r["career_file"], r["history_index"], r["condition"]): r for r in rows}
    moments = sorted({(r["career_file"], r["history_index"]) for r in rows})
    ok = [m for m in moments if (*m, "none") in by and by[(*m, "none")]["coverage"] >= 0.5]

    def level(cond):
        vals = [by[(*m, cond)]["p_order_along"] for m in ok if (*m, cond) in by]
        return (100 * np.mean(vals), len(vals)) if vals else (None, 0)

    def p_vs(cond, base):
        d = [by[(*m, cond)]["p_order_along"] - by[(*m, base)]["p_order_along"] for m in ok if (*m, cond) in by and (*m, base) in by]
        return flip_p(d)

    none, n0 = level("none")
    framed, _ = level(f"framed (loss + you), as read")
    pct = lambda v: "-" if v is None else f"{v:.1f}%"
    lines = ["# The frame's state at every layer (exploratory)", "",
             f"B's neutral careers at the 7 and 12 January requests: {len(moments)} moments, {len(ok)} where the scored "
             "orders cover at least half of the probability with nothing added. P(the order goes along) after the fixed "
             "neutral reasoning line; levels, the base first. \"whole\": the framed update's average state minus the "
             "neutral update's (notebook 35's construction); \"after\": the difference on the tokens after the framed words "
             "only (the document states' construction). Each added to every token of the update and the reply, against a "
             "random direction of the same size at the same layer. p: sign flips by career against none at the same moments.",
             "", f"**Nothing added: {pct(none)}. The blame words themselves, as read: {pct(framed)} "
             f"(p {fmt_p(p_vs('framed (loss + you), as read', 'none'))}).**", "",
             "| Layer | whole x1 | p vs none | random, whole size | after x1 | p vs none | after x2 | p vs none | p vs random | random, after x2 size | after x4 | p vs none | p vs random | random, after x4 size |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for L in LAYERS:
        w, _ = level(f"whole x1 L{L}")
        if w is None:
            continue
        rw, _ = level(f"random, whole size, L{L}")
        a1, _ = level(f"after x1 L{L}")
        a2, _ = level(f"after x2 L{L}")
        ra, _ = level(f"random, after x2 size, L{L}")
        a4, _ = level(f"after x4 L{L}")
        ra4, _ = level(f"random, after x4 size, L{L}")
        lines.append(f"| {L} | {pct(w)} | {fmt_p(p_vs(f'whole x1 L{L}', 'none'))} | {pct(rw)} | {pct(a1)} | "
                     f"{fmt_p(p_vs(f'after x1 L{L}', 'none'))} | {pct(a2)} | {fmt_p(p_vs(f'after x2 L{L}', 'none'))} | "
                     f"{fmt_p(p_vs(f'after x2 L{L}', f'random, after x2 size, L{L}'))} | {pct(ra)} | {pct(a4)} | "
                     f"{fmt_p(p_vs(f'after x4 L{L}', 'none'))} | {fmt_p(p_vs(f'after x4 L{L}', f'random, after x4 size, L{L}'))} | {pct(ra4)} |")
    lines += ["", "## The states' sizes by layer (mean over the moments) and how far the two constructions agree", "",
              "| Layer | whole, size | after, size | cosine(whole, after) | tokens after the framed words |", "|---|---|---|---|---|"]
    shifts = [np.load(p, allow_pickle=False) for p in sorted(glob.glob(os.path.join(src, "shifts", "*.npz")))]
    if shifts:
        after_tok = [json.loads(str(z["meta"]))["after_tokens"] for z in shifts]
        for j, L in enumerate(LAYERS):
            w = np.stack([z["whole"][j] for z in shifts]); a = np.stack([z["after"][j] for z in shifts])
            cos = np.mean([float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y))) for x, y in zip(w, a)])
            lines.append(f"| {L} | {np.linalg.norm(w, axis=1).mean():.0f} | {np.linalg.norm(a, axis=1).mean():.0f} | {cos:.2f} | "
                         f"{np.mean(after_tok):.1f} |")
    os.makedirs(out, exist_ok=True)
    json.dump({"rows": rows}, open(os.path.join(out, "rows.json"), "w"))
    open(os.path.join(out, "TRANSPLANT_SWEEP.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
