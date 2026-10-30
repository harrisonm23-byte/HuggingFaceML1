# Attention onto "you", the chat-only days (exploratory)

B's 850 chat-only-day updates with a UBS line (50 careers), each read with UBS's lines in the five framings and the history held fixed. 48 layers (8 global, 40 local with a sliding window), 16 heads. A cell is the share of a head's attention on that group of tokens, averaged over heads, layers and moments. Levels, neutral first; comparisons between framings are paired within the moment.

## The framed sentence: negative or positive, "you" or not (all layers)

Each framing adds a sentence to UBS's line (or rewrites part of it). Attention on the whole sentence, and per token (the sentences differ in length). p: per-token difference, sign flips by career.

| Framed sentence | Tokens | Attention on the sentence | Per token |
|---|---|---|---|
| Loss | 27.0 | 1.1% | 0.041% |
| Gain | 23.8 | 1.0% | 0.042% |
| Blame | 34.6 | 1.3% | 0.038% |
| Credit | 32.1 | 1.3% | 0.039% |
| (UBS's neutral line, for scale) | 24.8 | 2.1% | 0.085% |

| Comparison, per token | Difference | p |
|---|---|---|
| Loss minus Gain (negative vs positive, no "you") | +0.002 points per token | 0.000 |
| Blame minus Credit (negative vs positive, with "you") | +0.001 points per token | 0.006 |
| Blame minus Loss ("you" vs not, negative) | -0.004 points per token | 0.000 |
| Credit minus Gain ("you" vs not, positive) | -0.003 points per token | 0.001 |

## Where the decision token looks, all layers

| Framing | History before the update | Rest of the update | UBS's neutral core | "you" in the core | The framed extra | "you" in the extra | Template tail |
|---|---|---|---|---|---|---|---|
| Neutral | 63.4% | 19.2% | 2.1% | 0.1% | 0.0% | 0.0% | 15.2% |
| Loss | 62.8% | 19.2% | 1.7% | 0.0% | 1.1% | 0.0% | 15.2% |
| Gain | 62.9% | 19.2% | 1.6% | 0.0% | 1.0% | 0.0% | 15.2% |
| Blame | 62.6% | 19.2% | 1.7% | 0.0% | 1.2% | 0.1% | 15.2% |
| Credit | 62.6% | 19.2% | 1.6% | 0.0% | 1.1% | 0.1% | 15.2% |

## Where the decision token looks, global layers only (the ones that can see the whole history)

| Framing | History before the update | Rest of the update | UBS's neutral core | "you" in the core | The framed extra | "you" in the extra | Template tail |
|---|---|---|---|---|---|---|---|
| Neutral | 92.5% | 4.4% | 0.4% | 0.0% | 0.0% | 0.0% | 2.7% |
| Loss | 92.4% | 4.2% | 0.4% | 0.0% | 0.3% | 0.0% | 2.6% |
| Gain | 92.4% | 4.2% | 0.4% | 0.0% | 0.3% | 0.0% | 2.7% |
| Blame | 92.3% | 4.2% | 0.3% | 0.0% | 0.4% | 0.0% | 2.7% |
| Credit | 92.4% | 4.2% | 0.4% | 0.0% | 0.4% | 0.0% | 2.6% |

## Attention per token: one "you" against one other token of the extra (all layers)

| Framing | Per "you" token | Per other token of the extra | Ratio |
|---|---|---|---|
| Blame | 0.04% | 0.05% | 0.87 |
| Credit | 0.05% | 0.05% | 0.91 |

## Does the "you" clause draw more attention than the loss or gain clause? (mass on the whole framed extra)

| Pair | Extra, first | Extra, second | Difference | p |
|---|---|---|---|---|
| Blame vs Loss | 1.3% | 1.1% | +0.19 points | 0.000 |
| Credit vs Gain | 1.3% | 1.0% | +0.26 points | 0.000 |
| Loss vs Gain | 1.1% | 1.0% | +0.10 points | 0.000 |
| Blame vs Credit | 1.3% | 1.3% | +0.04 points | 0.056 |

## By layer: share of a head's attention on "you" in the extra, and on the whole extra

| Layer | Type | Blame: "you" | Credit: "you" | Blame: extra | Loss: extra | Credit: extra | Gain: extra |
|---|---|---|---|---|---|---|---|
| 0 | local | 0.3% | 0.4% | 4.3% | 3.2% | 3.9% | 2.9% |
| 1 | local | 0.4% | 0.5% | 3.7% | 3.0% | 3.6% | 2.6% |
| 2 | local | 0.0% | 0.0% | 0.7% | 0.6% | 0.6% | 0.9% |
| 3 | local | 0.0% | 0.0% | 0.8% | 0.7% | 0.8% | 0.7% |
| 4 | local | 0.1% | 0.1% | 1.1% | 1.0% | 1.0% | 1.0% |
| 5 | global | 0.0% | 0.0% | 0.4% | 0.3% | 0.5% | 0.3% |
| 6 | local | 0.3% | 0.4% | 4.7% | 4.2% | 4.5% | 4.0% |
| 7 | local | 0.3% | 0.4% | 1.6% | 1.2% | 1.7% | 1.3% |
| 8 | local | 0.1% | 0.1% | 1.9% | 1.8% | 2.1% | 2.0% |
| 9 | local | 0.1% | 0.2% | 1.6% | 1.5% | 1.7% | 1.5% |
| 10 | local | 0.1% | 0.2% | 2.1% | 1.8% | 2.1% | 1.7% |
| 11 | global | 0.0% | 0.0% | 0.1% | 0.1% | 0.1% | 0.1% |
| 12 | local | 0.2% | 0.2% | 2.2% | 1.7% | 2.3% | 1.5% |
| 13 | local | 0.1% | 0.1% | 1.9% | 1.7% | 1.9% | 1.4% |
| 14 | local | 0.4% | 0.3% | 2.3% | 1.6% | 2.1% | 1.2% |
| 15 | local | 0.2% | 0.2% | 2.8% | 2.5% | 2.5% | 2.0% |
| 16 | local | 0.3% | 0.3% | 2.5% | 2.0% | 2.5% | 1.8% |
| 17 | global | 0.1% | 0.1% | 0.6% | 0.4% | 0.5% | 0.3% |
| 18 | local | 0.2% | 0.2% | 1.9% | 1.6% | 1.9% | 1.4% |
| 19 | local | 0.2% | 0.2% | 1.5% | 1.0% | 1.3% | 0.7% |
| 20 | local | 0.1% | 0.1% | 1.7% | 1.5% | 1.5% | 1.1% |
| 21 | local | 0.1% | 0.1% | 1.4% | 1.1% | 1.3% | 0.9% |
| 22 | local | 0.1% | 0.1% | 2.0% | 1.7% | 1.8% | 1.4% |
| 23 | global | 0.1% | 0.0% | 0.6% | 0.5% | 0.4% | 0.3% |
| 24 | local | 0.2% | 0.2% | 2.2% | 1.8% | 1.9% | 1.5% |
| 25 | local | 0.1% | 0.1% | 1.9% | 1.7% | 1.6% | 1.3% |
| 26 | local | 0.2% | 0.2% | 2.2% | 1.7% | 1.8% | 1.3% |
| 27 | local | 0.1% | 0.1% | 1.4% | 1.2% | 1.2% | 0.9% |
| 28 | local | 0.1% | 0.1% | 0.9% | 0.7% | 0.8% | 0.6% |
| 29 | global | 0.0% | 0.0% | 0.3% | 0.2% | 0.2% | 0.2% |
| 30 | local | 0.1% | 0.1% | 0.8% | 0.7% | 0.9% | 0.7% |
| 31 | local | 0.1% | 0.1% | 0.8% | 0.7% | 0.8% | 0.7% |
| 32 | local | 0.0% | 0.1% | 0.6% | 0.6% | 0.7% | 0.6% |
| 33 | local | 0.1% | 0.1% | 0.8% | 0.7% | 0.8% | 0.7% |
| 34 | local | 0.0% | 0.0% | 0.2% | 0.3% | 0.4% | 0.4% |
| 35 | global | 0.0% | 0.0% | 0.7% | 0.6% | 0.6% | 0.7% |
| 36 | local | 0.0% | 0.0% | 0.6% | 0.6% | 0.7% | 0.6% |
| 37 | local | 0.0% | 0.0% | 0.1% | 0.2% | 0.3% | 0.3% |
| 38 | local | 0.1% | 0.1% | 1.1% | 1.0% | 1.2% | 1.0% |
| 39 | local | 0.0% | 0.0% | 0.3% | 0.3% | 0.5% | 0.4% |
| 40 | local | 0.0% | 0.0% | 0.2% | 0.3% | 0.4% | 0.4% |
| 41 | global | 0.0% | 0.0% | 0.5% | 0.4% | 0.5% | 0.5% |
| 42 | local | 0.0% | 0.0% | 0.4% | 0.4% | 0.5% | 0.4% |
| 43 | local | 0.0% | 0.0% | 0.4% | 0.5% | 0.6% | 0.6% |
| 44 | local | 0.0% | 0.0% | 0.5% | 0.5% | 0.6% | 0.5% |
| 45 | local | 0.0% | 0.0% | 0.4% | 0.4% | 0.5% | 0.4% |
| 46 | local | 0.0% | 0.1% | 0.5% | 0.4% | 0.5% | 0.4% |
| 47 | global | 0.0% | 0.0% | 0.3% | 0.3% | 0.2% | 0.2% |

## The heads that look at "you" most (blame; mean share of the head's attention)

| Layer | Head | Blame: "you" in the extra | Credit: "you" in the extra | Neutral: "you" in the core |
|---|---|---|---|---|
| 14 | 1 | 3.3% | 1.8% | 0.8% |
| 1 | 9 | 2.4% | 3.0% | 0.8% |
| 1 | 7 | 2.1% | 2.7% | 0.7% |
| 7 | 5 | 1.5% | 1.9% | 0.6% |
| 0 | 1 | 1.5% | 1.7% | 0.5% |
| 7 | 14 | 1.3% | 1.2% | 0.7% |
| 12 | 12 | 1.2% | 1.5% | 0.8% |
| 7 | 15 | 1.1% | 1.7% | 0.4% |
| 19 | 9 | 1.0% | 1.1% | 0.6% |
| 6 | 2 | 1.0% | 1.5% | 0.3% |

## Into "you": where the "you" token itself looks (blame and credit; all layers, then global layers)

| Framing | Layers | History before the update | Rest of the update | UBS's core | The extra before "you" | Itself |
|---|---|---|---|---|---|---|
| Blame | all | 61.5% | 10.6% | 11.3% | 11.6% | 5.0% |
| Blame | global | 86.1% | 2.0% | 4.2% | 4.8% | 2.8% |
| Credit | all | 61.7% | 10.8% | 12.6% | 9.7% | 5.1% |
| Credit | global | 86.1% | 2.2% | 4.5% | 4.6% | 2.7% |

## Does attention on "you" go with the decision?

The reply each career actually wrote (its own framing), labelled blind from its chat message: does the attention on the framed sentence, per token, differ where it agreed in words? p: labels reshuffled across moments within the framing (20,000 times). The history's length is reported, since a longer history takes attention from everything in the update.

| Career's framing | Replies with UBS asking | Agreed | Per token, agreed | Per token, did not | p | History tokens, agreed | did not |
|---|---|---|---|---|---|---|---|
| Loss | 164 | 131 | 0.057% | 0.063% | 0.461 | 30,084 | 29,625 |
| Gain | 167 | 22 | 0.057% | 0.052% | 0.524 | 16,554 | 31,643 |
| Blame | 167 | 115 | 0.044% | 0.048% | 0.253 | 31,589 | 25,680 |
| Credit | 167 | 47 | 0.051% | 0.049% | 0.583 | 27,369 | 31,321 |
