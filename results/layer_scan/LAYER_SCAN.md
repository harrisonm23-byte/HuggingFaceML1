# Confirmation scan: each document's after-reading state at layers 18-21 (exploratory)

16 moments (B's 10 neutral careers at the 7 and 12 January requests; 4 more left out because the scored orders cover less than half of the model's probability with no injection). Each document type's after-reading change over the request's update, minus the neutral document's, built on the other half of the careers and added with no document at one layer. With no injection, P(the order goes along) averages 35.6%. Produced by `designs/rd2/analysis/layer_scan.py`.

## The read-out: P(the order goes along), change from no injection (points)

| Layer | loss x1 | loss x2 | blame x1 | blame x2 | gain x1 | gain x2 | credit x1 | credit x2 | random x2 |
|---|---|---|---|---|---|---|---|---|---|
| 18 | +2.1 (p 0.055) | +4.9 (p 0.009) | +1.7 (p 0.575) | +2.4 (p 0.612) | +1.8 (p 0.490) | +0.9 (p 0.790) | +0.3 (p 0.758) | -1.0 (p 0.627) | +7.9 (p 0.194) |
| 19 | +7.9 (p 0.009) | +18.1 (p 0.006) | +11.5 (p 0.014) | +28.1 (p 0.008) | +2.0 (p 0.442) | +2.6 (p 0.554) | +1.5 (p 0.524) | +5.0 (p 0.298) | -13.7 (p 0.294) |
| 20 | +13.0 (p 0.009) | +26.3 (p 0.009) | +17.3 (p 0.031) | +26.9 (p 0.024) | +3.3 (p 0.533) | +3.9 (p 0.560) | +1.0 (p 0.548) | -0.4 (p 0.959) | +12.9 (p 0.247) |
| 21 | +13.4 (p 0.008) | +24.6 (p 0.007) | +15.0 (p 0.031) | +25.8 (p 0.008) | +3.9 (p 0.234) | +8.8 (p 0.157) | +1.6 (p 0.556) | -0.2 (p 0.992) | +21.9 (p 0.008) |

**Against the random direction of the same size (x2)**

| Layer | loss | blame | gain | credit |
|---|---|---|---|---|
| 18 | -2.9 (p 0.595) | -5.5 (p 0.102) | -6.9 (p 0.044) | -8.9 (p 0.037) |
| 19 | +31.7 (p 0.023) | +41.7 (p 0.009) | +16.2 (p 0.229) | +18.6 (p 0.163) |
| 20 | +13.4 (p 0.151) | +14.0 (p 0.103) | -9.0 (p 0.242) | -13.3 (p 0.177) |
| 21 | +2.8 (p 0.657) | +4.0 (p 0.844) | -13.0 (p 0.083) | -22.0 (p 0.008) |

**Loss against gain (x1)**: layer 18 +0.3 (p 0.511); layer 19 +5.9 (p 0.008); layer 20 +9.7 (p 0.008); layer 21 +9.5 (p 0.007).

## The agent's own replies (two sampled per moment)

| Condition | Replies | Went along | Unreadable |
|---|---|---|---|
| none | 32 | 31% | 6% |
| blame x1 at layer 18 | 32 | 25% | 9% |
| blame x1 at layer 19 | 32 | 25% | 6% |
| blame x1 at layer 20 | 32 | 31% | 6% |
| blame x1 at layer 21 | 32 | 50% | 6% |
| credit x1 at layer 18 | 32 | 22% | 12% |
| credit x1 at layer 19 | 32 | 25% | 9% |
| credit x1 at layer 20 | 32 | 31% | 3% |
| credit x1 at layer 21 | 32 | 16% | 12% |
| gain x1 at layer 18 | 32 | 28% | 12% |
| gain x1 at layer 19 | 32 | 25% | 6% |
| gain x1 at layer 20 | 32 | 19% | 6% |
| gain x1 at layer 21 | 32 | 28% | 6% |
| loss x1 at layer 18 | 32 | 22% | 12% |
| loss x1 at layer 19 | 32 | 28% | 6% |
| loss x1 at layer 20 | 32 | 31% | 6% |
| loss x1 at layer 21 | 32 | 50% | 6% |

Coverage over the included moments, every condition: median 1.00, 10th percentile 0.91.
