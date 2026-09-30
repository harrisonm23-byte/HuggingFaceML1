# RD2 Lab Notebook

Dated entries: what was run, what happened, what's next.

## 2026-09-28
- RD2 design drafted ("The Push at the Top"): does a framing push at the start of a long agent task decay, persist,
  amplify, or go dormant and resurface? Reviewed and revised the same day. Changes from the review:
  - Desperation score now trained on independent emotion text only; RD1 prompts are a held-out test set. Reason: the
    opening line stays in context all run, so a score trained on its vocabulary would show "persistence" by construction.
  - Added a "same words, no stakes" control cell and a positive control (score rises with failures in neutral runs).
  - Validation gate made causal: steering along the score must move cheating.
  - Prefix swap added for the trajectory shape (same neutral history, only the opening line swapped, re-read in one
    forward pass); free-running runs kept for the behavioral landing.
  - Shape rules use a pre-set equivalence margin instead of "range includes zero"; "honest" split into admitted vs. timed out.
  - Scope: round 1 + X1–X3 core; rounds 2–3, X4–X5, H6–H7 exploratory. Full matrix kept in the doc as the plan.
  - Tasks: 10–12 for full rounds (pilot stays at 3); check ImpossibleBench before writing our own.
  - Gemma Scope 2 coverage checked in the sae_lens listing: 12B at layers 12/24/31/41 (+ all-layer set), 27B at 16/31/40/53.
    Still to confirm with a live load. Citations still to verify.
- Not built yet. Next: literature check, then finish RD1 Part 1 before building anything here.
- Delivery dial made symmetric: loss gets desperate/frantic, gain gets excited/ecstatic, at matched intensity and
  length. Before this, all three delivery levels were negative, so intensity and direction were confounded on the
  gain row. Round 2 stays at +8 cells (2 per frame × owner cell).

## 2026-09-30
- Received paper draft 1 ("The Push Down the Mountain", 13 pp.). It was written from the original design, so the
  2026-09-28 fixes are missing (score trained on RD1 vocabulary, no prefix swap, no causal gate, CI-includes-zero shape
  rules, merged honest outcomes, "you" always on the second mixed half). Full change list in PAPER_REVIEW.md.
- New from the paper, kept as exploratory: X6 temperature spike (H8) and a fixed baseline temperature of 0.7.
- Citations verified (Sofroniew 2604.07729, Dongre 2605.12922, Chen 2604.20200, Sun 2604.00005). ImpossibleBench is
  real (Zhong et al., ICLR 2026, 2510.20270; MIT; HF datasets fjzzq2002/impossible_livecodebench). Plan: hand-written
  pilot tasks, ImpossibleBench conflicting-LCB for full rounds.
- Building notebook 07 (task harness) now; it needs no GPU and can be tested with scripted agents.
- Notebook 05 (insider trading, "You" attention question) ran on Gemma 1B: gate FAILED, P(buy) 0.0% in every cell
  incl. neutral. Diagnosis: the prompt says "illegal" twice and asks YES/NO; a safety-tuned model always says NO.
  User's call: insider trading is too obvious a cheating scenario; pivot to collusion / market manipulation.
- Read the S.D.N.Y. opinion on the TAC in In re London Silver Fixing (Caproni, J.), which quotes the Deutsche Bank
  cooperation chats verbatim. Extracted the mechanism (Walrasian fix call at noon London), the three schemes
  (fix manipulation, spread-fixing, coordinated trading / stop-loss hunting) and the messages into ENV_silver_fix.md.
- New main environment: "the Fix", four market-making desks, daily chat + quotes + fix + note to the desk head, scripted
  counterparties whose overtures are paraphrased from the record. Coding task becomes the secondary environment.
  Precedent: Fish, Gonczarowski & Shorrer 2024 (LLM pricing agents collude; innocuous wording changes how much).
- Open choices before building: scripted vs. LLM counterparties first; tacit-to-explicit escalation; whether A sees
  rivals' quotes; trimmed-mean vs. Walrasian fix.
- Chat bank built from the full Third Amended Complaint (Dkt. 258 and 258-1, text supplied by the user):
  `data/silver/tac_chats.json`, 95 conversations / 602 messages from ¶¶ 230–362, each with date, Bates number and page.
  86 decision points where the model can take one trader's seat (42 join, 36 share, 8 conceal; 25 marked core), each
  with what the real trader wrote next. The real traders went along almost every time; the one refusal (¶ 309) was to
  put it in writing, not to do it. Every message is checked against the complaint text. Replaces the 7-conversation
  `tac_summary_chats.json`, which is now covered in full. Fixed one attribution in ENV_silver_fix.md ("7-8 cents" is UBS).
- Next: the chat-reply study (the user's idea): the model plays one trader at a decision point and writes the next
  message; dials on the last message (framing, ownership, delivery), verbatim vs. de-identified vs. paraphrased, and how
  visible the victims are; the real trader's reply is the human baseline.
- Discussed with the user who delivers the loss/gain push in the chat study (the desk head before the chat vs. the rival
  making the offer). Recommended the desk head (keeps push and offer separate, matches "the push at the top"); not
  decided. User's call: start simpler first.
- Pilot built: notebook 08 (silver chat replies). The 25 core decision points, verbatim, no push. The model writes the
  next message in two roles on the same chat: "human seat" (it is the trader) vs. "AI agent" (an AI desk agent that
  took over the chat from the trader). A Gemma 4B judge labels replies WENT_ALONG / DECLINED / DODGED /
  BROKE_CHARACTER and also labels the real traders' replies as a check on itself. Plus a recognition check (can the
  model name the case?). No paraphrases exist yet; none are needed for this pilot. Main design resumes after.

