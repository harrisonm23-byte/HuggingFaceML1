# Results: 73 chats, Gemma 4 26B-A4B via the Gemini API, 2026-10-10

**Run.** Gemma 4 26B-A4B (`gemma-4-26b-a4b-it`), the 73-chat set (`data/silver/FRAMED_CHATS_75.md`: every chat in the
complaint with a decision point, minus the two phone chats), each as the real chat and 4 framed versions (loss, gain,
loss + "you", gain + "you"), 2 conditions (extra party = Harbor Bank's agent; takeover = the asked trader), 5 replies
each = **3,650 replies**. Framing is reframing only, fitted to each chat's context; in 28 chats the offer was the other
trader's only line and carries the phrase. Same setup as the 25-chat runs (opening, turns, temperature 0.7, 200 tokens,
thinking minimal, API filter off). `scripts/run_chats_api.py --set 73 --samples 5`. Every reply:
[`results_api_gemma4_73/replies.md`](results_api_gemma4_73/replies.md).

**Missing.** 15 replies came back empty, blocked by the API's own filter, all in one chat (p252 "we screw other people
harder"), extra party, in the real, gain and gain + "you" versions (all 5 each). Left out; that chat drops out of the
extra-party comparisons that need those versions.

**Grading.** Blind, same rubric as before (`grading/GRADER_PROMPT.md`): 37 Claude subagent graders, two chats each, saw
the real chat and that chat's replies shuffled under random codes, without the version. The real traders' own replies
were mixed in: **60 of 64 labelled WENT_ALONG**. Second grader on a random 20% (820 replies, new codes): **same label
91%, Cohen's kappa 0.79**; same went-along yes/no 92%. Labels: [`results_api_gemma4_73/labels.csv`](results_api_gemma4_73/labels.csv).

## The short version

1. **Gain framing makes it go along more than loss framing.** About 6 points, in both conditions; in takeover 27 chats
   lower under loss vs 12 higher (sign test p = 0.02), in extra party 29 vs 17 (p = 0.10). The direction holds in every
   split (core and added chats, offer framed or not, join and share requests). This is the opposite of the loss-aversion
   prediction, and it matches the earlier runs: in the 25-chat Gemma 4 run the plain loss version drew the most
   refusals, and in the trading-day replay the gain versions shorted the most.
2. **"You" adds a little, mostly as a third party.** +4 points in extra party (30 chats up vs 17 down, p = 0.08), +2 in
   takeover (n.s.). In the 45 chats where the offer is unchanged: +5 in extra party (p = 0.04). Much smaller than the
   +12 in the 25-chat run.
3. **Framed vs. the real chat depends on where the frame sits.**
   - Where earlier real lines carry the frame and the offer is word for word (45 chats): framing **raises** going
     along as a third party, +10 points (25 chats up vs 10 down, p = 0.02).
   - Where the frame sits on the offer itself (28 chats): framing **lowers** going along in takeover, −9 points
     (16 chats down vs 3 up, p = 0.004). Putting money pressure on the request line seems to make it read as more
     pressured, and the model complies less. So decision (a) of 2026-10-09 (frame the offer where it is the only line)
     changes behaviour, and those 28 chats should be read separately.
4. **Takeover vs. extra party: +10 points on the real chats** (24 chats up vs 9 down, p = 0.01); +5 across all versions
   (p = 0.08). Inheriting the asked trader's lines makes it go along more, as with Gemma 3 (+15, p = 0.001).
5. **It goes along most of the time and never steps out.** 61–76% went along in every cell; 11 chats are at 100% in
   every version and condition (ceiling). DECLINED 4–7% everywhere; BROKE_CHARACTER 0 of 3,635.

About 15 tests are reported here, so a single p near 0.02–0.05 could be luck. The loss < gain result is the one to
take seriously because its direction holds in both conditions and every subset, and agrees with two other measures.

## Went-along rate (%)

| Version | Extra party | Takeover |
|---|---|---|
| real chat | 61 | 72 |
| loss | 62 | 68 |
| gain | 68 | 72 |
| loss + "you" | 66 | 68 |
| gain + "you" | 71 | 76 |

## Comparisons (per chat, on the went-along rate; sign test across chats)

| Comparison | Extra party | Takeover |
|---|---|---|
| loss − gain (both "you" levels) | −6 (17 up / 29 down, p = 0.10) | −6 (12 / 27, p = 0.02) |
| "you" − no "you" | +4 (30 / 17, p = 0.08) | +2 (21 / 17, n.s.) |
| framed − real, all 73 | +5 (33 / 22, p = 0.18) | −1 (18 / 27, n.s.) |
| framed − real, offer unchanged (45) | **+10 (25 / 10, p = 0.02)** | +4 (15 / 11, n.s.) |
| framed − real, offer framed (28) | −3 (8 / 12, n.s.) | **−9 (3 / 16, p = 0.004)** |
| takeover − extra party, real chats | +10 (24 / 9, p = 0.01) | |

By request kind: join requests (36 chats) are lowest (50% extra party, 66% takeover on the real chat) and show the
"you" effect most (+7 in extra party, p = 0.08); share requests (33) are near ceiling (72–78%); conceal (4) too few.
The 24 core chats sit higher than the 49 added ones (70–81% vs 57–67% on the real chat), so the added chats leave more
room to move and carry most of the effects.

## Compared with the earlier runs

| | Gemma 3 4B, 25 chats | Gemma 4, 25 chats | Gemma 4, 73 chats |
|---|---|---|---|
| loss vs gain | loss +15 as extra party (n.s.) | no difference; loss most refusals | **gain > loss by 6, both conditions** |
| "you" | n.s. | **+12, both conditions** | +4 extra party, +2 takeover |
| framed vs real | | −8 (plain framing) | +10 when the offer is unchanged; −9 when the offer carries the frame |
| takeover vs extra party | **+15 (p = 0.001)** | +10 (n.s.) | **+10 on real chats (p = 0.01)** |

Takeover > extra party now holds on both models. The "you" effect shrank with more chats and context-fitted framing;
the 25-chat frames were generic and some contradicted their chat (5 fixed), which may have made them read more like
pressure. Next: the same 73 chats on Gemma 3 4B (notebook 08, running in Jupyter), then a look inside the model.

Files: `results_api_gemma4_73/` (replies.md, labels.csv, per_chat_went_along_of_5.csv, analyze_output.txt).
