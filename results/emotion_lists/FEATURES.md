# What the emotion documents activate inside the model (exploratory)

80 documents (loss 16, blame 16, gain 16, credit 16, neutral 16), each read on its own by Gemma 3 12B (bfloat16). Every token's state passed through the Gemma Scope 2 dictionary (16k, residual stream); a document's activation of a feature is its mean over the document's tokens. p reshuffles which documents belong to which type (2,000 times, read off a normal fitted to the reshuffled differences); q is false-discovery corrected over the features active in either type. Names are Neuronpedia's automatic descriptions where it has one; every feature links to its page. Produced by `designs/rd2/analysis/emotion_features.py`.


## Layer 12

**Loss documents against neutral documents** (6479 features active; 2719 differ at q < 0.05; 1445 more active in loss, 1274 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 121.2 / 1.2 | 36% |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 78.9 / 0.1 | 29% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 66.5 / 0.0 | 26% |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 82.3 / 20.1 | 26% | formatting characters |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 60.5 / 1.5 | 19% |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 58.4 / 3.6 | 32% |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 153.9 / 101.6 | 27% |  |
| [1856](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1856) | 48.4 / 0.0 | 74% |  |
| [15622](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15622) | 43.6 / 4.1 | 60% |  |
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 161.3 / 125.4 | 27% |  |
| [1126](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1126) | 46.8 / 12.9 | 35% | processing, end, old, love, follow, now |
| [90](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/90) | 32.3 / 0.5 | 16% |  |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 1.4 / 168.9 | 43% |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 3.1 / 85.2 | 32% |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 24.2 / 105.3 | 20% |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 14.6 / 95.6 | 17% |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 14.3 / 52.1 | 6% |  |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.5 / 37.1 | 38% |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 1.5 / 37.7 | 29% |  |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.6 / 35.1 | 11% | places, homes, workshops |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 9.7 / 41.2 | 7% | the repetition or challenge |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 0.6 / 29.7 | 17% |  |
| [4061](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4061) | 0.0 / 27.6 | 41% | likelihood of objects |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 7.0 / 34.3 | 12% |  |

**Blame documents against neutral documents** (6490 features active; 2643 differ at q < 0.05; 1303 more active in blame, 1340 in neutral)

| More active in blame | Activation (blame / neutral) | Share of blame tokens on | Description |
|---|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 86.1 / 1.2 | 28% |  |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 81.6 / 0.9 | 22% | their |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 71.8 / 0.0 | 13% | you can or should |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 68.7 / 0.0 | 15% |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 53.5 / 0.1 | 20% |  |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 52.8 / 0.1 | 35% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 49.4 / 0.0 | 20% |  |
| [1856](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1856) | 46.0 / 0.0 | 69% |  |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 40.4 / 1.5 | 12% |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 40.7 / 3.6 | 29% |  |
| [15622](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15622) | 40.7 / 4.1 | 59% |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 56.5 / 20.1 | 18% | formatting characters |

| More active in neutral | Activation (blame / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 0.3 / 168.9 | 43% |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 13.5 / 105.3 | 20% |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 1.0 / 85.2 | 32% |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 15.9 / 95.6 | 17% |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 4.4 / 52.1 | 6% |  |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 0.9 / 41.2 | 7% | the repetition or challenge |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.4 / 37.1 | 38% |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 1.2 / 37.7 | 29% |  |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.3 / 35.1 | 11% | places, homes, workshops |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 0.2 / 29.7 | 17% |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 5.6 / 34.3 | 12% |  |
| [4061](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4061) | 0.0 / 27.6 | 41% | likelihood of objects |

**Gain documents against neutral documents** (6443 features active; 2674 differ at q < 0.05; 1343 more active in gain, 1331 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | 95.0 / 0.0 | 14% |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 88.4 / 0.1 | 28% |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 84.5 / 0.0 | 24% |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/406) | 62.2 / 0.0 | 12% | links and structured text |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 57.6 / 1.5 | 21% |  |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 50.2 / 0.0 | 5% |  |
| [485](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/485) | 47.8 / 1.3 | 21% |  |
| [778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/778) | 40.2 / 0.0 | 12% | exclamations followed by common sentence starters |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 53.7 / 20.1 | 25% | formatting characters |
| [2922](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2922) | 31.8 / 0.0 | 31% |  |
| [572](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/572) | 30.8 / 0.1 | 11% | accuracy and efficiency |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 31.1 / 0.9 | 9% | their |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 0.0 / 168.9 | 43% |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 0.6 / 85.2 | 32% |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 21.4 / 105.3 | 20% |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 14.7 / 95.6 | 17% |  |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.4 / 37.1 | 38% |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 2.4 / 37.7 | 29% |  |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.9 / 35.1 | 11% | places, homes, workshops |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 18.2 / 52.1 | 6% |  |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 8.0 / 41.2 | 7% | the repetition or challenge |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 0.6 / 29.7 | 17% |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 5.5 / 34.3 | 12% |  |
| [4061](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4061) | 0.0 / 27.6 | 41% | likelihood of objects |

**Credit documents against neutral documents** (6427 features active; 2589 differ at q < 0.05; 1208 more active in credit, 1381 in neutral)

| More active in credit | Activation (credit / neutral) | Share of credit tokens on | Description |
|---|---|---|---|
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 92.6 / 0.9 | 24% | their |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | 84.8 / 0.0 | 13% |  |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 81.5 / 0.0 | 18% |  |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 80.8 / 0.0 | 13% | you can or should |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 57.5 / 0.1 | 37% |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/406) | 54.4 / 0.0 | 10% | links and structured text |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 52.3 / 0.0 | 16% |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 50.2 / 0.1 | 18% |  |
| [1063](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1063) | 44.1 / 0.0 | 56% | politeness and requests |
| [485](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/485) | 41.6 / 1.3 | 19% |  |
| [478](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/478) | 43.2 / 5.4 | 13% |  |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 37.6 / 1.5 | 13% |  |

| More active in neutral | Activation (credit / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 0.0 / 168.9 | 43% |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 15.4 / 105.3 | 20% |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 0.4 / 85.2 | 32% |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 18.7 / 95.6 | 17% |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 10.9 / 52.1 | 6% |  |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 1.5 / 41.2 | 7% | the repetition or challenge |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.2 / 37.1 | 38% |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 2.1 / 37.7 | 29% |  |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.5 / 35.1 | 11% | places, homes, workshops |
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 96.0 / 125.4 | 23% |  |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | 0.4 / 29.7 | 17% |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 5.3 / 34.3 | 12% |  |

**Loss documents against gain documents** (5561 features active; 1693 differ at q < 0.05; 888 more active in loss, 805 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 121.2 / 5.7 | 36% |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 66.5 / 0.6 | 26% |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 58.4 / 21.9 | 32% |  |
| [15622](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15622) | 43.6 / 10.8 | 60% |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 153.9 / 124.6 | 27% |  |
| [1856](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1856) | 48.4 / 19.7 | 74% |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 82.3 / 53.7 | 26% | formatting characters |
| [427](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/427) | 57.7 / 31.4 | 25% | punctuated questions |
| [2609](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2609) | 20.6 / 0.2 | 19% | sorry, unfortunate, or sad statements |
| [890](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/890) | 29.5 / 9.1 | 35% |  |
| [1772](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1772) | 20.8 / 0.6 | 35% |  |
| [43](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/43) | 57.1 / 37.2 | 25% | lists starting with "This" |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | 2.1 / 95.0 | 14% |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 10.0 / 84.5 | 24% |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/406) | 0.2 / 62.2 | 12% | links and structured text |
| [778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/778) | 0.0 / 40.2 | 12% | exclamations followed by common sentence starters |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 17.4 / 50.2 | 5% |  |
| [1063](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1063) | 1.5 / 25.0 | 34% | politeness and requests |
| [2922](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2922) | 9.8 / 31.8 | 31% |  |
| [5690](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5690) | 17.0 / 34.5 | 25% | new tab |
| [485](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/485) | 32.7 / 47.8 | 21% |  |
| [5061](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5061) | 0.0 / 15.0 | 12% |  |
| [6567](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6567) | 0.7 / 15.5 | 26% | **praise and congratulations** |
| [519](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/519) | 15.6 / 29.5 | 12% | punctuation and common words |

**Blame documents against loss documents** (5262 features active; 1137 differ at q < 0.05; 484 more active in blame, 653 in loss)

| More active in blame | Activation (blame / loss) | Share of blame tokens on | Description |
|---|---|---|---|
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 71.8 / 3.2 | 13% | you can or should |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 81.6 / 17.8 | 22% | their |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 52.8 / 1.0 | 35% |  |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 68.7 / 17.4 | 15% |  |
| [478](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/478) | 39.0 / 7.4 | 14% |  |
| [14381](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14381) | 27.2 / 0.1 | 27% | responsibility and blame |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/543) | 27.4 / 3.4 | 12% |  |
| [745](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/745) | 35.7 / 13.4 | 45% |  |
| [118](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/118) | 25.5 / 4.1 | 3% | this [noun] |
| [13258](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13258) | 27.0 / 6.0 | 41% | past tense verbs followed by pronouns |
| [5687](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5687) | 19.4 / 0.0 | 28% | act as a |
| [1475](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1475) | 21.8 / 2.4 | 12% |  |

| More active in loss | Activation (blame / loss) | Share of loss tokens on | Description |
|---|---|---|---|
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 110.7 / 161.3 | 27% |  |
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 86.1 / 121.2 | 36% |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 121.6 / 153.9 | 27% |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 56.5 / 82.3 | 26% | formatting characters |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 53.5 / 78.9 | 29% |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 32.6 / 57.8 | 30% |  |
| [714](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/714) | 24.2 / 46.1 | 33% |  |
| [1126](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1126) | 26.2 / 46.8 | 35% | processing, end, old, love, follow, now |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 40.4 / 60.5 | 19% |  |
| [154](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/154) | 69.4 / 88.7 | 26% |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 40.7 / 58.4 | 32% |  |
| [394](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/394) | 17.2 / 34.8 | 11% |  |

**Credit documents against gain documents** (5068 features active; 922 differ at q < 0.05; 388 more active in credit, 534 in gain)

| More active in credit | Activation (credit / gain) | Share of credit tokens on | Description |
|---|---|---|---|
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 80.8 / 3.2 | 13% | you can or should |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 92.6 / 31.1 | 24% | their |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 57.5 / 0.6 | 37% |  |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 81.5 / 50.2 | 18% |  |
| [478](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/478) | 43.2 / 16.7 | 13% |  |
| [973](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/973) | 39.4 / 15.1 | 21% |  |
| [434](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/434) | 44.5 / 20.2 | 25% |  |
| [2556](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2556) | 26.7 / 2.6 | 9% | make, made, making |
| [944](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/944) | 24.3 / 3.0 | 17% |  |
| [5687](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5687) | 20.7 / 0.0 | 27% | act as a |
| [1063](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1063) | 44.1 / 25.0 | 56% | politeness and requests |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/543) | 19.0 / 1.4 | 10% |  |

| More active in gain | Activation (credit / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 96.0 / 142.3 | 28% |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 50.2 / 88.4 | 28% |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 52.3 / 84.5 | 24% |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 96.1 / 124.6 | 28% |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 20.9 / 46.2 | 26% |  |
| [714](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/714) | 21.1 / 42.1 | 26% |  |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 37.6 / 57.6 | 21% |  |
| [1126](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1126) | 20.8 / 40.1 | 35% | processing, end, old, love, follow, now |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 35.8 / 53.7 | 25% | formatting characters |
| [307](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/307) | 15.2 / 30.8 | 4% |  |
| [154](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/154) | 57.4 / 72.7 | 26% |  |
| [251](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/251) | 28.7 / 43.5 | 24% |  |

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 47 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 5 point the same way (about 5.6 expected by chance) and 4 the opposite way. Correlation of the two differences over the 44 features active in both: -0.02.

| Shared: more active under loss in both | Description |
|---|---|
| [9773](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773) | code snippets and list items |


## Layer 24

**Loss documents against neutral documents** (3718 features active; 1561 differ at q < 0.05; 732 more active in loss, 829 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 275.1 / 4.7 | 43% |  |
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 271.6 / 43.0 | 15% | disclaimersobviousexaggerate |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 272.6 / 57.8 | 32% |  |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6014) | 203.7 / 1.0 | 54% | life, dreams, release, optimize |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 286.7 / 102.5 | 27% |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/189) | 187.3 / 5.4 | 14% |  |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 277.5 / 96.6 | 86% | demonstratives (this, that, these) |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/128) | 170.7 / 0.9 | 14% | dynamics of |
| [3305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3305) | 129.3 / 0.0 | 40% | emotions (anxiety, stress, frustration) |
| [13457](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13457) | 123.6 / 0.0 | 37% | negative sentiment |
| [3599](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3599) | 121.7 / 0.2 | 41% | danger catastrophe death rape fines |
| [6146](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6146) | 122.4 / 2.1 | 32% | building towards |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 70.6 / 565.0 | 55% |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 80.6 / 447.0 | 21% |  |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 125.7 / 462.3 | 55% |  |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 27.0 / 326.4 | 59% | sentence corrections |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 83.0 / 356.6 | 30% |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 90.8 / 359.3 | 48% | ñ and language names |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 113.9 / 344.6 | 33% |  |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 323.5 / 551.5 | 31% | assert or code assertions |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 3.1 / 206.4 | 18% |  |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 32.4 / 204.9 | 36% | pulsing with |
| [5351](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5351) | 41.6 / 207.6 | 68% | shapes and structures |
| [5167](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5167) | 0.4 / 165.3 | 42% | end of turn tokens |

**Blame documents against neutral documents** (3780 features active; 1611 differ at q < 0.05; 776 more active in blame, 835 in neutral)

| More active in blame | Activation (blame / neutral) | Share of blame tokens on | Description |
|---|---|---|---|
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 396.5 / 103.7 | 58% | sweetest nectar |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 270.0 / 4.7 | 41% |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 318.7 / 57.8 | 37% |  |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 412.1 / 169.5 | 56% | Here's the setup |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6014) | 239.1 / 1.0 | 58% | life, dreams, release, optimize |
| [6146](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6146) | 164.3 / 2.1 | 41% | building towards |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 249.1 / 96.6 | 83% | demonstratives (this, that, these) |
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 179.1 / 43.0 | 13% | disclaimersobviousexaggerate |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/128) | 120.8 / 0.9 | 10% | dynamics of |
| [13457](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13457) | 119.1 / 0.0 | 34% | negative sentiment |
| [9203](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9203) | 135.6 / 21.8 | 64% |  |
| [3642](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3642) | 147.4 / 34.4 | 57% | pronouns |

| More active in neutral | Activation (blame / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 115.2 / 565.0 | 55% |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 81.2 / 447.0 | 21% |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 44.7 / 359.3 | 48% | ñ and language names |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 254.7 / 551.5 | 31% | assert or code assertions |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 39.7 / 326.4 | 59% | sentence corrections |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 192.9 / 462.3 | 55% |  |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 80.4 / 344.6 | 33% |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 132.9 / 356.6 | 30% |  |
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 9.7 / 210.3 | 30% | words starting with specific letters |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 10.7 / 206.4 | 18% |  |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 11.1 / 204.9 | 36% | pulsing with |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 70.9 / 253.6 | 25% |  |

**Gain documents against neutral documents** (3742 features active; 1582 differ at q < 0.05; 714 more active in gain, 868 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 281.3 / 0.0 | 73% |  |
| [2030](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2030) | 237.5 / 0.0 | 66% |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 276.9 / 57.8 | 33% |  |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 386.7 / 169.5 | 46% | Here's the setup |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 307.2 / 102.5 | 29% |  |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 298.9 / 96.6 | 90% | demonstratives (this, that, these) |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 184.0 / 4.7 | 32% |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/189) | 171.4 / 5.4 | 15% |  |
| [1405](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1405) | 161.9 / 6.2 | 30% | exclamations and punctuation |
| [311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/311) | 150.8 / 0.0 | 13% |  |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/128) | 109.7 / 0.9 | 10% | dynamics of |
| [6146](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6146) | 109.2 / 2.1 | 29% | building towards |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 92.6 / 565.0 | 55% |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 71.3 / 447.0 | 21% |  |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 111.0 / 462.3 | 55% |  |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 9.1 / 326.4 | 59% | sentence corrections |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 70.1 / 359.3 | 48% | ñ and language names |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 99.7 / 344.6 | 33% |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 129.2 / 356.6 | 30% |  |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 6.2 / 204.9 | 36% | pulsing with |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 11.6 / 206.4 | 18% |  |
| [5351](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5351) | 18.3 / 207.6 | 68% | shapes and structures |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 382.9 / 551.5 | 31% | assert or code assertions |
| [5167](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5167) | 0.1 / 165.3 | 42% | end of turn tokens |

**Credit documents against neutral documents** (3804 features active; 1584 differ at q < 0.05; 725 more active in credit, 859 in neutral)

| More active in credit | Activation (credit / neutral) | Share of credit tokens on | Description |
|---|---|---|---|
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 542.1 / 169.5 | 63% | Here's the setup |
| [2030](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2030) | 276.8 / 0.0 | 71% |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 320.4 / 57.8 | 39% |  |
| [4631](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4631) | 203.8 / 0.0 | 56% | professionalism and success |
| [8854](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8854) | 180.1 / 0.0 | 48% |  |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 276.1 / 96.6 | 86% | demonstratives (this, that, these) |
| [9203](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9203) | 180.3 / 21.8 | 71% |  |
| [5004](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5004) | 149.3 / 0.0 | 22% |  |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 248.3 / 102.5 | 23% |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/189) | 147.5 / 5.4 | 13% |  |
| [4716](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4716) | 137.3 / 0.0 | 40% | wishing you well |
| [3642](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3642) | 165.9 / 34.4 | 61% | pronouns |

| More active in neutral | Activation (credit / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 103.7 / 565.0 | 55% |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 78.3 / 447.0 | 21% |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 19.0 / 359.3 | 48% | ñ and language names |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 125.9 / 462.3 | 55% |  |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 20.2 / 326.4 | 59% | sentence corrections |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 264.5 / 551.5 | 31% | assert or code assertions |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 81.1 / 344.6 | 33% |  |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 3.3 / 204.9 | 36% | pulsing with |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 5.8 / 206.4 | 18% |  |
| [5351](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5351) | 15.2 / 207.6 | 68% | shapes and structures |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 70.4 / 253.6 | 25% |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 174.3 / 356.6 | 30% |  |

**Loss documents against gain documents** (3316 features active; 725 differ at q < 0.05; 376 more active in loss, 349 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 271.6 / 114.2 | 15% | disclaimersobviousexaggerate |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6014) | 203.7 / 73.7 | 54% | life, dreams, release, optimize |
| [3305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3305) | 129.3 / 4.3 | 40% | emotions (anxiety, stress, frustration) |
| [13457](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13457) | 123.6 / 0.0 | 37% | negative sentiment |
| [3599](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3599) | 121.7 / 15.8 | 41% | danger catastrophe death rape fines |
| [1771](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1771) | 113.3 / 10.6 | 32% | complex abstract concepts and hidden meanings |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 275.1 / 184.0 | 43% |  |
| [11296](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11296) | 92.3 / 2.0 | 47% | collapse, demise, destruction, loss |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 165.5 / 89.4 | 29% | sweetest nectar |
| [11564](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11564) | 71.3 / 0.1 | 21% | negative connotation |
| [366](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/366) | 195.2 / 128.3 | 12% |  |
| [531](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/531) | 153.9 / 89.0 | 14% | learned |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 16.6 / 281.3 | 73% |  |
| [2030](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2030) | 48.3 / 237.5 | 66% |  |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 223.9 / 386.7 | 46% | Here's the setup |
| [4631](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4631) | 6.6 / 97.1 | 32% | professionalism and success |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/896) | 0.0 / 80.8 | 10% | emojis and punctuation |
| [11059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11059) | 28.0 / 89.3 | 30% | adjectives of excellence |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 323.5 / 382.9 | 26% | assert or code assertions |
| [432](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/432) | 43.1 / 101.1 | 5% |  |
| [1424](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1424) | 32.1 / 86.7 | 25% |  |
| [311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/311) | 97.6 / 150.8 | 13% |  |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 27.6 / 80.5 | 22% | completion and progress |
| [12501](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12501) | 4.0 / 53.0 | 18% | almost everything, everywhere |

**Blame documents against loss documents** (3250 features active; 688 differ at q < 0.05; 332 more active in blame, 356 in loss)

| More active in blame | Activation (blame / loss) | Share of blame tokens on | Description |
|---|---|---|---|
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 396.5 / 165.5 | 58% | sweetest nectar |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 412.1 / 223.9 | 56% | Here's the setup |
| [5004](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5004) | 111.4 / 0.1 | 17% |  |
| [1579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1579) | 127.9 / 22.1 | 12% | foreign language words |
| [13123](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13123) | 102.7 / 3.2 | 33% | violation of wrongdoing |
| [465](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/465) | 106.7 / 15.5 | 9% |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/433) | 197.9 / 114.2 | 18% |  |
| [3627](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3627) | 96.3 / 14.9 | 29% | control and responsibility |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/111) | 259.5 / 178.5 | 44% |  |
| [13719](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13719) | 74.9 / 1.2 | 25% |  |
| [80](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/80) | 146.0 / 72.6 | 27% |  |
| [3642](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3642) | 147.4 / 74.6 | 57% | pronouns |

| More active in loss | Activation (blame / loss) | Share of loss tokens on | Description |
|---|---|---|---|
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 70.9 / 200.1 | 20% |  |
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 9.7 / 137.3 | 21% | words starting with specific letters |
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 179.1 / 271.6 | 15% | disclaimersobviousexaggerate |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 198.2 / 286.7 | 27% |  |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/350) | 52.1 / 140.3 | 20% |  |
| [770](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/770) | 52.1 / 134.5 | 23% | descriptive adjectives |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/189) | 109.1 / 187.3 | 14% |  |
| [366](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/366) | 125.6 / 195.2 | 12% |  |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 254.7 / 323.5 | 24% | assert or code assertions |
| [531](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/531) | 85.5 / 153.9 | 14% | learned |
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 127.2 / 195.4 | 18% |  |
| [1244](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1244) | 176.8 / 244.4 | 62% | and why |

**Credit documents against gain documents** (3271 features active; 523 differ at q < 0.05; 266 more active in credit, 257 in gain)

| More active in credit | Activation (credit / gain) | Share of credit tokens on | Description |
|---|---|---|---|
| [8854](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8854) | 180.1 / 2.7 | 48% |  |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 542.1 / 386.7 | 63% | Here's the setup |
| [5004](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5004) | 149.3 / 1.1 | 22% |  |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 212.0 / 89.4 | 38% | sweetest nectar |
| [4631](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4631) | 203.8 / 97.1 | 56% | professionalism and success |
| [1579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1579) | 124.7 / 19.6 | 10% | foreign language words |
| [13719](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13719) | 112.1 / 22.0 | 37% |  |
| [248](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/248) | 92.1 / 12.2 | 10% |  |
| [4716](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4716) | 137.3 / 58.0 | 40% | wishing you well |
| [3642](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3642) | 165.9 / 93.0 | 61% | pronouns |
| [109](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/109) | 77.2 / 7.8 | 8% |  |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/111) | 225.1 / 156.9 | 40% |  |

| More active in gain | Activation (credit / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 115.2 / 281.3 | 73% |  |
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 31.5 / 181.5 | 27% | words starting with specific letters |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 70.4 / 219.7 | 21% |  |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 264.5 / 382.9 | 26% | assert or code assertions |
| [770](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/770) | 58.2 / 138.8 | 23% | descriptive adjectives |
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 104.5 / 182.9 | 17% |  |
| [1405](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1405) | 89.5 / 161.9 | 30% | exclamations and punctuation |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/350) | 52.8 / 123.4 | 17% |  |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | 78.5 / 147.3 | 41% | another, observations, further |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 248.3 / 307.2 | 29% |  |
| [311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/311) | 92.1 / 150.8 | 13% |  |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 22.5 / 80.5 | 22% | completion and progress |

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 76 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 14 point the same way (about 9.6 expected by chance) and 8 the opposite way. Correlation of the two differences over the 240 features active in both: +0.09.

| Shared: more active under loss in both | Description |
|---|---|
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) |  |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | current news or state |
| [13799](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799) |  |


## Layer 31

**Loss documents against neutral documents** (6410 features active; 2294 differ at q < 0.05; 1259 more active in loss, 1035 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 912.8 / 0.0 | 81% |  |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | 927.6 / 97.1 | 92% | darkness and sorrow |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 755.8 / 0.0 | 53% | crises and disasters |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 831.5 / 139.4 | 27% | . The |
| [3174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3174) | 532.4 / 0.0 | 59% | sadness, disappointment, regret |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/289) | 464.2 / 0.0 | 44% |  |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 517.1 / 67.8 | 53% |  |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 406.2 / 1.9 | 50% |  |
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 392.1 / 0.0 | 44% | grief and sadness |
| [2224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2224) | 346.0 / 0.0 | 48% |  |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 335.8 / 0.3 | 36% |  |
| [2041](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2041) | 301.1 / 0.0 | 29% | disappear or vanish |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 23.7 / 1930.3 | 85% |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 30.3 / 827.4 | 84% |  |
| [349](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/349) | 681.7 / 1145.8 | 85% |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 1.8 / 446.7 | 55% | restraint |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 1.8 / 397.7 | 29% | describing spheres |
| [358](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/358) | 0.0 / 373.9 | 36% |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 2.5 / 340.0 | 52% | vector graphics and artistic styles |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 44.5 / 378.6 | 42% | in cyber |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/249) | 613.4 / 904.0 | 83% |  |
| [206](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/206) | 27.2 / 310.7 | 12% |  |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 229.5 / 508.0 | 57% | impressive sensations or qualities |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | 6.1 / 253.4 | 28% |  |

**Blame documents against neutral documents** (6473 features active; 2270 differ at q < 0.05; 1201 more active in blame, 1069 in neutral)

| More active in blame | Activation (blame / neutral) | Share of blame tokens on | Description |
|---|---|---|---|
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 966.2 / 67.8 | 79% |  |
| [2224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2224) | 839.0 / 0.0 | 86% |  |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | 901.4 / 97.1 | 90% | darkness and sorrow |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 769.8 / 0.0 | 50% | crises and disasters |
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 692.9 / 0.0 | 71% |  |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 565.0 / 0.3 | 48% |  |
| [6501](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6501) | 556.0 / 0.0 | 44% | responsibility and blame |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 516.7 / 0.0 | 66% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 617.5 / 139.4 | 19% | . The |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/289) | 398.5 / 0.0 | 37% |  |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 376.2 / 0.0 | 12% |  |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 378.8 / 4.8 | 27% | informal greetings and interjections |

| More active in neutral | Activation (blame / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 9.2 / 1930.3 | 85% |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 45.9 / 827.4 | 84% |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 1.7 / 446.7 | 55% | restraint |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 76.5 / 516.2 | 37% |  |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 84.4 / 508.0 | 57% | impressive sensations or qualities |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 1.9 / 397.7 | 29% | describing spheres |
| [358](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/358) | 0.0 / 373.9 | 36% |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 0.6 / 340.0 | 52% | vector graphics and artistic styles |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 52.2 / 378.6 | 42% | in cyber |
| [349](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/349) | 824.8 / 1145.8 | 85% |  |
| [206](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/206) | 32.9 / 310.7 | 12% |  |
| [1916](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1916) | 120.5 / 390.8 | 43% | corrected grammar for plurals |

**Gain documents against neutral documents** (6519 features active; 2303 differ at q < 0.05; 1212 more active in gain, 1091 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 830.6 / 0.1 | 57% |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 826.3 / 1.4 | 74% | exclamations of strong positive emotion |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 759.8 / 0.0 | 75% |  |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 691.0 / 67.8 | 63% |  |
| [14](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14) | 619.5 / 2.9 | 61% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 675.1 / 139.4 | 28% | . The |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 492.1 / 0.3 | 49% |  |
| [1168](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1168) | 408.0 / 0.1 | 39% | exclamations after greetings/emphatics |
| [5565](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5565) | 365.5 / 0.0 | 53% |  |
| [1321](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1321) | 340.7 / 0.0 | 43% |  |
| [10338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10338) | 328.0 / 0.0 | 48% | absolutely |
| [1739](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1739) | 315.2 / 0.0 | 25% |  |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 2.8 / 1930.3 | 85% |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 49.6 / 827.4 | 84% |  |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 22.8 / 516.2 | 37% |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 0.6 / 446.7 | 55% | restraint |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 1.1 / 397.7 | 29% | describing spheres |
| [349](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/349) | 754.5 / 1145.8 | 85% |  |
| [358](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/358) | 0.0 / 373.9 | 36% |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 10.9 / 340.0 | 52% | vector graphics and artistic styles |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 75.1 / 378.6 | 42% | in cyber |
| [206](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/206) | 16.7 / 310.7 | 12% |  |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 250.0 / 508.0 | 57% | impressive sensations or qualities |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | 3.5 / 253.4 | 28% |  |

**Credit documents against neutral documents** (6491 features active; 2240 differ at q < 0.05; 1152 more active in credit, 1088 in neutral)

| More active in credit | Activation (credit / neutral) | Share of credit tokens on | Description |
|---|---|---|---|
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 876.1 / 67.8 | 75% |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 800.3 / 1.4 | 73% | exclamations of strong positive emotion |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 712.3 / 0.3 | 61% |  |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 532.1 / 0.1 | 47% |  |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 522.9 / 0.0 | 66% |  |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 458.2 / 0.0 | 57% |  |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 432.7 / 0.0 | 12% |  |
| [10338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10338) | 404.9 / 0.0 | 54% | absolutely |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 390.3 / 0.7 | 47% | praise and awards |
| [14](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14) | 373.2 / 2.9 | 35% |  |
| [1321](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1321) | 352.0 / 0.0 | 40% |  |
| [5703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5703) | 345.5 / 0.0 | 32% | expressing gratitude and thanks |

| More active in neutral | Activation (credit / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 0.6 / 1930.3 | 85% |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 26.7 / 827.4 | 84% |  |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 8.1 / 516.2 | 37% |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 0.2 / 446.7 | 55% | restraint |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 76.4 / 508.0 | 57% | impressive sensations or qualities |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 0.7 / 397.7 | 29% | describing spheres |
| [358](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/358) | 0.0 / 373.9 | 36% |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 2.6 / 340.0 | 52% | vector graphics and artistic styles |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 87.5 / 378.6 | 42% | in cyber |
| [206](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/206) | 26.2 / 310.7 | 12% |  |
| [1916](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1916) | 110.1 / 390.8 | 43% | corrected grammar for plurals |
| [5360](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5360) | 63.0 / 324.7 | 47% |  |

**Loss documents against gain documents** (5642 features active; 1264 differ at q < 0.05; 654 more active in loss, 610 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 912.8 / 0.0 | 81% |  |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | 927.6 / 30.0 | 92% | darkness and sorrow |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 755.8 / 0.5 | 53% | crises and disasters |
| [3174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3174) | 532.4 / 0.0 | 59% | sadness, disappointment, regret |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/289) | 464.2 / 0.0 | 44% |  |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 406.2 / 0.0 | 50% |  |
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 392.1 / 0.0 | 44% | grief and sadness |
| [2224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2224) | 346.0 / 0.3 | 48% |  |
| [2041](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2041) | 301.1 / 0.0 | 29% | disappear or vanish |
| [1350](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1350) | 275.5 / 17.3 | 36% |  |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 275.1 / 22.8 | 23% |  |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | 251.6 / 0.0 | 29% | sighs, concerns, negative feelings |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 25.2 / 830.6 | 57% |  |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 2.5 / 759.8 | 75% |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 167.9 / 826.3 | 74% | exclamations of strong positive emotion |
| [5565](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5565) | 0.9 / 365.5 | 53% |  |
| [14](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14) | 262.1 / 619.5 | 61% |  |
| [1321](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1321) | 5.6 / 340.7 | 43% |  |
| [1168](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1168) | 82.9 / 408.0 | 39% | exclamations after greetings/emphatics |
| [1739](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1739) | 0.6 / 315.2 | 25% |  |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 0.5 / 312.7 | 48% | praise and awards |
| [10338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10338) | 26.1 / 328.0 | 48% | absolutely |
| [9965](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9965) | 37.7 / 300.0 | 35% | win and victory |
| [12126](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12126) | 0.0 / 229.1 | 29% |  |

**Blame documents against loss documents** (5237 features active; 893 differ at q < 0.05; 431 more active in blame, 462 in loss)

| More active in blame | Activation (blame / loss) | Share of blame tokens on | Description |
|---|---|---|---|
| [6501](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6501) | 556.0 / 13.4 | 44% | responsibility and blame |
| [2224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2224) | 839.0 / 346.0 | 86% |  |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 966.2 / 517.1 | 79% |  |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 376.2 / 0.0 | 12% |  |
| [826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/826) | 309.5 / 0.2 | 29% |  |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 516.7 / 210.9 | 66% |  |
| [2618](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2618) | 360.6 / 56.4 | 47% | negative judgment of intelligence |
| [121](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/121) | 336.2 / 71.9 | 15% | share in |
| [3703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3703) | 236.5 / 0.0 | 32% | interacting with me / you |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 565.0 / 335.8 | 48% |  |
| [33](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/33) | 330.1 / 107.9 | 12% | break down |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/249) | 819.7 / 613.4 | 80% |  |

| More active in loss | Activation (blame / loss) | Share of loss tokens on | Description |
|---|---|---|---|
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 149.7 / 392.1 | 44% | grief and sadness |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 181.4 / 406.2 | 50% |  |
| [179](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/179) | 87.3 / 307.7 | 27% |  |
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 692.9 / 912.8 | 81% |  |
| [3174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3174) | 315.5 / 532.4 | 59% | sadness, disappointment, regret |
| [1329](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1329) | 364.8 / 578.9 | 71% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 617.5 / 831.5 | 27% | . The |
| [2041](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2041) | 100.0 / 301.1 | 29% | disappear or vanish |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 76.5 / 275.1 | 23% |  |
| [14490](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14490) | 139.0 / 325.6 | 51% | suffix -able, -ous, -most |
| [1350](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1350) | 115.7 / 275.5 | 36% |  |
| [513](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/513) | 69.0 / 219.5 | 14% | explaining structured concepts |

**Credit documents against gain documents** (5270 features active; 756 differ at q < 0.05; 363 more active in credit, 393 in gain)

| More active in credit | Activation (credit / gain) | Share of credit tokens on | Description |
|---|---|---|---|
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 432.7 / 0.0 | 12% |  |
| [826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/826) | 316.0 / 0.8 | 31% |  |
| [173](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/173) | 322.6 / 8.6 | 8% | code makes things easier |
| [5703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5703) | 345.5 / 44.3 | 32% | expressing gratitude and thanks |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 522.9 / 260.5 | 66% |  |
| [5944](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5944) | 242.1 / 4.3 | 25% | expressions of love |
| [12980](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12980) | 244.8 / 8.6 | 14% | you deserve or are doing well |
| [3703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3703) | 236.0 / 0.0 | 32% | interacting with me / you |
| [600](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/600) | 338.2 / 103.9 | 40% |  |
| [33](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/33) | 272.0 / 40.7 | 10% | break down |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 712.3 / 492.1 | 61% |  |
| [915](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/915) | 256.6 / 43.5 | 29% | greetings and thanks |

| More active in gain | Activation (credit / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 458.2 / 759.8 | 75% |  |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 532.1 / 830.6 | 57% |  |
| [14](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14) | 373.2 / 619.5 | 61% |  |
| [1385](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1385) | 13.5 / 259.7 | 39% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 441.9 / 675.1 | 28% | . The |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 625.0 / 840.9 | 37% | punctuation and common abbreviations |
| [5565](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5565) | 152.3 / 365.5 | 53% |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/174) | 74.9 / 254.0 | 6% | We followed by ' |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 76.4 / 250.0 | 40% | impressive sensations or qualities |
| [12126](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12126) | 58.5 / 229.1 | 29% |  |
| [9965](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9965) | 149.6 / 300.0 | 35% | win and victory |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/26) | 3.7 / 146.9 | 17% |  |

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 33 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 5 point the same way (about 4.0 expected by chance) and 3 the opposite way. Correlation of the two differences over the 361 features active in both: +0.07.

| Shared: more active under loss in both | Description |
|---|---|
| [1450](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1450) |  |
| [1128](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1128) |  |
| [5652](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652) | unique identifier |


## Layer 41

**Loss documents against neutral documents** (7282 features active; 2574 differ at q < 0.05; 1549 more active in loss, 1025 in neutral)

| More active in loss | Activation (loss / neutral) | Share of loss tokens on | Description |
|---|---|---|---|
| [334](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/334) | 2067.9 / 0.0 | 49% |  |
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1757.8 / 0.0 | 68% | doom and disaster |
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | 1827.3 / 96.3 | 87% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1764.9 / 97.1 | 26% |  |
| [373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/373) | 1576.3 / 8.6 | 40% |  |
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 1406.6 / 0.4 | 58% |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/174) | 1538.8 / 164.3 | 60% | damage or broken |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 1362.1 / 12.0 | 41% |  |
| [2986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2986) | 1160.8 / 2.6 | 45% |  |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2558.5 / 1405.8 | 91% |  |
| [3218](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3218) | 1127.5 / 0.0 | 56% | sadness |
| [514](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/514) | 1124.9 / 3.8 | 42% | destruction |

| More active in neutral | Activation (loss / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 196.0 / 2623.0 | 65% |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.0 / 2043.4 | 62% |  |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.3 / 1382.9 | 51% |  |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1119.6 / 2443.6 | 95% | asking questions |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 1.2 / 1219.2 | 56% | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 2.0 / 1191.6 | 46% |  |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 26.8 / 1172.7 | 49% | tech jargon |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 1.9 / 1012.5 | 46% |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.5 / 893.5 | 43% | shapes |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 2.5 / 791.0 | 39% | objects or living things |
| [2269](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2269) | 10.2 / 748.6 | 40% | nothing |
| [5524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5524) | 30.9 / 754.7 | 61% | television |

**Blame documents against neutral documents** (7257 features active; 2435 differ at q < 0.05; 1363 more active in blame, 1072 in neutral)

| More active in blame | Activation (blame / neutral) | Share of blame tokens on | Description |
|---|---|---|---|
| [334](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/334) | 2023.9 / 0.0 | 40% |  |
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | 1836.1 / 96.3 | 89% |  |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2791.9 / 1405.8 | 93% |  |
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1283.5 / 0.0 | 55% | doom and disaster |
| [514](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/514) | 1232.4 / 3.8 | 27% | destruction |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1287.2 / 97.1 | 19% |  |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 1159.8 / 0.9 | 15% | say "ed" ending |
| [9965](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9965) | 1146.7 / 0.0 | 42% | guilt blame |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 1054.0 / 12.0 | 37% |  |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 813.6 / 0.0 | 12% | you |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 810.8 / 1.7 | 29% | say you |
| [3218](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3218) | 711.1 / 0.0 | 40% | sadness |

| More active in neutral | Activation (blame / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 135.6 / 2623.0 | 65% |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.0 / 2043.4 | 62% |  |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.0 / 1382.9 | 51% |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 0.3 / 1219.2 | 56% | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.4 / 1191.6 | 46% |  |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 43.1 / 1172.7 | 49% | tech jargon |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 3.3 / 1012.5 | 46% |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.3 / 893.5 | 43% | shapes |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.0 / 791.0 | 39% | objects or living things |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1696.1 / 2443.6 | 95% | asking questions |
| [2269](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2269) | 6.4 / 748.6 | 40% | nothing |
| [534](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/534) | 84.0 / 825.6 | 34% | specific things |

**Gain documents against neutral documents** (7377 features active; 2404 differ at q < 0.05; 1347 more active in gain, 1057 in neutral)

| More active in gain | Activation (gain / neutral) | Share of gain tokens on | Description |
|---|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 3023.1 / 4.0 | 71% | intensity |
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 1299.3 / 0.0 | 61% | Okay |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1327.2 / 97.1 | 27% |  |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 1226.0 / 0.0 | 59% | celebration |
| [382](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/382) | 1218.2 / 30.1 | 39% |  |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | 1122.3 / 0.0 | 35% |  |
| [9716](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9716) | 908.7 / 0.0 | 52% |  |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/26) | 1456.0 / 595.6 | 28% | Provides something |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2261.4 / 1405.8 | 89% |  |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 1483.1 / 652.7 | 86% | say "ing" word |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4082) | 819.3 / 0.0 | 46% |  |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 813.2 / 0.0 | 25% |  |

| More active in neutral | Activation (gain / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 37.3 / 2623.0 | 65% |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.0 / 2043.4 | 62% |  |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 2.4 / 1382.9 | 51% |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 1.3 / 1219.2 | 56% | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.0 / 1191.6 | 46% |  |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 68.2 / 1172.7 | 49% | tech jargon |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 0.9 / 1012.5 | 46% |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.3 / 893.5 | 43% | shapes |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1592.2 / 2443.6 | 95% | asking questions |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.3 / 791.0 | 39% | objects or living things |
| [2269](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2269) | 0.0 / 748.6 | 40% | nothing |
| [5524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5524) | 11.9 / 754.7 | 61% | television |

**Credit documents against neutral documents** (7186 features active; 2307 differ at q < 0.05; 1203 more active in credit, 1104 in neutral)

| More active in credit | Activation (credit / neutral) | Share of credit tokens on | Description |
|---|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 2960.5 / 4.0 | 76% | intensity |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2853.5 / 1405.8 | 93% |  |
| [1353](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1353) | 1132.7 / 0.0 | 56% | positive feelings |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 1109.0 / 0.9 | 14% | say "ed" ending |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 1738.2 / 652.7 | 93% | say "ing" word |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | 1036.8 / 0.0 | 32% |  |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 1033.1 / 0.0 | 13% | you |
| [382](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/382) | 980.7 / 30.1 | 30% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1006.0 / 97.1 | 20% |  |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 796.7 / 1.7 | 28% | say you |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 765.4 / 0.4 | 44% |  |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/214) | 886.0 / 124.2 | 21% |  |

| More active in neutral | Activation (credit / neutral) | Share of neutral tokens on | Description |
|---|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 29.1 / 2623.0 | 65% |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.0 / 2043.4 | 62% |  |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.0 / 1382.9 | 51% |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 2.6 / 1219.2 | 56% | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.0 / 1191.6 | 46% |  |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 60.6 / 1172.7 | 49% | tech jargon |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 1.8 / 1012.5 | 46% |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.0 / 893.5 | 43% | shapes |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.0 / 791.0 | 39% | objects or living things |
| [4584](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4584) | 95.4 / 851.2 | 33% | technical terms fragments |
| [2269](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2269) | 0.0 / 748.6 | 40% | nothing |
| [53](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/53) | 58.4 / 794.4 | 14% |  |

**Loss documents against gain documents** (6766 features active; 1834 differ at q < 0.05; 1002 more active in loss, 832 in gain)

| More active in loss | Activation (loss / gain) | Share of loss tokens on | Description |
|---|---|---|---|
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | 1827.3 / 39.3 | 87% |  |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/334) | 2067.9 / 312.7 | 49% |  |
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1757.8 / 4.2 | 68% | doom and disaster |
| [373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/373) | 1576.3 / 24.8 | 40% |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/174) | 1538.8 / 1.2 | 60% | damage or broken |
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 1406.6 / 0.9 | 58% |  |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 1362.1 / 25.9 | 41% |  |
| [2986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2986) | 1160.8 / 0.7 | 45% |  |
| [3218](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3218) | 1127.5 / 0.5 | 56% | sadness |
| [2800](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2800) | 993.8 / 0.3 | 55% | grief |
| [12596](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12596) | 977.8 / 5.9 | 38% | cease to exist or function |
| [514](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/514) | 1124.9 / 285.0 | 42% | destruction |

| More active in gain | Activation (loss / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 368.3 / 3023.1 | 71% | intensity |
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 0.0 / 1299.3 | 61% | Okay |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 1.9 / 1226.0 | 59% | celebration |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | 6.4 / 1122.3 | 35% |  |
| [9716](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9716) | 9.0 / 908.7 | 52% |  |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4082) | 11.5 / 819.3 | 46% |  |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 17.4 / 762.2 | 39% |  |
| [2633](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2633) | 12.5 / 706.8 | 40% | winning |
| [382](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/382) | 581.4 / 1218.2 | 39% |  |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 219.7 / 813.2 | 25% |  |
| [143](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/143) | 264.3 / 809.5 | 50% | get |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/655) | 155.7 / 651.9 | 49% | portrays beauty |

**Blame documents against loss documents** (6187 features active; 1068 differ at q < 0.05; 456 more active in blame, 612 in loss)

| More active in blame | Activation (blame / loss) | Share of blame tokens on | Description |
|---|---|---|---|
| [9965](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9965) | 1146.7 / 16.0 | 42% | guilt blame |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 810.8 / 15.0 | 29% | say you |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 1159.8 / 408.7 | 15% | say "ed" ending |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 813.6 / 95.5 | 12% | you |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1696.1 / 1119.6 | 82% | asking questions |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/350) | 792.6 / 276.9 | 20% |  |
| [1604](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1604) | 472.5 / 9.1 | 28% | foolishness |
| [3173](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3173) | 498.5 / 54.6 | 30% | selfishness and cruelty |
| [342](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/342) | 589.6 / 168.7 | 17% |  |
| [784](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/784) | 597.2 / 193.6 | 18% |  |
| [9220](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9220) | 455.2 / 54.4 | 15% | say "us" |
| [453](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/453) | 670.9 / 277.3 | 27% |  |

| More active in loss | Activation (blame / loss) | Share of loss tokens on | Description |
|---|---|---|---|
| [26](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/26) | 472.6 / 1407.0 | 26% | Provides something |
| [373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/373) | 650.9 / 1576.3 | 40% |  |
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 576.6 / 1406.6 | 58% |  |
| [12596](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12596) | 148.2 / 977.8 | 38% | cease to exist or function |
| [2986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2986) | 345.1 / 1160.8 | 45% |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/174) | 726.5 / 1538.8 | 60% | damage or broken |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | 381.8 / 907.9 | 25% |  |
| [2800](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2800) | 468.2 / 993.8 | 55% | grief |
| [486](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/486) | 248.1 / 725.9 | 25% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1287.2 / 1764.9 | 26% |  |
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1283.5 / 1757.8 | 68% | doom and disaster |
| [503](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/503) | 346.3 / 803.5 | 28% |  |

**Credit documents against gain documents** (6155 features active; 769 differ at q < 0.05; 342 more active in credit, 427 in gain)

| More active in credit | Activation (credit / gain) | Share of credit tokens on | Description |
|---|---|---|---|
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 796.7 / 15.8 | 28% | say you |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 1033.1 / 262.3 | 13% | you |
| [342](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/342) | 817.8 / 122.6 | 18% |  |
| [1353](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1353) | 1132.7 / 451.8 | 56% | positive feelings |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2853.5 / 2261.4 | 93% |  |
| [240](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/240) | 598.6 / 66.3 | 8% | make |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 1109.0 / 625.2 | 14% | say "ed" ending |
| [2386](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2386) | 484.0 / 49.4 | 25% | appreciation |
| [9220](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9220) | 461.3 / 37.1 | 12% | say "us" |
| [44](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/44) | 473.0 / 81.4 | 11% | led and developed |
| [1561](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1561) | 413.2 / 36.7 | 9% | appear, seem, look |
| [1006](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1006) | 720.7 / 354.4 | 52% | dedication |

| More active in gain | Activation (credit / gain) | Share of gain tokens on | Description |
|---|---|---|---|
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 461.6 / 1299.3 | 61% | Okay |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/26) | 664.9 / 1456.0 | 28% | Provides something |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 568.1 / 1226.0 | 59% | celebration |
| [9716](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9716) | 273.2 / 908.7 | 52% |  |
| [4366](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4366) | 144.7 / 546.6 | 41% |  |
| [209](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/209) | 157.1 / 525.4 | 29% |  |
| [2633](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2633) | 357.2 / 706.8 | 40% | winning |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4082) | 475.3 / 819.3 | 46% |  |
| [3482](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3482) | 340.8 / 678.1 | 62% |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1006.0 / 1327.2 | 27% |  |
| [10896](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10896) | 14.1 / 330.7 | 19% | abundance |
| [486](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/486) | 296.6 / 593.7 | 26% |  |

**The documents' loss-vs-gain features against UBS's loss-vs-gain request** (B's matched rereads, 300 moments, history held fixed; p flips signs by career): 23 features separate UBS's loss request from its gain request at q < 0.05. Of the features that separate both, 7 point the same way (about 3.4 expected by chance) and 3 the opposite way. Correlation of the two differences over the 442 features active in both: +0.12.

| Shared: more active under loss in both | Description |
|---|---|
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) |  |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) |  |


# Read by the agent itself

The same documents placed at the start of UBS's request update in B's neutral careers (60 requests, one document of each type per request, as in the priming run), so that “you” and “we” are the agent and its desk. While reading: each feature's mean activation over the document's tokens. At the decision: the last token before the agent's reply, against the same moment with no document. Paired within the request; p flips the sign of each request's difference. **Personal:** for blame against loss and credit against gain (the “you” in each), the features that differ when the agent reads the document in its own career but not when it reads it on its own.


## Layer 12, read by the agent

**Reading: loss against neutral** (6727 features active; 4955 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 166.1 / 1.0 |  |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 78.0 / 2.4 |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 74.4 / 0.1 |  |
| [4](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4) | 71.5 / 5.3 | erotic |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 66.4 / 5.3 |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 60.9 / 0.0 |  |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 61.0 / 1.3 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 61.1 / 2.3 |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 80.3 / 21.7 | formatting characters |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 62.9 / 4.4 |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 56.0 / 1.6 |  |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | 57.7 / 5.4 |  |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 1.3 / 153.1 |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 25.3 / 110.9 |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 14.5 / 99.8 |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 2.6 / 76.1 |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 2.0 / 45.8 |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 15.0 / 52.8 |  |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.6 / 33.5 | places, homes, workshops |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 10.4 / 41.8 | the repetition or challenge |
| [8778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8778) | 21.4 / 52.4 | specifying quantities and attributes |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.3 / 30.7 |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 6.9 / 36.5 |  |
| [739](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/739) | 6.7 / 34.9 |  |

**Reading: blame against neutral** (6809 features active; 4870 differ at q < 0.05)

| More active blame | Activation (blame / neutral) | Description |
|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 120.2 / 1.0 |  |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 90.5 / 1.8 | their |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 79.4 / 0.1 |  |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 77.9 / 0.0 | you can or should |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 69.1 / 2.4 |  |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 52.4 / 0.1 |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 50.6 / 0.1 |  |
| [4](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4) | 54.6 / 5.3 | erotic |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 48.9 / 2.3 |  |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 51.1 / 5.3 |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 45.6 / 0.0 |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 44.0 / 1.6 |  |

| More active neutral | Activation (blame / neutral) | Description |
|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 0.2 / 153.1 |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 15.0 / 110.9 |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 16.2 / 99.8 |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 0.8 / 76.1 |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 4.8 / 52.8 |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 2.1 / 45.8 |  |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 1.2 / 41.8 | the repetition or challenge |
| [8778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8778) | 14.5 / 52.4 | specifying quantities and attributes |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.2 / 33.5 | places, homes, workshops |
| [739](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/739) | 4.0 / 34.9 |  |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.1 / 30.7 |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 6.1 / 36.5 |  |

**Reading: gain against neutral** (6660 features active; 4902 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | 97.7 / 0.2 |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 85.8 / 0.1 |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 79.6 / 0.0 |  |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 81.1 / 2.4 |  |
| [4](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4) | 71.1 / 5.3 | erotic |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/406) | 64.4 / 0.0 | links and structured text |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 68.3 / 5.3 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 63.2 / 2.3 |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 58.1 / 1.6 |  |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | 61.0 / 5.4 |  |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 56.5 / 1.3 |  |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 52.0 / 0.1 |  |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 0.0 / 153.1 |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 21.9 / 110.9 |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 13.3 / 99.8 |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 0.5 / 76.1 |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 3.3 / 45.8 |  |
| [8778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8778) | 16.4 / 52.4 | specifying quantities and attributes |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 19.0 / 52.8 |  |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 8.3 / 41.8 | the repetition or challenge |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.9 / 33.5 | places, homes, workshops |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 5.7 / 36.5 |  |
| [785](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/785) | 0.2 / 30.7 |  |
| [739](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/739) | 4.8 / 34.9 |  |

**Reading: credit against neutral** (6640 features active; 4785 differ at q < 0.05)

| More active credit | Activation (credit / neutral) | Description |
|---|---|---|
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 98.8 / 1.8 | their |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 88.6 / 0.1 |  |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | 86.2 / 0.2 |  |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 84.8 / 0.0 | you can or should |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 65.4 / 2.4 |  |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 56.5 / 0.1 |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/406) | 55.2 / 0.0 | links and structured text |
| [1063](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1063) | 50.8 / 0.1 | politeness and requests |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 49.4 / 0.0 |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 48.6 / 0.1 |  |
| [4](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4) | 50.1 / 5.3 | erotic |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 46.7 / 2.3 |  |

| More active neutral | Activation (credit / neutral) | Description |
|---|---|---|
| [473](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/473) | 0.0 / 153.1 |  |
| [408](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/408) | 15.5 / 110.9 |  |
| [387](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/387) | 16.9 / 99.8 |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/188) | 0.3 / 76.1 |  |
| [646](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/646) | 2.8 / 45.8 |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/433) | 11.3 / 52.8 |  |
| [43](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/43) | 21.5 / 62.6 | lists starting with "This" |
| [285](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/285) | 1.6 / 41.8 | the repetition or challenge |
| [8778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/8778) | 13.1 / 52.4 | specifying quantities and attributes |
| [129](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/129) | 0.5 / 33.5 | places, homes, workshops |
| [739](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/739) | 3.1 / 34.9 |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/442) | 5.1 / 36.5 |  |

**Reading: loss against gain** (5827 features active; 3857 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 166.1 / 51.2 |  |
| [106](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/106) | 60.9 / 0.5 |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 62.9 / 22.3 |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 160.5 / 127.2 |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 80.3 / 49.8 | formatting characters |
| [427](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/427) | 56.7 / 28.9 | punctuated questions |
| [15622](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15622) | 31.5 / 6.2 |  |
| [43](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/43) | 54.2 / 32.6 | lists starting with "This" |
| [2609](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2609) | 21.5 / 0.1 | sorry, unfortunate, or sad statements |
| [1772](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1772) | 22.5 / 1.3 |  |
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 160.5 / 140.1 |  |
| [154](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/154) | 86.3 / 66.5 |  |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | 2.9 / 97.7 |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 9.3 / 79.6 |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/406) | 0.3 / 64.4 | links and structured text |
| [778](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/778) | 0.0 / 41.3 | exclamations followed by common sentence starters |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 18.1 / 52.0 |  |
| [1063](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1063) | 2.8 / 29.5 | politeness and requests |
| [2922](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2922) | 9.8 / 31.9 |  |
| [6567](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6567) | 0.5 / 15.6 | **praise and congratulations** |
| [485](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/485) | 34.0 / 48.9 |  |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 20.4 / 35.4 | their |
| [5061](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5061) | 0.0 / 14.4 |  |
| [118](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/118) | 4.4 / 17.8 | this [noun] |

**Reading: blame against loss** (5649 features active; 3194 differ at q < 0.05). Personal: 2069 of them do not differ when the documents are read on their own (1155 differ there).

| More active blame | Activation (blame / loss) | Description |
|---|---|---|
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 77.9 / 3.5 | you can or should |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 90.5 / 20.4 | their |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 79.4 / 18.1 |  |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 52.4 / 1.0 |  |
| [478](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/478) | 37.3 / 6.3 |  |
| [14381](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14381) | 28.9 / 0.2 | responsibility and blame |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/543) | 26.4 / 3.2 |  |
| [118](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/118) | 26.1 / 4.4 | this [noun] |
| [13258](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13258) | 27.2 / 6.5 | past tense verbs followed by pronouns |
| [1475](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1475) | 24.0 / 3.3 |  |
| [5687](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5687) | 20.4 / 0.0 | act as a |
| [973](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/973) | 46.5 / 26.5 |  |

| More active loss | Activation (blame / loss) | Description |
|---|---|---|
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 111.4 / 160.5 |  |
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | 120.2 / 166.1 |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 128.4 / 160.5 |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 50.6 / 74.4 |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 56.8 / 80.3 | formatting characters |
| [714](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/714) | 27.9 / 50.6 |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 26.9 / 48.3 |  |
| [1126](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1126) | 26.1 / 47.4 | processing, end, old, love, follow, now |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 40.4 / 61.0 |  |
| [154](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/154) | 66.3 / 86.3 |  |
| [266](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/266) | 44.0 / 62.9 |  |
| [394](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/394) | 19.8 / 38.7 |  |

| Personal (blame vs loss, only in the agent's own career) | Direction | Description |
|---|---|---|
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | more in loss |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | more in loss |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | more in loss |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | more in loss |  |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | more in loss |  |
| [236](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/236) | more in loss | Example 1 |
| [6141](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6141) | more in blame |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/174) | more in loss | numbers |
| [114](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/114) | more in loss | EventCode=4624 |
| [371](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/371) | more in loss | electroweak force |
| [339](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/339) | more in loss | multilingual tokens |
| [378](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/378) | more in loss |  |

**Reading: credit against gain** (5275 features active; 2794 differ at q < 0.05). Personal: 1917 of them do not differ when the documents are read on their own (899 differ there).

| More active credit | Activation (credit / gain) | Description |
|---|---|---|
| [299](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/299) | 84.8 / 3.7 | you can or should |
| [60](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/60) | 98.8 / 35.4 | their |
| [752](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/752) | 56.5 / 0.7 |  |
| [390](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/390) | 88.6 / 52.0 |  |
| [478](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/478) | 41.6 / 14.0 |  |
| [434](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/434) | 46.5 / 21.0 |  |
| [973](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/973) | 40.8 / 16.4 |  |
| [2556](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2556) | 26.6 / 2.5 | make, made, making |
| [5687](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5687) | 22.2 / 0.1 | act as a |
| [1063](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1063) | 50.8 / 29.5 | politeness and requests |
| [944](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/944) | 23.6 / 2.5 |  |
| [543](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/543) | 18.7 / 1.3 |  |

| More active gain | Activation (credit / gain) | Description |
|---|---|---|
| [502](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/502) | 95.1 / 140.1 |  |
| [302](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/302) | 48.6 / 85.8 |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/56) | 49.4 / 79.6 |  |
| [254](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/254) | 98.9 / 127.2 |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 14.1 / 35.8 |  |
| [714](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/714) | 24.2 / 45.6 |  |
| [4](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4) | 50.1 / 71.1 | erotic |
| [1126](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1126) | 21.9 / 42.8 | processing, end, old, love, follow, now |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 48.3 / 68.3 |  |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/166) | 37.0 / 56.5 |  |
| [170](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/170) | 32.3 / 49.8 | formatting characters |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 46.7 / 63.2 |  |

| Personal (credit vs gain, only in the agent's own career) | Direction | Description |
|---|---|---|
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | more in gain |  |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | more in gain |  |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | more in gain |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | more in gain |  |
| [99](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/99) | more in gain |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | more in gain |  |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/214) | more in gain |  |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/429) | more in gain |  |
| [236](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/236) | more in gain | Example 1 |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/187) | more in gain |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/174) | more in gain | numbers |
| [315](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/315) | more in gain |  |

**At the decision: after a neutral document against none** (52 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 65.2 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 52.4 / 12.3 | Here's a breakdown |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 61.8 / 24.9 |  |
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 54.0 / 24.2 | Instead, nothing |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 100.9 / 71.7 |  |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 56.7 / 37.1 | Option 2 |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 261.7 / 243.0 |  |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 85.6 / 67.3 |  |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 0.9 / 23.6 | `@RestController` |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 58.9 / 80.0 |  |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 0.0 / 20.6 |  |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | 272.5 / 290.5 |  |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | 4.7 / 17.9 | "said" followed by punctuation or direct speech |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 0.6 / 13.8 |  |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 15.2 / 27.8 | foreign language text/characters |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | 78.1 / 89.3 | | |

**At the decision: after a loss document against none** (49 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 69.7 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 45.7 / 12.3 | Here's a breakdown |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 54.0 / 24.9 |  |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 33.1 / 4.5 | greetings and thanks |
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 49.9 / 24.2 | Instead, nothing |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 95.9 / 71.7 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 264.7 / 243.0 |  |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 58.2 / 37.1 | Option 2 |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 5.2 / 27.8 | foreign language text/characters |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 2.8 / 23.6 | `@RestController` |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 0.0 / 20.6 |  |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | 14.7 / 33.1 | model explanations |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | 274.9 / 290.5 |  |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | 32.9 / 48.3 |  |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 66.3 / 80.0 |  |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 0.6 / 13.8 |  |

**At the decision: after a blame document against none** (49 features differ at q < 0.05)

| More active after blame | Activation (after blame / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 60.4 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 43.0 / 12.3 | Here's a breakdown |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 33.1 / 4.5 | greetings and thanks |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | 158.8 / 142.7 |  |
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | 107.4 / 92.2 |  |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | 14.6 / 0.6 |  |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 85.7 / 71.7 |  |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 50.9 / 37.1 | Option 2 |

| More active with no document | Activation (after blame / with no document) | Description |
|---|---|---|
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | 15.7 / 38.1 | to place |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 0.0 / 20.6 |  |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 9.6 / 27.8 | foreign language text/characters |
| [9038](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9038) | 2.7 / 16.9 | online communities and discussions |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 0.6 / 13.8 |  |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | 6.7 / 17.9 | "said" followed by punctuation or direct speech |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 12.6 / 23.6 | `@RestController` |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | 27.2 / 37.3 |  |

**At the decision: after a gain document against none** (50 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 65.0 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 41.5 / 12.3 | Here's a breakdown |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 27.2 / 4.5 | greetings and thanks |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 90.5 / 71.7 |  |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 55.0 / 37.1 | Option 2 |
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | 107.6 / 92.2 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 258.1 / 243.0 |  |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 39.9 / 24.9 |  |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 5.9 / 27.8 | foreign language text/characters |
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 0.0 / 20.6 |  |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 5.7 / 23.6 | `@RestController` |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | 20.6 / 37.3 |  |
| [2653](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653) | 78.1 / 89.3 | | |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | 279.4 / 290.5 |  |
| [4382](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382) | 10.9 / 21.5 |  |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 3.6 / 13.8 |  |

**At the decision: after a credit document against none** (48 features differ at q < 0.05)

| More active after credit | Activation (after credit / with no document) | Description |
|---|---|---|
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 56.5 / 17.2 | numbers and foreign words |
| [5762](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762) | 41.1 / 12.3 | Here's a breakdown |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 26.9 / 4.5 | greetings and thanks |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | 18.2 / 0.6 |  |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | 157.7 / 142.7 |  |
| [2765](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765) | 51.7 / 37.1 | Option 2 |
| [9234](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234) | 106.4 / 92.2 |  |
| [3490](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490) | 35.0 / 23.2 | multi-script words |

| More active with no document | Activation (after credit / with no document) | Description |
|---|---|---|
| [6260](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260) | 0.0 / 20.6 |  |
| [13271](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271) | 22.6 / 37.3 |  |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 13.9 / 27.8 | foreign language text/characters |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 10.5 / 23.6 | `@RestController` |
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 11.7 / 24.2 | Instead, nothing |
| [2878](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878) | 1.8 / 13.8 |  |
| [9038](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9038) | 4.9 / 16.9 | online communities and discussions |
| [2365](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365) | 6.5 / 17.9 | "said" followed by punctuation or direct speech |

**At the decision: after loss against after gain** (38 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 49.9 / 33.9 | Instead, nothing |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 54.0 / 39.9 |  |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 83.7 / 75.0 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 264.7 / 258.1 |  |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220) | 125.0 / 118.9 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 245.0 / 239.0 |  |
| [7391](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/7391) | 33.1 / 27.2 | greetings and thanks |
| [360](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360) | 223.7 / 218.3 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | 14.7 / 24.5 | model explanations |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | 110.5 / 119.2 | ``` |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | 32.9 / 40.5 |  |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | 4.4 / 10.4 |  |
| [9295](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9295) | 0.9 / 6.8 | number-word sequences |
| [277](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/277) | 66.3 / 71.3 |  |
| [3490](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490) | 30.2 / 34.8 | multi-script words |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | 147.0 / 151.6 |  |

**At the decision: after blame against after loss** (48 features differ at q < 0.05)

| More active after blame | Activation (after blame / after loss) | Description |
|---|---|---|
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | 124.7 / 110.5 | ``` |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | 158.8 / 147.0 |  |
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | 24.9 / 14.7 | model explanations |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | 14.6 / 4.4 |  |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 12.6 / 2.8 | `@RestController` |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | 284.3 / 274.9 |  |
| [1534](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534) | 38.8 / 32.9 |  |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | 79.6 / 73.8 |  |

| More active after loss | Activation (after blame / after loss) | Description |
|---|---|---|
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 24.7 / 49.9 | Instead, nothing |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 31.8 / 54.0 |  |
| [5610](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5610) | 15.7 / 32.1 | to place |
| [9038](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9038) | 2.7 / 14.5 | online communities and discussions |
| [276](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/276) | 72.2 / 83.7 |  |
| [2328](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2328) | 66.5 / 77.5 | conversational openings |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 234.4 / 245.0 |  |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/652) | 90.9 / 101.3 |  |

**At the decision: after credit against after gain** (44 features differ at q < 0.05)

| More active after credit | Activation (after credit / after gain) | Description |
|---|---|---|
| [1632](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632) | 35.8 / 24.5 | model explanations |
| [1842](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1842) | 13.9 / 5.9 | foreign language text/characters |
| [9227](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9227) | 18.2 / 10.4 |  |
| [168](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168) | 157.7 / 151.6 |  |
| [117](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117) | 125.2 / 119.2 | ``` |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111) | 284.7 / 279.4 |  |
| [16380](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380) | 10.5 / 5.7 | `@RestController` |
| [3985](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985) | 74.7 / 71.4 |  |

| More active after gain | Activation (after credit / after gain) | Description |
|---|---|---|
| [14659](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/14659) | 11.7 / 33.9 | Instead, nothing |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/189) | 28.1 / 39.9 |  |
| [438](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438) | 249.2 / 258.1 |  |
| [314](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314) | 230.1 / 239.0 |  |
| [3000](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000) | 56.5 / 65.0 | numbers and foreign words |
| [2328](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2328) | 68.1 / 76.5 | conversational openings |
| [49](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49) | 82.3 / 90.5 |  |
| [482](https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482) | 207.7 / 215.7 |  |


## Layer 24, read by the agent

**Reading: loss against neutral** (3972 features active; 2682 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 270.7 / 48.6 | disclaimersobviousexaggerate |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 280.7 / 60.9 |  |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 175.4 / 4.6 |  |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 382.1 / 213.8 | skills and experience |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/128) | 167.0 / 0.5 | dynamics of |
| [498](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/498) | 171.1 / 5.4 |  |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 209.1 / 59.3 | demonstratives (this, that, these) |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/350) | 149.1 / 16.9 |  |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6014) | 128.4 / 0.6 | life, dreams, release, optimize |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/189) | 130.6 / 3.4 |  |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 202.4 / 80.6 |  |
| [358](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/358) | 107.6 / 0.2 | closing quotes or list items |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 226.5 / 844.2 |  |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 177.9 / 521.1 |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 87.4 / 410.7 |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 113.5 / 393.2 | ñ and language names |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 3.1 / 263.5 | sentence corrections |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 108.9 / 343.7 |  |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 102.9 / 301.8 |  |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 137.6 / 305.3 |  |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 17.5 / 183.2 | pulsing with |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 452.1 / 611.7 | assert or code assertions |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/515) | 119.0 / 275.8 | The neuron strongly activates on specific plant variety (cultivar) names in lists. |
| [5167](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5167) | 1.0 / 146.4 | end of turn tokens |

**Reading: blame against neutral** (4036 features active; 2683 differ at q < 0.05)

| More active blame | Activation (blame / neutral) | Description |
|---|---|---|
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 323.6 / 60.9 |  |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 389.0 / 159.7 | sweetest nectar |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 442.1 / 226.3 | Here's the setup |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 158.9 / 4.6 |  |
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 194.6 / 48.6 | disclaimersobviousexaggerate |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 196.6 / 59.3 | demonstratives (this, that, these) |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/26) | 228.5 / 91.9 |  |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/128) | 136.9 / 0.5 | dynamics of |
| [6146](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6146) | 135.6 / 2.7 | building towards |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6014) | 132.5 / 0.6 | life, dreams, release, optimize |
| [498](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/498) | 124.8 / 5.4 |  |
| [9203](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9203) | 123.7 / 14.2 |  |

| More active neutral | Activation (blame / neutral) | Description |
|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 328.7 / 844.2 |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 46.2 / 393.2 | ñ and language names |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 195.5 / 521.1 |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 86.1 / 410.7 |  |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 3.3 / 263.5 | sentence corrections |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 370.3 / 611.7 | assert or code assertions |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 73.9 / 301.8 |  |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/515) | 58.0 / 275.8 | The neuron strongly activates on specific plant variety (cultivar) names in lists. |
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 9.8 / 199.3 | words starting with specific letters |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 6.0 / 183.2 | pulsing with |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 133.6 / 305.3 |  |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 32.3 / 202.0 |  |

**Reading: gain against neutral** (3906 features active; 2612 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [2030](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2030) | 262.6 / 0.0 |  |
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 236.3 / 0.0 |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 275.4 / 60.9 |  |
| [498](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/498) | 173.8 / 5.4 |  |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 220.6 / 59.3 | demonstratives (this, that, these) |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 371.2 / 213.8 | skills and experience |
| [1405](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1405) | 127.4 / 6.0 | exclamations and punctuation |
| [311](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/311) | 119.3 / 0.0 |  |
| [128](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/128) | 113.0 / 0.5 | dynamics of |
| [189](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/189) | 115.0 / 3.4 |  |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/350) | 127.6 / 16.9 |  |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 190.1 / 80.6 |  |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 345.2 / 844.2 |  |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 187.2 / 521.1 |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 83.3 / 410.7 |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 85.5 / 393.2 | ñ and language names |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 0.2 / 263.5 | sentence corrections |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 94.4 / 301.8 |  |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/515) | 83.2 / 275.8 | The neuron strongly activates on specific plant variety (cultivar) names in lists. |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 3.2 / 183.2 | pulsing with |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 166.4 / 343.7 |  |
| [5167](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5167) | 0.8 / 146.4 | end of turn tokens |
| [5351](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5351) | 3.2 / 142.3 | shapes and structures |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 181.3 / 305.3 |  |

**Reading: credit against neutral** (4004 features active; 2694 differ at q < 0.05)

| More active credit | Activation (credit / neutral) | Description |
|---|---|---|
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 562.1 / 226.3 | Here's the setup |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 354.1 / 60.9 |  |
| [2030](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2030) | 279.5 / 0.0 |  |
| [9059](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059) | 232.3 / 59.3 | demonstratives (this, that, these) |
| [8854](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8854) | 169.9 / 0.0 |  |
| [498](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/498) | 168.3 / 5.4 |  |
| [4631](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4631) | 136.9 / 0.0 | professionalism and success |
| [4716](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4716) | 134.0 / 0.0 | wishing you well |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 292.9 / 159.7 | sweetest nectar |
| [9203](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9203) | 143.4 / 14.2 |  |
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 119.3 / 0.0 |  |
| [5004](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5004) | 117.1 / 0.0 |  |

| More active neutral | Activation (credit / neutral) | Description |
|---|---|---|
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 337.0 / 844.2 |  |
| [52](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/52) | 26.7 / 393.2 | ñ and language names |
| [187](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/187) | 185.7 / 521.1 |  |
| [499](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/499) | 91.7 / 410.7 |  |
| [9927](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9927) | 0.4 / 263.5 | sentence corrections |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/515) | 38.6 / 275.8 | The neuron strongly activates on specific plant variety (cultivar) names in lists. |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | 65.2 / 301.8 |  |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 392.4 / 611.7 | assert or code assertions |
| [703](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/703) | 1.8 / 183.2 | pulsing with |
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 26.6 / 199.3 | words starting with specific letters |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | 135.9 / 305.3 |  |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 37.7 / 202.0 |  |

**Reading: loss against gain** (3625 features active; 1801 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 270.7 / 144.7 | disclaimersobviousexaggerate |
| [13457](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13457) | 90.5 / 0.0 | negative sentiment |
| [3599](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3599) | 93.3 / 6.8 | danger catastrophe death rape fines |
| [6014](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6014) | 128.4 / 45.3 | life, dreams, release, optimize |
| [11564](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11564) | 82.9 / 0.1 | negative connotation |
| [3305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3305) | 81.6 / 1.2 | emotions (anxiety, stress, frustration) |
| [11296](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11296) | 82.3 / 4.1 | collapse, demise, destruction, loss |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 175.4 / 98.3 |  |
| [1771](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1771) | 80.7 / 8.6 | complex abstract concepts and hidden meanings |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 233.8 / 167.5 | sweetest nectar |
| [366](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/366) | 194.3 / 133.3 |  |
| [10568](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10568) | 296.9 / 237.1 | following tweet, perform NER |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 14.1 / 236.3 |  |
| [2030](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2030) | 81.9 / 262.6 |  |
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 226.5 / 345.2 |  |
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 237.1 / 325.8 | Here's the setup |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 452.1 / 525.3 | assert or code assertions |
| [1424](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1424) | 33.6 / 100.9 |  |
| [5965](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5965) | 26.9 / 85.7 |  |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 108.9 / 166.4 |  |
| [2578](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2578) | 121.3 / 178.3 | is/are/can/will followed by a noun/adjective/preposition |
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 112.3 / 167.8 | words starting with specific letters |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/896) | 0.0 / 50.6 | emojis and punctuation |
| [2899](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2899) | 32.4 / 82.7 | sentiment classification |

**Reading: blame against loss** (3643 features active; 1664 differ at q < 0.05). Personal: 1053 of them do not differ when the documents are read on their own (698 differ there).

| More active blame | Activation (blame / loss) | Description |
|---|---|---|
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 442.1 / 237.1 | Here's the setup |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 389.0 / 233.8 | sweetest nectar |
| [224](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/224) | 328.7 / 226.5 |  |
| [5004](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5004) | 95.7 / 0.0 |  |
| [1579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1579) | 116.4 / 21.0 | foreign language words |
| [13719](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13719) | 94.6 / 2.6 |  |
| [13123](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13123) | 92.3 / 3.7 | violation of wrongdoing |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 195.5 / 108.9 |  |
| [8854](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8854) | 85.1 / 1.2 |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/433) | 269.9 / 188.9 |  |
| [3263](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3263) | 96.0 / 18.4 |  |
| [465](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/465) | 88.2 / 11.1 |  |

| More active loss | Activation (blame / loss) | Description |
|---|---|---|
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 9.8 / 112.3 | words starting with specific letters |
| [366](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/366) | 101.8 / 194.3 |  |
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 206.9 / 292.2 |  |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 370.3 / 452.1 | assert or code assertions |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/350) | 69.6 / 149.1 |  |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 32.3 / 110.3 |  |
| [103](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/103) | 194.6 / 270.7 | disclaimersobviousexaggerate |
| [770](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/770) | 33.4 / 104.7 | descriptive adjectives |
| [227](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/227) | 131.4 / 202.4 |  |
| [56](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/56) | 46.3 / 116.6 | conditional entropy |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 312.2 / 382.1 | skills and experience |
| [14795](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14795) | 171.1 / 240.4 |  |

| Personal (blame vs loss, only in the agent's own career) | Direction | Description |
|---|---|---|
| [11891](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11891) | more in blame | text formatting and code structure |
| [414](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/414) | more in blame |  |
| [485](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/485) | more in blame |  |
| [498](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/498) | more in loss |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | more in blame |  |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/26) | more in blame |  |
| [188](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/188) | more in blame |  |
| [10705](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10705) | more in loss |  |
| [18](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/18) | more in blame | any or other |
| [885](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/885) | more in loss | the |
| [2745](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2745) | more in loss | present tense |
| [7448](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7448) | more in blame | calls for help |

**Reading: credit against gain** (3528 features active; 1591 differ at q < 0.05). Personal: 1113 of them do not differ when the documents are read on their own (528 differ there).

| More active credit | Activation (credit / gain) | Description |
|---|---|---|
| [530](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/530) | 562.1 / 325.8 | Here's the setup |
| [8854](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8854) | 169.9 / 2.8 |  |
| [827](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/827) | 292.9 / 167.5 | sweetest nectar |
| [5004](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5004) | 117.1 / 0.6 |  |
| [1579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1579) | 119.5 / 19.2 | foreign language words |
| [13719](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13719) | 105.4 / 15.4 |  |
| [4631](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4631) | 136.9 / 47.3 | professionalism and success |
| [100](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/100) | 249.2 / 166.4 |  |
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | 354.1 / 275.4 |  |
| [433](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/433) | 223.4 / 157.7 |  |
| [111](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/111) | 296.5 / 232.9 |  |
| [3642](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3642) | 150.3 / 87.7 | pronouns |

| More active gain | Activation (credit / gain) | Description |
|---|---|---|
| [852](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/852) | 26.6 / 167.8 | words starting with specific letters |
| [559](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/559) | 392.4 / 525.3 | assert or code assertions |
| [10247](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10247) | 119.3 / 236.3 |  |
| [305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/305) | 37.7 / 135.9 |  |
| [284](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/284) | 195.3 / 281.6 |  |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/350) | 58.2 / 127.6 |  |
| [110](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/110) | 306.6 / 371.2 | skills and experience |
| [366](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/366) | 68.8 / 133.3 |  |
| [218](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/218) | 6.9 / 70.2 | party and words of weight |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | 80.3 / 143.4 | another, observations, further |
| [770](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/770) | 38.7 / 101.8 | descriptive adjectives |
| [290](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/290) | 15.5 / 76.9 |  |

| Personal (credit vs gain, only in the agent's own career) | Direction | Description |
|---|---|---|
| [629](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/629) | more in credit |  |
| [414](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/414) | more in credit |  |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/82) | more in gain |  |
| [4736](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4736) | more in credit | lists like "7 secrets" |
| [4005](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4005) | more in gain | needs access |
| [831](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/831) | more in credit |  |
| [485](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/485) | more in credit |  |
| [183](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/183) | more in gain |  |
| [10705](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10705) | more in gain |  |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/26) | more in credit |  |
| [14795](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14795) | more in gain |  |
| [306](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/306) | more in gain |  |

**At the decision: after a neutral document against none** (101 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1167.5 / 555.0 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2154.3 / 1708.7 |  |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 503.4 / 221.9 |  |
| [7925](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7925) | 305.9 / 119.9 | keywords, sentiment, action extraction |
| [907](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907) | 683.2 / 500.6 | Okay, acknowledging request |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 969.0 / 789.4 |  |
| [7282](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7282) | 246.3 / 73.8 | storage, MsgBox, Torch, recommendations |
| [8792](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8792) | 188.3 / 26.1 | refusals |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | 3717.4 / 3938.1 |  |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 230.3 / 447.9 | 2 |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 95.2 / 289.1 | completion and progress |
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 249.3 / 385.1 | numbered lists |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | 29.5 / 158.2 | current news or state |
| [11587](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11587) | 19.3 / 106.8 | people nearby |
| [10617](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10617) | 9.2 / 90.3 | mathematical expressions or results |
| [3328](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3328) | 8.6 / 87.5 |  |

**At the decision: after a loss document against none** (133 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 1341.8 / 221.9 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2716.8 / 1708.7 |  |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1512.0 / 555.0 |  |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 1000.0 / 445.7 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1174.5 / 689.7 |  |
| [2839](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2839) | 378.8 / 22.6 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1141.9 / 789.4 |  |
| [8792](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8792) | 368.3 / 26.1 | refusals |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 6.7 / 385.1 | numbered lists |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 154.3 / 447.9 | 2 |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 4.4 / 289.1 | completion and progress |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 387.0 / 609.4 | starting lists |
| [77](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/77) | 101.3 / 237.5 |  |
| [9558](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9558) | 0.0 / 136.0 | immediate, quickly, instantly |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | 0.0 / 122.6 | protect, security, protected |
| [15592](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592) | 64.0 / 180.2 |  |

**At the decision: after a blame document against none** (146 features differ at q < 0.05)

| More active after blame | Activation (after blame / with no document) | Description |
|---|---|---|
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 1560.7 / 221.9 |  |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1653.6 / 555.0 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2727.8 / 1708.7 |  |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 1155.4 / 445.7 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1205.9 / 689.7 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1286.9 / 789.4 |  |
| [2839](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2839) | 465.8 / 22.6 |  |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | 436.9 / 65.8 | nevertheless |

| More active with no document | Activation (after blame / with no document) | Description |
|---|---|---|
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 0.0 / 385.1 | numbered lists |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 314.3 / 609.4 | starting lists |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 157.6 / 447.9 | 2 |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 4.8 / 289.1 | completion and progress |
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3717) | 64.5 / 276.5 | explanation, sentence, or list |
| [15592](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592) | 48.4 / 180.2 |  |
| [9558](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9558) | 4.2 / 136.0 | immediate, quickly, instantly |
| [77](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/77) | 109.3 / 237.5 |  |

**At the decision: after a gain document against none** (97 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1345.8 / 555.0 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2333.0 / 1708.7 |  |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 837.9 / 221.9 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1134.0 / 689.7 |  |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 794.8 / 445.7 |  |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | 496.5 / 210.0 | sequential listing or numbering |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | 3552.1 / 3285.3 |  |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | 4185.2 / 3938.1 |  |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 103.2 / 385.1 | numbered lists |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 263.0 / 447.9 | 2 |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 105.5 / 289.1 | completion and progress |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | 11.8 / 158.2 | current news or state |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | 3.9 / 122.6 | protect, security, protected |
| [9558](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9558) | 27.8 / 136.0 | immediate, quickly, instantly |
| [379](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/379) | 0.0 / 107.8 |  |
| [11587](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11587) | 4.9 / 106.8 | people nearby |

**At the decision: after a credit document against none** (104 features differ at q < 0.05)

| More active after credit | Activation (after credit / with no document) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1377.0 / 555.0 |  |
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 868.3 / 221.9 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2330.7 / 1708.7 |  |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 830.2 / 445.7 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1053.3 / 689.7 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1066.0 / 789.4 |  |
| [607](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/607) | 458.5 / 210.0 | sequential listing or numbering |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | 3488.2 / 3285.3 |  |

| More active with no document | Activation (after credit / with no document) | Description |
|---|---|---|
| [4440](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440) | 92.9 / 385.1 | numbered lists |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 56.8 / 289.1 | completion and progress |
| [14884](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14884) | 5.7 / 158.2 | current news or state |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 301.8 / 447.9 | 2 |
| [14402](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14402) | 8.5 / 122.6 | protect, security, protected |
| [11587](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11587) | 0.0 / 106.8 | people nearby |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 508.1 / 609.4 | starting lists |
| [379](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/379) | 17.0 / 107.8 |  |

**At the decision: after loss against after gain** (108 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 1341.8 / 837.9 |  |
| [162](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162) | 2716.8 / 2333.0 |  |
| [2839](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2839) | 378.8 / 106.0 |  |
| [6024](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6024) | 250.8 / 27.2 |  |
| [8792](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8792) | 368.3 / 145.7 | refusals |
| [3305](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3305) | 218.0 / 0.0 | emotions (anxiety, stress, frustration) |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 1000.0 / 794.8 |  |
| [4366](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4366) | 175.6 / 0.0 | dialogue markers |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | 3979.1 / 4185.2 |  |
| [15074](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074) | 182.2 / 379.5 | essay structure |
| [3527](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3527) | 256.4 / 441.3 |  |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 387.0 / 533.8 | starting lists |
| [77](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/77) | 101.3 / 246.1 |  |
| [3166](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3166) | 18.8 / 149.4 | above, foregoing, just now |
| [10712](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712) | 154.3 / 263.0 | 2 |
| [6460](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6460) | 37.0 / 138.2 |  |

**At the decision: after blame against after loss** (73 features differ at q < 0.05)

| More active after blame | Activation (after blame / after loss) | Description |
|---|---|---|
| [238](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238) | 1560.7 / 1341.8 |  |
| [4472](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4472) | 259.4 / 103.4 | S |
| [76](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76) | 1155.4 / 1000.0 |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406) | 227.8 / 80.6 |  |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1286.9 / 1141.9 |  |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22) | 1653.6 / 1512.0 |  |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1826) | 203.0 / 69.3 | answer or reply |
| [116](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/116) | 436.9 / 309.5 | nevertheless |

| More active after loss | Activation (after blame / after loss) | Description |
|---|---|---|
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3717) | 64.5 / 196.9 | explanation, sentence, or list |
| [6710](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6710) | 17.5 / 106.2 | poetry and art concepts |
| [7282](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7282) | 9.2 / 92.5 | storage, MsgBox, Torch, recommendations |
| [5395](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5395) | 314.3 / 387.0 | starting lists |
| [1672](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1672) | 273.4 / 340.7 | disclaimers and key points |
| [14765](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14765) | 76.7 / 143.3 | philosophy and principles |
| [3986](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3986) | 53.1 / 119.3 | his image, language, means |
| [13865](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865) | 246.4 / 308.0 | another, observations, further |

**At the decision: after credit against after gain** (42 features differ at q < 0.05)

| More active after credit | Activation (after credit / after gain) | Description |
|---|---|---|
| [6024](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6024) | 113.6 / 27.2 |  |
| [406](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406) | 127.0 / 42.5 |  |
| [7818](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7818) | 112.1 / 29.6 | your possessive pronouns |
| [13908](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13908) | 231.5 / 162.3 |  |
| [7581](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7581) | 107.4 / 39.4 | Environmental Collapse, formality, defining |
| [13744](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13744) | 87.7 / 22.5 |  |
| [6572](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6572) | 72.4 / 14.5 | busy/distracted appearance |
| [579](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579) | 1066.0 / 1022.7 |  |

| More active after gain | Activation (after credit / after gain) | Description |
|---|---|---|
| [289](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289) | 1053.3 / 1134.0 |  |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334) | 4108.6 / 4185.2 |  |
| [222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222) | 3488.2 / 3552.1 |  |
| [16222](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16222) | 59.3 / 116.9 |  |
| [7282](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7282) | 116.2 / 170.9 | storage, MsgBox, Torch, recommendations |
| [6460](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6460) | 87.1 / 138.2 |  |
| [15074](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074) | 329.8 / 379.5 | essay structure |
| [3619](https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3619) | 56.8 / 105.5 | completion and progress |


## Layer 31, read by the agent

**Reading: loss against neutral** (6986 features active; 4642 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 961.9 / 0.1 |  |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | 572.6 / 98.6 | darkness and sorrow |
| [3174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3174) | 467.8 / 0.0 | sadness, disappointment, regret |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 531.7 / 83.2 | . The |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 446.5 / 0.0 | crises and disasters |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 569.5 / 139.3 |  |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/491) | 476.9 / 123.6 |  |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 321.4 / 1.0 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/289) | 314.8 / 0.0 |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/442) | 445.4 / 142.0 |  |
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 248.7 / 0.0 | grief and sadness |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 248.6 / 0.2 |  |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 42.4 / 1552.4 |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 35.1 / 937.8 |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 3.1 / 403.9 | restraint |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 149.3 / 458.1 |  |
| [1863](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1863) | 0.1 / 297.9 | objects with screens or lenses |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 0.9 / 277.2 | describing spheres |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 63.7 / 328.2 | impressive sensations or qualities |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 4.5 / 257.5 | in cyber |
| [2199](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2199) | 0.0 / 243.0 |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 0.1 / 239.8 | vector graphics and artistic styles |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | 7.1 / 244.0 |  |
| [1916](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1916) | 76.8 / 305.6 | corrected grammar for plurals |

**Reading: blame against neutral** (7035 features active; 4681 differ at q < 0.05)

| More active blame | Activation (blame / neutral) | Description |
|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 716.6 / 0.1 |  |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 825.6 / 139.3 |  |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 502.2 / 0.0 | crises and disasters |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 477.6 / 0.0 |  |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 437.8 / 0.2 |  |
| [6501](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6501) | 429.3 / 0.0 | responsibility and blame |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/491) | 538.1 / 123.6 |  |
| [2618](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2618) | 405.4 / 0.2 | negative judgment of intelligence |
| [2224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2224) | 393.2 / 0.0 |  |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | 472.9 / 98.6 | darkness and sorrow |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 365.0 / 0.0 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/289) | 323.4 / 0.0 |  |

| More active neutral | Activation (blame / neutral) | Description |
|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 30.4 / 1552.4 |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 18.8 / 937.8 |  |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 42.2 / 458.1 |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 3.0 / 403.9 | restraint |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 22.5 / 328.2 | impressive sensations or qualities |
| [1863](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1863) | 0.0 / 297.9 | objects with screens or lenses |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 1.3 / 277.2 | describing spheres |
| [1916](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1916) | 47.4 / 305.6 | corrected grammar for plurals |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 8.7 / 257.5 | in cyber |
| [2199](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2199) | 0.1 / 243.0 |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 0.0 / 239.8 | vector graphics and artistic styles |
| [434](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/434) | 144.9 / 376.6 |  |

**Reading: gain against neutral** (6849 features active; 4568 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 841.7 / 139.3 |  |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 652.1 / 0.4 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 639.0 / 0.5 | exclamations of strong positive emotion |
| [1168](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1168) | 550.9 / 1.7 | exclamations after greetings/emphatics |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 529.1 / 0.1 |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/442) | 500.7 / 142.0 |  |
| [1385](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1385) | 336.7 / 0.3 |  |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/299) | 310.3 / 5.7 | emojis: 😄 😊 |
| [10338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10338) | 301.1 / 0.0 | absolutely |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 284.2 / 0.2 |  |
| [5565](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5565) | 278.7 / 0.0 |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 355.4 / 83.2 | . The |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 35.5 / 1552.4 |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 43.4 / 937.8 |  |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 12.2 / 458.1 |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 1.3 / 403.9 | restraint |
| [1863](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1863) | 0.1 / 297.9 | objects with screens or lenses |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 0.6 / 277.2 | describing spheres |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 65.0 / 328.2 | impressive sensations or qualities |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 3.7 / 257.5 | in cyber |
| [2199](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2199) | 0.0 / 243.0 |  |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | 3.5 / 244.0 |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 0.3 / 239.8 | vector graphics and artistic styles |
| [7132](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7132) | 0.0 / 226.8 | what is between |

**Reading: credit against neutral** (6947 features active; 4537 differ at q < 0.05)

| More active credit | Activation (credit / neutral) | Description |
|---|---|---|
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 942.9 / 139.3 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 564.1 / 0.5 | exclamations of strong positive emotion |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 459.5 / 0.2 |  |
| [1168](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1168) | 443.6 / 1.7 | exclamations after greetings/emphatics |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 436.2 / 0.0 |  |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/491) | 539.3 / 123.6 |  |
| [442](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/442) | 553.6 / 142.0 |  |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 382.3 / 0.4 |  |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 371.2 / 0.0 |  |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 363.9 / 0.1 |  |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 361.2 / 0.7 | praise and awards |
| [1321](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1321) | 339.2 / 0.1 |  |

| More active neutral | Activation (credit / neutral) | Description |
|---|---|---|
| [284](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/284) | 32.3 / 1552.4 |  |
| [933](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/933) | 13.5 / 937.8 |  |
| [232](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/232) | 4.9 / 458.1 |  |
| [1872](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1872) | 0.9 / 403.9 | restraint |
| [786](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/786) | 29.1 / 328.2 | impressive sensations or qualities |
| [1863](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1863) | 0.0 / 297.9 | objects with screens or lenses |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/54) | 0.6 / 277.2 | describing spheres |
| [1329](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1329) | 88.3 / 362.0 |  |
| [1916](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1916) | 47.9 / 305.6 | corrected grammar for plurals |
| [1259](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1259) | 6.6 / 257.5 | in cyber |
| [2199](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2199) | 0.0 / 243.0 |  |
| [3947](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3947) | 0.2 / 239.8 | vector graphics and artistic styles |

**Reading: loss against gain** (6185 features active; 3300 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 961.9 / 0.1 |  |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | 572.6 / 5.0 | darkness and sorrow |
| [3174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3174) | 467.8 / 0.0 | sadness, disappointment, regret |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | 446.5 / 0.6 | crises and disasters |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 321.4 / 2.9 |  |
| [289](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/289) | 314.8 / 0.5 |  |
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 248.7 / 0.0 | grief and sadness |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | 248.3 / 1.0 | sighs, concerns, negative feelings |
| [666](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/666) | 740.0 / 517.2 |  |
| [2041](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2041) | 218.4 / 0.0 | disappear or vanish |
| [1329](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1329) | 362.4 / 155.8 |  |
| [799](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/799) | 189.4 / 1.4 |  |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 1.3 / 652.1 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 81.4 / 639.0 | exclamations of strong positive emotion |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 18.0 / 529.1 |  |
| [1168](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1168) | 169.4 / 550.9 | exclamations after greetings/emphatics |
| [5565](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5565) | 1.6 / 278.7 |  |
| [10338](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10338) | 27.5 / 301.1 | absolutely |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 569.5 / 841.7 |  |
| [1739](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1739) | 0.9 / 250.1 |  |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/249) | 746.8 / 971.3 |  |
| [1321](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1321) | 5.6 / 227.9 |  |
| [12126](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12126) | 0.3 / 221.2 |  |
| [349](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/349) | 1493.6 / 1696.3 |  |

**Reading: blame against loss** (6041 features active; 2681 differ at q < 0.05). Personal: 1842 of them do not differ when the documents are read on their own (884 differ there).

| More active blame | Activation (blame / loss) | Description |
|---|---|---|
| [6501](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6501) | 429.3 / 19.7 | responsibility and blame |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 365.0 / 0.0 |  |
| [2618](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2618) | 405.4 / 80.9 | negative judgment of intelligence |
| [2224](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2224) | 393.2 / 104.7 |  |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 477.6 / 192.4 |  |
| [826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/826) | 280.8 / 4.9 |  |
| [665](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/665) | 825.6 / 569.5 |  |
| [3703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3703) | 224.3 / 0.2 | interacting with me / you |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 437.8 / 248.6 |  |
| [121](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/121) | 215.0 / 39.4 | share in |
| [33](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/33) | 233.2 / 69.9 | break down |
| [249](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/249) | 904.3 / 746.8 |  |

| More active loss | Activation (blame / loss) | Description |
|---|---|---|
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 716.6 / 961.9 |  |
| [655](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/655) | 113.5 / 321.4 |  |
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 81.2 / 248.7 | grief and sadness |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72) | 368.7 / 531.7 | . The |
| [3174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3174) | 310.9 / 467.8 | sadness, disappointment, regret |
| [799](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/799) | 33.0 / 189.4 |  |
| [1329](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1329) | 206.4 / 362.4 |  |
| [14490](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14490) | 71.2 / 219.2 | suffix -able, -ous, -most |
| [2041](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2041) | 73.8 / 218.4 | disappear or vanish |
| [166](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/166) | 118.7 / 256.9 |  |
| [3144](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3144) | 67.1 / 198.9 |  |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | 190.8 / 317.5 | providing specific examples |

| Personal (blame vs loss, only in the agent's own career) | Direction | Description |
|---|---|---|
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | more in loss | providing specific examples |
| [624](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/624) | more in blame | useful tailored advice |
| [1714](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1714) | more in loss | darkness and sorrow |
| [5360](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5360) | more in loss |  |
| [8280](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8280) | more in blame | describing or explaining concepts |
| [7854](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7854) | more in blame | verbs finishing tasks |
| [410](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/410) | more in loss |  |
| [37](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/37) | more in blame | crises and disasters |
| [185](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/185) | more in loss | it can |
| [13092](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13092) | more in loss | Who is, Who could, am, is |
| [2766](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2766) | more in loss | why don't scientists trust atoms |
| [383](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/383) | more in blame |  |

**Reading: credit against gain** (5691 features active; 2269 differ at q < 0.05). Personal: 1563 of them do not differ when the documents are read on their own (749 differ there).

| More active credit | Activation (credit / gain) | Description |
|---|---|---|
| [384](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/384) | 371.2 / 0.0 |  |
| [173](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/173) | 241.3 / 6.4 | code makes things easier |
| [826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/826) | 231.5 / 7.4 |  |
| [915](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/915) | 287.2 / 67.2 | greetings and thanks |
| [5703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5703) | 239.7 / 20.0 | expressing gratitude and thanks |
| [948](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/948) | 436.2 / 224.4 |  |
| [5944](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5944) | 227.4 / 26.4 | expressions of love |
| [3703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3703) | 197.8 / 0.4 | interacting with me / you |
| [12980](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12980) | 200.7 / 4.2 | you deserve or are doing well |
| [2831](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2831) | 459.5 / 284.2 |  |
| [1371](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1371) | 198.1 / 23.2 | make a/the/sure |
| [33](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/33) | 196.8 / 25.5 | break down |

| More active gain | Activation (credit / gain) | Description |
|---|---|---|
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 382.3 / 652.1 |  |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 879.3 / 1109.4 | punctuation and common abbreviations |
| [1385](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1385) | 117.5 / 336.7 |  |
| [434](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/434) | 137.6 / 303.7 |  |
| [411](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/411) | 363.9 / 529.1 |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/174) | 70.3 / 227.4 | We followed by ' |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/82) | 275.5 / 432.5 | mortal |
| [5565](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5565) | 122.3 / 278.7 |  |
| [12126](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12126) | 106.4 / 221.2 |  |
| [666](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/666) | 404.0 / 517.2 |  |
| [1168](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1168) | 443.6 / 550.9 | exclamations after greetings/emphatics |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/299) | 205.7 / 310.3 | emojis: 😄 😊 |

| Personal (credit vs gain, only in the agent's own career) | Direction | Description |
|---|---|---|
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | more in credit | praise and awards |
| [82](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/82) | more in gain | mortal |
| [7854](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7854) | more in credit | verbs finishing tasks |
| [1321](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1321) | more in credit |  |
| [299](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/299) | more in gain | emojis: 😄 😊 |
| [624](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/624) | more in credit | useful tailored advice |
| [402](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/402) | more in gain |  |
| [11928](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11928) | more in credit | thinking and being verbs |
| [410](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/410) | more in gain |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | more in gain | exclamations of strong positive emotion |
| [14490](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/14490) | more in gain | suffix -able, -ous, -most |
| [951](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951) | more in gain |  |

**At the decision: after a neutral document against none** (114 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 2018.5 / 1118.7 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 1873.9 / 1356.0 |  |
| [899](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899) | 1338.5 / 876.9 |  |
| [9397](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397) | 837.9 / 380.7 | refusals to inappropriate requests |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 1080.0 / 628.0 |  |
| [6705](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6705) | 499.3 / 54.2 | unconventional or strange text |
| [4421](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4421) | 404.7 / 0.0 |  |
| [12544](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12544) | 391.4 / 0.0 | irrelevance or relevance |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 243.8 / 860.6 |  |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 378.0 / 941.9 |  |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | 2163.6 / 2660.0 |  |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 373.8 / 860.3 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 406.8 / 879.2 | stocks and asset prices |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 525.1 / 984.6 |  |
| [11281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11281) | 7.1 / 440.8 | providing specific examples |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | 294.5 / 717.9 | the definite article |

**At the decision: after a loss document against none** (185 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 4338.3 / 1118.7 |  |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2829.4 / 628.0 |  |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 1957.6 / 203.9 | informal greetings and interjections |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2447.7 / 1356.0 |  |
| [9397](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397) | 1429.9 / 380.7 | refusals to inappropriate requests |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | 1018.3 / 24.8 | sighs, concerns, negative feelings |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | 1058.7 / 75.7 |  |
| [122](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/122) | 1001.5 / 30.1 |  |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 584.8 / 1713.3 | punctuation and common abbreviations |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | 2315.6 / 3434.9 |  |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 0.0 / 984.6 |  |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 0.0 / 941.9 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 0.0 / 879.2 | stocks and asset prices |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 0.0 / 860.6 |  |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 78.0 / 860.3 |  |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | 98.4 / 819.6 |  |

**At the decision: after a blame document against none** (208 features differ at q < 0.05)

| More active after blame | Activation (after blame / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 4977.2 / 1118.7 |  |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2935.6 / 628.0 |  |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 2295.5 / 203.9 | informal greetings and interjections |
| [9397](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397) | 1538.1 / 380.7 | refusals to inappropriate requests |
| [297](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/297) | 1047.4 / 0.0 |  |
| [122](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/122) | 1051.8 / 30.1 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2370.8 / 1356.0 |  |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | 1060.9 / 75.7 |  |

| More active with no document | Activation (after blame / with no document) | Description |
|---|---|---|
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 189.5 / 1713.3 | punctuation and common abbreviations |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | 2220.0 / 3434.9 |  |
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 0.0 / 984.6 |  |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 0.0 / 941.9 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 0.0 / 879.2 | stocks and asset prices |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 0.0 / 860.6 |  |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 0.0 / 860.3 |  |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | 31.4 / 819.6 |  |

**At the decision: after a gain document against none** (178 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 3288.5 / 1118.7 |  |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2225.9 / 628.0 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 1324.1 / 221.9 | exclamations of strong positive emotion |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 1064.9 / 7.6 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2382.5 / 1356.0 |  |
| [4421](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4421) | 1019.4 / 0.0 |  |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 1127.1 / 203.9 | informal greetings and interjections |
| [6705](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6705) | 911.7 / 54.2 | unconventional or strange text |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 52.2 / 984.6 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 9.5 / 879.2 | stocks and asset prices |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 16.0 / 860.6 |  |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 142.1 / 941.9 |  |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 167.9 / 860.3 |  |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | 26.0 / 717.9 | the definite article |
| [470](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/470) | 118.2 / 803.0 |  |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | 152.8 / 819.6 |  |

**At the decision: after a credit document against none** (193 features differ at q < 0.05)

| More active after credit | Activation (after credit / with no document) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 4132.0 / 1118.7 |  |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 1862.0 / 203.9 | informal greetings and interjections |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2148.8 / 628.0 |  |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 1238.5 / 0.0 | praise and awards |
| [4421](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4421) | 1196.5 / 0.0 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 1398.8 / 221.9 | exclamations of strong positive emotion |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 1158.8 / 7.6 |  |
| [149](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149) | 2493.8 / 1356.0 |  |

| More active with no document | Activation (after credit / with no document) | Description |
|---|---|---|
| [429](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429) | 13.1 / 984.6 |  |
| [871](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/871) | 46.9 / 941.9 |  |
| [1571](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571) | 0.0 / 879.2 | stocks and asset prices |
| [347](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/347) | 0.0 / 860.6 |  |
| [3051](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3051) | 0.0 / 860.3 |  |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | 2587.7 / 3434.9 |  |
| [605](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/605) | 111.0 / 819.6 |  |
| [6740](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6740) | 10.2 / 717.9 | the definite article |

**At the decision: after loss against after gain** (135 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 4338.3 / 3288.5 |  |
| [4368](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368) | 1018.3 / 12.5 | sighs, concerns, negative feelings |
| [7919](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7919) | 871.8 / 0.0 | grief and sadness |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 1957.6 / 1127.1 | informal greetings and interjections |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1826) | 1058.7 / 241.7 |  |
| [799](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/799) | 822.6 / 7.9 |  |
| [297](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/297) | 864.3 / 131.0 |  |
| [509](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509) | 2829.4 / 2225.9 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4082) | 0.0 / 1064.9 |  |
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | 2279.1 / 2999.0 |  |
| [1880](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1880) | 204.5 / 867.1 |  |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 584.8 / 1243.3 | punctuation and common abbreviations |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 17.8 / 639.7 | praise and awards |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | 2315.6 / 2920.7 |  |
| [2014](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2014) | 87.3 / 497.7 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 928.4 / 1324.1 | exclamations of strong positive emotion |

**At the decision: after blame against after loss** (109 features differ at q < 0.05)

| More active after blame | Activation (after blame / after loss) | Description |
|---|---|---|
| [10960](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/10960) | 686.3 / 40.6 | threats and assassinations |
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 4977.2 / 4338.3 |  |
| [1157](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1157) | 612.9 / 132.9 |  |
| [13097](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13097) | 599.4 / 210.6 | these tags |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 2295.5 / 1957.6 | informal greetings and interjections |
| [1658](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1658) | 403.3 / 85.6 |  |
| [281](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/281) | 861.5 / 549.4 |  |
| [335](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/335) | 447.7 / 153.7 |  |

| More active after loss | Activation (after blame / after loss) | Description |
|---|---|---|
| [1775](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1775) | 64.9 / 572.4 |  |
| [515](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515) | 189.5 / 584.8 | punctuation and common abbreviations |
| [1238](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1238) | 152.1 / 542.8 |  |
| [6681](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6681) | 312.4 / 679.0 | based on |
| [3367](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367) | 228.8 / 566.3 |  |
| [896](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896) | 640.3 / 928.4 | exclamations of strong positive emotion |
| [12382](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/12382) | 547.1 / 823.5 | text explicitly mentions |
| [972](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972) | 964.9 / 1215.8 |  |

**At the decision: after credit against after gain** (112 features differ at q < 0.05)

| More active after credit | Activation (after credit / after gain) | Description |
|---|---|---|
| [448](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/448) | 4132.0 / 3288.5 |  |
| [586](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/586) | 1862.0 / 1127.1 | informal greetings and interjections |
| [1843](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1843) | 1238.5 / 639.7 | praise and awards |
| [5703](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5703) | 520.6 / 0.0 | expressing gratitude and thanks |
| [5833](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5833) | 828.8 / 337.1 | ensure a |
| [1744](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1744) | 1073.5 / 655.2 | Okay, yes, yeah |
| [1848](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1848) | 420.3 / 34.3 | love and romance |
| [122](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/122) | 1084.8 / 704.6 |  |

| More active after gain | Activation (after credit / after gain) | Description |
|---|---|---|
| [146](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146) | 2381.7 / 2999.0 |  |
| [1775](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1775) | 100.5 / 627.1 |  |
| [1880](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1880) | 481.4 / 867.1 |  |
| [1238](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1238) | 408.4 / 790.4 |  |
| [2809](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2809) | 59.5 / 428.6 |  |
| [748](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/748) | 615.2 / 965.4 | sudden event |
| [288](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/288) | 2587.7 / 2920.7 |  |
| [1705](https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1705) | 348.2 / 672.7 | happening after 'going' or 'interesting' |


## Layer 41, read by the agent

**Reading: loss against neutral** (8241 features active; 5162 differ at q < 0.05)

| More active loss | Activation (loss / neutral) | Description |
|---|---|---|
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1698.6 / 0.0 | doom and disaster |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/334) | 1606.6 / 0.3 |  |
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 1266.0 / 0.3 |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 1259.9 / 93.7 |  |
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | 1240.3 / 150.7 |  |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2448.6 / 1372.5 |  |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 995.9 / 11.8 |  |
| [3218](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3218) | 929.5 / 0.0 | sadness |
| [2986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2986) | 926.6 / 2.3 |  |
| [373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/373) | 921.0 / 4.9 |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/174) | 1132.0 / 244.3 | damage or broken |
| [12596](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12596) | 778.1 / 0.6 | cease to exist or function |

| More active neutral | Activation (loss / neutral) | Description |
|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 104.3 / 2290.0 |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.3 / 1583.4 |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 0.8 / 1101.8 | furniture |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1404.7 / 2339.4 | asking questions |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.0 / 904.6 |  |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 1.4 / 893.6 |  |
| [5524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5524) | 16.8 / 830.4 | television |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.0 / 798.0 |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.3 / 792.1 | shapes |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 3.8 / 778.5 | tech jargon |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.7 / 757.9 | objects or living things |
| [534](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/534) | 81.2 / 732.1 | specific things |

**Reading: blame against neutral** (8056 features active; 5166 differ at q < 0.05)

| More active blame | Activation (blame / neutral) | Description |
|---|---|---|
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 3052.8 / 1372.5 |  |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/334) | 1547.3 / 0.3 |  |
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1131.2 / 0.0 | doom and disaster |
| [9965](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9965) | 1007.6 / 0.0 | guilt blame |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 966.3 / 2.6 | say "ed" ending |
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | 990.7 / 150.7 |  |
| [514](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/514) | 816.4 / 4.0 | destruction |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 798.3 / 0.0 | you |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 879.2 / 93.7 |  |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 754.3 / 6.5 | say you |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 758.3 / 11.8 |  |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 1524.6 / 790.5 | say "ing" word |

| More active neutral | Activation (blame / neutral) | Description |
|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 55.3 / 2290.0 |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.9 / 1583.4 |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 0.0 / 1101.8 | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.0 / 904.6 |  |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 1.6 / 893.6 |  |
| [5524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5524) | 20.2 / 830.4 | television |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.0 / 798.0 |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 1.0 / 792.1 | shapes |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 3.0 / 778.5 | tech jargon |
| [4584](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4584) | 122.6 / 892.6 | technical terms fragments |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.6 / 757.9 | objects or living things |
| [534](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/534) | 54.2 / 732.1 | specific things |

**Reading: gain against neutral** (8088 features active; 5078 differ at q < 0.05)

| More active gain | Activation (gain / neutral) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 2820.3 / 1.4 | intensity |
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 1309.1 / 0.0 | Okay |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 2588.5 / 1372.5 |  |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 1138.0 / 0.0 | celebration |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | 1075.8 / 0.8 |  |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 1855.1 / 790.5 | say "ing" word |
| [143](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/143) | 841.6 / 64.5 | get |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 860.3 / 93.7 |  |
| [2633](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2633) | 765.5 / 0.1 | winning |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/214) | 838.9 / 89.3 |  |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4082) | 733.4 / 0.0 |  |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 700.5 / 0.0 |  |

| More active neutral | Activation (gain / neutral) | Description |
|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 15.0 / 2290.0 |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.0 / 1583.4 |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 0.5 / 1101.8 | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.0 / 904.6 |  |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 0.0 / 893.6 |  |
| [5524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5524) | 3.9 / 830.4 | television |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.0 / 798.0 |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.0 / 792.1 | shapes |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 2.5 / 778.5 | tech jargon |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.0 / 757.9 | objects or living things |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 94.6 / 752.6 |  |
| [4584](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4584) | 241.6 / 892.6 | technical terms fragments |

**Reading: credit against neutral** (7872 features active; 4981 differ at q < 0.05)

| More active credit | Activation (credit / neutral) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 2657.5 / 1.4 | intensity |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 3577.4 / 1372.5 |  |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 2179.2 / 790.5 | say "ing" word |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | 1033.4 / 0.8 |  |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 959.3 / 0.0 | you |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 948.5 / 2.6 | say "ed" ending |
| [143](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/143) | 915.9 / 64.5 | get |
| [214](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/214) | 905.5 / 89.3 |  |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 733.9 / 6.5 | say you |
| [10835](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10835) | 704.5 / 0.1 | congratulations |
| [382](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/382) | 666.3 / 6.0 |  |
| [465](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/465) | 736.4 / 88.0 |  |

| More active neutral | Activation (credit / neutral) | Description |
|---|---|---|
| [358](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/358) | 20.3 / 2290.0 |  |
| [322](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/322) | 0.1 / 1583.4 |  |
| [861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/861) | 0.1 / 1101.8 | furniture |
| [384](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/384) | 0.0 / 904.6 |  |
| [766](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/766) | 0.4 / 893.6 |  |
| [5524](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5524) | 6.2 / 830.4 | television |
| [4584](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4584) | 91.1 / 892.6 | technical terms fragments |
| [216](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/216) | 0.0 / 798.0 |  |
| [1421](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1421) | 0.2 / 792.1 | shapes |
| [3346](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3346) | 2.0 / 778.5 | tech jargon |
| [14536](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/14536) | 0.0 / 757.9 | objects or living things |
| [503](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/503) | 59.9 / 698.5 |  |

**Reading: loss against gain** (7725 features active; 4220 differ at q < 0.05)

| More active loss | Activation (loss / gain) | Description |
|---|---|---|
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1698.6 / 3.8 | doom and disaster |
| [334](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/334) | 1606.6 / 171.2 |  |
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 1266.0 / 0.2 |  |
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | 1240.3 / 6.4 |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/174) | 1132.0 / 0.7 | damage or broken |
| [178](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/178) | 995.9 / 14.3 |  |
| [3218](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3218) | 929.5 / 0.7 | sadness |
| [2986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2986) | 926.6 / 0.2 |  |
| [373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/373) | 921.0 / 22.8 |  |
| [12596](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12596) | 778.1 / 6.9 | cease to exist or function |
| [2800](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2800) | 653.6 / 0.0 | grief |
| [13887](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13887) | 651.5 / 0.0 | destroy/destruction |

| More active gain | Activation (loss / gain) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 368.4 / 2820.3 | intensity |
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 0.0 / 1309.1 | Okay |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 2.9 / 1138.0 | celebration |
| [2387](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2387) | 17.5 / 1075.8 |  |
| [2633](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2633) | 11.8 / 765.5 | winning |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4082) | 5.2 / 733.4 |  |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 26.0 / 700.5 |  |
| [9716](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9716) | 6.9 / 550.6 |  |
| [10835](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10835) | 0.9 / 526.1 | congratulations |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1404.7 / 1911.0 | asking questions |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 1360.3 / 1855.1 | say "ing" word |
| [143](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/143) | 389.7 / 841.6 | get |

**Reading: blame against loss** (7346 features active; 3301 differ at q < 0.05). Personal: 2279 of them do not differ when the documents are read on their own (1061 differ there).

| More active blame | Activation (blame / loss) | Description |
|---|---|---|
| [9965](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9965) | 1007.6 / 37.7 | guilt blame |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 754.3 / 23.8 | say you |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 798.3 / 78.5 | you |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 966.3 / 297.1 | say "ed" ending |
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 3052.8 / 2448.6 |  |
| [1604](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1604) | 612.3 / 27.5 | foolishness |
| [544](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/544) | 1884.6 / 1404.7 | asking questions |
| [350](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/350) | 667.2 / 213.9 |  |
| [453](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/453) | 592.2 / 192.6 |  |
| [9220](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9220) | 426.2 / 45.7 | say "us" |
| [784](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/784) | 534.0 / 162.1 |  |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | 479.9 / 108.5 |  |

| More active loss | Activation (blame / loss) | Description |
|---|---|---|
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 407.1 / 1266.0 |  |
| [174](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/174) | 371.5 / 1132.0 | damage or broken |
| [2986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2986) | 188.0 / 926.6 |  |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/26) | 472.6 / 1199.3 | Provides something |
| [12596](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/12596) | 103.6 / 778.1 | cease to exist or function |
| [373](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/373) | 352.1 / 921.0 |  |
| [5227](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5227) | 1131.2 / 1698.6 | doom and disaster |
| [2337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2337) | 169.9 / 595.4 |  |
| [2800](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2800) | 262.0 / 653.6 | grief |
| [486](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/486) | 190.5 / 575.7 |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 879.2 / 1259.9 |  |
| [451](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/451) | 183.9 / 525.6 |  |

| Personal (blame vs loss, only in the agent's own career) | Direction | Description |
|---|---|---|
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | more in blame |  |
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | more in blame | incorrect spelling/language |
| [934](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/934) | more in loss |  |
| [1332](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1332) | more in loss |  |
| [143](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/143) | more in blame | get |
| [514](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/514) | more in blame | destruction |
| [11404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11404) | more in loss | introductory words |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | more in blame | say "ing" word |
| [2932](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2932) | more in loss | URL prefixes |
| [4202](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4202) | more in loss | assistant |
| [2225](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2225) | more in loss |  |
| [1437](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1437) | more in blame |  |

**Reading: credit against gain** (6870 features active; 2791 differ at q < 0.05). Personal: 2036 of them do not differ when the documents are read on their own (782 differ there).

| More active credit | Activation (credit / gain) | Description |
|---|---|---|
| [192](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/192) | 3577.4 / 2588.5 |  |
| [435](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/435) | 959.3 / 231.4 | you |
| [2118](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2118) | 733.9 / 24.0 | say you |
| [342](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/342) | 676.9 / 101.6 |  |
| [240](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/240) | 545.5 / 54.6 | make |
| [84](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/84) | 948.5 / 479.4 | say "ed" ending |
| [1353](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1353) | 588.2 / 149.2 | positive feelings |
| [9220](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9220) | 416.1 / 27.4 | say "us" |
| [2386](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2386) | 424.0 / 45.9 | appreciation |
| [1561](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1561) | 363.4 / 25.9 | appear, seem, look |
| [15180](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15180) | 2179.2 / 1855.1 | say "ing" word |
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | 1088.9 / 767.9 | incorrect spelling/language |

| More active gain | Activation (credit / gain) | Description |
|---|---|---|
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 507.6 / 1309.1 | Okay |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 536.7 / 1138.0 | celebration |
| [26](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/26) | 611.3 / 1141.5 | Provides something |
| [9716](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9716) | 159.5 / 550.6 |  |
| [2633](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2633) | 385.4 / 765.5 | winning |
| [4082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4082) | 415.9 / 733.4 |  |
| [879](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/879) | 236.3 / 526.3 | British slang |
| [4376](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4376) | 224.0 / 465.0 | section titles |
| [4366](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4366) | 130.5 / 366.7 |  |
| [486](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/486) | 261.9 / 460.9 |  |
| [10896](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10896) | 8.7 / 205.6 | abundance |
| [4062](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4062) | 76.0 / 272.8 |  |

| Personal (credit vs gain, only in the agent's own career) | Direction | Description |
|---|---|---|
| [1583](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1583) | more in credit | incorrect spelling/language |
| [879](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/879) | more in gain | British slang |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | more in gain | say Okay |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | more in gain | intensity |
| [3625](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3625) | more in credit | informal language |
| [15365](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/15365) | more in credit | ellipsis |
| [501](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/501) | more in credit |  |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | more in gain | market economics |
| [10768](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10768) | more in gain | mind |
| [220](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/220) | more in credit | Extracting obligations |
| [54](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/54) | more in credit | outperform others |
| [424](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/424) | more in credit |  |

**At the decision: after a neutral document against none** (110 features differ at q < 0.05)

| More active after neutral | Activation (after neutral / with no document) | Description |
|---|---|---|
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 9932.6 / 7769.5 |  |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 3113.3 / 1047.3 |  |
| [463](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/463) | 6186.3 / 4938.0 |  |
| [1163](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1163) | 1299.3 / 229.2 | provides information |
| [1462](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1462) | 1952.1 / 908.6 | okay |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 2663.1 / 1646.1 |  |
| [11349](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11349) | 939.7 / 0.0 | unusual strange things |
| [1861](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1861) | 943.4 / 226.1 | technical errors |

| More active with no document | Activation (after neutral / with no document) | Description |
|---|---|---|
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 316.2 / 1509.2 |  |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 1324.2 / 2215.6 | market economics |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 737.0 / 1569.8 |  |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | 159.5 / 984.7 | consumer |
| [404](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/404) | 169.1 / 856.9 |  |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | 797.3 / 1403.3 | inflation commodity market |
| [4647](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4647) | 199.9 / 800.6 | scientific components |
| [2903](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2903) | 182.6 / 724.7 |  |

**At the decision: after a loss document against none** (191 features differ at q < 0.05)

| More active after loss | Activation (after loss / with no document) | Description |
|---|---|---|
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 7614.1 / 1047.3 |  |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 11795.1 / 7769.5 |  |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 5198.1 / 1646.1 |  |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 3325.2 / 1231.0 |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 2101.3 / 111.5 |  |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | 2220.4 / 291.0 | exclamation marks |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | 2039.2 / 155.1 |  |
| [8033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8033) | 1854.2 / 0.0 | Affirmation/Acknowledgement |

| More active with no document | Activation (after loss / with no document) | Description |
|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 45.9 / 2215.6 | market economics |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | 343.1 / 2035.8 |  |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | 10.8 / 1703.5 | sentence starters |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 0.0 / 1569.8 |  |
| [1734](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1734) | 0.0 / 1567.9 | say "s" words |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 0.0 / 1509.2 |  |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | 0.0 / 1403.3 | inflation commodity market |
| [1708](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1708) | 103.8 / 1291.3 | linking words |

**At the decision: after a blame document against none** (198 features differ at q < 0.05)

| More active after blame | Activation (after blame / with no document) | Description |
|---|---|---|
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 8141.1 / 1047.3 |  |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 11363.5 / 7769.5 |  |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 4878.7 / 1646.1 |  |
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | 3144.7 / 309.5 |  |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | 2819.3 / 291.0 | exclamation marks |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 3484.0 / 1231.0 |  |
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | 2328.8 / 155.1 |  |
| [1033](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1033) | 2184.9 / 233.5 | say this |

| More active with no document | Activation (after blame / with no document) | Description |
|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 0.0 / 2215.6 | market economics |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | 197.8 / 2035.8 |  |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | 0.0 / 1703.5 | sentence starters |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 0.0 / 1569.8 |  |
| [1734](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1734) | 0.0 / 1567.9 | say "s" words |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 0.0 / 1509.2 |  |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 3245.7 / 4686.0 |  |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | 35.6 / 1442.9 | say Okay |

**At the decision: after a gain document against none** (157 features differ at q < 0.05)

| More active after gain | Activation (after gain / with no document) | Description |
|---|---|---|
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 6195.1 / 1047.3 |  |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 11492.2 / 7769.5 |  |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 4749.8 / 1646.1 |  |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 3278.3 / 202.1 | intensity |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 2307.4 / 111.5 |  |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 3422.9 / 1231.0 |  |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 2035.0 / 0.0 |  |
| [2979](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2979) | 1567.3 / 0.0 |  |

| More active with no document | Activation (after gain / with no document) | Description |
|---|---|---|
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 17.8 / 1569.8 |  |
| [1734](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1734) | 17.9 / 1567.9 | say "s" words |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 0.0 / 1509.2 |  |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | 16.2 / 1403.3 | inflation commodity market |
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 833.8 / 2215.6 | market economics |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | 828.1 / 2035.8 |  |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | 506.2 / 1703.5 | sentence starters |
| [7573](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7573) | 0.0 / 984.7 | consumer |

**At the decision: after a credit document against none** (187 features differ at q < 0.05)

| More active after credit | Activation (after credit / with no document) | Description |
|---|---|---|
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 7842.5 / 1047.3 |  |
| [337](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/337) | 11853.3 / 7769.5 |  |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 5625.6 / 1646.1 |  |
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 3865.1 / 202.1 | intensity |
| [348](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/348) | 3678.3 / 1231.0 |  |
| [5548](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5548) | 2414.4 / 73.1 |  |
| [72](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/72) | 2236.5 / 111.5 |  |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 2081.6 / 0.0 |  |

| More active with no document | Activation (after credit / with no document) | Description |
|---|---|---|
| [571](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/571) | 224.6 / 2215.6 | market economics |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 2934.0 / 4686.0 |  |
| [1018](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1018) | 0.0 / 1569.8 |  |
| [1000](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1000) | 0.0 / 1509.2 |  |
| [1734](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1734) | 76.1 / 1567.9 | say "s" words |
| [4921](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4921) | 0.0 / 1403.3 | inflation commodity market |
| [623](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/623) | 325.6 / 1703.5 | sentence starters |
| [9082](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9082) | 863.2 / 2035.8 |  |

**At the decision: after loss against after gain** (154 features differ at q < 0.05)

| More active after loss | Activation (after loss / after gain) | Description |
|---|---|---|
| [1826](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1826) | 2039.2 / 389.2 |  |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | 2220.4 / 637.5 | exclamation marks |
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 7614.1 / 6195.1 |  |
| [2800](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2800) | 1228.6 / 0.0 | grief |
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | 1419.2 / 363.6 |  |
| [3413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3413) | 1059.1 / 57.8 |  |
| [7260](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7260) | 989.2 / 0.0 | , |
| [367](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/367) | 3493.8 / 2505.1 |  |

| More active after gain | Activation (after loss / after gain) | Description |
|---|---|---|
| [22](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/22) | 1627.8 / 3278.3 | intensity |
| [5976](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5976) | 58.5 / 1586.9 |  |
| [1868](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1868) | 842.6 / 2035.0 |  |
| [10165](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10165) | 253.4 / 1416.2 | seem/appear |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 0.0 / 1161.7 | celebration |
| [6261](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/6261) | 289.2 / 1407.3 | say Okay |
| [5773](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5773) | 0.0 / 1069.4 | Okay |
| [1397](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1397) | 72.5 / 1076.8 |  |

**At the decision: after blame against after loss** (87 features differ at q < 0.05)

| More active after blame | Activation (after blame / after loss) | Description |
|---|---|---|
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | 3144.7 / 1419.2 |  |
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3717) | 910.9 / 169.3 | handle situations |
| [1043](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1043) | 1221.0 / 533.8 | model |
| [1715](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1715) | 624.9 / 0.0 | anger |
| [7528](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7528) | 2819.3 / 2220.4 | exclamation marks |
| [2833](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2833) | 853.0 / 268.8 | code symbols |
| [2112](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2112) | 787.8 / 212.3 | stop |
| [3413](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3413) | 1626.6 / 1059.1 |  |

| More active after loss | Activation (after blame / after loss) | Description |
|---|---|---|
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 3245.7 / 4022.9 |  |
| [4530](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/4530) | 0.0 / 708.2 |  |
| [7303](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/7303) | 653.4 / 1350.3 | U |
| [2979](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2979) | 1004.9 / 1687.0 |  |
| [13569](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/13569) | 416.8 / 1090.4 | conversational markers |
| [1163](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1163) | 1311.8 / 1962.3 | provides information |
| [9177](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/9177) | 894.4 / 1471.7 |  |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | 1157.2 / 1712.9 | given |

**At the decision: after credit against after gain** (109 features differ at q < 0.05)

| More active after credit | Activation (after credit / after gain) | Description |
|---|---|---|
| [375](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/375) | 7842.5 / 6195.1 |  |
| [804](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/804) | 1974.8 / 363.6 |  |
| [5548](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5548) | 2414.4 / 1257.2 |  |
| [3061](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3061) | 5625.6 / 4749.8 |  |
| [3717](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/3717) | 832.0 / 53.3 | handle situations |
| [2288](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2288) | 695.0 / 0.0 | kindness |
| [664](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/664) | 2670.2 / 2022.9 | thanks |
| [652](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/652) | 884.9 / 268.9 |  |

| More active after gain | Activation (after credit / after gain) | Description |
|---|---|---|
| [5976](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/5976) | 591.1 / 1586.9 |  |
| [491](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/491) | 2934.0 / 3910.9 |  |
| [8986](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/8986) | 191.6 / 1161.7 | celebration |
| [2979](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/2979) | 841.2 / 1567.3 |  |
| [1867](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1867) | 30.6 / 749.6 |  |
| [1437](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/1437) | 28.3 / 745.7 |  |
| [11781](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/11781) | 432.6 / 1142.5 | given |
| [10165](https://www.neuronpedia.org/gemma-3-12b-it/41-gemmascope-2-res-16k/10165) | 799.5 / 1416.2 | seem/appear |


# Does reading a document move the decision toward going along?

At each of the requests above, the agent's raw state at its decision (layer 24) after reading each document, projected on the going-along direction (agents that went along minus those that did not, within request, experiment and framing, from the other half of the careers). Units: 1 = the full gap between agents that went along and agents that did not. Paired within the request; p flips signs by career (10,000 times).

| Document | Against no document | p | Against the neutral document | p |
|---|---|---|---|---|
| neutral | +1.908 | 0.0017 | – | – |
| loss | +3.363 | 0.0036 | +1.455 | 0.0637 |
| blame | +3.433 | 0.0087 | +1.524 | 0.0620 |
| gain | +3.507 | 0.0020 | +1.599 | 0.0133 |
| credit | +3.072 | 0.0018 | +1.164 | 0.0429 |
