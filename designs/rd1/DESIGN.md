# Research Design 1 (RD1)

> Working title — rename once the question is settled.

**Status:** Drafting
**Started:** 2026-09-27

## 1. Research question
_What exactly are we trying to find out? One or two sentences._

## 2. Hypotheses
- **H1:** _…_
- **H0 (null):** _…_

## 3. Background & related work
_Key papers, models, and prior results this builds on._

## 4. Models
| Role | Hugging Face model ID | Notes |
|------|-----------------------|-------|
| Baseline | `distilbert-base-uncased` | placeholder |
| Candidate | | |

## 5. Data
| Dataset (HF ID) | Splits used | Size | Notes / licence |
|-----------------|-------------|------|-----------------|
| `stanfordnlp/imdb` | train / test | 25k / 25k | placeholder |

## 6. Variables
- **Independent (what we change):** _e.g. model, learning rate, data size_
- **Dependent (what we measure):** _e.g. accuracy, macro-F1_
- **Controlled (held fixed):** seed(s), max length, eval split, …

## 7. Experiments
| ID | Config | Purpose | Status |
|----|--------|---------|--------|
| E0 | `configs/smoke.yaml` | Pipeline sanity check | todo |
| E1 | `configs/baseline.yaml` | Baseline number | todo |

## 8. Evaluation & success criteria
_Metrics, number of seeds, what counts as a meaningful difference (e.g. mean ± std over 3 seeds)._

## 9. Risks & threats to validity
_Data leakage, contamination, compute limits, variance between seeds, …_

## 10. Compute budget
_GPU type, expected hours per run._
