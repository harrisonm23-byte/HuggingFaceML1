# Runbook: finishing the injection series

Everything left to run, launched at once. No step waits on another. Run from the repo on the Mac.

```
git pull
```

## 1. The framed test at layers 14 and 22 (about 1 hour, 3 GPUs)

All four emotional states, all five wordings of UBS's request, with the agent's own sampled replies for every state.

```
modal run --detach scripts/modal_layer_scan.py --framed --layers 14,22 --parts 3
```

Result: `results/layer_scan/LAYER_SCAN_FRAMED_L14_22.md`

## 2. The careers: a pilot, 2 careers per arm (28 careers, roughly $112; launched)

Seven arms, 2 careers each (rounds 0 and 1), in UBS's neutral and loss wording, including a no-state arm run with the
same code. B's own neutral and loss careers are a second baseline (the same seeds, nothing switched on).

```
modal run --detach scripts/modal_state_careers.py --arms "none,loss@21,blame@21,random@21,loss@14,gain@14,random@14" --framings "neutral,loss" --rounds 0-1 --per-arm
```

- Two careers per arm shows whether a state does something large, or breaks the agent. It cannot prove a modest
  effect: B's neutral careers went along 5% of the time and its loss careers 25%.
- This is the run launched on 22 Oct (Modal app ap-4YzC80iebLRTjXDKAFgS8S).

Then top up the arms that look promising to 10 careers. Saved careers are skipped, so rounds 0 and 1 count:

```
modal run --detach scripts/modal_state_careers.py --arms "none,loss@21" --framings "neutral,loss" --rounds 2-9 --per-arm
```

Results:
- `results/state_careers/STATE_CAREERS.md` (neutral wording)
- `results/state_careers_loss/STATE_CAREERS.md` (loss wording)

## 3. When everything has landed

Tell Claude: "Everything's in. Read LAYER_SCAN_FRAMED_L14_22, STATE_CAREERS and STATE_CAREERS for loss, and update the injection-series document."

## If something stops

- A career job that fails is retried by Modal and carries on from its last saved trading day.
- Rerunning the same command skips every career already saved and only runs what is missing.
- If only the analysis failed, rerun it alone:

```
modal run scripts/modal_state_careers.py --arms "none" --framings "neutral,loss" --analysis-only
```

## Left out on purpose

- **Financial states:** no layer beat random in the sweep (`results/layer_scan_fin/LAYER_SWEEP.md`).
- **Layer 19:** the order went up there, but the agent's own replies went down.
- **The other three wordings** (gain, loss + you, gain + you): only if the neutral and loss careers show an effect.
