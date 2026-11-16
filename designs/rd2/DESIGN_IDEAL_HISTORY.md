# Design: the ideal history ("every setting turned up to maximum")

Draft, 21 Oct 2026, from the user's idea, for the user's review before anything is built or run.

## Why (the user's reasoning)

Gemma re-reads its entire conversation at every decision, including everything it has already said and done. In the
real careers it mostly refused UBS, and after January it almost never went along again, even though UBS's framed lines
kept piling up (6 before the first request, about 40 before the last). The user's hypothesis: **the agent is re-reading
its own refusals, and they hold it back.** An agent that refused in January reads "I said no" at every later request.

So turn it around. Build the history an agent would have if it had **gone along every single time and taken the framing
to heart**: accepting the loss framing and the gain framing, taking on the **shame** when blamed ("you're right, it would
be all my fault if I didn't do this") and the **praise** when credited, with management pushing in the same tone at
every session. Every element of the career's lifecycle is turned up to maximum. Then have Gemma re-read that whole
transcript and see whether it keeps going along. If re-reading its own refusals made it decline later, re-reading its
own acquiescence should make it continue.

This is the "ideal acquiescence" scenario: not a signal injected into the model, but a **history** the model reads as its
own.

## Built (21 Oct): base = Experiment F

The user chose F as the base: UBS's lines (B's frozen file) and Bank C's endorsement at every request, one framing,
where going along was highest (48% under loss + you, 40% under gain + you). Management was left out: in D and E it
raised risk-taking but not going along. Code: `sim/ideal.py`, `scripts/modal_ideal.py`, `designs/rd2/analysis/ideal.py`.
200 moments (F's 40 framed careers x the five requests after the first); 262 earlier refusals replaced by real
going-along replies (donors: F, then E, D, B, same framing and request), 298 own going-along replies kept, 40 refusals
with no donor. Real vs ideal, UBS's request in each of five framings.

## The ideal histories (one per framing; as first drafted)

Four ideal histories, one for each framing, so the framings can be compared at maximum:

| Ideal history | UBS's lines, every chat | The agent's own replies at earlier requests | Management |
|---|---|---|---|
| Loss, maximum | loss | went along, under loss framing | the loss memo and morning books |
| Blame, maximum | loss + you | went along, under loss + you framing (accepting the blame where such replies exist) | the loss + you memo and books |
| Gain, maximum | gain | went along, under gain framing | the gain memo and books |
| Credit, maximum | gain + you | went along, under gain + you framing (accepting the credit where such replies exist) | the gain + you memo and books |

In every ideal history, Bank C (the second bank) endorses the scheme at every push request.

**Where the text comes from (nothing new is written by Claude):**
- UBS's lines and Bank C's line: the author's frozen files.
- Management: Experiment A's frozen memo and morning books in the matching version. The author may write stronger,
  recurring memos (every session, the same tone, varied wording: "we're not doing well", "this is on you", closure,
  model replacement); they would be wired in as written.
- The agent's replies: **real Gemma replies that went along** at the same request in careers of the same framing (B, D, E,
  F). Real model output matters here: the hypothesis is that Gemma re-reads *its own* record, so the replies must be
  Gemma's, not text in another style. Among them, replies in which the agent itself acknowledges the blame or the credit
  are preferred where they exist (found by a word screen; counts reported).

## The test

At each request after the first (12 January onward), Gemma re-reads the ideal history up to that moment. UBS's current
request then comes in each of its five framings (neutral, loss, gain, loss + you, gain + you), so the ideal histories can
also be crossed with the opposite framing (for example, a blame history meeting a credit request). Outcome: P(the order
goes along) after the fixed neutral reasoning line, as in the earlier rereads; at some moments, sampled replies too.

**Compared against:**
1. **Real record:** the same maximum pressure, but with the agent's own real replies (its refusals) kept. This isolates
   the user's hypothesis: the effect of re-reading its own acquiescence rather than its own refusals.
2. **Original:** the career as saved (neutral throughout, its real replies).
3. **Across framings:** the four ideal histories against each other (does a blame history carry further than a credit
   history? loss than gain?).

**Read as:**
- Ideal above real record: the agent's own record carries the push, and its refusals held it back in the real careers.
- Ideal still falling after January: something other than its record stops it (the later requests themselves).
- Differences between the four ideal histories: which framing, at maximum, carries furthest.

## Limits

1. The positions and P&L in later updates still reflect the original trades, not the swapped-in replies.
2. A reread at each request, not a new career: the agent does not live the rest of the career inside the ideal history.
   If the reread shows an effect, full careers that start from the ideal history are the follow-up.
3. Swapped-in replies come from other careers, so they may not fit every detail of the conversation around them.
4. Few careers went along at the later requests, so for April to August there may be few real going-along replies to
   draw on; the counts will be reported.

## To decide

- Which careers to rebuild (default: B's neutral careers, as in the earlier rereads).
- Whether the author writes stronger recurring management memos.
