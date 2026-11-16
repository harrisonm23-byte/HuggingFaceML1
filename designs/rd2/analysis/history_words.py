"""Does what a Ministral 3 career said before 2011 go with whether it later went along? (exploratory)

    python designs/rd2/analysis/history_words.py      -> results/history_words_ministral/HISTORY_WORDS.md

Labels: two blind graders on every pre-2011 chat reply (history_words_prep.py; rubric GRADER_PROMPT.md, the paper's
words rubric with any trader's proposal counted, not only UBS's). A label counts where both graders gave it. Each career's
early agreement: its AGREES among the replies where something was proposed (NO_ASK and split labels left out).
Outcomes from the trades, as in B: went along at 7 Jan, and at the six push requests. Tests reshuffle careers (100,000
times), also within framing, since the five framings are mixed here.
"""
import collections, glob, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, "results", "history_words_ministral")
FOLDER = os.path.join(ROOT, "results", "full_career_Ministral-3-14B-Instruct-2512-BF16_4bit_ubs_framing_v2")
PUSH = ["p344_i_can_hunt_with_u", "p316_bust_through_it", "p252_screw_other_people_harder", "p250_grow_our_mafia",
        "p317_stop_busters", "p253_11_oclock_rule"]
key = json.load(open(os.path.join(OUT, "key.json")))
g1, g2 = (json.load(open(os.path.join(OUT, f"labels_g{n}.json"))) for n in (1, 2))
graded = {k for k, m in key.items() if m["has_chat"]}
assert set(g1) == set(g2) == graded
rng = random.Random(20261030)


def outcomes(name):
    joined = {}
    for d in glob.glob(os.path.join(FOLDER, "days", name[:-5] + "_2011-*.json")):
        ch = json.load(open(d))["summary"]["chats"]
        joined.update({c: bool(ch[c]["joined"]) for c in PUSH if c in ch})
    return [joined[c] for c in PUSH]


def early(labels):
    by = collections.defaultdict(list)
    for k in graded:
        if labels[k] not in ("NO_ASK", None):
            by[key[k]["career_file"]].append(labels[k] == "AGREES")
    return {c: sum(v) / len(v) for c, v in by.items()}


def version(c):
    return c.rsplit("_r", 1)[0]


def ranks(x):
    order = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den


def test(careers, x, y, stat, n=100_000, within=False):
    """Two-sided: reshuffle y across careers (within framing if asked); p of a statistic as far from 0 as observed."""
    obs = stat([x[c] for c in careers], [y[c] for c in careers])
    groups = collections.defaultdict(list)
    for i, c in enumerate(careers):
        groups[version(c) if within else ""].append(i)
    ys, hits = [y[c] for c in careers], 0
    for _ in range(n):
        z = ys[:]
        for idx in groups.values():
            vals = [ys[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                z[i] = v
        hits += abs(stat([x[c] for c in careers], z)) >= abs(obs) - 1e-12
    return obs, (hits + 1) / (n + 1)


def diff(a, b):                     # mean of a where b is True minus where b is False
    t = [x for x, f in zip(a, b) if f]
    f = [x for x, g in zip(a, b) if not g]
    return sum(t) / len(t) - sum(f) / len(f)


def spearman(a, b):
    return corr(ranks(a), ranks(b))


both = {k: g1[k] if g1[k] == g2[k] else None for k in graded}
careers = sorted({m["career_file"] for m in key.values()})
outs = {c: outcomes(c) for c in careers}
jan7 = {c: outs[c][0] for c in careers}
total = {c: sum(outs[c]) for c in careers}
later = {c: sum(outs[c][1:]) for c in careers}
agree = sum(g1[k] == g2[k] for k in graded)
lines = ["# What Ministral 3 said before 2011, against what it later traded (exploratory)", "",
         f"{len(graded)} chat replies from the eight chat-only days of 2007-2010 in all 25 B careers, graded blind by two "
         f"graders (same label {agree} of {len(graded)}). Early agreement: the share of a career's replies that agreed "
         "with what another trader proposed (labels both graders gave; NO_ASK left out). Went along: trades, as in B."]
for name, labels in (("both graders", both), ("grader 1 alone", g1), ("grader 2 alone", g2)):
    e = early(labels)
    cs = [c for c in careers if c in e]
    went = [c for c in cs if jan7[c]]
    lines += ["", f"## Labels: {name}", "",
              "| Careers | Early agreement, mean | Went along on 7 Jan | Later requests gone along (of 5 each) |",
              "|---|---|---|---|"]
    order = sorted(cs, key=lambda c: e[c])
    third = len(order) // 3
    for label, grp in (("lowest third of early agreement", order[:third]),
                       ("middle third", order[third:len(order) - third]),
                       ("highest third", order[len(order) - third:])):
        lines.append(f"| {label} ({len(grp)}) | {100 * sum(e[c] for c in grp) / len(grp):.0f}% | "
                     f"{sum(jan7[c] for c in grp)} of {len(grp)} | {sum(later[c] for c in grp)} of {5 * len(grp)} |")
    d, p = test(cs, e, jan7, diff)
    _, pw = test(cs, e, jan7, diff, within=True)
    r, pr = test(cs, e, total, spearman)
    _, prw = test(cs, e, total, spearman, within=True)
    lines += ["",
              f"- Early agreement, careers that went along on 7 Jan ({len(went)}) vs those that did not ({len(cs) - len(went)}): "
              f"{100 * sum(e[c] for c in went) / len(went):.0f}% vs "
              f"{100 * sum(e[c] for c in cs if not jan7[c]) / (len(cs) - len(went)):.0f}%, p = {p:.3f} "
              f"(within framing p = {pw:.3f})",
              f"- Early agreement against requests gone along of six: Spearman r = {r:.2f}, p = {pr:.3f} "
              f"(within framing p = {prw:.3f})"]
lines += ["", "## Every career", "", "| Career | Early replies agreeing (both graders) | 7 Jan | Six requests |",
          "|---|---|---|---|"]
for c in careers:
    ks = [k for k in graded if key[k]["career_file"] == c and both[k] not in ("NO_ASK", None)]
    lines.append(f"| {c[:-5]} | {sum(both[k] == 'AGREES' for k in ks)} of {len(ks)} | {'went along' if jan7[c] else 'no'} | "
                 + "".join("X" if x else "." for x in outs[c]) + f" ({total[c]}) |")
open(os.path.join(OUT, "HISTORY_WORDS.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
