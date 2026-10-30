"""The four frames' states side by side (sim/transplant_sweep.py run per frame): results/transplant_sweep/FRAMES.md.

    python designs/rd2/analysis/transplant_frames.py /states/v2 results/transplant_sweep [results/words_b/key.json]

Reads every transplant_sweep* folder under the states folder (one frame each). At each layer every frame was run at:
P(the order goes along) with the frame's "after" state at one, two and four times its size, the frame's words as read,
and the random direction of the same size (the same direction for every frame), each with the probability still on a
proper order in brackets. Moments: those where the scored orders cover at least half of the probability with nothing
added. p: sign flips by career against none at the same moments. B's careers' traded-along share at the six push requests
(results/words_b/key.json) sits beside each frame as the yardstick of what the words did over careers.
"""
import glob, json, os, random, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
NAME = {"loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit"}
ORDER = ["gain", "gain + you", "loss", "loss + you"]


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


def main(states, out, b_key=None):
    frames = {}
    for folder in sorted(glob.glob(os.path.join(states, "transplant_sweep*"))):
        rows = load(folder)
        if rows:
            framed = next(r["condition"] for r in rows if r["kind"] == "framed")
            frames[framed[len("framed ("):-len("), as read")]] = rows
    frames = {f: frames[f] for f in ORDER if f in frames}
    assert frames, f"no transplant_sweep folders under {states}"
    base_rows = frames.get("loss + you", next(iter(frames.values())))
    none = {(r["career_file"], r["history_index"]): r for r in base_rows if r["condition"] == "none"}
    ok = sorted(m for m, r in none.items() if r["coverage"] >= 0.5)
    layers = sorted(set.intersection(*[{r["layer"] for r in rows if r["layer"] is not None} for rows in frames.values()]))
    traded = {}
    b_key = b_key or os.path.join(ROOT, "results/words_b/key.json")
    if os.path.exists(b_key):
        key = json.load(open(b_key))
        for v in NAME:
            push = [m for m in key.values() if m["version"] == v and m["push_request"]]
            traded[v] = 100 * sum(bool(m["traded_along"]) for m in push) / len(push) if push else None

    def cell(rows, cond, with_p=False):
        by = {(r["career_file"], r["history_index"]): r for r in rows if r["condition"] == cond}
        vals = [by[m]["p_order_along"] for m in ok if m in by]
        if not vals:
            return "-" + (" | " if with_p else "")
        cov = np.mean([by[m]["coverage"] for m in ok if m in by])
        s = f"{100 * np.mean(vals):.1f}% ({cov:.2f})"
        if with_p:
            s += " | " + fmt_p(flip_p([by[m]["p_order_along"] - none[m]["p_order_along"] for m in ok if m in by]))
        return s

    none_level = 100 * np.mean([none[m]["p_order_along"] for m in ok]) if ok else None
    none_cov = np.mean([none[m]["coverage"] for m in ok]) if ok else None
    lines = ["# The four frames' states, side by side (exploratory)", "",
             f"B's neutral careers at the 7 and 12 January requests: {len(none)} moments, {len(ok)} where the scored orders "
             "cover at least half of the probability with nothing added. Each frame's \"after\" state (the framed request "
             "minus the neutral one on the tokens after the framed words) added to every token of the update and the reply, "
             "at one, two and four times its size, against the frame's words as read and a random direction of the same "
             "size (one direction per layer, the same for every frame). Cells: P(the order goes along), and in brackets the "
             "probability still on a proper order (HOLD or a TARGET). p: sign flips by career against none at the same "
             "moments. \"B careers\": the share of the six push requests traded along in B's ten careers of that frame.", "",
             f"**Nothing added: {none_level:.1f}% ({none_cov:.2f}).**" if ok else "**Nothing added: -**",
             f"Frames run: {', '.join(NAME[f] for f in frames)}; layers run for every frame: {layers}."]
    for L in layers:
        lines += ["", f"## Layer {L}", "",
                  "| Frame | B careers | words as read | p | after x1 | p | after x2 | p | after x4 | p | random, x2 size | random, x4 size |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for f, rows in frames.items():
            b = f"{traded[f]:.0f}%" if traded.get(f) is not None else "-"
            lines.append(f"| {NAME[f]} | {b} | {cell(rows, f'framed ({f}), as read', True)} | {cell(rows, f'after x1 L{L}', True)} | "
                         f"{cell(rows, f'after x2 L{L}', True)} | {cell(rows, f'after x4 L{L}', True)} | "
                         f"{cell(rows, f'random, after x2 size, L{L}')} | {cell(rows, f'random, after x4 size, L{L}')} |")
    lines += ["", "## The states' sizes by frame and layer (mean over the moments)", "",
              "| Frame | " + " | ".join(f"L{L}" for L in layers) + " |", "|---|" + "---|" * len(layers)]
    for f in frames:
        folder = next(p for p in glob.glob(os.path.join(states, "transplant_sweep*"))
                      if any(r["condition"] == f"framed ({f}), as read" for r in load(p)))
        zs = [np.load(p, allow_pickle=False) for p in sorted(glob.glob(os.path.join(folder, "shifts", "*.npz")))]
        sizes = []
        for L in layers:
            a = [np.linalg.norm(z["after"][list(z["layers"]).index(L)]) for z in zs if L in list(z["layers"])]
            sizes.append(f"{np.mean(a):.0f}" if a else "-")
        lines.append(f"| {NAME[f]} | " + " | ".join(sizes) + " |")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "FRAMES.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
