"""Agreement in words, every experiment (words_prep_all.py, then blind labels): results/words_all/WORDS_ALL.md.

    python designs/rd2/analysis/words_all.py

The unit is the agent's whole response to a UBS message (its first reply and anything later the same day before UBS
spoke again). B combines its single-reply labels (results/words_b) with the responses graded again here. "Agreed" is
the share of responses that went along in words, among those where UBS asked or proposed something; a response with no
chat message counts in the denominator as not agreeing. Each experiment is compared with its own control, reshuffling
whole careers (10,000 times) on each career's share agreed.
"""
import collections, glob, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ALL, B = os.path.join(ROOT, "results/words_all"), os.path.join(ROOT, "results/words_b")
NAME = {"neutral": "Neutral", "loss": "Loss", "gain": "Gain", "loss + you": "Blame", "gain + you": "Credit",
        "no ask": "No ask", "clean": "Clean", "first line": "First line", "up to 7 Jan": "Up to 7 Jan",
        "whole career": "Whole career"}
EXPS = [("A", "the memo and morning book; UBS's lines neutral", "neutral"),
        ("A real lines", "as A, UBS's real lines (stopped early)", "neutral"),
        ("B", "UBS's framing", "neutral"),
        ("C", "the takeover ladder", "clean"),
        ("D", "memo and UBS share the framing (no neutral arm: B's neutral careers are the base)", ("B", "neutral")),
        ("E", "B plus Bank C", "neutral"),
        ("F", "memo, UBS and Bank C share the framing", "neutral"),
        ("One push", "only UBS's 7 January request framed (notebook 34; B's neutral careers are the base)", ("B", "neutral"))]
rng = random.Random(20261029)


def labels(folder, kind):
    out = {}
    for p in sorted(glob.glob(os.path.join(folder, f"labels_{kind}_*.json"))):
        out.update({k: v.strip().upper() for k, v in json.load(open(p)).items()})
    return out


key, lab = json.load(open(os.path.join(ALL, "key.json"))), labels(ALL, "batch")
need = {k for k, m in key.items() if m["has_chat"]}
assert set(lab) == need, f"{len(lab)} labels for {len(need)} responses with a chat message"
rows = []
for k, m in key.items():
    if m["experiment"] != "B":
        rows.append({**m, "label": lab.get(k) if m["has_chat"] else None})
regraded = {m["b_item"]: lab[k] for k, m in key.items() if m["experiment"] == "B" and m["b_item"] and m["has_chat"]}
bkey, blab = json.load(open(os.path.join(B, "key.json"))), labels(B, "batch")
for k, m in bkey.items():
    label = regraded.get(k, blab.get(k) if m["has_chat"] else None)
    rows.append({**m, "experiment": "B", "has_chat": label is not None, "label": label})


def asked(rs):
    return [r for r in rs if r["label"] != "NO_ASK"]


def share(rs, label="AGREES"):
    rs = asked(rs)
    return sum(r["label"] == label for r in rs) / len(rs) if rs else float("nan")


def per_career(rs):
    by = collections.defaultdict(list)
    for r in asked(rs):
        by[r["career_file"]].append(r["label"] == "AGREES")
    return [sum(v) / len(v) for v in by.values()]


def perm(a, b, n=10_000):
    if not a or not b:
        return float("nan")
    obs, pool, hits = sum(a) / len(a) - sum(b) / len(b), a + b, 0
    for _ in range(n):
        rng.shuffle(pool)
        x, y = pool[:len(a)], pool[len(a):]
        hits += abs(sum(x) / len(x) - sum(y) / len(y)) >= abs(obs) - 1e-12
    return (hits + 1) / (n + 1)


def fmt_p(p):
    return "" if p != p else ("<0.001" if p < 0.001 else f"{p:.3f}")


out = ["# Agreement in words, every experiment (exploratory)", "",
       "Each response the agent sent UBS, labelled blind from its chat messages alone (UBS's and Bank C's lines shown in "
       "the neutral wording). \"Agreed\": the share of responses that went along in words, where UBS asked or proposed "
       "something (no message counts as not agreeing). Levels, not changes; each experiment's control first. "
       "\"Traded along\" is the paper's measure (the simulator's \"joined\") at the six push requests."]
for exp, what, ctrl in EXPS:
    rs = [r for r in rows if r["experiment"] == exp]
    if not rs:
        continue
    base = [r for r in rows if r["experiment"] == ctrl[0] and r["version"] == ctrl[1]] if isinstance(ctrl, tuple) else \
        [r for r in rs if r["version"] == ctrl]
    base_name = f"{ctrl[0]} {NAME[ctrl[1]].lower()} (base)" if isinstance(ctrl, tuple) else f"{NAME[ctrl]} (control)"
    versions = [v for v in NAME if any(r["version"] == v for r in rs) and (isinstance(ctrl, tuple) or v != ctrl)]
    out += ["", f"## {exp}: {what}", "",
            "| Version | Careers | Agreed, chat-only days | p | Agreed, trading days | p | At the push requests: agreed in words | Traded along |",
            "|---|---|---|---|---|---|---|---|"]
    for name, group in [(base_name, base)] + [(NAME[v], [r for r in rs if r["version"] == v]) for v in versions]:
        cells = [name, str(len({r["career_file"] for r in group}))]
        for day in ("chat-only", "trading"):
            g = [r for r in group if r["day"] == day]
            cells.append(f"{100 * share(g):.0f}%" if asked(g) else "-")
            cells.append("" if group is base else fmt_p(perm(per_career(g), per_career([r for r in base if r["day"] == day]))))
        push = [r for r in group if r["push_request"]]
        cells.append(f"{100 * sum(r['label'] == 'AGREES' for r in push) / len(push):.0f}%" if push else "-")
        cells.append(f"{100 * sum(bool(r['traded_along']) for r in push) / len(push):.0f}%" if push else "-")
        out.append("| " + " | ".join(cells) + " |")
chk = labels(ALL, "recheck")
both = [k for k in chk if k in lab]
if both:
    same = sum(lab[k] == chk[k] for k in both)
    cats = ["AGREES", "REFUSES", "NONCOMMITTAL", "NO_ASK"]
    pe = sum((sum(lab[k] == c for k in both) / len(both)) * (sum(chk[k] == c for k in both) / len(both)) for c in cats)
    po = same / len(both)
    out += ["", f"## The re-check: {len(both)} responses graded twice, independently", "",
            f"Same label {same} of {len(both)} ({100 * po:.0f}%); Cohen's kappa {(po - pe) / (1 - pe):.2f}. AGREES or "
            f"not: {sum((lab[k] == 'AGREES') == (chk[k] == 'AGREES') for k in both)} of {len(both)} the same."]
open(os.path.join(ALL, "WORDS_ALL.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
