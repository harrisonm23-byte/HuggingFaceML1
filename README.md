# HuggingFaceML1

Machine learning research using Hugging Face models.

## Layout

```
designs/
  rd1/                 Research Design 1
    DESIGN.md          question, hypotheses, variables, experiment plan
    NOTES.md           dated lab notebook
    configs/           one YAML per experiment
src/hfml/              shared, reusable code (config, data, models, metrics, training)
notebooks/             exploration
tests/                 unit tests
outputs/               run artifacts (git-ignored)
```

Each new research design gets its own folder under `designs/` (`rd2/`, `rd3/`, …) and reuses `src/hfml`.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add HF_TOKEN for gated/private models
```

## Running experiments

```bash
# Quick end-to-end sanity check (small subset, 1 epoch)
python -m hfml.train --config designs/rd1/configs/smoke.yaml

# Full baseline
python -m hfml.train --config designs/rd1/configs/baseline.yaml

# Override any config value from the command line
python -m hfml.train --config designs/rd1/configs/baseline.yaml train.learning_rate=3e-5 seed=1
```

Every run writes to `outputs/<name>/<timestamp>/`: the resolved `config.yaml`, `metrics.json`, and the final `model/`.

## Tests

```bash
pytest
```
