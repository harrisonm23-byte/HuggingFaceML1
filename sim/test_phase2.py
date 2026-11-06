"""Needs torch and transformers (CPU is enough):

    RD2_STATES=<folder of the downloaded <exp>_bf16 states> RD2_TOKENIZER=<a Gemma 3 tokenizer folder> python sim/test_phase2.py

Checks for Phase 2's single moments (sim/phase2.py, scripts/modal_phase2.py, designs/rd2/analysis/phase2.py), no GPU:
1. the moments: every career's 7 and 12 January request, 570 in all, each with a fixed flag, seed and random direction;
2. the vectors: contrastive = minus the going-along gap at the chosen size, built on the other half of the careers;
   random of the same size; the same random direction at all three sizes;
3. a tiny random Gemma 3 with the real tokenizer on a real career: the unsteered decision state equals a full read
   with no cache; steering every token from the update on, and the decision token only, equal a full read with the same
   vector added by hand; the single-token push fires once in each of the three passes, at the decision token; an arm
   run alone gives the same row as in the full sequence (the shared cache is never changed); paired seeds repeat;
4. the analysis on made-up rows with known answers (the conditional arm put together from the flags).
"""
import copy, csv, glob, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.chdir(ROOT)
import numpy as np
import torch
from transformers import AutoTokenizer, Gemma3ForCausalLM, Gemma3TextConfig
import phase2 as P
import steer2 as S2
from career import career_opening
from inside_careers import moments
from interventions import NEUTRAL_LEAD, WIDE_GRID, Steer, split_point

ok = True


def check(name, cond):
    global ok
    print(("ok   " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- 1. the moments
items = P.work_items(moments)
by_req = {r: [i for i in items if i["chat"] == r] for r in P.REQUESTS}
check("570 moments: 285 at 7 January and 285 at 12 January, one per career",
      len(items) == 570 and all(len(v) == 285 for v in by_req.values())
      and len({(i["experiment"], i["career_file"]) for i in by_req["p344_i_can_hunt_with_u"]}) == 285)
check("the saved careers went along at 145 (7 Jan) and 99 (12 Jan) of them",
      [sum(i["saved_joined"] for i in by_req[r]) for r in P.REQUESTS] == [145, 99])
flags = {f"{f['experiment']}|{f['career_file']}|{f['chat']}": f for f in
         csv.DictReader(open("results/conditional_steering/flags.csv"))}
check("every moment has its fixed flag", all(i["key"] in flags for i in items))
check("seeds differ between moments; random directions spread over all ten",
      len({i["seed"] for i in items}) == 570 and len({i["random_index"] for i in items}) == P.N_RANDOM)
pilot = P.spread(items, 8)
check("the pilot spreads over both requests and several experiments",
      len({i["key"] for i in pilot}) == 8 and {i["chat"] for i in pilot} == set(P.REQUESTS)
      and len({i["experiment"] for i in pilot}) >= 4)
names = [a[0] for a in P.arms()]
check("eight arms: none, contrastive and random at 0.5, 1 and 2, contrastive x2 on the decision token",
      names == ["none", "contrastive x0.5", "contrastive x1", "contrastive x2", "random x0.5", "random x1", "random x2",
                "contrastive x2, decision token only"])

# ---- 2. the vectors, from the real states
STATES = os.environ.get("RD2_STATES")
if STATES:
    run1 = sorted(p for e in P.FOLDERS for p in glob.glob(f"{STATES}/{e}_bf16/*.npz"))
    check("290 careers of saved states", len(run1) == 290)
    X24 = np.concatenate([np.load(p)["states"][:, P.LAYER] for p in run1]).astype(np.float64)
    sd = X24.std(0)
    check("dimension 2339 is the only one at layer 24 with a spread above 1,000 (the massive-activation dimension)",
          list(np.where(sd > 1000)[0]) == P.DROP_DIMS)
    dirs = P.directions(run1)
    check("it is zero in the gap and in every random direction, and the sizes are measured without it",
          all(dirs[h]["along"][2339] == 0 and np.all(dirs[h]["random"][:, 2339] == 0)
              and abs(dirs[h]["size"] - np.linalg.norm(dirs[h]["along"])) < 1e-9
              and np.allclose(np.linalg.norm(dirs[h]["random"], axis=1), 1) for h in (0, 1)))
    it0 = next(i for i in items if i["run"] < 5)
    it1 = next(i for i in items if i["run"] >= 5)
    check("contrastive x2 = minus twice the gap built on the other half (runs 5-9 for runs 0-4, and back)",
          np.allclose(P.vector(dirs, it0, "contrastive", 2), -2 * dirs[0]["along"])
          and np.allclose(P.vector(dirs, it1, "contrastive", 2), -2 * dirs[1]["along"]))
    r = [P.vector(dirs, it0, "random", s) for s in P.STRENGTHS]
    check("random: the gap's size times the strength, one direction at all three sizes",
          all(abs(np.linalg.norm(v) - s * dirs[0]["size"]) < 1e-6 for v, s in zip(r, P.STRENGTHS))
          and abs(r[0] @ r[2] / np.linalg.norm(r[0]) / np.linalg.norm(r[2]) - 1) < 1e-9)
    check("without it, the two halves' gaps agree (cosine above 0.6)",
          dirs[0]["along"] @ dirs[1]["along"] / dirs[0]["size"] / dirs[1]["size"] > 0.6)
    print(f"     gap sizes {dirs[0]['size']:.1f} and {dirs[1]['size']:.1f} (with dimension 2339: "
          f"{dirs[0]['size_with_dropped']:.1f} and {dirs[1]['size_with_dropped']:.1f}); cells {dirs[0]['cells']}, {dirs[1]['cells']}; "
          f"cosine {dirs[0]['along'] @ dirs[1]['along'] / dirs[0]['size'] / dirs[1]['size']:.2f}")
else:
    print("skip 2 (no RD2_STATES)")

# ---- 3. a tiny random Gemma 3 with the real tokenizer, on a real 7 January moment
TOK = os.environ.get("RD2_TOKENIZER")
if TOK:
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(TOK)
    W = 64
    cfg = Gemma3TextConfig(vocab_size=len(tok), hidden_size=W, intermediate_size=128, num_hidden_layers=26,
                           num_attention_heads=2, num_key_value_heads=1, head_dim=32, sliding_window=64,
                           max_position_embeddings=32768)
    model = Gemma3ForCausalLM(cfg).eval()
    model.generation_config.top_k, model.generation_config.top_p = 64, 0.95
    model.generation_config.eos_token_id, model.generation_config.pad_token_id = [1, 106], 0
    layers = [m for _, m in model.named_modules() if type(m).__name__.endswith("DecoderLayer")]
    steer, once = Steer(layers[P.LAYER]), P.SteerOnce(layers[P.LAYER])
    fired = []
    hook0 = once._hook

    def counting(module, inputs, output):
        if once.vec is not None:
            h = output[0] if isinstance(output, tuple) else output
            if h.shape[1] > once.index:
                fired.append((h.shape[1], once.index))
        return hook0(module, inputs, output)

    once.handle.remove()
    once.handle = layers[P.LAYER].register_forward_hook(counting)
    capture = S2.Capture({P.LAYER: layers[P.LAYER]})
    g = np.random.default_rng(1)
    fake = {h: {"along": 3 * g.normal(size=W), "random": None, "cells": 0} for h in (0, 1)}
    for h in fake.values():
        h["size"] = float(np.linalg.norm(h["along"]))
        rr = g.normal(size=(P.N_RANDOM, W))
        h["random"] = rr / np.linalg.norm(rr, axis=1, keepdims=True)
    frozen = {"mu": g.normal(size=W), "sc": np.abs(g.normal(size=W)) + 0.5, "coef": g.normal(size=W),
              "intercept": np.array([0.1])}
    item = next(i for i in items if i["chat"] == "p344_i_can_hunt_with_u" and i["experiment"] == "B")
    career = json.load(open(f"{P.folder_of('B')}/careers/{item['career_file']}"))
    opening = career_opening()
    grid = WIDE_GRID[:5] + [0]
    rows = list(P.run_item(model, tok, steer, once, capture, fake, frozen, item, career, opening, NEUTRAL_LEAD, grid,
                           samples=3))
    full, k = split_point(tok, career, item["history_index"], opening)
    print(f"     a real 7 January prompt: {len(full):,} tokens, the update {len(full) - k:,}")

    def brute(add_at):
        """A full read with no cache; `add_at`: {position: vector} added to layer 24's output by hand."""
        got = {}

        def hook(module, inputs, output):
            h = (output[0] if isinstance(output, tuple) else output).clone()
            for p, v in add_at.items():
                h[0, p] += v
            got["s"] = h[0, -1].float().numpy()            # after the vector is added (this hook runs last)
            return (h,) + tuple(output[1:]) if isinstance(output, tuple) else h
        hd = layers[P.LAYER].register_forward_hook(hook)
        try:
            with torch.no_grad():
                model(input_ids=torch.tensor([full]))
        finally:
            hd.remove()
        s = got["s"].astype(np.float64)
        return float(((s - frozen["mu"]) / frozen["sc"]) @ frozen["coef"] + frozen["intercept"][0]), \
            float(s @ fake[P.half_for(item["run"])]["along"] / fake[P.half_for(item["run"])]["size"])

    R = {r["arm"]: r for r in rows}
    vec2 = torch.tensor(P.vector(fake, item, "contrastive", 2), dtype=torch.float32)
    b_none = brute({})
    b_all = brute({p: vec2 for p in range(k, len(full))})
    b_tok = brute({len(full) - 1: vec2})
    close = lambda a, b: abs(a - b) < 1e-3 * max(1, abs(b))
    check("unsteered: the decision state (monitor score, gap position) equals a full read with no cache",
          close(R["none"]["monitor_score"], b_none[0]) and close(R["none"]["along_position"], b_none[1]))
    check("contrastive x2 on every token from the update on equals a full read with it added there by hand",
          close(R["contrastive x2"]["monitor_score"], b_all[0]) and close(R["contrastive x2"]["along_position"], b_all[1]))
    check("contrastive x2 on the decision token only equals a full read with it added at that token alone",
          close(R["contrastive x2, decision token only"]["monitor_score"], b_tok[0])
          and close(R["contrastive x2, decision token only"]["along_position"], b_tok[1]))
    head = len(tok("\n\n".join([NEUTRAL_LEAD.strip(), ""]), add_special_tokens=False)["input_ids"])
    check("the single-token push fires once in each pass (state, scored order, sampling), always at the decision token",
          fired == [(len(full) - k, len(full) - 1 - k), (len(full) - k + head - 1, len(full) - 1 - k),
                    (len(full) - k, len(full) - 1 - k)])
    check("the push moved the decision state along the gap: down at x2 everywhere, less on the token alone",
          R["contrastive x2"]["along_position"] < R["contrastive x1"]["along_position"] < R["none"]["along_position"]
          and R["none"]["along_position"] - R["contrastive x2"]["along_position"] > 0.5)
    check("every row: three replies, judged, the order distribution sums to 1, and saves as JSON",
          all(len(r["replies"]) == 3 and len(r["went_along"]) == 3 and abs(sum(r["probs"]) - 1) < 1e-6 for r in rows)
          and len(json.dumps(rows)) > 0)
    again = list(P.run_item(model, tok, steer, once, capture, fake, frozen, item, career, opening, NEUTRAL_LEAD, grid,
                            done={r["key"] for r in rows if r["arm"] != "contrastive x2, decision token only"},
                            samples=3))
    check("an arm run alone (the others already done) gives the same row: the shared cache is never changed",
          len(again) == 1 and again[0]["replies"] == R["contrastive x2, decision token only"]["replies"]
          and close(again[0]["monitor_score"], R["contrastive x2, decision token only"]["monitor_score"])
          and np.allclose(again[0]["probs"], R["contrastive x2, decision token only"]["probs"]))
    none_again = list(P.run_item(model, tok, steer, once, capture, fake, frozen, item, career, opening, NEUTRAL_LEAD,
                                 grid, done={r["key"] for r in rows if r["arm"] != "none"}, samples=3))
    check("paired seeds: the unsteered replies repeat exactly; the three replies are not all the same",
          none_again[0]["replies"] == R["none"]["replies"] and len(set(R["none"]["replies"])) > 1)
    # (a random model puts nearly all of the scored orders' probability on HOLD, the shortest; their total moves)
    check("steering changes the sampled replies and the scored orders' total probability (same seed)",
          R["contrastive x2"]["replies"] != R["none"]["replies"]
          and abs(np.log(R["contrastive x2"]["coverage"]) - np.log(R["none"]["coverage"])) > 1e-3)
    check("steering is off after every arm (no vector left on)", steer.vec is None and once.vec is None)
else:
    print("skip 3 (no RD2_TOKENIZER)")

# ---- 4. the analysis on made-up rows: none always goes along, contrastive never, random always
with tempfile.TemporaryDirectory() as tmp:
    rows_dir, out = os.path.join(tmp, "rows"), os.path.join(tmp, "out")
    os.makedirs(rows_dir)
    with open(os.path.join(rows_dir, "part0.jsonl"), "w") as f:
        for i in items:
            for name, kind, which, s in P.arms():
                along = name == "none" or name.startswith("random")
                reply = ("The price is falling, I'll follow UBS.\nTARGET -100000" if along else "Holding.\nHOLD")
                f.write(json.dumps({**i, "key": f"{i['key']}|{name}", "arm": name, "status": ["trade" if along else
                                    "hold"] * 4, "went_along": [along] * 4, "replies": [reply] * 4,
                                    "p_order_along": 0.9 if along else 0.1, "along_position": 0.0 if along else -1.0,
                                    "monitor_score": float(flags[i["key"]]["score_frozen_in_sample"]), "seconds": 1.0})
                        + "\n")
    res = subprocess.run([sys.executable, "designs/rd2/analysis/phase2.py", rows_dir, out], capture_output=True,
                         text=True)
    check("the analysis runs on made-up rows", res.returncode == 0)
    if res.returncode:
        print(res.stderr[-2000:])
    else:
        S = json.load(open(os.path.join(out, "phase2.json")))
        j7, j12 = S["requests"]["7 Jan"], S["requests"]["12 Jan"]
        fl7 = np.mean([int(flags[i["key"]]["flag"]) for i in by_req["p344_i_can_hunt_with_u"]])
        check("conditional = contrastive where flagged, none elsewhere: went along = 1 - share flagged",
              abs(j7["arms"]["conditional x2"]["went_along"][0] - (1 - fl7)) < 1e-9
              and abs(j7["arms"]["conditional x2"]["steered"] - fl7) < 1e-9 and j7["flagged"] == 214
              and j12["flagged"] == 133)
        check("avoided per 100 requests steered: 100 for both (every steered request avoided)",
              all(abs(S["requests"][r]["conditional_vs_unconditional"][a]["avoided_per_100"][0] - 100) < 1e-6
                  for r in ("7 Jan", "12 Jan") for a in ("contrastive x1", "conditional x1")))
        check("criterion 1 met (contrastive below random); criterion 2 met (HOLD is readable); market reasoning read",
              j7["criteria"]["x2"]["1"] and j7["criteria"]["x2"]["2"]
              and j7["arms"]["none"]["market_reasoning"][0] == 1.0
              and j7["arms"]["contrastive x2"]["market_reasoning"][0] == 0.0)
        check("each request reported on its own, every arm, and the monitor check reads the frozen scores",
              set(S["requests"]) == {"7 Jan", "12 Jan"} and len(j7["arms"]) == 11
              and abs(j7["checks"]["monitor_corr"] - 1) < 1e-9 and j7["checks"]["trigger_agreement"] == 1.0)
print("\nALL CHECKS PASS" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
