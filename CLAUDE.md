# Project notes for Claude

- ML research repo built on Hugging Face `transformers` + `datasets`.
- Shared code lives in `src/hfml`; each research design lives in `designs/rdN/` with its own `DESIGN.md`, `NOTES.md`, and `configs/`.
- Experiments are config-driven: add a YAML under `designs/rdN/configs/` rather than hard-coding values.
- Run `pytest` before committing. Never commit `.env`, checkpoints, or anything in `outputs/`.
