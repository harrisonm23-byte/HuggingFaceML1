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

