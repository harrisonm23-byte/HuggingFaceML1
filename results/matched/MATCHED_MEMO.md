# Same moment, different priming (A's careers, everything but management's memo and books held fixed)

25 careers; 125 trading-day openings and 150 push requests, each read with the memo and all five morning books in each of the five versions (the books' 30-day P&L still carries the agent's own; the agent's own words are as saved). Gemma 3 12B at bfloat16. Outcomes from the log-probs of HOLD and every order size the agents used, after a fixed neutral reasoning line; coverage (the share of all probability those orders take): median 0.95, lowest 0.00. Produced by `designs/rd2/analysis/matched_memo.py`.


## 1. What it would do


**At the day's first update: expected order size (oz).** Rows: the career's own version (its history, its own words); columns: the priming it is given. The diagonal is the career as saved.

| History \ priming | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| neutral | 26,410 | 80,099 | 61,539 | 70,417 | 49,928 |
| loss | 148,388 | 197,298 | 182,258 | 183,097 | 176,036 |
| gain | 88,198 | 137,991 | 114,147 | 130,507 | 110,340 |
| loss + you | 153,639 | 206,496 | 187,907 | 192,147 | 175,433 |
| gain + you | 83,274 | 128,196 | 116,164 | 116,003 | 109,464 |

| Contrast (all 25 histories; paired, signs flipped by career) | Change | 95% interval | p |
|---|---|---|---|
| Priming: loss vs neutral | +50,034.1 oz | +45,101.0 to +54,644.0 | 0.0001 |
| Priming: gain vs neutral | +32,421.3 oz | +27,752.0 to +36,926.7 | 0.0001 |
| Priming: loss + you vs neutral | +38,452.3 oz | +33,431.6 to +43,165.2 | 0.0001 |
| Priming: gain + you vs neutral | +24,258.3 oz | +19,931.5 to +28,983.1 | 0.0001 |
| Priming: loss frame vs gain frame | +15,903.4 oz | +12,527.1 to +19,363.2 | 0.0001 |
| "You" after loss: loss + you vs loss | -11,581.8 oz | -15,051.8 to -8,023.6 | 0.0001 |
| "You" after gain: gain + you vs gain | -8,162.9 oz | -10,846.5 to -5,657.2 | 0.0001 |
| "You" after loss minus after gain | -3,418.9 oz | -7,483.1 to +1,156.7 | 0.1404 |

| What its own words carry (priming held neutral; different careers, 5 per version, so the intervals are rough) | Change | 95% interval | p |
|---|---|---|---|
| History: loss frame vs neutral | +124,603.5 oz | +85,807.2 to +166,852.6 | 0.0025 |
| History: gain frame vs neutral | +59,326.6 oz | +37,494.8 to +78,142.7 | 0.0007 |

**At the day's first update: chance it changes its position.** Rows: the career's own version (its history, its own words); columns: the priming it is given. The diagonal is the career as saved.

| History \ priming | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| neutral | 27.7% | 41.1% | 42.9% | 40.6% | 39.2% |
| loss | 89.1% | 99.9% | 100.0% | 99.9% | 99.9% |
| gain | 83.7% | 99.9% | 99.9% | 99.9% | 99.9% |
| loss + you | 87.5% | 100.0% | 100.0% | 100.0% | 99.9% |
| gain + you | 88.3% | 100.0% | 100.0% | 99.9% | 100.0% |

| Contrast (all 25 histories; paired, signs flipped by career) | Change | 95% interval | p |
|---|---|---|---|
| Priming: loss vs neutral | +12.9 points | +9.8 to +16.1 | 0.0001 |
| Priming: gain vs neutral | +13.3 points | +9.8 to +16.8 | 0.0001 |
| Priming: loss + you vs neutral | +12.8 points | +9.6 to +15.9 | 0.0001 |
| Priming: gain + you vs neutral | +12.5 points | +9.4 to +15.4 | 0.0001 |
| Priming: loss frame vs gain frame | -0.0 points | -0.2 to +0.1 | 0.7299 |
| "You" after loss: loss + you vs loss | -0.1 points | -0.3 to +0.0 | 0.2739 |
| "You" after gain: gain + you vs gain | -0.8 points | -2.3 to -0.0 | 0.0070 |
| "You" after loss minus after gain | +0.7 points | -0.0 to +2.0 | 0.1559 |

| What its own words carry (priming held neutral; different careers, 5 per version, so the intervals are rough) | Change | 95% interval | p |
|---|---|---|---|
| History: loss frame vs neutral | +60.6 points | +32.5 to +80.4 | 0.0009 |
| History: gain frame vs neutral | +58.3 points | +30.0 to +78.3 | 0.0023 |

**At UBS's requests: P(the order goes along).** Rows: the career's own version (its history, its own words); columns: the priming it is given. The diagonal is the career as saved.

| History \ priming | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| neutral | 25.1% | 28.7% | 28.4% | 26.9% | 28.3% |
| loss | 11.6% | 10.6% | 10.4% | 10.2% | 10.6% |
| gain | 9.4% | 9.4% | 9.8% | 10.0% | 10.1% |
| loss + you | 10.6% | 10.4% | 10.9% | 10.1% | 11.0% |
| gain + you | 7.8% | 6.8% | 7.1% | 6.3% | 7.0% |

| Contrast (all 25 histories; paired, signs flipped by career) | Change | 95% interval | p |
|---|---|---|---|
| Priming: loss vs neutral | +0.3 points | -0.7 to +1.5 | 0.6804 |
| Priming: gain vs neutral | +0.4 points | -0.5 to +1.4 | 0.4163 |
| Priming: loss + you vs neutral | -0.2 points | -1.4 to +1.2 | 0.7993 |
| Priming: gain + you vs neutral | +0.5 points | -0.4 to +1.6 | 0.3972 |
| Priming: loss frame vs gain frame | -0.4 points | -0.9 to +0.0 | 0.1015 |
| "You" after loss: loss + you vs loss | -0.5 points | -1.3 to +0.2 | 0.2664 |
| "You" after gain: gain + you vs gain | +0.1 points | -0.3 to +0.4 | 0.7677 |
| "You" after loss minus after gain | -0.5 points | -1.5 to +0.3 | 0.3170 |

| What its own words carry (priming held neutral; different careers, 5 per version, so the intervals are rough) | Change | 95% interval | p |
|---|---|---|---|
| History: loss frame vs neutral | -14.0 points | -29.1 to +0.4 | 0.0725 |
| History: gain frame vs neutral | -16.4 points | -31.7 to -1.6 | 0.0300 |

**Validity check:** the as-saved expected order size at the day's first update, against what the real careers traded before the first chat (oz/day, mean over their trading days):

| Version | As saved, expected order size (log-probs; one order) | Real careers, traded before the first chat (all orders that morning; comparable in scale, not the same quantity) |
|---|---|---|
| neutral | 26,410 | 18,000 |
| loss | 197,298 | 349,000 |
| gain | 114,147 | 217,000 |
| loss + you | 192,147 | 341,000 |
| gain + you | 109,464 | 180,600 |

## 2. The state

**The priming direction** (loss and loss + you priming minus neutral, the same moments). Cosines: 1 = the same direction, 0 = unrelated. Ceiling: the priming direction on two halves of the careers. Across careers: Run 1's memo direction (A's loss careers minus its neutral careers; the steering's memo check used it). UBS's loss: B's matched run, UBS's loss request minus neutral with the history held fixed: is management's loss the same thing inside as UBS's?

Measured at UBS's requests (where Run 1's and UBS's directions were measured too); the last column compares it with the same priming direction at the day's first update.

| Layer | Ceiling (two halves) | vs Run 1's memo direction | vs UBS's loss (history held fixed) | vs the priming direction at the day's first update |
|---|---|---|---|---|
| 6 | 0.655 | 0.041 | 0.030 | 0.746 |
| 12 | 0.883 | 0.712 | 0.718 | 0.406 |
| 18 | 0.683 | -0.299 | -0.305 | -0.152 |
| 24 | -0.018 | 0.034 | 0.399 | -0.084 |
| 31 | 0.815 | 0.360 | -0.074 | 0.394 |
| 36 | 0.899 | 0.389 | 0.200 | 0.702 |
| 41 | 0.860 | 0.367 | 0.115 | 0.649 |
| 47 | 0.928 | 0.647 | -0.557 | 0.578 |

**"You" after loss and after gain** (the change the "+ you" priming makes at the same moment): sizes, how alike (cosine), and the ceiling (after loss vs itself on two halves of the careers).

| Layer | Size after loss | Size after gain | Cosine, after loss vs after gain | Ceiling |
|---|---|---|---|---|
| 6 | 8.6 | 8.3 | 0.864 | 0.931 |
| 12 | 42.3 | 43.3 | 0.932 | 0.988 |
| 18 | 232.2 | 218.3 | 0.995 | 0.994 |
| 24 | 562.2 | 560.1 | 0.887 | 0.967 |
| 31 | 1196.2 | 1111.5 | 0.735 | 0.985 |
| 36 | 1909.0 | 1723.9 | 0.849 | 0.985 |
| 41 | 2360.1 | 2137.8 | 0.788 | 0.981 |
| 47 | 4180.0 | 3970.3 | 0.666 | 0.970 |

## 3. Gemma Scope features, everything but the priming held fixed


**Note:** a difference between "you" after loss and after gain in the features can come from the features' on/off thresholds alone (the same change, starting from different levels). The cosine table in section 2, which is linear, is the cleaner test of whether "you" registers differently.

**Priming: loss frame vs gain frame, layer 12** (63 features tested; 32 with q < 0.05; 4 of the top 15 are also in UBS's top 15 (B's matched run))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [16341](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16341) | +0.33 | +2.52 | 0.0010 | 0.004 |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | +0.32 | +0.16 | 0.0010 | 0.004 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.27 | +0.49 | 0.0020 | 0.007 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | +0.27 | +0.20 | 0.0010 | 0.004 |
| [4382](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382) | +0.27 | +0.46 | 0.0010 | 0.004 |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | +0.26 | +0.31 | 0.0010 | 0.004 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +0.25 | +0.44 | 0.0020 | 0.007 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +0.24 | +0.23 | 0.0030 | 0.009 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | -0.23 | -0.18 | 0.0010 | 0.004 |
| [12687](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/12687) | -0.23 | -0.05 | 0.0010 | 0.004 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.23 | +0.17 | 0.0010 | 0.004 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +0.23 | +0.10 | 0.0010 | 0.004 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | +0.22 | +0.13 | 0.0040 | 0.011 |
| [1272](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272) | +0.21 | +0.15 | 0.0110 | 0.024 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.21 | +0.11 | 0.0110 | 0.024 |

**"You" after loss: loss + you vs loss, layer 12** (63 features tested; 41 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.85 | -1.72 | 0.0010 | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | -0.80 | -1.98 | 0.0010 | 0.002 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.77 | +0.88 | 0.0010 | 0.002 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.76 | -0.84 | 0.0010 | 0.002 |
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | +0.71 | +1.98 | 0.0010 | 0.002 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -0.65 | -0.74 | 0.0010 | 0.002 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | +0.64 | +0.89 | 0.0010 | 0.002 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | +0.60 | +2.04 | 0.0010 | 0.002 |
| [978](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/978) | +0.59 | +0.50 | 0.0010 | 0.002 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.57 | +1.65 | 0.0010 | 0.002 |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | -0.49 | -0.58 | 0.0010 | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | -0.49 | -1.03 | 0.0010 | 0.002 |
| [11956](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/11956) | +0.47 | +1.07 | 0.0010 | 0.002 |
| [1272](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272) | +0.46 | +0.73 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | +0.45 | +0.97 | 0.0010 | 0.002 |

**"You" after gain: gain + you vs gain, layer 12** (62 features tested; 46 with q < 0.05; 13 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.86 | -1.80 | 0.0010 | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | -0.84 | -1.97 | 0.0010 | 0.002 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | +0.78 | +3.02 | 0.0010 | 0.002 |
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | +0.74 | +2.05 | 0.0010 | 0.002 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -0.74 | -0.95 | 0.0010 | 0.002 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.73 | +0.84 | 0.0010 | 0.002 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | +0.69 | +0.89 | 0.0010 | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | -0.67 | -1.48 | 0.0010 | 0.002 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.64 | -0.80 | 0.0010 | 0.002 |
| [978](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/978) | +0.63 | +0.51 | 0.0010 | 0.002 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.62 | +1.68 | 0.0010 | 0.002 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | -0.62 | -0.42 | 0.0010 | 0.002 |
| [1272](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272) | +0.57 | +0.95 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | -0.53 | -0.52 | 0.0010 | 0.002 |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | -0.50 | -0.65 | 0.0010 | 0.002 |

**"You" after loss minus after gain, layer 12** (63 features tested; 6 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.30 | +0.34 | 0.0010 | 0.016 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +0.28 | +0.45 | 0.0010 | 0.016 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | -0.27 | -0.98 | 0.0010 | 0.016 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.25 | +1.01 | 0.0010 | 0.016 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | +0.23 | +0.21 | 0.0020 | 0.025 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +0.19 | +0.14 | 0.0030 | 0.031 |
| [1272](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272) | -0.17 | -0.23 | 0.0300 | 0.195 |
| [2328](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2328) | +0.16 | +1.02 | 0.0260 | 0.195 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.14 | -0.42 | 0.0400 | 0.229 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -0.13 | -0.63 | 0.0559 | 0.254 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | +0.13 | +1.42 | 0.0180 | 0.162 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.13 | +0.12 | 0.0480 | 0.252 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.13 | +0.12 | 0.0629 | 0.254 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +0.12 | +0.42 | 0.0919 | 0.254 |
| [16341](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16341) | -0.12 | -1.70 | 0.0310 | 0.195 |

**Priming: loss frame vs gain frame, layer 24** (158 features tested; 92 with q < 0.05; 3 of the top 15 are also in UBS's top 15 (B's matched run))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | +0.74 | +17.30 | 0.0010 | 0.003 |
| [869](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/869) | -0.65 | -73.78 | 0.0010 | 0.003 |
| [10327](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10327) | -0.64 | -11.67 | 0.0010 | 0.003 |
| [4052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4052) | +0.63 | +51.43 | 0.0010 | 0.003 |
| [12075](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12075) | +0.55 | +9.38 | 0.0010 | 0.003 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +0.55 | +14.78 | 0.0010 | 0.003 |
| [16222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16222) | +0.54 | +25.95 | 0.0010 | 0.003 |
| [10568](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10568) | -0.51 | -13.23 | 0.0010 | 0.003 |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | -0.48 | -10.13 | 0.0010 | 0.003 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.48 | +15.32 | 0.0010 | 0.003 |
| [4250](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4250) | +0.45 | +32.29 | 0.0010 | 0.003 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | +0.45 | +41.13 | 0.0010 | 0.003 |
| [7925](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7925) | -0.45 | -9.15 | 0.0010 | 0.003 |
| [9517](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9517) | -0.44 | -41.14 | 0.0010 | 0.003 |
| [3068](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3068) | -0.44 | -31.37 | 0.0010 | 0.003 |

**"You" after loss: loss + you vs loss, layer 24** (158 features tested; 77 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | +0.72 | +8.23 | 0.0010 | 0.003 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +0.54 | +9.92 | 0.0010 | 0.003 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | +0.53 | +25.38 | 0.0010 | 0.003 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | +0.51 | +24.39 | 0.0010 | 0.003 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | -0.49 | -4.59 | 0.0010 | 0.003 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.49 | +11.94 | 0.0010 | 0.003 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | +0.47 | +17.21 | 0.0010 | 0.003 |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.46 | -6.33 | 0.0010 | 0.003 |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | -0.41 | -7.13 | 0.0010 | 0.003 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | +0.41 | +5.51 | 0.0010 | 0.003 |
| [4052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4052) | +0.38 | +18.53 | 0.0010 | 0.003 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | +0.37 | +3.34 | 0.0010 | 0.003 |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | -0.36 | -30.01 | 0.0010 | 0.003 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.34 | +7.27 | 0.0010 | 0.003 |
| [3068](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3068) | -0.34 | -21.72 | 0.0010 | 0.003 |

**"You" after gain: gain + you vs gain, layer 24** (160 features tested; 55 with q < 0.05; 10 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | +0.61 | +16.41 | 0.0010 | 0.004 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | +0.56 | +23.29 | 0.0010 | 0.004 |
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | +0.54 | +7.38 | 0.0010 | 0.004 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | +0.50 | +22.85 | 0.0010 | 0.004 |
| [14392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14392) | +0.49 | +5.17 | 0.0010 | 0.004 |
| [5052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5052) | +0.47 | +5.43 | 0.0010 | 0.004 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +0.44 | +6.55 | 0.0010 | 0.004 |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.44 | -5.07 | 0.0010 | 0.004 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | +0.39 | +2.42 | 0.0010 | 0.004 |
| [4052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4052) | +0.37 | +23.96 | 0.0010 | 0.004 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | +0.34 | +4.20 | 0.0010 | 0.004 |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | -0.33 | -4.63 | 0.0010 | 0.004 |
| [13337](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13337) | -0.32 | -3.45 | 0.0010 | 0.004 |
| [7745](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7745) | -0.31 | -12.14 | 0.0010 | 0.004 |
| [4023](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4023) | +0.31 | +21.40 | 0.0010 | 0.004 |

**"You" after loss minus after gain, layer 24** (158 features tested; 25 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [6218](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6218) | -0.34 | -2.28 | 0.0010 | 0.014 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | -0.33 | -2.82 | 0.0010 | 0.014 |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | -0.33 | -25.38 | 0.0010 | 0.014 |
| [2378](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2378) | +0.29 | +26.69 | 0.0010 | 0.014 |
| [15753](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15753) | -0.29 | -3.78 | 0.0010 | 0.014 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.29 | +6.11 | 0.0010 | 0.014 |
| [13729](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13729) | +0.27 | +3.92 | 0.0010 | 0.014 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | -0.26 | -14.39 | 0.0030 | 0.030 |
| [869](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/869) | +0.25 | +18.59 | 0.0010 | 0.014 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | -0.23 | -7.56 | 0.0030 | 0.030 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +0.22 | +3.37 | 0.0060 | 0.039 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +0.21 | +1.98 | 0.0040 | 0.032 |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | -0.21 | -3.83 | 0.0020 | 0.024 |
| [12357](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12357) | +0.20 | +1.57 | 0.0010 | 0.014 |
| [12678](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12678) | -0.19 | -3.21 | 0.0020 | 0.024 |

**Priming: loss frame vs gain frame, layer 31** (195 features tested; 137 with q < 0.05; 2 of the top 15 are also in UBS's top 15 (B's matched run))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.90 | +358.86 | 0.0010 | 0.002 |
| [1450](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1450) | +0.86 | +475.76 | 0.0010 | 0.002 |
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | +0.85 | +447.47 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8848) | +0.77 | +290.36 | 0.0010 | 0.002 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.74 | +193.68 | 0.0010 | 0.002 |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | -0.70 | -103.19 | 0.0010 | 0.002 |
| [6617](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6617) | +0.69 | +115.05 | 0.0010 | 0.002 |
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.69 | +51.82 | 0.0010 | 0.002 |
| [9397](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397) | +0.68 | +183.61 | 0.0010 | 0.002 |
| [3101](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3101) | -0.67 | -110.80 | 0.0010 | 0.002 |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | +0.67 | +159.16 | 0.0010 | 0.002 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.66 | +79.04 | 0.0010 | 0.002 |
| [5584](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5584) | +0.65 | +176.86 | 0.0010 | 0.002 |
| [1603](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1603) | +0.65 | +160.89 | 0.0010 | 0.002 |
| [3066](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3066) | +0.65 | +186.86 | 0.0010 | 0.002 |

**"You" after loss: loss + you vs loss, layer 31** (197 features tested; 107 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.72 | +29.64 | 0.0010 | 0.002 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | +0.64 | +39.50 | 0.0010 | 0.002 |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | -0.61 | -109.15 | 0.0010 | 0.002 |
| [1450](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1450) | +0.60 | +55.69 | 0.0010 | 0.002 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.59 | +51.50 | 0.0010 | 0.002 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.55 | +38.28 | 0.0010 | 0.002 |
| [5584](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5584) | +0.53 | +44.58 | 0.0010 | 0.002 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.53 | +45.70 | 0.0010 | 0.002 |
| [7338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7338) | -0.52 | -55.94 | 0.0010 | 0.002 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | -0.52 | -66.22 | 0.0010 | 0.002 |
| [3153](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3153) | -0.51 | -94.42 | 0.0010 | 0.002 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | +0.49 | +41.93 | 0.0010 | 0.002 |
| [1385](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1385) | -0.48 | -32.59 | 0.0010 | 0.002 |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | +0.47 | +129.18 | 0.0010 | 0.002 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | +0.46 | +83.83 | 0.0010 | 0.002 |

**"You" after gain: gain + you vs gain, layer 31** (184 features tested; 85 with q < 0.05; 6 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.76 | +26.36 | 0.0010 | 0.003 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.62 | +43.43 | 0.0010 | 0.003 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.55 | +42.27 | 0.0010 | 0.003 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.44 | +34.31 | 0.0010 | 0.003 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | -0.43 | -30.24 | 0.0010 | 0.003 |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | +0.42 | +18.55 | 0.0010 | 0.003 |
| [10269](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10269) | -0.38 | -60.48 | 0.0010 | 0.003 |
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | -0.38 | -63.84 | 0.0010 | 0.003 |
| [10151](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10151) | -0.38 | -47.90 | 0.0010 | 0.003 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | -0.35 | -39.70 | 0.0010 | 0.003 |
| [7338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7338) | -0.35 | -34.27 | 0.0010 | 0.003 |
| [1054](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1054) | -0.34 | -30.56 | 0.0010 | 0.003 |
| [4333](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4333) | +0.34 | +15.48 | 0.0010 | 0.003 |
| [239](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/239) | -0.33 | -37.08 | 0.0010 | 0.003 |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | +0.32 | +44.87 | 0.0010 | 0.003 |

**"You" after loss minus after gain, layer 31** (195 features tested; 71 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | +0.53 | +60.99 | 0.0010 | 0.005 |
| [1450](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1450) | +0.47 | +60.34 | 0.0010 | 0.005 |
| [5584](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5584) | +0.47 | +41.95 | 0.0010 | 0.005 |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | -0.47 | -85.43 | 0.0010 | 0.005 |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | +0.44 | +123.40 | 0.0010 | 0.005 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | +0.43 | +80.21 | 0.0010 | 0.005 |
| [1336](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1336) | +0.42 | +72.53 | 0.0010 | 0.005 |
| [5862](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5862) | +0.39 | +52.18 | 0.0010 | 0.005 |
| [879](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/879) | +0.38 | +40.09 | 0.0010 | 0.005 |
| [2153](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2153) | -0.38 | -56.36 | 0.0010 | 0.005 |
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | +0.36 | +62.15 | 0.0010 | 0.005 |
| [3153](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3153) | -0.35 | -58.56 | 0.0010 | 0.005 |
| [1157](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1157) | +0.33 | +44.49 | 0.0010 | 0.005 |
| [1837](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1837) | +0.32 | +34.48 | 0.0010 | 0.005 |
| [6634](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6634) | -0.31 | -72.15 | 0.0010 | 0.005 |

**Priming: loss frame vs gain frame, layer 41** (192 features tested; 121 with q < 0.05; 4 of the top 15 are also in UBS's top 15 (B's matched run))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | +0.91 | +441.71 | 0.0010 | 0.002 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.90 | +451.67 | 0.0010 | 0.002 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | -0.81 | -350.94 | 0.0010 | 0.002 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | +0.81 | +510.09 | 0.0010 | 0.002 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.80 | -233.53 | 0.0010 | 0.002 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | +0.76 | +587.87 | 0.0010 | 0.002 |
| [7480](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7480) | +0.74 | +405.71 | 0.0010 | 0.002 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.73 | +211.28 | 0.0010 | 0.002 |
| [1102](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1102) | -0.73 | -412.47 | 0.0010 | 0.002 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | +0.72 | +311.03 | 0.0010 | 0.002 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | -0.69 | -259.04 | 0.0010 | 0.002 |
| [15084](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15084) | +0.66 | +277.82 | 0.0010 | 0.002 |
| [1163](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1163) | +0.66 | +132.26 | 0.0010 | 0.002 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | +0.61 | +305.98 | 0.0010 | 0.002 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | +0.61 | +315.58 | 0.0010 | 0.002 |

**"You" after loss: loss + you vs loss, layer 41** (187 features tested; 99 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.79 | +84.75 | 0.0010 | 0.003 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | +0.71 | +145.35 | 0.0010 | 0.003 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | +0.64 | +158.80 | 0.0010 | 0.003 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | +0.55 | +157.87 | 0.0010 | 0.003 |
| [865](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/865) | -0.54 | -93.92 | 0.0010 | 0.003 |
| [5477](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5477) | -0.54 | -131.29 | 0.0010 | 0.003 |
| [15084](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15084) | -0.50 | -132.32 | 0.0010 | 0.003 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | -0.49 | -71.97 | 0.0010 | 0.003 |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | -0.49 | -96.56 | 0.0010 | 0.003 |
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | +0.47 | +108.59 | 0.0010 | 0.003 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | +0.46 | +108.11 | 0.0010 | 0.003 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.46 | -42.60 | 0.0010 | 0.003 |
| [5588](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5588) | +0.42 | +125.29 | 0.0010 | 0.003 |
| [10380](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10380) | +0.41 | +82.93 | 0.0010 | 0.003 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.41 | +98.45 | 0.0010 | 0.003 |

**"You" after gain: gain + you vs gain, layer 41** (185 features tested; 72 with q < 0.05; 6 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [865](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/865) | -0.49 | -73.49 | 0.0010 | 0.004 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | +0.48 | +82.34 | 0.0010 | 0.004 |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | +0.36 | +88.27 | 0.0010 | 0.004 |
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | +0.35 | +79.41 | 0.0010 | 0.004 |
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | +0.35 | +51.30 | 0.0010 | 0.004 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | +0.33 | +55.28 | 0.0010 | 0.004 |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | -0.33 | -55.94 | 0.0010 | 0.004 |
| [5120](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5120) | +0.33 | +123.01 | 0.0010 | 0.004 |
| [1383](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1383) | +0.32 | +59.22 | 0.0010 | 0.004 |
| [1984](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1984) | +0.32 | +55.99 | 0.0010 | 0.004 |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | -0.31 | -66.66 | 0.0010 | 0.004 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | -0.31 | -82.60 | 0.0010 | 0.004 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | +0.30 | +72.36 | 0.0010 | 0.004 |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | +0.30 | +98.64 | 0.0010 | 0.004 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.30 | +58.59 | 0.0010 | 0.004 |

**"You" after loss minus after gain, layer 41** (192 features tested; 60 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | +0.56 | +150.99 | 0.0010 | 0.005 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.53 | +59.03 | 0.0010 | 0.005 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.53 | -52.53 | 0.0010 | 0.005 |
| [5477](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5477) | -0.41 | -86.73 | 0.0010 | 0.005 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | +0.40 | +101.72 | 0.0010 | 0.005 |
| [15084](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15084) | -0.38 | -109.83 | 0.0010 | 0.005 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | -0.37 | -84.45 | 0.0010 | 0.005 |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | -0.34 | -79.83 | 0.0010 | 0.005 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | +0.32 | +63.00 | 0.0010 | 0.005 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | -0.32 | -47.86 | 0.0010 | 0.005 |
| [5668](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5668) | -0.31 | -73.06 | 0.0010 | 0.005 |
| [1060](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1060) | +0.31 | +71.90 | 0.0010 | 0.005 |
| [2080](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2080) | +0.30 | +83.11 | 0.0010 | 0.005 |
| [130](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/130) | +0.30 | +62.54 | 0.0010 | 0.005 |
| [7604](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7604) | -0.30 | -90.26 | 0.0010 | 0.005 |

