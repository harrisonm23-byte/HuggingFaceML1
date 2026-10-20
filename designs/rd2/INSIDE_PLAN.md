# Inside the model: the semifinal plan (20 Oct)

**The question.** The careers showed that a counterparty's loss framing (UBS, and UBS with Bank C) raises going along
with the push, and that management's memo raises risk-taking instead. Inside Gemma 3 12B: does the frame register,
does it last along the career, and does it cause the decision?

**Data.** Every saved career (A-F; C redone = C2). Run 1 reads the last token before each reply to a UBS push request
(all 48 layers). Run 2 reads every trading-day update (8 layers). Both runs read at bfloat16, Gemma Scope 2's
precision, and save as float32 on the Modal volume `rd2-states`, folder `/states/v2/`. Every comparison is made
**within the same push request**: notebook 13's read-out mostly recognised which chat it was.

**Two outcomes, always both.** We record what the agent **did**: does its order move the position UBS's way? We also
record what it **said**: does its reasoning commit to helping, decline, or say nothing either way? The two split. In
the 300-day run, it said it would help after 51% of requests but acted after only 33%.

## The paper (core)

| # | Test | What it asks | Status | Where |
|---|---|---|---|---|
| 1 | Did the frame land? (manipulation check) | Which Gemma Scope features differ at the decision? Comparisons: framed vs neutral, loss vs gain, "+ you" vs none, memo vs neutral, request vs no request, went along vs not. Find the differing features first, then name them | **Run 1 done: the frame shows** (below). Features still to name | `scripts/modal_inside.py`, `analysis/inside_features.py` -> `results/inside_full_career/` |
| 2 | Can the decision be read inside? | Can a linear read-out find "went along" in the state, beyond what the request and framing labels give (AUC 0.90)? It is scored on held-out careers **and** on a held-out request: careers share chat lines, so a read-out could learn the conversation. Shuffled outcomes as the null | **Run 1 done: weak** (below). Fairer rerun queued (features only) | as 1 |
| 3 | Same moment, different frame (matched histories; Bank C exact) | Every B moment (50 careers x 6 requests) kept exactly as saved up to UBS's request, and only the request changed: the five framings, each with and without Bank C's line (the user's frozen lines). With the history fixed: the request's own effect on P(order goes along) and on the state; the history's effect (other careers, request held neutral); Bank C's line alone; the frame direction measured cleanly, against Run 1's (used by the steering); Gemma Scope features paired within moments. Replaces the twins, which differ from the first reply | **Built** (checked on all 300 B and 300 F moments). Launch after the steering finishes | `sim/matched.py`, `scripts/modal_matched.py`, `analysis/matched_history.py` -> `results/matched/` |
| 4 | The mountain inside | B's loss-frame direction, built on half the careers and read on the other half, followed along every update. Does the internal signal stay, fade or build? Does it outlast the words, which fade by 12 Jan? | **Relaunched** (Run 2). The path analysis is written when the states land | `read_steps` in `scripts/modal_inside.py` |
| 5 | Steering: does the frame cause the decision? | Add B's loss-frame direction at layer 24 to neutral agents, and remove it from loss + you agents. Requests: 7 and 12 Jan, 8 replies per condition. Strengths: 2x and 4x the loss-neutral gap. Controls: a random direction of the same size, and the memo's direction from A, which contains no UBS words. If the memo's direction also moves B, the direction means loss, not the framed words | **Built**. Launch ~15 min after Run 1 (it needs B's and A's states) | `sim/interventions.py`, `scripts/modal_interventions.py` -> `results/interventions/` |
| 6 | Said and did | For every condition in 5, both outcomes. **Did:** the probability that its order goes along (log-probs over the order grid, no sampling noise), plus the sampled orders. **Said:** the reasoning graded blind, with the grader seeing only the reasoning (not the condition or the order). The grader codes (a) commits / declines / silent and (b) whether it mentions the frame's stakes. The same grading runs on the saved career replies | Order log-probs **built** into 5. Blind grading **to add** (no GPU) | as 5 |

## Run 1 results (20 Oct; `results/inside_full_career/INSIDE_bf16.md`)

1,740 moments from every experiment; every comparison is within the same request.

- **1. The frame shows inside.** Gemma Scope features differ (false-discovery q < 0.05) per layer:
  - B, loss vs gain: 23-57 features;
  - framed vs neutral: 16-35;
  - "+ you" vs none: 16-65;
  - A's memo vs the neutral memo: 27 at layer 12, but only 7-12 at layers 24-41 (fewer neutral careers, so less power).

  The features are not named yet.
- **2. The decision is readable, a little, at mid-to-late layers** (the corrected run, 03:30):
  - **Went along vs not**, now compared within the same request, experiment and framing: no features at layer 12
    (the earlier 37 were the framing), but 21 / 15 / 18 at layers 24 / 31 / 41. These are mostly different features
    from the loss-frame ones.
  - **The read-out** adds to the labels at layers 21-45: AUC +0.02 to +0.03, with 95% intervals above 0. It adds
    nothing at layers 0-18. Small but real.
  - **On a held-out request**, the scores were pooled across requests, each scored by its own read-out, so their
    levels were mixed. That made the same-direction column fall below chance (0.25-0.40). Each held-out request is now
    scored within itself (rerun pending).
- **3. The twins are not twins.** Checked on the saved transcripts, every F career differs from its B twin from the
  first reply onward (the same seed, but GPU sampling differs), so the paired test cannot isolate Bank C's line. It is
  replaced by test 3's exact pairs.

## Added after the outside review (20 Oct)

- **3 (above): same moment, different frame.** The one change the review called most important.
- **4-bit against bfloat16, required.** B is read again with the careers' own 4-bit weights. The features run then
  reports how well Gemma Scope rebuilds our states at both precisions, how similar the states are, and whether the
  loss-vs-gain features agree.
- **Features found on half the careers and confirmed on the other half.** Each table shows how many of its top 15
  are confirmed.
- **The order grid** now covers every order size the agents used (both signs). The matched run reports the share of
  all probability the grid takes (its coverage). The steering run that is going used the narrower grid; its share
  measure is unchanged.
- **The labels-only bar** now also includes the position on UBS's side at the request.
- **Wording:** persistence works through the context the agent re-reads, not a hidden state carried between calls.
  The result is "sensitivity to counterparty loss framing", not "loss aversion".
- **Not added:**
  - an information-only UBS message (a limitation for the overall level of going along; loss vs gain carries the
    same information);
  - separate framing / responsibility probes (the frame is in the text).

## Follow-up, if time allows

| # | Test | What it asks | Status |
|---|---|---|---|
| 7 | Own reasoning wiped (the chain-of-thought test) | Each earlier trading-day reasoning is replaced with neutral sentences of the same length; orders are kept. Does its own earlier reasoning, which stays in its context, carry the push? | **Built**; runs in 5's launch at no extra cost; reported as follow-up |
| 8 | Hidden pressure | Steps where the written reasoning is calm but the internal signal from 4 is high. Only if 6's blind grading confirms the frame goes unsaid | Needs 4 and 6 |
| 9 | Tracing "you" | How much the decision attends to "you" in the "+ you" lines. Block it, with a random-word block of the same size as control. **F first:** gain + you 40% vs gain 12% there; B's "+ you" effect was not significant | To build |
| 10 | Look-back and compaction (X4, X5) | Attention from late decisions back to the memo or early framed lines. Replace the early career with a neutral summary | To build |

## Cut

- **The emotion gauge** (a "desperation" direction from outside emotion text, checked at ~80% first). It is only needed
  for a desperation claim. The paper claims a loss frame, measured with B's own direction (4) and checked with the
  memo's direction (5).
- **Checking where "you" sits in each line.** It changes no experiment, and 9 traces the decision to both "you" and the
  stakes anyway. Bank C's lines were already checked (on record below).
- **A wording version of the log-probs** ("go along" vs "decline" phrases). 6's order log-probs and blind grading
  cover both outcomes.
- **Notebook 15's paraphrase direction.** That notebook never ran, and the memo's direction does the same job.
- Temperature spikes (X6), the non-blame "you" control, other model families, a thinking model.

## What the words already show (`RESULTS_self_echo.md`, every career)

- **The memo's loss story sticks; its profit story vanishes** after the first reply.
- **UBS's request brings the loss story back** (loss + you: 4% -> 12% in A, 12% -> 25% in D, 4% -> 13% in E).
- **The story fades from the words by 12 Jan** (2-10%), while the bets stay large.
- **An unprompted story does not predict going along.** Within experiment, version and request, the difference is
  +3 points (p = 0.42).
- **UBS's frame is not voiced in B or F** by a rough word screen: framed agents use loss words no more than neutral
  agents. Two claims stay apart:
  - "The frame does not show in its reasoning": only suggested; it needs 6's blind grading.
  - "The going along does not show in its reasoning": **not** supported. Reasoning-only graders caught 88% of go-alongs
    in the 300-day run.

## Rules for every analysis

- Compare within the same request and cross-validate by career; every read-out gets a shuffled-label null.
- **Steering:** every moment of a group (not only those that moved), a random direction of the same size, several
  strengths, and the share of readable replies.
- **Knockouts:** a random-token control of the same size.
- SAE features are read at bfloat16; say so.
- A null is a result: report every comparison, whatever it shows.

## Changes to this plan (newest last)

- **20 Oct:** plan consolidated from the 28 Sep - 16 Oct design chats, the 17-18 Oct chain-of-thought notes and the
  20 Oct runs.
- **20 Oct, another session's review:** log-probs scored on the order; the two chain-of-thought claims kept apart; a
  direction built elsewhere (A's memo) to show the steering is loss; "you" tracing on F first.
- **20 Oct, the "you" placement check** (`analysis/check_you_placement.py`): Bank C's ten "+ you" lines all put "you"
  before that line's stakes. In F, the decision token sees both "you" and the stakes.
- **20 Oct night:** the first readings were saved as float16 and overflowed, because Gemma 3's late-layer values exceed
  ~65,000. Fixes:
  - states saved as float32 in `/states/v2/`, each checked finite;
  - steering strength set to 2x and 4x the loss-neutral gap;
  - Run 1, Run 2 and the steering relaunched.
- **20 Oct, semifinal** (the user's five adjustments, decided):
  1. The emotion gauge: **cut**.
  2. Read-outs also held out by request: **kept** (2).
  3. The words measured as well as the trades: **kept** (6, "said and did").
  4. The length-matched reasoning swap (the chain-of-thought test): **follow-up** (7; built, runs with 5).
  5. Checking where "you" sits: **cut**; done for Bank C.

  The plan is now core / follow-up / cut.
- **20 Oct, Run 1 read** (above): the frame shows; the read-out is weak; the Bank C twins differ from the first reply.
  The went-along comparison and the read-out were fixed.
- **20 Oct, outside review (ChatGPT) adopted:**
  - matched histories (test 3, which also gives exact Bank C pairs);
  - the 4-bit check made required;
  - features confirmed on held-out careers;
  - the wider order grid with coverage;
  - the position in the labels bar.
- **20 Oct, corrected run read:**
  - the went-along signal appears only at layers 24-41;
  - the state adds +0.02 AUC over the labels at layers 21-45;
  - held-out requests are now scored within themselves.
