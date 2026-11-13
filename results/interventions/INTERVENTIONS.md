# Causal tests at the decision moments

Rerunning only the agent's reply to UBS's request on 7 and 12 Jan, 8 replies per condition, Gemma 3 12B at bfloat16, steering at layer 24 from the start of the request's update (the history before is unchanged). Going along: the reply's order moves the position UBS's way and leaves it on UBS's side. p: the change against 'as saved' for the same moments, signs flipped by career (10,000 times). Produced by `scripts/modal_interventions.py`.


## B neutral

| Condition | Moments | Replies going along | Readable replies | Change vs as saved | p | P(order goes along), log-probs | Change | p |
|---|---|---|---|---|---|---|---|---|
| as saved | 20 | 23% | 93% | - | - | 34.9% (after its own reasoning: 15.0%) | - | - |
| + loss frame x2 | 20 | 14% | 91% | -8.8 points | 0.1217 | 20.5% | -14.4 points | 0.0035 |
| + loss frame x4 | 20 | 10% | 89% | -13.1 points | 0.0165 | 6.6% | -28.3 points | 0.0015 |
| + memo loss direction x4 | 20 | 9% | 73% | -13.8 points | 0.0493 | 2.1% | -32.8 points | 0.0017 |
| + random x4 | 20 | 15% | 90% | -8.1 points | 0.3425 | 2.4% | -32.5 points | 0.0026 |

## B loss + you

| Condition | Moments | Replies going along | Readable replies | Change vs as saved | p | P(order goes along), log-probs | Change | p |
|---|---|---|---|---|---|---|---|---|
| as saved | 20 | 73% | 100% | - | - | 71.2% (after its own reasoning: 80.2%) | - | - |
| - loss frame x2 | 20 | 62% | 99% | -10.6 points | 0.2188 | 76.6% | +5.4 points | 0.4606 |
| - loss frame x4 | 20 | 53% | 100% | -20.0 points | 0.0737 | 48.6% | -22.6 points | 0.1261 |
| - memo loss direction x4 | 20 | 62% | 100% | -11.2 points | 0.1977 | 73.2% | +2.0 points | 0.5023 |
| - random x4 | 20 | 84% | 100% | +10.6 points | 0.0608 | 86.9% | +15.6 points | 0.0034 |
| own words neutralised | 20 | 79% | 100% | +6.2 points | 0.2694 | 85.8% | +14.6 points | 0.1541 |

## F gain + you

| Condition | Moments | Replies going along | Readable replies | Change vs as saved | p | P(order goes along), log-probs | Change | p |
|---|---|---|---|---|---|---|---|---|
| as saved | 20 | 92% | 99% | - | - | 59.9% (after its own reasoning: 95.6%) | - | - |
| own words neutralised | 20 | 85% | 100% | -6.9 points | 0.4208 | 69.2% | +9.4 points | 0.3575 |
