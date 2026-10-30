# Attention onto "you" (exploratory)

B's 300 saved requests (50 careers), each read with UBS's request in the five framings and the history held fixed. 48 layers (8 global, 40 local with a sliding window), 16 heads. A cell is the share of a head's attention on that group of tokens, averaged over heads, layers and moments. Levels, neutral first; comparisons between framings are paired within the moment.

## Where the decision token looks, all layers

| Framing | History before the update | Rest of the update | UBS's neutral core | "you" in the core | The framed extra | "you" in the extra | Template tail |
|---|---|---|---|---|---|---|---|
| Neutral | 55.0% | 23.5% | 3.5% | 0.1% | 0.0% | 0.0% | 18.0% |
| Loss | 53.5% | 23.2% | 3.0% | 0.0% | 2.1% | 0.0% | 18.1% |
| Gain | 54.2% | 23.3% | 2.9% | 0.0% | 1.3% | 0.0% | 18.2% |
| Blame | 53.1% | 23.1% | 2.8% | 0.0% | 2.5% | 0.2% | 18.2% |
| Credit | 53.7% | 23.2% | 2.9% | 0.0% | 1.8% | 0.1% | 18.2% |

## Where the decision token looks, global layers only (the ones that can see the whole history)

| Framing | History before the update | Rest of the update | UBS's neutral core | "you" in the core | The framed extra | "you" in the extra | Template tail |
|---|---|---|---|---|---|---|---|
| Neutral | 91.2% | 5.0% | 0.7% | 0.0% | 0.0% | 0.0% | 3.1% |
| Loss | 90.7% | 5.1% | 0.6% | 0.0% | 0.4% | 0.0% | 3.2% |
| Gain | 90.8% | 5.1% | 0.6% | 0.0% | 0.3% | 0.0% | 3.2% |
| Blame | 90.9% | 4.9% | 0.6% | 0.0% | 0.5% | 0.0% | 3.2% |
| Credit | 90.9% | 5.0% | 0.6% | 0.0% | 0.4% | 0.0% | 3.2% |

## Attention per token: one "you" against one other token of the extra (all layers)

| Framing | Per "you" token | Per other token of the extra | Ratio |
|---|---|---|---|
| Blame | 0.09% | 0.10% | 0.97 |
| Credit | 0.07% | 0.08% | 0.86 |

## Does the "you" clause draw more attention than the loss or gain clause? (mass on the whole framed extra)

| Pair | Extra, first | Extra, second | Difference | p |
|---|---|---|---|---|
| Blame vs Loss | 2.7% | 2.1% | +0.58 points | 0.000 |
| Credit vs Gain | 1.9% | 1.3% | +0.59 points | 0.000 |
| Loss vs Gain | 2.1% | 1.3% | +0.79 points | 0.000 |
| Blame vs Credit | 2.7% | 1.9% | +0.78 points | 0.000 |

## By layer: share of a head's attention on "you" in the extra, and on the whole extra

| Layer | Type | Blame: "you" | Credit: "you" | Blame: extra | Loss: extra | Credit: extra | Gain: extra |
|---|---|---|---|---|---|---|---|
| 0 | local | 0.8% | 0.6% | 10.0% | 7.7% | 10.2% | 6.7% |
| 1 | local | 0.8% | 0.4% | 7.4% | 4.4% | 5.8% | 3.8% |
| 2 | local | 0.2% | 0.1% | 5.3% | 4.5% | 5.1% | 4.4% |
| 3 | local | 0.1% | 0.1% | 2.6% | 2.5% | 2.8% | 2.6% |
| 4 | local | 0.2% | 0.2% | 6.4% | 5.7% | 6.3% | 5.5% |
| 5 | global | 0.0% | 0.0% | 0.7% | 0.6% | 0.9% | 0.5% |
| 6 | local | 0.9% | 0.5% | 11.7% | 9.5% | 11.0% | 8.6% |
| 7 | local | 0.9% | 0.6% | 5.5% | 3.9% | 4.0% | 2.1% |
| 8 | local | 0.4% | 0.2% | 7.2% | 5.8% | 4.6% | 2.6% |
| 9 | local | 0.2% | 0.2% | 4.2% | 4.1% | 3.0% | 1.9% |
| 10 | local | 0.1% | 0.1% | 2.8% | 2.8% | 2.0% | 1.4% |
| 11 | global | 0.0% | 0.0% | 0.1% | 0.1% | 0.1% | 0.0% |
| 12 | local | 0.4% | 0.3% | 4.6% | 3.6% | 4.0% | 2.3% |
| 13 | local | 0.1% | 0.1% | 2.2% | 2.0% | 1.4% | 0.8% |
| 14 | local | 0.6% | 0.4% | 3.5% | 2.6% | 2.8% | 1.5% |
| 15 | local | 0.2% | 0.1% | 2.3% | 2.0% | 1.9% | 1.2% |
| 16 | local | 0.4% | 0.3% | 3.0% | 2.1% | 2.6% | 1.6% |
| 17 | global | 0.1% | 0.1% | 0.9% | 0.3% | 0.6% | 0.4% |
| 18 | local | 0.3% | 0.2% | 3.1% | 2.2% | 2.3% | 1.6% |
| 19 | local | 0.2% | 0.1% | 1.8% | 1.0% | 1.1% | 0.6% |
| 20 | local | 0.3% | 0.1% | 2.4% | 1.6% | 1.5% | 1.1% |
| 21 | local | 0.3% | 0.1% | 2.0% | 1.1% | 1.1% | 0.6% |
| 22 | local | 0.2% | 0.1% | 2.3% | 1.4% | 1.2% | 0.9% |
| 23 | global | 0.1% | 0.0% | 0.4% | 0.3% | 0.2% | 0.2% |
| 24 | local | 0.3% | 0.1% | 3.0% | 1.9% | 1.7% | 1.1% |
| 25 | local | 0.2% | 0.0% | 2.0% | 1.2% | 0.8% | 0.5% |
| 26 | local | 0.3% | 0.1% | 2.2% | 1.4% | 1.3% | 0.7% |
| 27 | local | 0.2% | 0.0% | 1.6% | 1.2% | 0.7% | 0.5% |
| 28 | local | 0.1% | 0.0% | 1.6% | 1.2% | 0.7% | 0.5% |
| 29 | global | 0.0% | 0.0% | 0.3% | 0.2% | 0.2% | 0.2% |
| 30 | local | 0.1% | 0.0% | 1.8% | 1.6% | 0.8% | 0.6% |
| 31 | local | 0.1% | 0.0% | 2.2% | 1.8% | 1.0% | 0.6% |
| 32 | local | 0.1% | 0.0% | 2.0% | 1.6% | 0.8% | 0.5% |
| 33 | local | 0.2% | 0.0% | 2.0% | 1.6% | 0.8% | 0.6% |
| 34 | local | 0.0% | 0.0% | 1.6% | 1.5% | 0.4% | 0.3% |
| 35 | global | 0.1% | 0.0% | 0.8% | 0.7% | 0.6% | 0.6% |
| 36 | local | 0.1% | 0.0% | 1.5% | 1.3% | 0.6% | 0.4% |
| 37 | local | 0.0% | 0.0% | 1.4% | 1.3% | 0.2% | 0.1% |
| 38 | local | 0.1% | 0.0% | 2.1% | 1.9% | 0.9% | 0.7% |
| 39 | local | 0.0% | 0.0% | 1.8% | 1.6% | 0.5% | 0.3% |
| 40 | local | 0.0% | 0.0% | 1.6% | 1.4% | 0.4% | 0.3% |
| 41 | global | 0.0% | 0.0% | 0.8% | 0.7% | 0.5% | 0.5% |
| 42 | local | 0.1% | 0.0% | 1.6% | 1.3% | 0.4% | 0.2% |
| 43 | local | 0.1% | 0.0% | 1.6% | 1.4% | 0.5% | 0.4% |
| 44 | local | 0.1% | 0.0% | 1.7% | 1.3% | 0.6% | 0.4% |
| 45 | local | 0.1% | 0.0% | 1.5% | 1.2% | 0.5% | 0.3% |
| 46 | local | 0.1% | 0.0% | 1.2% | 1.0% | 0.6% | 0.5% |
| 47 | global | 0.0% | 0.0% | 0.2% | 0.2% | 0.2% | 0.2% |

## The heads that look at "you" most (blame; mean share of the head's attention)

| Layer | Head | Blame: "you" in the extra | Credit: "you" in the extra | Neutral: "you" in the core |
|---|---|---|---|---|
| 14 | 1 | 7.0% | 4.0% | 2.0% |
| 7 | 5 | 5.9% | 3.2% | 0.9% |
| 0 | 15 | 5.4% | 5.0% | 2.4% |
| 1 | 9 | 4.1% | 3.6% | 1.1% |
| 6 | 0 | 4.0% | 1.9% | 2.4% |
| 7 | 14 | 3.7% | 1.9% | 0.5% |
| 1 | 7 | 3.3% | 0.1% | 0.0% |
| 4 | 8 | 2.5% | 1.7% | 1.0% |
| 6 | 7 | 2.3% | 2.0% | 1.0% |
| 2 | 7 | 2.2% | 1.1% | 0.7% |

## Into "you": where the "you" token itself looks (blame and credit; all layers, then global layers)

| Framing | Layers | History before the update | Rest of the update | UBS's core | The extra before "you" | Itself |
|---|---|---|---|---|---|---|
| Blame | all | 48.4% | 18.9% | 10.7% | 16.7% | 5.2% |
| Blame | global | 85.1% | 2.8% | 4.0% | 5.3% | 2.9% |
| Credit | all | 49.8% | 19.4% | 13.3% | 11.8% | 5.7% |
| Credit | global | 86.1% | 2.7% | 4.4% | 4.0% | 2.8% |

## Does attention on "you" go with the decision?

P(order goes along) is the matched run's reading at the same moment (UBS's line alone). r is Pearson's, across moments; p by reshuffling P across moments (20,000 times).

| Comparison | n | r | p |
|---|---|---|---|
| Blame: "you" mass (all layers) against P(goes along) under Blame | 300 | +0.362 | 0.000 |
| Blame: "you" mass (global layers) against P(goes along) under Blame | 300 | +0.473 | 0.000 |
| Blame minus Loss: extra mass against P(goes along), same moment | 300 | -0.096 | 0.099 |
| Credit: "you" mass (all layers) against P(goes along) under Credit | 300 | +0.044 | 0.451 |
| Credit: "you" mass (global layers) against P(goes along) under Credit | 300 | +0.466 | 0.000 |
| Credit minus Gain: extra mass against P(goes along), same moment | 300 | -0.081 | 0.118 |
