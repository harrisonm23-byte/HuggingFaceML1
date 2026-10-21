# Incidental emotion before UBS's request (exploratory)

60 moments (B's neutral careers at their requests), each read in 25 versions: no document or one of the author's emotion documents just before UBS's request (a different document per moment), times the request's five framings. P(the order goes along) after the fixed neutral reasoning line, in percent. Produced by `designs/rd2/analysis/prime.py` from `scripts/modal_prime.py`.

## P(the order goes along): document read (rows) x UBS's framing (columns)

| Document \ request | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| none | 14.3% | 20.3% | 18.9% | 20.4% | 18.5% |
| neutral | 22.7% | 23.0% | 22.0% | 22.9% | 24.0% |
| loss | 32.1% | 31.6% | 32.7% | 37.6% | 33.6% |
| blame | 26.8% | 27.9% | 30.9% | 36.6% | 32.5% |
| gain | 29.1% | 29.3% | 29.7% | 32.9% | 29.5% |
| credit | 22.8% | 25.6% | 24.7% | 25.6% | 24.6% |

## Each document against none, UBS's request neutral (points)

| Document | Change | 95% interval | p |
|---|---|---|---|
| neutral | +8.4 | +3.1 to +14.5 | 0.0172 |
| loss | +17.8 | +9.1 to +26.4 | 0.0038 |
| blame | +12.5 | +5.5 to +18.8 | 0.0105 |
| gain | +14.8 | +8.6 to +20.7 | 0.0042 |
| credit | +8.5 | +2.9 to +14.9 | 0.0153 |

## Each emotion document against the neutral document, UBS's request neutral (points): emotion itself, beyond reading any document

| Document | Change | 95% interval | p |
|---|---|---|---|
| loss | +9.4 | +1.8 to +17.4 | 0.0588 |
| blame | +4.1 | -4.3 to +10.9 | 0.3453 |
| gain | +6.4 | +1.9 to +11.6 | 0.0300 |
| credit | +0.1 | -5.7 to +6.0 | 0.9471 |

Pooled over all five framings:

| Document | Change | 95% interval | p |
|---|---|---|---|
| loss | +10.6 | +3.9 to +17.8 | 0.0199 |
| blame | +8.0 | +2.3 to +13.3 | 0.0314 |
| gain | +7.2 | +3.2 to +12.1 | 0.0069 |
| credit | +1.7 | -3.3 to +6.1 | 0.4805 |

## The two crossed predictions (points): the framing's effect over the neutral request, with the document minus without it

| Prediction | Change | 95% interval | p |
|---|---|---|---|
| After blame, a credit-framed request (gain + you) lands harder (relief) | +1.5 | -7.4 to +10.0 | 0.7574 |
| After credit, a blame-framed request (loss + you) lands harder (avoiding blame) | -3.3 | -9.9 to +2.8 | 0.3848 |

## Every document x framing: how the document changes the framing's effect (points, against no document)

| Document | loss | gain | loss + you | gain + you |
|---|---|---|---|---|
| neutral | -5.7 (-11.5 to -0.5) | -5.3 (-9.9 to -1.4) | -5.9 (-11.5 to -0.6) | -2.8 (-7.6 to +1.6) |
| loss | -6.5 (-13.6 to +0.1) | -3.9 (-9.0 to +0.4) | -0.6 (-8.4 to +7.0) | -2.7 (-10.2 to +4.3) |
| blame | -4.9 (-12.5 to +2.0) | -0.5 (-5.2 to +4.4) | +3.7 (-3.6 to +10.9) | +1.5 (-7.6 to +10.5) |
| gain | -5.8 (-11.4 to -0.4) | -3.9 (-7.3 to -0.4) | -2.3 (-9.6 to +4.2) | -3.8 (-8.1 to +0.4) |
| credit | -3.2 (-8.3 to +1.8) | -2.6 (-6.3 to +1.1) | -3.3 (-10.0 to +2.8) | -2.3 (-8.5 to +3.1) |

Coverage (the share of the model's probability on the orders scored): median 0.75, lowest 0.00.
