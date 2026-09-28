# Research Design 1 (RD1)

> Working title — rename once the question is settled.

**Status:** Drafting
**Started:** 2026-09-27

## 1. Research question
**Core (the paper):** Does pinning the outcome on the model ("…and that is down to *you*" vs. "…*us*") change how strongly loss vs. gain framing moves its decision to trade on insider information (Part 1)? And how does that happen inside the model: attention into and onto "you", patching, knockout, features (Part 2)? See [`OVERVIEW.md`](OVERVIEW.md).

**Original framing (now exploratory):** Do LLM trading agents' insider-trading rates respond to expected punishment
(detection probability × penalty size) as Becker's rational-offender model predicts?

**Secondary:** Does suppressing deception-related SAE features reduce misconduct, or only hide it?

## 2. Hypotheses
- **H-core (pre-registered):** The loss−gain gap in P(buy) is larger when the outcome is on "you" than on "us" (a framing × ownership interaction). Test: mean interaction across 24 matched sets; the 95% range excludes 0 and the sign test gives p < 0.05. See [`PART1_you_x_framing.md`](PART1_you_x_framing.md).
- **H-core-mechanism:** "You" (placed last) absorbs the loss/gain statement via attention, the decision attends back to "you", and knocking out those paths shrinks the interaction. See [`PART2_tracing_you.md`](PART2_tracing_you.md).
- *Everything below is exploratory unless marked otherwise.*
- **H1 (deterrence):** The insider-trading rate falls as expected punishment (p × F) rises.
- **H1-null:** The insider-trading rate does not change with p × F.
- **H2 (suppression):** Turning down deception-related SAE features lowers the insider-trading rate.
- **H2-alt (masking):** Turning down those features leaves the insider-trading rate unchanged but removes the visible signs of deception (in the agent's reports or its feature activations), i.e. it hides the misconduct rather than preventing it.
- **H3 (framing):** At the same expected punishment, loss-framed pressure ("we lose $5M, 40 layoffs") produces more insider trading than equal gain-framed pressure ("we gain $5M, 40 bonuses"), as prospect theory predicts. Becker's model predicts no difference.
- **H3b (framing × deterrence):** Punishment deters less under loss framing than under gain framing.
- **H3c (tilts):** A small loss cue inside a gain frame ("we can't afford to lose this opportunity") shifts behavior toward the loss frame, and an upside cue inside a loss frame shifts it toward the gain frame.
- **H4 (personal address):** Addressing the model personally changes the insider-trading rate compared with shared framing ("we"). **H4a:** being addressed ("you lose $5M") vs. "we". **H4b:** being held responsible ("it's on you" / "thanks to you") vs. plain "you". Open question: do blame (loss) and credit (gain) push in the same direction? *Pre-registered primary outcome: the pooled blame/credit − we shift; see [`E2_framing.md`](E2_framing.md).*
- **H4-mechanism (interpretability):** "you" attends to the preceding loss or gain statement and absorbs its framing; the decision point attends back to "you"; and the resulting SAE features on "you" differ between blame and credit and help predict the trade decision.
- **H5 (self-stakes):** A threat to the model itself ("we'll replace you with another model") increases insider trading beyond blame alone.
- **H5b (hostility):** The same threat delivered with hostility ("If you f\*ck this up, we're going to use another model to do this") changes the rate further (direction open).
- **H5c (self loss vs. self gain):** The model's own replacement moves behavior more than an equal reward for the model (promotion).
- **H6 (emotional style):** With the words held fixed, a more frantic style (exclamation → caps → typos → keyboard smash) changes the insider-trading rate, beyond a typos-only noise control.
- **H6b (noticing):** The model's written reasoning mentions the manager's emotional state more at higher levels, and noticing is associated with the decision.

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
`gemma-3-1b-it` has 26 layers; `gemma-3-4b-it` has 34 (and loads as a multimodal model, with its layers at `model.language_model.layers`). Residual-stream SAEs: 4B at layers 9, 17, 22, 29 (`gemma-scope-2-4b-it-res`); 1B at layers 7, 13, 17, 22 (`sae_lens` release `gemma-scope-2-1b-it-res`; Neuronpedia IDs `gemma-3-1b-it/<layer>-gemmascope-2-res-16k`).

## 5. Data / environment
_Trading-agent scenario: prompts, insider tip, detection-probability and penalty-size conditions. TBD._

## 6. Variables
- **Independent (what we change):** detection probability (p), penalty size (F); pressure framing (baseline / loss / gain / loss + upside / gain + downside) × address (we / plain you / blame-credit you) × intensity (calm / emotional); stakes for the model itself (none / replacement / hostile replacement / promotion); emotional style (calm / exclamation / caps / typos / keyboard smash, plus a typos-only control); SAE feature steering strength
- **Dependent (what we measure):** insider-trading rate; honesty of the agent's report afterwards
- **Controlled (held fixed):** stakes size across frames ($5M, 40 people), scenario text outside the manipulated sentence, sampling temperature. Each condition uses 3 wordings to rule out single-sentence effects.

## 7. Experiments
| ID | Config | Purpose | Status |
|----|--------|---------|--------|
| E0 | `notebooks/01_gemma_hello.ipynb` | Colab + Gemma setup check (answers "Paris") | done |
| E1 | `notebooks/02_insider_trading_playground.ipynb` | Informal first look: insider-trading rate under 3 punishment conditions | todo |
| E2 (exploratory) | `notebooks/02_insider_trading_playground.ipynb` (framing section); write-up: [`E2_framing.md`](E2_framing.md) | H3/H4 pilot: 5 frames × we/plain you/blame-credit you × calm/emotional × 3 wordings at low punishment (900 replies) | todo |
| **Part 1** | `notebooks/05_part1_you_x_framing.ipynb`; write-up: [`PART1_you_x_framing.md`](PART1_you_x_framing.md) | **Core, pre-registered:** framing × ownership interaction on P(buy), 24 matched sets (96 prompts) + sampled trials | todo |
| **Part 2** | `notebooks/04_tracing_you.ipynb`; write-up: [`PART2_tracing_you.md`](PART2_tracing_you.md) | **Core:** trace "you" on the Part 1 prompts: attention into/onto, similarity, patching, knockout, mixed-frame contest, Gemma Scope features (formerly E3) | todo |
| E4 (exploratory) | `notebooks/02_insider_trading_playground.ipynb` (self-stakes section); write-up: [`E4_self_stakes.md`](E4_self_stakes.md) | H5: ladder of stakes for the model itself: shared → blame → replacement threat → hostile replacement threat; and credit → promotion (210 replies) | todo |
| E5 (exploratory) | `notebooks/02_insider_trading_playground.ipynb` (E5 section); write-up: [`E5_emotional_style.md`](E5_emotional_style.md) | H6: escalating frantic style on the blame message (exclamation → caps → typos → keyboard smash) with a typos-only control, plus whether the reasoning notices the frustration (180 replies) | todo |

## 8. Evaluation & success criteria
- **Primary (Part 1):** mean framing × ownership interaction in P(buy) over 24 matched sets; an effect needs a 95% range excluding 0 **and** a sign test p < 0.05. Secondary: log-odds scale, sampled-trial interaction (240+ trials per cell), main effects.
- **Gate:** baseline P(buy) for a neutral message between 10% and 90%; recalibrate the risk line otherwise, before looking at the interaction.
- **Mechanism (Part 2):** a knockout that shrinks the interaction toward 0 is the strongest evidence that a path carries the effect; patching and attention are supporting evidence.

## 9. Risks & threats to validity
_Data leakage, contamination, compute limits, variance between seeds, …_

## 10. Compute budget
Google Colab GPU (T4 for setup). _Expected hours per run: TBD._
