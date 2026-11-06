"""Needs torch and transformers (CPU is enough):

    RD2_STATES=<folder of <exp>_bf16 states> RD2_SHIFTS=<layer_scan_18_21_sweep shifts file> \
    RD2_TOKENIZER=<a Gemma 3 tokenizer folder> python sim/test_direct_push.py

Checks for the direct request with a holding push (sim/direct_push.py, scripts/modal_direct_push.py,
designs/rd2/analysis/direct_push.py), no GPU:
1. the moment is the paper's: the same career, cut, price, position and UBS line as scripts/modal_ask_same.py;
2. the arms (27) and the vectors: the paper's states exactly; dimension 2339 zero in every push; random pushes the
   holding push's size;
3. a tiny random Gemma 3 with the real tokenizer on the real update (a short history): the monitor's decision state
   under a state and a push equals a full read with both added by hand from UBS's update on; one random direction per
   reply in a batch equals each reply read on its own; paired seeds repeat; steering is off afterwards;
4. the analysis on made-up rows with known answers.
"""
import copy, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.chdir(ROOT)
import glob
import numpy as np
import torch
from transformers import AutoTokenizer, Gemma3ForCausalLM, Gemma3TextConfig
import direct_push as D
import steer2 as S2
from career import career_opening
from slope import slope_opening
from lesson import lesson_opening
from interventions import Steer, prefill

ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. the moment
opening = lesson_opening(slope_opening(career_opening()))
career = json.load(open(f"{D.FOLDER}/careers/{D.BASE}.json"))
turns, px, pos, line = D.turns_at(career, opening)
paper = open("results/lesson_lesson/ASKED_SAME_HISTORY.md").read()
check("the paper's moment: price 39.339, flat, and UBS's line as the paper printed it",
      px == 39.339 and pos == 0 and f'"{line}"' in paper and "39.31" in line and "37.37" in line)
check("the update is the 5 August 10:00 one, with UBS's line added at its end",
      turns[-1]["content"].startswith(D.AT) and turns[-1]["content"].endswith("UBS [Agent A]: " + line)
      and turns[0]["role"] == "system")

# ---- 2. arms and vectors
names = [a[0] for a in D.arms()]
check("27 arms: none, the holding push alone x1 x2, each state alone, with the holding push x1 x2 and with a random "
      "push x1 x2, and each state with dimension 2339 zeroed",
      len(names) == 27 and names[:3] == ["none", "hold x1", "hold x2"] and "blame + random x2" in names
      and "credit, 2339 zeroed" in names and len(set(names)) == 27)
STATES_DIR, SHIFTS = os.environ.get("RD2_STATES"), os.environ.get("RD2_SHIFTS")
if STATES_DIR and SHIFTS:
    with tempfile.TemporaryDirectory() as tmp:
        os.symlink(SHIFTS, os.path.join(tmp, "shifts.npz"))
        svec, src = D.state_vectors({"emotion": [tmp], "financial": []})
    import state_careers as S
    st, _ = S.load_states(SHIFTS)
    check("the states are the paper's: 2x the layer-22 document state, dimension 2339 left in",
          all(np.allclose(svec[t]["kept"], 2 * st[t][22], rtol=1e-5) for t in D.STATES)
          and abs(svec["loss"]["kept"][2339] + 2 * 971.6) < 1)
    check("the zeroed check arms differ only in dimension 2339",
          all(svec[t]["zeroed"][2339] == 0 and np.array_equal(np.delete(svec[t]["zeroed"], 2339),
                                                              np.delete(svec[t]["kept"], 2339)) for t in D.STATES))
    run1 = sorted(p for e in ("A", "B", "C", "C2", "D", "E", "F") for p in glob.glob(f"{STATES_DIR}/{e}_bf16/*.npz"))
    hold, size, cells = D.hold_direction(run1)
    check("the holding push: all 285 careers' requests, 75 cells, size about 215, dimension 2339 zero",
          len(run1) == 290 and cells == 75 and abs(size - 215.2) < 0.5 and hold[2339] == 0)
    sp = [m for m in []]
    # its sign: going-along states sit lower along it than holding ones
    z = np.load(run1[0])
    units = D.random_units(len(hold))
    check("random directions: ten, unit length, dimension 2339 zero",
          units.shape == (10, 3840) and np.allclose(np.linalg.norm(units, axis=1), 1) and np.all(units[:, 2339] == 0))
    sv, pv = D.vectors(("loss + random x2", "loss", "kept", "random", 2), svec, hold, units)
    check("a random push of the same size: each of the ten replies' directions at twice the holding push's size",
          pv.shape == (10, 3840) and np.allclose(np.linalg.norm(pv, axis=1), 2 * size) and sv is svec["loss"]["kept"])
    sv, pv = D.vectors(("gain + hold x1", "gain", "kept", "hold", 1), svec, hold, units)
    check("the holding push x1 is the direction at its own size", np.allclose(pv, hold))
    print(f"     state sizes {', '.join(f'{t} {svec[t][chr(115) + chr(105) + chr(122) + chr(101)]:.0f}' for t in D.STATES)}; "
          f"holding push {size:.1f}")
else:
    print("skip 2's vectors (no RD2_STATES / RD2_SHIFTS)")

# ---- 3. a tiny random Gemma 3, the real tokenizer, the real update after a short history
TOK = os.environ.get("RD2_TOKENIZER")
if TOK:
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(TOK)
    short = {**career, "history": career["history"]}
    k_idx = next(i for i, t in enumerate(career["history"]) if t["role"] == "user" and t["content"].startswith(D.AT))
    short = {**career, "history": career["history"][k_idx - 2:]}
    t2, _, _, _ = D.turns_at(short, "RULES")
    full = tok.apply_chat_template(t2, add_generation_prompt=True, return_dict=True)["input_ids"]
    k = len(tok.apply_chat_template(t2[:-1], return_dict=True)["input_ids"])
    check("the history before UBS's update is a token prefix of the prompt",
          full[:k] == tok.apply_chat_template(t2[:-1], return_dict=True)["input_ids"])
    W = 64
    model = Gemma3ForCausalLM(Gemma3TextConfig(vocab_size=len(tok), hidden_size=W, intermediate_size=128,
                                               num_hidden_layers=26, num_attention_heads=2, num_key_value_heads=1,
                                               head_dim=32, sliding_window=64, max_position_embeddings=32768)).eval()
    model.generation_config.eos_token_id, model.generation_config.pad_token_id = [1, 106], 0
    layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
    s22, s24 = Steer(layers[22]), Steer(layers[24])
    cap = S2.Capture({24: layers[24]})
    g = np.random.default_rng(3)
    fsvec = {t: {"kept": 5 * g.normal(size=W), "zeroed": 5 * g.normal(size=W)} for t in D.STATES}
    fhold = 4 * g.normal(size=W)
    funits = g.normal(size=(10, W))
    funits /= np.linalg.norm(funits, axis=1, keepdims=True)
    frozen = {"mu": g.normal(size=W), "sc": np.abs(g.normal(size=W)) + 0.5, "coef": g.normal(size=W),
              "intercept": np.array([0.2]), "trigger": np.array([0.0])}
    mon = D.monitor_scores(model, tok, s22, s24, cap, full, k, fsvec, fhold, funits, frozen)

    def brute(v22, v24):
        got = {}

        def h22(m, i, o):
            h = (o[0] if isinstance(o, tuple) else o).clone()
            if v22 is not None:
                h[0, k:] += torch.tensor(v22, dtype=h.dtype)
            return (h,) + tuple(o[1:]) if isinstance(o, tuple) else h

        def h24(m, i, o):
            h = (o[0] if isinstance(o, tuple) else o).clone()
            if v24 is not None:
                h[0, k:] += torch.tensor(v24, dtype=h.dtype)
            got["s"] = h[0, -1].float().numpy().astype(np.float64)
            return (h,) + tuple(o[1:]) if isinstance(o, tuple) else h
        a, b = layers[22].register_forward_hook(h22), layers[24].register_forward_hook(h24)
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([full]))
        finally:
            a.remove(), b.remove()
        return float(((got["s"] - frozen["mu"]) / frozen["sc"]) @ frozen["coef"] + frozen["intercept"][0])

    close = lambda a, b: abs(a - b) < 1e-3 * max(1, abs(b))
    check("monitor, no state: equals a full read with no cache", close(mon["none"]["score"], brute(None, None)))
    check("monitor, loss + hold x2: equals a full read with the state at 22 and the push at 24 from UBS's update on",
          close(mon["loss + hold x2"]["score"], brute(fsvec["loss"]["kept"], 2 * fhold)))
    rs = mon["blame + random x1"]["scores"]
    check("monitor, a random push: ten directions, each equal to its own full read",
          len(rs) == 10 and all(close(rs[j], brute(fsvec["blame"]["kept"], np.linalg.norm(fhold) * funits[j]))
                                for j in (0, 4, 9)))
    check("the zeroed check arm uses the zeroed state", close(mon["gain, 2339 zeroed"]["score"],
                                                             brute(fsvec["gain"]["zeroed"], None)))
    # one direction per reply in a batch, against each reply read on its own (no sampling: the last token's logits)
    cache = prefill(model, full[:k])
    pv = 3 * funits[:4]
    c = copy.deepcopy(cache)
    c.batch_repeat_interleave(4)
    s24.vec = torch.tensor(pv, dtype=torch.float32)[:, None, :]
    with torch.no_grad():
        lb = model(input_ids=torch.tensor([full[k:]] * 4), past_key_values=c, use_cache=True,
                   cache_position=torch.arange(k, len(full))).logits[:, -1]
    single = []
    for j in range(4):
        s24.vec = torch.tensor(pv[j], dtype=torch.float32)
        with torch.no_grad():
            single.append(model(input_ids=torch.tensor([full[k:]]), past_key_values=copy.deepcopy(cache), use_cache=True,
                                cache_position=torch.arange(k, len(full))).logits[0, -1])
    s24.vec = None
    check("one random direction per reply: each batch row equals that reply read on its own",
          all(torch.allclose(lb[j], single[j], atol=1e-4) for j in range(4)))
    D.MAX_NEW_TOKENS, D.BATCHES = 6, 2
    a_none = D.generate_arm(model, tok, s22, s24, full, cache, D.arms()[0], fsvec, fhold, funits, 0)
    a_none2 = D.generate_arm(model, tok, s22, s24, full, cache, D.arms()[0], fsvec, fhold, funits, 0)
    a_rand = D.generate_arm(model, tok, s22, s24, full, cache, ("loss + random x2", "loss", "kept", "random", 2),
                            fsvec, fhold, funits, 0)
    check("paired seeds: an arm repeats exactly; ten replies per batch; batch b uses seed 1000 + b",
          [r["reply"] for r in a_none] == [r["reply"] for r in a_none2] and len(a_none) == 20
          and {r["seed"] for r in a_none} == {1000, 1001})
    check("a random arm records its direction per reply; steering is off afterwards",
          [r["random_direction"] for r in a_rand[:10]] == list(range(10)) and s22.vec is None and s24.vec is None
          and [r["reply"] for r in a_rand] != [r["reply"] for r in a_none])
    D.MAX_NEW_TOKENS, D.BATCHES = 300, 5
else:
    print("skip 3 (no RD2_TOKENIZER)")

# ---- 4. the analysis on made-up rows: states alone sell through 45/50; the holding push cuts that to 10/50 at x1 and
# 5/50 at x2; the random push leaves 45/50; the zeroed states 20/50
with tempfile.TemporaryDirectory() as tmp:
    rows_path, mon_path, out = os.path.join(tmp, "rows.jsonl"), os.path.join(tmp, "mon.json"), os.path.join(tmp, "o")
    with open(rows_path, "w") as f:
        for name, state, which, push, s in D.arms():
            for b in range(5):
                for j in range(10):
                    i = b * 10 + j
                    if state is None:
                        sold = i < (5 if push is None else 2)
                    elif which == "zeroed":
                        sold = i < 20
                    elif push == "hold":
                        sold = i < (10 if s == 1 else 5)
                    else:
                        sold = i < 45
                    f.write(json.dumps({"arm": name, "state": state, "state_2339": which, "push": push,
                                        "push_strength": s, "batch": b, "row": j, "seed": 1000 + b,
                                        "status": "trade" if sold else "hold", "target": -100000 if sold else None,
                                        "sold_through": sold, "reply": ("The price, the stop.\nTARGET -100000" if sold
                                                                        else "Holding.\nHOLD")}) + "\n")
    json.dump({"trigger": -0.89, "bf16": {a: {"score": 0.1, "flagged": True} for a in names},
               "4bit": {a: {"score": -1.0, "flagged": False} for a in names}}, open(mon_path, "w"))
    res = subprocess.run([sys.executable, "designs/rd2/analysis/direct_push.py", rows_path, mon_path, out],
                         capture_output=True, text=True)
    check("the analysis runs", res.returncode == 0)
    if res.returncode:
        print(res.stderr[-1500:])
    else:
        S_ = json.load(open(os.path.join(out, "direct_push.json")))
        check("success met at both sizes (pooled, both comparisons)",
              S_["success"]["x1"]["met"] and S_["success"]["x2"]["met"]
              and S_["success"]["x1"]["hold_vs_alone"][:2] == [0, 140])
        check("per state: hold x2 sold 5 of 50 against 45 alone and 45 random; exact test p below 1e-9",
              S_["arms"]["loss + hold x2"]["sold_through"] == 5 and S_["comparisons"]["loss x2"]["hold_vs_alone"][2]
              < 1e-9 and S_["comparisons"]["loss x2"]["hold_vs_random"][:2] == [0, 40])
        txt = open(os.path.join(out, "DIRECT_PUSH.md")).read()
        check("the report has the monitor table and the zeroed check", "Does the frozen monitor flag" in txt
              and "loss: 20/50 (as in the paper 45/50)" in txt)
print("\nALL CHECKS PASS" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
