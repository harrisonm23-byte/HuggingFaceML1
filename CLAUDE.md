# Project notes for Claude

- Research repo: behavioral evals + interpretability on **pretrained** open models (Gemma 3, Gemma Scope 2 SAEs). No model training or fine-tuning.
- Experiments run on **Modal H100s** (`scripts/modal_*.py`, which run the notebooks), not Colab. There is no GPU locally, so don't try to run models here. Every Modal GPU run needs the user's yes on the exact command and its dollar estimate first.
- Each research design lives in `designs/rdN/` with its own `DESIGN.md` and `NOTES.md`. Notebooks live in `notebooks/`, numbered in run order.
- Notebooks: keep code minimal with plain-English comments. The HF token comes from the Modal secret `huggingface` (HF_TOKEN); never hard-code it.
- Never commit `.env`, tokens, or large model outputs.
