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
