"""Section 2 of designs/rd2/analysis/matched_memo.py (management's priming direction vs UBS's loss direction), run twice:
as published, and with dimension 2339 set to zero in both directions. Section 3 (SAE features) is cut.
Usage (from the repo root): python memo_cos.py <states root> <out dir>"""
import os, sys, json
src = open(os.path.join(os.getcwd(), "designs/rd2/analysis/matched_memo.py")).read()
src = src.split("# ---------------- 3.")[0]
assert "ucos = lambda a, b: float(unit(a) @ unit(b))" in src
res = {}
for drop in (False, True):
    s = src
    if drop:
        s = s.replace("ucos = lambda a, b: float(unit(a) @ unit(b))",
                      "def _z(x):\n    x = np.array(x, np.float64); x[..., 2339] = 0.0\n    return x\n"
                      "ucos = lambda a, b: float(unit(_z(a)) @ unit(_z(b)))")
    s = s.replace('np.save(os.path.join(ROOT, "matched", "memo_direction_held_fixed_L24.npy"), unit(u))', "pass")
    g = {"__name__": "__main__", "__file__": os.path.join(os.getcwd(), "designs/rd2/analysis/matched_memo.py")}
    sys.argv = ["matched_memo.py", sys.argv[1], os.path.join(sys.argv[2], "with" if not drop else "without")]
    os.makedirs(sys.argv[2], exist_ok=True)
    exec(compile(s, "matched_memo.py", "exec"), g)
    res["without 2339" if drop else "with 2339 (as published)"] = g["summary"]["direction"]
argv_out = sys.argv[2].rsplit("/", 1)[0]
json.dump(res, open(os.path.join(argv_out, "memo_cos.json"), "w"), indent=1, default=float)
for k, v in res.items():
    print(k)
    for l, r in v.items():
        print(f"  layer {l}: ceiling {r['ceiling']:.3f}  vs Run 1 memo {r['run1_memo']}  vs UBS loss {r['ubs_loss']}")
