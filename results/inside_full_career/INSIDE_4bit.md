# Inside the model at the push requests (full careers)

States: Gemma 3 12B at 4bit, the last token before each push-request reply, 300 moments (B: 300). Every comparison is within the same request (went along vs not: within the same request, experiment and framing); p-values reshuffle labels within those groups (1000 times); q = false-discovery-corrected. Features active in fewer than 5% of the moments compared are left out. Produced by `designs/rd2/analysis/inside_features.py`.

Gemma Scope 2 (google/gemma-scope-2-12b-it, residual stream, 16k): layers [12, 24, 31, 41]; files `resid_post/layer_12_width_16k_l0_medium/params.safetensors`, `resid_post/layer_24_width_16k_l0_medium/params.safetensors`, `resid_post/layer_31_width_16k_l0_medium/params.safetensors`, `resid_post/layer_41_width_16k_l0_medium/params.safetensors`. Each table lists the 15 features that differ most on half the careers, then the same features on the other half (confirmed: the same sign, p < 0.05 there); the count of features with q < 0.05 is over all careers.


## B: UBS's loss frame vs gain frame

**Layer 12** (120 vs 120 moments; 52 features tested; 19 with q < 0.05; 9 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.95 | +0.64 | +2.20 | 0.0050 | yes | 0.004 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | -0.94 | +0.15 | +0.42 | 0.4845 | no | 0.013 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -0.85 | -0.30 | -4.30 | 0.1459 | no | 0.004 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.84 | +0.85 | +4.15 | 0.0010 | yes | 0.004 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.81 | -0.69 | -15.47 | 0.0030 | yes | 0.004 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.69 | +0.84 | +2.09 | 0.0010 | yes | 0.004 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.68 | +0.30 | +0.74 | 0.1359 | no | 0.004 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.68 | +0.34 | +0.84 | 0.0979 | no | 0.004 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.58 | +0.44 | +5.52 | 0.0350 | yes | 0.004 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -0.57 | -0.91 | -16.14 | 0.0010 | yes | 0.004 |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | +0.52 | +0.29 | +2.84 | 0.1708 | no | 0.004 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +0.51 | +0.42 | +3.71 | 0.0500 | yes | 0.004 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +0.49 | +0.09 | +1.10 | 0.6613 | no | 0.049 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -0.45 | -0.47 | -1.53 | 0.0240 | yes | 0.007 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +0.45 | +0.45 | +4.27 | 0.0250 | yes | 0.004 |

**Layer 24** (120 vs 120 moments; 136 features tested; 52 with q < 0.05; 7 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +1.01 | +0.41 | +24.67 | 0.0639 | no | 0.004 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | -1.01 | -0.74 | -100.81 | 0.0020 | yes | 0.004 |
| [8992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8992) | -0.89 | -0.15 | -11.48 | 0.4645 | no | 0.004 |
| [7741](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7741) | +0.86 | +0.66 | +80.45 | 0.0050 | yes | 0.004 |
| [15592](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592) | -0.84 | -0.17 | -4.46 | 0.4196 | no | 0.004 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | -0.84 | -0.61 | -60.92 | 0.0070 | yes | 0.004 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | -0.83 | +0.08 | +39.15 | 0.7043 | no | 0.014 |
| [7789](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7789) | +0.82 | +0.12 | +17.77 | 0.5814 | no | 0.004 |
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | +0.82 | +0.12 | +17.03 | 0.5564 | no | 0.004 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | -0.81 | -0.48 | -31.44 | 0.0320 | yes | 0.004 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | +0.81 | +0.12 | +8.87 | 0.5734 | no | 0.004 |
| [6309](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6309) | +0.81 | -0.00 | -0.01 | 1.0000 | no | 0.014 |
| [14071](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14071) | -0.80 | -0.58 | -31.09 | 0.0200 | yes | 0.004 |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | -0.80 | -0.91 | -99.37 | 0.0020 | yes | 0.004 |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.79 | -0.79 | -20.15 | 0.0010 | yes | 0.004 |

**Layer 31** (120 vs 120 moments; 163 features tested; 37 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | +1.17 | -0.18 | -88.42 | 0.3786 | no | 0.008 |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | +1.09 | +0.18 | +70.65 | 0.3896 | no | 0.008 |
| [929](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/929) | +1.01 | +0.15 | +30.13 | 0.4935 | no | 0.008 |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | +1.00 | +0.01 | +4.90 | 0.9720 | no | 0.008 |
| [4805](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4805) | -0.97 | -0.02 | -9.69 | 0.9321 | no | 0.008 |
| [2900](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2900) | -0.81 | -0.01 | -2.80 | 0.9660 | no | 0.014 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/404) | +0.80 | -0.18 | -64.24 | 0.3576 | no | 0.076 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +0.77 | +0.28 | +42.90 | 0.2078 | no | 0.008 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | +0.71 | +0.14 | +69.93 | 0.5105 | no | 0.018 |
| [8224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8224) | -0.70 | -0.30 | -50.25 | 0.1209 | no | 0.008 |
| [4747](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4747) | +0.70 | -0.27 | -34.73 | 0.1618 | no | 0.195 |
| [4214](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4214) | -0.69 | -0.12 | -48.97 | 0.5654 | no | 0.008 |
| [10806](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10806) | -0.69 | +0.45 | +85.72 | 0.0490 | no | 0.129 |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | -0.69 | -0.26 | -51.71 | 0.1958 | no | 0.014 |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | -0.68 | +0.08 | +36.77 | 0.6973 | no | 0.076 |

**Layer 41** (120 vs 120 moments; 158 features tested; 48 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +1.16 | +0.00 | +2.91 | 0.9950 | no | 0.013 |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | +1.08 | +0.10 | +51.34 | 0.5994 | no | 0.013 |
| [755](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/755) | -1.01 | -0.16 | -165.25 | 0.4525 | no | 0.013 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | +0.97 | -0.01 | -9.41 | 0.9570 | no | 0.013 |
| [137](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/137) | +0.86 | -0.08 | -11.41 | 0.7263 | no | 0.013 |
| [3637](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3637) | +0.86 | +0.01 | +3.07 | 0.9790 | no | 0.020 |
| [897](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/897) | -0.85 | +0.17 | +66.88 | 0.3936 | no | 0.026 |
| [946](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/946) | -0.85 | +0.12 | +76.47 | 0.5814 | no | 0.020 |
| [12726](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12726) | +0.85 | +0.45 | +135.65 | 0.0260 | yes | 0.013 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | +0.81 | -0.24 | -187.32 | 0.2398 | no | 0.095 |
| [345](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/345) | +0.80 | +0.11 | +41.83 | 0.5654 | no | 0.016 |
| [2559](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2559) | +0.80 | +0.35 | +210.43 | 0.0809 | no | 0.013 |
| [9797](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9797) | -0.78 | +0.24 | +63.51 | 0.2577 | no | 0.045 |
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | +0.77 | -0.05 | -69.43 | 0.8262 | no | 0.032 |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | +0.76 | +0.11 | +58.88 | 0.6024 | no | 0.016 |


## B: "+ you" vs no owner

**Layer 12** (120 vs 120 moments; 52 features tested; 16 with q < 0.05; 4 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.24 | +0.36 | +0.96 | 0.0879 | no | 0.006 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.94 | -0.04 | -0.21 | 0.8641 | no | 0.006 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.71 | -0.53 | -11.95 | 0.0090 | yes | 0.006 |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | +0.68 | -0.05 | -0.12 | 0.8042 | no | 0.049 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | -0.68 | -0.63 | -4.90 | 0.0030 | yes | 0.006 |
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | -0.61 | -0.28 | -1.53 | 0.2178 | no | 0.026 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.57 | -0.34 | -3.10 | 0.0929 | no | 0.006 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -0.57 | +0.00 | +0.00 | 0.9980 | no | 0.090 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +0.57 | +0.12 | +0.29 | 0.5804 | no | 0.031 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.56 | +0.91 | +6.75 | 0.0010 | yes | 0.006 |
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | +0.56 | -0.16 | -3.19 | 0.4815 | no | 0.228 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -0.51 | +0.59 | +1.77 | 0.0100 | no | 0.984 |
| [3264](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3264) | -0.47 | -0.31 | -2.78 | 0.1359 | no | 0.030 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.43 | -0.62 | -2.33 | 0.0090 | yes | 0.006 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +0.43 | -0.04 | -0.40 | 0.8152 | no | 0.221 |

**Layer 24** (120 vs 120 moments; 136 features tested; 35 with q < 0.05; 6 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [3068](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3068) | -0.71 | -0.60 | -47.20 | 0.0030 | yes | 0.010 |
| [11000](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11000) | -0.70 | -0.73 | -38.28 | 0.0010 | yes | 0.010 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.68 | +1.16 | +61.80 | 0.0010 | yes | 0.010 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.66 | +0.92 | +30.02 | 0.0010 | yes | 0.010 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | +0.61 | -0.08 | -1.98 | 0.6773 | no | 0.180 |
| [8108](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8108) | -0.60 | -0.19 | -3.49 | 0.3407 | no | 0.059 |
| [5247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5247) | -0.57 | -0.20 | -3.32 | 0.3367 | no | 0.051 |
| [12646](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12646) | +0.57 | -0.04 | -1.77 | 0.8711 | no | 0.086 |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | +0.57 | +0.25 | +9.56 | 0.2098 | no | 0.033 |
| [15043](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15043) | +0.56 | +0.49 | +59.80 | 0.0180 | yes | 0.010 |
| [13585](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13585) | +0.54 | +0.09 | +2.62 | 0.6503 | no | 0.078 |
| [15737](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15737) | -0.49 | -0.34 | -13.02 | 0.0969 | no | 0.023 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | -0.49 | -0.42 | -26.11 | 0.0400 | yes | 0.010 |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | -0.47 | +0.05 | +1.35 | 0.8292 | no | 0.112 |
| [2896](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2896) | +0.46 | +0.08 | +7.73 | 0.7033 | no | 0.105 |

**Layer 31** (120 vs 120 moments; 163 features tested; 53 with q < 0.05; 7 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [15017](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15017) | -0.68 | -0.29 | -31.25 | 0.1928 | no | 0.008 |
| [3331](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3331) | +0.65 | +0.19 | +21.54 | 0.3037 | no | 0.015 |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | +0.64 | +0.37 | +38.02 | 0.0879 | no | 0.011 |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | +0.62 | +0.58 | +179.28 | 0.0100 | yes | 0.008 |
| [1519](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1519) | +0.61 | +0.18 | +34.93 | 0.3676 | no | 0.008 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | +0.51 | +0.62 | +312.43 | 0.0050 | yes | 0.008 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +0.50 | +0.96 | +135.72 | 0.0010 | yes | 0.008 |
| [2882](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2882) | -0.49 | -0.91 | -105.94 | 0.0010 | yes | 0.008 |
| [6889](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6889) | -0.48 | -0.08 | -12.83 | 0.6843 | no | 0.099 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | +0.47 | -0.12 | -32.90 | 0.5614 | no | 0.374 |
| [13577](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13577) | -0.46 | -0.69 | -172.10 | 0.0030 | yes | 0.008 |
| [3597](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3597) | -0.46 | -0.39 | -62.59 | 0.0659 | no | 0.011 |
| [2079](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2079) | -0.46 | -0.23 | -28.45 | 0.2527 | no | 0.018 |
| [32](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/32) | +0.44 | +0.54 | +87.51 | 0.0100 | yes | 0.008 |
| [3315](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3315) | -0.43 | -0.67 | -116.91 | 0.0020 | yes | 0.008 |

**Layer 41** (120 vs 120 moments; 158 features tested; 41 with q < 0.05; 2 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | +0.67 | -0.23 | -69.69 | 0.2737 | no | 0.158 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.62 | +0.10 | +40.56 | 0.6424 | no | 0.027 |
| [2080](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2080) | -0.60 | +0.23 | +94.34 | 0.2537 | no | 0.241 |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/262) | +0.55 | -0.09 | -39.32 | 0.6434 | no | 0.126 |
| [10433](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10433) | -0.55 | -0.42 | -154.05 | 0.0639 | no | 0.010 |
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | +0.54 | +0.87 | +1178.65 | 0.0010 | yes | 0.010 |
| [1663](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1663) | -0.49 | +0.59 | +102.55 | 0.0090 | no | 0.596 |
| [9624](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9624) | -0.46 | -0.61 | -171.71 | 0.0060 | yes | 0.010 |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | +0.44 | -0.26 | -142.65 | 0.2208 | no | 0.566 |
| [1635](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1635) | +0.43 | +0.00 | +1.77 | 0.9840 | no | 0.106 |
| [345](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/345) | +0.42 | +0.37 | +131.28 | 0.0929 | no | 0.033 |
| [3067](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3067) | -0.41 | +0.09 | +11.37 | 0.6693 | no | 0.444 |
| [13373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13373) | +0.39 | +0.35 | +99.20 | 0.0859 | no | 0.040 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | -0.38 | -0.17 | -102.28 | 0.4316 | no | 0.083 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | -0.38 | -0.30 | -46.41 | 0.1489 | no | 0.074 |


## B: framed vs neutral

**Layer 12** (240 vs 60 moments; 53 features tested; 31 with q < 0.05; 14 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | +3.20 | +1.57 | +13.75 | 0.0010 | yes | 0.002 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | +3.16 | +1.79 | +6.17 | 0.0010 | yes | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.95 | +2.56 | +7.33 | 0.0010 | yes | 0.002 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -1.85 | -2.03 | -32.06 | 0.0010 | yes | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +1.53 | +1.35 | +11.19 | 0.0010 | yes | 0.002 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -1.46 | -1.47 | -31.42 | 0.0010 | yes | 0.002 |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | -1.38 | -0.56 | -7.36 | 0.0030 | yes | 0.002 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +1.37 | +1.50 | +19.29 | 0.0010 | yes | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +1.32 | +2.01 | +6.85 | 0.0010 | yes | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +1.27 | +1.70 | +24.47 | 0.0010 | yes | 0.002 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +1.21 | +1.59 | +17.35 | 0.0010 | yes | 0.002 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | -1.16 | -1.49 | -17.72 | 0.0010 | yes | 0.002 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +1.10 | -0.62 | -3.13 | 0.0010 | no | 0.858 |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +1.00 | +1.32 | +10.71 | 0.0010 | yes | 0.002 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +0.98 | +1.50 | +16.53 | 0.0010 | yes | 0.002 |

**Layer 24** (240 vs 60 moments; 135 features tested; 26 with q < 0.05; 5 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +1.23 | -0.40 | -48.08 | 0.0370 | no | 0.482 |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | +1.11 | +0.28 | +41.85 | 0.1339 | no | 0.010 |
| [1672](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1672) | +1.04 | -0.19 | -17.28 | 0.3207 | no | 0.288 |
| [9712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712) | -0.97 | -0.73 | -25.96 | 0.0010 | yes | 0.010 |
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | -0.95 | -0.52 | -18.88 | 0.0060 | yes | 0.010 |
| [15357](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15357) | -0.90 | -0.24 | -8.21 | 0.2078 | no | 0.026 |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | +0.78 | -0.12 | -20.10 | 0.5405 | no | 0.547 |
| [13585](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13585) | +0.77 | +0.23 | +6.92 | 0.2378 | no | 0.065 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | -0.68 | -0.80 | -18.87 | 0.0010 | yes | 0.010 |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | +0.65 | +0.34 | +49.01 | 0.0789 | no | 0.113 |
| [15074](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074) | +0.64 | +0.54 | +64.07 | 0.0050 | yes | 0.010 |
| [7283](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7283) | +0.63 | -0.39 | -31.24 | 0.0370 | no | 0.718 |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | -0.58 | +0.28 | +20.56 | 0.1499 | no | 0.943 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.58 | +1.00 | +56.45 | 0.0010 | yes | 0.010 |
| [16304](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16304) | +0.57 | +0.28 | +26.92 | 0.1129 | no | 0.042 |

**Layer 31** (240 vs 60 moments; 162 features tested; 37 with q < 0.05; 5 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | -1.11 | -0.72 | -134.92 | 0.0010 | yes | 0.015 |
| [1744](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1744) | -0.88 | -0.18 | -39.52 | 0.3467 | no | 0.038 |
| [10806](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10806) | -0.74 | +0.26 | +42.86 | 0.1479 | no | 0.660 |
| [3369](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3369) | -0.71 | -0.28 | -51.98 | 0.1528 | no | 0.031 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | +0.70 | +0.14 | +53.45 | 0.4645 | no | 0.054 |
| [8305](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8305) | -0.70 | +0.12 | +5.38 | 0.3177 | no | 0.448 |
| [12281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12281) | -0.69 | +0.17 | +20.98 | 0.5874 | no | 0.635 |
| [5652](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652) | -0.68 | -0.62 | -52.73 | 0.0010 | yes | 0.015 |
| [6294](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6294) | +0.68 | +0.58 | +131.24 | 0.0030 | yes | 0.015 |
| [2411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2411) | -0.67 | -0.32 | -34.15 | 0.1209 | no | 0.044 |
| [10755](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10755) | -0.64 | +0.08 | +7.91 | 0.7073 | no | 0.630 |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | -0.64 | -0.56 | -138.62 | 0.0050 | yes | 0.015 |
| [132](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/132) | -0.62 | +0.43 | +56.13 | 0.0310 | no | 0.719 |
| [3728](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3728) | +0.61 | -0.26 | -43.91 | 0.1918 | no | 0.859 |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | +0.60 | +0.41 | +99.35 | 0.0260 | yes | 0.041 |

**Layer 41** (240 vs 60 moments; 156 features tested; 10 with q < 0.05; 3 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1059](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1059) | -0.90 | +0.19 | +24.26 | 0.3077 | no | 0.427 |
| [1234](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1234) | -0.81 | -0.44 | -131.55 | 0.0270 | yes | 0.026 |
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | -0.72 | -0.81 | -119.33 | 0.0010 | yes | 0.026 |
| [6928](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6928) | +0.72 | +0.39 | +139.56 | 0.0320 | yes | 0.026 |
| [5982](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5982) | -0.70 | +0.23 | +52.42 | 0.1419 | no | 0.617 |
| [1861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1861) | -0.68 | +0.26 | +76.39 | 0.1818 | no | 0.833 |
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | -0.68 | -0.34 | -73.05 | 0.0759 | no | 0.086 |
| [942](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/942) | +0.68 | +0.21 | +86.86 | 0.2917 | no | 0.130 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | -0.68 | -0.14 | -46.16 | 0.4366 | no | 0.115 |
| [7953](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7953) | -0.67 | +0.20 | +34.17 | 0.3047 | no | 0.639 |
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | -0.67 | -0.12 | -53.28 | 0.5694 | no | 0.177 |
| [3798](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3798) | +0.67 | +0.34 | +125.51 | 0.0909 | no | 0.075 |
| [1048](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1048) | +0.66 | +0.07 | +13.90 | 0.6474 | no | 0.145 |
| [1559](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1559) | -0.66 | +0.18 | +63.55 | 0.3407 | no | 0.601 |
| [8441](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8441) | -0.65 | -0.04 | -9.11 | 0.6454 | no | 0.294 |


## All experiments: went along vs did not (same request, experiment and framing)

**Layer 12** (55 vs 245 moments; 53 features tested; 0 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | +1.60 | -0.15 | -0.50 | 0.8232 | no | 0.688 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | -1.56 | +0.21 | +0.57 | 0.7632 | no | 0.750 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | +1.28 | -1.00 | -6.04 | 0.1748 | no | 0.940 |
| [1272](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272) | -1.27 | -0.54 | -1.70 | 0.3776 | no | 0.688 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | +1.02 | +0.20 | +4.41 | 0.9011 | no | 0.688 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | -0.96 | +0.02 | +0.05 | 0.9770 | no | 1.000 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | +0.95 | -0.70 | -1.52 | 0.3257 | no | 1.000 |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | +0.87 | +0.09 | +1.69 | 0.9540 | no | 0.940 |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | -0.87 | +0.42 | +4.41 | 0.6593 | no | 0.874 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | -0.83 | -0.12 | -1.22 | 0.8751 | no | 0.750 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +0.79 | -0.12 | -0.84 | 0.8581 | no | 0.688 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.76 | -0.70 | -3.61 | 0.3177 | no | 1.000 |
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | -0.76 | -1.08 | -4.04 | 0.3137 | no | 0.688 |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | -0.71 | +0.28 | +1.69 | 0.6753 | no | 1.000 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.65 | -0.13 | -0.44 | 0.8222 | no | 1.000 |

**Layer 24** (55 vs 245 moments; 135 features tested; 3 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [11587](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11587) | -53.93 | +0.00 | +0.00 | 1.0000 | no | 0.323 |
| [12646](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12646) | +2.37 | +0.29 | +12.33 | 0.6913 | no | 0.045 |
| [9053](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9053) | +1.76 | +0.42 | +46.98 | 0.4535 | no | 0.054 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | -1.64 | +0.17 | +6.00 | 0.7822 | no | 0.367 |
| [6382](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6382) | +1.51 | +1.92 | +59.29 | 0.0080 | yes | 0.045 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +1.43 | +0.45 | +20.86 | 0.5125 | no | 0.297 |
| [6460](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6460) | +1.39 | -0.00 | -0.31 | 1.0000 | no | 0.238 |
| [9558](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9558) | +1.38 | -0.19 | -1.37 | 0.9051 | no | 0.124 |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | +1.35 | -1.40 | -139.24 | 0.0390 | no | 0.370 |
| [14392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14392) | +1.18 | +1.10 | +45.58 | 0.1009 | no | 0.124 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | -1.15 | -0.74 | -42.25 | 0.2797 | no | 0.239 |
| [12075](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12075) | -1.13 | +0.29 | +5.28 | 0.5934 | no | 0.435 |
| [8992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8992) | +1.12 | +0.69 | +46.18 | 0.3247 | no | 0.297 |
| [8326](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326) | -1.12 | -1.02 | -97.94 | 0.1518 | no | 0.045 |
| [5052](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5052) | +1.12 | +0.43 | +17.33 | 0.5794 | no | 0.323 |

**Layer 31** (55 vs 245 moments; 162 features tested; 4 with q < 0.05; 1 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | +1.95 | +1.21 | +246.25 | 0.1299 | no | 0.041 |
| [239](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/239) | +1.61 | +0.50 | +20.18 | 0.5604 | no | 0.282 |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | +1.40 | -0.74 | -145.40 | 0.2527 | no | 0.930 |
| [1880](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1880) | +1.40 | +0.08 | +9.69 | 0.8831 | no | 0.637 |
| [1238](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1238) | +1.36 | -0.83 | -160.86 | 0.2907 | no | 0.896 |
| [3180](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3180) | +1.36 | +0.67 | +139.80 | 0.3696 | no | 0.041 |
| [12382](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12382) | +1.22 | +0.27 | +33.34 | 0.8012 | no | 0.575 |
| [7525](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7525) | +1.19 | -0.54 | -67.62 | 0.7932 | no | 0.738 |
| [470](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/470) | -1.16 | -1.25 | -332.01 | 0.0879 | no | 0.148 |
| [4214](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4214) | +1.13 | +0.85 | +247.13 | 0.1958 | no | 0.230 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +1.04 | +1.55 | +716.24 | 0.0440 | yes | 0.065 |
| [357](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/357) | -1.03 | -1.02 | -163.45 | 0.1788 | no | 0.314 |
| [10755](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10755) | -1.02 | +0.00 | +0.00 | 1.0000 | no | 0.662 |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | -1.00 | +1.41 | +278.73 | 0.0839 | no | 0.607 |
| [10374](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10374) | -0.98 | +0.66 | +62.13 | 1.0000 | no | 1.000 |

**Layer 41** (55 vs 245 moments; 156 features tested; 0 with q < 0.05; 0 of the top 15 confirmed on the other half)

| Feature | Found (half 1, spread units) | Other half (spread units) | Activation difference (other half) | p (other half) | Confirmed | q (all careers) |
|---|---|---|---|---|---|---|
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | -1.75 | -0.66 | -127.06 | 1.0000 | no | 0.104 |
| [7004](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7004) | +1.64 | +0.65 | +165.49 | 0.2827 | no | 0.303 |
| [1742](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1742) | -1.29 | -0.34 | -49.13 | 0.6703 | no | 0.241 |
| [1761](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1761) | +1.26 | -0.02 | -4.70 | 1.0000 | no | 0.628 |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | -1.24 | -0.86 | -504.87 | 0.2158 | no | 0.249 |
| [1939](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1939) | -1.19 | +1.28 | +202.64 | 0.4076 | no | 0.665 |
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | -1.18 | +0.00 | +0.00 | 1.0000 | no | 0.510 |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | +1.14 | -1.36 | -306.48 | 0.1089 | no | 1.000 |
| [13569](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13569) | +1.12 | -0.66 | -219.37 | 1.0000 | no | 0.629 |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | +1.12 | -0.66 | -156.45 | 1.0000 | no | 0.976 |
| [911](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/911) | +1.10 | -4.72 | -626.56 | 0.1089 | no | 0.253 |
| [1059](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1059) | -1.10 | +0.00 | +0.00 | 1.0000 | no | 0.399 |
| [7328](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7328) | -1.09 | +0.00 | +0.00 | 1.0000 | no | 0.579 |
| [787](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/787) | +1.07 | +0.38 | +34.20 | 1.0000 | no | 0.628 |
| [3420](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3420) | -1.06 | -1.25 | -450.44 | 0.1079 | no | 0.104 |


## Checks: how well Gemma Scope rebuilds our states, and 4-bit against bfloat16

Share of variance rebuilt: 1 minus the dictionary's squared error over the states' variance (Gemma Scope's own reports are typically 0.6-0.9 on ordinary text; much lower here would mean its features read our states poorly). 4-bit: B's moments read again with the careers' own 4-bit weights; the loss vs gain feature differences compared between the two precisions.

| Layer | Variance rebuilt (all moments) | B, bfloat16 | B, 4-bit | State similarity, 4-bit vs bfloat16 (median cosine; lowest) | Loss vs gain differences: correlation | Top 15 shared | Top 15, same sign |
|---|---|---|---|---|---|---|---|
| 12 | -1.208 | - | - | - | - | - | - |
| 24 | -0.189 | - | - | - | - | - | - |
| 31 | 0.380 | - | - | - | - | - | - |
| 41 | -0.042 | - | - | - | - | - | - |

B has not been read in 4-bit yet (`modal run --detach scripts/modal_inside.py --exps B --precision 4bit`).

## Can "went along" be read from the state, beyond the request and the framing?

300 moments with a request, 55 went along. Read-out scored on careers it was not trained on (5 folds by career), and on a request it never saw (careers share chat lines, e.g. C clean = B neutral, so the held-out request shows it is not learning the conversation). **The labels alone (request, experiment, version, and the position on UBS's side at the request) score AUC 0.905.** States are centred within each request and reduced to 64 components per layer (fitted on all careers' states, no outcome used). "Gain" is state + labels minus labels alone, with a 95% interval from resampling careers (an interval above 0 means the state adds something). The held-out request is also scored by a read-out trained only on requests where UBS wants the same direction (going along is buying in some requests and selling in others). A held-out request is scored within itself (its own going-along against its own not), since each held-out request gets its own read-out.

| Layer | AUC: state | AUC: state + labels | Gain over labels (95% interval) | AUC: a held-out request | AUC: a held-out request, same direction | AUC: state, outcomes reshuffled within request |
|---|---|---|---|---|---|---|
| 0 | 0.612 | 0.852 | -0.053 (-0.098 to -0.007) | 0.420 | 0.538 | 0.460 |
| 3 | 0.597 | 0.885 | -0.021 (-0.055 to +0.011) | 0.599 | 0.580 | 0.434 |
| 6 | 0.602 | 0.892 | -0.014 (-0.051 to +0.025) | 0.598 | 0.547 | 0.368 |
| 9 | 0.598 | 0.881 | -0.024 (-0.068 to +0.015) | 0.584 | 0.609 | 0.359 |
| 12 | 0.550 | 0.853 | -0.052 (-0.110 to -0.001) | 0.550 | 0.484 | 0.322 |
| 15 | 0.519 | 0.833 | -0.073 (-0.122 to -0.023) | 0.628 | 0.592 | 0.391 |
| 18 | 0.537 | 0.858 | -0.047 (-0.093 to -0.002) | 0.630 | 0.550 | 0.414 |
| 21 | 0.601 | 0.864 | -0.041 (-0.083 to -0.001) | 0.628 | 0.466 | 0.336 |
| 24 | 0.597 | 0.859 | -0.046 (-0.086 to -0.009) | 0.680 | 0.479 | 0.356 |
| 27 | 0.591 | 0.904 | -0.002 (-0.037 to +0.028) | 0.738 | 0.602 | 0.334 |
| 30 | 0.593 | 0.878 | -0.027 (-0.079 to +0.015) | 0.698 | 0.653 | 0.374 |
| 33 | 0.610 | 0.895 | -0.011 (-0.057 to +0.028) | 0.681 | 0.627 | 0.432 |
| 36 | 0.608 | 0.884 | -0.022 (-0.077 to +0.026) | 0.696 | 0.568 | 0.368 |
| 39 | 0.606 | 0.879 | -0.026 (-0.083 to +0.019) | 0.689 | 0.598 | 0.393 |
| 42 | 0.644 | 0.875 | -0.030 (-0.090 to +0.017) | 0.710 | 0.615 | 0.377 |
| 45 | 0.624 | 0.858 | -0.047 (-0.110 to +0.003) | 0.697 | 0.550 | 0.406 |

## Bank C at 7 Jan, paired with each career's B twin

