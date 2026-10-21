# Incidental emotion before UBS's request (exploratory)

53 moments (B's neutral careers at their requests), each read in 25 versions: no document or one of the author's emotion documents just before UBS's request (a different document per moment), times the request's five framings. P(the order goes along) after the fixed neutral reasoning line, in percent. Produced by `designs/rd2/analysis/prime.py` from `scripts/modal_prime.py`.

## P(the order goes along): document read (rows) x UBS's framing (columns)

| Document \ request | neutral | loss | gain | loss + you | gain + you |
|---|---|---|---|---|---|
| none | 14.1% | 19.2% | 17.6% | 19.2% | 17.0% |
| loss | 31.5% | 30.6% | 31.3% | 33.8% | 30.7% |
| blame | 26.0% | 27.0% | 29.4% | 33.9% | 30.6% |
| gain | 28.2% | 27.4% | 27.9% | 29.0% | 27.0% |
| credit | 23.8% | 26.7% | 25.8% | 26.2% | 25.4% |

## Each document against none, UBS's request neutral (points)

| Document | Change | 95% interval | p |
|---|---|---|---|
| loss | +16.8 | +8.2 to +27.0 | 0.0050 |
| blame | +11.5 | +3.8 to +17.9 | 0.0190 |
| gain | +13.8 | +8.3 to +20.3 | 0.0042 |
| credit | +9.6 | +3.7 to +15.5 | 0.0052 |

## The two crossed predictions (points): the framing's effect over the neutral request, with the document minus without it

| Prediction | Change | 95% interval | p |
|---|---|---|---|
| After blame, a credit-framed request (gain + you) lands harder (relief) | +2.1 | -6.9 to +11.0 | 0.6697 |
| After credit, a blame-framed request (loss + you) lands harder (avoiding blame) | -2.8 | -8.9 to +2.7 | 0.4383 |

## Every document x framing: how the document changes the framing's effect (points, against no document)

| Document | loss | gain | loss + you | gain + you |
|---|---|---|---|---|
| loss | -5.1 (-12.9 to +1.5) | -2.9 (-8.1 to +2.2) | -2.8 (-9.4 to +3.9) | -3.5 (-9.9 to +2.2) |
| blame | -3.0 (-11.5 to +5.5) | +0.8 (-5.2 to +6.5) | +2.7 (-3.1 to +8.5) | +2.1 (-6.4 to +10.3) |
| gain | -4.9 (-11.6 to +0.7) | -1.8 (-7.0 to +4.0) | -4.3 (-11.3 to +1.8) | -3.8 (-8.1 to +0.3) |
| credit | -1.5 (-6.4 to +3.1) | -0.5 (-4.2 to +3.4) | -2.8 (-9.1 to +2.5) | -1.2 (-6.4 to +4.0) |

Coverage (the share of the model's probability on the orders scored): median 0.87, lowest 0.00.
