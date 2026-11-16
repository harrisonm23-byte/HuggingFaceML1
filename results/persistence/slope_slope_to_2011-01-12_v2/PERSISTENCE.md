# Persistence check: does a state pushed once at the top reach later decisions?

5 careers from `results/full_career_gemma-3-12b-it_4bit_slope_slope_to_2011-01-12_v2`, reread at bfloat16 with the text unchanged. Each state is added at 8 x its natural size at one layer to the pushed moment (the first 7 January update, with the memo, and the reply under it: about 319 tokens) at every read, as the jolt is kept. "Left" is the push's change to the agent's state at a later decision as a share of its change at the pushed moment itself, at the same layer (1 = all of it); "cos" whether it still points the same way. Layers that see the whole conversation: 5, 11, 17, 23, 29, 35, 41, 47. Means over careers. Produced by `designs/rd2/analysis/persistence.py`.


## Pushed at layer 14: what is left at layer 17

| Moment | Tokens after the push | loss x8 L14 | gain x8 L14 | blame x8 L14 | credit x8 L14 | random x8 L14 |
|---|---|---|---|---|---|---|
| 2011-01-07 08:15 | 250 | 13% (cos +0.85) | 12% (cos +0.84) | 12% (cos +0.84) | 13% (cos +0.84) | 22% (cos +0.03) |
| 2011-01-07 09:45 | 2,121 | 3% (cos +0.90) | 4% (cos +0.92) | 3% (cos +0.71) | 4% (cos +0.91) | 5% (cos +0.01) |
| 2011-01-07 13:45 | 6,882 | 2% (cos +0.39) | 2% (cos +0.38) | 2% (cos +0.38) | 2% (cos +0.38) | 4% (cos +0.06) |
| 2011-01-12 08:00 | 7,205 | 7% (cos +0.93) | 7% (cos +0.93) | 6% (cos +0.91) | 7% (cos +0.92) | 10% (cos -0.07) |
| 2011-01-12 09:30 | 8,995 | 3% (cos +0.75) | 2% (cos +0.56) | 2% (cos +0.55) | 2% (cos +0.55) | 5% (cos -0.04) |
| 2011-01-12 13:45 | 13,868 | 1% (cos +0.38) | 1% (cos +0.39) | 1% (cos +0.38) | 1% (cos +0.38) | 2% (cos +0.01) |

## Pushed at layer 14: what is left at layer 47

| Moment | Tokens after the push | loss x8 L14 | gain x8 L14 | blame x8 L14 | credit x8 L14 | random x8 L14 |
|---|---|---|---|---|---|---|
| 2011-01-07 08:15 | 250 | 69% (cos +0.07) | 76% (cos +0.31) | 75% (cos +0.27) | 83% (cos +0.31) | 26% (cos -0.43) |
| 2011-01-07 09:45 | 2,121 | 21% (cos -0.15) | 20% (cos +0.06) | 19% (cos +0.08) | 22% (cos +0.16) | 7% (cos -0.25) |
| 2011-01-07 13:45 | 6,882 | 9% (cos +0.05) | 9% (cos -0.01) | 7% (cos +0.09) | 8% (cos -0.02) | 5% (cos -0.33) |
| 2011-01-12 08:00 | 7,205 | 27% (cos +0.02) | 26% (cos -0.09) | 23% (cos -0.05) | 27% (cos -0.08) | 9% (cos +0.13) |
| 2011-01-12 09:30 | 8,995 | 9% (cos +0.03) | 9% (cos -0.10) | 9% (cos -0.05) | 10% (cos -0.15) | 3% (cos +0.09) |
| 2011-01-12 13:45 | 13,868 | 7% (cos +0.18) | 6% (cos +0.17) | 6% (cos +0.14) | 6% (cos -0.07) | 3% (cos -0.25) |

## Pushed at layer 22: what is left at layer 23

| Moment | Tokens after the push | loss x8 L22 | gain x8 L22 | blame x8 L22 | credit x8 L22 | random x8 L22 |
|---|---|---|---|---|---|---|
| 2011-01-07 08:15 | 250 | 21% (cos +0.34) | 21% (cos +0.47) | 21% (cos +0.07) | 22% (cos +0.51) | 14% (cos +0.12) |
| 2011-01-07 09:45 | 2,121 | 7% (cos +0.17) | 8% (cos +0.28) | 8% (cos +0.04) | 7% (cos +0.35) | 4% (cos +0.05) |
| 2011-01-07 13:45 | 6,882 | 8% (cos +0.23) | 6% (cos +0.34) | 5% (cos +0.07) | 3% (cos +0.10) | 1% (cos +0.00) |
| 2011-01-12 08:00 | 7,205 | 20% (cos +0.47) | 21% (cos +0.52) | 24% (cos +0.15) | 22% (cos +0.55) | 14% (cos +0.15) |
| 2011-01-12 09:30 | 8,995 | 3% (cos +0.11) | 5% (cos +0.25) | 4% (cos +0.04) | 4% (cos +0.10) | 1% (cos +0.01) |
| 2011-01-12 13:45 | 13,868 | 2% (cos +0.12) | 2% (cos +0.13) | 2% (cos +0.05) | 2% (cos +0.14) | 1% (cos +0.06) |

## Pushed at layer 22: what is left at layer 47

| Moment | Tokens after the push | loss x8 L22 | gain x8 L22 | blame x8 L22 | credit x8 L22 | random x8 L22 |
|---|---|---|---|---|---|---|
| 2011-01-07 08:15 | 250 | 37% (cos -0.21) | 35% (cos -0.12) | 40% (cos -0.13) | 39% (cos +0.03) | 32% (cos +0.01) |
| 2011-01-07 09:45 | 2,121 | 15% (cos +0.22) | 10% (cos +0.19) | 15% (cos +0.13) | 9% (cos +0.14) | 7% (cos +0.01) |
| 2011-01-07 13:45 | 6,882 | 6% (cos -0.04) | 6% (cos +0.10) | 5% (cos +0.08) | 6% (cos +0.04) | 3% (cos -0.02) |
| 2011-01-12 08:00 | 7,205 | 17% (cos -0.17) | 17% (cos -0.16) | 17% (cos -0.12) | 18% (cos -0.08) | 12% (cos -0.04) |
| 2011-01-12 09:30 | 8,995 | 5% (cos -0.03) | 5% (cos +0.11) | 5% (cos +0.07) | 6% (cos +0.10) | 4% (cos -0.05) |
| 2011-01-12 13:45 | 13,868 | 3% (cos -0.15) | 4% (cos +0.03) | 3% (cos +0.04) | 4% (cos -0.03) | 3% (cos +0.06) |

## The agent's order at the key moments

Change from no push: P(the order goes toward the stops) in points, the expected position it sets (oz), and P(it changes its position) in points; in brackets, the careers where it moved toward the stops.

| Moment | Push | Toward the stops | Expected position | Changes position |
|---|---|---|---|---|
| 2011-01-07 09:45 | loss x8 L14 | +5.5 (3/5) | +25,466 | +9.7 |
| 2011-01-07 09:45 | gain x8 L14 | +9.0 (3/5) | +37,680 | +11.9 |
| 2011-01-07 09:45 | blame x8 L14 | -0.7 (3/5) | +15,991 | +4.8 |
| 2011-01-07 09:45 | credit x8 L14 | +7.3 (4/5) | +25,045 | +8.9 |
| 2011-01-07 09:45 | random x8 L14 | +7.4 (3/5) | +14,611 | +9.6 |
| 2011-01-07 09:45 | loss x8 L22 | +7.0 (2/5) | +2,821 | +6.9 |
| 2011-01-07 09:45 | gain x8 L22 | +6.7 (4/5) | +4,066 | +5.6 |
| 2011-01-07 09:45 | blame x8 L22 | +10.6 (2/5) | +5,397 | +10.0 |
| 2011-01-07 09:45 | credit x8 L22 | +6.8 (3/5) | +3,803 | +6.1 |
| 2011-01-07 09:45 | random x8 L22 | +12.5 (4/5) | +18,154 | +12.3 |
| 2011-01-12 08:00 | loss x8 L14 | +32.0 (4/5) | +41,124 | +32.1 |
| 2011-01-12 08:00 | gain x8 L14 | +46.6 (4/5) | +60,186 | +46.7 |
| 2011-01-12 08:00 | blame x8 L14 | +37.7 (4/5) | +50,040 | +37.7 |
| 2011-01-12 08:00 | credit x8 L14 | +46.1 (4/5) | +61,764 | +46.1 |
| 2011-01-12 08:00 | random x8 L14 | +2.5 (3/5) | -817 | +4.5 |
| 2011-01-12 08:00 | loss x8 L22 | +21.4 (4/5) | +17,076 | +21.4 |
| 2011-01-12 08:00 | gain x8 L22 | +18.1 (4/5) | +13,233 | +18.2 |
| 2011-01-12 08:00 | blame x8 L22 | +22.0 (4/5) | +18,313 | +22.0 |
| 2011-01-12 08:00 | credit x8 L22 | +18.8 (4/5) | +13,413 | +18.8 |
| 2011-01-12 08:00 | random x8 L22 | +53.0 (4/5) | +64,925 | +53.0 |
| 2011-01-12 09:30 | loss x8 L14 | +0.1 (2/5) | -1,096 | +2.0 |
| 2011-01-12 09:30 | gain x8 L14 | +0.1 (4/5) | -1,323 | +2.4 |
| 2011-01-12 09:30 | blame x8 L14 | -0.2 (4/5) | -1,445 | +0.6 |
| 2011-01-12 09:30 | credit x8 L14 | -0.1 (4/5) | -1,292 | +1.5 |
| 2011-01-12 09:30 | random x8 L14 | +0.0 (4/5) | -1,502 | +1.3 |
| 2011-01-12 09:30 | loss x8 L22 | -0.4 (2/5) | +1,040 | -0.5 |
| 2011-01-12 09:30 | gain x8 L22 | -1.3 (2/5) | +1,641 | -1.2 |
| 2011-01-12 09:30 | blame x8 L22 | -0.2 (2/5) | +630 | -0.3 |
| 2011-01-12 09:30 | credit x8 L22 | -0.9 (2/5) | +2,223 | -0.8 |
| 2011-01-12 09:30 | random x8 L22 | -0.7 (2/5) | +1,643 | -0.9 |
