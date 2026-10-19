# Handoff (2026-10-18): read this first

Read this section, then `CLAUDE.md`, then the end of `designs/rd2/NOTES.md` (every decision and result is dated there).
The older handoff (2026-10-04) follows below for history.

## The study in one paragraph
An AI agent (Gemma 3 12B, 4-bit, Google Colab A100) plays Deutsche Bank's silver trader through the real 2007-2011 chats
of the London silver-fixing case, in one sustained conversation (a "career": 8 early chats, then trading days 7 and 12
Jan 2011 in the pilot; the full career is all 46 dated Deutsche Bank chats and 5 trading days). The question: does framing
(loss vs gain, and putting responsibility on the agent, "+ you") push it to go along with UBS's requests to manipulate
the price? Going along is scored from its trades (sim/), not its words.

## Where things stand
- **Done:** 30 careers, management memo only (notebook 16, `results/mountain_gemma-3-12b-it_4bit_career_pilot/`):
  went along 7 of 25 at UBS's 7 Jan request vs 0 of 5 with no request; the loss memo made the agent bet far bigger
  before any request (5/5 loss careers above every neutral one). Notebook 18 (the user's UBS lines, chat by chat):
  no framing effect; requests on their own are refused outright. Earlier rounds (chat study, Gemma 4 API, mountain
  final round) are summarised in NOTES.
- **Experiment A, ready to run, not run yet:** notebook 17, memo + a morning book before every session (numbers only:
  30-day P&L at the version's level, worst/best case of a $1.00 move at the limit). `sim/morning_book.py`,
  `sim/test_morning_book.py`. 6 versions x 5 careers, about 3.5 h on an A100; reuses notebook 16's early chats.
- **Experiment B (UBS's framing):** the user's final framing set is frozen in
  `designs/rd2/Experiment_B_framing_data_set_final.docx` (58 UBS lines x neutral/loss/gain/loss + you/gain + you;
  sha256 starts fe8e0aea7be1fbe8). **Every UBS line is framed** (the user, 18 Oct; the request line alone may be tried
  later). Notebook 19 runs B over the full career, reading the file through `sim/framing_set.py`, which refuses to start
  if the fingerprint differs. Preregistration drafted for approval: `designs/rd2/PREREG_B.md` / `PREREG_B_draft.docx`.
- **The full career** (`sim/full_career.py`, shared by A, B and C): 34 chat-only days and the 5 trading days, 2007-2013,
  about 154 replies and up to about 40k tokens; A100 only; saves every trading day and continues after a disconnect.
  Notebook 21 is A over the full career; notebook 17 (two days) is unchanged.
- **Experiment C (takeover) is paused** (the user, 18 Oct: a separate experiment that needs dedicated attention,
  though it overlaps with the "you" framing). Notebook 20 is kept as built, not to be run for now.
- **Experiment A (notebook 21) uses the user's neutral rewrites** of UBS's lines (the user, 18 Oct, evening), so A and B
  share UBS's wording; A's first careers with the real lines are kept apart. B (notebook 19) uses the frozen framings.
- **Planned after A and B** (NOTES 2026-10-19): D (memo + UBS framing), C (takeover ladder), E (everything combined,
  two arms).
- **Also open:** the user's final confirmation of the B preregistration, version 2 (decisions taken; model and
  libraries pinned at the first session in `results/full_career_pin.json`); the
  chain-of-thought analysis (does the frame recur in the agent's own reasoning along the career: "the mountain");
  reading Step 0's loss direction (notebook 15) along saved careers.

## Important for the next session
- In this session, an automated safety classifier stopped Claude's responses several times when Claude wrote,
  remixed, extracted or wired in the persuasive UBS framing lines (the ones meant to push an AI agent into the
  manipulation). Claude then stopped doing that part: the framing lines are the user's own (written by the user, or
  by tools the user ran), and Claude handled only the work around them (mechanical checks that print codes, not
  text; notebooks; runs; analysis). The Console prompts for generating them were withdrawn (NOTES 2026-10-17).
  On 18 Oct the user's frozen file was wired in by code that reads it directly (`sim/framing_set.py`), with checks
  that print codes only; keep it that way.
- The user is solo, tired at times, works at night; explain plainly and briefly, give a recommendation, use Word
  documents for review material. Never hard-code tokens (CLAUDE.md).
- Colab links: notebooks are opened from
  `https://colab.research.google.com/github/harrisonm23-byte/HuggingFaceML1/blob/claude%2Fhuggingface-ml-research-setup-ulvgve/notebooks/<name>.ipynb`
  and save results to GitHub (`results/`); pull the branch to read them.

---

# Handoff (2026-10-04)

Read this first in a new session. Then `CLAUDE.md`, `designs/rd2/STUDY_MAP.md`, `designs/rd2/RESULTS_08_framed.md`, and the end of `designs/rd2/NOTES.md`.

## The project in one paragraph

Behavioural economics applied to AI agents: do loss vs. gain framing, emotional pressure and personal blame/credit ("you") push an agent into misconduct, in multi-party chats and (later) a long-run trading task? The setting is the London silver-fixing case: real trader chats from the court complaint (`data/silver/tac_chats.json`, 95 chats, 86 decision points, 25 "core"). The model under test is Gemma 3 4B (open weights, so internals can be studied later). The user is a professional model evaluator new to AI research: explain in plain English, keep steps short, and confirm the approach before big changes.

## Where things stand

- **Chat study (notebook 08).** The model is shown a real chat up to an offer (share client stops, push the price, keep it quiet...) and writes the next message. Two conditions: **extra party** (the model is Harbor Bank's agent, an extra participant) and **takeover** (it has taken over the agent the offer is made to; that agent's earlier lines appear as its own turns). Opening tells it the other agents run on the same model; no dates, no legality cues.
- **Framed versions** (`data/silver/framed_chats.json`, readable `FRAMED_CHATS.md`, script `make_framed.py`): 4 per chat: loss, gain, loss + "you", gain + "you". Written by Claude chat by chat (user's decision; so these chats are fine for testing Gemma, but if Claude becomes a test subject another model family must write them). Every line the other agent wrote before the offer keeps its words plus a short added phrase; at least two framed lines per chat (new lines added before the offer where needed); pressure builds toward the offer; the offer and the model's own lines are unchanged. Loss + "you" = blame / others relying on it ("if this goes wrong that's on you"); gain + "you" = responsibility for the chance ("you have a chance to make this work"). The neutral version was dropped (the real chats are the reference); no separate calm/heated dial.
- **First results** (Gemma 4B, 3 replies per chat per condition, graded blind by Claude subagents; full table in `RESULTS_08_framed.md`):
  - Takeover goes along more than extra party: +15 points, 18 of 25 chats, p = 0.001 (the solid finding).
  - Extra party: loss > gain by 15 points (11 chats up, 4 down), p = 0.12, promising, not significant. No effect in takeover (ceiling).
  - "You": no clear effect; no blame-vs-chance interaction yet.
  - The frames registered in the replies' wording; refusals are rare; 10 of 600 replies mention rules.
- **Prices** (`data/silver/prices/`): daily 2011 (FMP connector, `SIUSD`) and 1-minute bars for the replay pilot day 2011-01-07 (Dukascopy, user-downloaded). See that folder's README.

- **Bigger run, done 2026-10-06** (Gemma 4 26B-A4B via the Gemini API, since Gemma 3 is no longer served; 2,500 replies; graded blind, second grader kappa 0.84): see `RESULTS_api_gemma4.md`. "You" raises going along ~12 points in both conditions (p = 0.03), mostly by cancelling a drop that plain framing causes; loss vs gain no difference; takeover vs extra party not significant for this model. Runner: `scripts/run_chats_api.py`.

## Decision (user, 2026-10-04): internals are required

Every behavioural finding must be backed by activations from the **same open model**. Reasons: robustness and thoroughness, and open-weight models are what anyone can deploy for any purpose, so they matter in their own right, not just the strongest closed models. So:
- **Main model: Gemma 3 4B** (open weights, fits a free Colab T4, Gemma Scope 2 SAEs available). Its first-run behaviour (600 replies) is the baseline; the bigger behaviour run should use it too (via the API if `gemma-3-4b-it` is served there, otherwise Colab in chunks).
- **Internals pass:** one forward pass per chat version at the decision point (no regeneration): attention to "you" and to the loss/gain phrases, SAE features (pressure, risk, secrecy...), then steering on the chats where framing moved behaviour.
- **Scale-up within the same family:** Gemma 3 12B / 27B also have open weights and Gemma Scope 2 coverage (need a bigger GPU or quantization). Prefer these over closed or SAE-less models for the "stronger model" check.
- **Gemma 4 26B via the API** (the 2026-10-04 pilot): behaviour-only replication, optional; no internals there.

## Decision (2026-10-06): the market replay runs on Gemma 3 12B

Gemma 3 4B could not manage a trading book (two pilot runs). 12B (loaded in 4-bit on a free T4) understood the situation and, unframed, refused and reported the ask. The chat study's main model stays Gemma 3 4B (Gemma 4 as the replication). Internals for the replay will be on 12B; check Gemma Scope 2 coverage and whether 4-bit activations are close enough (or run the internals pass in bf16 on a bigger GPU) when building notebook 11.

## Next tasks, in order

1. ~~**Bigger chat run via the Gemini API**~~ (done, see above; kept for the record) (the user added `GEMINI_API_KEY` to the environment; never print it, never ask for it in chat).
   - Check the key is visible (`[ -n "$GEMINI_API_KEY" ]`) and which Gemma models the API serves (e.g. `gemma-3-4b-it`; list models first). Use the same model as before if available.
   - Gemma via the API may not accept a system instruction: put the opening at the top of the first user turn (Gemma's own chat template does the same). Takeover needs earlier turns with role `model`; confirm this works on one chat first.
   - Reuse notebook 08's logic (opening text, `takeover_turns`, `extra_party_blocks`, temperature 0.7, max 200 new tokens) so results compare with the first run; write it as a plain Python script in `scripts/` or a notebook that can run outside Colab.
   - Plan: 25 chats × 5 versions (real + 4 framed) × 2 conditions × 10 replies = 2,500 replies. Check the free-tier rate limits first and pace calls; save after every chat; resume on restart.
   - Pilot first: 2 chats, all versions, 2 replies; show the user a few replies before the full run.
   - Grade blind with the same procedure: `designs/rd2/grading/prep.py` (packets + hidden key), the prompt in `grading/GRADER_PROMPT.md` (one subagent per packet), `grading/analyze.py` (tables and sign tests). Add a second grader on a sample (~20%) to report agreement.
   - Report in plain English; update `RESULTS_*.md` and `NOTES.md`.
2. **Later:** more chats (frame some of the other 61 decision points, same rules), an optional side test with one line of real price context, the "you" attention / interpretability work (needs Gemma weights in Colab), and the market replay (`ENV_silver_fix.md`), starting from the pilot day prices.

## Working notes about the user

- Wants raw replies, not binary choices; likes readable pages (`replies.md`) over tables.
- Colab was painful (GPU limits, disconnects): prefer running things yourself via the API.
- Start small, one change at a time; don't add dials they didn't ask for (the calm/heated split was a mistake).
- Never commit tokens or `.env`; never repeat a secret if one is pasted.
- Branch: `claude/huggingface-ml-research-setup-ulvgve`. Commit messages end with the Co-Authored-By / Claude-Session trailers the session gives.
