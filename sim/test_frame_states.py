"""No GPU or model needed, from the repo root: python sim/test_frame_states.py

Checks for the framed messages' states in the direct request (sim/frame_states.py, scripts/modal_frame_states.py):
1. common_suffix on made-up sequences (an insertion at the end, in the middle, and a tail that matches by chance);
2. on B's 20 neutral-career moments (7 and 12 January), with a Gemma-like template (one character per token): each
   framing's request shares the history before the update with the neutral one, differs from it, and has tokens after
   the framed words that line up with the neutral request's;
3. pooled() and conditions() on made-up states: 15 conditions, each vector the size it should be;
4. fisher() against values worked out by hand;
5. the direct request's moment in the saved lesson career (5 August 10:00), as scripts/modal_frame_states.py finds it.
Prints counts and checks, not the lines.
"""
import ast, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import frame_states as F
from career import career_opening
from framing_set import read_set
from inside_careers import encode, moments, turns_at
from interventions import SIGN, split_point
from matched import matched
import prime as P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. common_suffix
check("an insertion at the end keeps the shared tail", F.common_suffix([1, 2, 3, 9, 9, 7, 8], [1, 2, 3, 7, 8]) == 2)
check("an insertion in the middle keeps the shared tail", F.common_suffix([1, 2, 5, 6, 3, 4], [1, 2, 3, 4]) == 2)
check("a tail that matches by chance does not reach back before the first difference",
      F.common_suffix([5, 3, 9, 5, 3], [5, 3]) == 0)


# ---- 2. the prompts at B's 20 moments
class Tok:
    def apply_chat_template(self, turns, add_generation_prompt=False, return_dict=False, tokenize=True):
        sys_ = turns[0]["content"] if turns and turns[0]["role"] == "system" else None
        rest = turns[1:] if sys_ is not None else turns
        text = "^"
        for i, t in enumerate(rest):
            c = (sys_ + "\n\n" + t["content"]) if i == 0 and sys_ else t["content"]
            text += f"<{'model' if t['role'] == 'assistant' else 'user'}>\n{c}<end>\n"
        text += "<model>\n" if add_generation_prompt else ""
        return {"input_ids": [ord(ch) % 97 for ch in text]}


B = os.path.join(ROOT, "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
items = [m for m in P.work_items(B, moments, SIGN) if m["date"] in ("2011-01-07", "2011-01-12")]
check(f"20 moments ({len(items)})", len(items) == 20)
tok, opening, chats = Tok(), career_opening(), read_set()
bad, after, extra = [], [], []
for m in items:
    c = json.load(open(f"{B}/careers/{m['career_file']}"))
    idx = m["history_index"]
    base = matched(c, idx, m["date"], "neutral", "neutral", chats)
    plain = encode(tok, turns_at(base, idx, opening))
    _, k = split_point(tok, base, idx, opening)
    for f in F.FRAMES:
        seq = encode(tok, turns_at(matched(c, idx, m["date"], "neutral", f, chats), idx, opening))
        s = F.common_suffix(seq, plain)
        d = next(i for i, (x, y) in enumerate(zip(seq, plain)) if x != y)
        fine = seq[:k] == plain[:k] and seq != plain and s >= 1 and d >= k and len(plain) - s >= d \
            and seq[len(seq) - s:] == plain[len(plain) - s:]
        if not fine:
            bad.append((m["career_file"], m["date"], f))
        after.append(s)
        extra.append(len(seq) - len(plain))
check(f"every framing at every moment: same history, a different request, a shared tail after the framed words "
      f"({len(items) * len(F.FRAMES) - len(bad)}/{len(items) * len(F.FRAMES)})", not bad)
print(f"     tail after the framed words: {min(after)}-{max(after)} characters; framed words add {min(extra)}-{max(extra)}")

# ---- 3. pooled and conditions on made-up states
rng = np.random.default_rng(0)
W, layers = 16, [12, 22, 24]
shifts = rng.normal(size=(20, len(F.FRAMES), len(F.KINDS), len(layers), W))
fs = F.pooled(shifts, F.FRAMES, F.KINDS, layers)
check("pooled: one vector per framing, kind and layer, the mean over the moments",
      len(fs) == 4 * 2 * 3 and np.allclose(fs[("gain", "whole", 22)], shifts[:, 1, 1, 1].mean(0)))
docs = {f"{t} x2 L22": {"vec": rng.normal(size=W) * (i + 3)} for i, t in enumerate(["loss", "gain", "blame", "credit", "random"])}
conds = F.conditions(fs, docs, 22, 2.0)
names = [n for n, _, _ in conds]
check(f"15 conditions, none first ({len(conds)})", len(conds) == 15 and names[0] == "none" and conds[0][1] is None)
size = lambda n: float(np.linalg.norm(dict((a, b) for a, b, _ in conds)[n]))
check("the framed 'after' state at twice its own size",
      math.isclose(size("frame loss + you, after, x2 own size"), 2 * np.linalg.norm(fs[("loss + you", "after", 22)]), rel_tol=1e-5))
check("the framed states at the twin document state's size (loss + you with blame, gain + you with credit)",
      math.isclose(size("frame loss + you, after, blame document size"), np.linalg.norm(docs["blame x2 L22"]["vec"]), rel_tol=1e-5)
      and math.isclose(size("frame gain + you, whole, credit document size"), np.linalg.norm(docs["credit x2 L22"]["vec"]), rel_tol=1e-5))
check("the references are the earlier run's vectors", np.array_equal(dict((a, b) for a, b, _ in conds)["random x2 L22"],
                                                                     docs["random x2 L22"]["vec"]))
check("cosine of a vector with itself is 1, with its opposite -1",
      math.isclose(F.cosine(fs[("loss", "after", 22)], fs[("loss", "after", 22)]), 1) and
      math.isclose(F.cosine(fs[("loss", "after", 22)], -fs[("loss", "after", 22)]), -1))

# ---- 4. Fisher's exact test
check(f"9/10 vs 1/10: p = {F.fisher(9, 10, 1, 10):.5f} (0.00109)", math.isclose(F.fisher(9, 10, 1, 10), 0.0010944, rel_tol=1e-3))
check(f"10/10 vs 0/10: p = {F.fisher(10, 10, 0, 10):.6f} (0.0000108)", math.isclose(F.fisher(10, 10, 0, 10), 1.0825e-5, rel_tol=1e-3))
check("equal counts: p = 1", F.fisher(3, 10, 3, 10) == 1.0)

# ---- 5. the direct request's moment
src = open(os.path.join(ROOT, "scripts/modal_frame_states.py")).read()
ast.parse(src)
g = {}
for line in src.splitlines():
    if re.match(r"^(LESSON|BASE|AT) = ", line):
        exec(line, g)
career = json.load(open(os.path.join(ROOT, g["LESSON"], "careers", g["BASE"] + ".json")))
h = career["history"]
k = [i for i, t in enumerate(h) if t["role"] == "user" and t["content"].startswith(g["AT"])]
px = re.search(r"Silver \(XAG/USD\): ([0-9]+\.[0-9]+)", h[k[0]]["content"]) if k else None
pos = re.search(r"Your position: ([+-]?[0-9,]+) oz", h[k[0]]["content"]) if k else None
check(f"the script parses; one 5 August 10:00 update in the saved lesson career, with a price and a position "
      f"({px.group(1) if px else None}, {pos.group(1) if pos else None})", len(k) == 1 and px and pos)
print("all checks pass" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
