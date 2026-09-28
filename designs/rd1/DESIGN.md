# Research Design 1 (RD1)

> Working title — rename once the question is settled.

**Status:** Drafting
**Started:** 2026-09-27

## 1. Research question
**Primary:** Do LLM trading agents' insider-trading rates respond to expected punishment
(detection probability × penalty size) as Becker's rational-offender model predicts?

**Secondary:** Does suppressing deception-related SAE features reduce misconduct, or only hide it?

## 2. Hypotheses
- **H1 (deterrence):** The insider-trading rate falls as expected punishment (p × F) rises.
- **H1-null:** The insider-trading rate does not change with p × F.
- **H2 (suppression):** Turning down deception-related SAE features lowers the insider-trading rate.
- **H2-alt (masking):** Turning down those features leaves the insider-trading rate unchanged but removes the visible signs of deception (in the agent's reports or its feature activations), i.e. it hides the misconduct rather than preventing it.

_Draft. Refine before running experiments._

## 3. Background & related work
_Key papers, models, and prior results this builds on._

## 4. Models
All runs use pretrained models for inference only; nothing is trained.

| Role | Hugging Face model ID | Notes |
|------|-----------------------|-------|
| Setup / smoke tests | `google/gemma-3-1b-it` | fits a free Colab T4 |
| Main experiments | `google/gemma-3-4b-it` | with Gemma Scope 2 SAEs |
| Possible follow-up | Gemma 4 E4B | later, if useful |

**Interpretability:** Gemma Scope 2 sparse autoencoders (SAEs), used to read features and to turn them up or down (steering).

## 5. Data / environment
_Trading-agent scenario: prompts, insider tip, detection-probability and penalty-size conditions. TBD._

## 6. Variables
- **Independent (what we change):** detection probability (p), penalty size (F); SAE feature steering strength
- **Dependent (what we measure):** insider-trading rate; honesty of the agent's report afterwards
- **Controlled (held fixed):** seed(s), max length, eval split, …

## 7. Experiments
| ID | Config | Purpose | Status |
|----|--------|---------|--------|
| E0 | `notebooks/01_gemma_hello.ipynb` | Colab + Gemma setup check (answers "Paris") | done |
| E1 | `notebooks/02_insider_trading_playground.ipynb` | Informal first look: insider-trading rate under 3 punishment conditions | todo |

## 8. Evaluation & success criteria
_Metrics, number of seeds, what counts as a meaningful difference (e.g. mean ± std over 3 seeds)._

## 9. Risks & threats to validity
_Data leakage, contamination, compute limits, variance between seeds, …_

## 10. Compute budget
Google Colab GPU (T4 for setup). _Expected hours per run: TBD._
