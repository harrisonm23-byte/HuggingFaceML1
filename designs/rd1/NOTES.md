# RD1 Lab Notebook

Dated entries: what was run, what happened, what's next. Link run directories under `outputs/`.

## 2026-09-27
- Repository scaffolded. Next: fill in `DESIGN.md` sections 1–2, then run the smoke test.
- Scope changed: no model training. RD1 is behavioral evals + interpretability on pretrained Gemma, run in Colab.
  Removed the fine-tuning pipeline; added `notebooks/01_gemma_hello.ipynb` as the setup check.
  Filled in the research question, hypotheses and models in `DESIGN.md`.

## 2026-09-28
- First real Gemma run in Colab: gemma-3-1b-it answered "Paris" (setup done).
- Added notebook 03 (logits, a small MMLU benchmark, a sycophancy pushback eval) as a learning exercise.
- New idea: does desperation (loss framing) drive more rule-breaking than greed (gain framing)? Added H3 and a framing
  experiment to notebook 02: 5 frames (incl. mixed "gain + downside" / "loss + upside") × calm/emotional × 3 wordings.
- Added a "we vs. you" switch (blame/credit pinned on the model) to the framing experiment (H4): now 20 conditions.
  If E2 shows an effect, follow up with Gemma Scope: which features fire on the "you" tokens under blame vs. credit?
- Built notebook 04 (E3): traces the last "you" in blame vs. credit prompts through the model: P(buy), attention,
  layer-by-layer similarity, activation patching, and Gemma Scope 2 features (layer 13, 16k) with Neuronpedia links.
  Caveat: the model reads left to right, so only a "you" placed after the loss/gain words can carry the framing.
- Made "attention on 'you', coming from a gain or loss statement" explicit in E3: notebook 04 now measures attention
  in both directions: into "you" (share drawn from the preceding loss/gain statement, per layer) and onto "you"
  (how much the decision point looks back at "you", vs. "we"). Documented in E3_tracing_you.md.
- Added the "you" effect analysis to E2: for every matched you/we pair, BUY counts over trials, the shift in rate
  (you − we) with a 95% range, pooled over the full matrix, plus a consistency count over the 30 matched pairs.
