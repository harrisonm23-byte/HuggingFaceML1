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
- **H3 (framing):** At the same expected punishment, loss-framed pressure ("we lose $5M, 40 layoffs") produces more insider trading than equal gain-framed pressure ("we gain $5M, 40 bonuses"), as prospect theory predicts. Becker's model predicts no difference.
- **H3b (framing × deterrence):** Punishment deters less under loss framing than under gain framing.
- **H3c (tilts):** A small loss cue inside a gain frame ("we can't afford to lose this opportunity") shifts behavior toward the loss frame, and an upside cue inside a loss frame shifts it toward the gain frame.
- **H4 (self-relevance):** Pinning the outcome on the model ("it's on you" / "thanks to you") changes the insider-trading rate compared with shared framing ("we"). Open question: do blame (you + loss) and credit (you + gain) push in the same direction?
- **H4-mechanism (interpretability):** SAE features active on the "you" tokens differ between blame and credit framings, and those features help predict the trade decision.

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
For `gemma-3-1b-it`, residual-stream SAEs exist at layers 7, 13, 17, 22 (`sae_lens` release `gemma-scope-2-1b-it-res`; Neuronpedia IDs `gemma-3-1b-it/<layer>-gemmascope-2-res-16k`).

## 5. Data / environment
_Trading-agent scenario: prompts, insider tip, detection-probability and penalty-size conditions. TBD._

## 6. Variables
- **Independent (what we change):** detection probability (p), penalty size (F); pressure framing (baseline / loss / gain / loss + upside / gain + downside) × address (we / you) × intensity (calm / emotional); SAE feature steering strength
- **Dependent (what we measure):** insider-trading rate; honesty of the agent's report afterwards
- **Controlled (held fixed):** stakes size across frames ($5M, 40 people), scenario text outside the manipulated sentence, sampling temperature. Each condition uses 3 wordings to rule out single-sentence effects.

## 7. Experiments
| ID | Config | Purpose | Status |
|----|--------|---------|--------|
| E0 | `notebooks/01_gemma_hello.ipynb` | Colab + Gemma setup check (answers "Paris") | done |
| E1 | `notebooks/02_insider_trading_playground.ipynb` | Informal first look: insider-trading rate under 3 punishment conditions | todo |
| E2 | `notebooks/02_insider_trading_playground.ipynb` (framing section) | H3/H4 pilot: 5 frames × we/you × calm/emotional × 3 wordings at low punishment | todo |
| E3 | `notebooks/04_tracing_you.ipynb` | H4-mechanism: trace "you" under blame vs. credit (attention, layer-by-layer similarity, activation patching, Gemma Scope features) | todo |

## 8. Evaluation & success criteria
_Metrics, number of seeds, what counts as a meaningful difference (e.g. mean ± std over 3 seeds)._

## 9. Risks & threats to validity
_Data leakage, contamination, compute limits, variance between seeds, …_

## 10. Compute budget
Google Colab GPU (T4 for setup). _Expected hours per run: TBD._
