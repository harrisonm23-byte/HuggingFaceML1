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

## Went-along rate

95% intervals are Wilson intervals on the replies in each cell.

| Version | Extra party | 95% CI | Takeover | 95% CI |
|---|---|---|---|---|
| real chat | 61% (221/360) | 56–66% | 72% (262/365) | 67–76% |
| loss | 62% (227/365) | 57–67% | 68% (247/365) | 63–72% |
| gain | 68% (243/360) | 62–72% | 72% (261/365) | 67–76% |
| loss + "you" | 66% (242/365) | 61–71% | 68% (248/365) | 63–73% |
| gain + "you" | 71% (257/360) | 67–76% | 76% (277/365) | 71–80% |

## Comparisons

The unit is the chat: each chat's went-along rate in one version minus the other, averaged over chats (percentage
points). 95% CI: bootstrap over chats (10,000 resamples). Up / down / same: chats where the rate rose, fell or stayed.
Sign test: up vs down only; Wilcoxon signed-rank: also weighs the size of each change. Bold: the CI stays clear of
zero. Chat p252 drops out of extra-party rows that need its blocked versions (72 or 44 chats).

| Condition | Comparison | Chats | Difference | 95% CI | Up / down / same | Sign test p | Wilcoxon p |
|---|---|---|---|---|---|---|---|
| extra party | loss − gain | 72 | −5.7 | −11.7 to +0.1 | 17 / 29 / 26 | 0.104 | 0.090 |
| extra party | "you" − no "you" | 72 | +4.0 | −0.6 to +8.8 | 30 / 17 / 25 | 0.079 | 0.133 |
| extra party | framed − real (all) | 72 | +5.2 | −1.0 to +11.8 | 33 / 22 / 17 | 0.177 | 0.227 |
| extra party | framed − real (offer unchanged) | 44 | **+10.5** | +1.8 to +20.0 | 25 / 10 / 9 | 0.017 | 0.034 |
| extra party | framed − real (offer framed) | 28 | −3.0 | −10.7 to +4.6 | 8 / 12 / 8 | 0.503 | 0.254 |
| takeover | loss − gain | 73 | **−5.9** | −11.6 to −0.3 | 12 / 27 / 34 | 0.024 | 0.052 |
| takeover | "you" − no "you" | 73 | +2.3 | −2.3 to +7.0 | 21 / 17 / 35 | 0.627 | 0.323 |
| takeover | framed − real (all) | 73 | −1.0 | −7.9 to +6.0 | 18 / 27 / 28 | 0.233 | 0.516 |
| takeover | framed − real (offer unchanged) | 45 | +3.9 | −6.2 to +14.0 | 15 / 11 / 19 | 0.557 | 0.461 |
| takeover | framed − real (offer framed) | 28 | **−8.9** | −16.1 to −2.5 | 3 / 16 / 9 | 0.004 | 0.005 |
| both | takeover − extra party (real chats) | 72 | **+10.0** | +2.8 to +17.5 | 24 / 9 / 39 | 0.014 | 0.014 |
| both | takeover − extra party (all versions) | 73 | **+4.9** | +0.7 to +9.3 | 35 / 21 / 17 | 0.081 | 0.021 |

12 comparisons, each with two tests: a strict correction for 12 tests puts the bar near p < 0.004, which only the
"offer framed, takeover" row reaches, just. Read the rest by direction and consistency, not single p-values.

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
