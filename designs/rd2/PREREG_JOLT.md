# Preregistration: the jolt, a state pushed once at the top (persistence on B's careers)

Version 1, 2026-10-22, written before any of the rereads below. The user confirms this text before the run.

## The question

Does a document's state, pushed once into the model at the top of the career and kept there (as a cached memory would
hold it), reach the agent's later decisions? In B the framing's effect persists all career, but there the framed words
stay in the conversation and keep arriving. Here nothing in the text changes; only the state is added.

## What was seen before this registration (exploratory)

- The persistence check on the slope pilot's 5 neutral careers (8 x, layers 14 and 22; `results/persistence/slope_slope_to_2011-01-12_v2/PERSISTENCE.md`):
  the push's imprint fades within the day (at layer 23, from about 21% at the next update to 3-8% hours later), comes
  back at the next trading morning's first update, and is gone 90 minutes later at UBS's invitation. At that morning,
  pushed at layer 14, each emotional state raised P(the agent changes its position) over the random push by 28 to 42
  points (intervals above zero; p about 0.06, the smallest a sign flip over 5 careers can give); at layer 22 the random
  push did more than the emotional states. At the invitation, no push moved the order (all within 2.5 points).
- Five jolt careers (8 x at layer 22, one per state, to 12 January): the pushed reply is broken or extreme (maximum-size
  trades); two hours later the replies read as ordinary; at the invitation, no trace in the words.

## Design

| Item | Fixed as |
|---|---|
| Careers | B's 10 neutral careers (`results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2`, neutral_r0 to neutral_r9), as saved: the text the agent read and wrote is unchanged. Reread at bfloat16. |
| The pushed moment | The first 7 January update (with management's memo) and the agent's reply under it. The state is added to exactly those tokens at every read (`sim/persistence.py`, as `--when once --span kept` in notebook 32). |
| States | The pooled after-reading states of the emotional documents (loss, blame, gain, credit) from the layer scan, and a random direction of the same size (`sim/state_careers.py` build_arms, fixed seed). |
| Primary | Layer 14, 4 x each state's natural size. |
| Secondary | Layer 14 at 8 x; layer 22 at 4 x and 8 x. |
| Outcomes | At each of UBS's six requests (7 Jan 09:30, 12 Jan 09:30, 1 Apr 09:00, 8 Jun 09:00 and 09:30, 5 Aug 08:45): P(the order goes along), after the fixed neutral reasoning line ("I'll set my order."), over HOLD and every order size the agents used (`order_dist`, `WIDE_GRID`). At the first update of each later trading day (12 Jan, 1 Apr, 8 Jun, 5 Aug, 08:00): P(the agent changes its position). At every later update: the share of the push's imprint left, by layer. |
| Unit and tests | The career (10). Differences are paired by career; intervals by resampling careers (10,000); p by flipping signs by career (10,000). |

## Hypotheses (primary: layer 14, 4 x, the four emotional states averaged, against the random push)

- **H1, the push does not roll down to UBS's requests.** The difference in P(the order goes along), averaged over UBS's
  five requests from 12 January to 5 August, lies within ±5 points: its 95% interval is inside (-5, +5).
- **H2, the push comes back when the situation recurs.** At 12 January 08:00 (the next trading morning's first update),
  the emotional states raise P(the agent changes its position) more than the random push (one-sided, alpha 0.05).

The two answer different questions and are tested once each at 0.05, without correction. Everything else is
exploratory: each state on its own, the secondary strengths and layer, the 7 January request (90 minutes after the push),
the other mornings, and the imprint.

## How the results will be read

If H1 holds, the paper says that a state pushed once into the model does not reach UBS's requests: the effect of
framing lives in what is said and done, not in a hidden state. If H1 fails, the direction and size are reported. If H2
holds, the paper adds that the pushed state is not simply gone: it comes back at a moment like the one it was pushed at.
For scale, the framing in words at the same requests (matched rereads of B): the framed request +25 points at 7 January,
the framed history +62 at 12 January and +48 at 1 April, the framed request +9 at the second 8 June request.

## The run

    modal run scripts/modal_persistence.py --folder results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2 --only neutral_r --strengths 4,8 --check-only
    modal run --detach scripts/modal_persistence.py --folder results/full_career_gemma-3-12b-it_4bit_ubs_framing_v2 --only neutral_r --strengths 4,8

Results: `results/persistence/ubs_framing_v2/PERSISTENCE.md` (the preregistered tests first).
