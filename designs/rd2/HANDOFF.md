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

## Next tasks, in order

1. **Bigger chat run via the Gemini API** (the user added `GEMINI_API_KEY` to the environment; never print it, never ask for it in chat).
   - **Status (2026-10-04):** script ready and tested offline: `scripts/gemini_chat_replies.py` (see the NOTES entry). The key was not visible in the session that wrote it, so no API call has been made yet. Next: `--list-models`, then the pilot.
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
