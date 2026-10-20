"""Before tracing "you" (the user, 20 Oct): in every "+ you" line, does "you" come after the stakes? A model reads left
to right, so "you" can only take in stakes that come before it in the same line (stakes in earlier lines are still in
view). Prints codes and positions only, not the lines (the lines are the user's).

    python designs/rd2/analysis/check_you_placement.py
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from framing_set import read_set
from peer_lines import read_peers

YOU = re.compile(r"\b(you|your|you're|you'll|yours|u|ur)\b", re.I)
STAKES = re.compile(r"\b(los\w*|underwater|hit|gain\w*|ahead|profit\w*|money|make|made|red|black|ground|burn\w*|bleed\w*|"
                    r"cost\w*|pay\w*|paid|wrong|right side|fail\w*|works?|waste|fizzle\w*|less|more|most|double\w*|"
                    r"amplif\w*|dilut\w*|concentrat\w*|benefit\w*|wrong-footed|nothing to show|something real|"
                    r"settle for less|walk away|empty|down on it|up on it|stuck|sitting on)\b", re.I)


def check(text):
    y = [m.start() for m in YOU.finditer(text)]
    s = [m.start() for m in STAKES.finditer(text)]
    if not y:
        return "no 'you'"
    if not s:
        return "no stakes word found"
    return "you after stakes" if max(y) > min(s) else "you BEFORE all stakes"


rows = []
for c in read_set():
    for l in c["lines"]:
        for f in ("loss + you", "gain + you"):
            rows.append((f"B {c['date']} line {l['n']} {f}", check(l["text"][f])))
for pid, fr in read_peers().items():
    for f in ("loss + you", "gain + you"):
        rows.append((f"F Bank C {pid} {f}", check(fr[f]["peer"])))
from collections import Counter
print(Counter(r[1] for r in rows))
for k, v in rows:
    if v != "you after stakes":
        print(f"  {k}: {v}")
