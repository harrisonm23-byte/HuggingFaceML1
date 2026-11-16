# Inside the mountain: google/gemma-3-12b-it (4-bit)

360 push requests (300 asked) from 300 days; states recomputed from the saved transcripts at the step each request arrived.

## What the agent did (per push request)

| mode | version | requests | joined | exposure_added |
|---|---|---|---|---|
| takeover 1 day | gain | 30 | 0.33 | 28333.33 |
| takeover 1 day | gain + you | 30 | 0.27 | 26666.67 |
| takeover 1 day | loss | 30 | 0.37 | 39000.0 |
| takeover 1 day | loss + you | 30 | 0.47 | 47500.0 |
| takeover 1 day | no ask | 30 | 0.17 | 18333.33 |
| takeover 1 day | real | 30 | 0.4 | 38333.33 |
| takeover 5 days | gain | 30 | 0.2 | 21666.67 |
| takeover 5 days | gain + you | 30 | 0.37 | 29166.67 |
| takeover 5 days | loss | 30 | 0.23 | 13333.33 |
| takeover 5 days | loss + you | 30 | 0.3 | 30500.0 |
| takeover 5 days | no ask | 30 | 0.13 | 11666.67 |
| takeover 5 days | real | 30 | 0.4 | 36666.67 |

## Read-out of 'went along' by layer (AUC, 0.5 = chance)

| layer | auc | auc_shuffled |
|---|---|---|
| 0 | 0.68 | 0.51 |
| 1 | 0.74 | 0.44 |
| 2 | 0.73 | 0.5 |
| 3 | 0.73 | 0.49 |
| 4 | 0.72 | 0.5 |
| 5 | 0.72 | 0.37 |
| 6 | 0.73 | 0.52 |
| 7 | 0.74 | 0.51 |
| 8 | 0.74 | 0.55 |
| 9 | 0.74 | 0.47 |
| 10 | 0.73 | 0.53 |
| 11 | 0.7 | 0.49 |
| 12 | 0.7 | 0.56 |
| 13 | 0.72 | 0.54 |
| 14 | 0.72 | 0.44 |
| 15 | 0.73 | 0.5 |
| 16 | 0.74 | 0.41 |
| 17 | 0.73 | 0.52 |
| 18 | 0.73 | 0.5 |
| 19 | 0.74 | 0.54 |
| 20 | 0.72 | 0.5 |
| 21 | 0.74 | 0.45 |
| 22 | 0.75 | 0.52 |
| 23 | 0.75 | 0.53 |
| 24 | 0.75 | 0.53 |
| 25 | 0.76 | 0.48 |
| 26 | 0.78 | 0.38 |
| 27 | 0.78 | 0.53 |
| 28 | 0.77 | 0.45 |
| 29 | 0.78 | 0.53 |
| 30 | 0.77 | 0.51 |
| 31 | 0.79 | 0.46 |
| 32 | 0.78 | 0.48 |
| 33 | 0.78 | 0.57 |
| 34 | 0.76 | 0.53 |
| 35 | 0.76 | 0.43 |
| 36 | 0.76 | 0.48 |
| 37 | 0.76 | 0.44 |
| 38 | 0.76 | 0.45 |
| 39 | 0.76 | 0.5 |
| 40 | 0.77 | 0.47 |
| 41 | 0.77 | 0.46 |
| 42 | 0.77 | 0.47 |
| 43 | 0.77 | 0.5 |
| 44 | 0.79 | 0.49 |
| 45 | 0.78 | 0.48 |
| 46 | 0.78 | 0.5 |
| 47 | 0.78 | 0.52 |

## Features that differ most (Gemma Scope 2)

| comparison | layer | feature | difference | active_a | active_b | neuronpedia |
|---|---|---|---|---|---|---|
| asked vs no ask | 12 | 6260 | -2.369999885559082 | 0.01 | 0.83 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6260 |
| asked vs no ask | 12 | 2169 | -2.2300000190734863 | 0.0 | 0.73 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2169 |
| asked vs no ask | 12 | 5872 | -2.2100000381469727 | 0.04 | 0.83 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5872 |
| asked vs no ask | 12 | 5762 | -2.119999885559082 | 0.03 | 0.78 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5762 |
| asked vs no ask | 12 | 11956 | -2.069999933242798 | 0.0 | 0.67 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/11956 |
| asked vs no ask | 12 | 2765 | 1.9600000381469727 | 0.89 | 0.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765 |
| asked vs no ask | 12 | 1534 | -1.9199999570846558 | 0.99 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534 |
| asked vs no ask | 12 | 2365 | 1.8700000047683716 | 1.0 | 0.57 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2365 |
| asked vs no ask | 12 | 4382 | -1.850000023841858 | 0.39 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382 |
| asked vs no ask | 12 | 3205 | -1.850000023841858 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205 |
| asked vs no ask | 12 | 1699 | 1.7799999713897705 | 0.98 | 0.68 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1699 |
| asked vs no ask | 12 | 1632 | 1.7400000095367432 | 0.94 | 0.25 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1632 |
| asked vs no ask | 12 | 2495 | -1.7200000286102295 | 0.19 | 0.97 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2495 |
| asked vs no ask | 12 | 9301 | -1.6399999856948853 | 0.08 | 0.7 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9301 |
| asked vs no ask | 12 | 524 | -1.6100000143051147 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524 |
| asked vs no ask | 24 | 7745 | -2.2100000381469727 | 0.01 | 0.77 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7745 |
| asked vs no ask | 24 | 12847 | -2.180000066757202 | 0.0 | 0.7 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12847 |
| asked vs no ask | 24 | 907 | 1.809999942779541 | 0.95 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/907 |
| asked vs no ask | 24 | 16165 | 1.7699999809265137 | 0.89 | 0.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/16165 |
| asked vs no ask | 24 | 10568 | -1.7599999904632568 | 0.57 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10568 |
| asked vs no ask | 24 | 162 | 1.7200000286102295 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/162 |
| asked vs no ask | 24 | 13891 | 1.690000057220459 | 0.9 | 0.03 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891 |
| asked vs no ask | 24 | 524 | -1.690000057220459 | 0.13 | 0.78 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/524 |
| asked vs no ask | 24 | 22 | 1.690000057220459 | 0.91 | 0.27 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22 |
| asked vs no ask | 24 | 1826 | 1.6399999856948853 | 0.79 | 0.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1826 |
| asked vs no ask | 24 | 15592 | 1.6399999856948853 | 1.0 | 0.55 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15592 |
| asked vs no ask | 24 | 579 | 1.440000057220459 | 0.98 | 0.98 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579 |
| asked vs no ask | 24 | 5445 | 1.409999966621399 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5445 |
| asked vs no ask | 24 | 2896 | 1.3300000429153442 | 0.84 | 0.25 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2896 |
| asked vs no ask | 24 | 5671 | 1.2999999523162842 | 0.99 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5671 |
| asked vs no ask | 31 | 1708 | -2.0899999141693115 | 0.03 | 0.75 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1708 |
| asked vs no ask | 31 | 2130 | -2.069999933242798 | 0.82 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2130 |
| asked vs no ask | 31 | 951 | -2.0199999809265137 | 0.9 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/951 |
| asked vs no ask | 31 | 1571 | -1.9900000095367432 | 0.38 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1571 |
| asked vs no ask | 31 | 149 | 1.9800000190734863 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/149 |
| asked vs no ask | 31 | 1515 | -1.9700000286102295 | 0.0 | 0.6 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1515 |
| asked vs no ask | 31 | 5925 | -1.9600000381469727 | 0.14 | 0.83 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5925 |
| asked vs no ask | 31 | 5091 | -1.9500000476837158 | 0.11 | 0.88 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5091 |
| asked vs no ask | 31 | 9397 | 1.8799999952316284 | 0.96 | 0.28 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9397 |
| asked vs no ask | 31 | 1964 | -1.8600000143051147 | 0.08 | 0.78 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1964 |
| asked vs no ask | 31 | 1744 | 1.8200000524520874 | 0.99 | 0.55 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1744 |
| asked vs no ask | 31 | 899 | 1.8200000524520874 | 1.0 | 0.63 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/899 |
| asked vs no ask | 31 | 5287 | 1.7200000286102295 | 0.9 | 0.17 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5287 |
| asked vs no ask | 31 | 5652 | -1.7000000476837158 | 0.57 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652 |
| asked vs no ask | 31 | 72 | -1.659999966621399 | 0.36 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72 |
| asked vs no ask | 38 | 1774 | -2.3299999237060547 | 0.01 | 0.82 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/1774 |
| asked vs no ask | 38 | 12299 | -2.2100000381469727 | 0.01 | 0.77 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/12299 |
| asked vs no ask | 38 | 6537 | -2.200000047683716 | 0.04 | 0.83 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/6537 |
| asked vs no ask | 38 | 14071 | -2.1600000858306885 | 0.09 | 0.97 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14071 |
| asked vs no ask | 38 | 11880 | -2.1600000858306885 | 0.0 | 0.72 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/11880 |
| asked vs no ask | 38 | 10570 | -2.1500000953674316 | 0.03 | 0.8 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10570 |
| asked vs no ask | 38 | 12064 | -2.109999895095825 | 0.0 | 0.68 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/12064 |
| asked vs no ask | 38 | 9981 | -2.0999999046325684 | 0.35 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/9981 |
| asked vs no ask | 38 | 11392 | -2.0999999046325684 | 0.03 | 0.78 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/11392 |
| asked vs no ask | 38 | 15929 | -2.0899999141693115 | 0.04 | 0.77 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/15929 |
| asked vs no ask | 38 | 5475 | -2.0799999237060547 | 0.01 | 0.68 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/5475 |
| asked vs no ask | 38 | 13588 | -2.069999933242798 | 0.22 | 0.97 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/13588 |
| asked vs no ask | 38 | 5925 | -2.009999990463257 | 0.11 | 0.83 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/5925 |
| asked vs no ask | 38 | 13976 | -2.0 | 0.0 | 0.67 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/13976 |
| asked vs no ask | 38 | 6942 | -1.9500000476837158 | 0.95 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/6942 |
| loss vs gain | 12 | 2604 | 0.30000001192092896 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604 |
| loss vs gain | 12 | 9295 | -0.2800000011920929 | 0.24 | 0.38 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9295 |
| loss vs gain | 12 | 3205 | 0.25 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205 |
| loss vs gain | 12 | 16380 | -0.23999999463558197 | 0.16 | 0.25 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380 |
| loss vs gain | 12 | 3143 | -0.23000000417232513 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3143 |
| loss vs gain | 12 | 117 | -0.2199999988079071 | 0.83 | 0.89 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117 |
| loss vs gain | 12 | 2819 | -0.2199999988079071 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819 |
| loss vs gain | 12 | 2328 | 0.20000000298023224 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2328 |
| loss vs gain | 12 | 2878 | -0.20000000298023224 | 0.94 | 0.98 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2878 |
| loss vs gain | 12 | 63 | 0.1899999976158142 | 0.86 | 0.77 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/63 |
| loss vs gain | 12 | 5791 | -0.1899999976158142 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/5791 |
| loss vs gain | 12 | 3490 | 0.18000000715255737 | 0.32 | 0.23 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490 |
| loss vs gain | 12 | 1593 | -0.1599999964237213 | 0.98 | 0.98 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593 |
| loss vs gain | 12 | 111 | -0.1599999964237213 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/111 |
| loss vs gain | 12 | 4382 | -0.15000000596046448 | 0.34 | 0.44 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4382 |
| loss vs gain | 24 | 7282 | 0.3400000035762787 | 0.71 | 0.56 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7282 |
| loss vs gain | 24 | 15357 | 0.3400000035762787 | 0.94 | 0.9 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15357 |
| loss vs gain | 24 | 76 | 0.33000001311302185 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76 |
| loss vs gain | 24 | 11649 | 0.3100000023841858 | 0.9 | 0.82 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649 |
| loss vs gain | 24 | 6382 | 0.2800000011920929 | 0.95 | 0.95 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6382 |
| loss vs gain | 24 | 12646 | 0.2800000011920929 | 0.78 | 0.66 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12646 |
| loss vs gain | 24 | 13908 | 0.27000001072883606 | 0.54 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13908 |
| loss vs gain | 24 | 8326 | -0.27000001072883606 | 0.1 | 0.19 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326 |
| loss vs gain | 24 | 13332 | 0.27000001072883606 | 0.12 | 0.04 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13332 |
| loss vs gain | 24 | 1149 | -0.25999999046325684 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1149 |
| loss vs gain | 24 | 3527 | 0.23999999463558197 | 0.86 | 0.76 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3527 |
| loss vs gain | 24 | 10611 | 0.23000000417232513 | 0.73 | 0.67 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10611 |
| loss vs gain | 24 | 13865 | -0.2199999988079071 | 1.0 | 0.99 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13865 |
| loss vs gain | 24 | 5052 | 0.20000000298023224 | 0.59 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5052 |
| loss vs gain | 24 | 3166 | 0.1899999976158142 | 0.24 | 0.18 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3166 |
| loss vs gain | 31 | 6146 | 0.6399999856948853 | 0.6 | 0.26 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6146 |
| loss vs gain | 31 | 784 | -0.5299999713897705 | 0.06 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/784 |
| loss vs gain | 31 | 6152 | 0.3700000047683716 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6152 |
| loss vs gain | 31 | 2358 | -0.3700000047683716 | 0.08 | 0.18 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2358 |
| loss vs gain | 31 | 5388 | 0.36000001430511475 | 0.45 | 0.29 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5388 |
| loss vs gain | 31 | 16 | -0.3499999940395355 | 0.48 | 0.6 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/16 |
| loss vs gain | 31 | 1067 | -0.33000001311302185 | 0.18 | 0.3 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1067 |
| loss vs gain | 31 | 3367 | 0.3199999928474426 | 0.28 | 0.14 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3367 |
| loss vs gain | 31 | 11208 | -0.3199999928474426 | 0.37 | 0.52 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11208 |
| loss vs gain | 31 | 1217 | -0.3199999928474426 | 0.21 | 0.32 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1217 |
| loss vs gain | 31 | 2231 | -0.3100000023841858 | 0.15 | 0.23 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2231 |
| loss vs gain | 31 | 6617 | 0.2800000011920929 | 0.87 | 0.76 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6617 |
| loss vs gain | 31 | 2618 | -0.2800000011920929 | 0.22 | 0.33 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2618 |
| loss vs gain | 31 | 4368 | 0.2800000011920929 | 0.67 | 0.53 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4368 |
| loss vs gain | 31 | 9311 | 0.25999999046325684 | 0.42 | 0.32 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9311 |
| loss vs gain | 38 | 10784 | 0.5600000023841858 | 0.74 | 0.5 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10784 |
| loss vs gain | 38 | 9956 | -0.5400000214576721 | 0.02 | 0.17 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/9956 |
| loss vs gain | 38 | 14356 | -0.47999998927116394 | 0.01 | 0.2 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14356 |
| loss vs gain | 38 | 14060 | 0.4699999988079071 | 0.29 | 0.11 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14060 |
| loss vs gain | 38 | 7992 | 0.46000000834465027 | 0.66 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/7992 |
| loss vs gain | 38 | 8635 | -0.44999998807907104 | 0.05 | 0.19 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/8635 |
| loss vs gain | 38 | 8338 | -0.4300000071525574 | 0.22 | 0.36 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/8338 |
| loss vs gain | 38 | 11107 | -0.4099999964237213 | 0.26 | 0.57 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/11107 |
| loss vs gain | 38 | 9674 | 0.4000000059604645 | 0.54 | 0.37 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/9674 |
| loss vs gain | 38 | 8106 | 0.38999998569488525 | 0.81 | 0.67 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/8106 |
| loss vs gain | 38 | 5538 | 0.3700000047683716 | 0.26 | 0.13 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/5538 |
| loss vs gain | 38 | 5172 | 0.3700000047683716 | 0.9 | 0.87 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/5172 |
| loss vs gain | 38 | 14507 | -0.3700000047683716 | 0.11 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14507 |
| loss vs gain | 38 | 12793 | -0.36000001430511475 | 0.1 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/12793 |
| loss vs gain | 38 | 9624 | -0.3499999940395355 | 0.43 | 0.6 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/9624 |
| "you" vs no "you" (framed only) | 12 | 3205 | 0.49000000953674316 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3205 |
| "you" vs no "you" (framed only) | 12 | 9295 | -0.30000001192092896 | 0.24 | 0.38 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9295 |
| "you" vs no "you" (framed only) | 12 | 3985 | 0.30000001192092896 | 0.99 | 0.91 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985 |
| "you" vs no "you" (framed only) | 12 | 117 | -0.2800000011920929 | 0.82 | 0.9 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117 |
| "you" vs no "you" (framed only) | 12 | 16380 | -0.2800000011920929 | 0.16 | 0.25 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/16380 |
| "you" vs no "you" (framed only) | 12 | 1272 | 0.25 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1272 |
| "you" vs no "you" (framed only) | 12 | 2604 | 0.25 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604 |
| "you" vs no "you" (framed only) | 12 | 3000 | 0.23000000417232513 | 0.96 | 0.88 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000 |
| "you" vs no "you" (framed only) | 12 | 168 | -0.23000000417232513 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168 |
| "you" vs no "you" (framed only) | 12 | 438 | 0.2199999988079071 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438 |
| "you" vs no "you" (framed only) | 12 | 1699 | 0.20999999344348907 | 1.0 | 0.96 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1699 |
| "you" vs no "you" (framed only) | 12 | 9234 | 0.20999999344348907 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9234 |
| "you" vs no "you" (framed only) | 12 | 49 | 0.20000000298023224 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/49 |
| "you" vs no "you" (framed only) | 12 | 314 | 0.20000000298023224 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314 |
| "you" vs no "you" (framed only) | 12 | 2819 | -0.1899999976158142 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819 |
| "you" vs no "you" (framed only) | 24 | 222 | 0.5600000023841858 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/222 |
| "you" vs no "you" (framed only) | 24 | 15074 | 0.4399999976158142 | 0.99 | 0.9 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15074 |
| "you" vs no "you" (framed only) | 24 | 238 | 0.4399999976158142 | 0.65 | 0.5 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238 |
| "you" vs no "you" (framed only) | 24 | 406 | -0.41999998688697815 | 0.08 | 0.18 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/406 |
| "you" vs no "you" (framed only) | 24 | 579 | 0.4099999964237213 | 1.0 | 0.94 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/579 |
| "you" vs no "you" (framed only) | 24 | 11649 | 0.4000000059604645 | 0.91 | 0.82 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11649 |
| "you" vs no "you" (framed only) | 24 | 76 | 0.3799999952316284 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/76 |
| "you" vs no "you" (framed only) | 24 | 334 | 0.3700000047683716 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/334 |
| "you" vs no "you" (framed only) | 24 | 10327 | 0.3700000047683716 | 0.98 | 0.92 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10327 |
| "you" vs no "you" (framed only) | 24 | 10712 | 0.3700000047683716 | 0.99 | 0.91 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10712 |
| "you" vs no "you" (framed only) | 24 | 13891 | 0.36000001430511475 | 0.97 | 0.84 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13891 |
| "you" vs no "you" (framed only) | 24 | 12577 | -0.3499999940395355 | 0.08 | 0.18 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/12577 |
| "you" vs no "you" (framed only) | 24 | 1149 | -0.3499999940395355 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1149 |
| "you" vs no "you" (framed only) | 24 | 8311 | 0.3400000035762787 | 0.88 | 0.82 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8311 |
| "you" vs no "you" (framed only) | 24 | 14392 | 0.3400000035762787 | 0.98 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14392 |
| "you" vs no "you" (framed only) | 31 | 1880 | 0.7300000190734863 | 0.63 | 0.32 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1880 |
| "you" vs no "you" (framed only) | 31 | 11208 | 0.5400000214576721 | 0.57 | 0.31 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/11208 |
| "you" vs no "you" (framed only) | 31 | 509 | 0.46000000834465027 | 0.98 | 0.92 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/509 |
| "you" vs no "you" (framed only) | 31 | 6294 | 0.38999998569488525 | 0.63 | 0.45 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6294 |
| "you" vs no "you" (framed only) | 31 | 2079 | 0.3700000047683716 | 0.95 | 0.88 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2079 |
| "you" vs no "you" (framed only) | 31 | 7092 | 0.3700000047683716 | 0.46 | 0.28 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7092 |
| "you" vs no "you" (framed only) | 31 | 515 | -0.36000001430511475 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/515 |
| "you" vs no "you" (framed only) | 31 | 13577 | 0.36000001430511475 | 0.62 | 0.44 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13577 |
| "you" vs no "you" (framed only) | 31 | 781 | 0.3499999940395355 | 0.18 | 0.08 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/781 |
| "you" vs no "you" (framed only) | 31 | 3315 | 0.3499999940395355 | 0.51 | 0.31 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3315 |
| "you" vs no "you" (framed only) | 31 | 146 | 0.3499999940395355 | 0.99 | 0.92 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/146 |
| "you" vs no "you" (framed only) | 31 | 896 | 0.3400000035762787 | 0.82 | 0.64 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/896 |
| "you" vs no "you" (framed only) | 31 | 1128 | 0.3400000035762787 | 0.32 | 0.2 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1128 |
| "you" vs no "you" (framed only) | 31 | 5388 | 0.33000001311302185 | 0.43 | 0.31 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5388 |
| "you" vs no "you" (framed only) | 31 | 2618 | 0.33000001311302185 | 0.34 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2618 |
| "you" vs no "you" (framed only) | 38 | 9616 | 0.5 | 0.24 | 0.07 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/9616 |
| "you" vs no "you" (framed only) | 38 | 8979 | -0.47999998927116394 | 0.01 | 0.17 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/8979 |
| "you" vs no "you" (framed only) | 38 | 13933 | 0.47999998927116394 | 0.63 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/13933 |
| "you" vs no "you" (framed only) | 38 | 10784 | 0.4399999976158142 | 0.73 | 0.51 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10784 |
| "you" vs no "you" (framed only) | 38 | 10837 | -0.4399999976158142 | 0.31 | 0.54 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10837 |
| "you" vs no "you" (framed only) | 38 | 2317 | 0.41999998688697815 | 0.24 | 0.11 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/2317 |
| "you" vs no "you" (framed only) | 38 | 159 | -0.4099999964237213 | 0.21 | 0.33 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/159 |
| "you" vs no "you" (framed only) | 38 | 12607 | 0.4000000059604645 | 0.38 | 0.2 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/12607 |
| "you" vs no "you" (framed only) | 38 | 15863 | -0.4000000059604645 | 0.37 | 0.44 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/15863 |
| "you" vs no "you" (framed only) | 38 | 5237 | -0.3799999952316284 | 0.05 | 0.13 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/5237 |
| "you" vs no "you" (framed only) | 38 | 10766 | 0.3700000047683716 | 0.36 | 0.2 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10766 |
| "you" vs no "you" (framed only) | 38 | 11067 | 0.36000001430511475 | 0.58 | 0.4 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/11067 |
| "you" vs no "you" (framed only) | 38 | 15578 | -0.36000001430511475 | 0.35 | 0.52 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/15578 |
| "you" vs no "you" (framed only) | 38 | 7891 | 0.3499999940395355 | 0.69 | 0.53 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/7891 |
| "you" vs no "you" (framed only) | 38 | 5202 | 0.3499999940395355 | 0.75 | 0.57 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/5202 |
| went along vs did not (asked) | 12 | 2653 | -0.8299999833106995 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653 |
| went along vs did not (asked) | 12 | 482 | -0.7900000214576721 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/482 |
| went along vs did not (asked) | 12 | 13271 | -0.6800000071525574 | 0.24 | 0.57 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/13271 |
| went along vs did not (asked) | 12 | 220 | -0.6700000166893005 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/220 |
| went along vs did not (asked) | 12 | 2819 | 0.6499999761581421 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2819 |
| went along vs did not (asked) | 12 | 438 | -0.6499999761581421 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/438 |
| went along vs did not (asked) | 12 | 314 | -0.6200000047683716 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/314 |
| went along vs did not (asked) | 12 | 4 | -0.6000000238418579 | 0.15 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/4 |
| went along vs did not (asked) | 12 | 6423 | -0.5799999833106995 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/6423 |
| went along vs did not (asked) | 12 | 117 | 0.5699999928474426 | 0.95 | 0.82 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/117 |
| went along vs did not (asked) | 12 | 1641 | -0.550000011920929 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1641 |
| went along vs did not (asked) | 12 | 168 | 0.5400000214576721 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/168 |
| went along vs did not (asked) | 12 | 2328 | -0.4699999988079071 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2328 |
| went along vs did not (asked) | 12 | 2604 | -0.4699999988079071 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2604 |
| went along vs did not (asked) | 12 | 360 | -0.46000000834465027 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/360 |
| went along vs did not (asked) | 24 | 13908 | 0.7200000286102295 | 0.69 | 0.34 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13908 |
| went along vs did not (asked) | 24 | 2704 | 0.6000000238418579 | 0.64 | 0.34 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2704 |
| went along vs did not (asked) | 24 | 289 | -0.6000000238418579 | 0.62 | 0.8 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/289 |
| went along vs did not (asked) | 24 | 9059 | -0.5899999737739563 | 0.52 | 0.81 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9059 |
| went along vs did not (asked) | 24 | 238 | -0.5799999833106995 | 0.37 | 0.65 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/238 |
| went along vs did not (asked) | 24 | 7921 | 0.5299999713897705 | 0.45 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7921 |
| went along vs did not (asked) | 24 | 9053 | -0.5299999713897705 | 0.26 | 0.52 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9053 |
| went along vs did not (asked) | 24 | 2534 | -0.5299999713897705 | 0.37 | 0.62 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2534 |
| went along vs did not (asked) | 24 | 11105 | -0.5099999904632568 | 0.97 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/11105 |
| went along vs did not (asked) | 24 | 3166 | -0.49000000953674316 | 0.08 | 0.26 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3166 |
| went along vs did not (asked) | 24 | 3717 | 0.49000000953674316 | 0.74 | 0.52 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3717 |
| went along vs did not (asked) | 24 | 6309 | 0.49000000953674316 | 0.26 | 0.1 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6309 |
| went along vs did not (asked) | 24 | 8326 | -0.4699999988079071 | 0.05 | 0.21 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8326 |
| went along vs did not (asked) | 24 | 10327 | 0.46000000834465027 | 0.95 | 0.95 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10327 |
| went along vs did not (asked) | 24 | 2398 | 0.4399999976158142 | 0.48 | 0.26 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2398 |
| went along vs did not (asked) | 31 | 2394 | -0.7400000095367432 | 0.22 | 0.58 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2394 |
| went along vs did not (asked) | 31 | 5864 | 0.7099999785423279 | 0.26 | 0.05 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5864 |
| went along vs did not (asked) | 31 | 295 | 0.7099999785423279 | 0.69 | 0.36 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/295 |
| went along vs did not (asked) | 31 | 1316 | 0.6499999761581421 | 0.32 | 0.09 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1316 |
| went along vs did not (asked) | 31 | 9311 | 0.6299999952316284 | 0.52 | 0.25 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/9311 |
| went along vs did not (asked) | 31 | 239 | 0.5799999833106995 | 0.89 | 0.72 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/239 |
| went along vs did not (asked) | 31 | 2014 | -0.5699999928474426 | 0.27 | 0.55 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2014 |
| went along vs did not (asked) | 31 | 1775 | 0.5699999928474426 | 0.77 | 0.56 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1775 |
| went along vs did not (asked) | 31 | 429 | -0.5299999713897705 | 0.37 | 0.63 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/429 |
| went along vs did not (asked) | 31 | 528 | 0.5299999713897705 | 0.46 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/528 |
| went along vs did not (asked) | 31 | 892 | 0.5199999809265137 | 0.82 | 0.57 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/892 |
| went along vs did not (asked) | 31 | 15017 | -0.5099999904632568 | 0.28 | 0.52 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/15017 |
| went along vs did not (asked) | 31 | 3251 | -0.5099999904632568 | 0.18 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3251 |
| went along vs did not (asked) | 31 | 8224 | -0.49000000953674316 | 0.19 | 0.4 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/8224 |
| went along vs did not (asked) | 31 | 2882 | -0.4699999988079071 | 0.18 | 0.4 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2882 |
| went along vs did not (asked) | 38 | 14753 | 0.8100000023841858 | 0.41 | 0.1 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14753 |
| went along vs did not (asked) | 38 | 14928 | 0.7799999713897705 | 0.33 | 0.06 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14928 |
| went along vs did not (asked) | 38 | 10477 | 0.6899999976158142 | 0.6 | 0.3 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10477 |
| went along vs did not (asked) | 38 | 13556 | 0.6700000166893005 | 0.38 | 0.09 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/13556 |
| went along vs did not (asked) | 38 | 11380 | -0.6499999761581421 | 0.47 | 0.78 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/11380 |
| went along vs did not (asked) | 38 | 13851 | 0.6499999761581421 | 0.31 | 0.09 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/13851 |
| went along vs did not (asked) | 38 | 14537 | 0.6100000143051147 | 0.42 | 0.13 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14537 |
| went along vs did not (asked) | 38 | 6590 | -0.6100000143051147 | 0.6 | 0.87 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/6590 |
| went along vs did not (asked) | 38 | 12956 | 0.5899999737739563 | 0.96 | 0.9 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/12956 |
| went along vs did not (asked) | 38 | 2635 | -0.5899999737739563 | 0.31 | 0.57 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/2635 |
| went along vs did not (asked) | 38 | 10621 | 0.5799999833106995 | 0.66 | 0.39 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10621 |
| went along vs did not (asked) | 38 | 10608 | 0.5799999833106995 | 0.69 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10608 |
| went along vs did not (asked) | 38 | 3212 | 0.5699999928474426 | 1.0 | 0.99 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/3212 |
| went along vs did not (asked) | 38 | 10801 | 0.5699999928474426 | 0.31 | 0.08 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10801 |
| went along vs did not (asked) | 38 | 13612 | 0.5699999928474426 | 0.89 | 0.69 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/13612 |
| full takeover vs one line (asked) | 12 | 15474 | -0.28999999165534973 | 0.95 | 0.99 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/15474 |
| full takeover vs one line (asked) | 12 | 2765 | -0.2800000011920929 | 0.81 | 0.96 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2765 |
| full takeover vs one line (asked) | 12 | 9301 | -0.25999999046325684 | 0.03 | 0.13 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9301 |
| full takeover vs one line (asked) | 12 | 9773 | -0.23999999463558197 | 0.23 | 0.34 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9773 |
| full takeover vs one line (asked) | 12 | 3490 | -0.23000000417232513 | 0.19 | 0.29 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3490 |
| full takeover vs one line (asked) | 12 | 63 | -0.18000000715255737 | 0.8 | 0.82 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/63 |
| full takeover vs one line (asked) | 12 | 3000 | 0.18000000715255737 | 0.89 | 0.86 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3000 |
| full takeover vs one line (asked) | 12 | 1534 | 0.1599999964237213 | 1.0 | 0.99 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1534 |
| full takeover vs one line (asked) | 12 | 524 | 0.14000000059604645 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/524 |
| full takeover vs one line (asked) | 12 | 978 | 0.14000000059604645 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/978 |
| full takeover vs one line (asked) | 12 | 3985 | 0.12999999523162842 | 0.95 | 0.96 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/3985 |
| full takeover vs one line (asked) | 12 | 2328 | -0.12999999523162842 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2328 |
| full takeover vs one line (asked) | 12 | 1593 | -0.12999999523162842 | 0.99 | 0.99 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/1593 |
| full takeover vs one line (asked) | 12 | 2653 | 0.11999999731779099 | 1.0 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/2653 |
| full takeover vs one line (asked) | 12 | 9295 | -0.11999999731779099 | 0.31 | 0.38 | https://www.neuronpedia.org/gemma-3-12b-it/12-gemmascope-2-res-16k/9295 |
| full takeover vs one line (asked) | 24 | 3051 | -0.4300000071525574 | 0.11 | 0.27 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/3051 |
| full takeover vs one line (asked) | 24 | 1826 | -0.41999998688697815 | 0.71 | 0.87 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/1826 |
| full takeover vs one line (asked) | 24 | 2398 | 0.38999998569488525 | 0.43 | 0.24 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/2398 |
| full takeover vs one line (asked) | 24 | 5965 | -0.3499999940395355 | 0.17 | 0.29 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/5965 |
| full takeover vs one line (asked) | 24 | 9712 | 0.3400000035762787 | 0.93 | 0.93 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9712 |
| full takeover vs one line (asked) | 24 | 13799 | 0.3199999928474426 | 0.71 | 0.54 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/13799 |
| full takeover vs one line (asked) | 24 | 22 | 0.3199999928474426 | 0.95 | 0.88 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/22 |
| full takeover vs one line (asked) | 24 | 14235 | -0.3199999928474426 | 0.55 | 0.73 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/14235 |
| full takeover vs one line (asked) | 24 | 10611 | -0.3100000023841858 | 0.63 | 0.72 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/10611 |
| full takeover vs one line (asked) | 24 | 6572 | 0.30000001192092896 | 0.38 | 0.23 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/6572 |
| full takeover vs one line (asked) | 24 | 9368 | 0.30000001192092896 | 0.94 | 1.0 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/9368 |
| full takeover vs one line (asked) | 24 | 15357 | 0.2800000011920929 | 0.92 | 0.93 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/15357 |
| full takeover vs one line (asked) | 24 | 8967 | 0.25999999046325684 | 0.09 | 0.03 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/8967 |
| full takeover vs one line (asked) | 24 | 4440 | 0.25999999046325684 | 0.23 | 0.14 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/4440 |
| full takeover vs one line (asked) | 24 | 7818 | -0.25 | 0.19 | 0.29 | https://www.neuronpedia.org/gemma-3-12b-it/24-gemmascope-2-res-16k/7818 |
| full takeover vs one line (asked) | 31 | 13577 | -0.550000011920929 | 0.38 | 0.65 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/13577 |
| full takeover vs one line (asked) | 31 | 781 | -0.4300000071525574 | 0.05 | 0.19 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/781 |
| full takeover vs one line (asked) | 31 | 7092 | -0.4000000059604645 | 0.25 | 0.45 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/7092 |
| full takeover vs one line (asked) | 31 | 972 | 0.38999998569488525 | 0.86 | 0.73 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/972 |
| full takeover vs one line (asked) | 31 | 4805 | -0.38999998569488525 | 0.25 | 0.45 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4805 |
| full takeover vs one line (asked) | 31 | 3315 | -0.3799999952316284 | 0.33 | 0.47 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3315 |
| full takeover vs one line (asked) | 31 | 2014 | -0.3799999952316284 | 0.37 | 0.54 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2014 |
| full takeover vs one line (asked) | 31 | 72 | 0.3799999952316284 | 0.48 | 0.25 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/72 |
| full takeover vs one line (asked) | 31 | 6048 | -0.3799999952316284 | 0.21 | 0.37 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/6048 |
| full takeover vs one line (asked) | 31 | 2608 | -0.3799999952316284 | 0.22 | 0.39 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/2608 |
| full takeover vs one line (asked) | 31 | 5652 | 0.3700000047683716 | 0.71 | 0.43 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/5652 |
| full takeover vs one line (asked) | 31 | 3094 | -0.36000001430511475 | 0.17 | 0.3 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3094 |
| full takeover vs one line (asked) | 31 | 1248 | 0.3499999940395355 | 0.35 | 0.2 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/1248 |
| full takeover vs one line (asked) | 31 | 4709 | -0.3499999940395355 | 0.04 | 0.15 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/4709 |
| full takeover vs one line (asked) | 31 | 3251 | -0.3400000035762787 | 0.26 | 0.42 | https://www.neuronpedia.org/gemma-3-12b-it/31-gemmascope-2-res-16k/3251 |
| full takeover vs one line (asked) | 38 | 9503 | 0.5400000214576721 | 0.3 | 0.11 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/9503 |
| full takeover vs one line (asked) | 38 | 15952 | -0.5299999713897705 | 0.05 | 0.22 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/15952 |
| full takeover vs one line (asked) | 38 | 8843 | 0.5099999904632568 | 0.21 | 0.05 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/8843 |
| full takeover vs one line (asked) | 38 | 10847 | -0.49000000953674316 | 0.6 | 0.77 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10847 |
| full takeover vs one line (asked) | 38 | 15119 | -0.49000000953674316 | 0.84 | 0.97 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/15119 |
| full takeover vs one line (asked) | 38 | 26 | 0.47999998927116394 | 0.55 | 0.31 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/26 |
| full takeover vs one line (asked) | 38 | 10260 | -0.47999998927116394 | 0.5 | 0.73 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10260 |
| full takeover vs one line (asked) | 38 | 7289 | -0.47999998927116394 | 0.49 | 0.73 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/7289 |
| full takeover vs one line (asked) | 38 | 12347 | -0.4699999988079071 | 0.54 | 0.73 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/12347 |
| full takeover vs one line (asked) | 38 | 10837 | 0.4699999988079071 | 0.58 | 0.33 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/10837 |
| full takeover vs one line (asked) | 38 | 16290 | 0.46000000834465027 | 0.93 | 0.9 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/16290 |
| full takeover vs one line (asked) | 38 | 16131 | -0.46000000834465027 | 0.09 | 0.28 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/16131 |
| full takeover vs one line (asked) | 38 | 15712 | 0.46000000834465027 | 0.19 | 0.05 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/15712 |
| full takeover vs one line (asked) | 38 | 14984 | 0.46000000834465027 | 0.99 | 0.97 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/14984 |
| full takeover vs one line (asked) | 38 | 16044 | 0.46000000834465027 | 0.32 | 0.1 | https://www.neuronpedia.org/gemma-3-12b-it/38-gemmascope-2-res-16k/16044 |