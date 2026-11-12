"""Cohen's kappa for every double-graded set of the agent's words. Usage: python kappa.py <repo> <out json>"""
import glob, json, os, sys, collections
R = os.path.join(sys.argv[1], "results")
def load(pattern):
    out = {}
    for p in sorted(glob.glob(os.path.join(R, pattern))):
        j = json.load(open(p))
        if isinstance(j, list):
            j = {x.get("id") or x.get("code"): x.get("label") for x in j}
        out.update({k: (v.get("label") if isinstance(v, dict) else v) for k, v in j.items()})
    return out
def kappa(a, b):
    n = len(a); cats = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[c] * cb[c] for c in cats) / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")
def report(name, pairs):
    a = [x for x, _ in pairs]; b = [y for _, y in pairs]
    po, k = kappa(a, b)
    ab = ["AGREE" if "AGREE" in str(x).upper() else "OTHER" for x in a]
    bb = ["AGREE" if "AGREE" in str(y).upper() else "OTHER" for y in b]
    po2, k2 = kappa(ab, bb)
    tab = collections.Counter(zip(a, b))
    print(f"\n== {name}: n = {len(a)}; same label {po:.1%}, kappa {k:.2f}; agreement vs not: same {po2:.1%}, kappa {k2:.2f}")
    print("   ", dict(tab.most_common(12)))
    return {"n": len(a), "same": po, "kappa": k, "same_binary": po2, "kappa_binary": k2,
            "table": {f"{x} | {y}": c for (x, y), c in tab.items()}}
res = {}
# words_b: first grading vs recheck (same codes?)
b1, b2 = load("words_b/labels_batch_*.json"), load("words_b/labels_recheck_*.json")
common = sorted(set(b1) & set(b2))
print("words_b recheck ids", len(b2), "overlap with first", len(common))
if common:
    res["words_b first vs recheck"] = report("words_b: first grader vs recheck", [(b1[k], b2[k]) for k in common])
# words_all items that repeat a words_b item (b_item)
ka = json.load(open(os.path.join(R, "words_all/key.json")))
a1 = load("words_all/labels_batch_*.json")
pairs = [(b1[v["b_item"]], a1[k]) for k, v in ka.items() if v.get("b_item") and k in a1 and v["b_item"] in b1]
if pairs:
    res["words_b vs words_all (same B replies)"] = report("words_b grader vs words_all grader, same B replies", pairs)
# state careers: grader1 vs grader2
g1, g2 = load("state_careers_words/grader1.json"), load("state_careers_words/grader2.json")
c = sorted(set(g1) & set(g2))
if c:
    res["state careers g1 vs g2"] = report("state-career injections: grader 1 vs grader 2", [(g1[k], g2[k]) for k in c])
h1, h2 = load("history_words_ministral/labels_g1.json"), load("history_words_ministral/labels_g2.json")
c = sorted(set(h1) & set(h2))
if c:
    res["ministral history g1 vs g2"] = report("Ministral history: grader 1 vs grader 2", [(h1[k], h2[k]) for k in c])
json.dump(res, open(sys.argv[2], "w"), indent=1)
