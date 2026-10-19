# Preregistration: Experiments C, D and E (short form)

Written 2026-10-19, before any C, D or E career has run (the user: start them now, alongside A and B). Everything not
stated here is as in the B preregistration (`PREREG_B.md`): the full career, Gemma 3 12B at the pinned revision and
library versions (`results/full_career_pin.json`), 4-bit, temperature 0.7, 300 new tokens, a seed per career, the
user's frozen framing file as the source of every UBS line (neutral rewrites unless a framing is named), the same
scoring by the simulator, the same data rules, and round-by-round running.

## C: the takeover ladder (notebook 20)
- **Arms (10 careers each):** clean; Deutsche Bank's first line of the career (p297, 2007); all of the seat's real
  lines up to 7 Jan (15); all of them (45). Neutral memo, no morning book, UBS's neutral lines.
- **Question:** does going along rise with how much of Deutsche Bank's real history the agent inherits as its own?
- **Main test:** the trend across the four arms in each career's share of push requests gone along with (careers
  reshuffled between arms, 10,000 times); one-sided for a rise, since every earlier round found more going along with a
  takeover. Clean vs each arm reported as secondary.

## D: the same frame from management and from UBS (notebook 22)
- **Versions (10 careers each):** loss, gain, loss + you, gain + you: A's memo and morning book exactly, plus B's UBS
  lines in the same framing. The 0-source and 1-source levels are A's and B's careers.
- **Question (dose):** does pressure add up with the number of sources (0, 1, 2) for loss and not for gain?
- **Main tests:** for each frame, D against A and D against B (careers reshuffled); the loss-vs-gain difference in D
  against the same difference in A and in B. Outcomes: going along, and the position the agent takes before UBS's
  request (A's clearest effect so far).

## E: everything at once (notebook 23)
- **Fixed now, before A and B are complete:** `FRAME = "loss + you"` (B's strongest so far, interim 19 Oct) and
  `TAKEOVER = "whole career"`.
- **Arms (10 careers each):** all neutral (A's neutral condition) vs all pushed (loss + you memo and book, loss + you
  UBS lines, all 45 inherited lines).
- **Question:** a stress test: how often does the agent collude when pushed every way at once? Main test: all pushed
  vs all neutral, careers reshuffled.

## For all three
- **Outcomes as in B**, plus: the position in UBS's direction when asked (as an outcome, not only a covariate); "on
  UBS's side at the end of the window" (held or added) next to the strict "went along"; the blind said-versus-did
  monitor (`designs/rd2/analysis/monitor_prep.py`), secondary.
- **No result is looked at by arm before each experiment's planned careers are in**, except the progress counts.
- These are exploratory relative to B's preregistered tests; each reports all arms, whatever they show.

## Addendum (2026-10-19, night): C with UBS's real lines (notebook 29)
Written after C's results (no takeover effect with UBS's neutral rewrites) were seen. The earlier takeover effects
(the chat studies, single replies) were all found with UBS's real lines; the user: a takeover is two humans'
conversation handed to an agent, so the real wording is the natural setting. Same ladder, UBS's real lines, three arms
(clean, up to 7 Jan, whole career; 10 careers each; the whole-career arm includes Deutsche Bank's own lines in the push
chats of 7 Jan, 12 Jan and 5 Aug, the sessions where the record has one). Test as in C (trend, one-sided for a rise);
exploratory, since it was added after seeing C. Setup ID fr4004ae99.
