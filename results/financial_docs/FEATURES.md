# What the financial documents activate inside the model (exploratory)

39 documents (neutral 13, loss 13, gain 13), each read on its own by Gemma 3 12B (bfloat16). Every token's state passed through the Gemma Scope 2 dictionary (16k, residual stream); a document's activation of a feature is its mean over the document's tokens. p reshuffles which documents belong to which type (2,000 times, read off a normal fitted to the reshuffled differences); q is false-discovery corrected over the features active in either type. Names are Neuronpedia's automatic descriptions where it has one; every feature links to its page. Produced by `designs/rd2/analysis/emotion_features.py`.


## Layer 12

**Loss documents against neutral documents** (7515 features active; 302 differ at q < 0.05; 164 more active in loss, 138 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 44.0 / 3.1 | 17% |  |
| [2503](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2503) | 38.5 / 1.7 | 40% | growth patterns |
| [2887](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2887) | 35.4 / 9.2 | 62% |  |
| [12](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/12) | 30.7 / 6.3 | 19% | ' followed by 't' or 'm' |
| [258](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/258) | 26.9 / 7.2 | 17% |  |
| [217](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/217) | 17.6 / 0.5 | 7% |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 21.3 / 4.1 | 22% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 17.3 / 1.0 | 10% |  |
| [320](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/320) | 17.4 / 3.5 | 7% |  |
| [11371](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/11371) | 12.9 / 0.2 | 20% | economic downturns and crises |
| [714](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/714) | 19.7 / 7.0 | 16% |  |
| [853](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/853) | 16.5 / 4.5 | 11% |  |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 7.2 / 42.6 | 23% |  |
| [267](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/267) | 27.1 / 59.8 | 18% |  |
| [510](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/510) | 9.1 / 40.9 | 17% |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/100) | 13.7 / 40.4 | 17% |  |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/262) | 7.0 / 30.8 | 6% |  |
| [619](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/619) | 25.1 / 46.5 | 42% |  |
| [656](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/656) | 10.2 / 31.4 | 33% | attention scores |
| [647](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/647) | 27.1 / 47.8 | 32% |  |
| [402](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/402) | 21.7 / 42.1 | 7% |  |
| [621](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/621) | 8.0 / 26.7 | 22% |  |
| [357](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/357) | 15.3 / 33.9 | 5% |  |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 16.2 / 34.6 | 35% |  |

**Gain documents against neutral documents** (7363 features active; 510 differ at q < 0.05; 272 more active in gain, 238 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [2503](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2503) | 52.6 / 1.7 | 52% | growth patterns |
| [1042](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1042) | 117.9 / 69.1 | 95% | finance and economic volatility |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/420) | 38.8 / 0.2 | 12% |  |
| [217](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/217) | 34.7 / 0.5 | 12% |  |
| [12](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/12) | 40.4 / 6.3 | 24% | ' followed by 't' or 'm' |
| [163](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/163) | 36.6 / 8.0 | 17% |  |
| [2887](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2887) | 33.6 / 9.2 | 60% |  |
| [258](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/258) | 30.8 / 7.2 | 20% |  |
| [659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/659) | 23.5 / 3.0 | 16% | mathematical expressions with numbers |
| [251](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/251) | 27.5 / 7.7 | 14% |  |
| [10287](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/10287) | 19.9 / 1.8 | 26% | quantities and units |
| [826](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/826) | 17.7 / 0.3 | 15% |  |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [267](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/267) | 17.3 / 59.8 | 18% |  |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 6.3 / 42.6 | 23% |  |
| [510](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/510) | 6.5 / 40.9 | 17% |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/100) | 10.5 / 40.4 | 17% |  |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/262) | 4.6 / 30.8 | 6% |  |
| [8818](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8818) | 10.1 / 35.0 | 41% | government bonds and securities |
| [619](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/619) | 23.3 / 46.5 | 42% |  |
| [402](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/402) | 18.9 / 42.1 | 7% |  |
| [656](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/656) | 9.2 / 31.4 | 33% | attention scores |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 13.2 / 34.6 | 35% |  |
| [647](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/647) | 27.0 / 47.8 | 32% |  |
| [621](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/621) | 6.4 / 26.7 | 22% |  |

**Loss documents against gain documents** (7104 features active; 3 differ at q < 0.05; 3 more active in loss, 0 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 44.0 / 5.2 | 17% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 17.3 / 1.2 | 10% |  |
| [1772](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1772) | 5.5 / 0.3 | 10% |  |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 46 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 0 point the same way (about 0.0 expected by chance) and 0 the opposite way. Correlation of the two differences over the 38 features active in both: -0.03.


## Layer 24

**Loss documents against neutral documents** (4988 features active; 366 differ at q < 0.05; 172 more active in loss, 194 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [701](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/701) | 364.7 / 16.8 | 76% | reportedly |
| [13109](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13109) | 272.8 / 72.8 | 73% | economic conditions and volatility |
| [338](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/338) | 202.0 / 9.8 | 10% |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 239.8 / 48.2 | 31% |  |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 381.8 / 196.7 | 27% |  |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/420) | 235.9 / 57.1 | 19% |  |
| [527](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/527) | 193.1 / 41.2 | 34% | India judgment |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/277) | 148.4 / 2.9 | 6% | foreign language words |
| [1992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1992) | 183.1 / 37.7 | 15% |  |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/249) | 132.3 / 0.3 | 5% | 6 |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 345.3 / 214.8 | 36% |  |
| [210](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/210) | 231.7 / 101.3 | 31% |  |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 63.5 / 281.9 | 24% |  |
| [271](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/271) | 80.0 / 221.4 | 16% |  |
| [459](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/459) | 139.1 / 276.0 | 19% |  |
| [1244](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1244) | 98.2 / 219.4 | 53% | and why |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/543) | 7.9 / 101.2 | 4% | listing conjunctions and examples |
| [5167](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5167) | 15.3 / 107.4 | 23% | end of turn tokens |
| [24](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/24) | 49.2 / 141.2 | 21% | explaining various contexts |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 175.1 / 262.4 | 14% | skills and experience |
| [12863](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12863) | 2.3 / 88.5 | 33% | science and biology terms |
| [468](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/468) | 45.0 / 127.2 | 11% |  |
| [97](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/97) | 63.9 / 138.6 | 11% |  |
| [412](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/412) | 168.2 / 236.6 | 5% |  |

**Gain documents against neutral documents** (4923 features active; 556 differ at q < 0.05; 251 more active in gain, 305 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [338](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/338) | 415.6 / 9.8 | 17% |  |
| [701](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/701) | 348.0 / 16.8 | 74% | reportedly |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/420) | 386.4 / 57.1 | 26% |  |
| [3147](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3147) | 387.6 / 111.5 | 78% | numbers and statistics |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/277) | 274.4 / 2.9 | 10% | foreign language words |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 456.7 / 196.7 | 32% |  |
| [1992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1992) | 275.7 / 37.7 | 21% |  |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/249) | 217.7 / 0.3 | 8% | 6 |
| [210](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/210) | 286.7 / 101.3 | 37% |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 228.1 / 48.2 | 31% |  |
| [527](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/527) | 218.2 / 41.2 | 38% | India judgment |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/111) | 373.2 / 207.2 | 56% |  |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 52.5 / 281.9 | 24% |  |
| [459](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/459) | 109.4 / 276.0 | 19% |  |
| [271](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/271) | 58.1 / 221.4 | 16% |  |
| [1244](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1244) | 79.0 / 219.4 | 53% | and why |
| [468](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/468) | 25.3 / 127.2 | 11% |  |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 161.3 / 262.4 | 14% | skills and experience |
| [385](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/385) | 104.9 / 199.0 | 11% |  |
| [465](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/465) | 16.5 / 110.3 | 6% |  |
| [538](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/538) | 44.3 / 137.4 | 8% | groups of people or entities |
| [5167](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5167) | 14.6 / 107.4 | 23% | end of turn tokens |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/543) | 9.6 / 101.2 | 4% | listing conjunctions and examples |
| [12863](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12863) | 3.3 / 88.5 | 33% | science and biology terms |

**Loss documents against gain documents** (4726 features active; 4 differ at q < 0.05; 4 more active in loss, 0 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [11564](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11564) | 32.3 / 2.0 | 9% | negative connotation |
| [9245](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9245) | 24.6 / 1.9 | 8% | dissolution, loss, decrease |
| [4376](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4376) | 20.7 / 1.1 | 6% |  |
| [2367](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2367) | 15.4 / 1.5 | 4% | removed, discard, forget, paused |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 77 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 0 point the same way (about 0.0 expected by chance) and 0 the opposite way. Correlation of the two differences over the 250 features active in both: +0.00.


## Layer 31

**Loss documents against neutral documents** (7923 features active; 282 differ at q < 0.05; 153 more active in loss, 129 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 438.4 / 0.3 | 47% |  |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 271.3 / 9.3 | 20% | crises and disasters |
| [342](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/342) | 374.7 / 123.0 | 27% |  |
| [4697](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4697) | 242.2 / 2.4 | 17% | increase or decrease by |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/442) | 404.6 / 171.5 | 37% |  |
| [2261](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2261) | 246.4 / 20.6 | 36% | aid to Ukraine |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 216.4 / 14.4 | 26% |  |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/316) | 195.6 / 1.8 | 9% | quantifying numbers followed by units |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 193.0 / 11.3 | 27% |  |
| [4471](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4471) | 180.5 / 15.7 | 17% |  |
| [1229](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1229) | 162.2 / 2.7 | 17% | declines and victory |
| [696](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/696) | 164.1 / 7.6 | 20% | reportedly criticized or controversial allegations |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [296](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/296) | 23.1 / 327.6 | 20% |  |
| [325](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/325) | 210.4 / 496.2 | 20% |  |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/227) | 99.9 / 379.4 | 28% |  |
| [4372](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4372) | 68.8 / 317.4 | 46% | cost, exam, errors, amount |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/543) | 43.8 / 260.1 | 12% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/106) | 35.9 / 217.3 | 9% |  |
| [479](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/479) | 188.6 / 369.9 | 18% |  |
| [303](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/303) | 111.3 / 271.5 | 8% |  |
| [264](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/264) | 170.9 / 327.1 | 18% |  |
| [371](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/371) | 40.3 / 195.6 | 9% |  |
| [263](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/263) | 26.8 / 174.7 | 13% |  |
| [309](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/309) | 161.5 / 307.9 | 14% |  |

**Gain documents against neutral documents** (8031 features active; 424 differ at q < 0.05; 231 more active in gain, 193 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | 1945.8 / 556.7 | 97% |  |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/316) | 351.3 / 1.8 | 15% | quantifying numbers followed by units |
| [338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/338) | 270.9 / 5.0 | 13% | currency and price ranges |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/285) | 258.4 / 0.0 | 13% | arithmetic operations involving numbers |
| [1229](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1229) | 244.6 / 2.7 | 25% | declines and victory |
| [4697](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4697) | 227.8 / 2.4 | 16% | increase or decrease by |
| [18](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/18) | 219.8 / 0.1 | 12% | numbers and fractions |
| [8196](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8196) | 217.1 / 1.5 | 20% | comparing or relating values |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/442) | 381.2 / 171.5 | 34% |  |
| [112](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/112) | 222.1 / 28.4 | 12% |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/387) | 191.2 / 7.1 | 9% | mg/kg dosage |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 168.9 / 11.3 | 25% |  |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [2010](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2010) | 586.5 / 1669.9 | 92% |  |
| [325](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/325) | 171.9 / 496.2 | 20% |  |
| [296](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/296) | 22.4 / 327.6 | 20% |  |
| [4372](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4372) | 30.5 / 317.4 | 46% | cost, exam, errors, amount |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/227) | 124.2 / 379.4 | 28% |  |
| [479](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/479) | 116.3 / 369.9 | 18% |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/543) | 30.1 / 260.1 | 12% |  |
| [309](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/309) | 93.8 / 307.9 | 14% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/106) | 13.9 / 217.3 | 9% |  |
| [303](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/303) | 69.4 / 271.5 | 8% |  |
| [484](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/484) | 79.3 / 249.6 | 8% |  |
| [264](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/264) | 157.7 / 327.1 | 18% |  |

**Loss documents against gain documents** (7785 features active; 0 differ at q < 0.05; 0 more active in loss, 0 in gain)

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 34 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 0 point the same way (about 0.1 expected by chance) and 0 the opposite way. Correlation of the two differences over the 425 features active in both: -0.00.


## Layer 41

**Loss documents against neutral documents** (9992 features active; 197 differ at q < 0.05; 117 more active in loss, 80 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 4045.2 / 1441.4 | 90% | market economics |
| [6929](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6929) | 1171.8 / 74.3 | 64% | copy/paste |
| [469](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/469) | 687.5 / 36.1 | 9% |  |
| [3964](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3964) | 653.8 / 16.0 | 27% |  |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 667.5 / 30.6 | 11% | say "ed" ending |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | 482.4 / 41.9 | 24% | outperform others |
| [374](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/374) | 437.6 / 7.9 | 9% | state verbs |
| [130](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/130) | 518.1 / 94.5 | 21% |  |
| [453](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/453) | 443.5 / 25.7 | 17% |  |
| [504](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/504) | 829.9 / 427.1 | 20% |  |
| [610](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/610) | 369.8 / 5.4 | 5% | numerical quantities and units |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 335.3 / 3.9 | 13% |  |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/413) | 722.8 / 1475.1 | 23% |  |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/524) | 766.9 / 1410.0 | 37% | types or categories |
| [287](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/287) | 15.9 / 631.9 | 30% | andMethod used: 1Reason: All MAX_ACTIVATING_TOKENS are the word "and" |
| [417](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/417) | 150.0 / 682.9 | 20% |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/543) | 221.2 / 647.0 | 21% | listing punctuation |
| [471](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/471) | 294.5 / 709.5 | 16% |  |
| [309](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/309) | 418.1 / 781.0 | 17% |  |
| [133](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/133) | 267.3 / 615.8 | 12% |  |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/128) | 77.7 / 426.1 | 29% |  |
| [479](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/479) | 10.4 / 312.2 | 5% |  |
| [193](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/193) | 29.3 / 291.2 | 12% |  |
| [8](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8) | 159.7 / 421.0 | 8% | actions and functions |

**Gain documents against neutral documents** (10274 features active; 443 differ at q < 0.05; 271 more active in gain, 172 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 4160.6 / 1441.4 | 87% | market economics |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | 1201.8 / 41.9 | 49% | outperform others |
| [2136](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2136) | 1243.8 / 151.4 | 56% | year-over-year financial metrics |
| [6929](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6929) | 1038.9 / 74.3 | 57% | copy/paste |
| [469](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/469) | 853.0 / 36.1 | 13% |  |
| [610](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/610) | 495.0 / 5.4 | 8% | numerical quantities and units |
| [504](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/504) | 913.8 / 427.1 | 20% |  |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 512.6 / 30.6 | 8% | say "ed" ending |
| [6961](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6961) | 506.6 / 68.2 | 25% | :** |
| [2294](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2294) | 442.9 / 25.2 | 30% | current events |
| [1623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1623) | 411.9 / 8.6 | 20% | increase |
| [445](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/445) | 377.9 / 0.2 | 11% | numbers |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [7808](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7808) | 240.0 / 2098.8 | 62% | the |
| [413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/413) | 570.7 / 1475.1 | 23% |  |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/524) | 552.9 / 1410.0 | 37% | types or categories |
| [287](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/287) | 18.9 / 631.9 | 30% | andMethod used: 1Reason: All MAX_ACTIVATING_TOKENS are the word "and" |
| [417](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/417) | 79.9 / 682.9 | 20% |  |
| [471](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/471) | 192.3 / 709.5 | 16% |  |
| [309](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/309) | 272.1 / 781.0 | 17% |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/543) | 191.6 / 647.0 | 21% | listing punctuation |
| [133](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/133) | 204.3 / 615.8 | 12% |  |
| [393](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/393) | 269.7 / 661.1 | 19% |  |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/128) | 38.4 / 426.1 | 29% |  |
| [8](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8) | 51.4 / 421.0 | 8% | actions and functions |

**Loss documents against gain documents** (9900 features active; 6 differ at q < 0.05; 3 more active in loss, 3 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [130](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/130) | 518.1 / 89.3 | 21% |  |
| [453](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/453) | 443.5 / 43.1 | 17% |  |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | 176.2 / 33.6 | 11% |  |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | 482.4 / 1201.8 | 49% | outperform others |
| [1623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1623) | 85.1 / 411.9 | 20% | increase |
| [1412](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1412) | 40.3 / 255.1 | 17% |  |

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 29 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 0 point the same way (about 0.1 expected by chance) and 0 the opposite way. Correlation of the two differences over the 514 features active in both: +0.08.


# Read by the agent itself

The same documents placed at the start of UBS's request update in B's neutral careers (60 requests, one document of each type per request, as in the priming run), so that “you” and “we” are the agent and its desk. While reading: each feature's mean activation over the document's tokens. At the decision: the last token before the agent's reply, against the same moment with no document. Paired within the request; p flips the sign of each request's difference. **Personal:** for blame against loss and credit against gain (the “you” in each), the features that differ when the agent reads the document in its own career but not when it reads it on its own.


## Layer 12, read by the agent

**Reading: loss against neutral** (7672 features active; 4051 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 55.5 / 15.0 |  |
| [1042](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1042) | 97.6 / 64.8 | finance and economic volatility |
| [2503](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2503) | 34.2 / 1.6 | growth patterns |
| [7188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7188) | 67.4 / 37.1 | chn |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/420) | 24.1 / 0.2 |  |
| [12](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/12) | 29.7 / 6.4 | ' followed by 't' or 'm' |
| [258](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/258) | 30.6 / 9.5 |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 26.4 / 6.4 |  |
| [217](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/217) | 18.9 / 0.6 |  |
| [163](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/163) | 22.9 / 5.2 |  |
| [659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/659) | 21.0 / 3.3 | mathematical expressions with numbers |
| [2887](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2887) | 26.6 / 9.6 |  |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [267](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/267) | 23.8 / 54.8 |  |
| [647](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/647) | 31.4 / 60.4 |  |
| [510](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/510) | 8.0 / 35.2 |  |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 20.4 / 47.2 |  |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/262) | 7.5 / 33.0 |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/100) | 14.1 / 39.3 |  |
| [619](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/619) | 28.1 / 51.5 |  |
| [402](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/402) | 22.6 / 44.9 |  |
| [656](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/656) | 12.4 / 34.5 | attention scores |
| [10870](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/10870) | 29.2 / 49.9 | banking and finance |
| [357](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/357) | 15.3 / 35.9 |  |
| [7320](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7320) | 7.4 / 27.8 |  |

**Reading: gain against neutral** (7524 features active; 4211 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [2503](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2503) | 49.3 / 1.6 | growth patterns |
| [7188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7188) | 78.1 / 37.1 | chn |
| [1042](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1042) | 105.1 / 64.8 | finance and economic volatility |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/420) | 38.4 / 0.2 |  |
| [217](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/217) | 36.7 / 0.6 |  |
| [12](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/12) | 38.4 / 6.4 | ' followed by 't' or 'm' |
| [163](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/163) | 34.1 / 5.2 |  |
| [258](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/258) | 35.5 / 9.5 |  |
| [659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/659) | 26.0 / 3.3 | mathematical expressions with numbers |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 42.7 / 20.4 |  |
| [10739](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/10739) | 25.1 / 4.9 | technical analysis and prediction |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 51.1 / 31.4 |  |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [267](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/267) | 15.0 / 54.8 |  |
| [647](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/647) | 29.7 / 60.4 |  |
| [510](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/510) | 6.1 / 35.2 |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/100) | 10.7 / 39.3 |  |
| [262](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/262) | 5.2 / 33.0 |  |
| [8818](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8818) | 10.1 / 36.7 | government bonds and securities |
| [619](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/619) | 25.6 / 51.5 |  |
| [402](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/402) | 19.6 / 44.9 |  |
| [656](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/656) | 10.4 / 34.5 | attention scores |
| [437](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/437) | 14.5 / 36.1 |  |
| [7320](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7320) | 6.4 / 27.8 |  |
| [10870](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/10870) | 31.2 / 49.9 | banking and finance |

**Reading: loss against gain** (7325 features active; 2947 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 55.5 / 29.9 |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 14.6 / 0.8 |  |
| [8818](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8818) | 21.1 / 10.1 | government bonds and securities |
| [28](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/28) | 17.9 / 7.4 | will/would followed by verb |
| [472](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/472) | 20.6 / 10.2 |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 26.4 / 17.6 |  |
| [267](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/267) | 23.8 / 15.0 |  |
| [11371](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/11371) | 13.0 / 5.2 | economic downturns and crises |
| [1772](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1772) | 8.7 / 1.6 |  |
| [500](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/500) | 20.9 / 14.0 |  |
| [437](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/437) | 21.1 / 14.5 |  |
| [307](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/307) | 9.4 / 3.1 |  |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 33.1 / 51.1 |  |
| [217](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/217) | 18.9 / 36.7 |  |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 24.9 / 42.7 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 26.8 / 42.4 |  |
| [2503](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2503) | 34.2 / 49.3 | growth patterns |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 20.1 / 34.5 |  |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/420) | 24.1 / 38.4 |  |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | 20.9 / 33.9 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 15.9 / 28.0 |  |
| [250](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/250) | 20.0 / 31.8 |  |
| [163](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/163) | 22.9 / 34.1 |  |
| [826](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/826) | 6.2 / 17.3 |  |

**At the decision: after a neutral document against none** (51 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 57.9 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 47.5 / 12.3 | Here's a breakdown |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 90.7 / 71.7 |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 39.9 / 24.9 |  |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 51.2 / 37.1 | Option 2 |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 80.4 / 67.3 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 255.7 / 243.0 |  |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 127.0 / 114.8 |  |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 2.0 / 24.2 | Instead, nothing |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 0.6 / 20.6 |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 63.0 / 80.0 |  |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 8.6 / 23.6 | `@RestController` |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 15.3 / 27.8 | foreign language text/characters |
| [15474](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15474) | 41.1 / 52.8 | listing categories |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | 6.9 / 17.9 | "said" followed by punctuation or direct speech |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 3.0 / 13.8 |  |

**At the decision: after a loss document against none** (48 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 58.7 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 44.5 / 12.3 | Here's a breakdown |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 48.7 / 24.9 |  |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 92.4 / 71.7 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 262.3 / 243.0 |  |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 85.1 / 67.3 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 247.5 / 231.0 |  |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 20.0 / 4.5 | greetings and thanks |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 57.7 / 80.0 |  |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 2.2 / 20.6 |  |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | 100.4 / 117.0 | ``` |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 11.8 / 27.8 | foreign language text/characters |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | 19.2 / 33.1 | model explanations |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 1.2 / 13.8 |  |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | 5.6 / 17.9 | "said" followed by punctuation or direct speech |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 11.6 / 23.6 | `@RestController` |

**At the decision: after a gain document against none** (48 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 61.6 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 43.5 / 12.3 | Here's a breakdown |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 46.8 / 24.9 |  |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 92.8 / 71.7 |  |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 22.7 / 4.5 | greetings and thanks |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 261.1 / 243.0 |  |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 84.5 / 67.3 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 246.6 / 231.0 |  |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 58.3 / 80.0 |  |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 1.2 / 20.6 |  |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 10.6 / 27.8 | foreign language text/characters |
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 7.7 / 24.2 | Instead, nothing |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | 103.5 / 117.0 | ``` |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | 20.4 / 33.1 | model explanations |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | 5.4 / 17.9 | "said" followed by punctuation or direct speech |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 13.3 / 23.6 | `@RestController` |

**At the decision: after loss against after gain** (10 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | 81.1 / 79.2 |  |
| [2604](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604) | 76.9 / 75.7 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 58.7 / 61.6 | numbers and foreign words |
| [2819](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819) | 69.4 / 71.2 | foreign words or scripts |
| [9499](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9499) | 69.1 / 70.8 | web browser refinements |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8848) | 50.5 / 51.9 | :** |
| [3264](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3264) | 34.2 / 35.5 | Replace with |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 50.1 / 51.2 | Option 2 |
| [978](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/978) | 53.0 / 53.6 |  |
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | 22.0 / 22.6 | code snippets and list items |


## Layer 24, read by the agent

**Reading: loss against neutral** (5187 features active; 2698 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [701](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/701) | 328.5 / 13.9 | reportedly |
| [527](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/527) | 414.1 / 158.7 | India judgment |
| [13109](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13109) | 271.6 / 60.7 | economic conditions and volatility |
| [338](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/338) | 195.7 / 8.6 |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 219.3 / 55.4 |  |
| [1992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1992) | 217.9 / 55.0 |  |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/420) | 212.5 / 51.9 |  |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 323.0 / 164.0 |  |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/111) | 505.8 / 357.1 |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 383.1 / 245.2 |  |
| [3147](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3147) | 217.5 / 84.2 | numbers and statistics |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/249) | 130.3 / 0.9 | 6 |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 120.3 / 382.9 |  |
| [1244](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1244) | 289.0 / 431.2 | and why |
| [271](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/271) | 87.6 / 215.2 |  |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 263.6 / 380.1 | skills and experience |
| [459](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/459) | 116.6 / 227.4 |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/543) | 7.0 / 116.3 | listing conjunctions and examples |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/26) | 88.8 / 174.7 |  |
| [1653](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1653) | 199.8 / 278.8 | of other languages |
| [18](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/18) | 41.8 / 119.5 | any or other |
| [315](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/315) | 111.5 / 184.0 |  |
| [12863](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12863) | 0.6 / 70.4 | science and biology terms |
| [743](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/743) | 10.4 / 78.9 |  |

**Reading: gain against neutral** (5179 features active; 2777 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [338](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/338) | 384.8 / 8.6 |  |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/420) | 336.8 / 51.9 |  |
| [701](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/701) | 285.8 / 13.9 | reportedly |
| [527](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/527) | 398.8 / 158.7 | India judgment |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/277) | 237.8 / 3.3 | foreign language words |
| [3147](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3147) | 303.3 / 84.2 | numbers and statistics |
| [1992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1992) | 273.8 / 55.0 |  |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/249) | 209.2 / 0.9 | 6 |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 351.9 / 164.0 |  |
| [354](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/354) | 190.2 / 7.9 | This neuron detects numeric tokens—values and measurements (e.g., quantities, statistics, or other numbers) in the text. |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/111) | 511.6 / 357.1 |  |
| [13109](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13109) | 213.2 / 60.7 | economic conditions and volatility |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 139.5 / 382.9 |  |
| [1244](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1244) | 269.1 / 431.2 | and why |
| [459](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/459) | 92.2 / 227.4 |  |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 250.9 / 380.1 | skills and experience |
| [271](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/271) | 87.8 / 215.2 |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/543) | 9.2 / 116.3 | listing conjunctions and examples |
| [1653](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1653) | 176.6 / 278.8 | of other languages |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/26) | 82.1 / 174.7 |  |
| [18](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/18) | 32.2 / 119.5 | any or other |
| [315](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/315) | 100.7 / 184.0 |  |
| [538](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/538) | 39.2 / 118.7 | groups of people or entities |
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 261.7 / 340.0 |  |

**Reading: loss against gain** (5129 features active; 1864 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [13109](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13109) | 271.6 / 213.2 | economic conditions and volatility |
| [11296](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11296) | 58.0 / 9.1 | collapse, demise, destruction, loss |
| [701](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/701) | 328.5 / 285.8 | reportedly |
| [13457](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13457) | 43.4 / 2.6 | negative sentiment |
| [5230](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5230) | 45.9 / 5.9 |  |
| [8620](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8620) | 48.0 / 8.9 | chickenpox and related health emergencies |
| [4005](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4005) | 107.7 / 68.8 | needs access |
| [1090](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1090) | 73.1 / 37.7 | voice cloning or woolens |
| [7285](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7285) | 36.4 / 2.2 | cancel, remove, delete |
| [11564](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11564) | 33.6 / 1.6 | negative connotation |
| [1735](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1735) | 54.9 / 23.2 | legal and technical requirements |
| [11165](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11165) | 145.9 / 114.9 | HTTP URL |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [338](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/338) | 195.7 / 384.8 |  |
| [420](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/420) | 212.5 / 336.8 |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/277) | 127.0 / 237.8 | foreign language words |
| [498](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/498) | 59.7 / 166.3 |  |
| [3147](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3147) | 217.5 / 303.3 | numbers and statistics |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/249) | 130.3 / 209.2 | 6 |
| [139](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/139) | 88.9 / 152.6 | currency amounts with commas |
| [354](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/354) | 132.8 / 190.2 | This neuron detects numeric tokens—values and measurements (e.g., quantities, statistics, or other numbers) in the text. |
| [358](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/358) | 16.4 / 73.6 | closing quotes or list items |
| [1992](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1992) | 217.9 / 273.8 |  |
| [28](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/28) | 37.7 / 84.4 | digits followed by operators and symbols |
| [53](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/53) | 92.6 / 138.1 | yòng, bork, amah, k |

**At the decision: after a neutral document against none** (99 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1184.1 / 555.0 |  |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 653.6 / 221.9 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2114.6 / 1708.7 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1036.9 / 789.4 |  |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | 3521.9 / 3285.3 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 916.3 / 689.7 |  |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 654.7 / 445.7 |  |
| [7925](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7925) | 299.1 / 119.9 | keywords, sentiment, action extraction |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 77.4 / 289.1 | completion and progress |
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 203.1 / 385.1 | numbered lists |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 313.1 / 447.9 | 2 |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | 41.6 / 158.2 | current news or state |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406) | 37.8 / 144.4 |  |
| [10617](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10617) | 0.0 / 90.3 | mathematical expressions or results |
| [3328](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3328) | 0.0 / 87.5 |  |
| [9558](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9558) | 49.9 / 136.0 | immediate, quickly, instantly |

**At the decision: after a loss document against none** (119 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1418.5 / 555.0 |  |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 978.6 / 221.9 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1292.4 / 689.7 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2264.1 / 1708.7 |  |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | 4377.8 / 3938.1 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1160.4 / 789.4 |  |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | 577.2 / 210.0 | sequential listing or numbering |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | 3642.8 / 3285.3 |  |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 51.2 / 385.1 | numbered lists |
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3717) | 96.0 / 276.5 | explanation, sentence, or list |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 131.3 / 289.1 | completion and progress |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406) | 0.0 / 144.4 |  |
| [2704](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2704) | 40.4 / 163.1 | brand availability |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | 8.4 / 122.6 | protect, security, protected |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 496.4 / 609.4 | starting lists |
| [11000](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11000) | 78.6 / 171.9 | numbered lists |

**At the decision: after a gain document against none** (106 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1323.8 / 555.0 |  |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 833.3 / 221.9 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1205.7 / 689.7 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2203.7 / 1708.7 |  |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | 4338.7 / 3938.1 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1110.6 / 789.4 |  |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | 3592.6 / 3285.3 |  |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | 510.1 / 210.0 | sequential listing or numbering |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 72.8 / 385.1 | numbered lists |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406) | 0.0 / 144.4 |  |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 146.0 / 289.1 | completion and progress |
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3717) | 133.9 / 276.5 | explanation, sentence, or list |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | 32.6 / 158.2 | current news or state |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | 0.0 / 122.6 | protect, security, protected |
| [11105](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11105) | 360.5 / 460.8 | language connectors and continuations |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 517.9 / 609.4 | starting lists |

**At the decision: after loss against after gain** (40 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 978.6 / 833.3 |  |
| [14765](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14765) | 213.1 / 85.5 | philosophy and principles |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | 222.1 / 95.4 | nevertheless |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1418.5 / 1323.8 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1292.4 / 1205.7 |  |
| [4473](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4473) | 240.8 / 166.9 |  |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | 577.2 / 510.1 | sequential listing or numbering |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2264.1 / 2203.7 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [869](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/869) | 3.5 / 79.6 |  |
| [5082](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5082) | 4.4 / 68.7 |  |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4368) | 67.3 / 116.6 | Anything interesting, what's new |
| [3166](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3166) | 49.0 / 94.6 | above, foregoing, just now |
| [14235](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235) | 114.6 / 149.7 | examples, interesting, or features |
| [2704](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2704) | 40.4 / 73.7 | brand availability |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 496.4 / 517.9 | starting lists |
| [13799](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799) | 103.4 / 122.8 |  |


## Layer 31, read by the agent

**Reading: loss against neutral** (8352 features active; 4220 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | 1434.5 / 436.3 |  |
| [7492](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7492) | 784.9 / 254.8 | operating income and profit |
| [2453](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2453) | 443.4 / 26.8 |  |
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 383.0 / 0.1 |  |
| [5500](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5500) | 366.4 / 29.7 | reflects ongoing |
| [13882](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13882) | 351.4 / 20.0 | financial collapse and Enron |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 660.6 / 404.1 | stocks and asset prices |
| [2261](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2261) | 276.3 / 20.4 | aid to Ukraine |
| [342](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/342) | 315.5 / 80.2 |  |
| [338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/338) | 221.0 / 4.8 | currency and price ranges |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/316) | 201.6 / 1.9 | quantifying numbers followed by units |
| [4697](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4697) | 199.5 / 1.2 | increase or decrease by |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [2010](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2010) | 947.1 / 1657.9 |  |
| [9551](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9551) | 474.7 / 835.4 |  |
| [19](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/19) | 219.4 / 468.4 | absence or presence |
| [9548](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9548) | 120.3 / 353.0 | holding or selling stock |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/543) | 44.8 / 266.6 |  |
| [325](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/325) | 159.0 / 375.1 |  |
| [2732](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2732) | 63.6 / 272.9 | financial accounting |
| [296](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/296) | 16.2 / 224.7 |  |
| [612](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/612) | 270.3 / 475.9 |  |
| [4372](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4372) | 44.8 / 248.0 | cost, exam, errors, amount |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/227) | 53.5 / 255.4 |  |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/249) | 526.6 / 704.1 |  |

**Reading: gain against neutral** (8520 features active; 4442 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | 1837.6 / 436.3 |  |
| [7492](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7492) | 838.2 / 254.8 | operating income and profit |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/316) | 336.0 / 1.9 | quantifying numbers followed by units |
| [2453](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2453) | 352.1 / 26.8 |  |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11781) | 360.5 / 81.1 | companies and financial growth |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 683.0 / 404.1 | stocks and asset prices |
| [338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/338) | 282.7 / 4.8 | currency and price ranges |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/285) | 269.4 / 0.2 | arithmetic operations involving numbers |
| [18](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/18) | 262.7 / 0.8 | numbers and fractions |
| [2261](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2261) | 281.0 / 20.4 | aid to Ukraine |
| [5500](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5500) | 289.3 / 29.7 | reflects ongoing |
| [4697](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4697) | 216.5 / 1.2 | increase or decrease by |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [2010](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2010) | 731.5 / 1657.9 |  |
| [9551](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9551) | 414.0 / 835.4 |  |
| [19](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/19) | 205.7 / 468.4 | absence or presence |
| [2732](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2732) | 16.6 / 272.9 | financial accounting |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/543) | 28.0 / 266.6 |  |
| [612](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/612) | 238.9 / 475.9 |  |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/249) | 469.3 / 704.1 |  |
| [9548](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9548) | 125.5 / 353.0 | holding or selling stock |
| [4372](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4372) | 27.6 / 248.0 | cost, exam, errors, amount |
| [325](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/325) | 158.2 / 375.1 |  |
| [296](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/296) | 15.4 / 224.7 |  |
| [479](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/479) | 91.6 / 281.8 |  |

**Reading: loss against gain** (8308 features active; 2966 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 383.0 / 16.9 |  |
| [13882](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13882) | 351.4 / 52.0 | financial collapse and Enron |
| [2010](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2010) | 947.1 / 731.5 |  |
| [15024](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15024) | 230.0 / 54.7 | depreciation, expense, or loss calculations |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 170.1 / 16.8 |  |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 194.2 / 47.5 | crises and disasters |
| [7380](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7380) | 141.8 / 17.7 | bankruptcy, insolvency, liquidation |
| [14685](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14685) | 192.3 / 94.1 |  |
| [8604](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8604) | 123.9 / 36.2 | reduction or cuts |
| [8848](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8848) | 81.6 / 1.7 | negative values or operations |
| [5500](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5500) | 366.4 / 289.3 | reflects ongoing |
| [479](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/479) | 164.5 / 91.6 |  |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | 1434.5 / 1837.6 |  |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/285) | 128.4 / 269.4 | arithmetic operations involving numbers |
| [7496](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7496) | 120.6 / 260.5 | finance and regulation |
| [316](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/316) | 201.6 / 336.0 | quantifying numbers followed by units |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11781) | 228.5 / 360.5 | companies and financial growth |
| [10074](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10074) | 290.1 / 416.6 | bank transactions and accounts |
| [14262](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14262) | 29.2 / 142.2 |  |
| [1519](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1519) | 53.3 / 164.1 |  |
| [1523](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1523) | 27.6 / 129.2 |  |
| [10957](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10957) | 122.8 / 220.6 | liquidity and cash flow metrics |
| [8303](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8303) | 156.7 / 248.3 | gold, silver, metallic items |
| [18](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/18) | 171.2 / 262.7 | numbers and fractions |

**At the decision: after a neutral document against none** (118 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 2284.1 / 1118.7 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2015.0 / 1356.0 |  |
| [2809](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2809) | 563.0 / 31.1 |  |
| [12382](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12382) | 730.5 / 205.1 | text explicitly mentions |
| [9397](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397) | 884.9 / 380.7 | refusals to inappropriate requests |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 1052.3 / 628.0 |  |
| [6617](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6617) | 540.3 / 132.7 |  |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | 1242.0 / 876.9 |  |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 216.7 / 860.6 |  |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 347.8 / 941.9 |  |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 298.6 / 860.3 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 346.6 / 879.2 | stocks and asset prices |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | 214.5 / 717.9 | the definite article |
| [4056](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4056) | 107.8 / 579.4 |  |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 544.2 / 984.6 |  |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | 14.5 / 440.8 | providing specific examples |

**At the decision: after a loss document against none** (171 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 2943.8 / 1118.7 |  |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2355.5 / 628.0 |  |
| [1238](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1238) | 1435.8 / 229.3 |  |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | 1244.9 / 70.2 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2400.9 / 1356.0 |  |
| [95](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/95) | 1070.5 / 213.1 |  |
| [5287](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5287) | 831.5 / 43.9 | sounds |
| [12382](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12382) | 974.1 / 205.1 | text explicitly mentions |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 27.8 / 941.9 |  |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 73.6 / 984.6 |  |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 7.9 / 860.6 |  |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 880.7 / 1713.3 | punctuation and common abbreviations |
| [470](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/470) | 25.2 / 803.0 |  |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | 28.6 / 717.9 | the definite article |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | 135.3 / 819.6 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 296.4 / 879.2 | stocks and asset prices |

**At the decision: after a gain document against none** (160 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2116.6 / 628.0 |  |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 2474.4 / 1118.7 |  |
| [1238](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1238) | 1579.9 / 229.3 |  |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | 997.5 / 70.2 |  |
| [95](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/95) | 1083.2 / 213.1 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2212.0 / 1356.0 |  |
| [1293](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1293) | 956.4 / 143.3 | meanwhile, elsewhere, continuing |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | 3320.6 / 2660.0 |  |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 73.5 / 941.9 |  |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 27.4 / 860.6 |  |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 200.4 / 984.6 |  |
| [470](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/470) | 53.0 / 803.0 |  |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | 140.7 / 819.6 |  |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | 48.1 / 717.9 | the definite article |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 1070.0 / 1713.3 | punctuation and common abbreviations |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 277.7 / 860.3 |  |

**At the decision: after loss against after gain** (100 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [1450](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1450) | 811.1 / 190.9 |  |
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 512.1 / 38.8 |  |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 2943.8 / 2474.4 |  |
| [4471](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4471) | 648.3 / 302.3 |  |
| [6294](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6294) | 557.0 / 288.1 | **Explanation of Neuron Behavior**The neuron is primarily associated with the act of receiving something, often an item, payment, or message. The context implies successful acquisition or arrival.- `MAX_ACTIVATING_TOKENS`: `received`, `Receiving`, `received`, `arrived`, `orders`. The consistent theme is "receiving" or "arriving".- `TOKENS_AFTER_MAX_ACTIVATING_TOKEN`: `my`, `the`, `payment`, `unexpectedly`, `directly`. These specify what is received ("my item", "the payment") or how ("unexpectedly", "directly").- `TOP_POSITIVE_LOGITS`: `received`, `received`, `Received`, `recieved`, `incoming`, `Received`, `Receive`, `receb`, `收到`, `recibido`. This overwhelmingly reinforces "received" and similar concepts across languages.- `TOP_ACTIVATING_TEXTS`: Look for sentences where these verbs appear. Examples: "I never received my item", "I never received a refund", "received the ticket", "haven't yet received payment".The pattern is very strong: the neuron fires when it observes the act of receiving, often followed by the object being received or how it arrived.The most specific and encompassing pattern is the act of receiving itself.Possible phrases:- receiving items or payments- acquisition of items- incoming transactions- receipt of goods or information- receivingConsidering the instructions:- Concise (3 to 20 words): Yes.- Single word, phrase, or pattern: Yes.- About tokens following/preceding: Yes, implicitly.- About words starting with sequence: Not directly applicable here.- Avoid listing all tokens: Yes.- Just say the pattern: Yes.- No "words related to", etc.: Yes.- No "This neuron detects/predicts": Yes.- No "tokens" or "patterns": Yes.- Not capitalize first letter unless proper noun: Yes.- Specific: Yes.- Majority should match: Yes, the majority strongly match.- If cannot guess, return first MAX_ACTIVATING_TOKEN: Not needed.Let's refine. "received" is too short. "receiving items or payments" is good. "incoming data" is another option. "receipt of goods" is also good.Looking at `orders` in MAX_ACTIVATING_TOKENS and `directly` in TOKENS_AFTER_MAX_ACTIVATING_TOKEN, it might relate to fulfilling orders or receiving them directly. However, the vast majority are about `received`."received payments" fits well. "receiving goods/payments" is also fitting. "item received" or "payment received" are good.Let's try to find the most salient aspect. The raw logs are `received`, `arrived`. The follow-ups are `my`, `the`, `payment`. The positive logits are all `received` variants.The core is the *act of receiving*.Considering the examples:- "I never received my item" -> receiving item- "I never received a refund" -> receiving refund- "received the ticket" -> receiving ticket- "haven't yet received payment" -> receiving payment- "arrived unexpectedly" -> arriving unexpectedly (related to receiving)- "take orders directly" -> receiving orders (from the customer's perspective)The neuron seems to capture the event of something arriving or being successfully acquired. "receiving" is the verb."receiving items or payments" captures it well.Maybe simpler? "item or payment received".Let's re-read the prompt carefully: "what the neuron detects or predicts *by finding patterns in lists*." and "explanation could be about tokens following or *preceding* certain tokens." (though we have tokens *after*).The neuron is heavily weighted on "received". The common things received are items and payments.How about: "items or payments received"? This is 4 words, specific."receiving items and payments" is 4 words.Let's look at the top logits again:`received`, `recieved`, `incoming`, `Receive`, `recibido`, `收到`. All point to reception.The explanation should ideally capture the *intent* or *classification* that the neuron provides. It's not just any "receiving", but receiving specific things common in transactions or communications."incoming transactions" - a bit too broad, doesn't fit "ticket"."item acquisition" - fits."payment acquisition" - fits.Let's stick to the most common elements.Items and payments are very common themes in the examples. "ticket" is also present."receiving items, payments, tickets" is a bit long."receiving transactional items" - maybe?What if the neuron is simply about *completion* of an action involving receiving?"item or payment received" is good.Let's consider "arrived" and "orders". If the neuron means "things that have arrived or are ordered", it's a bit different. But `received` is so dominant.The prompt asks for what it *detects or predicts*.It detects the state of having received something."received item or payment""item or payment received"The instruction "Do not mention 'tokens' or 'patterns'" is key.I need to state *what it is*, not *how I found it*."receiving incoming data" - maybe too general."act of receiving" - too general.Let's go with the specific nouns that appear most often in the context of being received.Items, payments, refunds, tickets."receiving items and payments" seems like a strong candidate. It's 4 words. It's specific. It covers the majority of cases derived from the lists.Let's consider the original MAX_ACTIVATING_TOKENS: `received`, `Receiving`, `received`, `arrived`, `orders`.The `orders` token is a bit of an anomaly if we focus purely on "receiving". However, in a transactional context, receiving orders and receiving payment for orders are closely linked.If the neuron detects "orders", what follows? `directly`. "orders directly". This fits the e-commerce example: "take orders directly through WhatsApp".This means the neuron might be about *transactions*, specifically things that are received or ordered.Let's re-examine the `TOP_ACTIVATING_TEXTS`.- "I never received my item and i never received a refund." -> `received item`, `received refund`.- "I never received the item and never received refund." -> `received item`, `received refund`.- "what to do immediately after receiving the ticket" |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | 674.5 / 421.1 | sudden event |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | 262.3 / 10.0 |  |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | 1244.9 / 997.5 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | 409.2 / 733.1 |  |
| [12126](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12126) | 0.0 / 263.5 |  |
| [6755](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6755) | 0.0 / 260.1 | news and recent news |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 0.0 / 218.5 |  |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 25.7 / 242.9 | praise and awards |
| [6006](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6006) | 18.5 / 235.1 |  |
| [7963](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7963) | 168.2 / 382.8 | country names and nationalities |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 500.3 / 710.6 | exclamations of strong positive emotion |


## Layer 41, read by the agent

**Reading: loss against neutral** (10985 features active; 4882 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 3700.4 / 1228.8 | market economics |
| [6929](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6929) | 1234.7 / 65.4 | copy/paste |
| [10414](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10414) | 1402.0 / 389.2 |  |
| [11745](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11745) | 1064.2 / 115.2 | bankruptcy |
| [8441](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8441) | 956.9 / 155.7 | investors and sentiment |
| [2294](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2294) | 714.5 / 53.6 | current events |
| [2136](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2136) | 696.8 / 130.9 | year-over-year financial metrics |
| [469](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/469) | 552.4 / 36.4 |  |
| [3964](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3964) | 514.4 / 13.8 |  |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 514.0 / 24.4 | say "ed" ending |
| [5301](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5301) | 430.9 / 3.3 | degree of change |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/106) | 2162.9 / 1740.3 | Financial terms |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [7808](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7808) | 1036.1 / 2324.1 | the |
| [1437](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1437) | 1146.6 / 2006.1 |  |
| [413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/413) | 588.0 / 1217.0 |  |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | 265.4 / 803.9 | transactions, payments |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/524) | 574.1 / 1072.1 | types or categories |
| [417](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/417) | 116.5 / 580.4 |  |
| [287](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/287) | 25.9 / 489.4 | andMethod used: 1Reason: All MAX_ACTIVATING_TOKENS are the word "and" |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/543) | 212.3 / 667.5 | listing punctuation |
| [15914](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15914) | 95.6 / 498.4 | regulatory, supervision |
| [2806](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2806) | 89.4 / 451.1 |  |
| [309](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/309) | 323.5 / 662.3 |  |
| [471](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/471) | 242.3 / 576.1 |  |

**Reading: gain against neutral** (11067 features active; 5111 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 3919.3 / 1228.8 | market economics |
| [2136](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2136) | 1257.4 / 130.9 | year-over-year financial metrics |
| [6929](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6929) | 1190.9 / 65.4 | copy/paste |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | 962.1 / 22.2 | outperform others |
| [10414](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10414) | 1253.0 / 389.2 |  |
| [8441](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8441) | 1010.2 / 155.7 | investors and sentiment |
| [469](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/469) | 749.6 / 36.4 |  |
| [2294](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2294) | 723.1 / 53.6 | current events |
| [610](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/610) | 552.9 / 5.1 | numerical quantities and units |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 1038.0 / 573.1 |  |
| [1623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1623) | 458.5 / 11.0 | increase |
| [5301](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5301) | 436.0 / 3.3 | degree of change |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [7808](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7808) | 515.2 / 2324.1 | the |
| [1437](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1437) | 1040.3 / 2006.1 |  |
| [413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/413) | 496.8 / 1217.0 |  |
| [524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/524) | 417.7 / 1072.1 | types or categories |
| [698](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/698) | 249.2 / 803.9 | transactions, payments |
| [417](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/417) | 65.9 / 580.4 |  |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 1490.6 / 1995.5 |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/543) | 173.7 / 667.5 | listing punctuation |
| [287](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/287) | 28.4 / 489.4 | andMethod used: 1Reason: All MAX_ACTIVATING_TOKENS are the word "and" |
| [309](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/309) | 208.3 / 662.3 |  |
| [471](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/471) | 163.2 / 576.1 |  |
| [2806](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2806) | 43.2 / 451.1 |  |

**Reading: loss against gain** (10828 features active; 3601 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [11745](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11745) | 1064.2 / 155.6 | bankruptcy |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/106) | 2162.9 / 1538.0 | Financial terms |
| [7808](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7808) | 1036.1 / 515.2 | the |
| [3964](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3964) | 514.4 / 51.0 |  |
| [130](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/130) | 409.2 / 70.7 |  |
| [2243](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2243) | 853.6 / 518.7 | monetary policy |
| [453](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/453) | 371.2 / 47.3 |  |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1899.0 / 1610.4 | asking questions |
| [11422](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11422) | 437.9 / 158.2 | accounting terms |
| [3214](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3214) | 471.3 / 204.1 | mergers and acquisitions |
| [1275](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1275) | 393.1 / 127.1 | Here |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 1725.0 / 1490.6 |  |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | 354.0 / 962.1 | outperform others |
| [2136](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2136) | 696.8 / 1257.4 | year-over-year financial metrics |
| [1623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1623) | 87.1 / 458.5 | increase |
| [8254](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8254) | 992.6 / 1232.7 | branch wealth |
| [11080](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11080) | 96.8 / 322.9 | dividends fundamentals |
| [445](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/445) | 166.5 / 383.1 | numbers |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 824.2 / 1038.0 |  |
| [1412](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1412) | 35.1 / 242.0 |  |
| [469](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/469) | 552.4 / 749.6 |  |
| [3566](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3566) | 52.9 / 247.9 |  |
| [610](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/610) | 382.4 / 552.9 | numerical quantities and units |
| [4062](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4062) | 285.4 / 446.3 |  |

**At the decision: after a neutral document against none** (124 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 9957.6 / 7769.5 |  |
| [1163](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1163) | 1778.1 / 229.2 | provides information |
| [3296](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3296) | 2132.9 / 734.0 | seeing, knowing, hearing |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 2393.1 / 1231.0 |  |
| [5548](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5548) | 1184.1 / 73.1 |  |
| [753](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/753) | 1124.8 / 17.7 |  |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | 1770.9 / 731.4 | given |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 2081.7 / 1047.3 |  |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 226.1 / 1509.2 |  |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 515.2 / 1569.8 |  |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 1265.9 / 2215.6 | market economics |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | 128.4 / 984.7 | consumer |
| [4647](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4647) | 63.2 / 800.6 | scientific components |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | 690.3 / 1403.3 | inflation commodity market |
| [2162](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2162) | 147.2 / 856.6 | operation outcome |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | 168.8 / 856.9 |  |

**At the decision: after a loss document against none** (181 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [1867](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1867) | 4151.2 / 185.1 |  |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 11223.4 / 7769.5 |  |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 4442.9 / 1231.0 |  |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | 2554.7 / 500.9 |  |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 2867.2 / 1047.3 |  |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | 2367.2 / 731.4 | given |
| [1163](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1163) | 1801.2 / 229.2 | provides information |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 2992.4 / 1646.1 |  |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | 127.1 / 2035.8 |  |
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | 3235.6 / 4938.0 |  |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 13.6 / 1569.8 |  |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 21.2 / 1509.2 |  |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | 330.5 / 1703.5 | sentence starters |
| [1734](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1734) | 206.5 / 1567.9 | say "s" words |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | 237.2 / 1442.9 | say Okay |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | 121.1 / 1291.3 | linking words |

**At the decision: after a gain document against none** (189 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [1867](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1867) | 3639.4 / 185.1 |  |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 10788.7 / 7769.5 |  |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 4047.9 / 1231.0 |  |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 2489.5 / 202.1 | intensity |
| [1102](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1102) | 1793.3 / 12.2 | good |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | 2157.4 / 500.9 |  |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 3789.4 / 2215.6 | market economics |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 1406.5 / 0.0 |  |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | 3158.9 / 4938.0 |  |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | 372.0 / 2035.8 |  |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 15.0 / 1569.8 |  |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | 1954.1 / 3382.2 |  |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 123.3 / 1509.2 |  |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 3374.7 / 4686.0 |  |
| [7303](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7303) | 360.8 / 1563.4 | U |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | 271.7 / 1442.9 | say Okay |

**At the decision: after loss against after gain** (148 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 1353.5 / 209.2 |  |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 2992.4 / 1970.8 |  |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 4288.0 / 3374.7 |  |
| [1002](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1002) | 1608.7 / 718.0 |  |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | 2367.2 / 1504.0 | given |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 2867.2 / 2059.3 |  |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | 1438.1 / 646.9 | say this |
| [2979](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2979) | 1186.8 / 472.7 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [1102](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1102) | 29.5 / 1793.3 | good |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 1436.5 / 2489.5 | intensity |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 3037.7 / 3789.4 | market economics |
| [325](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/325) | 374.4 / 1070.8 |  |
| [6961](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6961) | 306.3 / 959.5 | :** |
| [10835](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10835) | 0.0 / 633.3 | congratulations |
| [13576](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13576) | 0.0 / 613.7 | positive |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | 1419.0 / 2016.5 | inflation commodity market |


# Does reading a document move the decision toward going along?

At each of the requests above, the agent's raw state at its decision (layer 24) after reading each document, projected on the going-along direction (agents that went along minus those that did not, within request, experiment and framing, from the other half of the careers). Units: 1 = the full gap between agents that went along and agents that did not. Paired within the request; p flips signs by career (10,000 times).

| Document | Against no document | p | Against the neutral document | p |
|---|---|---|---|---|
| neutral | +3.665 | 0.0025 | – | – |
| loss | +5.279 | 0.0018 | +1.614 | 0.0659 |
| gain | +4.818 | 0.0019 | +1.152 | 0.1009 |
