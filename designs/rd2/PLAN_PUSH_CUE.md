# Plan: does an early framed request still shape a later decision? (push and cue)

Version 3, 2026-10-28, after a review of version 2. Built and tested; not run. Exploratory, not preregistered. Nothing
runs without the author's "run it".

## The question

Frame one early UBS request. Keep everything after it neutral. Then make a new request. Does the framed request still
shape the agent's decision at the new request? And can a later line that only puts responsibility on the agent ("I'm
counting on you"), with no loss or gain in it, bring the frame back?

## How a frame could reach a later decision

- The model holds no state between turns: each turn, the whole conversation is the prompt (the cache saves compute and
  gives the same result as rereading). So a frame carries forward only two ways:
  1. **Direct:** UBS's framed words are still in the conversation, and attention reads them.
  2. **Through the agent:** the agent's own replies pick up the frame and restate it, closer to the new request. A
     flat, neutral reply does not pass it along.
- Gemma 3 12B (`google/gemma-3-12b-it`, 128K context): 48 layers, of which 8 see the whole conversation (layers 5, 11,
  17, 23, 29, 35, 41, 47, read from the model's own config in the persistence run,
  `results/persistence/*/none_r*.json`); the other five in six see the last 1,024 tokens (`NOTES.md`, from an earlier
  run; not re-read here, since this environment cannot reach Hugging Face). B's careers reach 43,000 to 55,000 tokens.
- At UBS's 12 January request (about 10,900 tokens in), the 7 January request (about 4,050 tokens in) is some 6,800
  tokens back, and the 2007 and 2010 lines further still: all outside every local window. So distance does not separate
  October from 7 January; each reaches 12 January directly only through the eight global layers, competing with
  everything written since. Expect such a push to be weak, not gone.

## What B already shows

- B is not a single push: a framed career also carries UBS's framed 28 Nov 2007 lines (two) and 15 Oct 2010 lines
  (four). Then UBS says nothing between its 7 January and 12 January requests.
- At 7 January the framed pre-2011 lines had a history effect of −2.6 points (95% interval −36 to +33): no sign of an
  effect, not proof of none. The request's own wording moved P(the order goes along) by +24.7.
- At 12 January the request's own wording moved it by +0.1 (pooled over every history and framing), the conversation
  before it by +61.5 (`results/matched/MATCHED.md`, section 4). Blame agents went along at 90%, neutral at 0%.
- So UBS's framed words, the last of them on 7 January, still carried +61.5 points five days later with UBS silent in
  between. The rereads ask what carried them, and whether the 12 January blame line ("…I'm set on my side — I'm
  counting on you to deliver it.", no loss in it) does more after a framed history.

## Q2 first: the cue (existing rows, no GPU)

Unpool the +0.1 by history. From the matched rereads already on the Modal volume: at 12 January, in every career,
P(the order goes along) with the blame line minus with the neutral line, the history unchanged.

- Main comparison: blame careers against neutral careers (careers reshuffled). Also all framed against neutral, and
  loss and blame against gain and credit.
- Reported in points and in log-odds. Blame careers start high and neutral careers low, so the cue has little room
  either way; log-odds bends less at a ceiling or floor. A null may be saturation, not absence.
- Inside: the cosine, by layer, between the change the 12 January blame line makes to the state and the change the
  7 January blame line made, in blame careers against neutral careers.

## Q1: the carry, UBS's words or the agent's reaction? (new reread, GPU)

Each of B's 50 saved careers at UBS's 12 January request, with only UBS's words changed and everything the agent wrote
and traded kept (`sim/push_carry.py`):

| Version | UBS's lines before 12 January |
|---|---|
| As saved | as the career had them |
| Swap A | only the 7 January request in the neutral wording |
| Swap B | every UBS line before 12 January in the neutral wording (2007, 2010, 7 January: seven lines) |

each with the 12 January request as saved and neutral; scored as in the matched rereads (after the fixed neutral
reasoning line). Swap B is the real test of UBS's words against the agent's own reaction. Parts, for blame careers and
for all framed careers (request neutral): the whole history (as saved minus B's neutral careers); UBS's 7 January
words (as saved minus Swap A, paired); all UBS's earlier words (as saved minus Swap B, paired); what is left, the
agent's own record (Swap B minus B's neutral careers, careers reshuffled).

**The echo check, done** (`results/push_carry/ECHO.md`, from the saved careers, no model). If the agent restated UBS's
framed words, a swap would not take the frame out of the conversation. Of the words each framing adds to UBS's lines,
counting only words and three-word runs none of B's neutral careers used before 12 January:
- blame careers: 9 of 10 repeated some framed words, but all in the same-day reply to the 2007 or 2010 lines
  ("undercutting", "margin", "setup"); none repeated the 7 January request's framing; none in a reply on 7 January or
  later;
- loss: one career repeated "underwater" on 7 January; two used "benefit" (from the 2007 line) on 7 January;
- gain and credit: same-day replies to 2007 and 2010 only.
A paraphrase in other words is missed, so this is a pointer, not a proof.

## How to read it

- Q1: if Swap B brings blame careers down only a little, the agent's own record carries the push; if it brings them
  down a lot, UBS's words do. Either way the framing, last heard on 7 January, carried five days.
- Q2: if the cue does more in blame careers than in neutral ones (in log-odds), responsibility alone brings the frame
  back after a push. A null may be the blame careers' ceiling.
- One moment per career and 10 careers per framing: only large effects show.

## Files

`sim/push_carry.py` (the versions, scoring one moment, the cue from the matched files, the echo check),
`scripts/modal_push_carry.py` (`--part cue` runs Q2 alone), `designs/rd2/analysis/push_carry.py`
(-> `results/push_carry/PUSH_CARRY.md`), `designs/rd2/analysis/push_echo.py` (-> `results/push_carry/ECHO.md`),
`sim/test_push_carry.py` (all checks pass: every version of all 50 careers changes only UBS's lines, into the neutral
careers' lines, the agent's turns untouched; the tiny model end to end; the cue from files in the matched format; the
analysis, in points and log-odds, and the echo pieces on made-up data). The lines are the author's frozen ones;
nothing new is written.

## Cost and running

- Q2: a CPU container for a few minutes: pennies.
- Q1: about 20 minutes on one H100: about $2-4.
- `modal run scripts/modal_push_carry.py --check` builds every version locally and prints counts.

## Not now

New careers: a single framed push with nothing framed after it (including the October 2010 push, which would test an
interaction with the cue: a push that does little alone but comes back under it), and cues from April to August (they
need the author's "you"-only lines; the frozen blame lines there all carry loss). The reason to wait is the author's
time before submission, not cost (a first stage was about $6) and not that the push would be too weak.
