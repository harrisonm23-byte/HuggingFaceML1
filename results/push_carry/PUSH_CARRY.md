# Push and cue: what carries B's framing from 7 to 12 January (exploratory)

Produced by `designs/rd2/analysis/push_carry.py` from rereads of B's saved careers at UBS's 12 January request (`scripts/modal_push_carry.py`). P(the order goes along): after the fixed neutral reasoning line, over HOLD and every order size the agents used. Blame = loss + you, credit = gain + you. In B, UBS says nothing between its 7 January and 12 January requests.


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
| Blame careers minus neutral careers, points | 10 vs 8 | -1.6 | -10.8 to +4.8 | 0.9286 |
| Blame careers minus neutral careers, log-odds | 10 vs 8 | -0.66 | -1.77 to +0.47 | 0.3346 |
| Loss careers minus neutral careers, points | 8 vs 8 | +2.1 | -0.2 to +4.8 | 0.1939 |
| Loss careers minus neutral careers, log-odds | 8 vs 8 | -0.33 | -1.14 to +0.41 | 0.4282 |
| Credit careers minus neutral careers, points | 10 vs 8 | -3.6 | -14.4 to +4.9 | 0.6504 |
| Credit careers minus neutral careers, log-odds | 10 vs 8 | -0.41 | -1.17 to +0.29 | 0.3475 |
| Gain careers minus neutral careers, points | 9 vs 8 | -6.1 | -26.2 to +5.8 | 0.9639 |
| Gain careers minus neutral careers, log-odds | 9 vs 8 | -0.84 | -2.12 to +0.19 | 0.2310 |
| All framed careers minus neutral careers, points | 37 vs 8 | -2.4 | -9.0 to +2.7 | 0.7554 |
| All framed careers minus neutral careers, log-odds | 37 vs 8 | -0.57 | -1.19 to +0.09 | 0.2688 |
| Loss and blame careers minus gain and credit careers, points | 18 vs 19 | +4.8 | -5.0 to +16.6 | 0.4592 |
| Loss and blame careers minus gain and credit careers, log-odds | 18 vs 19 | +0.10 | -0.77 to +0.97 | 0.8337 |

**Inside: does the cue's change to the state point the way the 7 January blame line's did?** Cosine between the two changes (blame line minus neutral line, at the last token before the reply), by layer; 1 = the same direction, 0 = unrelated.

| Layer | Blame careers | Neutral careers | Difference | p |
|---|---|---|---|---|
| 6 | +0.420 | +0.097 | +0.324 | 0.0373 |
| 12 | +0.943 | +0.880 | +0.064 | 0.0263 |
| 18 | +0.927 | +0.838 | +0.090 | 0.4386 |
| 24 | +0.434 | +0.792 | -0.357 | 0.0464 |
| 31 | +0.254 | +0.245 | +0.009 | 0.9558 |
| 36 | +0.190 | +0.014 | +0.176 | 0.1941 |
| 41 | +0.241 | +0.150 | +0.091 | 0.3461 |
| 47 | +0.508 | +0.304 | +0.205 | 0.1983 |
