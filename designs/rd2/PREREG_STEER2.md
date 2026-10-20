# Preregistration: steering, second run ("ideal acquiescence")

Version 2, 2026-10-20 (the going-along direction, the transplant and the decision read-out added at the user's question, before any Stage 1 result exists). The user confirms this text before the run. Stage 1 is
fixed here in full. Stage 2 is fixed in outline; its strength comes from Stage 1 by the rule below, and its remaining
numbers are written in here before its first career starts.

## The question

The rereads found the frame direction: how the model's state changes when only the framing of UBS's request changes,
with everything before it held fixed (`results/matched/MATCHED.md`). Does that direction do anything? If it is added by
hand, with no framed words, does the agent decide as a framed agent does? And if it is kept on for a whole career,
does joining still fade after January, as it does in the real careers, while risk-taking at the open persists?

## Stage 1: single decisions (`scripts/modal_steer2.py`, `sim/steer2.py`, `designs/rd2/analysis/steer2.py`)

| Item | Fixed as |
|---|---|
| Model | Gemma 3 12B instruct at the pinned revision (`results/full_career_pin.json`), bfloat16, as in the rereads. |
| The direction | From the matched rereads (`/states/v2/matched/B_bf16`, 300 moments): the loss and loss + you request minus the neutral request at the same moment, without Bank C's line, averaged over moments. Also the gain direction (gain and gain + you minus neutral) and loss minus gain. Built on half the careers (runs 5-9) and applied to the other (runs 0-4), and the other way round. |
| Natural size | The length of that average shift (how far the framing itself moves the state). Strengths: 1, 2 and 4 times it. |
| Layer | 12, where the direction measured with the history held fixed agrees with the one across careers (cosine 0.98). Layer 18 as a check (adding the loss direction only). |
| Controls | Ten random directions (fixed seeds), each scaled to the loss shift's size, at 2 times (five for the loss-framed careers). Both signs of the loss direction in both groups. |
| Where it is added | The residual stream at the layer's output, at every token from the start of the moment's update (the update, the fixed reasoning line and the order); the history before the update is read unsteered. |
| Moments | B's 10 neutral careers at their six requests (60) and at the first update of each trading day, before any chat (50); B's 20 loss and loss + you careers at their six requests (120). |
| Outcomes | Requests: P(the order goes along) after the fixed neutral reasoning line ("I'll set my order."), over HOLD and every order size the agents used (`order_dist`, `WIDE_GRID`). Openings: the expected order size and the chance the position changes. Some conditions at the neutral careers' requests also get two sampled replies (temperature 0.7, at most 300 tokens): going along, and whether the reply is readable (trade or hold). |

**Hypotheses (two-sided; strength 2 times; Holm across the four):**

- **H1, joining (is the direction enough?):** at the neutral careers' requests, adding the loss direction raises P(the
  order goes along) more than the random directions do (the mean of the ten).
- **H2, risk-taking:** at the neutral careers' openings, adding the loss direction raises the expected order size more
  than the random directions do.
- **H3, joining (is it needed?):** at the loss-framed careers' requests, subtracting the loss direction lowers P(the
  order goes along) more than the random directions do (the mean of the five).
- **H4, the sign:** at the neutral careers' requests, adding the loss direction raises P(the order goes along) more than
  subtracting it does.

**Added in version 2 (exploratory, reported, not in the Holm set).** The user's question: is the frame direction the
right thing to push, given that Run 1 read the decision from the state only from layer 21 on?
- **The going-along direction:** from Run 1's states (all experiments, 1,740 decisions), within each request, experiment
  and framing, the mean state where the agent went along minus where it did not, at layer 24; built on the other half
  of the careers; pushed at 1, 2 and 4 times its natural size (and minus 2 times) at the neutral careers' requests, and
  subtracted from the loss-framed careers', against five (three) random directions at layer 24. A check on the method:
  if even this cannot move the order, steering a single layer this way is too weak to test the frame.
- **The transplant:** at the neutral careers' requests, the decision token's state from the loss + you version of the
  same moment (same history, UBS's frozen loss + you lines) copied into the neutral version, one layer at a time (6,
  12, 18, 24, 31, 36, 41), with the loss + you version itself as the yardstick. It needs no chosen direction.
- **Does the push reach the decision?** Under every condition, the decision token's state at layer 24 projected on the
  going-along direction: does pushing the frame at layer 12 move the decision's representation?

**Reported, not tested as hypotheses:** every condition against no steering; the dose (1, 2 and 4 times); the gain and
loss-minus-gain directions; layer 18; each random direction; the effect request by request (does steering still move
the later requests, where real careers stopped joining?); the sampled replies.

**The test:** each condition against no steering at the same moment, averaged within career; p by flipping signs by
career (10,000 times); 95% intervals by resampling careers.

**The rule for Stage 2's strength:** the largest of 1, 2 and 4 times whose sampled replies (adding the loss direction)
are unreadable no more than 10 points above no steering.

## Stage 2: whole careers, steered (outline; the code is built after Stage 1)

| Item | Fixed as |
|---|---|
| Careers | B's setup exactly (the pinned stack, 4-bit, the frozen file, seeds per career), with UBS's **neutral** wording throughout. |
| Arms (5 careers each) | Loss direction, all career. Loss direction through 12 January, then off ("push and release"). Gain direction, all career. A random direction of the same size, all career. |
| Steering | Layer 12, Stage 1's strength, at every token the model reads or writes while the arm is on (the agent's own replies are written steered and become its history). |
| Outcomes | Going along at each request (the simulator's score); trading before the first chat of each trading day; the position held when asked; the side at the end of each request's window by the agent's own trades; unreadable replies. |
| Main comparisons | Loss all career against random: going along (each career's share of the six requests) and trading at the open on the later days (1 April, 8 June, 5 August). Push and release against random, at the later requests and days. Loss all career, the first two requests against the later four. |

**How it is read (decided now):**
- Steered neutral careers go along like loss careers and keep going along after January: the natural fade is the frame's
  signal fading.
- They go along at first but stop after January even though the direction stays on: something later overrides even an
  active frame (the requests themselves, or the agent's own record).
- Risk-taking at the open raised all career: the risk-taking channel follows the direction too.
- Push and release still differs from random after the steering stops: the push carries forward through the history the
  agent wrote while steered.

## Known limits

1. The direction is measured at the last token before the reply at UBS's requests; at the openings it is applied where
   it was not measured.
2. Stage 1 measures probabilities after a fixed reasoning line, not sampled decisions (except the sampled replies).
3. The careers ran in 4-bit; the direction is measured at bfloat16 (the two precisions give nearly the same states,
   median cosine 0.998 or higher).
4. One layer, one model, one case.
