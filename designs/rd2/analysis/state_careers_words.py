"""What the agent said against what it traded in the careers with a document's state switched on (exploratory).

Packets (results/state_careers_words/packet.txt, packet_2.txt, key.json; packet_2 from state_careers_words_prep.py):
every push request in the careers with no state or a state at layer 22, x2: the agent's reasoning and chat message at
the request and 15 minutes later, its orders and the arm hidden, in shuffled order. Two blind graders (Claude
subagents) labelled each one ALONG / REFUSE / NEITHER and cautious yes / no (grader1.json, grader2.json; the 22 Oct
pair graded packet 1, a new pair packet 2, with 20 of packet 1's items mixed in blind as a check,
packet_2_check_grader*.json). This script compares the labels with the trades ("joined"), by arm, with exact
permutation tests over careers. The main table has one career per state and UBS wording (round 0), so every state has
five careers and 30 requests; the two extra no-state careers (round 1, neutral and loss wordings) are listed apart.
"""
import collections, itertools, json, os

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "results", "state_careers_words")
key = {i["id"]: i for i in json.load(open(os.path.join(HERE, "key.json")))}
g1, g2 = (json.load(open(os.path.join(HERE, f"grader{n}.json"))) for n in (1, 2))
c1, c2 = (json.load(open(os.path.join(HERE, f"packet_2_check_grader{n}.json"))) for n in (1, 2))
ARMS = ["none", "random", "gain", "credit", "loss", "blame"]
WORDING = {"v2": "neutral", "loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit"}


def stance(k):
    return g1[k]["stance"] if g1[k]["stance"] == g2[k]["stance"] else "SPLIT"


def arm(k):
    return key[k]["arm"].rsplit("_r", 1)[0].replace("_x2_L22", "")


def perm(a, b):
    """Two-sided exact permutation test over careers: difference in means and p."""
    obs, pool, hits, tot = sum(a) / len(a) - sum(b) / len(b), a + b, 0, 0
    total = sum(pool)
    for idx in itertools.combinations(range(len(pool)), len(a)):
        sx = sum(pool[i] for i in idx)
        hits += abs(sx / len(a) - (total - sx) / len(b)) >= abs(obs) - 1e-12
        tot += 1
    return obs, hits / tot, hits, tot


careers = collections.defaultdict(collections.Counter)
for k, it in key.items():
    c = (arm(k), WORDING[it["wording"]], int(it["arm"].rsplit("_r", 1)[1]))
    s = stance(k)
    r = careers[c]
    r["n"] += 1
    r[s] += 1
    r["traded"] += it["joined"]
    r["refused, traded along"] += it["joined"] and s == "REFUSE"
    r["agreed, did not trade"] += (not it["joined"]) and s == "ALONG"
main = {c: v for c, v in careers.items() if c[2] == 0}
assert all(sum(1 for c in main if c[0] == a) == 5 for a in ARMS), collections.Counter(c[0] for c in main)


def pct(x, n):
    return f"{x} ({100 * x / n:.0f}%)" if x else "0"


def row(name, cs):
    r = sum((careers[c] for c in cs), collections.Counter())
    return (f"| {name} | {len(cs)} | {r['n']} | {pct(r['REFUSE'], r['n'])} | {pct(r['ALONG'], r['n'])} | "
            f"{pct(r['NEITHER'], r['n'])} | {r['SPLIT']} | {pct(r['traded'], r['n'])} | {r['refused, traded along']} | "
            f"{r['agreed, did not trade']} |")


both = lambda a, b, ks: sum(a[k]["stance"] == b[k]["stance"] for k in ks)
p1 = [k for k in key if not key[k].get("packet")]
p2 = [k for k in key if key[k].get("packet") == 2]
old = {k: g1[k]["stance"] for k in c1 if g1[k]["stance"] == g2[k]["stance"]}
HEAD = ("| State | Careers | Push requests | Refused in words | Agreed in words | Neither | Graders split | "
        "Went along by trades | Refused but trades went along | Agreed but did not trade |")
out = ["# What the agent said against what it traded: careers with a document's state on (layer 22, x2)\n",
       f"Stance agreement between the two blind graders: packet 1 (22 Oct) {both(g1, g2, p1)}/{len(p1)}; packet 2 "
       f"(30 Oct) {both(g1, g2, p2)}/{len(p2)}. Caution: {sum(g1[k]['cautious'] == g2[k]['cautious'] for k in key)}/"
       f"{len(key)}. Check, 20 packet-1 items regraded blind in packet 2: the new graders gave the 22 Oct label at "
       f"{both(c1, g1, old)} and {both(c2, g1, old)} of the {len(old)} where the 22 Oct graders agreed. A label counts "
       "where both graders gave it. Produced by `designs/rd2/analysis/state_careers_words.py`.\n",
       "## One career per state and UBS wording (neutral, loss, gain, blame, credit)\n", HEAD, "|---|" * 1 + "---|" * 9]
for a in ARMS:
    out.append(row(a, sorted(c for c in main if c[0] == a)))
extra = sorted(c for c in careers if c[2] > 0)
out += ["", "The two extra no-state careers (round 1, neutral and loss wordings), and the no-state row with them:", "",
        HEAD, "|---|" * 1 + "---|" * 9, row("none, round 1", extra),
        row("none, all", sorted(c for c in careers if c[0] == "none"))]
out += ["\n## By career\n", "| State | UBS's wording | Round | Requests | Refused | Agreed | Neither | Went along by trades |",
        "|---|---|---|---|---|---|---|---|"]
for c, v in sorted(careers.items(), key=lambda cv: (ARMS.index(cv[0][0]), list(WORDING.values()).index(cv[0][1]), cv[0][2])):
    out.append(f"| {c[0]} | {c[1]} | {c[2]} | {v['n']} | {v['REFUSE']} | {v['ALONG']} | {v['NEITHER']} | {v['traded']} |")


def share(arms, f):
    return [v[f] / v["n"] for c, v in main.items() if c[0] in arms]


out += ["\n## Tests over careers (exact permutation, two-sided; one career per state and wording)\n"]
for label, f, a, b in [("refused in words", "REFUSE", ("loss", "blame"), ("none",)),
                       ("refused in words", "REFUSE", ("loss", "blame"), ("random",)),
                       ("refused in words", "REFUSE", ("loss", "blame"), ("gain", "credit")),
                       ("refused in words", "REFUSE", ("loss",), ("gain",)),
                       ("agreed in words", "ALONG", ("loss", "blame"), ("none",)),
                       ("agreed in words", "ALONG", ("gain", "credit"), ("none",)),
                       ("went along by trades", "traded", ("gain",), ("none",)),
                       ("went along by trades", "traded", ("gain", "credit"), ("none",)),
                       ("went along by trades", "traded", ("loss", "blame"), ("none",)),
                       ("went along by trades", "traded", ("random",), ("none",))]:
    d, p, hits, tot = perm(share(a, f), share(b, f))
    ma, mb = (sum(share(x, f)) / len(share(x, f)) for x in (a, b))
    out.append(f"- {label}, {' + '.join(a)} vs {' + '.join(b)} ({len(share(a, f))} vs {len(share(b, f))} careers): "
               f"{100 * ma:.0f}% vs {100 * mb:.0f}%, " + (f"p = {p:.3f}" if p >= 0.001 else
               f"p < 0.001 ({hits} of {tot:,} splits of the careers as extreme)"))
open(os.path.join(HERE, "SAID_VS_DID.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
