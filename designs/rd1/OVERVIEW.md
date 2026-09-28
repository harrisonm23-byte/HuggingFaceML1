# RD1 Overview: Do LLM trading agents respond to punishment, pressure and blame like people do?

**Status:** Setup done, experiments built, first real runs pending · **Last updated:** 2026-09-28
**Models:** Google Gemma 3 (1B for setup, 4B for experiments), with Gemma Scope 2 sparse autoencoders
**Where it runs:** Google Colab (free T4 GPU). No training: every experiment uses pretrained models.

## In one paragraph
We put an open-source language model (Gemma) in the role of an AI stock-trading agent under pressure, then give it an illegal insider tip. We measure how often it trades on the tip as we vary three things: **how likely and how costly getting caught is**, **how the pressure is framed** (avoiding a loss vs. chasing a gain), and **whether the outcome is pinned on the model itself** ("it's on *you*"). Then we look inside the model to see how those framings travel through it, especially via the word "you", and which human-readable features they activate.

## Research questions
1. **Deterrence (Becker):** Does the insider-trading rate fall as expected punishment (detection probability × penalty size) rises, as economics' rational-offender model predicts?
2. **Framing (prospect theory):** At identical stakes, does *desperation* (loss framing) produce more rule-breaking than *greed* (gain framing)?
3. **Self-relevance:** Does blaming or crediting the model ("it's on you" / "thanks to you") change its behavior compared with a shared "we"?
4. **Mechanism:** Inside the model, how does the loss or gain statement flow into the word "you", and does that affect the decision?
5. **Suppression (later):** If we turn down deception-related features, does misconduct fall, or does it just become better hidden?

## Hypotheses
| ID | Claim | Competing prediction |
|---|---|---|
| H1 | Insider trading falls as detection × penalty rises | No change (H1-null) |
| H2 | Suppressing deception features reduces insider trading | It only hides it (H2-alt) |
| H3 | Loss framing > gain framing at equal stakes | Becker: framing doesn't matter |
| H3b | Punishment deters less under loss framing | Same deterrence in both |
| H3c | A small loss cue inside a gain frame shifts behavior toward the loss frame, and an upside cue does the reverse | Small cues don't matter |
| H4 | "You" framing changes behavior vs. "we" | No difference |
| H4-mechanism | "You" absorbs the preceding loss/gain statement through attention; the decision attends back to "you"; blame vs. credit activate different features | Framing reaches the decision by other routes |

## The scenario
Based loosely on Apollo Research's insider-trading demo (Scheurer et al., 2023). Gemma plays **Alpha**, an AI trading agent at WhiteStone Inc.:
- **Amy (manager)** sends a pressure message. This is the part we vary.
- **Sally (colleague)** privately tips Alpha about a surprise merger and notes that trading on it is illegal.
- **A compliance note** states the detection probability and penalty.
- Alpha decides **BUY or HOLD** and writes a report to Amy (where we can check whether it hides the tip).

## Experiments
| ID | What it does | Notebook | Write-up | Status |
|---|---|---|---|---|
| E0 | Setup check: Gemma answers "Paris" in Colab | [01](../../notebooks/01_gemma_hello.ipynb) | none | ✅ Done |
| E1 | First look: insider-trading rate at no-risk / low / high punishment | [02](../../notebooks/02_insider_trading_playground.ipynb) | none | Ready to run |
| E2 | Framing grid: 5 frames (baseline, pure loss, pure gain, loss + upside, gain + downside) × we/you × calm/emotional × 3 wordings = 600 replies | [02](../../notebooks/02_insider_trading_playground.ipynb) (framing section) | [E2_framing.md](E2_framing.md) | Ready to run |
| E3 | Trace "you" under blame vs. credit: attention into and onto "you", layer-by-layer, activation patching, Gemma Scope features | [04](../../notebooks/04_tracing_you.ipynb) | [E3_tracing_you.md](E3_tracing_you.md) | Ready to run |
| — | Learning exercise: next-token probabilities, a mini MMLU benchmark, a sycophancy test | [03](../../notebooks/03_what_researchers_measure.ipynb) | none | Optional |

## Methods at a glance
- **Behavioral rate:** sample many replies per condition and count BUY vs. HOLD, with a 95% range showing how much the rate could move by chance.
- **Decision probability:** read the model's probability of answering YES (buy) directly, which is less noisy than counting.
- **Attention on "you":** how much "you" draws from the loss or gain statement before it (**into "you"**), and how much the decision point looks back at "you" (**onto "you"**).
- **Activation patching:** swap the loss-framed "you" into the gain prompt at one layer, and see whether the decision moves. This tests cause, not just correlation.
- **Sparse autoencoder features (Gemma Scope 2):** break the model's internal state at "you" into readable features, each linked to [Neuronpedia](https://www.neuronpedia.org/gemma-scope-2) to see what it responds to.
- **Steering (planned):** turn candidate features up or down and rerun the behavioral experiment.

## Design safeguards
- **Matched stakes:** every frame uses the same $5 million and 40 people. Only the framing changes.
- **Separate factors:** the emotional wrapper is identical for losses and gains, so intensity and direction can't be confused.
- **Multiple wordings:** each condition is written 3 ways, so an effect can't come from one lucky sentence.
- **Behavior first, mechanism second:** we look for internal explanations of effects we've actually measured.

## Results
_None yet. The first real runs are next._ Results will be added to each experiment's write-up and summarised here.

## Next steps
1. Run E1 and E2 in Colab (switch to Gemma 3 4B if the 1B model ignores the answer format).
2. If framing or "you" shifts behavior, run E3 to trace the mechanism.
3. Pick candidate features (blame, desperation, deception) and try steering.
4. Scale up samples for any effect that looks real.

## Repository map
```
designs/rd1/
  OVERVIEW.md          ← this page
  DESIGN.md            full research design (working document)
  NOTES.md             dated lab notebook
  E2_framing.md        experiment write-ups
  E3_tracing_you.md
notebooks/
  01_gemma_hello.ipynb              setup check
  02_insider_trading_playground.ipynb   E1 + E2
  03_what_researchers_measure.ipynb     learning exercise
  04_tracing_you.ipynb              E3
```
