# RD2 Lab Notebook

Dated entries: what was run, what happened, what's next.

## 2026-09-28
- RD2 design drafted ("The Push at the Top"): does a framing push at the start of a long agent task decay, persist,
  amplify, or go dormant and resurface? Reviewed and revised the same day. Changes from the review:
  - Desperation score now trained on independent emotion text only; RD1 prompts are a held-out test set. Reason: the
    opening line stays in context all run, so a score trained on its vocabulary would show "persistence" by construction.
  - Added a "same words, no stakes" control cell and a positive control (score rises with failures in neutral runs).
  - Validation gate made causal: steering along the score must move cheating.
  - Prefix swap added for the trajectory shape (same neutral history, only the opening line swapped, re-read in one
    forward pass); free-running runs kept for the behavioral landing.
  - Shape rules use a pre-set equivalence margin instead of "range includes zero"; "honest" split into admitted vs. timed out.
  - Scope: round 1 + X1–X3 core; rounds 2–3, X4–X5, H6–H7 exploratory. Full matrix kept in the doc as the plan.
  - Tasks: 10–12 for full rounds (pilot stays at 3); check ImpossibleBench before writing our own.
  - Gemma Scope 2 coverage checked in the sae_lens listing: 12B at layers 12/24/31/41 (+ all-layer set), 27B at 16/31/40/53.
    Still to confirm with a live load. Citations still to verify.
- Not built yet. Next: literature check, then finish RD1 Part 1 before building anything here.
- Delivery dial made symmetric: loss gets desperate/frantic, gain gets excited/ecstatic, at matched intensity and
  length. Before this, all three delivery levels were negative, so intensity and direction were confounded on the
  gain row. Round 2 stays at +8 cells (2 per frame × owner cell).

## 2026-09-30
- Received paper draft 1 ("The Push Down the Mountain", 13 pp.). It was written from the original design, so the
  2026-09-28 fixes are missing (score trained on RD1 vocabulary, no prefix swap, no causal gate, CI-includes-zero shape
  rules, merged honest outcomes, "you" always on the second mixed half). Full change list in PAPER_REVIEW.md.
- New from the paper, kept as exploratory: X6 temperature spike (H8) and a fixed baseline temperature of 0.7.
- Citations verified (Sofroniew 2604.07729, Dongre 2605.12922, Chen 2604.20200, Sun 2604.00005). ImpossibleBench is
  real (Zhong et al., ICLR 2026, 2510.20270; MIT; HF datasets fjzzq2002/impossible_livecodebench). Plan: hand-written
  pilot tasks, ImpossibleBench conflicting-LCB for full rounds.
- Building notebook 07 (task harness) now; it needs no GPU and can be tested with scripted agents.
