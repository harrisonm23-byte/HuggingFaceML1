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

## 2. The careers, neutral and loss wording (about 140 GPU-hours)

Seven arms, 10 careers each, in two wordings of UBS's lines:

| Arm | Why |
|---|---|
| none | the baseline |
| loss@21, blame@21, random@21 | bad-news states; the agent's own replies went along more at 21 |
| loss@14, gain@14, random@14 | every emotional state acts at 14, and random does not |

```
modal run --detach scripts/modal_state_careers.py --arms "none,loss@21,blame@21,random@21,loss@14,gain@14,random@14" --framings "neutral,loss" --per-arm
```

- It prints the arms and their sizes first, then starts. A typo stops it before any GPU starts.
- `--per-arm` gives every career its own GPU. If Modal limits how many run at once, the rest wait in line on their own.
- To halve the cost, drop the loss wording: `--framings "neutral"` (about 70 GPU-hours).

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
- **Layer 22 careers:** layer 14 covers the same all-states effect, with a quieter random control.
- **Layer 19:** the order went up there, but the agent's own replies went down.
- **The other three wordings** (gain, loss + you, gain + you): only if the neutral and loss careers show an effect.
