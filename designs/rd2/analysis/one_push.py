"""One framed push (notebook 34; the user, 28 Oct): only UBS's 7 January request in blame or credit, every other UBS
line neutral. Against B's neutral careers (every UBS line neutral) and, for reference, B's blame and credit careers
(every UBS line framed, the frozen file's lines).

    python designs/rd2/analysis/one_push.py > results/one_push/ONE_PUSH.md

Went along: the simulator's "joined" at each of UBS's six push requests, as in final_full_career.py. The test reshuffles
whole careers between the two groups (10,000 times), on each career's share of the five later requests it went along
with.
"""
import glob, json, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PUSH = [("p344_i_can_hunt_with_u", "7 Jan"), ("p316_bust_through_it", "12 Jan"),
        ("p252_screw_other_people_harder", "1 Apr"), ("p250_grow_our_mafia", "8 Jun (third bank)"),
        ("p317_stop_busters", "8 Jun (stops)"), ("p253_11_oclock_rule", "5 Aug")]
LATER = [cid for cid, _ in PUSH[1:]]
B, P1 = "ubs_framing_v2", "one_push_v2"
GROUPS = [("B neutral: every UBS line neutral", B, "neutral"),
          ("One push, blame: only 7 Jan framed", P1, "loss + you"),
          ("One push, credit: only 7 Jan framed", P1, "gain + you"),
          ("B blame: every UBS line framed (reference)", B, "loss + you"),
          ("B credit: every UBS line framed (reference)", B, "gain + you")]
RNG = np.random.default_rng(20261028)
N = 10_000


def careers(folder, version):
    """[{push chat: went along (0/1)}] for every finished career of this version."""
    out = []
    for p in sorted(glob.glob(f"{ROOT}/results/full_career_gemma-3-12b-it_4bit_{folder}/careers/*.json")):
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
        out.append(row)
    return out


def later_share(rows):
    return np.array([np.mean([r[c] for c in LATER if c in r]) for r in rows])


def perm(a, b):
    obs, pool, hits = a.mean() - b.mean(), np.concatenate([a, b]), 0
    for _ in range(N):
        RNG.shuffle(pool)
        hits += abs(pool[:len(a)].mean() - pool[len(a):].mean()) >= abs(obs) - 1e-12
    return (hits + 1) / (N + 1)


data = {name: careers(folder, v) for name, folder, v in GROUPS}
print("# One framed push: does a framed 7 January request change the later neutral requests? (exploratory)\n")
print("Notebook 34: B's career with only UBS's 7 January request framed, in the user's lines of 28 Oct (blame \"...If it "
      "stays up, we're both underwater, and that'd be on you.\"; credit \"...If it drops, we both come out ahead, that'd "
      "be all thanks to you.\"); every other UBS line neutral, the neutral memo. B's blame and credit careers used the "
      "frozen file's lines and every UBS line framed, so they are a reference, not a control.\n")
print("## Went along at each push request (careers that went along / careers)\n")
print("| Careers | n | " + " | ".join(label for _, label in PUSH) + " | The five later requests |")
print("|---|---|" + "---|" * (len(PUSH) + 1))
for name, rows in data.items():
    if not rows:
        print(f"| {name} | 0 |" + " |" * (len(PUSH) + 1))
        continue
    cells = []
    for cid, _ in PUSH:
        hit = [r[cid] for r in rows if cid in r]
        cells.append(f"{100 * np.mean(hit):.0f}% ({sum(hit)}/{len(hit)})" if hit else "-")
    print(f"| {name} | {len(rows)} | " + " | ".join(cells) + f" | {100 * later_share(rows).mean():.0f}% |")
print("\n## The five later requests, against B's neutral careers (careers reshuffled)\n")
print("| Careers | n | Share of the later requests went along | p (vs B neutral) |")
print("|---|---|---|---|")
base = later_share(data[GROUPS[0][0]])
print(f"| {GROUPS[0][0]} | {len(base)} | {100 * base.mean():.0f}% | |")
for name, _, _ in GROUPS[1:3]:
    rows = data[name]
    if rows:
        s = later_share(rows)
        print(f"| {name} | {len(s)} | {100 * s.mean():.0f}% | {perm(s, base):.3f} |")
print("\n## Did going along on 7 January carry on? (one-push careers)\n")
for name, _, _ in GROUPS[1:3]:
    rows = data[name]
    for joined in (1, 0):
        sub = [r for r in rows if r.get(PUSH[0][0]) == joined]
        if sub:
            print(f"- {name}, {'went along' if joined else 'did not go along'} on 7 Jan ({len(sub)} careers): "
                  f"later requests went along {100 * later_share(sub).mean():.0f}%")
