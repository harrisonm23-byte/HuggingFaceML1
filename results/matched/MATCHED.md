# Same moment, different frame (B's moments, history held fixed)

300 moments (50 careers x their push requests), each read in 10 versions: UBS's request in the five framings, each with and without Bank C's line; everything before the request is the saved career, unchanged. Gemma 3 12B at bfloat16. Produced by `designs/rd2/analysis/matched_history.py`.


## 1. What it would do: P(the order goes along)

After a fixed neutral reasoning line, the probability of HOLD and of every order size the agents used (both signs), and the share of it on orders that go along. Coverage, the share of all probability those orders take: median 0.67, lowest 0.00.


**Without Bank C's line.** Rows: the career's own framing (its history); columns: the framing of UBS's request at this moment. The diagonal is the career as saved.

| History \ request | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| neutral | 14.3% | 20.3% | 18.9% | 20.4% | 18.5% |
| loss | 35.1% | 38.2% | 37.8% | 41.8% | 39.1% |
| gain | 32.1% | 37.3% | 34.6% | 38.3% | 36.4% |
| loss + you | 35.8% | 42.4% | 39.2% | 44.0% | 41.0% |
| gain + you | 28.1% | 35.1% | 33.8% | 35.5% | 33.6% |

**With Bank C's line.** Rows: the career's own framing (its history); columns: the framing of UBS's request at this moment. The diagonal is the career as saved plus Bank C.

| History \ request | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| neutral | 22.8% | 23.8% | 24.8% | 30.4% | 27.7% |
| loss | 40.1% | 38.2% | 39.7% | 42.6% | 39.6% |
| gain | 39.6% | 39.6% | 38.8% | 43.7% | 42.1% |
| loss + you | 39.5% | 42.2% | 41.1% | 46.2% | 43.5% |
| gain + you | 36.0% | 36.3% | 36.5% | 37.6% | 39.2% |

**The request's own effect** (the same moments, all 50 histories; paired, signs flipped by career):

| Contrast | Change in P(order goes along) | 95% interval | p |
|---|---|---|---|
| Request: loss frame vs gain frame | +2.0 points | +1.0 to +3.1 | 0.0009 |
| Request: loss vs neutral | +5.6 points | +3.7 to +7.5 | 0.0001 |
| Request: loss + you vs neutral | +6.9 points | +4.2 to +9.7 | 0.0001 |
| Request: gain vs neutral | +3.8 points | +1.8 to +5.8 | 0.0010 |
| Request: gain + you vs neutral | +4.6 points | +2.6 to +6.8 | 0.0002 |
| Request: "+ you" vs none | +1.1 points | -0.4 to +2.6 | 0.1631 |
| Bank C's line (all framings) | +4.0 points | +2.7 to +5.3 | 0.0001 |
| "You" after loss: loss + you vs loss | +1.3 points | -0.9 to +3.5 | 0.2623 |
| "You" after gain: gain + you vs gain | +0.9 points | -0.6 to +2.4 | 0.2944 |
| "You" after loss minus after gain | +0.5 points | -1.8 to +2.9 | 0.7203 |
| "You" after loss: loss + you vs loss, with Bank C | +4.1 points | +2.3 to +5.9 | 0.0001 |
| "You" after gain: gain + you vs gain, with Bank C | +2.2 points | +0.8 to +3.7 | 0.0021 |
| "You" after loss minus after gain, with Bank C | +1.8 points | +0.0 to +3.7 | 0.0588 |
| Bank C's line (neutral) | +6.5 points | +4.4 to +8.6 | 0.0001 |
| Bank C's line (loss) | +1.4 points | +0.4 to +2.5 | 0.0164 |
| Bank C's line (gain) | +3.3 points | +1.9 to +4.8 | 0.0001 |
| Bank C's line (loss + you) | +4.1 points | +1.8 to +6.6 | 0.0003 |
| Bank C's line (gain + you) | +4.7 points | +2.8 to +6.5 | 0.0001 |

**The history's effect** (different careers, the request held neutral; careers reshuffled between the groups), next to the whole effect as saved:

| Contrast | Change in P(order goes along) | 95% interval | p |
|---|---|---|---|
| History: loss frame vs gain frame (request neutral) | +5.4 points | -3.7 to +15.2 | 0.2992 |
| History: framed vs neutral (request neutral) | +18.5 points | +10.6 to +26.1 | 0.0010 |
| As saved: loss frame vs gain frame (history and request) | +7.0 points | -2.4 to +17.1 | 0.1828 |
| As saved: framed vs neutral (history and request) | +23.3 points | +15.0 to +31.4 | 0.0001 |

## 2. The state

**Check:** the as-saved version against Run 1's reading of the same moment (cosine; Run 1 read the career in one pass, this run from a saved cache, so tiny differences are expected):

| Layer | Median | Lowest |
|---|---|---|
| 6 | 1.0000 | 1.0000 |
| 12 | 1.0000 | 1.0000 |
| 18 | 1.0000 | 1.0000 |
| 24 | 1.0000 | 1.0000 |
| 31 | 1.0000 | 1.0000 |
| 36 | 1.0000 | 1.0000 |
| 41 | 1.0000 | 1.0000 |
| 47 | 1.0000 | 0.9998 |

**How far each change moves the state** (mean distance, by layer), against two different B careers of the same framing at the same request (Run 1: different histories):

| Layer | Request loss vs gain (same moment) | Request framed vs neutral | Bank C's line | Two careers, same framing |
|---|---|---|---|---|
| 6 | 20.3 | 28.4 | 28.2 | 39.5 |
| 12 | 55.8 | 154.0 | 166.6 | 189.1 |
| 18 | 249.9 | 542.7 | 596.9 | 774.4 |
| 24 | 630.3 | 1056.0 | 1663.7 | 2597.4 |
| 31 | 1158.9 | 1961.5 | 3735.2 | 6841.9 |
| 36 | 1643.7 | 2731.8 | 5990.3 | 9250.1 |
| 41 | 2008.1 | 3467.1 | 6752.3 | 12599.0 |
| 47 | 3705.4 | 6583.4 | 11627.7 | 20919.5 |

**"You" after loss and after gain** (the change "+ you" makes to the state at the same moment): its size in each frame, and how alike the two changes are (cosine of the average changes: 1 = the same change, 0 = unrelated). The last column is the ceiling: the change after loss compared with itself, measured on two halves of the careers. A cosine between the frames well below that ceiling means "you" registers differently after loss than after gain.

| Layer | Size after loss | Size after gain | Cosine, after loss vs after gain | Median cosine, moment by moment | Ceiling: after loss vs itself (two halves) |
|---|---|---|---|---|---|
| 6 | 20.6 | 18.8 | 0.096 | 0.229 | 0.992 |
| 12 | 70.7 | 68.9 | 0.711 | 0.458 | 0.996 |
| 18 | 398.5 | 293.9 | 0.897 | 0.584 | 1.000 |
| 24 | 813.1 | 751.8 | 0.918 | 0.526 | 0.998 |
| 31 | 1813.7 | 1373.2 | 0.771 | 0.584 | 0.994 |
| 36 | 2591.8 | 1859.3 | 0.792 | 0.593 | 0.994 |
| 41 | 3070.3 | 2355.6 | 0.731 | 0.590 | 0.989 |
| 47 | 6214.9 | 4893.9 | 0.813 | 0.607 | 0.982 |

**The frame direction** (loss and loss + you minus neutral, averaged over requests). Held fixed: from this run, at the same moments. Across careers: from Run 1, B's loss careers minus its neutral careers at the same request (the direction the steering used). Bank C's change along the held-fixed direction is in units of the loss - neutral gap along it (1 = as far as the loss frame itself moves the state).

| Layer | Cosine: held fixed vs across careers | Bank C's change along it (all framings) | Bank C, neutral request | Bank C, loss + you request |
|---|---|---|---|---|
| 6 | 0.615 | +0.23 | -0.08 | +0.38 |
| 12 | 0.983 | +0.91 | +0.93 | +1.07 |
| 18 | 0.816 | +1.25 | +0.77 | +1.51 |
| 24 | -0.291 | +1.95 | +1.84 | +2.25 |
| 31 | 0.387 | +0.12 | +0.01 | +0.46 |
| 36 | 0.010 | +1.26 | +0.97 | +2.04 |
| 41 | 0.101 | +0.35 | +0.23 | +0.93 |
| 47 | -0.134 | +0.86 | +0.64 | +1.56 |

## 3. Gemma Scope features, the history held fixed


**Note:** a difference between "you" after loss and after gain in the features can come from the features' on/off thresholds alone (the same change, starting from different levels). The cosine table in section 2, which is linear, is the cleaner test of whether "you" registers differently.

**Request: loss frame vs gain frame, layer 12** (56 features tested; 47 with q < 0.05; 9 of the top 15 are also in Run 1's top 15 (loss vs gain across careers))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -1.06 | -1.50 | 0.0010 | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +1.02 | +1.16 | 0.0010 | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.82 | +1.58 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | +0.61 | +0.51 | 0.0010 | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | -0.54 | -1.22 | 0.0010 | 0.002 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.53 | +0.53 | 0.0010 | 0.002 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | -0.49 | -0.45 | 0.0010 | 0.002 |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | -0.49 | -4.51 | 0.0010 | 0.002 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.49 | +0.41 | 0.0010 | 0.002 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -0.47 | -6.68 | 0.0010 | 0.002 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.46 | -6.33 | 0.0010 | 0.002 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.46 | -4.37 | 0.0010 | 0.002 |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | -0.43 | -0.68 | 0.0010 | 0.002 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.40 | -0.62 | 0.0010 | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.39 | -0.80 | 0.0010 | 0.002 |

**"You" after loss: loss + you vs loss, layer 12** (57 features tested; 41 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.46 | +4.55 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | +1.30 | +1.49 | 0.0010 | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +1.13 | +2.47 | 0.0010 | 0.002 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.97 | +1.84 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.91 | +1.41 | 0.0010 | 0.002 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +0.68 | +3.30 | 0.0010 | 0.002 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +0.63 | +1.53 | 0.0010 | 0.002 |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | +0.55 | +1.46 | 0.0010 | 0.002 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | +0.55 | +0.95 | 0.0010 | 0.002 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.53 | -8.29 | 0.0010 | 0.002 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -0.51 | -3.56 | 0.0010 | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.47 | -1.89 | 0.0010 | 0.002 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.46 | +4.60 | 0.0010 | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.42 | +2.03 | 0.0010 | 0.002 |
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | -0.41 | -3.02 | 0.0010 | 0.002 |

**"You" after gain: gain + you vs gain, layer 12** (56 features tested; 45 with q < 0.05; 10 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.24 | +3.14 | 0.0010 | 0.002 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | +1.10 | +1.31 | 0.0010 | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.71 | +1.18 | 0.0010 | 0.002 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | +0.68 | +1.01 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | +0.67 | +0.80 | 0.0010 | 0.002 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -0.62 | -3.50 | 0.0010 | 0.002 |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | +0.54 | +7.29 | 0.0010 | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.52 | +3.39 | 0.0010 | 0.002 |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | +0.41 | +1.13 | 0.0010 | 0.002 |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | -0.40 | -1.61 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.40 | +0.60 | 0.0010 | 0.002 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +0.36 | +0.48 | 0.0010 | 0.002 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +0.35 | +2.09 | 0.0010 | 0.002 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.33 | +2.58 | 0.0010 | 0.002 |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +0.33 | +1.32 | 0.0010 | 0.002 |

**"You" after loss minus after gain, layer 12** (56 features tested; 33 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.98 | +1.28 | 0.0010 | 0.002 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.87 | +1.45 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.73 | +0.81 | 0.0010 | 0.002 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +0.70 | +1.05 | 0.0010 | 0.002 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | +0.51 | +0.53 | 0.0010 | 0.002 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -0.51 | -1.09 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | +0.50 | +0.69 | 0.0010 | 0.002 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.47 | -7.88 | 0.0010 | 0.002 |
| [1699](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1699) | -0.44 | -0.42 | 0.0010 | 0.002 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | +0.43 | +0.75 | 0.0010 | 0.002 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.41 | -0.61 | 0.0010 | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.41 | +1.41 | 0.0010 | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.37 | -1.06 | 0.0010 | 0.002 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.34 | +0.40 | 0.0010 | 0.002 |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | +0.32 | +1.26 | 0.0010 | 0.002 |

**Bank C's line (all framings), layer 12** (55 features tested; 48 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +1.99 | +21.27 | 0.0010 | 0.001 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.99 | +18.65 | 0.0010 | 0.001 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +1.63 | +7.18 | 0.0010 | 0.001 |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +1.61 | +6.19 | 0.0010 | 0.001 |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | +1.59 | +7.90 | 0.0010 | 0.001 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -1.58 | -11.04 | 0.0010 | 0.001 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -1.44 | -4.43 | 0.0010 | 0.001 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -1.32 | -14.71 | 0.0010 | 0.001 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +1.30 | +11.81 | 0.0010 | 0.001 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +1.29 | +10.76 | 0.0010 | 0.001 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +1.28 | +11.86 | 0.0010 | 0.001 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | -1.24 | -1.65 | 0.0010 | 0.001 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +1.12 | +4.11 | 0.0010 | 0.001 |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | -1.09 | -14.27 | 0.0010 | 0.001 |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | +1.07 | +10.51 | 0.0010 | 0.001 |

**Request: loss frame vs gain frame, layer 24** (146 features tested; 79 with q < 0.05; 2 of the top 15 are also in Run 1's top 15 (loss vs gain across careers))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | +1.03 | +7.73 | 0.0010 | 0.003 |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.81 | -7.98 | 0.0010 | 0.003 |
| [1149](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1149) | -0.81 | -10.96 | 0.0010 | 0.003 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | -0.52 | -8.12 | 0.0010 | 0.003 |
| [16165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16165) | +0.50 | +10.40 | 0.0010 | 0.003 |
| [12075](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12075) | +0.40 | +3.03 | 0.0010 | 0.003 |
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.38 | -5.33 | 0.0010 | 0.003 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | -0.37 | -12.38 | 0.0010 | 0.003 |
| [13799](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799) | +0.37 | +3.52 | 0.0010 | 0.003 |
| [3987](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3987) | -0.34 | -13.35 | 0.0010 | 0.003 |
| [5082](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5082) | -0.32 | -20.01 | 0.0010 | 0.003 |
| [9712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712) | -0.32 | -2.83 | 0.0010 | 0.003 |
| [15592](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592) | -0.31 | -2.93 | 0.0010 | 0.003 |
| [13585](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13585) | +0.30 | +4.74 | 0.0010 | 0.003 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.30 | +5.69 | 0.0010 | 0.003 |

**"You" after loss: loss + you vs loss, layer 24** (145 features tested; 102 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -1.48 | -19.34 | 0.0010 | 0.002 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +1.20 | +21.04 | 0.0010 | 0.002 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | +0.91 | +14.72 | 0.0010 | 0.002 |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | +0.84 | +81.64 | 0.0010 | 0.002 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +0.79 | +13.14 | 0.0010 | 0.002 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +0.77 | +41.39 | 0.0010 | 0.002 |
| [8326](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326) | +0.63 | +63.91 | 0.0010 | 0.002 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +0.61 | +16.17 | 0.0010 | 0.002 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | +0.60 | +53.41 | 0.0010 | 0.002 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | +0.60 | +10.81 | 0.0010 | 0.002 |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | +0.59 | +61.66 | 0.0010 | 0.002 |
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.59 | -11.25 | 0.0010 | 0.002 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | +0.59 | +34.37 | 0.0010 | 0.002 |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | +0.59 | +64.36 | 0.0010 | 0.002 |
| [14392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14392) | +0.56 | +10.17 | 0.0010 | 0.002 |

**"You" after gain: gain + you vs gain, layer 24** (151 features tested; 101 with q < 0.05; 10 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.81 | -11.74 | 0.0010 | 0.002 |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.70 | -8.62 | 0.0010 | 0.002 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | +0.68 | +30.36 | 0.0010 | 0.002 |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | +0.61 | +70.46 | 0.0010 | 0.002 |
| [15357](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15357) | -0.61 | -7.81 | 0.0010 | 0.002 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | +0.61 | +33.63 | 0.0010 | 0.002 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.58 | +7.68 | 0.0010 | 0.002 |
| [14392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14392) | +0.56 | +7.50 | 0.0010 | 0.002 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | +0.56 | +29.79 | 0.0010 | 0.002 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +0.52 | +8.00 | 0.0010 | 0.002 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +0.45 | +25.09 | 0.0010 | 0.002 |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | +0.44 | +46.29 | 0.0010 | 0.002 |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | +0.44 | +33.00 | 0.0010 | 0.002 |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | +0.44 | +37.17 | 0.0010 | 0.002 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | +0.44 | +35.71 | 0.0010 | 0.002 |

**"You" after loss minus after gain, layer 24** (146 features tested; 72 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.73 | -10.72 | 0.0010 | 0.003 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.69 | +13.36 | 0.0010 | 0.003 |
| [15737](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15737) | -0.54 | -13.82 | 0.0010 | 0.003 |
| [13799](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799) | +0.48 | +8.32 | 0.0010 | 0.003 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | +0.47 | +7.43 | 0.0010 | 0.003 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +0.41 | +10.97 | 0.0010 | 0.003 |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | +0.41 | +40.13 | 0.0010 | 0.003 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +0.36 | +16.30 | 0.0010 | 0.003 |
| [3068](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3068) | -0.35 | -28.59 | 0.0010 | 0.003 |
| [1149](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1149) | -0.35 | -7.51 | 0.0010 | 0.003 |
| [13585](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13585) | +0.34 | +8.75 | 0.0010 | 0.003 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | +0.34 | +7.69 | 0.0010 | 0.003 |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | +0.33 | +29.06 | 0.0010 | 0.003 |
| [1672](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1672) | +0.33 | +19.26 | 0.0010 | 0.003 |
| [8326](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326) | +0.32 | +32.68 | 0.0010 | 0.003 |

**Bank C's line (all framings), layer 24** (144 features tested; 131 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1672](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1672) | +1.80 | +82.40 | 0.0010 | 0.001 |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | +1.67 | +238.67 | 0.0010 | 0.001 |
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | -1.67 | -44.26 | 0.0010 | 0.001 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +1.61 | +48.86 | 0.0010 | 0.001 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | +1.57 | +239.22 | 0.0010 | 0.001 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +1.43 | +110.23 | 0.0010 | 0.001 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | +1.41 | +97.93 | 0.0010 | 0.001 |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | +1.36 | +111.20 | 0.0010 | 0.001 |
| [15737](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15737) | -1.36 | -21.26 | 0.0010 | 0.001 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | +1.35 | +24.91 | 0.0010 | 0.001 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | +1.21 | +71.51 | 0.0010 | 0.001 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +1.19 | +25.80 | 0.0010 | 0.001 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | +1.19 | +25.29 | 0.0010 | 0.001 |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | +1.17 | +163.25 | 0.0010 | 0.001 |
| [8311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311) | +1.13 | +28.33 | 0.0010 | 0.001 |

**Request: loss frame vs gain frame, layer 31** (163 features tested; 63 with q < 0.05; 2 of the top 15 are also in Run 1's top 15 (loss vs gain across careers))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [5652](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652) | +0.71 | +14.98 | 0.0010 | 0.005 |
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.48 | +17.88 | 0.0010 | 0.005 |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | +0.41 | +26.83 | 0.0010 | 0.005 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | +0.41 | +29.41 | 0.0010 | 0.005 |
| [1744](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1744) | +0.34 | +27.93 | 0.0010 | 0.005 |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | -0.33 | -10.39 | 0.0010 | 0.005 |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | +0.31 | +25.37 | 0.0010 | 0.005 |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | +0.30 | +12.80 | 0.0010 | 0.005 |
| [5381](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5381) | -0.25 | -21.00 | 0.0010 | 0.005 |
| [239](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/239) | -0.25 | -9.75 | 0.0010 | 0.005 |
| [1128](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1128) | +0.24 | +18.41 | 0.0010 | 0.005 |
| [2927](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2927) | -0.24 | -24.79 | 0.0010 | 0.005 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +0.24 | +9.33 | 0.0010 | 0.005 |
| [8799](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8799) | -0.23 | -19.50 | 0.0010 | 0.005 |
| [13577](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13577) | -0.23 | -16.70 | 0.0010 | 0.005 |

**"You" after loss: loss + you vs loss, layer 31** (161 features tested; 97 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.88 | +35.79 | 0.0010 | 0.003 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.72 | +128.78 | 0.0010 | 0.003 |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | +0.63 | +42.28 | 0.0010 | 0.003 |
| [137](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/137) | -0.44 | -55.48 | 0.0010 | 0.003 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.43 | +95.74 | 0.0010 | 0.003 |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | +0.43 | +112.35 | 0.0010 | 0.003 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.43 | +48.38 | 0.0010 | 0.003 |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | +0.43 | +61.28 | 0.0010 | 0.003 |
| [357](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/357) | -0.39 | -57.87 | 0.0010 | 0.003 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | +0.37 | +55.33 | 0.0010 | 0.003 |
| [3039](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3039) | -0.37 | -57.90 | 0.0010 | 0.003 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +0.37 | +48.73 | 0.0010 | 0.003 |
| [929](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/929) | -0.36 | -46.90 | 0.0010 | 0.003 |
| [2683](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2683) | -0.35 | -68.32 | 0.0010 | 0.003 |
| [1238](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1238) | +0.34 | +47.81 | 0.0010 | 0.003 |

**"You" after gain: gain + you vs gain, layer 31** (162 features tested; 86 with q < 0.05; 6 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.68 | +22.61 | 0.0010 | 0.003 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.61 | +80.06 | 0.0010 | 0.003 |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | +0.59 | +28.10 | 0.0010 | 0.003 |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | -0.40 | -50.92 | 0.0010 | 0.003 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.36 | +35.54 | 0.0010 | 0.003 |
| [324](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/324) | +0.32 | +21.64 | 0.0010 | 0.003 |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | +0.31 | +26.80 | 0.0010 | 0.003 |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/26) | -0.30 | -22.32 | 0.0010 | 0.003 |
| [3369](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3369) | -0.28 | -19.24 | 0.0010 | 0.003 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/348) | -0.28 | -34.50 | 0.0010 | 0.003 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | -0.28 | -32.79 | 0.0010 | 0.003 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.28 | +47.58 | 0.0010 | 0.003 |
| [294](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/294) | +0.27 | +15.64 | 0.0010 | 0.003 |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | -0.27 | -33.01 | 0.0010 | 0.003 |
| [2014](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2014) | +0.27 | +30.32 | 0.0010 | 0.003 |

**"You" after loss minus after gain, layer 31** (163 features tested; 71 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +0.69 | +75.18 | 0.0010 | 0.005 |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | -0.42 | -56.43 | 0.0010 | 0.005 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | +0.39 | +53.16 | 0.0010 | 0.005 |
| [5652](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652) | +0.37 | +13.45 | 0.0010 | 0.005 |
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.36 | +13.18 | 0.0010 | 0.005 |
| [137](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/137) | -0.34 | -39.66 | 0.0010 | 0.005 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.33 | +48.71 | 0.0010 | 0.005 |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | +0.32 | +29.09 | 0.0010 | 0.005 |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | +0.31 | +66.22 | 0.0010 | 0.005 |
| [2683](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2683) | -0.31 | -58.20 | 0.0010 | 0.005 |
| [1519](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1519) | +0.30 | +43.40 | 0.0010 | 0.005 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.27 | +48.16 | 0.0010 | 0.005 |
| [357](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/357) | -0.27 | -39.22 | 0.0010 | 0.005 |
| [635](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/635) | +0.27 | +19.39 | 0.0010 | 0.005 |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | +0.26 | +34.48 | 0.0010 | 0.005 |

**Bank C's line (all framings), layer 31** (176 features tested; 140 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +1.39 | +214.79 | 0.0010 | 0.001 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +1.11 | +368.14 | 0.0010 | 0.001 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.97 | +186.27 | 0.0010 | 0.001 |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | -0.93 | -306.46 | 0.0010 | 0.001 |
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.91 | +49.79 | 0.0010 | 0.001 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +0.90 | +91.90 | 0.0010 | 0.001 |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | +0.86 | +174.79 | 0.0010 | 0.001 |
| [1293](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1293) | +0.84 | +194.32 | 0.0010 | 0.001 |
| [3331](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3331) | +0.84 | +139.17 | 0.0010 | 0.001 |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | -0.80 | -198.88 | 0.0010 | 0.001 |
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | +0.79 | +123.33 | 0.0010 | 0.001 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.70 | +182.34 | 0.0010 | 0.001 |
| [9397](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397) | +0.70 | +113.88 | 0.0010 | 0.001 |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | -0.70 | -110.55 | 0.0010 | 0.001 |
| [12956](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12956) | +0.69 | +118.19 | 0.0010 | 0.001 |

**Request: loss frame vs gain frame, layer 41** (163 features tested; 62 with q < 0.05; 3 of the top 15 are also in Run 1's top 15 (loss vs gain across careers))

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.48 | +76.42 | 0.0010 | 0.005 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +0.43 | +100.00 | 0.0010 | 0.005 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.35 | +46.92 | 0.0010 | 0.005 |
| [2903](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2903) | +0.35 | +43.02 | 0.0010 | 0.005 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | -0.28 | -50.29 | 0.0010 | 0.005 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | +0.27 | +41.51 | 0.0010 | 0.005 |
| [395](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/395) | -0.27 | -23.07 | 0.0010 | 0.005 |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/316) | -0.26 | -14.00 | 0.0010 | 0.005 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.25 | -11.59 | 0.0020 | 0.009 |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | +0.24 | +22.53 | 0.0010 | 0.005 |
| [1234](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1234) | +0.24 | +26.99 | 0.0010 | 0.005 |
| [1951](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1951) | -0.23 | -23.95 | 0.0030 | 0.013 |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | +0.22 | +37.03 | 0.0020 | 0.009 |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1571) | -0.22 | -43.77 | 0.0010 | 0.005 |
| [6705](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6705) | +0.21 | +29.67 | 0.0010 | 0.005 |

**"You" after loss: loss + you vs loss, layer 41** (162 features tested; 78 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | +0.97 | +395.50 | 0.0010 | 0.003 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.67 | +148.16 | 0.0010 | 0.003 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | +0.63 | +115.50 | 0.0010 | 0.003 |
| [1462](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1462) | +0.59 | +104.17 | 0.0010 | 0.003 |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | +0.58 | +157.44 | 0.0010 | 0.003 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.56 | +169.97 | 0.0010 | 0.003 |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | +0.51 | +166.04 | 0.0010 | 0.003 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | +0.48 | +148.95 | 0.0010 | 0.003 |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/948) | +0.45 | +162.95 | 0.0010 | 0.003 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | +0.43 | +92.67 | 0.0010 | 0.003 |
| [3420](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3420) | +0.39 | +149.04 | 0.0010 | 0.003 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | +0.30 | +129.67 | 0.0010 | 0.003 |
| [11793](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11793) | -0.30 | -59.89 | 0.0010 | 0.003 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | -0.30 | -81.35 | 0.0010 | 0.003 |
| [1742](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1742) | -0.30 | -34.46 | 0.0010 | 0.003 |

**"You" after gain: gain + you vs gain, layer 41** (161 features tested; 74 with q < 0.05; 5 of its top 15 are also in the top 15 after loss)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | +0.62 | +197.79 | 0.0010 | 0.003 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | -0.49 | -105.67 | 0.0010 | 0.003 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | +0.46 | +66.53 | 0.0010 | 0.003 |
| [1462](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1462) | +0.42 | +64.70 | 0.0010 | 0.003 |
| [9177](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9177) | +0.41 | +80.55 | 0.0010 | 0.003 |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | -0.39 | -99.18 | 0.0010 | 0.003 |
| [755](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/755) | +0.38 | +92.31 | 0.0010 | 0.003 |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | +0.36 | +79.66 | 0.0010 | 0.003 |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | +0.36 | +93.57 | 0.0010 | 0.003 |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | -0.32 | -54.04 | 0.0010 | 0.003 |
| [998](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/998) | -0.31 | -94.94 | 0.0010 | 0.003 |
| [8589](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8589) | +0.29 | +73.39 | 0.0010 | 0.003 |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | -0.28 | -34.74 | 0.0010 | 0.003 |
| [7303](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7303) | +0.28 | +82.14 | 0.0010 | 0.003 |
| [946](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/946) | +0.28 | +53.01 | 0.0010 | 0.003 |

**"You" after loss minus after gain, layer 41** (163 features tested; 55 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | +0.54 | +197.71 | 0.0010 | 0.006 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.53 | +121.14 | 0.0010 | 0.006 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.48 | +133.15 | 0.0010 | 0.006 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | +0.43 | +126.27 | 0.0010 | 0.006 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | +0.37 | +48.97 | 0.0010 | 0.006 |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | +0.35 | +86.38 | 0.0010 | 0.006 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.33 | -26.10 | 0.0010 | 0.006 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | -0.31 | -79.43 | 0.0010 | 0.006 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | +0.31 | +103.81 | 0.0010 | 0.006 |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/948) | +0.29 | +99.77 | 0.0010 | 0.006 |
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | +0.29 | +60.73 | 0.0010 | 0.006 |
| [2162](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2162) | +0.26 | +18.88 | 0.0010 | 0.006 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | +0.26 | +45.94 | 0.0010 | 0.006 |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | +0.24 | +63.86 | 0.0010 | 0.006 |
| [1462](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1462) | +0.22 | +39.47 | 0.0010 | 0.006 |

**Bank C's line (all framings), layer 41** (169 features tested; 136 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | +1.27 | +383.18 | 0.0010 | 0.001 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | -1.22 | -377.45 | 0.0010 | 0.001 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | +1.21 | +394.21 | 0.0010 | 0.001 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +1.07 | +352.00 | 0.0010 | 0.001 |
| [6938](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6938) | +1.05 | +614.59 | 0.0010 | 0.001 |
| [3981](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3981) | +1.05 | +463.46 | 0.0010 | 0.001 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | +0.96 | +305.07 | 0.0010 | 0.001 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.95 | +959.19 | 0.0010 | 0.001 |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | -0.87 | -212.65 | 0.0010 | 0.001 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | +0.86 | +161.79 | 0.0010 | 0.001 |
| [1405](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1405) | +0.85 | +417.22 | 0.0010 | 0.001 |
| [1635](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1635) | -0.85 | -212.81 | 0.0010 | 0.001 |
| [1281](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1281) | +0.83 | +341.34 | 0.0010 | 0.001 |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | +0.80 | +513.73 | 0.0010 | 0.001 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.79 | -68.27 | 0.0010 | 0.001 |

