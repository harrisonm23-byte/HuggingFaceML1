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
