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

## 2. The careers: one state, two wordings (20 careers, about 20 GPU-hours, roughly $80)

The loss state at layer 21, 10 careers with UBS's neutral wording and 10 with its loss wording. No no-state arm is
run: B's own neutral and loss careers are the baseline (the same seeds and the same code, with nothing switched on).

```
modal run --detach scripts/modal_state_careers.py --arms "loss@21" --framings "neutral,loss" --per-arm
```

- It prints the arm and its size first, then starts. A typo stops it before any GPU starts.
- Neutral wording asks: does the loss state alone push the agent along, against B's neutral careers?
- Loss wording asks: does the state add to a loss-worded career (the "double loss"), against B's loss careers?
- If the neutral arm shows an effect, the next run is the random control (10 careers, about $40):
  `--arms "random@21" --framings "neutral" --per-arm`.

Results:
- `results/state_careers/STATE_CAREERS.md` (neutral wording)
- `results/state_careers_loss/STATE_CAREERS.md` (loss wording)

The full version (7 arms, both wordings, 140 careers, about $550) is
`--arms "none,loss@21,blame@21,random@21,loss@14,gain@14,random@14" --framings "neutral,loss"`.

## 3. When everything has landed

Tell Claude: "Everything's in. Read LAYER_SCAN_FRAMED_L14_22, STATE_CAREERS and STATE_CAREERS for loss, and update the injection-series document."

## If something stops

- A career job that fails is retried by Modal and carries on from its last saved trading day.
- Rerunning the same command skips every career already saved and only runs what is missing.
- If only the analysis failed, rerun it alone:

```
modal run scripts/modal_state_careers.py --arms "loss@21" --framings "neutral,loss" --analysis-only
```

## Left out on purpose

- **Financial states:** no layer beat random in the sweep (`results/layer_scan_fin/LAYER_SWEEP.md`).
- **Blame, gain and the layer-14 arms:** left for budget. Layer 21 is the one layer where the agent's own replies already went along more; step 1 shows whether layer 14 does too.
- **Layer 19:** the order went up there, but the agent's own replies went down.
- **The other three wordings** (gain, loss + you, gain + you): only if the neutral and loss careers show an effect.
