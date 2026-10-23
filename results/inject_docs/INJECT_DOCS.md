# The state after reading a document, injected without the document (exploratory)

36 moments (B's neutral careers at their requests; 24 more left out because the scored orders cover less than half of the model's probability with no document). The agent reads the document just before UBS's (neutral) request; the change that reading makes to each layer's state over the request's update is then put back by hand with the document left out: **mean** (the average change, added to every token) or **aligned** (the change at each token of the update, restored token by token). P(the order goes along) after the fixed neutral reasoning line, each condition minus no document at the same moment, in points. Produced by `designs/rd2/analysis/inject_docs.py`.


## Neutral document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +9.4 | +2.3 to +16.6 | 0.0526 | 100% |
| injected, mean, layer 12 | -2.0 | -5.4 to +0.7 | 0.2952 | -21% |
| injected, mean, layer 18 | +6.4 | +2.5 to +11.2 | 0.0046 | 67% |
| injected, mean, layer 24 | -7.1 | -12.6 to -2.3 | 0.0169 | -75% |
| random, mean, layer 18 | -8.7 | -16.5 to -2.2 | 0.0415 | – |
| injected, aligned, layer 12 | -0.9 | -5.9 to +3.2 | 0.8162 | -9% |
| injected, aligned, layer 18 | +1.0 | -7.0 to +10.5 | 0.7735 | 11% |
| injected, aligned, layer 24 | -6.0 | -11.9 to -1.4 | 0.0212 | -63% |
| random, aligned, layer 18 | +2.1 | -4.9 to +9.5 | 0.6192 | – |

Injected against random at layer 18: mean +15.0 | +8.3 to +22.3 | 0.0048; aligned -1.1 | -14.8 to +13.1 | 0.8900 (change | interval | p).

## Loss document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +20.3 | +9.1 to +32.2 | 0.0051 | 100% |
| injected, mean, layer 12 | -2.0 | -4.9 to -0.0 | 0.1890 | -10% |
| injected, mean, layer 18 | +7.1 | +2.4 to +13.0 | 0.0041 | 35% |
| injected, mean, layer 24 | -2.4 | -7.1 to +1.2 | 0.3937 | -12% |
| random, mean, layer 18 | -1.7 | -9.8 to +5.6 | 0.7044 | – |
| injected, aligned, layer 12 | +0.5 | -0.9 to +2.0 | 0.5362 | 3% |
| injected, aligned, layer 18 | +9.6 | +1.7 to +18.0 | 0.0478 | 47% |
| injected, aligned, layer 24 | +1.0 | -6.8 to +8.4 | 0.8146 | 5% |
| random, aligned, layer 18 | -7.9 | -15.5 to -1.1 | 0.0709 | – |

Injected against random at layer 18: mean +8.8 | +3.0 to +15.7 | 0.0078; aligned +17.5 | +9.6 to +25.7 | 0.0037 (change | interval | p).
Beyond the neutral document: as read +10.9 | +0.9 to +21.2 | 0.0926; aligned at layer 18 +8.6 | +1.1 to +15.6 | 0.0471.

## Blame document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +13.5 | +3.2 to +23.6 | 0.0385 | 100% |
| injected, mean, layer 12 | -1.9 | -4.4 to -0.1 | 0.0999 | -14% |
| injected, mean, layer 18 | +7.3 | +2.5 to +12.8 | 0.0186 | 54% |
| injected, mean, layer 24 | -0.7 | -2.7 to +1.5 | 0.6127 | -5% |
| random, mean, layer 18 | +5.0 | -8.6 to +22.4 | 0.6294 | – |
| injected, aligned, layer 12 | +1.7 | +0.4 to +3.3 | 0.0159 | 13% |
| injected, aligned, layer 18 | +13.5 | +5.7 to +21.8 | 0.0016 | 100% |
| injected, aligned, layer 24 | +6.9 | -0.5 to +14.1 | 0.1219 | 51% |
| random, aligned, layer 18 | +1.7 | -9.5 to +15.1 | 0.8475 | – |

Injected against random at layer 18: mean +2.3 | -11.1 to +14.5 | 0.7347; aligned +11.8 | +1.6 to +23.7 | 0.0673 (change | interval | p).
Beyond the neutral document: as read +4.0 | -5.9 to +12.6 | 0.4296; aligned at layer 18 +12.5 | -0.2 to +24.1 | 0.1033.

## Gain document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +20.5 | +11.4 to +30.0 | 0.0070 | 100% |
| injected, mean, layer 12 | -2.5 | -5.3 to -0.2 | 0.1068 | -12% |
| injected, mean, layer 18 | +6.2 | +2.7 to +9.9 | 0.0114 | 30% |
| injected, mean, layer 24 | -2.9 | -7.0 to +0.2 | 0.2296 | -14% |
| random, mean, layer 18 | -4.8 | -14.3 to +4.6 | 0.2992 | – |
| injected, aligned, layer 12 | -1.6 | -4.6 to +0.4 | 0.3541 | -8% |
| injected, aligned, layer 18 | +6.3 | -1.1 to +13.2 | 0.1533 | 31% |
| injected, aligned, layer 24 | +7.2 | -1.2 to +16.0 | 0.1928 | 35% |
| random, aligned, layer 18 | -0.3 | -8.4 to +8.0 | 0.9542 | – |

Injected against random at layer 18: mean +11.0 | +2.1 to +20.4 | 0.0483; aligned +6.6 | -5.7 to +18.2 | 0.3192 (change | interval | p).
Beyond the neutral document: as read +11.1 | +2.5 to +20.4 | 0.0362; aligned at layer 18 +5.3 | -1.1 to +11.9 | 0.1592.

## Credit document

| Condition | Change from no document | 95% interval | p | Share of the document's own effect |
|---|---|---|---|---|
| the document, as read | +11.7 | +3.7 to +19.4 | 0.0239 | 100% |
| injected, mean, layer 12 | -1.6 | -3.9 to +0.1 | 0.0840 | -14% |
| injected, mean, layer 18 | +6.1 | +2.6 to +10.6 | 0.0040 | 52% |
| injected, mean, layer 24 | -3.6 | -7.9 to +0.2 | 0.1898 | -30% |
| random, mean, layer 18 | -0.9 | -13.2 to +11.6 | 0.8680 | – |
| injected, aligned, layer 12 | +2.0 | +0.1 to +4.8 | 0.0994 | 17% |
| injected, aligned, layer 18 | +5.8 | -0.5 to +14.1 | 0.1913 | 50% |
| injected, aligned, layer 24 | +3.6 | -1.1 to +9.0 | 0.2238 | 31% |
| random, aligned, layer 18 | +7.2 | -1.8 to +19.0 | 0.3182 | – |

Injected against random at layer 18: mean +7.0 | -5.7 to +18.9 | 0.3170; aligned -1.4 | -10.3 to +6.8 | 0.7817 (change | interval | p).
Beyond the neutral document: as read +2.3 | -8.5 to +12.3 | 0.6894; aligned at layer 18 +4.8 | -5.4 to +16.7 | 0.4746.

Coverage: median 0.81, lowest 0.00.
