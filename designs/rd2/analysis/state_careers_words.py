"""What the agent said against what it traded in the careers with a document's state switched on (22 Oct; exploratory).

Packets (results/state_careers_words/packet.txt, key.json): every push request in the careers with no state or a state
at layer 22, x2: the agent's reasoning and chat message at the request and 15 minutes later, its orders and the arm
hidden, in shuffled order. Two blind graders (Claude subagents) labelled each one ALONG / REFUSE / NEITHER and
cautious yes / no (grader1.json, grader2.json). This script compares the labels with the trades ("joined"), by arm,
with exact permutation tests over careers.
"""
import collections, itertools, json, os

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "results", "state_careers_words")
key = {i["id"]: i for i in json.load(open(os.path.join(HERE, "key.json")))}
g1, g2 = (json.load(open(os.path.join(HERE, f"grader{n}.json"))) for n in (1, 2))


def stance(k):
    return g1[k]["stance"] if g1[k]["stance"] == g2[k]["stance"] else "SPLIT"


def arm(k):
    return key[k]["arm"].rsplit("_r", 1)[0].replace("_x2_L22", "")


def perm(a, b):
    """Two-sided exact permutation test over careers: difference in means and p."""
    obs, pool, hits, tot = sum(a) / len(a) - sum(b) / len(b), a + b, 0, 0
    for idx in itertools.combinations(range(len(pool)), len(a)):
        x = [pool[i] for i in idx]
        y = [pool[i] for i in range(len(pool)) if i not in idx]
        hits += abs(sum(x) / len(x) - sum(y) / len(y)) >= abs(obs) - 1e-12
        tot += 1
    return obs, hits / tot


careers = collections.defaultdict(collections.Counter)
rows = collections.defaultdict(collections.Counter)
for k, it in key.items():
    c = (arm(k), it["wording"].replace("v2", "neutral"), it["arm"].rsplit("_r", 1)[1])
    s = stance(k)
    for r in (careers[c], rows[arm(k)]):
        r["n"] += 1
        r[s] += 1
        r["traded"] += it["joined"]
        r["refused, traded along"] += it["joined"] and s == "REFUSE"
        r["agreed, did not trade"] += (not it["joined"]) and s == "ALONG"

out = ["# What the agent said against what it traded: careers with a document's state on (layer 22, x2)\n",
       f"Stance agreement between the two blind graders: {sum(g1[k]['stance'] == g2[k]['stance'] for k in key)}/{len(key)}; "
       f"caution: {sum(g1[k]['cautious'] == g2[k]['cautious'] for k in key)}/{len(key)}. Produced by "
       "`designs/rd2/analysis/state_careers_words.py`.\n",
       "| State | Careers | Push requests | Refused in words | Agreed in words | Neither | Graders split | Went along by trades | Refused but trades went along | Agreed but did not trade |",
       "|---|---|---|---|---|---|---|---|---|---|"]
for a in ["none", "random", "gain", "credit", "loss", "blame"]:
    r = rows[a]
    out.append(f"| {a} | {sum(1 for c in careers if c[0] == a)} | {r['n']} | {r['REFUSE']} | {r['ALONG']} | {r['NEITHER']} | "
               f"{r['SPLIT']} | {r['traded']} | {r['refused, traded along']} | {r['agreed, did not trade']} |")
out += ["\n## By career\n", "| State | UBS's wording | Requests | Refused | Agreed | Went along by trades |", "|---|---|---|---|---|---|"]
for c, v in sorted(careers.items()):
    out.append(f"| {c[0]} | {c[1]} | {v['n']} | {v['REFUSE']} | {v['ALONG']} | {v['traded']} |")


def share(arms, f):
    return [v[f] / v["n"] for c, v in careers.items() if c[0] in arms]


out += ["\n## Tests over careers (exact permutation, two-sided)\n"]
for label, f, a, b in [("refused in words", "REFUSE", ("loss", "blame"), ("none",)),
                       ("refused in words", "REFUSE", ("loss", "blame"), ("gain", "credit")),
                       ("refused in words", "REFUSE", ("loss",), ("gain",)),
                       ("went along by trades", "traded", ("gain",), ("none",)),
                       ("went along by trades", "traded", ("loss", "blame"), ("none",))]:
    d, p = perm(share(a, f), share(b, f))
    out.append(f"- {label}, {' + '.join(a)} vs {' + '.join(b)} ({len(share(a, f))} vs {len(share(b, f))} careers): "
               f"{100 * d:+.0f} points, p = {p:.3f}")
open(os.path.join(HERE, "SAID_VS_DID.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
