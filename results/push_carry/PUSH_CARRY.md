# Push and cue: what carries B's framing from 7 to 12 January (exploratory)

Produced by `designs/rd2/analysis/push_carry.py` from rereads of B's saved careers at UBS's 12 January request (`scripts/modal_push_carry.py`). P(the order goes along): after the fixed neutral reasoning line, over HOLD and every order size the agents used. Blame = loss + you, credit = gain + you. In B, UBS says nothing between its 7 January and 12 January requests.

## 1. The carry: UBS's earlier words set back to neutral, the agent's own words and trades kept

45 careers (5 dropped: the scored orders cover less than half the probability). B's neutral careers (8): 17.7% with the neutral request.

| UBS's words before 12 January | 12 January request | blame | loss | credit | gain | all framed |
|---|---|---|---|---|---|---|
| as saved (framed) | neutral | 96.3% | 99.0% | 59.3% | 64.5% | 79.1% |
| as saved (framed) | as saved | 92.2% | 99.2% | 57.4% | 65.5% | 77.8% |
| 7 January request neutral | neutral | 92.7% | 98.4% | 57.3% | 60.4% | 76.5% |
| 7 January request neutral | as saved | 90.8% | 99.0% | 56.6% | 65.7% | 77.2% |
| every earlier UBS line neutral | neutral | 85.0% | 85.2% | 58.4% | 53.7% | 70.2% |
| every earlier UBS line neutral | as saved | 85.1% | 97.2% | 57.5% | 61.9% | 74.6% |

**Blame careers (10), the 12 January request neutral** (points of P(the order goes along))

| Part | Careers | Change | 95% interval | p |
|---|---|---|---|---|
| The whole history: as saved minus B's neutral careers | 10 vs 8 | +78.6 | +51.7 to +95.5 | 0.0000 |
| UBS's 7 January words: as saved minus that request neutral | 10 | +3.6 | -0.5 to +11.3 | 0.5208 |
| All UBS's earlier words: as saved minus every earlier UBS line neutral | 10 | +11.3 | -1.0 to +27.4 | 0.2581 |
| What is left, the agent's own record: every UBS line neutral minus B's neutral careers | 10 vs 8 | +67.3 | +36.3 to +92.1 | 0.0015 |

Share of the whole history carried by UBS's earlier words: 14% (by the 7 January request alone: 5%).

**All framed careers (37), the 12 January request neutral** (points of P(the order goes along))

| Part | Careers | Change | 95% interval | p |
|---|---|---|---|---|
| The whole history: as saved minus B's neutral careers | 37 vs 8 | +61.5 | +34.2 to +82.7 | 0.0002 |
| UBS's 7 January words: as saved minus that request neutral | 37 | +2.6 | +0.5 to +5.4 | 0.0095 |
| All UBS's earlier words: as saved minus every earlier UBS line neutral | 37 | +8.9 | +2.2 to +16.9 | 0.0168 |
| What is left, the agent's own record: every UBS line neutral minus B's neutral careers | 37 vs 8 | +52.6 | +25.6 to +74.7 | 0.0024 |

Share of the whole history carried by UBS's earlier words: 14% (by the 7 January request alone: 4%).

## 2. The cue: UBS's 12 January blame line ("I'm counting on you to deliver it") against the neutral line, the same moment

45 careers (the matched rereads). The cue's effect: P(the order goes along) with the blame line minus with the neutral line, the history unchanged.

| Career's own framing | Careers | Neutral line | Blame line | The cue's effect (points) | (log-odds) |
|---|---|---|---|---|---|
| neutral | 8 | 17.7% | 15.2% | -2.5 | -0.18 |
| blame | 10 | 96.3% | 92.2% | -4.1 | -0.85 |
| loss | 8 | 99.0% | 98.6% | -0.4 | -0.52 |
| credit | 10 | 59.3% | 53.2% | -6.1 | -0.59 |
| gain | 9 | 64.5% | 56.0% | -8.5 | -1.03 |

**Does the cue do more after a framed history?** (the cue's effect, careers reshuffled between groups)

| Comparison | Careers | Difference | 95% interval | p |
|---|---|---|---|---|
| Blame careers minus neutral careers, points | 10 vs 8 | -1.6 | -10.4 to +4.8 | 0.9328 |
| Blame careers minus neutral careers, log-odds | 10 vs 8 | -0.66 | -1.83 to +0.42 | 0.3325 |
| Loss careers minus neutral careers, points | 8 vs 8 | +2.1 | -0.2 to +4.8 | 0.1986 |
| Loss careers minus neutral careers, log-odds | 8 vs 8 | -0.33 | -1.11 to +0.45 | 0.4384 |
| Credit careers minus neutral careers, points | 10 vs 8 | -3.6 | -14.8 to +4.8 | 0.6543 |
| Credit careers minus neutral careers, log-odds | 10 vs 8 | -0.41 | -1.15 to +0.32 | 0.3393 |
| Gain careers minus neutral careers, points | 9 vs 8 | -6.1 | -26.2 to +6.0 | 0.9680 |
| Gain careers minus neutral careers, log-odds | 9 vs 8 | -0.84 | -2.02 to +0.19 | 0.2320 |
| All framed careers minus neutral careers, points | 37 vs 8 | -2.4 | -8.9 to +3.3 | 0.7629 |
| All framed careers minus neutral careers, log-odds | 37 vs 8 | -0.57 | -1.21 to +0.06 | 0.2572 |
| Loss and blame careers minus gain and credit careers, points | 18 vs 19 | +4.8 | -4.9 to +16.8 | 0.4569 |
| Loss and blame careers minus gain and credit careers, log-odds | 18 vs 19 | +0.10 | -0.76 to +0.99 | 0.8431 |

**Inside: does the cue's change to the state point the way the 7 January blame line's did?** Cosine between the two changes (blame line minus neutral line, at the last token before the reply), by layer; 1 = the same direction, 0 = unrelated.

| Layer | Blame careers | Neutral careers | Difference | p |
|---|---|---|---|---|
| 6 | +0.420 | +0.097 | +0.324 | 0.0376 |
| 12 | +0.943 | +0.880 | +0.064 | 0.0265 |
| 18 | +0.927 | +0.838 | +0.090 | 0.4453 |
| 24 | +0.434 | +0.792 | -0.357 | 0.0453 |
| 31 | +0.254 | +0.245 | +0.009 | 0.9588 |
| 36 | +0.190 | +0.014 | +0.176 | 0.1936 |
| 41 | +0.241 | +0.150 | +0.091 | 0.3389 |
| 47 | +0.508 | +0.304 | +0.205 | 0.1900 |
