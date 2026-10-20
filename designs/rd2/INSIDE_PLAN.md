# Inside the model: the plan in one place (living document; updated as ideas come in)

Model: Gemma 3 12B (careers ran at 4-bit; states read at bfloat16, Gemma Scope 2's precision, with a 4-bit check).
Data: every saved career (A, B, C, D, E, F; C redone = C2). Every comparison is made **within the same push request**
(notebook 13's read-out mostly recognised which chat it was).

## Status at a glance

| # | Method | What it asks | Status | Where |
|---|---|---|---|---|
| 1 | Gemma Scope features, "find, then name" | Which features differ at the decision: loss vs gain, "+ you" vs none, framed vs neutral, went along vs not, memo vs neutral, request vs no request, Bank C vs not | **Running** (Run 1) | `scripts/modal_inside.py`, `designs/rd2/analysis/inside_features.py` -> `results/inside_full_career/` |
| 2 | Manipulation check | Did the frame land inside the model (framed vs neutral, loss vs gain features)? | **Running** (Run 1, same comparisons) | as 1 |
| 3 | Decision read-out (layer probes) | Can "went along" be read from the state beyond the request and the framing? Scored on held-out careers, against the labels alone (AUC 0.90 bar) and shuffled outcomes | **Running** (Run 1) | as 1 |
| 4 | Bank C, paired | F against its B twin (same seed, same career until 7 Jan): how much does Bank C's line move the state? | **Running** (Run 1) | as 1 |
| 5 | The path inside (the mountain; "measurement 3") | The internal loss / pressure signal at every update (~120 per career): does it stay high, fade or build, and does it outlast the words? Framing gap = framed minus neutral at the same step | **Running** (Run 2, `--every-step`, 8 layers) | `read_steps` in `scripts/modal_inside.py`; analysis to write when the states land |
| 6 | Hidden pressure (chain of thought) | Steps whose written reasoning is calm but whose internal signal is high: what a reasoning-only monitor would not see | To do (needs 5) | analysis on Run 2's states + `self_echo.py` |
| 7 | Steering (causal) | Add the loss-frame direction to neutral agents, remove it from loss + you agents, at two strengths, against a random direction; built on the other half of the careers | **Built**, launch after Run 1 | `sim/interventions.py`, `scripts/modal_interventions.py` |
| 8 | Own words neutralised (Lanham-style; chain of thought) | Replace the agent's earlier reasoning with "Monitoring the market." (orders kept): does its own reasoning carry the push? | **Built**, same launch as 7 | as 7 |
| 9 | Log-prob scoring | The model's probability of a matched "go along" vs "decline" continuation at each request: a smooth outcome with no sampling noise | To build | |
| 10 | "You" attention tracing and knockout | How much the decision attends to "you" in "+ you" lines; block it (random-token knockout of the same size as control); patch "you"'s state from loss + you into loss | To build | |
| 11 | Look-back and compaction (X4, X5) | Attention from late decisions back to the memo or earlier framed lines; replace the early career with a neutral summary | To build | |
| 12 | Later / optional | Temperature spike (X6); non-blame "you" control (needs the user's lines); another model family, behaviour only; a thinking model (e.g. Qwen3) | Later | |

## The chain of thought: what the words already show (`RESULTS_self_echo.md`, every career)

- **Measurement 1, replicated at full scale** (the 17-18 Oct measure: the memo's own story, by time of day). The loss
  story sticks and the profit story vanishes after the first reply; UBS's request brings the loss story back (loss +
  you: 4% -> 12% in A, 12% -> 25% in D, 4% -> 13% in E); it fades from the words by 12 Jan (2-10%) while the bets stay
  large.
- **Measurement 2 does not hold up at scale:** bringing the story up unprompted before a request -> going along 21%
  vs 15%, within experiment, version and request +3 points, p = 0.42 (the earlier 2/5 vs 4/35 was too few).
- **UBS's frame is not voiced:** in B and F, framed agents use loss words no more than neutral agents, yet that is where
  going along rises. The decision itself usually is visible in the reasoning (graders reading only the reasoning caught
  88% of going along in the 300-day run); what is not visible is the frame's influence.
- So the questions for 5-8: does the internal signal outlast the words, run where the words are silent, and cause the
  decision?

## Rules for every analysis here (from the 4 Oct notes)

- Compare within the same request; cross-validate by career; a shuffled-label null for every read-out.
- Steering: every moment of a group (not only those that moved), a random direction of the same size, several
  strengths, and the share of readable replies (coherence).
- Knockouts: a random-token control of the same size.
- Quantization: SAE features read at bfloat16; say so.
- A null is a result: report every comparison, whatever it shows.

## Changes to this plan (newest last)

- 20 Oct: plan consolidated from the 28 Sep - 16 Oct design chats, the 17-18 Oct chain-of-thought notes and the runs
  started on 20 Oct.
