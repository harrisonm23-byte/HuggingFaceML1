# Experiment B in other models (exploratory)

The same careers, framed lines, memo and settings as Gemma's Experiment B (4-bit, temperature 0.7); each model's chat template laid out as Gemma's (sim/other_models.py). Went along at UBS's six push requests; each model's own neutral careers are its base. "No valid order": requests where no reply in the join window gave a readable order (counted as not going along, shown apart). Levels, the base first.

## Gemma 3 12B

| Framing | Careers | 7 Jan | 12 Jan | 1 Apr | 8 Jun (third bank) | 8 Jun (stops) | 5 Aug | Share of six | p vs its neutral | No valid order | Orders per career | Replies sent back per career |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Neutral (base) | 10 | 3/10 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 | 5% |  | 4 of 60 | 33 | 11 |
| Loss | 10 | 7/10 | 7/10 | 0/10 | 0/10 | 0/10 | 1/10 | 25% | 0.008 | 1 of 60 | 58 | 1 |
| Gain | 10 | 4/10 | 2/10 | 0/10 | 0/10 | 0/10 | 0/10 | 10% | 0.521 | 2 of 60 | 68 | 0 |
| Blame | 10 | 8/10 | 9/10 | 1/10 | 0/10 | 2/10 | 0/10 | 33% | 0.000 | 0 of 60 | 72 | 3 |
| Credit | 10 | 5/10 | 6/10 | 0/10 | 0/10 | 0/10 | 0/10 | 18% | 0.044 | 0 of 60 | 76 | 1 |

## Qwen3.5 9B

| Framing | Careers | 7 Jan | 12 Jan | 1 Apr | 8 Jun (third bank) | 8 Jun (stops) | 5 Aug | Share of six | p vs its neutral | No valid order | Orders per career | Replies sent back per career |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Neutral (base) | 2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0% |  | 0 of 12 | 3 | 0 |
| Blame | 1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0% | 1.000 | 0 of 6 | 0 | 0 |
| Credit | 1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0% | 1.000 | 0 of 6 | 3 | 1 |

## Mistral Nemo 12B

| Framing | Careers | 7 Jan | 12 Jan | 1 Apr | 8 Jun (third bank) | 8 Jun (stops) | 5 Aug | Share of six | p vs its neutral | No valid order | Orders per career | Replies sent back per career |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Neutral (base) | 1 | 0/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 17% |  | 0 of 6 | 43 | 74 |
| Loss | 1 | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 33% | 1.000 | 0 of 6 | 73 | 5 |
| Gain | 1 | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 1/1 | 50% | 1.000 | 0 of 6 | 80 | 4 |
| Blame | 1 | 0/1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 17% | 1.000 | 1 of 6 | 106 | 137 |
| Credit | 1 | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 | 50% | 1.000 | 1 of 6 | 60 | 17 |
