"""Needs torch and transformers (CPU is enough), from the repo root: python sim/test_push_carry.py

Checks for push and cue (sim/push_carry.py, scripts/modal_push_carry.py, designs/rd2/analysis/push_carry.py), with no
download:
1. on B's 50 saved careers at 12 January: "7 Jan neutral" changes exactly UBS's 7 January request, "UBS neutral" exactly
   UBS's seven earlier lines (2007, 2010, 7 January), each into the line B's neutral careers saw on that date; the
   12 January request becomes the neutral careers' line; nothing else changes (the agent's turns, the rest of every
   turn); a neutral career is unchanged in every version;
2. the prompts: within a history version, both request versions share the history before the request; the versions
   differ from where UBS's first changed line is;
3. score_moment on a tiny random Gemma 3 and a shortened saved career: six rows for a framed career, one for a neutral
   one, probabilities that sum to one;
4. cue_row on files in the matched rereads' format;
5. the analysis on made-up rows with known answers.
Prints counts and checks, not the lines.
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import torch
from transformers import Gemma3ForCausalLM, Gemma3TextConfig
import push_carry as PC
from career import career_opening
from framing_set import read_set
from inside_careers import moments
from interventions import split_point

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER = os.path.join(ROOT, "results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2")
ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


chats = read_set()
M = {m["career_file"]: m for m in moments(FOLDER, "B") if m["chat"] == PC.CUE_CHAT}
load = lambda f: json.load(open(f"{FOLDER}/careers/{f}"))
ubs_by_date = lambda h, upto: {PC.turn_date(t["content"]): PC.UBS_LINE.findall(t["content"])
                               for t in h[:upto] if t["role"] == "user" and PC.UBS_LINE.search(t["content"])}
strip = lambda text: PC.UBS_LINE.sub("", text)

# ---- 1. every career's versions
check(f"50 careers at 12 January ({len(M)})", len(M) == 50)
bad = []
for f, m in sorted(M.items()):
    c, idx = load(f), m["history_index"]
    ref = load(f"neutral_r{c['run']}.json")
    want = ubs_by_date(ref["history"], M[f"neutral_r{c['run']}.json"]["history_index"])
    req_ref = PC.UBS_LINE.findall(ref["history"][M[f"neutral_r{c['run']}.json"]["history_index"]]["content"])
    V = PC.reread_versions(c, idx, chats)
    for (cond, req), (cc, changed) in V.items():
        h0, h1 = c["history"], cc["history"]
        same_rest = len(h0) == len(h1) and all(
            a["role"] == b["role"] and (a == b if a["role"] != "user" else strip(a["content"]) == strip(b["content"]))
            for a, b in zip(h0, h1))
        got = ubs_by_date(h1, idx)
        if c["version"] == "neutral":
            good = h1 == h0 if req == "as saved" else same_rest
        elif cond == "as saved":
            good = same_rest and [x[:2] for x in changed] == [] and got == ubs_by_date(h0, idx)
        elif cond == "7 Jan neutral":
            good = (same_rest and [(d, n) for _, d, n in changed] == [("2011-01-07", 1)] and got["2011-01-07"] == want["2011-01-07"]
                    and all(got[d] == v for d, v in ubs_by_date(h0, idx).items() if d != "2011-01-07"))
        else:
            good = (same_rest and [(d, n) for _, d, n in changed] == [("2007-11-28", 2), ("2010-10-15", 4), ("2011-01-07", 1)]
                    and got == want)
        if req == "neutral":
            good = good and PC.UBS_LINE.findall(h1[idx]["content"]) == req_ref
        else:
            good = good and h1[idx] == h0[idx]
        if not good:
            bad.append((f, cond, req))
check(f"every version of every career: only UBS's lines change, into the neutral careers' lines ({len(bad)} bad)",
      not bad)


# ---- 2. the prompts (a Gemma-like template, one character per token)
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

    def __call__(self, text, **k):
        return {"input_ids": [ord(ch) % 97 for ch in text]}

    def get_vocab(self):
        return {chr(c): c % 97 for c in range(32, 127)}


tok, opening = Tok(), career_opening()
f = "loss_plus_you_r0.json"
c, m = load(f), M[f]
V = PC.reread_versions(c, m["history_index"], chats)
enc = {k: split_point(tok, v[0], m["history_index"], opening) for k, v in V.items()}
first_diff = lambda a, b: next(i for i, (x, y) in enumerate(zip(a, b)) if x != y)
check("within each history version, both requests share the history before the request",
      all(enc[(cond, "as saved")][0][:enc[(cond, "as saved")][1]] == enc[(cond, "neutral")][0][:enc[(cond, "neutral")][1]]
          and enc[(cond, "as saved")][1] == enc[(cond, "neutral")][1] for cond in PC.CONDITIONS))
base = enc[("as saved", "as saved")][0]
d7, dall = first_diff(base, enc[("7 Jan neutral", "as saved")][0]), first_diff(base, enc[("UBS neutral", "as saved")][0])
check(f"the versions part where UBS's first changed line is (7 January at token {d7:,}, 2007 at token {dall:,}, the "
      f"request at {enc[('as saved', 'as saved')][1]:,})", dall < d7 < enc[("as saved", "as saved")][1])

# ---- 3. score_moment on a tiny model, with the saved career shortened to its UBS turns and the request
torch.manual_seed(0)
model = Gemma3ForCausalLM(Gemma3TextConfig(vocab_size=97, hidden_size=64, intermediate_size=128, num_hidden_layers=6,
                                           num_attention_heads=2, num_key_value_heads=1, head_dim=32, sliding_window=16,
                                           max_position_embeddings=16384)).eval()


def shortened(career, idx):
    """The UBS turns before the request (each with the agent's reply), and the request, each update cut to its header
    and its chat lines."""
    h, keep = career["history"], []
    for i in range(idx):
        if h[i]["role"] == "user" and PC.UBS_LINE.search(h[i]["content"]):
            keep += [i, i + 1]
    cut = lambda t: t if not t.startswith("Time:") else "\n".join(
        [t.split("\n")[0]] + [l for l in t.split("\n") if PC.UBS_LINE.match(l) or l.startswith("New chat")])
    hh = [{**h[i], "content": cut(h[i]["content"]) if h[i]["role"] == "user" else h[i]["content"][:200]} for i in keep]
    hh.append({**h[idx], "content": cut(h[idx]["content"])})
    return {**career, "history": hh}, len(hh) - 1


short_opening = opening[:400]
for f, n_rows in [("loss_plus_you_r0.json", 6), ("neutral_r0.json", 1)]:
    c, m = load(f), dict(M[f])
    sc, m["history_index"] = shortened(c, m["history_index"])
    rows = PC.score_moment(model, tok, sc, m, chats, short_opening)
    check(f"{f}: {len(rows)} rows ({sorted({(r['condition'], r['request']) for r in rows})[:2]}...), probabilities sum to "
          f"one, coverage in (0, 1]", len(rows) == n_rows and all(abs(sum(r["probs"]) - 1) < 1e-6 and 0 < r["coverage"] <= 1
                                                                   and 0 <= r["p_order_along"] <= 1 for r in rows))
    if n_rows == 6:
        check("the swapped turns are recorded per version",
              [len(r["swapped"]) for r in rows] == [0, 0, 1, 1, 3, 3])

# ---- 4. cue_row on files in the matched rereads' format (10 versions: five framings, with and without Bank C)
tmp0 = tempfile.mkdtemp()
FR = ["neutral", "loss", "gain", "loss + you", "gain + you"]
files = {}
for chat, base in [(PC.CUE_CHAT, 0.0), (PC.PUSH_CHAT, 1.0)]:
    meta = [{"framing": v, "bank_c": b, "history": "loss + you", "run": 0, "p_order_along": 0.1 * i + 0.01 * b,
             "coverage": 0.8} for i, v in enumerate(FR) for b in (False, True)]
    st = np.zeros((10, 2, 4), np.float32)
    st[6] = [[1, 0, 0, 0], [0, 1, 0, 0]] if chat == PC.CUE_CHAT else [[1, 0, 0, 0], [0, 0, 1, 0]]   # blame, no Bank C
    np.savez_compressed(f"{tmp0}/{chat}.npz", states=st, layers=np.array([12, 24]), meta=np.array(json.dumps(meta)))
    files[chat] = np.load(f"{tmp0}/{chat}.npz")
cr = PC.cue_row(files[PC.CUE_CHAT], files[PC.PUSH_CHAT], "x.json")
check(f"cue_row: P by framing without Bank C, cosines {cr['cosine_12_vs_7']} (made up: 1 at layer 12, 0 at 24)",
      cr["p"] == {v: 0.1 * i for i, v in enumerate(FR)} and np.allclose(cr["cosine_12_vs_7"], [1, 0])
      and cr["layers"] == [12, 24] and cr["coverage"] == 0.8)

# ---- 5. the analysis on made-up rows: as saved 60%, 7 Jan neutral 40%, every UBS line neutral 25%, neutral careers 10%;
# the cue adds 20 points in blame careers and 5 in neutral ones
tmp = tempfile.mkdtemp()
rows, cue = [], []
for v in ["neutral", "loss + you", "loss", "gain + you", "gain"]:
    for run in range(10):
        cf = f"{v.replace(' + ', '_plus_')}_r{run}.json"
        conds = [("as saved", "neutral", 0.10)] if v == "neutral" else \
            [(cond, req, p) for cond, p in [("as saved", 0.60), ("7 Jan neutral", 0.40), ("UBS neutral", 0.25)]
             for req in ["as saved", "neutral"]]
        rows += [{"career_file": cf, "history": v, "run": run, "condition": cond, "request": req,
                  "p_order_along": p + 0.01 * (run % 3), "coverage": 0.9} for cond, req, p in conds]
        lift = {"loss + you": 0.20, "neutral": 0.05}.get(v, 0.10)
        cue.append({"career_file": cf, "history": v, "run": run, "coverage": 0.9, "layers": [12, 24],
                    "p": {"neutral": 0.3, "loss + you": 0.3 + lift + 0.001 * run},
                    "cosine_12_vs_7": [0.5 if v == "loss + you" else 0.2, 0.4], "size_12": [1, 1], "size_7": [1, 1]})
json.dump(rows, open(f"{tmp}/carry_rows.json", "w"))
json.dump(cue, open(f"{tmp}/cue_rows.json", "w"))
r = subprocess.run([sys.executable, f"{ROOT}/designs/rd2/analysis/push_carry.py", tmp], capture_output=True, text=True)
md = open(f"{tmp}/PUSH_CARRY.md").read() if r.returncode == 0 else r.stderr
s = json.load(open(f"{tmp}/push_carry.json")) if r.returncode == 0 else {}
c = s.get("carry_blame", {})
check(f"the analysis finds the made-up carry (whole {100 * c.get('whole', 0):+.1f}, 7 January words "
      f"{100 * c.get('words_7jan', 0):+.1f}, all UBS words {100 * c.get('words_all', 0):+.1f}, left "
      f"{100 * c.get('rest', 0):+.1f} points)",
      r.returncode == 0 and abs(c["whole"] - 0.50) < 0.02 and abs(c["words_7jan"] - 0.20) < 1e-9
      and abs(c["words_all"] - 0.35) < 1e-9 and abs(c["rest"] - 0.15) < 0.02 and "Share of the whole history" in md)
check(f"the analysis finds the made-up cue (blame minus neutral careers {100 * s.get('cue_blame_minus_neutral', 0):+.1f} "
      "points) and the inside table", r.returncode == 0 and abs(s["cue_blame_minus_neutral"] - 0.15) < 1e-6
      and "| 12 | +0.500 | +0.200 | +0.300 |" in md)
print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
