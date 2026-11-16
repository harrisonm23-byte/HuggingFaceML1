# Layer sweep: each document's after-reading state at layers 4-42 (exploratory)

16 moments (B's 10 neutral careers at the 7 and 12 January requests; 4 more left out because the scored orders cover less than half of the model's probability with no injection). Each document type's after-reading change over the request's update, minus the neutral document's, built on the other half of the careers and added with no document at one layer. With no injection, P(the order goes along) averages 36.1%. Produced by `designs/rd2/analysis/layer_scan.py`.

## The read-out: P(the order goes along), change from no injection (points)

| Layer | loss x2 | gain x2 | random x2 |
|---|---|---|---|
| 4 | -1.4 (p 0.248) | -0.6 (p 0.685) | +3.8 (p 0.837) |
| 6 | +0.2 (p 0.807) | -3.3 (p 0.120) | +0.1 (p 0.935) |
| 8 | -1.4 (p 0.585) | -2.9 (p 0.674) | +1.0 (p 0.377) |
| 10 | -1.6 (p 0.834) | -4.6 (p 0.117) | -2.2 (p 0.638) |
| 12 | -1.6 (p 0.901) | -2.7 (p 0.879) | -16.7 (p 0.154) |
| 14 | +6.2 (p 0.008) | +4.6 (p 0.021) | +4.2 (p 0.499) |
| 16 | -4.1 (p 0.100) | -2.1 (p 0.342) | -0.0 (p 0.963) |
| 18 | -1.3 (p 0.994) | +1.0 (p 0.622) | +10.0 (p 0.263) |
| 20 | +3.2 (p 0.461) | -4.1 (p 0.039) | +12.1 (p 0.021) |
| 22 | +7.6 (p 0.009) | +6.9 (p 0.045) | +9.4 (p 0.320) |
| 24 | +3.5 (p 0.790) | -2.8 (p 0.008) | -0.8 (p 0.590) |
| 26 | +7.4 (p 0.016) | +0.1 (p 0.912) | +3.1 (p 0.023) |
| 28 | +2.7 (p 0.520) | -3.0 (p 0.064) | +0.4 (p 0.640) |
| 30 | -0.2 (p 0.611) | -0.8 (p 0.272) | +4.9 (p 0.257) |
| 32 | +0.5 (p 0.671) | +0.5 (p 0.008) | -0.2 (p 0.811) |
| 34 | -0.1 (p 0.979) | +0.3 (p 0.267) | -2.0 (p 0.023) |
| 36 | -0.1 (p 1.000) | -0.0 (p 1.000) | -1.1 (p 0.447) |
| 38 | +0.1 (p 0.755) | +1.1 (p 0.008) | -3.6 (p 0.170) |
| 40 | +0.2 (p 0.646) | +0.6 (p 0.306) | +1.8 (p 0.566) |
| 42 | +0.0 (p 0.964) | -0.2 (p 0.974) | -0.5 (p 0.585) |

**Against the random direction of the same size (x2)**

| Layer | loss | gain |
|---|---|---|
| 4 | -5.2 (p 0.348) | -4.4 (p 0.375) |
| 6 | +0.1 (p 0.929) | -3.4 (p 0.296) |
| 8 | -2.4 (p 0.532) | -3.9 (p 0.404) |
| 10 | +0.7 (p 0.375) | -2.4 (p 0.194) |
| 12 | +15.1 (p 0.159) | +14.0 (p 0.157) |
| 14 | +2.0 (p 0.752) | +0.4 (p 0.901) |
| 16 | -4.0 (p 0.308) | -2.1 (p 0.443) |
| 18 | -11.3 (p 0.169) | -9.0 (p 0.436) |
| 20 | -8.9 (p 0.221) | -16.2 (p 0.029) |
| 22 | -1.7 (p 0.855) | -2.5 (p 0.406) |
| 24 | +4.3 (p 0.614) | -2.0 (p 0.400) |
| 26 | +4.3 (p 0.599) | -3.0 (p 0.219) |
| 28 | +2.3 (p 0.411) | -3.5 (p 0.015) |
| 30 | -5.1 (p 0.430) | -5.7 (p 0.131) |
| 32 | +0.7 (p 0.560) | +0.7 (p 0.416) |
| 34 | +1.9 (p 0.275) | +2.4 (p 0.023) |
| 36 | +1.0 (p 0.397) | +1.1 (p 0.450) |
| 38 | +3.7 (p 0.052) | +4.7 (p 0.009) |
| 40 | -1.6 (p 0.960) | -1.2 (p 0.698) |
| 42 | +0.5 (p 0.527) | +0.3 (p 0.537) |

**Loss against gain (x1)**: layer 4 –; layer 6 –; layer 8 –; layer 10 –; layer 12 –; layer 14 –; layer 16 –; layer 18 –; layer 20 –; layer 22 –; layer 24 –; layer 26 –; layer 28 –; layer 30 –; layer 32 –; layer 34 –; layer 36 –; layer 38 –; layer 40 –; layer 42 –.

## The agent's own replies (two sampled per moment)

| Condition | Replies | Went along | Unreadable |
|---|---|---|---|
| none | 32 | 28% | 6% |

Coverage over the included moments, every condition: median 0.98, 10th percentile 0.63.
