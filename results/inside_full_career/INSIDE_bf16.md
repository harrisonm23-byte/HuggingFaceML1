# Inside the model at the push requests (full careers)

States: Gemma 3 12B at bf16, the last token before each push-request reply, 1740 moments (A: 180, B: 300, C: 240, C2: 180, D: 240, E: 300, F: 300). Every comparison is within the same request (went along vs not: within the same request, experiment and framing); p-values reshuffle labels within those groups (1000 times); q = false-discovery-corrected. Features active in fewer than 5% of the moments compared are left out. Produced by `designs/rd2/analysis/inside_features.py`.

Gemma Scope 2 (google/gemma-scope-2-12b-it, residual stream, 16k): layers [12, 24, 31, 41]; files `resid_post/layer_12_width_16k_l0_medium/params.safetensors`, `resid_post/layer_24_width_16k_l0_medium/params.safetensors`, `resid_post/layer_31_width_16k_l0_medium/params.safetensors`, `resid_post/layer_41_width_16k_l0_medium/params.safetensors`.


## B: UBS's loss frame vs gain frame

**Layer 12** (120 vs 120 moments; 56 features tested; 23 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.81 | +3.25 | 0.0010 | 0.007 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -0.76 | -16.58 | 0.0010 | 0.007 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.66 | +2.04 | 0.0010 | 0.007 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -0.61 | -8.87 | 0.0010 | 0.007 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | +0.59 | +3.17 | 0.0010 | 0.007 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.56 | -13.03 | 0.0010 | 0.007 |
| [3490](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490) | +0.49 | +6.14 | 0.0010 | 0.007 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.45 | -1.28 | 0.0010 | 0.007 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.44 | +5.74 | 0.0020 | 0.010 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.43 | -1.98 | 0.0030 | 0.012 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +0.41 | +3.71 | 0.0030 | 0.012 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -0.41 | -1.43 | 0.0020 | 0.010 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +0.40 | +3.95 | 0.0030 | 0.012 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +0.40 | +1.29 | 0.0020 | 0.010 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.40 | -3.86 | 0.0040 | 0.013 |

**Layer 24** (120 vs 120 moments; 151 features tested; 56 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | -0.83 | -139.98 | 0.0010 | 0.004 |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | -0.76 | -93.91 | 0.0010 | 0.004 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | -0.73 | -64.06 | 0.0010 | 0.004 |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | -0.72 | -100.34 | 0.0010 | 0.004 |
| [8967](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8967) | +0.70 | +48.75 | 0.0010 | 0.004 |
| [13332](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13332) | +0.69 | +49.52 | 0.0010 | 0.004 |
| [15592](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592) | -0.68 | -25.47 | 0.0010 | 0.004 |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | +0.68 | +51.03 | 0.0010 | 0.004 |
| [7741](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7741) | +0.67 | +86.04 | 0.0010 | 0.004 |
| [2839](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2839) | -0.66 | -62.15 | 0.0010 | 0.004 |
| [13891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891) | -0.64 | -29.11 | 0.0010 | 0.004 |
| [16222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16222) | +0.64 | +41.06 | 0.0010 | 0.004 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | +0.62 | +43.67 | 0.0010 | 0.004 |
| [8326](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326) | -0.62 | -74.36 | 0.0010 | 0.004 |
| [8992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8992) | -0.61 | -49.65 | 0.0010 | 0.004 |

**Layer 31** (120 vs 120 moments; 162 features tested; 46 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | +0.70 | +315.16 | 0.0010 | 0.006 |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | +0.67 | +136.35 | 0.0010 | 0.006 |
| [929](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/929) | +0.64 | +123.62 | 0.0010 | 0.006 |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | +0.62 | +352.94 | 0.0010 | 0.006 |
| [15017](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15017) | -0.56 | -114.05 | 0.0010 | 0.006 |
| [8224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8224) | -0.56 | -93.94 | 0.0010 | 0.006 |
| [195](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/195) | +0.55 | +65.80 | 0.0010 | 0.006 |
| [5652](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652) | +0.55 | +50.27 | 0.0020 | 0.012 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +0.54 | +112.30 | 0.0010 | 0.006 |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | +0.54 | +236.44 | 0.0010 | 0.006 |
| [5381](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5381) | -0.53 | -69.91 | 0.0010 | 0.006 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | -0.52 | -144.34 | 0.0010 | 0.006 |
| [4805](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4805) | -0.52 | -283.44 | 0.0010 | 0.006 |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | -0.51 | -262.81 | 0.0010 | 0.006 |
| [3369](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3369) | +0.48 | +102.78 | 0.0010 | 0.006 |

**Layer 41** (120 vs 120 moments; 163 features tested; 30 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | +0.70 | +407.33 | 0.0010 | 0.012 |
| [2903](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2903) | +0.66 | +325.13 | 0.0010 | 0.012 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +0.64 | +1207.44 | 0.0010 | 0.012 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | +0.62 | +388.11 | 0.0010 | 0.012 |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | +0.61 | +374.85 | 0.0010 | 0.012 |
| [755](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/755) | -0.61 | -671.66 | 0.0010 | 0.012 |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | -0.59 | -384.70 | 0.0010 | 0.012 |
| [12726](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12726) | +0.57 | +196.25 | 0.0010 | 0.012 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | -0.57 | -267.18 | 0.0010 | 0.012 |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | +0.55 | +371.95 | 0.0010 | 0.012 |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | +0.54 | +302.45 | 0.0010 | 0.012 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | +0.53 | +405.75 | 0.0020 | 0.017 |
| [2559](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2559) | +0.49 | +264.00 | 0.0020 | 0.017 |
| [1951](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1951) | -0.49 | -210.95 | 0.0010 | 0.012 |
| [946](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/946) | -0.45 | -312.94 | 0.0010 | 0.012 |


## B: "+ you" vs no owner

**Layer 12** (120 vs 120 moments; 56 features tested; 16 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +0.79 | +7.43 | 0.0010 | 0.005 |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | -0.78 | -7.18 | 0.0010 | 0.005 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | -0.69 | -5.71 | 0.0010 | 0.005 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +0.66 | +2.07 | 0.0010 | 0.005 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.63 | -4.18 | 0.0010 | 0.005 |
| [978](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/978) | +0.61 | +1.06 | 0.0010 | 0.005 |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | +0.58 | +7.26 | 0.0010 | 0.005 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | -0.49 | -2.31 | 0.0010 | 0.005 |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | -0.46 | -6.79 | 0.0010 | 0.005 |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | -0.46 | -10.77 | 0.0010 | 0.005 |
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | -0.45 | -2.16 | 0.0010 | 0.005 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | +0.38 | +4.50 | 0.0100 | 0.037 |
| [9038](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9038) | -0.37 | -4.16 | 0.0050 | 0.021 |
| [3490](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490) | -0.35 | -4.48 | 0.0050 | 0.021 |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | +0.34 | +4.02 | 0.0140 | 0.049 |

**Layer 24** (120 vs 120 moments; 151 features tested; 38 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.78 | +39.82 | 0.0010 | 0.011 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.63 | +21.45 | 0.0010 | 0.011 |
| [11000](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11000) | -0.58 | -43.98 | 0.0020 | 0.018 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | +0.57 | +40.30 | 0.0010 | 0.011 |
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.55 | -21.94 | 0.0010 | 0.011 |
| [7741](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7741) | +0.55 | +72.01 | 0.0010 | 0.011 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | -0.54 | -48.25 | 0.0010 | 0.011 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | +0.52 | +65.37 | 0.0010 | 0.011 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | +0.49 | +27.30 | 0.0010 | 0.011 |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | -0.49 | -112.64 | 0.0010 | 0.011 |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | +0.47 | +29.29 | 0.0020 | 0.018 |
| [8185](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8185) | -0.47 | -26.98 | 0.0050 | 0.026 |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | -0.47 | -215.45 | 0.0010 | 0.011 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3051) | +0.47 | +70.49 | 0.0010 | 0.011 |
| [7789](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7789) | +0.47 | +61.42 | 0.0010 | 0.011 |

**Layer 31** (120 vs 120 moments; 162 features tested; 65 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | +0.73 | +383.31 | 0.0010 | 0.006 |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | +0.72 | +321.93 | 0.0010 | 0.006 |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | +0.70 | +230.69 | 0.0010 | 0.006 |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | +0.69 | +298.55 | 0.0010 | 0.006 |
| [4214](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4214) | -0.68 | -237.45 | 0.0010 | 0.006 |
| [15017](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15017) | -0.62 | -124.07 | 0.0010 | 0.006 |
| [2882](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2882) | -0.62 | -117.91 | 0.0010 | 0.006 |
| [1744](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1744) | -0.61 | -135.68 | 0.0010 | 0.006 |
| [2900](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2900) | -0.60 | -151.15 | 0.0020 | 0.008 |
| [2079](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2079) | -0.60 | -131.12 | 0.0010 | 0.006 |
| [4805](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4805) | -0.60 | -318.97 | 0.0020 | 0.008 |
| [13577](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13577) | -0.60 | -186.12 | 0.0010 | 0.006 |
| [2608](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2608) | -0.59 | -132.65 | 0.0020 | 0.008 |
| [7092](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7092) | -0.59 | -149.10 | 0.0010 | 0.006 |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | +0.59 | +103.63 | 0.0010 | 0.006 |

**Layer 41** (120 vs 120 moments; 163 features tested; 40 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | +0.79 | +1148.45 | 0.0010 | 0.007 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | +0.67 | +503.13 | 0.0010 | 0.007 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | +0.66 | +428.90 | 0.0010 | 0.007 |
| [1462](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1462) | +0.62 | +229.36 | 0.0010 | 0.007 |
| [822](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/822) | -0.60 | -722.19 | 0.0010 | 0.007 |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | -0.59 | -184.43 | 0.0010 | 0.007 |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | +0.59 | +1113.50 | 0.0010 | 0.007 |
| [10433](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10433) | -0.56 | -231.76 | 0.0010 | 0.007 |
| [4228](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4228) | -0.54 | -120.33 | 0.0010 | 0.007 |
| [897](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/897) | -0.53 | -201.59 | 0.0010 | 0.007 |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1571) | -0.52 | -542.93 | 0.0010 | 0.007 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | +0.51 | +222.86 | 0.0010 | 0.007 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | +0.50 | +186.47 | 0.0010 | 0.007 |
| [9624](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9624) | -0.50 | -89.61 | 0.0010 | 0.007 |
| [3798](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3798) | -0.50 | -192.52 | 0.0010 | 0.007 |


## B: framed vs neutral

**Layer 12** (240 vs 60 moments; 56 features tested; 35 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | +2.26 | +7.43 | 0.0010 | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +2.18 | +7.22 | 0.0010 | 0.002 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -2.09 | -33.13 | 0.0010 | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +1.74 | +7.08 | 0.0010 | 0.002 |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | +1.73 | +12.55 | 0.0010 | 0.002 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +1.59 | +16.25 | 0.0010 | 0.002 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +1.58 | +19.48 | 0.0010 | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +1.55 | +21.90 | 0.0010 | 0.002 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +1.43 | +15.45 | 0.0010 | 0.002 |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | -1.41 | -32.85 | 0.0010 | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +1.41 | +12.02 | 0.0010 | 0.002 |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | -1.40 | -17.26 | 0.0010 | 0.002 |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +1.34 | +12.30 | 0.0010 | 0.002 |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | +1.32 | +17.43 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +1.26 | +3.77 | 0.0010 | 0.002 |

**Layer 24** (240 vs 60 moments; 147 features tested; 23 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [11000](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11000) | -0.81 | -58.73 | 0.0010 | 0.009 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | -0.73 | -19.63 | 0.0010 | 0.009 |
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | -0.66 | -25.33 | 0.0010 | 0.009 |
| [13585](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13585) | +0.66 | +18.84 | 0.0010 | 0.009 |
| [11165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11165) | -0.66 | -19.14 | 0.0010 | 0.009 |
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.64 | -25.39 | 0.0010 | 0.009 |
| [831](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/831) | +0.63 | +86.92 | 0.0010 | 0.009 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.63 | +32.69 | 0.0010 | 0.009 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | -0.62 | -60.16 | 0.0010 | 0.009 |
| [9712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712) | -0.60 | -19.70 | 0.0010 | 0.009 |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | +0.58 | +87.31 | 0.0010 | 0.009 |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3051) | +0.57 | +83.24 | 0.0010 | 0.009 |
| [10617](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10617) | -0.55 | -50.70 | 0.0020 | 0.017 |
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | -0.54 | -30.32 | 0.0010 | 0.009 |
| [12577](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12577) | +0.53 | +27.92 | 0.0010 | 0.009 |

**Layer 31** (240 vs 60 moments; 160 features tested; 29 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | -0.75 | -157.91 | 0.0010 | 0.027 |
| [3331](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3331) | -0.74 | -111.89 | 0.0010 | 0.027 |
| [2069](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2069) | -0.62 | -136.16 | 0.0010 | 0.027 |
| [4056](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4056) | -0.62 | -184.24 | 0.0010 | 0.027 |
| [1519](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1519) | -0.55 | -120.26 | 0.0010 | 0.027 |
| [6294](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6294) | +0.51 | +144.19 | 0.0010 | 0.027 |
| [1128](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1128) | +0.51 | +106.11 | 0.0020 | 0.035 |
| [6048](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6048) | +0.50 | +123.10 | 0.0020 | 0.035 |
| [12956](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12956) | -0.47 | -73.91 | 0.0050 | 0.044 |
| [2900](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2900) | +0.46 | +111.99 | 0.0030 | 0.040 |
| [3369](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3369) | -0.46 | -98.47 | 0.0060 | 0.044 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1708) | -0.45 | -53.09 | 0.0050 | 0.044 |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | -0.45 | -122.62 | 0.0030 | 0.040 |
| [2608](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2608) | +0.45 | +96.34 | 0.0040 | 0.044 |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | -0.44 | -231.25 | 0.0020 | 0.035 |

**Layer 41** (240 vs 60 moments; 166 features tested; 17 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | -0.64 | -90.78 | 0.0010 | 0.018 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | -0.58 | -372.09 | 0.0010 | 0.018 |
| [2880](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2880) | -0.53 | -162.91 | 0.0010 | 0.018 |
| [10380](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10380) | -0.53 | -103.19 | 0.0010 | 0.018 |
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | -0.51 | -142.44 | 0.0010 | 0.018 |
| [1409](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1409) | -0.50 | -103.76 | 0.0040 | 0.044 |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | -0.50 | -226.58 | 0.0010 | 0.018 |
| [1179](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1179) | -0.49 | -205.35 | 0.0020 | 0.028 |
| [13569](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13569) | -0.49 | -122.58 | 0.0040 | 0.044 |
| [3420](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3420) | -0.49 | -187.33 | 0.0010 | 0.018 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | -0.48 | -176.84 | 0.0010 | 0.018 |
| [14456](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14456) | +0.48 | +134.72 | 0.0020 | 0.028 |
| [4647](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4647) | -0.48 | -207.68 | 0.0010 | 0.018 |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | -0.47 | -325.68 | 0.0030 | 0.038 |
| [5548](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5548) | +0.46 | +197.26 | 0.0020 | 0.028 |


## All experiments: went along vs did not (same request, experiment and framing)

**Layer 12** (286 vs 1424 moments; 56 features tested; 0 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | -0.38 | -1.78 | 0.0030 | 0.084 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.33 | -0.91 | 0.0030 | 0.084 |
| [9038](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9038) | +0.31 | +2.35 | 0.0060 | 0.112 |
| [16341](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16341) | +0.29 | +3.09 | 0.0170 | 0.140 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -0.28 | -0.85 | 0.0140 | 0.140 |
| [1245](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1245) | -0.27 | -1.75 | 0.0230 | 0.140 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | -0.26 | -0.82 | 0.0170 | 0.140 |
| [6423](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423) | -0.25 | -1.36 | 0.0250 | 0.140 |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | +0.25 | +3.00 | 0.0230 | 0.140 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -0.25 | -0.68 | 0.0240 | 0.140 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | +0.22 | +0.67 | 0.0330 | 0.168 |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | -0.20 | -2.41 | 0.0629 | 0.264 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | -0.20 | -1.76 | 0.0659 | 0.264 |
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | -0.20 | -0.81 | 0.0609 | 0.264 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -0.20 | -1.33 | 0.0769 | 0.269 |

**Layer 24** (286 vs 1424 moments; 140 features tested; 21 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3068](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3068) | +0.61 | +66.30 | 0.0010 | 0.013 |
| [13799](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799) | -0.51 | -17.54 | 0.0010 | 0.013 |
| [869](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/869) | +0.48 | +41.29 | 0.0010 | 0.013 |
| [16222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16222) | -0.45 | -29.71 | 0.0010 | 0.013 |
| [11975](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11975) | -0.41 | -15.02 | 0.0010 | 0.013 |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | -0.41 | -63.70 | 0.0010 | 0.013 |
| [12075](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12075) | -0.41 | -7.44 | 0.0010 | 0.013 |
| [7925](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7925) | +0.41 | +44.43 | 0.0020 | 0.021 |
| [2896](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2896) | -0.40 | -37.03 | 0.0010 | 0.013 |
| [5341](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5341) | +0.40 | +29.05 | 0.0040 | 0.031 |
| [4250](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4250) | -0.39 | -30.05 | 0.0010 | 0.013 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +0.39 | +40.97 | 0.0020 | 0.021 |
| [3987](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3987) | +0.39 | +37.85 | 0.0010 | 0.013 |
| [12678](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12678) | +0.38 | +13.61 | 0.0010 | 0.013 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +0.35 | +16.27 | 0.0030 | 0.026 |

**Layer 31** (286 vs 1424 moments; 162 features tested; 15 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | -0.69 | -159.45 | 0.0010 | 0.018 |
| [7338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7338) | +0.68 | +97.49 | 0.0010 | 0.018 |
| [95](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/95) | +0.53 | +124.71 | 0.0010 | 0.018 |
| [1128](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1128) | +0.47 | +107.99 | 0.0010 | 0.018 |
| [3331](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3331) | +0.43 | +75.55 | 0.0020 | 0.027 |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | -0.42 | -78.00 | 0.0010 | 0.018 |
| [892](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/892) | +0.42 | +65.44 | 0.0010 | 0.018 |
| [1275](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1275) | +0.39 | +58.49 | 0.0010 | 0.018 |
| [3309](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3309) | -0.38 | -75.28 | 0.0010 | 0.018 |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | -0.38 | -74.17 | 0.0010 | 0.018 |
| [6617](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6617) | +0.37 | +88.50 | 0.0030 | 0.032 |
| [5297](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5297) | -0.36 | -38.07 | 0.0030 | 0.032 |
| [2069](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2069) | -0.34 | -66.88 | 0.0020 | 0.027 |
| [1293](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1293) | +0.33 | +71.52 | 0.0030 | 0.032 |
| [879](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/879) | -0.32 | -60.58 | 0.0020 | 0.027 |

**Layer 41** (286 vs 1424 moments; 171 features tested; 18 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3296](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3296) | +0.43 | +179.03 | 0.0010 | 0.029 |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | -0.43 | -244.04 | 0.0010 | 0.029 |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | -0.42 | -190.99 | 0.0020 | 0.038 |
| [2880](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2880) | -0.41 | -104.20 | 0.0010 | 0.029 |
| [911](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/911) | -0.40 | -171.13 | 0.0020 | 0.038 |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | +0.39 | +68.36 | 0.0010 | 0.029 |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | +0.38 | +204.92 | 0.0020 | 0.038 |
| [865](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/865) | +0.38 | +150.57 | 0.0010 | 0.029 |
| [14456](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14456) | +0.37 | +120.21 | 0.0010 | 0.029 |
| [6705](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6705) | -0.36 | -114.56 | 0.0050 | 0.048 |
| [7808](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7808) | +0.35 | +127.58 | 0.0050 | 0.048 |
| [3021](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3021) | -0.34 | -74.79 | 0.0030 | 0.047 |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | -0.34 | -297.94 | 0.0030 | 0.047 |
| [3067](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3067) | -0.34 | -65.34 | 0.0060 | 0.051 |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | -0.34 | -122.56 | 0.0040 | 0.048 |


## A: a memo (loss, gain, + you) vs the neutral memo

**Layer 12** (120 vs 30 moments; 55 features tested; 27 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +2.36 | +6.70 | 0.0010 | 0.003 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | -1.61 | -4.13 | 0.0010 | 0.003 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +1.55 | +12.86 | 0.0010 | 0.003 |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | -1.53 | -17.15 | 0.0010 | 0.003 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +1.47 | +12.60 | 0.0010 | 0.003 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | +1.47 | +3.77 | 0.0010 | 0.003 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | +1.46 | +14.59 | 0.0010 | 0.003 |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | -1.39 | -4.40 | 0.0010 | 0.003 |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | +1.28 | +19.39 | 0.0010 | 0.003 |
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | +1.22 | +2.45 | 0.0010 | 0.003 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +1.17 | +13.01 | 0.0010 | 0.003 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +1.09 | +3.41 | 0.0010 | 0.003 |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | +1.06 | +6.02 | 0.0010 | 0.003 |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | +1.05 | +7.23 | 0.0010 | 0.003 |
| [3490](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490) | +0.99 | +12.87 | 0.0010 | 0.003 |

**Layer 24** (120 vs 30 moments; 136 features tested; 14 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [13744](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13744) | -1.19 | -53.32 | 0.0010 | 0.019 |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | +1.05 | +66.40 | 0.0010 | 0.019 |
| [11552](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11552) | +0.84 | +48.70 | 0.0010 | 0.019 |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1826) | +0.80 | +105.14 | 0.0020 | 0.025 |
| [4392](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4392) | +0.77 | +52.38 | 0.0020 | 0.025 |
| [5445](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445) | +0.73 | +32.88 | 0.0010 | 0.019 |
| [10327](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10327) | -0.72 | -16.56 | 0.0010 | 0.019 |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | +0.70 | +90.05 | 0.0020 | 0.025 |
| [6460](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6460) | -0.67 | -58.34 | 0.0010 | 0.019 |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | +0.66 | +51.92 | 0.0020 | 0.025 |
| [8185](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8185) | +0.66 | +32.59 | 0.0030 | 0.031 |
| [14414](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14414) | -0.65 | -55.31 | 0.0030 | 0.031 |
| [9368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368) | -0.64 | -23.91 | 0.0040 | 0.039 |
| [9712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712) | +0.62 | +20.93 | 0.0010 | 0.019 |
| [5480](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5480) | -0.60 | -77.14 | 0.0060 | 0.054 |

**Layer 31** (120 vs 30 moments; 153 features tested; 8 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [2927](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2927) | -1.23 | -158.59 | 0.0010 | 0.022 |
| [3180](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3180) | -1.06 | -193.93 | 0.0010 | 0.022 |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | +0.92 | +166.50 | 0.0010 | 0.022 |
| [1519](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1519) | -0.87 | -230.27 | 0.0010 | 0.022 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | -0.87 | -198.57 | 0.0010 | 0.022 |
| [3101](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3101) | -0.77 | -150.08 | 0.0010 | 0.022 |
| [1880](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1880) | -0.76 | -110.64 | 0.0010 | 0.022 |
| [7525](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7525) | -0.74 | -97.17 | 0.0040 | 0.051 |
| [968](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/968) | +0.73 | +114.10 | 0.0040 | 0.051 |
| [569](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/569) | -0.72 | -69.89 | 0.0040 | 0.051 |
| [1293](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1293) | -0.71 | -116.80 | 0.0020 | 0.038 |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | -0.65 | -245.38 | 0.0040 | 0.051 |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | -0.57 | -180.30 | 0.0050 | 0.059 |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | +0.56 | +259.46 | 0.0100 | 0.102 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8848) | +0.55 | +56.90 | 0.0360 | 0.246 |

**Layer 41** (120 vs 30 moments; 160 features tested; 0 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [5413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5413) | -0.82 | -202.82 | 0.0010 | 0.053 |
| [2697](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2697) | +0.81 | +346.07 | 0.0010 | 0.053 |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | +0.76 | +365.23 | 0.0020 | 0.060 |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | -0.74 | -512.31 | 0.0010 | 0.053 |
| [1163](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1163) | +0.73 | +279.51 | 0.0030 | 0.060 |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | -0.72 | -219.40 | 0.0020 | 0.060 |
| [1734](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1734) | -0.68 | -423.96 | 0.0030 | 0.060 |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/262) | -0.67 | -172.48 | 0.0050 | 0.073 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | +0.64 | +239.09 | 0.0080 | 0.107 |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | -0.64 | -307.30 | 0.0030 | 0.060 |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | -0.62 | -144.84 | 0.0050 | 0.073 |
| [3798](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3798) | -0.56 | -187.30 | 0.0050 | 0.073 |
| [1742](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1742) | -0.55 | -108.44 | 0.0150 | 0.133 |
| [1861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1861) | +0.55 | +194.75 | 0.0210 | 0.168 |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | -0.54 | -287.28 | 0.0130 | 0.132 |


## A: UBS's request vs the same moment without it

**Layer 12** (30 vs 30 moments; 62 features tested; 47 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [329](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/329) | -19.13 | -5.97 | 0.0110 | 0.015 |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | +14.41 | +12.99 | 0.0010 | 0.002 |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | -12.00 | -25.87 | 0.0010 | 0.002 |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | -7.75 | -17.88 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | -7.18 | -13.22 | 0.0010 | 0.002 |
| [1593](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593) | +6.05 | +17.15 | 0.0010 | 0.002 |
| [4382](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382) | -5.16 | -14.44 | 0.0010 | 0.002 |
| [3205](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205) | -5.04 | -11.00 | 0.0010 | 0.002 |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | -4.60 | -10.01 | 0.0010 | 0.002 |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | -4.15 | -37.78 | 0.0010 | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | -4.00 | -8.46 | 0.0010 | 0.002 |
| [5872](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5872) | -3.92 | -24.33 | 0.0010 | 0.002 |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | -3.91 | -8.10 | 0.0010 | 0.002 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -3.88 | -12.38 | 0.0010 | 0.002 |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | +3.38 | +22.39 | 0.0010 | 0.002 |

**Layer 24** (30 vs 30 moments; 154 features tested; 90 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [7745](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7745) | -6.40 | -208.52 | 0.0010 | 0.003 |
| [8790](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8790) | -5.52 | -182.94 | 0.0010 | 0.003 |
| [6357](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6357) | -4.78 | -51.63 | 0.0100 | 0.019 |
| [9503](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9503) | -4.39 | -219.92 | 0.0010 | 0.003 |
| [11649](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649) | +4.05 | +30.17 | 0.0070 | 0.014 |
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | +3.70 | +93.00 | 0.0010 | 0.003 |
| [11105](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11105) | -3.63 | -124.34 | 0.0010 | 0.003 |
| [8967](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8967) | -3.55 | -129.00 | 0.0010 | 0.003 |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | +3.54 | +311.12 | 0.0010 | 0.003 |
| [2697](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2697) | -3.32 | -131.86 | 0.0010 | 0.003 |
| [11296](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11296) | -3.32 | -19.33 | 0.0070 | 0.014 |
| [16165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16165) | +3.25 | +127.36 | 0.0010 | 0.003 |
| [1672](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1672) | +3.24 | +203.34 | 0.0010 | 0.003 |
| [12075](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12075) | +3.24 | +47.09 | 0.0010 | 0.003 |
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3717) | +3.17 | +279.46 | 0.0010 | 0.003 |

**Layer 31** (30 vs 30 moments; 192 features tested; 83 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1260](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1260) | -14.12 | -195.50 | 0.0010 | 0.004 |
| [756](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/756) | -11.89 | -79.95 | 0.0050 | 0.015 |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | -4.44 | -603.14 | 0.0010 | 0.004 |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | -4.30 | -747.00 | 0.0010 | 0.004 |
| [2750](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2750) | -3.51 | -379.19 | 0.0010 | 0.004 |
| [15513](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15513) | -3.45 | -96.01 | 0.0090 | 0.026 |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1708) | -3.41 | -356.22 | 0.0010 | 0.004 |
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | -3.06 | -497.71 | 0.0010 | 0.004 |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/26) | -2.68 | -629.90 | 0.0010 | 0.004 |
| [2103](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2103) | +2.63 | +338.62 | 0.0010 | 0.004 |
| [3369](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3369) | -2.49 | -287.81 | 0.0010 | 0.004 |
| [15940](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15940) | -2.31 | -145.60 | 0.0010 | 0.004 |
| [357](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/357) | +2.21 | +437.02 | 0.0010 | 0.004 |
| [584](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/584) | -2.19 | -115.56 | 0.0050 | 0.015 |
| [7579](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7579) | -2.19 | -211.47 | 0.0010 | 0.004 |

**Layer 41** (30 vs 30 moments; 192 features tested; 104 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [1594](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1594) | -10.83 | -177.09 | 0.0070 | 0.016 |
| [5301](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5301) | -8.72 | -1377.08 | 0.0010 | 0.003 |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | -7.62 | -560.80 | 0.0010 | 0.003 |
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | -5.67 | -518.95 | 0.0010 | 0.003 |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | -4.91 | -2233.84 | 0.0010 | 0.003 |
| [8441](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8441) | -4.80 | -1018.66 | 0.0010 | 0.003 |
| [10380](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10380) | -4.52 | -1013.62 | 0.0010 | 0.003 |
| [2998](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2998) | -3.92 | -1252.29 | 0.0010 | 0.003 |
| [1838](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1838) | -3.65 | -414.07 | 0.0010 | 0.003 |
| [1232](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1232) | -3.62 | -230.36 | 0.0120 | 0.024 |
| [1102](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1102) | -3.47 | -197.65 | 0.0070 | 0.016 |
| [4586](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4586) | +3.20 | +908.25 | 0.0010 | 0.003 |
| [6679](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6679) | -3.17 | -292.88 | 0.0010 | 0.003 |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | +3.10 | +995.28 | 0.0010 | 0.003 |
| [1059](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1059) | -2.75 | -336.13 | 0.0010 | 0.003 |


## Bank C: F vs B (same framings)

**Layer 12** (300 vs 300 moments; 55 features tested; 38 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | +3.06 | +17.89 | 0.0010 | 0.002 |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524) | +1.58 | +5.29 | 0.0010 | 0.002 |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | +1.37 | +19.89 | 0.0010 | 0.002 |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | -1.28 | -11.19 | 0.0010 | 0.002 |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | +1.25 | +3.40 | 0.0010 | 0.002 |
| [5791](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791) | -1.09 | -4.14 | 0.0010 | 0.002 |
| [4382](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382) | -1.03 | -3.68 | 0.0010 | 0.002 |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | -1.03 | -14.42 | 0.0010 | 0.002 |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | +0.91 | +11.61 | 0.0010 | 0.002 |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | +0.84 | +11.31 | 0.0010 | 0.002 |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | +0.83 | +4.21 | 0.0010 | 0.002 |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | +0.83 | +15.12 | 0.0010 | 0.002 |
| [3143](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143) | -0.82 | -2.67 | 0.0010 | 0.002 |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | -0.81 | -14.72 | 0.0010 | 0.002 |
| [1641](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641) | +0.79 | +7.21 | 0.0010 | 0.002 |

**Layer 24** (300 vs 300 moments; 143 features tested; 71 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [13674](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13674) | +0.90 | +48.54 | 0.0010 | 0.003 |
| [9712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712) | +0.78 | +26.55 | 0.0010 | 0.003 |
| [5671](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671) | -0.74 | -27.94 | 0.0010 | 0.003 |
| [16165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16165) | -0.69 | -32.98 | 0.0010 | 0.003 |
| [2098](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2098) | +0.65 | +17.16 | 0.0010 | 0.003 |
| [1672](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1672) | +0.64 | +53.44 | 0.0010 | 0.003 |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | +0.64 | +24.18 | 0.0010 | 0.003 |
| [15074](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074) | +0.64 | +68.31 | 0.0010 | 0.003 |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | +0.62 | +36.90 | 0.0010 | 0.003 |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | -0.62 | -96.80 | 0.0010 | 0.003 |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | +0.55 | +74.24 | 0.0010 | 0.003 |
| [11359](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11359) | +0.52 | +8.13 | 0.0010 | 0.003 |
| [11837](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11837) | +0.51 | +14.43 | 0.0010 | 0.003 |
| [10327](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10327) | +0.47 | +15.32 | 0.0010 | 0.003 |
| [3122](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3122) | +0.47 | +42.11 | 0.0010 | 0.003 |

**Layer 31** (300 vs 300 moments; 167 features tested; 73 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [2790](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2790) | +0.95 | +195.25 | 0.0010 | 0.003 |
| [3976](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3976) | +0.80 | +112.95 | 0.0010 | 0.003 |
| [1316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1316) | +0.74 | +100.54 | 0.0010 | 0.003 |
| [1293](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1293) | +0.70 | +192.37 | 0.0010 | 0.003 |
| [3723](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3723) | +0.67 | +100.33 | 0.0010 | 0.003 |
| [16063](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/16063) | +0.65 | +117.64 | 0.0010 | 0.003 |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | +0.64 | +478.45 | 0.0010 | 0.003 |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | +0.63 | +185.20 | 0.0010 | 0.003 |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | +0.62 | +106.98 | 0.0010 | 0.003 |
| [2130](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130) | +0.60 | +136.26 | 0.0010 | 0.003 |
| [7201](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7201) | +0.59 | +95.16 | 0.0010 | 0.003 |
| [1460](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1460) | +0.59 | +78.50 | 0.0010 | 0.003 |
| [1880](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1880) | +0.59 | +130.95 | 0.0010 | 0.003 |
| [1824](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1824) | +0.57 | +148.71 | 0.0010 | 0.003 |
| [2809](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2809) | +0.56 | +134.96 | 0.0010 | 0.003 |

**Layer 41** (300 vs 300 moments; 171 features tested; 86 with q < 0.05)

| Feature | Difference (spread units) | Activation difference | p | q |
|---|---|---|---|---|
| [6938](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6938) | +1.51 | +554.30 | 0.0010 | 0.003 |
| [3981](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3981) | +1.23 | +407.58 | 0.0010 | 0.003 |
| [8520](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8520) | +1.10 | +797.91 | 0.0010 | 0.003 |
| [1405](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1405) | +0.94 | +240.66 | 0.0010 | 0.003 |
| [843](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/843) | +0.93 | +275.93 | 0.0010 | 0.003 |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | +0.92 | +422.67 | 0.0010 | 0.003 |
| [5120](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5120) | +0.86 | +277.23 | 0.0010 | 0.003 |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | +0.79 | +952.90 | 0.0010 | 0.003 |
| [5976](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5976) | +0.75 | +374.90 | 0.0010 | 0.003 |
| [1331](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1331) | +0.73 | +239.09 | 0.0010 | 0.003 |
| [5736](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5736) | +0.72 | +176.20 | 0.0010 | 0.003 |
| [2697](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2697) | +0.69 | +258.86 | 0.0010 | 0.003 |
| [1281](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1281) | +0.69 | +152.83 | 0.0010 | 0.003 |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | -0.65 | -466.92 | 0.0010 | 0.003 |
| [865](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/865) | +0.62 | +233.47 | 0.0010 | 0.003 |


## Can "went along" be read from the state, beyond the request and the framing?

1710 moments with a request, 286 went along. Read-out scored on careers it was not trained on (5 folds by career), and on a request it never saw (careers share chat lines, e.g. C clean = B neutral, so the held-out request shows it is not learning the conversation). **The labels alone (request, experiment, version) score AUC 0.892.** States are centred within each request and reduced to 64 components per layer (fitted on all careers' states, no outcome used). "Gain" is state + labels minus labels alone, with a 95% interval from resampling careers (an interval above 0 means the state adds something). The held-out request is also scored by a read-out trained only on requests where UBS wants the same direction (going along is buying in some requests and selling in others).

| Layer | AUC: state | AUC: state + labels | Gain over labels (95% interval) | AUC: a held-out request | AUC: a held-out request, same direction | AUC: state, outcomes reshuffled within request |
|---|---|---|---|---|---|---|
| 0 | 0.679 | 0.894 | +0.002 (-0.009 to +0.013) | 0.475 | 0.281 | 0.483 |
| 3 | 0.699 | 0.894 | +0.002 (-0.008 to +0.012) | 0.480 | 0.261 | 0.482 |
| 6 | 0.700 | 0.893 | +0.002 (-0.009 to +0.011) | 0.436 | 0.326 | 0.502 |
| 9 | 0.701 | 0.889 | -0.003 (-0.013 to +0.008) | 0.427 | 0.247 | 0.449 |
| 12 | 0.701 | 0.897 | +0.005 (-0.005 to +0.015) | 0.483 | 0.299 | 0.451 |
| 15 | 0.703 | 0.896 | +0.005 (-0.005 to +0.015) | 0.511 | 0.307 | 0.491 |
| 18 | 0.709 | 0.899 | +0.007 (-0.004 to +0.017) | 0.557 | 0.305 | 0.445 |
| 21 | 0.738 | 0.915 | +0.023 (+0.011 to +0.034) | 0.539 | 0.303 | 0.505 |
| 24 | 0.748 | 0.918 | +0.026 (+0.014 to +0.037) | 0.590 | 0.345 | 0.448 |
| 27 | 0.741 | 0.913 | +0.021 (+0.008 to +0.033) | 0.589 | 0.367 | 0.466 |
| 30 | 0.736 | 0.917 | +0.025 (+0.011 to +0.037) | 0.575 | 0.387 | 0.474 |
| 33 | 0.734 | 0.914 | +0.023 (+0.010 to +0.035) | 0.589 | 0.396 | 0.522 |
| 36 | 0.734 | 0.913 | +0.022 (+0.008 to +0.033) | 0.569 | 0.387 | 0.428 |
| 39 | 0.723 | 0.912 | +0.021 (+0.007 to +0.032) | 0.558 | 0.375 | 0.453 |
| 42 | 0.713 | 0.914 | +0.022 (+0.010 to +0.033) | 0.537 | 0.402 | 0.465 |
| 45 | 0.730 | 0.917 | +0.025 (+0.013 to +0.037) | 0.555 | 0.390 | 0.440 |

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
