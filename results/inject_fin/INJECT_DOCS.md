# The state after reading a document, injected without the document (exploratory)

36 moments (B's neutral careers at their requests; 24 more left out because the scored orders cover less than half of the model's probability with no document). The agent reads the document just before UBS's (neutral) request; the change that reading makes to each layer's state over the request's update is then put back by hand with the document left out: **mean** (the average change, added to every token) or **aligned** (the change at each token of the update, restored token by token). P(the order goes along) after the fixed neutral reasoning line, each condition minus no document at the same moment, in points. Produced by `designs/rd2/analysis/inject_docs.py`.


## Neutral document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +5.7 | -0.0 to +11.3 | 0.0887 | 100% |
| injected, mean, layer 12 | -1.3 | -3.9 to +0.4 | 0.3643 | -23% |
| injected, mean, layer 18 | +6.0 | +0.9 to +12.7 | 0.0364 | 105% |
| injected, mean, layer 24 | -4.5 | -9.9 to -0.4 | 0.0601 | -78% |
| random, mean, layer 18 | -12.5 | -19.7 to -5.9 | 0.0098 | – |
| injected, aligned, layer 12 | +1.6 | -2.5 to +6.1 | 0.5113 | 28% |
| injected, aligned, layer 18 | +1.3 | -4.4 to +6.1 | 0.6418 | 23% |
| injected, aligned, layer 24 | -3.1 | -7.6 to +0.2 | 0.2077 | -54% |
| random, aligned, layer 18 | +0.5 | -6.0 to +6.8 | 0.8650 | – |

Injected against random at layer 18: mean +18.5 | +9.7 to +27.4 | 0.0126; aligned +0.8 | -8.5 to +10.0 | 0.8360 (change | interval | p).

## Loss document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +16.9 | +7.5 to +26.3 | 0.0058 | 100% |
| injected, mean, layer 12 | -1.3 | -3.9 to +0.4 | 0.3790 | -8% |
| injected, mean, layer 18 | +4.8 | +0.8 to +9.5 | 0.0041 | 29% |
| injected, mean, layer 24 | -2.7 | -7.7 to +1.1 | 0.3187 | -16% |
| random, mean, layer 18 | +3.3 | -10.2 to +17.7 | 0.6678 | – |
| injected, aligned, layer 12 | +1.7 | +0.5 to +3.3 | 0.0052 | 10% |
| injected, aligned, layer 18 | +10.1 | +2.1 to +20.0 | 0.0507 | 60% |
| injected, aligned, layer 24 | -2.6 | -10.3 to +5.2 | 0.5481 | -15% |
| random, aligned, layer 18 | -10.0 | -17.6 to -3.3 | 0.0282 | – |

Injected against random at layer 18: mean +1.5 | -11.9 to +14.5 | 0.8383; aligned +20.0 | +11.1 to +30.0 | 0.0037 (change | interval | p).
Beyond the neutral document: as read +11.1 | +1.9 to +19.7 | 0.0602; aligned at layer 18 +8.8 | +1.8 to +17.2 | 0.0481.

## Gain document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +26.4 | +12.5 to +42.1 | 0.0055 | 100% |
| injected, mean, layer 12 | -1.5 | -3.4 to -0.1 | 0.0829 | -6% |
| injected, mean, layer 18 | +4.7 | +0.5 to +9.6 | 0.0188 | 18% |
| injected, mean, layer 24 | -7.5 | -16.1 to -1.1 | 0.1281 | -29% |
| random, mean, layer 18 | +7.5 | -4.4 to +21.8 | 0.3445 | – |
| injected, aligned, layer 12 | +2.8 | -0.4 to +8.4 | 0.4488 | 11% |
| injected, aligned, layer 18 | +6.4 | -0.9 to +13.5 | 0.1237 | 24% |
| injected, aligned, layer 24 | +0.6 | -6.1 to +6.2 | 0.8551 | 2% |
| random, aligned, layer 18 | -0.2 | -13.1 to +14.0 | 0.9735 | – |

Injected against random at layer 18: mean -2.9 | -14.8 to +9.0 | 0.6383; aligned +6.5 | -6.4 to +19.0 | 0.3723 (change | interval | p).
Beyond the neutral document: as read +20.6 | +6.0 to +38.1 | 0.0205; aligned at layer 18 +5.0 | +0.7 to +10.8 | 0.0469.

Coverage: median 0.51, lowest 0.00.
