# Incidental emotion before UBS's request (exploratory)

36 moments (B's neutral careers at their requests), each read in 25 versions: no document or one of the author's emotion documents just before UBS's request (a different document per moment), times the request's five framings. P(the order goes along) after the fixed neutral reasoning line, in percent. Produced by `designs/rd2/analysis/prime.py` from `scripts/modal_prime.py`.

## P(the order goes along): document read (rows) x UBS's framing (columns)

| Document \ request | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| none | 20.5% | 28.8% | 26.9% | 30.3% | 27.6% |
| neutral | 31.5% | 32.7% | 30.3% | 30.6% | 32.3% |
| loss | 44.8% | 46.3% | 45.3% | 45.3% | 46.1% |
| blame | 34.8% | 35.7% | 41.1% | 43.2% | 42.0% |
| gain | 42.4% | 40.6% | 42.7% | 41.7% | 40.6% |
| credit | 33.4% | 36.1% | 35.4% | 34.4% | 34.0% |

## Each document against none, UBS's request neutral (points)

| Document | Change | 95% interval | p |
|---|---|---|---|
| neutral | +9.4 | +2.3 to +17.0 | 0.0558 |
| loss | +20.3 | +9.5 to +31.0 | 0.0065 |
| blame | +13.5 | +3.3 to +23.7 | 0.0398 |
| gain | +20.5 | +11.5 to +29.1 | 0.0061 |
| credit | +11.7 | +4.3 to +19.7 | 0.0250 |

## Each emotion document against the neutral document, UBS's request neutral (points): emotion itself, beyond reading any document

| Document | Change | 95% interval | p |
|---|---|---|---|
| loss | +10.9 | +1.0 to +21.1 | 0.0896 |
| blame | +4.0 | -5.3 to +12.8 | 0.4261 |
| gain | +11.1 | +2.6 to +20.6 | 0.0344 |
| credit | +2.3 | -8.8 to +12.3 | 0.7036 |

Pooled over all five framings:

| Document | Change | 95% interval | p |
|---|---|---|---|
| loss | +11.8 | +3.4 to +21.4 | 0.0222 |
| blame | +7.3 | +1.5 to +13.4 | 0.0619 |
| gain | +10.0 | +2.7 to +19.5 | 0.0188 |
| credit | +5.2 | -6.3 to +17.5 | 0.4669 |

## The two crossed predictions (points): the framing's effect over the neutral request, with the document minus without it

| Prediction | Change | 95% interval | p |
|---|---|---|---|
| After blame, a credit-framed request (gain + you) lands harder (relief) | -2.5 | -15.7 to +9.8 | 0.7122 |
| After credit, a blame-framed request (loss + you) lands harder (avoiding blame) | -8.0 | -16.6 to +0.1 | 0.1329 |

## Every document x framing: how the document changes the framing's effect (points, against no document)

| Document | loss | gain | loss + you | gain + you |
|---|---|---|---|---|
| neutral | -9.8 (-20.9 to -0.6) | -7.3 (-14.1 to -1.3) | -9.2 (-17.8 to -1.4) | -7.0 (-14.4 to +0.0) |
| loss | -9.1 (-22.2 to +3.5) | -5.6 (-13.9 to +1.3) | -8.1 (-17.0 to -0.4) | -6.4 (-15.2 to +2.3) |
| blame | -10.5 (-23.7 to +1.2) | -1.6 (-10.0 to +6.2) | -2.6 (-11.8 to +6.5) | -2.5 (-14.9 to +9.9) |
| gain | -13.1 (-24.9 to -2.0) | -6.2 (-12.9 to +0.5) | -9.9 (-20.5 to -0.2) | -9.8 (-16.1 to -3.2) |
| credit | -3.3 (-12.8 to +6.5) | -0.5 (-9.9 to +11.5) | -8.0 (-16.8 to -0.1) | -7.1 (-14.9 to -0.7) |

Coverage (the share of the model's probability on the orders scored): median 0.96, lowest 0.00.
