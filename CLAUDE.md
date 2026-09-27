# Project notes for Claude

- Research repo: behavioral evals + interpretability on **pretrained** open models (Gemma 3, Gemma Scope 2 SAEs). No model training or fine-tuning.
- Experiments run in **Google Colab** on a GPU (T4 for setup). This cloud environment has no GPU, so don't try to run models here.
- Each research design lives in `designs/rdN/` with its own `DESIGN.md` and `NOTES.md`. Notebooks live in `notebooks/`, numbered in run order.
- Notebooks: keep code minimal with plain-English comments. Read the HF token with `google.colab.userdata.get('HF_TOKEN')`, never hard-code it.
- Never commit `.env`, tokens, or large model outputs.
