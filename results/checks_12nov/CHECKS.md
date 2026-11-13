# Checks of 12 November (CPU, saved states and saved episodes; exploratory)

Repo letters throughout (repo E = the paper's F, repo F = the paper's E). Every script takes its inputs as arguments; the
states are the rd2-states volume's `v2/{A,B,C,C2,D,E,F}_bf16`, `v2/{A,B,D,E,F}_bf16_steps` and `v2/matched/{A,B}_bf16`.

## Grader agreement (`kappa/`)

| Set | Items graded twice | Same label | Cohen's kappa |
|---|---|---|---|
| B's words (`results/words_b`, first grader vs re-check) | 247 | 93.9% | 0.91 |
| B's words, graded again inside `results/words_all` | 54 | 90.7% | 0.87 |
| Whole-episode injections, stance (`results/state_careers_words`) | 192 | 97.4% | 0.96 |
| Whole-episode injections, "cautious" side label | 192 | 81.8% | 0.63 |
| Ministral history (`results/history_words_ministral`) | 198 | 91.4% | 0.88 |

## Dimension 2339 (`dim2339/`)

- **steer2's directions** (`check.py`): the layer-12 frame direction behind the preregistered H1-H4 is 87% dimension
  2339 by squared size in both halves (loss 0.866 / 0.870; gain 0.874 / 0.868); loss and gain are nearly the same
  vector. Dimension 2339 averages about 8,500 at layer 12 (next largest about 345) and 72,000 at layer 24. The
  layer-24 going-along direction (the +14.0-point check) is 87% dimension 2339 in half 0 and 1% in half 1.
- **Management's loss vs UBS's loss** (`memo_cos.py`, the matched_memo.py section 2 cosine): layer 12, 0.590 as
  published, -0.036 without 2339 (ceiling 0.738 without). Without it, -0.08 to +0.07 at every layer.
- **The frame along every update** (`mountain_no2339.py`, mountain_inside.py with 2339 zeroed in the yardsticks): B,
  framed minus neutral on the layer-12 frame direction, 7 Jan to 5 Aug: as published +0.64 (p 0.04), +0.64 (0.04),
  +0.56 (0.08), +0.47 (0.13), +0.45 (0.13); without 2339 +0.13 (p 0.03), +0.12 (0.02), +0.11 (0.004), +0.16 (0.001),
  +0.15 (< 0.001), in units of UBS's loss request's own shift without 2339. The persistence holds, smaller and
  steadier. (The framed messages are still in the context throughout: the plan's F2.)

## State dependence (`state_dependence/`)

Dynamic random-effects logit with Wooldridge's initial condition, requests 2-6, 285 careers, request and
experiment x framing effects, 100 career-bootstrap refits. Going along at the last request: odds x 2.1 (1.2 to 4.5);
pooled logit x 2.5; the career's own lean sd 0.53 (0 to 0.87); going along at the first request 0.22 (-0.49 to 1.03)
on the log-odds scale. Average P(goes along) at requests 2-6: 8.0% after holding, 12.2% after going along. Raw: 12 Jan
72/145 after going along on 7 Jan vs 27/140; 1 Apr 14/99 vs 4/186. Every trading day of all 290 careers opens flat, so
no 7 Jan sale is bought back on 12 Jan. `p6b.py`: the same with the position held when asked, and on two stricter
scores (from a flat position; set off a client stop).

**Robustness (`p6b.py`, 290 careers, 100 refits each): the doubling does not hold up.**

| Version | Events, requests 2-6 | Odds ratio, last request (95%) | First request (log-odds) | Position held when asked |
|---|---|---|---|---|
| As above | 141 | 2.1 (1.2 to 4.5) | 0.22 (-0.49 to 1.03) | |
| + position held when asked (per 100,000 oz UBS's way) | 141 | 1.84 (0.76 to 3.47) | 0.50 (-0.28 to 1.79) | +0.29 (0.03 to 0.70) |
| Strict: went along from a flat position | 86 | 1.63 (0.32 to 6.17) | 2.52 (0.90 to 4.98) | |
| Strict, from flat + position | 86 | 1.58 (0.42 to 5.98) | 2.52 (1.23 to 5.10) | -0.26 (-0.60 to -0.10) |
| Strict: went along and set off a client stop | 62 | 0.39 (0.13 to 0.78) | 0.37 (-0.42 to 1.65) | |

With the position held, the interval includes 1 (the two 8 June requests fall on the same day, so a position taken at
the first is still held at the second). On the strict scores the lean sits in the first request, not in the last one,
and going along that set off a stop is followed by less going along. Not for the paper as a finding.

## Monitor transfer (`monitor_transfer/`)

M2 as frozen (layer 24, C = 0.001). Within-request AUROC (the request date alone separates going along), career
bootstrap; shuffled-label control: labels permuted within request on the training rows, 50 refits.

| Built on -> tested on | Within request | Shuffled, 95th percentile |
|---|---|---|
| B -> A | 0.673 (0.455 to 0.892) | 0.737 |
| B -> C | 0.777 (0.641 to 0.890) | 0.635 |
| B -> C2 | 0.628 (0.460 to 0.812) | 0.664 |
| B -> D | 0.731 (0.625 to 0.824) | 0.622 |
| B -> E | 0.804 (0.727 to 0.874) | 0.637 |
| B -> F | 0.791 (0.711 to 0.863) | 0.688 |
| B: neutral + loss -> blame + credit | 0.787 (0.632 to 0.954) | 0.729 |
| B + F: neutral + loss -> blame + credit | 0.726 (0.592 to 0.847) | 0.707 |
