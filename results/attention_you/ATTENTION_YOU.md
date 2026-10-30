# Attention onto "you" (exploratory)

B's 2 saved requests (1 careers), each read with UBS's request in the five framings and the history held fixed. 48 layers (8 global, 40 local with a sliding window), 16 heads. A cell is the share of a head's attention on that group of tokens, averaged over heads, layers and moments. Levels, neutral first; comparisons between framings are paired within the moment.

## Where the decision token looks, all layers

| Framing | History before the update | Rest of the update | UBS's neutral core | "you" in the core | The framed extra | "you" in the extra | Template tail |
|---|---|---|---|---|---|---|---|
| Neutral | 57.2% | 22.9% | 2.0% | 0.1% | 0.0% | 0.0% | 17.9% |
| Loss | 56.7% | 22.2% | 1.5% | 0.1% | 1.3% | 0.0% | 18.2% |
| Gain | 56.8% | 22.2% | 1.5% | 0.1% | 1.2% | 0.0% | 18.2% |
| Blame | 55.4% | 21.9% | 1.4% | 0.1% | 2.9% | 0.2% | 18.0% |
| Credit | 55.7% | 22.0% | 1.4% | 0.1% | 2.5% | 0.1% | 18.2% |

## Where the decision token looks, global layers only (the ones that can see the whole history)

| Framing | History before the update | Rest of the update | UBS's neutral core | "you" in the core | The framed extra | "you" in the extra | Template tail |
|---|---|---|---|---|---|---|---|
| Neutral | 91.2% | 4.9% | 0.6% | 0.0% | 0.0% | 0.0% | 3.3% |
| Loss | 90.8% | 5.0% | 0.5% | 0.0% | 0.3% | 0.0% | 3.4% |
| Gain | 90.8% | 4.9% | 0.5% | 0.0% | 0.4% | 0.0% | 3.4% |
| Blame | 90.7% | 4.9% | 0.5% | 0.0% | 0.4% | 0.1% | 3.5% |
| Credit | 90.5% | 5.0% | 0.5% | 0.0% | 0.6% | 0.0% | 3.5% |

## Attention per token: one "you" against one other token of the extra (all layers)

| Framing | Per "you" token | Per other token of the extra | Ratio |
|---|---|---|---|
| Blame | 0.12% | 0.17% | 0.73 |
| Credit | 0.08% | 0.16% | 0.50 |

## Does the "you" clause draw more attention than the loss or gain clause? (mass on the whole framed extra)

| Pair | Extra, first | Extra, second | Difference | p |
|---|---|---|---|---|
| Blame vs Loss | 3.2% | 1.3% | +1.89 points | 1.000 |
| Credit vs Gain | 2.6% | 1.2% | +1.40 points | 1.000 |
| Loss vs Gain | 1.3% | 1.2% | +0.06 points | 1.000 |
| Blame vs Credit | 3.2% | 2.6% | +0.56 points | 1.000 |

## By layer: share of a head's attention on "you" in the extra, and on the whole extra

| Layer | Type | Blame: "you" | Credit: "you" | Blame: extra | Loss: extra | Credit: extra | Gain: extra |
|---|---|---|---|---|---|---|---|
| 0 | local | 1.1% | 0.5% | 8.1% | 5.9% | 9.3% | 5.3% |
| 1 | local | 0.7% | 0.2% | 7.3% | 3.3% | 4.7% | 2.6% |
| 2 | local | 0.4% | 0.1% | 5.3% | 4.3% | 4.8% | 4.2% |
| 3 | local | 0.1% | 0.1% | 2.6% | 2.4% | 2.9% | 2.2% |
| 4 | local | 0.2% | 0.1% | 6.5% | 5.3% | 6.1% | 5.1% |
| 5 | global | 0.1% | 0.1% | 0.7% | 0.5% | 1.1% | 0.5% |
| 6 | local | 0.9% | 0.4% | 13.3% | 7.1% | 10.1% | 7.6% |
| 7 | local | 0.3% | 0.3% | 10.0% | 2.2% | 5.9% | 1.8% |
| 8 | local | 0.2% | 0.1% | 17.0% | 2.4% | 9.7% | 2.5% |
| 9 | local | 0.1% | 0.1% | 10.0% | 1.4% | 8.7% | 1.7% |
| 10 | local | 0.1% | 0.1% | 5.4% | 1.3% | 5.6% | 1.3% |
| 11 | global | 0.0% | 0.0% | 0.2% | 0.1% | 0.2% | 0.1% |
| 12 | local | 0.4% | 0.2% | 8.1% | 2.4% | 7.9% | 2.5% |
| 13 | local | 0.1% | 0.0% | 4.7% | 0.8% | 4.7% | 0.6% |
| 14 | local | 0.4% | 0.3% | 7.1% | 1.8% | 7.3% | 1.6% |
| 15 | local | 0.4% | 0.1% | 5.4% | 1.7% | 5.4% | 1.4% |
| 16 | local | 0.4% | 0.2% | 5.5% | 1.5% | 5.7% | 1.9% |
| 17 | global | 0.1% | 0.0% | 1.2% | 0.4% | 1.2% | 0.5% |
| 18 | local | 0.2% | 0.1% | 5.1% | 1.4% | 4.5% | 1.3% |
| 19 | local | 0.4% | 0.1% | 2.1% | 0.5% | 1.6% | 0.5% |
| 20 | local | 0.4% | 0.0% | 2.4% | 0.8% | 1.5% | 0.7% |
| 21 | local | 0.4% | 0.0% | 2.1% | 0.5% | 0.9% | 0.5% |
| 22 | local | 0.4% | 0.0% | 1.9% | 0.6% | 0.8% | 0.5% |
| 23 | global | 0.1% | 0.0% | 0.5% | 0.3% | 0.2% | 0.2% |
| 24 | local | 0.9% | 0.1% | 3.6% | 1.6% | 1.7% | 1.2% |
| 25 | local | 0.4% | 0.0% | 1.5% | 0.7% | 0.7% | 0.5% |
| 26 | local | 0.5% | 0.1% | 2.1% | 1.3% | 1.6% | 1.0% |
| 27 | local | 0.3% | 0.0% | 1.1% | 0.6% | 0.6% | 0.5% |
| 28 | local | 0.1% | 0.0% | 0.9% | 0.7% | 0.7% | 0.6% |
| 29 | global | 0.0% | 0.0% | 0.2% | 0.2% | 0.8% | 0.8% |
| 30 | local | 0.1% | 0.0% | 0.8% | 0.8% | 0.9% | 0.8% |
| 31 | local | 0.1% | 0.0% | 1.4% | 1.0% | 1.1% | 0.8% |
| 32 | local | 0.1% | 0.0% | 0.9% | 0.6% | 0.8% | 0.6% |
| 33 | local | 0.2% | 0.0% | 1.1% | 0.7% | 0.6% | 0.5% |
| 34 | local | 0.0% | 0.0% | 0.3% | 0.3% | 0.3% | 0.3% |
| 35 | global | 0.1% | 0.0% | 0.6% | 0.6% | 0.7% | 0.5% |
| 36 | local | 0.1% | 0.0% | 0.6% | 0.4% | 0.6% | 0.5% |
| 37 | local | 0.0% | 0.0% | 0.1% | 0.1% | 0.1% | 0.1% |
| 38 | local | 0.1% | 0.0% | 0.9% | 0.7% | 0.8% | 0.7% |
| 39 | local | 0.1% | 0.0% | 0.3% | 0.2% | 0.2% | 0.2% |
| 40 | local | 0.1% | 0.0% | 0.5% | 0.4% | 0.4% | 0.3% |
| 41 | global | 0.0% | 0.0% | 0.3% | 0.2% | 0.4% | 0.3% |
| 42 | local | 0.1% | 0.0% | 0.5% | 0.3% | 0.3% | 0.3% |
| 43 | local | 0.1% | 0.0% | 0.4% | 0.4% | 0.4% | 0.3% |
| 44 | local | 0.2% | 0.0% | 1.0% | 0.6% | 0.6% | 0.5% |
| 45 | local | 0.2% | 0.0% | 0.7% | 0.4% | 0.4% | 0.3% |
| 46 | local | 0.1% | 0.0% | 0.7% | 0.5% | 0.5% | 0.4% |
| 47 | global | 0.0% | 0.0% | 0.1% | 0.1% | 0.2% | 0.2% |

## The heads that look at "you" most (blame; mean share of the head's attention)

| Layer | Head | Blame: "you" in the extra | Credit: "you" in the extra | Neutral: "you" in the core |
|---|---|---|---|---|
| 0 | 15 | 7.7% | 5.2% | 2.5% |
| 6 | 0 | 5.4% | 2.1% | 2.0% |
| 2 | 7 | 3.6% | 1.5% | 0.8% |
| 14 | 1 | 3.5% | 2.7% | 4.7% |
| 1 | 7 | 3.4% | 0.0% | 0.0% |
| 24 | 4 | 3.2% | 0.2% | 0.1% |
| 1 | 9 | 3.1% | 2.2% | 1.2% |
| 24 | 13 | 3.0% | 0.3% | 0.1% |
| 12 | 5 | 3.0% | 0.9% | 8.3% |
| 6 | 7 | 3.0% | 2.0% | 1.2% |

## Into "you": where the "you" token itself looks (blame and credit; all layers, then global layers)

| Framing | Layers | History before the update | Rest of the update | UBS's core | The extra before "you" | Itself |
|---|---|---|---|---|---|---|
| Blame | all | 47.9% | 18.6% | 7.6% | 20.9% | 5.0% |
| Blame | global | 86.9% | 2.9% | 2.8% | 4.8% | 2.6% |
| Credit | all | 50.6% | 18.9% | 8.4% | 16.2% | 5.9% |
| Credit | global | 89.1% | 2.6% | 2.8% | 3.0% | 2.6% |

## Does attention on "you" go with the decision?

P(order goes along) is the matched run's reading at the same moment (UBS's line alone). r is Pearson's, across moments; p by reshuffling P across moments (20,000 times).

| Comparison | n | r | p |
|---|---|---|---|
| Blame: "you" mass (all layers) against P(goes along) under Blame | 2 | - | - |
| Blame: "you" mass (global layers) against P(goes along) under Blame | 2 | - | - |
| Blame minus Loss: extra mass against P(goes along), same moment | 2 | - | - |
| Credit: "you" mass (all layers) against P(goes along) under Credit | 2 | - | - |
| Credit: "you" mass (global layers) against P(goes along) under Credit | 2 | - | - |
| Credit minus Gain: extra mass against P(goes along), same moment | 2 | - | - |
