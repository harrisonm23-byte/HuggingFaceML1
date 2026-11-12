"""Run designs/rd2/analysis/mountain_inside.py with dimension 2339 set to zero in every yardstick (frame and going-
along directions), sizes measured without it. Usage (from the repo root): python mountain_no2339.py <states root> <out>"""
import os, runpy, sys
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "sim"))
import steer2
D = 2339
_dirs, _along = steer2.directions, steer2.along_direction
def directions(*a, **k):
    out = _dirs(*a, **k)
    for h in out.values():
        for key in ("loss", "gain", "loss_minus_gain"):
            h[key] = h[key].copy(); h[key][D] = 0.0
        h["size"] = float(np.linalg.norm(h["loss"]))
    return out
def along_direction(*a, **k):
    out = _along(*a, **k)
    for h in out.values():
        h["along"] = h["along"].copy(); h["along"][D] = 0.0; h["size"] = float(np.linalg.norm(h["along"]))
    return out
steer2.directions, steer2.along_direction = directions, along_direction
sys.argv = ["mountain_inside.py"] + sys.argv[1:]
runpy.run_path(os.path.join(os.getcwd(), "designs/rd2/analysis/mountain_inside.py"), run_name="__main__")
