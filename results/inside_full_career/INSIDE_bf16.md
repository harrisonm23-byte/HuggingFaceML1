# Inside the model at the push requests (full careers)

States: Gemma 3 12B at bf16, the last token before each push-request reply, 1740 moments (A: 180, B: 300, C: 240, C2: 180, D: 240, E: 300, F: 300). Every comparison is within the same request (went along vs not: within the same request, experiment and framing); p-values reshuffle labels within those groups (1000 times); q = false-discovery-corrected. Features active in fewer than 5% of the moments compared are left out. Produced by `designs/rd2/analysis/inside_features.py`.

Gemma Scope 2 (google/gemma-scope-2-12b-it, residual stream, 16k): layers [12, 24, 31, 41]; files `resid_post/layer_12_width_16k_l0_medium/params.safetensors`, `resid_post/layer_24_width_16k_l0_medium/params.safetensors`, `resid_post/layer_31_width_16k_l0_medium/params.safetensors`, `resid_post/layer_41_width_16k_l0_medium/params.safetensors`. Each table lists the 15 features that differ most on half the careers, then the same features on the other half (confirmed: the same sign, p < 0.05 there); the count of features with q < 0.05 is over all careers.


## B: UBS's loss frame vs gain frame

**Layer 12** (120 vs 120 moments; 56 features tested; 23 with q < 0.05; 9 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +1.08 | +0.87 | +3.38 | 0.0010 | yes | 0.007 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.82 | +0.57 | +1.89 | 0.0220 | yes | 0.007 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -0.80 | -0.99 | -21.03 | 0.0010 | yes | 0.007 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.76 | +0.06 | +0.17 | 0.7932 | no | 0.007 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.75 | -0.39 | -4.20 | 0.1029 | no | 0.013 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.74 | -0.22 | -1.08 | 0.3287 | no | 0.012 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.72 | -0.78 | -17.66 | 0.0020 | yes | 0.007 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.72 | +0.45 | +6.12 | 0.0529 | no | 0.010 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.69 | +1.07 | +5.75 | 0.0010 | yes | 0.007 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -0.68 | -1.20 | -15.14 | 0.0010 | yes | 0.007 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.65 | +0.40 | +1.11 | 0.0829 | no | 0.013 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.59 | +0.40 | +1.15 | 0.0759 | no | 0.010 |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | -0.59 | -0.63 | -8.16 | 0.0050 | yes | 0.013 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +0.56 | +0.84 | +6.89 | 0.0010 | yes | 0.012 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +0.52 | +0.79 | +7.48 | 0.0020 | yes | 0.012 |

**Layer 24** (120 vs 120 moments; 151 features tested; 59 with q < 0.05; 2 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [7741](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7741) | +1.50 | +0.17 | +21.65 | 0.4835 | no | 0.004 |
| [8967](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8967) | +1.25 | +0.43 | +29.13 | 0.0779 | no | 0.004 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +1.18 | +0.07 | +3.71 | 0.7802 | no | 0.007 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3051) | +1.13 | +0.01 | +2.07 | 0.9570 | no | 0.004 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | +1.10 | +0.30 | +20.93 | 0.1738 | no | 0.004 |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | +1.04 | +0.70 | +51.12 | 0.0030 | yes | 0.004 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | -1.00 | -0.60 | -91.80 | 0.0120 | yes | 0.004 |
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.96 | -0.22 | -7.57 | 0.3327 | no | 0.007 |
| [8992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8992) | -0.95 | -0.27 | -22.60 | 0.2507 | no | 0.004 |
| [7789](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7789) | +0.93 | +0.18 | +23.05 | 0.4236 | no | 0.007 |
| [11105](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11105) | -0.89 | -0.38 | -16.38 | 0.0889 | no | 0.004 |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | -0.87 | +0.17 | +10.97 | 0.4306 | no | 0.077 |
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | +0.87 | +0.20 | +30.86 | 0.3487 | no | 0.004 |
| [15592](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592) | -0.86 | -0.42 | -16.52 | 0.0719 | no | 0.004 |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | -0.85 | -0.26 | -84.24 | 0.2687 | no | 0.004 |

**Layer 31** (120 vs 120 moments; 162 features tested; 47 with q < 0.05; 2 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [3369](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3369) | +1.13 | -0.12 | -27.88 | 0.6064 | no | 0.009 |
| [195](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/195) | +0.92 | +0.40 | +48.40 | 0.0759 | no | 0.009 |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | +0.92 | +0.40 | +164.12 | 0.0959 | no | 0.009 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +0.86 | +0.40 | +82.04 | 0.1119 | no | 0.009 |
| [929](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/929) | +0.84 | +0.45 | +85.10 | 0.0440 | yes | 0.009 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | -0.80 | -0.32 | -90.87 | 0.1489 | no | 0.009 |
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | +0.78 | -0.24 | -44.96 | 0.2987 | no | 0.327 |
| [2079](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2079) | -0.78 | -0.22 | -47.29 | 0.3746 | no | 0.013 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | -0.76 | -0.30 | -152.92 | 0.2088 | no | 0.009 |
| [9310](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9310) | +0.72 | +0.12 | +16.91 | 0.5984 | no | 0.082 |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | +0.70 | +0.27 | +105.46 | 0.2567 | no | 0.009 |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | +0.70 | +0.58 | +119.88 | 0.0190 | yes | 0.009 |
| [3251](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3251) | -0.67 | -0.13 | -46.94 | 0.6084 | no | 0.009 |
| [4214](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4214) | -0.67 | -0.13 | -47.27 | 0.5784 | no | 0.013 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | +0.66 | +0.10 | +55.16 | 0.6793 | no | 0.009 |

**Layer 41** (120 vs 120 moments; 163 features tested; 27 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | +0.94 | +0.24 | +163.16 | 0.2917 | no | 0.016 |
| [12726](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12726) | +0.79 | +0.30 | +96.95 | 0.1968 | no | 0.016 |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | +0.79 | +0.37 | +200.93 | 0.1219 | no | 0.016 |
| [1838](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1838) | +0.76 | +0.10 | +17.07 | 0.6633 | no | 0.041 |
| [755](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/755) | -0.76 | -0.34 | -355.13 | 0.1419 | no | 0.018 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | +0.76 | +0.16 | +105.65 | 0.5085 | no | 0.018 |
| [2903](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2903) | +0.74 | +0.44 | +214.17 | 0.0579 | no | 0.016 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | -0.73 | -0.12 | -94.78 | 0.5964 | no | 0.048 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +0.73 | +0.35 | +594.47 | 0.1129 | no | 0.016 |
| [10562](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10562) | -0.73 | -0.05 | -47.57 | 0.8122 | no | 0.079 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | +0.71 | +0.01 | +1.99 | 0.9750 | no | 0.174 |
| [942](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/942) | -0.70 | -0.18 | -75.93 | 0.4466 | no | 0.051 |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | -0.70 | -0.02 | -6.99 | 0.8891 | no | 0.018 |
| [9177](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9177) | -0.69 | -0.21 | -269.65 | 0.3716 | no | 0.031 |
| [10495](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10495) | -0.68 | -0.22 | -221.44 | 0.3227 | no | 0.041 |


## B: "+ you" vs no owner

**Layer 12** (120 vs 120 moments; 56 features tested; 16 with q < 0.05; 8 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | -1.04 | -0.47 | -4.19 | 0.0270 | yes | 0.006 |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | -0.93 | -0.09 | -1.31 | 0.7003 | no | 0.028 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.72 | +0.81 | +2.49 | 0.0020 | yes | 0.006 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.67 | -0.37 | -1.78 | 0.0819 | no | 0.006 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.62 | -1.04 | -9.45 | 0.0010 | yes | 0.006 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | -0.62 | -0.13 | -0.79 | 0.5175 | no | 0.062 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.62 | -0.73 | -5.25 | 0.0020 | yes | 0.006 |
| [15474](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15474) | -0.61 | -0.11 | -0.93 | 0.6533 | no | 0.072 |
| [978](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/978) | +0.60 | +0.59 | +1.01 | 0.0080 | yes | 0.006 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.59 | +1.21 | +8.95 | 0.0010 | yes | 0.006 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | +0.52 | +0.33 | +4.16 | 0.1169 | no | 0.030 |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | +0.49 | +0.64 | +7.54 | 0.0060 | yes | 0.006 |
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | -0.46 | +0.29 | +1.19 | 0.1728 | no | 0.425 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.46 | -0.47 | -11.08 | 0.0270 | yes | 0.006 |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | -0.45 | +0.65 | +6.12 | 0.0050 | no | 0.465 |

**Layer 24** (120 vs 120 moments; 151 features tested; 38 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [8992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8992) | -1.01 | -0.02 | -1.35 | 0.9391 | no | 0.015 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | +1.00 | +0.14 | +9.73 | 0.4935 | no | 0.011 |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | -0.89 | +0.07 | +21.90 | 0.7692 | no | 0.020 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | -0.88 | +0.25 | +13.61 | 0.2458 | no | 0.055 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | -0.87 | -0.07 | -31.62 | 0.7393 | no | 0.015 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | -0.84 | -0.09 | -17.98 | 0.6773 | no | 0.011 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.84 | +0.71 | +32.60 | 0.0030 | yes | 0.011 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | +0.79 | +0.18 | +21.32 | 0.3896 | no | 0.011 |
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | +0.77 | +0.03 | +4.69 | 0.9061 | no | 0.015 |
| [11587](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11587) | -0.76 | +0.10 | +11.38 | 0.6543 | no | 0.068 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | -0.76 | +0.11 | +17.34 | 0.6064 | no | 0.098 |
| [379](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/379) | -0.74 | -0.20 | -15.28 | 0.3467 | no | 0.021 |
| [2391](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2391) | -0.74 | +0.29 | +26.16 | 0.1968 | no | 0.224 |
| [6754](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6754) | -0.72 | -0.14 | -7.65 | 0.5125 | no | 0.060 |
| [5052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5052) | -0.70 | -0.03 | -1.54 | 0.8781 | no | 0.041 |

**Layer 31** (120 vs 120 moments; 162 features tested; 64 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | +1.54 | +0.26 | +144.04 | 0.2328 | no | 0.005 |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | +1.51 | +0.12 | +51.63 | 0.5594 | no | 0.005 |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | +1.38 | +0.14 | +57.63 | 0.4815 | no | 0.005 |
| [4214](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4214) | -1.35 | -0.16 | -56.98 | 0.4735 | no | 0.005 |
| [2900](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2900) | -1.33 | -0.08 | -18.43 | 0.7113 | no | 0.005 |
| [4805](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4805) | -1.31 | -0.14 | -69.95 | 0.5175 | no | 0.005 |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | +1.25 | -0.04 | -21.71 | 0.8511 | no | 0.005 |
| [2608](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2608) | -1.23 | -0.11 | -25.09 | 0.6234 | no | 0.005 |
| [3251](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3251) | -1.23 | -0.10 | -35.67 | 0.6474 | no | 0.005 |
| [6048](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6048) | -1.22 | -0.02 | -4.00 | 0.9271 | no | 0.005 |
| [13577](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13577) | -1.22 | -0.13 | -40.40 | 0.5574 | no | 0.005 |
| [7092](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7092) | -1.21 | -0.13 | -32.69 | 0.5375 | no | 0.005 |
| [15017](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15017) | -1.21 | -0.16 | -29.79 | 0.4655 | no | 0.005 |
| [3315](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3315) | -1.18 | -0.09 | -15.51 | 0.6474 | no | 0.005 |
| [137](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/137) | -1.11 | -0.13 | -50.22 | 0.5245 | no | 0.005 |

**Layer 41** (120 vs 120 moments; 163 features tested; 41 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | +1.59 | +0.37 | +588.62 | 0.0849 | no | 0.008 |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | -1.36 | +0.00 | +1.28 | 0.9880 | no | 0.008 |
| [822](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/822) | -1.32 | -0.11 | -140.32 | 0.6214 | no | 0.008 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | +1.31 | +0.13 | +85.45 | 0.5594 | no | 0.008 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +1.26 | +0.14 | +250.35 | 0.5055 | no | 0.008 |
| [755](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/755) | -1.25 | +0.10 | +102.26 | 0.6464 | no | 0.008 |
| [897](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/897) | -1.17 | -0.05 | -16.92 | 0.8032 | no | 0.008 |
| [946](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/946) | -1.09 | +0.09 | +49.79 | 0.6823 | no | 0.008 |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1571) | -1.08 | -0.06 | -65.50 | 0.7822 | no | 0.008 |
| [10433](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10433) | -1.07 | -0.12 | -49.47 | 0.6454 | no | 0.008 |
| [10495](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10495) | -1.02 | +0.15 | +151.78 | 0.4645 | no | 0.014 |
| [2903](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2903) | +0.98 | +0.26 | +125.62 | 0.2617 | no | 0.008 |
| [12726](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12726) | +0.98 | +0.01 | +4.32 | 0.9411 | no | 0.019 |
| [1951](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1951) | -0.95 | +0.22 | +77.94 | 0.2907 | no | 0.046 |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | +0.91 | +0.20 | +105.11 | 0.3676 | no | 0.019 |


## B: framed vs neutral

**Layer 12** (240 vs 60 moments; 56 features tested; 36 with q < 0.05; 15 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | +2.29 | +2.22 | +7.50 | 0.0010 | yes | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +2.25 | +2.21 | +7.56 | 0.0010 | yes | 0.002 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -2.11 | -2.04 | -33.75 | 0.0010 | yes | 0.002 |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | +2.00 | +1.60 | +14.35 | 0.0010 | yes | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +1.87 | +0.88 | +2.76 | 0.0010 | yes | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +1.83 | +1.36 | +20.78 | 0.0010 | yes | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +1.82 | +1.74 | +6.76 | 0.0010 | yes | 0.002 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +1.71 | +1.44 | +18.69 | 0.0010 | yes | 0.002 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | -1.70 | -1.20 | -16.43 | 0.0010 | yes | 0.002 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +1.55 | +1.56 | +17.05 | 0.0010 | yes | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +1.53 | +1.29 | +11.75 | 0.0010 | yes | 0.002 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +1.52 | +1.32 | +15.54 | 0.0010 | yes | 0.002 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -1.49 | -1.36 | -32.83 | 0.0010 | yes | 0.002 |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +1.46 | +1.24 | +13.48 | 0.0010 | yes | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -1.45 | -1.08 | -8.07 | 0.0010 | yes | 0.002 |

**Layer 24** (240 vs 60 moments; 147 features tested; 22 with q < 0.05; 7 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [11165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11165) | -0.98 | -0.48 | -12.47 | 0.0110 | yes | 0.010 |
| [11000](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11000) | -0.93 | -0.73 | -48.97 | 0.0030 | yes | 0.010 |
| [1149](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1149) | +0.91 | +0.36 | +18.93 | 0.0719 | no | 0.010 |
| [11552](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11552) | -0.84 | +0.06 | +3.29 | 0.7512 | no | 0.114 |
| [15043](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15043) | -0.83 | -0.05 | -4.07 | 0.7732 | no | 0.092 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | -0.83 | -0.62 | -16.96 | 0.0030 | yes | 0.010 |
| [4392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4392) | -0.83 | +0.28 | +15.41 | 0.2218 | no | 0.392 |
| [8326](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326) | -0.79 | -0.16 | -19.73 | 0.4006 | no | 0.080 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | -0.77 | -0.55 | -52.11 | 0.0040 | yes | 0.010 |
| [13585](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13585) | +0.73 | +0.60 | +17.58 | 0.0040 | yes | 0.010 |
| [11105](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11105) | -0.72 | -0.40 | -21.36 | 0.0360 | yes | 0.015 |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | -0.71 | -0.03 | -4.10 | 0.8721 | no | 0.275 |
| [7283](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7283) | -0.71 | +0.65 | +58.77 | 0.0010 | no | 0.820 |
| [15074](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074) | +0.70 | +0.12 | +14.76 | 0.5534 | no | 0.085 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.70 | +0.57 | +26.34 | 0.0070 | yes | 0.010 |

**Layer 31** (240 vs 60 moments; 160 features tested; 27 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2069](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2069) | -1.24 | -0.21 | -43.62 | 0.2787 | no | 0.030 |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | -1.12 | -0.45 | -95.10 | 0.0280 | yes | 0.023 |
| [1519](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1519) | -0.93 | -0.29 | -63.18 | 0.1708 | no | 0.023 |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | +0.91 | +0.03 | +11.99 | 0.8881 | no | 0.047 |
| [5652](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652) | -0.86 | -0.07 | -6.63 | 0.7283 | no | 0.038 |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | -0.83 | +0.15 | +83.19 | 0.4605 | no | 0.141 |
| [12956](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12956) | -0.80 | -0.31 | -43.34 | 0.1289 | no | 0.030 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | -0.75 | +0.02 | +2.41 | 0.9271 | no | 0.192 |
| [4805](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4805) | +0.75 | -0.09 | -43.91 | 0.6713 | no | 0.141 |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | -0.72 | +0.07 | +22.33 | 0.7393 | no | 0.279 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | -0.70 | -0.22 | -115.43 | 0.2687 | no | 0.030 |
| [1744](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1744) | -0.69 | -0.20 | -46.67 | 0.3277 | no | 0.051 |
| [1412](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1412) | -0.68 | -0.13 | -26.45 | 0.5185 | no | 0.094 |
| [2900](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2900) | +0.66 | +0.25 | +53.85 | 0.2138 | no | 0.030 |
| [137](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/137) | +0.66 | +0.04 | +15.45 | 0.8332 | no | 0.134 |

**Layer 41** (240 vs 60 moments; 166 features tested; 17 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2880](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2880) | -1.32 | -0.02 | -6.52 | 0.9031 | no | 0.028 |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | -1.24 | -0.11 | -73.95 | 0.5834 | no | 0.028 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | -1.09 | -0.14 | -58.34 | 0.4765 | no | 0.049 |
| [3420](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3420) | -1.09 | -0.13 | -41.60 | 0.5195 | no | 0.028 |
| [10380](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10380) | -0.89 | -0.33 | -65.18 | 0.1528 | no | 0.028 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | -0.85 | -0.07 | -19.44 | 0.7353 | no | 0.178 |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | -0.80 | -0.14 | -28.09 | 0.4955 | no | 0.079 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | -0.74 | +0.02 | +15.29 | 0.9111 | no | 0.157 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | -0.72 | +0.20 | +350.29 | 0.3187 | no | 0.243 |
| [3296](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3296) | -0.71 | -0.10 | -45.83 | 0.6144 | no | 0.042 |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | -0.70 | +0.09 | +38.60 | 0.6743 | no | 0.275 |
| [13569](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13569) | -0.69 | -0.38 | -96.24 | 0.1179 | no | 0.028 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | -0.69 | -0.41 | -145.59 | 0.0430 | yes | 0.028 |
| [2932](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2932) | -0.68 | -0.07 | -13.72 | 0.7493 | no | 0.157 |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | -0.67 | -0.21 | -84.32 | 0.3157 | no | 0.089 |


## All experiments: went along vs did not (same request, experiment and framing)

**Layer 12** (286 vs 1424 moments; 56 features tested; 0 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1245](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1245) | -0.59 | -0.23 | -1.46 | 0.2967 | no | 0.123 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.51 | -0.34 | -1.02 | 0.1329 | no | 0.112 |
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | -0.48 | -0.56 | -2.47 | 0.0180 | yes | 0.112 |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | +0.47 | -0.02 | -0.06 | 0.9381 | no | 0.813 |
| [1699](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1699) | -0.44 | +0.04 | +0.07 | 0.8372 | no | 0.668 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +0.39 | +0.21 | +0.55 | 0.3297 | no | 0.263 |
| [1272](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272) | -0.35 | +0.01 | +0.02 | 0.9810 | no | 0.431 |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | -0.32 | -0.01 | -0.08 | 0.9411 | no | 0.813 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | -0.31 | -0.41 | -1.19 | 0.0789 | no | 0.123 |
| [9038](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9038) | +0.28 | +0.28 | +1.94 | 0.2188 | no | 0.112 |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | +0.27 | -0.14 | -1.67 | 0.5365 | no | 0.286 |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | +0.26 | +0.28 | +2.45 | 0.1938 | no | 0.123 |
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | +0.26 | -0.15 | -0.72 | 0.5135 | no | 0.813 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -0.26 | -0.37 | -1.29 | 0.0929 | no | 0.123 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | +0.25 | +0.17 | +1.21 | 0.4785 | no | 0.578 |

**Layer 24** (286 vs 1424 moments; 140 features tested; 24 with q < 0.05; 7 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2896](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2896) | -0.64 | -0.54 | -42.28 | 0.0210 | yes | 0.014 |
| [3068](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3068) | +0.63 | +0.75 | +88.11 | 0.0010 | yes | 0.014 |
| [11975](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11975) | -0.63 | +0.09 | +1.69 | 0.6464 | no | 0.014 |
| [10568](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10568) | +0.63 | -0.05 | -2.15 | 0.8162 | no | 0.607 |
| [13799](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799) | -0.61 | -0.71 | -25.97 | 0.0040 | yes | 0.014 |
| [11012](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11012) | +0.59 | -0.34 | -21.71 | 0.1518 | no | 0.401 |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | -0.55 | -0.07 | -7.04 | 0.7293 | no | 0.035 |
| [869](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/869) | +0.55 | +0.45 | +37.95 | 0.0400 | yes | 0.014 |
| [8790](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8790) | +0.54 | +0.01 | +0.54 | 0.9590 | no | 0.515 |
| [15504](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15504) | -0.53 | -0.36 | -6.42 | 0.2118 | no | 0.068 |
| [10327](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10327) | +0.48 | -0.03 | -0.64 | 0.9071 | no | 0.377 |
| [7925](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7925) | +0.48 | +0.72 | +72.32 | 0.0030 | yes | 0.021 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/524) | +0.46 | -0.13 | -16.35 | 0.6074 | no | 0.372 |
| [9053](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9053) | +0.46 | +0.54 | +24.72 | 0.0080 | yes | 0.105 |
| [5341](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5341) | +0.44 | +0.55 | +42.02 | 0.0180 | yes | 0.014 |

**Layer 31** (286 vs 1424 moments; 162 features tested; 17 with q < 0.05; 5 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [139](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/139) | +2.01 | +0.00 | +0.00 | 1.0000 | no | 0.123 |
| [7338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7338) | +0.75 | +1.02 | +154.30 | 0.0010 | yes | 0.015 |
| [95](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/95) | +0.67 | +0.53 | +123.28 | 0.0240 | yes | 0.015 |
| [1128](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1128) | +0.65 | +0.79 | +175.83 | 0.0010 | yes | 0.015 |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | -0.63 | -0.84 | -171.15 | 0.0020 | yes | 0.015 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | -0.58 | -0.11 | -12.80 | 0.6074 | no | 0.038 |
| [2069](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2069) | -0.57 | -0.32 | -49.80 | 0.1558 | no | 0.025 |
| [15940](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15940) | -0.56 | -0.24 | -7.50 | 0.2997 | no | 0.126 |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | -0.55 | -0.41 | -77.68 | 0.0669 | no | 0.015 |
| [7525](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7525) | +0.52 | +0.10 | +14.09 | 0.6444 | no | 0.123 |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6014) | -0.50 | -0.18 | -26.56 | 0.3916 | no | 0.068 |
| [134](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/134) | +0.48 | +0.00 | +0.00 | 1.0000 | no | 0.412 |
| [1275](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1275) | +0.47 | +0.38 | +60.23 | 0.0949 | no | 0.015 |
| [892](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/892) | +0.47 | +0.51 | +71.48 | 0.0220 | yes | 0.015 |
| [3039](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3039) | +0.46 | +0.10 | +14.33 | 0.6354 | no | 0.963 |

**Layer 41** (286 vs 1424 moments; 171 features tested; 18 with q < 0.05; 2 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [3420](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3420) | -0.84 | +0.14 | +29.94 | 0.5325 | no | 0.032 |
| [2880](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2880) | -0.76 | -0.17 | -44.05 | 0.4046 | no | 0.021 |
| [865](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/865) | +0.65 | +0.60 | +260.77 | 0.0070 | yes | 0.021 |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | -0.56 | -0.20 | -68.98 | 0.3736 | no | 0.038 |
| [5588](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5588) | +0.51 | +0.05 | +19.52 | 0.8082 | no | 0.745 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | -0.49 | -0.38 | -317.95 | 0.0969 | no | 0.032 |
| [4972](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4972) | -0.49 | +0.25 | +76.73 | 0.2757 | no | 0.701 |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | -0.49 | -0.17 | -90.52 | 0.4625 | no | 0.032 |
| [6705](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6705) | -0.48 | -0.25 | -89.57 | 0.2767 | no | 0.021 |
| [3021](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3021) | -0.47 | -0.61 | -71.91 | 0.0599 | no | 0.031 |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | -0.47 | -0.63 | -359.63 | 0.0050 | yes | 0.021 |
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | -0.47 | +0.03 | +3.11 | 0.7512 | no | 0.551 |
| [13373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13373) | -0.46 | +0.02 | +5.04 | 0.9101 | no | 0.105 |
| [3067](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3067) | -0.46 | -0.38 | -72.23 | 0.1059 | no | 0.054 |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | +0.46 | +0.16 | +66.54 | 0.4785 | no | 0.334 |


## A: a memo (loss, gain, + you) vs the neutral memo

**Layer 12** (120 vs 30 moments; 55 features tested; 27 with q < 0.05; 9 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | +3.01 | +0.15 | +0.20 | 0.6064 | no | 0.003 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +2.28 | +2.68 | +6.73 | 0.0010 | yes | 0.003 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | -1.65 | -1.31 | -3.49 | 0.0010 | yes | 0.003 |
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | +1.55 | +0.14 | +0.21 | 0.6533 | no | 0.003 |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | +1.46 | -0.93 | -6.99 | 0.0040 | no | 0.570 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +1.44 | +0.74 | +1.74 | 0.0190 | yes | 0.003 |
| [15474](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15474) | +1.41 | -0.87 | -1.39 | 0.0080 | no | 0.146 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +1.39 | +1.95 | +13.27 | 0.0010 | yes | 0.003 |
| [3490](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490) | +1.39 | +0.86 | +9.64 | 0.0070 | yes | 0.003 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +1.33 | +1.94 | +15.05 | 0.0010 | yes | 0.003 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -1.26 | -2.15 | -20.03 | 0.0010 | yes | 0.003 |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | +1.24 | +1.22 | +6.33 | 0.0010 | yes | 0.003 |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | -1.23 | +0.40 | +4.73 | 0.1848 | no | 0.284 |
| [4156](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4156) | +1.20 | -0.23 | -2.99 | 0.4675 | no | 0.362 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.18 | +1.11 | +3.39 | 0.0020 | yes | 0.003 |

**Layer 24** (120 vs 30 moments; 136 features tested; 15 with q < 0.05; 2 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [14414](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14414) | -2.27 | +0.30 | +18.94 | 0.2168 | no | 0.039 |
| [11000](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11000) | +1.89 | -0.53 | -31.51 | 0.0879 | no | 0.310 |
| [16165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16165) | -1.68 | +0.60 | +26.28 | 0.0470 | no | 0.455 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +1.62 | -0.99 | -46.33 | 0.0010 | no | 0.617 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | -1.34 | +0.91 | +93.20 | 0.0060 | no | 0.743 |
| [15357](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15357) | +1.30 | -0.76 | -31.15 | 0.0140 | no | 0.982 |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | +1.30 | -0.78 | -45.88 | 0.0150 | no | 0.617 |
| [7741](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7741) | -1.29 | +0.69 | +71.95 | 0.0410 | no | 0.937 |
| [943](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/943) | -1.23 | +0.30 | +16.16 | 0.2158 | no | 0.580 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | +1.17 | -1.44 | -206.45 | 0.0010 | no | 0.865 |
| [13744](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13744) | -1.14 | -1.17 | -55.67 | 0.0010 | yes | 0.027 |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | +1.10 | -0.57 | -53.29 | 0.0659 | no | 0.729 |
| [5052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5052) | +1.10 | -0.66 | -25.65 | 0.0320 | no | 0.766 |
| [9558](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9558) | -1.09 | +0.32 | +28.26 | 0.2697 | no | 0.536 |
| [4392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4392) | +1.07 | +0.71 | +58.05 | 0.0280 | yes | 0.039 |

**Layer 31** (120 vs 30 moments; 153 features tested; 11 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1693](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1693) | -1.86 | +0.52 | +106.30 | 0.0939 | no | 0.343 |
| [402](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/402) | -1.44 | +0.63 | +56.49 | 0.0959 | no | 0.892 |
| [12269](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12269) | -1.35 | +0.66 | +151.08 | 0.0310 | no | 0.962 |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | -1.28 | +1.31 | +261.94 | 0.0010 | no | 0.787 |
| [3309](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3309) | +1.26 | -0.54 | -120.05 | 0.0919 | no | 0.525 |
| [324](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/324) | -1.18 | +0.71 | +97.23 | 0.0450 | no | 0.774 |
| [8799](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8799) | -1.15 | +0.97 | +245.58 | 0.0010 | no | 0.777 |
| [6152](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152) | -1.15 | +1.86 | +265.45 | 0.0010 | no | 0.355 |
| [470](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/470) | -1.13 | +1.08 | +418.07 | 0.0020 | no | 0.909 |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | -1.13 | +0.04 | +11.88 | 0.8771 | no | 0.278 |
| [1174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1174) | -1.11 | +0.41 | +56.16 | 0.1309 | no | 0.712 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | +1.10 | -0.00 | -0.18 | 0.9950 | no | 0.327 |
| [7531](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7531) | -1.06 | +0.50 | +57.51 | 0.0989 | no | 0.595 |
| [672](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/672) | -1.03 | +0.53 | +73.61 | 0.0769 | no | 0.666 |
| [2927](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2927) | -0.95 | -2.04 | -202.04 | 0.0010 | yes | 0.025 |

**Layer 41** (120 vs 30 moments; 160 features tested; 4 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [8589](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8589) | -3.17 | +0.60 | +447.20 | 0.0350 | no | 0.586 |
| [160](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/160) | -2.04 | +0.51 | +90.54 | 0.1838 | no | 0.912 |
| [2178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2178) | -1.89 | +0.47 | +82.63 | 0.1888 | no | 0.865 |
| [2080](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2080) | -1.73 | +0.66 | +214.63 | 0.0470 | no | 0.635 |
| [1663](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1663) | -1.65 | +0.44 | +39.04 | 0.2607 | no | 0.865 |
| [870](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/870) | -1.50 | +1.18 | +601.46 | 0.0010 | no | 0.865 |
| [1927](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1927) | -1.28 | +0.46 | +94.37 | 0.1039 | no | 0.425 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | -1.25 | +0.40 | +276.26 | 0.1698 | no | 0.462 |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/316) | -1.23 | +0.40 | +69.21 | 0.3117 | no | 0.950 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +1.22 | -0.85 | -812.04 | 0.0050 | no | 0.926 |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | -1.20 | -0.03 | -14.75 | 0.8971 | no | 0.141 |
| [10495](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10495) | +1.17 | -1.92 | -1138.53 | 0.0010 | no | 0.586 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | -1.15 | +0.62 | +402.62 | 0.0529 | no | 0.635 |
| [225](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/225) | -1.13 | +0.46 | +86.14 | 0.2388 | no | 0.934 |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/262) | -1.10 | -0.46 | -122.87 | 0.1518 | no | 0.053 |


## A: UBS's request vs the same moment without it

**Layer 12** (30 vs 30 moments; 62 features tested; 46 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +nan | +2.63 | +36.49 | 0.0010 | no | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | +nan | -0.97 | -7.27 | 0.0180 | no | 0.002 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | +nan | -2.88 | -23.70 | 0.0010 | no | 0.002 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | +nan | -1.88 | -13.19 | 0.0010 | no | 0.002 |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | +nan | +3.10 | +8.72 | 0.0250 | no | 0.232 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +nan | -0.14 | -1.01 | 0.6923 | no | 0.726 |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | +nan | +1.49 | +26.88 | 0.0020 | no | 0.002 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | +nan | -2.05 | -19.39 | 0.0020 | no | 0.002 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +nan | +0.68 | +4.80 | 0.0909 | no | 0.144 |
| [329](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/329) | +nan | -16.71 | -5.99 | 0.0340 | no | 0.011 |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | +nan | +3.87 | +25.16 | 0.0010 | no | 0.002 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +nan | +0.43 | +3.69 | 0.2488 | no | 0.593 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +nan | +0.47 | +3.93 | 0.2108 | no | 0.118 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +nan | -8.05 | -12.72 | 0.0010 | no | 0.002 |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | +nan | -1.50 | -6.73 | 0.0020 | no | 0.002 |

**Layer 24** (30 vs 30 moments; 154 features tested; 88 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | +nan | +2.84 | +431.45 | 0.0010 | no | 0.003 |
| [40](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/40) | +nan | -0.84 | -33.13 | 0.1658 | no | 0.217 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | +nan | +0.77 | +100.68 | 0.0519 | no | 0.825 |
| [77](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/77) | +nan | +1.61 | +194.78 | 0.0030 | no | 0.003 |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | +nan | -1.29 | -100.93 | 0.0200 | no | 0.003 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | +nan | +0.82 | +104.35 | 0.0370 | no | 0.005 |
| [213](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/213) | +nan | -3.98 | -52.57 | 0.0320 | no | 0.008 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +nan | +3.91 | +312.09 | 0.0010 | no | 0.003 |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | +nan | +1.23 | +178.93 | 0.0010 | no | 0.005 |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | +nan | +1.83 | +329.03 | 0.0010 | no | 0.039 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | +nan | +0.88 | +250.95 | 0.0280 | no | 0.577 |
| [379](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/379) | +nan | +1.56 | +105.94 | 0.0010 | no | 0.003 |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406) | +nan | -2.50 | -250.80 | 0.0010 | no | 0.003 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/524) | +nan | -2.60 | -41.22 | 0.0320 | no | 0.008 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | +nan | +2.61 | +303.04 | 0.0010 | no | 0.003 |

**Layer 31** (30 vs 30 moments; 192 features tested; 85 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [16](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/16) | +nan | -0.93 | -33.79 | 0.1499 | no | 0.112 |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/26) | +nan | -3.83 | -731.47 | 0.0010 | no | 0.005 |
| [32](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/32) | +nan | +0.46 | +72.30 | 0.2318 | no | 0.038 |
| [53](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/53) | +nan | -0.54 | -38.79 | 0.4006 | no | 0.229 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | +nan | -4.28 | -561.78 | 0.0010 | no | 0.005 |
| [95](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/95) | +nan | -0.95 | -130.71 | 0.0390 | no | 0.145 |
| [122](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/122) | +nan | -0.74 | -77.84 | 0.1608 | no | 0.164 |
| [134](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/134) | +nan | +0.44 | +22.23 | 0.4186 | no | 0.227 |
| [137](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/137) | +nan | +1.28 | +233.46 | 0.0010 | no | 0.005 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +nan | -0.44 | -176.17 | 0.2448 | no | 0.011 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +nan | +1.62 | +424.04 | 0.0010 | no | 0.005 |
| [239](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/239) | +nan | -2.06 | -352.55 | 0.0010 | no | 0.005 |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | +nan | -1.44 | -203.83 | 0.0030 | no | 0.005 |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | +nan | +1.24 | +339.12 | 0.0020 | no | 0.008 |
| [294](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/294) | +nan | +0.61 | +46.70 | 0.1848 | no | 0.050 |

**Layer 41** (30 vs 30 moments; 192 features tested; 101 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | +nan | +0.62 | +132.64 | 0.1948 | no | 0.527 |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/26) | +nan | -2.57 | -902.26 | 0.0010 | no | 0.003 |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | +nan | -7.06 | -569.90 | 0.0010 | no | 0.003 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | +nan | -2.12 | -505.34 | 0.0010 | no | 0.003 |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/262) | +nan | +1.23 | +263.48 | 0.0130 | no | 0.011 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +nan | -2.28 | -1821.78 | 0.0010 | no | 0.003 |
| [345](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/345) | +nan | +0.00 | +0.00 | 1.0000 | no | 0.112 |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | +nan | -0.98 | -524.49 | 0.0130 | no | 0.003 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | +nan | +1.72 | +768.81 | 0.0010 | no | 0.003 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | +nan | +0.28 | +138.50 | 0.4695 | no | 0.665 |
| [395](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/395) | +nan | +0.44 | +51.66 | 0.0320 | no | 0.146 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | +nan | +1.15 | +427.39 | 0.0030 | no | 0.003 |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | +nan | -3.25 | -1101.57 | 0.0010 | no | 0.003 |
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | +nan | +1.20 | +1229.26 | 0.0020 | no | 0.003 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +nan | -0.89 | -1053.52 | 0.0220 | no | 0.003 |


## Bank C: F vs B (same framings)

**Layer 12** (300 vs 300 moments; 55 features tested; 38 with q < 0.05; 15 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +3.10 | +3.04 | +18.36 | 0.0010 | yes | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +1.47 | +1.72 | +5.63 | 0.0010 | yes | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -1.33 | -1.24 | -10.82 | 0.0010 | yes | 0.002 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +1.33 | +1.43 | +20.39 | 0.0010 | yes | 0.002 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -1.21 | -0.99 | -3.74 | 0.0010 | yes | 0.002 |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | -1.20 | -0.89 | -12.81 | 0.0010 | yes | 0.002 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +1.19 | +1.32 | +3.40 | 0.0010 | yes | 0.002 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -1.00 | -0.65 | -2.08 | 0.0010 | yes | 0.002 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.92 | -0.70 | -7.90 | 0.0010 | yes | 0.002 |
| [4382](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382) | -0.82 | -1.34 | -4.35 | 0.0010 | yes | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.78 | +0.90 | +4.51 | 0.0010 | yes | 0.002 |
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | -0.70 | -0.82 | -3.73 | 0.0010 | yes | 0.002 |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | -0.69 | -0.55 | -8.13 | 0.0010 | yes | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.68 | +1.03 | +17.14 | 0.0010 | yes | 0.002 |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1000) | -0.63 | -0.70 | -4.72 | 0.0010 | yes | 0.002 |

**Layer 24** (300 vs 300 moments; 143 features tested; 72 with q < 0.05; 13 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +0.98 | +0.86 | +42.94 | 0.0010 | yes | 0.003 |
| [2098](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2098) | +0.82 | +0.51 | +12.82 | 0.0010 | yes | 0.003 |
| [16165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16165) | -0.77 | -0.61 | -28.91 | 0.0010 | yes | 0.003 |
| [9712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712) | +0.73 | +0.87 | +26.91 | 0.0010 | yes | 0.003 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | +0.71 | +0.30 | +7.83 | 0.0150 | yes | 0.003 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | -0.69 | -0.55 | -83.95 | 0.0010 | yes | 0.003 |
| [14360](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14360) | -0.64 | -0.24 | -23.31 | 0.0400 | yes | 0.003 |
| [15074](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074) | +0.64 | +0.63 | +67.72 | 0.0010 | yes | 0.003 |
| [8992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8992) | -0.59 | -0.28 | -23.07 | 0.0200 | yes | 0.003 |
| [8326](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326) | -0.58 | -0.11 | -12.92 | 0.3566 | no | 0.003 |
| [831](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/831) | -0.57 | -0.35 | -41.84 | 0.0070 | yes | 0.003 |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | +0.55 | +0.56 | +73.77 | 0.0010 | yes | 0.003 |
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | -0.54 | -0.26 | -42.40 | 0.0240 | yes | 0.003 |
| [943](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/943) | -0.52 | -0.08 | -5.83 | 0.5125 | no | 0.003 |
| [11975](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11975) | -0.50 | -0.37 | -16.89 | 0.0020 | yes | 0.003 |

**Layer 31** (300 vs 300 moments; 167 features tested; 68 with q < 0.05; 15 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2790](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2790) | +1.09 | +0.85 | +160.74 | 0.0010 | yes | 0.004 |
| [3976](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3976) | +0.84 | +0.76 | +105.35 | 0.0010 | yes | 0.004 |
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | +0.84 | +0.40 | +94.88 | 0.0020 | yes | 0.004 |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | +0.83 | +0.42 | +66.64 | 0.0010 | yes | 0.004 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.81 | +0.49 | +135.93 | 0.0020 | yes | 0.004 |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | -0.80 | -0.25 | -48.67 | 0.0370 | yes | 0.004 |
| [1293](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1293) | +0.79 | +0.64 | +168.87 | 0.0010 | yes | 0.004 |
| [3723](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3723) | +0.79 | +0.57 | +74.76 | 0.0010 | yes | 0.004 |
| [1316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1316) | +0.77 | +0.72 | +93.81 | 0.0010 | yes | 0.004 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +0.75 | +0.52 | +386.44 | 0.0010 | yes | 0.004 |
| [16063](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/16063) | +0.75 | +0.56 | +90.27 | 0.0010 | yes | 0.004 |
| [2809](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2809) | +0.73 | +0.43 | +100.53 | 0.0010 | yes | 0.004 |
| [7201](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7201) | +0.73 | +0.48 | +67.01 | 0.0010 | yes | 0.004 |
| [11327](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11327) | +0.69 | +0.42 | +59.78 | 0.0020 | yes | 0.004 |
| [3331](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3331) | +0.68 | +0.44 | +74.92 | 0.0010 | yes | 0.004 |

**Layer 41** (300 vs 300 moments; 171 features tested; 85 with q < 0.05; 15 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [6938](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6938) | +1.67 | +1.38 | +525.19 | 0.0010 | yes | 0.003 |
| [3981](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3981) | +1.30 | +1.17 | +401.20 | 0.0010 | yes | 0.003 |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | +1.24 | +0.67 | +311.62 | 0.0010 | yes | 0.003 |
| [8520](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8520) | +1.14 | +1.09 | +720.08 | 0.0010 | yes | 0.003 |
| [5976](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5976) | +1.04 | +0.50 | +250.82 | 0.0010 | yes | 0.003 |
| [1405](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1405) | +0.97 | +0.92 | +244.37 | 0.0010 | yes | 0.003 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.96 | +0.63 | +719.80 | 0.0010 | yes | 0.003 |
| [5736](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5736) | +0.88 | +0.62 | +157.30 | 0.0010 | yes | 0.003 |
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | +0.87 | +0.98 | +289.77 | 0.0010 | yes | 0.003 |
| [5120](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5120) | +0.87 | +0.86 | +266.90 | 0.0010 | yes | 0.003 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | -0.82 | -0.49 | -340.62 | 0.0010 | yes | 0.003 |
| [865](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/865) | +0.80 | +0.46 | +174.38 | 0.0010 | yes | 0.003 |
| [8441](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8441) | +0.78 | +0.39 | +111.89 | 0.0010 | yes | 0.003 |
| [2697](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2697) | +0.76 | +0.64 | +250.95 | 0.0010 | yes | 0.003 |
| [1331](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1331) | +0.76 | +0.74 | +230.61 | 0.0010 | yes | 0.003 |


## Checks: how well Gemma Scope rebuilds our states, and 4-bit against bfloat16

Share of variance rebuilt: 1 minus the dictionary's squared error over the states' variance (Gemma Scope's own reports are typically 0.6-0.9 on ordinary text; much lower here would mean its features read our states poorly). 4-bit: B's moments read again with the careers' own 4-bit weights; the loss vs gain feature differences compared between the two precisions.

| Layer | Variance rebuilt (all moments) | B, bfloat16 | B, 4-bit | State similarity, 4-bit vs bfloat16 (median cosine; lowest) | Loss vs gain differences: correlation | Top 15 shared | Top 15, same sign |
|---|---|---|---|---|---|---|---|
| 12 | -1.126 | - | - | - | - | - | - |
| 24 | 0.126 | - | - | - | - | - | - |
| 31 | 0.453 | - | - | - | - | - | - |
| 41 | 0.058 | - | - | - | - | - | - |

B has not been read in 4-bit yet (`modal run --detach scripts/modal_inside.py --exps B --precision 4bit`).

## Can "went along" be read from the state, beyond the request and the framing?

1710 moments with a request, 286 went along. Read-out scored on careers it was not trained on (5 folds by career), and on a request it never saw (careers share chat lines, e.g. C clean = B neutral, so the held-out request shows it is not learning the conversation). **The labels alone (request, experiment, version, and the position on UBS's side at the request) score AUC 0.897.** States are centred within each request and reduced to 64 components per layer (fitted on all careers' states, no outcome used). "Gain" is state + labels minus labels alone, with a 95% interval from resampling careers (an interval above 0 means the state adds something). The held-out request is also scored by a read-out trained only on requests where UBS wants the same direction (going along is buying in some requests and selling in others). A held-out request is scored within itself (its own going-along against its own not), since each held-out request gets its own read-out.

| Layer | AUC: state | AUC: state + labels | Gain over labels (95% interval) | AUC: a held-out request | AUC: a held-out request, same direction | AUC: state, outcomes reshuffled within request |
|---|---|---|---|---|---|---|
| 0 | 0.679 | 0.899 | +0.002 (-0.009 to +0.012) | 0.623 | 0.515 | 0.486 |
| 3 | 0.699 | 0.898 | +0.000 (-0.009 to +0.009) | 0.657 | 0.467 | 0.455 |
| 6 | 0.700 | 0.898 | +0.001 (-0.008 to +0.011) | 0.596 | 0.600 | 0.499 |
| 9 | 0.701 | 0.893 | -0.004 (-0.014 to +0.006) | 0.626 | 0.495 | 0.511 |
| 12 | 0.701 | 0.902 | +0.004 (-0.006 to +0.014) | 0.646 | 0.575 | 0.438 |
| 15 | 0.703 | 0.899 | +0.002 (-0.008 to +0.012) | 0.669 | 0.584 | 0.448 |
| 18 | 0.709 | 0.902 | +0.005 (-0.006 to +0.015) | 0.710 | 0.577 | 0.480 |
| 21 | 0.738 | 0.917 | +0.020 (+0.010 to +0.031) | 0.692 | 0.535 | 0.522 |
| 24 | 0.748 | 0.919 | +0.022 (+0.010 to +0.033) | 0.749 | 0.624 | 0.535 |
| 27 | 0.741 | 0.915 | +0.017 (+0.004 to +0.029) | 0.761 | 0.668 | 0.473 |
| 30 | 0.736 | 0.918 | +0.020 (+0.007 to +0.032) | 0.749 | 0.677 | 0.458 |
| 33 | 0.734 | 0.916 | +0.019 (+0.006 to +0.030) | 0.754 | 0.691 | 0.489 |
| 36 | 0.734 | 0.915 | +0.018 (+0.005 to +0.029) | 0.740 | 0.682 | 0.524 |
| 39 | 0.723 | 0.914 | +0.017 (+0.004 to +0.029) | 0.722 | 0.666 | 0.442 |
| 42 | 0.713 | 0.916 | +0.019 (+0.006 to +0.029) | 0.693 | 0.704 | 0.467 |
| 45 | 0.730 | 0.918 | +0.021 (+0.008 to +0.032) | 0.722 | 0.696 | 0.455 |

## Bank C at 7 Jan, paired with each career's B twin

50 pairs (twins share a seed, but on the saved transcripts every pair differs from the first reply, so this is not Bank C's line alone). The size of the state change, by layer, against the change between two B careers of the same version at the same moment:

| Layer | Bank C: mean change (F minus its twin) | Two B careers of the same version |
|---|---|---|
| 0 | 30.5 | 29.2 |
| 6 | 42.2 | 35.5 |
| 12 | 331.3 | 185.0 |
| 18 | 816.6 | 682.6 |
| 24 | 2031.3 | 2059.5 |
| 30 | 4382.9 | 4628.3 |
| 36 | 7792.3 | 7759.1 |
| 42 | 10583.6 | 11024.3 |

Where the first column is no larger than the second, F's state is no further from its twin than two B careers are from each other.
