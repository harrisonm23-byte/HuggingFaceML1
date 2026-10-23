# Confirmation scan: each document's after-reading state at layers 18-21 (exploratory)

16 moments (B's 10 neutral careers at the 7 and 12 January requests; 4 more left out because the scored orders cover less than half of the model's probability with no injection). Each document type's after-reading change over the request's update, minus the neutral document's, built on the other half of the careers and added with no document at one layer. With no injection, P(the order goes along) averages 36.1%. Produced by `designs/rd2/analysis/layer_scan.py`.

## The read-out: P(the order goes along), change from no injection (points)

| Layer | loss x1 | loss x2 | gain x1 | gain x2 | random x2 |
|---|---|---|---|---|---|
| 18 | -0.2 (p 0.991) | -1.3 (p 0.994) | +0.3 (p 0.771) | +1.0 (p 0.615) | +2.4 (p 0.670) |
| 19 | -1.1 (p 0.585) | -3.9 (p 0.473) | -2.4 (p 0.153) | -5.6 (p 0.100) | +16.5 (p 0.008) |
| 20 | +0.8 (p 0.514) | +3.2 (p 0.457) | -2.1 (p 0.036) | -4.1 (p 0.040) | -2.6 (p 0.915) |
| 21 | +7.5 (p 0.006) | +9.7 (p 0.008) | +1.4 (p 0.007) | +6.3 (p 0.069) | +10.0 (p 0.055) |

**Against the random direction of the same size (x2)**

| Layer | loss | gain |
|---|---|---|
| 18 | -3.6 (p 0.487) | -1.4 (p 0.681) |
| 19 | -20.3 (p 0.007) | -22.1 (p 0.008) |
| 20 | +5.8 (p 0.606) | -1.5 (p 0.865) |
| 21 | -0.4 (p 1.000) | -3.7 (p 0.754) |

**Loss against gain (x1)**: layer 18 -0.5 (p 0.679); layer 19 +1.3 (p 0.026); layer 20 +2.9 (p 0.029); layer 21 +6.1 (p 0.098).

## The agent's own replies (two sampled per moment)

| Condition | Replies | Went along | Unreadable |
|---|---|---|---|
| none | 32 | 25% | 6% |
| gain x1 at layer 18 | 32 | 28% | 9% |
| gain x1 at layer 19 | 32 | 31% | 9% |
| gain x1 at layer 20 | 32 | 34% | 6% |
| gain x1 at layer 21 | 32 | 47% | 6% |
| loss x1 at layer 18 | 32 | 34% | 9% |
| loss x1 at layer 19 | 32 | 16% | 12% |
| loss x1 at layer 20 | 32 | 38% | 0% |
| loss x1 at layer 21 | 32 | 25% | 6% |

Coverage over the included moments, every condition: median 0.99, 10th percentile 0.82.
