"""Careers with the frame's state carried in (notebook 35; sim/frame_state.py): B's neutral career with the state UBS's
framed lines (blame, or another frame) would have produced added at each UBS message and kept. Against B's neutral
careers (the base: the same words, nothing added) and the random direction of the same size; B's careers of that frame
(the framed words themselves) as the yardstick.

    python designs/rd2/analysis/frame_state.py [careers folder] [output dir]

Went along: the simulator's "joined" at each of UBS's six push requests, as in final_full_career.py. Tests reshuffle whole
careers between two groups (10,000 times), on each career's share of the six requests it went along with.
"""
import glob, json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PUSH = [("p344_i_can_hunt_with_u", "7 Jan"), ("p316_bust_through_it", "12 Jan"),
        ("p252_screw_other_people_harder", "1 Apr"), ("p250_grow_our_mafia", "8 Jun (third bank)"),
        ("p317_stop_busters", "8 Jun (stops)"), ("p253_11_oclock_rule", "5 Aug")]
FS = sys.argv[1] if len(sys.argv) > 1 else f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_frame_state_v2"
OUT = sys.argv[2] if len(sys.argv) > 2 else f"{ROOT}/results/frame_state"
B = f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2"
RNG = np.random.default_rng(20261029)
N = 10_000


def careers(folder, version):
    """[({push chat: went along (0/1)}, career)] for every finished career of this version."""
    out = []
    for p in sorted(glob.glob(f"{folder}/careers/*.json")):
        c = json.load(open(p))
        if c["version"] != version:
            continue
        days = sorted(glob.glob(p.replace("/careers/", "/days/")[:-5] + "_2011-*.json"))
        assert len(days) == 5, p
        row = {}
        for d in days:
            for cid, m in json.load(open(d))["summary"]["chats"].items():
                if cid in dict(PUSH) and m["wants"] in ("up", "down"):
                    row[cid] = int(bool(m["joined"]))
        out.append((row, c))
    return out


def share(rows):
    return np.array([np.mean([r[c] for c, _ in PUSH if c in r]) for r, _ in rows])


def perm(a, b):
    obs, pool, hits = a.mean() - b.mean(), np.concatenate([a, b]), 0
    for _ in range(N):
        RNG.shuffle(pool)
        hits += abs(pool[:len(a)].mean() - pool[len(a):].mean()) >= abs(obs) - 1e-12
    return (hits + 1) / (N + 1)


first = [json.load(open(p)) for p in sorted(glob.glob(f"{FS}/careers/*.json"))[:1]]
arms = sorted({json.load(open(p))["version"] for p in glob.glob(f"{FS}/careers/*.json")}, key=lambda v: v.startswith("random"))
how = (f"{first[0].get('construction', 'whole')} construction, {first[0].get('strength', 1):g} x its size, layer "
       f"{first[0]['layer']}") if first else "no careers yet"
FRAME = first[0].get("arm", ["frame", "loss + you"])[1] if first else "loss + you"
FRAME_NAME = {"loss + you": "blame", "gain + you": "credit", "loss": "loss", "gain": "gain"}[FRAME]
groups = [("B neutral: the same words, nothing added (base)", careers(B, "neutral"))]
groups += [(f"{v}: neutral words, the state carried in" if not v.startswith("random") else f"{v}: a random direction, same "
            "sizes (control)", careers(FS, v)) for v in arms]
groups += [(f"B {FRAME_NAME}: the framed words themselves (yardstick)", careers(B, FRAME))]
lines = ["# Careers with the frame's state carried in (exploratory)", "",
         "Notebook 35 (sim/frame_state.py): B's neutral career, UBS's neutral lines and the neutral memo, with the state "
         f"UBS's {FRAME_NAME} lines would have produced ({how}) added at each of the 29 updates with a UBS line, to the update "
         "and the reply under it, and kept there at every later read. \"whole\": the framed update's average state minus "
         "the neutral update's; \"after\": the difference on the tokens after the framed words only. Levels; the base "
         "first.", "",
         "## Went along at each push request (careers that went along / careers)", "",
         "| Careers | n | " + " | ".join(label for _, label in PUSH) + " | All six |",
         "|---|---|" + "---|" * (len(PUSH) + 1)]
for name, rows in groups:
    if not rows:
        lines.append(f"| {name} | 0 |" + " |" * (len(PUSH) + 1))
        continue
    cells = []
    for cid, _ in PUSH:
        hit = [r[cid] for r, _ in rows if cid in r]
        cells.append(f"{100 * np.mean(hit):.0f}% ({sum(hit)}/{len(hit)})" if hit else "-")
    lines.append(f"| {name} | {len(rows)} | " + " | ".join(cells) + f" | {100 * share(rows).mean():.0f}% |")
lines += ["", "## The six requests together (careers reshuffled)", "",
          "| Careers | n | Share of the six went along | p (vs B neutral) | p (vs random) |", "|---|---|---|---|---|"]
base = share(groups[0][1])
rand = next((share(rows) for name, rows in groups if name.startswith("random") and rows), None)
for name, rows in groups:
    if not rows:
        continue
    s = share(rows)
    p1 = "" if rows is groups[0][1] else f"{perm(s, base):.3f}"
    p2 = f"{perm(s, rand):.3f}" if rand is not None and not name.startswith(("random", "B neutral")) and len(rand) else ""
    lines.append(f"| {name} | {len(s)} | {100 * s.mean():.0f}% | {p1} | {p2} |")
lines += ["", "## The states added", "", "| Careers | Moments per career | Mean size | Replies steered |", "|---|---|---|---|"]
for name, rows in groups[1:-1]:
    for _, c in rows:
        ms = c["frame_state"]["moments"]
        lines.append(f"| {name.split(':')[0]} r{c['run']} | {len(ms)} | {np.mean([m['size'] for m in ms]):.1f} | "
                     f"{c['steered_replies']} of {sum(t['role'] == 'assistant' for t in c['history'])} |")
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/FRAME_STATE.md", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
