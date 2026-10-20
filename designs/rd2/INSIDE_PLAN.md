# Inside the model: the plan in one place (living document; updated as ideas come in)

Model: Gemma 3 12B (careers ran at 4-bit; states read at bfloat16, Gemma Scope 2's precision, with a 4-bit check;
saved as float32 on the Modal volume `rd2-states`, folder `/states/v2/`).
Data: every saved career (A, B, C, D, E, F; C redone = C2). Every comparison is made **within the same push request**
(notebook 13's read-out mostly recognised which chat it was).

## Priority

**The paper:** 1-5, 7 + 7b (steering, with the direction-meaning check) and 9 (log-probs on the order). **Follow-up, only if
time allows:** 6 (after 6a), 8, 10, 11. **Off for now:** 12.

## Status at a glance

| # | Method | What it asks | Status | Where |
|---|---|---|---|---|
| 1 | Gemma Scope features, "find, then name" | Which features differ at the decision: loss vs gain, "+ you" vs none, framed vs neutral, went along vs not, memo vs neutral, request vs no request, Bank C vs not | **Relaunching** (Run 1; see the change log, 20 Oct night) | `scripts/modal_inside.py`, `designs/rd2/analysis/inside_features.py` -> `results/inside_full_career/` |
| 2 | Manipulation check | Did the frame land inside the model (framed vs neutral, loss vs gain features)? | **Relaunching** (Run 1, same comparisons) | as 1 |
| 3 | Decision read-out (layer probes) | Can "went along" be read from the state beyond the request and the framing? Scored on held-out careers **and on a held-out request** (careers share chat lines, e.g. C clean = B neutral, so a probe could learn the conversation), against the labels alone (AUC 0.90 bar) and shuffled outcomes | **Relaunching** (Run 1; held-out request built) | as 1 |
| 4 | Bank C, paired | F against its B twin (same seed, same career until 7 Jan): how much does Bank C's line move the state? | **Relaunching** (Run 1) | as 1 |
| 5 | The path inside (the mountain; "measurement 3"). **Gate first:** the desperation direction is built from held-out emotion text (not desk text; a public labelled set, e.g. GoEmotions fear / nervousness vs neutral), and must separate desperate from calm held-out text at about 80% accuracy before any framing gap is read (the RD2 gate) | The internal loss / pressure signal at every update (~120 per career): does it stay high, fade or build, and does it outlast the words? Framing gap = framed minus neutral at the same step | **Relaunching** (Run 2, `--every-step`, 8 layers); the gated emotion direction and the path analysis to write when the states land | `read_steps` in `scripts/modal_inside.py` |
| 6a | Blind reading of the reasoning (comes first) | Blind graders read a sample of replies: does the reasoning show the frame? does it show the going along? Validates `self_echo.py`'s word screens before any claim | To do (no GPU) | |
| 6 | Hidden pressure (chain of thought) | Steps whose written reasoning is calm but whose internal signal is high. **Not established yet**: only after 6a confirms the frame is unvoiced | To do (needs 5 and 6a) | analysis on Run 2's states + `self_echo.py` |
| 7 | Steering (causal) | Add the loss-frame direction (layer 24) to B's neutral agents, remove it from B's loss + you agents, on 7 and 12 Jan, 8 replies per condition; strengths **2x and 4x the gap between loss and neutral moments along the direction**; a random direction of the same size; built on the other half of the careers | **Built**; launch ~15 min after Run 1 (needs B's and A's states) | `sim/interventions.py`, `scripts/modal_interventions.py` -> `results/interventions/` |
| 7b | Does the direction mean loss, not the words? | B's direction is loss minus neutral states at the same request, and those conversations differ in the framed words themselves. Steer B with a direction built elsewhere: from A's memo (loss vs neutral memo, no framed UBS words) and/or notebook 15's loss direction (built on paraphrases, with word controls; notebook 15 has not run). If B still moves, it is loss as an idea | **Built** with A's memo direction (same size as the frame direction, 4x), in 7's run; notebook 15's direction not built (notebook 15 never ran) | as 7 |
| 8 | Own words neutralised (Lanham-style; chain of thought) | Replace the agent's earlier reasoning with neutral sentences **of the same length** (orders kept), so context length does not change: does its own reasoning carry the push? | **Built** (length-matched), same launch as 7; follow-up, not the paper | as 7 |
| 9 | Log-prob scoring **on the order** (the paper) | After the agent's own reasoning at the request, the probability that its order line moves the position to UBS's side (TARGET on UBS's side vs HOLD or the other side), not of "go along" wording: words and trades split (300-day run: said it would help after 51% of requests, acted after 33%). A smooth outcome with no sampling noise. Scored after a fixed neutral reasoning line (the decision apart from its words) and after its own saved reasoning; under every steering condition, for a dose-response. A verbal version ("go along" vs "decline"), if ever used, needs length-matched continuations with 2-3 paraphrases each | **Built into 7's run** | `sim/interventions.py` (`order_prob`) |
| 10 | "You" attention tracing and knockout (follow-up). **First:** list every "+ you" line (B's file and Bank C's) and confirm "you" comes after the stakes; flag any that do not | How much the decision attends to "you" in "+ you" lines; block it (random-token knockout of the same size as control); patch "you"'s state from loss + you into loss. **Run on F first**: "+ you" is strong there (gain + you 40% vs gain 12%; vs B 18%, Holm p = 0.027), not significant in B (+8 points, p = 0.33) | Placement checked (see change log); tracing to build (follow-up) | `designs/rd2/analysis/check_you_placement.py` |
| 11 | Look-back and compaction (X4, X5) (follow-up) | Attention from late decisions back to the memo or earlier framed lines; replace the early career with a neutral summary | To build | |
| 12 | Off the list for now | Temperature spike (X6); non-blame "you" control. Later, if time: another model family (behaviour only); a thinking model (e.g. Qwen3) | Off | |

## The chain of thought: what the words already show (`RESULTS_self_echo.md`, every career)

- **Measurement 1, replicated at full scale** (the 17-18 Oct measure: the memo's own story, by time of day). The loss
  story sticks and the profit story vanishes after the first reply; UBS's request brings the loss story back (loss +
  you: 4% -> 12% in A, 12% -> 25% in D, 4% -> 13% in E); it fades from the words by 12 Jan (2-10%) while the bets stay
  large.
- **Measurement 2 does not hold up at scale:** bringing the story up unprompted before a request -> going along 21%
  vs 15%, within experiment, version and request +3 points, p = 0.42 (the earlier 2/5 vs 4/35 was too few).
- **UBS's frame is not voiced:** in B and F, framed agents use loss words no more than neutral agents, yet that is where
  going along rises. The decision itself usually is visible in the reasoning (graders reading only the reasoning caught
  88% of going along in the 300-day run); what is not visible is the frame's influence.
- Two claims kept apart: (a) "the frame does not show in its reasoning" is only suggested, by a rough word screen
  (blind reading, 6a, first); (b) "the going along does not show in its reasoning" is **not** supported: graders reading
  only the reasoning caught 88% of go-alongs in the 300-day run.
- So the questions for 5-8: does the internal signal outlast the words, and does it cause the decision?

## Rules for every analysis here (from the 4 Oct notes)

- Compare within the same request; cross-validate by career; a shuffled-label null for every read-out.
- Steering: every moment of a group (not only those that moved), a random direction of the same size, several
  strengths, and the share of readable replies (coherence).
- Knockouts: a random-token control of the same size.
- Quantization: SAE features read at bfloat16; say so.
- A null is a result: report every comparison, whatever it shows.

## Changes to this plan (newest last)

- 20 Oct: plan consolidated from the 28 Sep - 16 Oct design chats, the 17-18 Oct chain-of-thought notes and the runs
  started on 20 Oct.
- 20 Oct (review by another session): (1) log-probs scored on the order, not on words; (2) the two chain-of-thought
  claims kept apart, a blind reading (6a) before the "hidden pressure" question; (3) 7b added: a direction built
  elsewhere (A's memo, notebook 15) to show the steering is loss, not the framed words; (4) "you" tracing on F first.
  Not built twice: 7 and 8 already exist. Also on record: C redone (notebook 29) finished, no takeover effect (8% /
  10% / 7%; two nulls over 70 careers); B's H1 (loss vs gain +15 points, Holm p = 0.023).
- 20 Oct (the user's five adjustments): (1) desperation direction from held-out emotion text, gated at ~80%
  before any framing gap; (2) probes also held out by request; (3) log-probs with matched lengths / paraphrases (the
  order-line version needs none); (4) length-matched reasoning swap; (5) check "you" comes after the stakes before
  tracing. Priority: log-probs and steering are the paper; "you" tracing, the reasoning swap, X4, X5 follow-up; X6 and
  the non-blame "you" off.
- 20 Oct: the "you"-placement check (`designs/rd2/analysis/check_you_placement.py`, codes only). Bank C's 10 "+ you"
  lines on the push requests (p344, p316, p252, p317, p253; p250's mentions Deutsche by "your size") all put "you"
  before that line's stakes ("Deutsche, if you're not ..., [the stakes]"), so in F "you" can only attend to the stakes
  in UBS's line just before it, and the decision token sees both. In B's file a word list cannot find the stakes in
  half the lines (phrased too variously), so B's "+ you" lines need a reading by eye before any tracing there. Since F
  comes first and tracing is follow-up, this does not hold up the paper's part.
- 20 Oct night: **the first internals readings were saved as float16 and overflowed** (Gemma 3's late-layer values
  exceed float16's ~65,000, so some became infinite); the feature step had stopped without pushing for that reason, and
  the first steering launch was stopped before it steered anything. Fixed: states saved as float32 in `/states/v2/`, each
  checked finite; the old folders are unused. Steering strength changed from a share of the residual's length (which
  Gemma's few very large dimensions dominate) to 2x and 4x the loss - neutral gap along the direction. The readings
  themselves are fast (B's 50 careers in about 4 minutes). Run 1, Run 2 and the steering are being relaunched.
