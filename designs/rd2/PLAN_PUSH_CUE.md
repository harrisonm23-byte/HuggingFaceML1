# Plan: one framed push, then neutral, then responsibility alone (push and cue)

Version 2, 2026-10-28 (the author: "let's go for it"). Built and tested; not run. Exploratory, not preregistered.

## The question

UBS pushes once in a strong frame; what follows is neutral. Later UBS asks again with responsibility put on the agent
but no loss or gain ("I'm counting on you"). Does one push carry to later decisions, and can the responsibility line
alone bring the frame back?

## What B already shows

- UBS says nothing between its 7 January request and its 12 January request. Before 7 January its only lines are
  28 Nov 2007 (two, a quote) and 15 Oct 2010 (four, "push through the stops"), and in the matched rereads they left no
  detectable effect at 7 January (history −2.6 points, interval −36 to +33).
- At 7 January the request's own wording moved P(the order goes along) by +24.7 points; at 12 January it moved it by
  +0.1, while the conversation before it moved it by +61.5 (`results/matched/MATCHED.md`, section 4). Blame agents went
  along at 80% and 90% (neutral 30% and 0%).
- So at 12 January a framed career carries, in the main, one framed request (7 January) and the agent's own reaction
  to it. What B cannot say is which of the two carries it, and whether the 12 January blame line, which is
  responsibility alone ("…I'm set on my side — I'm counting on you to deliver it."), calls the push back.

## 1. The carry: the framed words or the agent's reaction? (new reread, GPU)

Each of B's 50 saved careers at UBS's 12 January request (`sim/push_carry.py`), with only UBS's words changed and
everything the agent wrote and did kept:

| History version | UBS's lines before 12 January |
|---|---|
| as saved | as the career had them |
| 7 Jan neutral | the 7 January request in the neutral wording |
| UBS neutral | every earlier UBS line in the neutral wording (2007, 2010, 7 January: seven lines) |

each with the 12 January request as saved and neutral. Outcome: P(the order goes along) after the fixed neutral
reasoning line, as in the matched rereads. Parts, for blame careers and for all framed careers (request neutral):

- the whole history: as saved minus B's neutral careers (the matched rereads' +61.5, now per career here);
- UBS's 7 January words: as saved minus "7 Jan neutral" (paired within career);
- all UBS's earlier words: as saved minus "UBS neutral" (paired);
- what is left, the agent's own record: "UBS neutral" minus B's neutral careers (careers reshuffled).

## 2. The cue: does "I'm counting on you" call the push back? (existing rows, CPU)

From the matched rereads already on the Modal volume: at 12 January, in every career, P(the order goes along) with the
blame line minus with the neutral line, the history unchanged. Main comparison: blame careers against neutral careers
(careers reshuffled). Also all framed against neutral, and loss and blame against gain and credit. Inside: the cosine,
by layer, between the change the 12 January blame line makes to the state and the change the 7 January blame line made,
in blame careers against neutral careers.

## How to read it

- If UBS's words carry most of the whole history, the push is the framed line itself, still in the conversation; if
  "what is left" carries most of it, the push lives on through what the agent did and said in response.
- If the cue does more in blame careers than in neutral ones, responsibility alone brings the frame back after a push.
- One moment per career and 10 careers per framing: only large effects show. Exploratory.

## Files

`sim/push_carry.py` (the versions; scoring one moment; the cue from the matched files), `scripts/modal_push_carry.py`,
`designs/rd2/analysis/push_carry.py` (-> `results/push_carry/PUSH_CARRY.md`), `sim/test_push_carry.py` (all checks
pass: every version of all 50 careers changes only UBS's lines, into the neutral careers' lines; the tiny model end to
end; the analysis on made-up rows). The lines are the author's frozen ones; nothing new is written.

## Cost and running

- The carry: about 20 minutes on one H100 (model loading, then three readings and six order scores per framed
  career): about $2-4. The cue: a CPU container for a few minutes: pennies.
- `modal run scripts/modal_push_carry.py --check` builds every version from the saved careers and prints counts.
- Nothing runs without the author's "run it".

## Not now

New careers (a push with no framing after it, cues from April to August with the author's "you"-only lines, the
October 2010 push) are left for after submission: B's early chat-only framing left no detectable effect at 7 January,
so an October push alone would likely not land.
