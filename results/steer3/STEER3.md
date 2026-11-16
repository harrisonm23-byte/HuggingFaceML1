# Steering, third run (exploratory)

60 moments (B's neutral careers at their requests). P(the order goes along) after the fixed neutral reasoning line, each condition minus none at the same moment, in points. Produced by `designs/rd2/analysis/steer3.py`.

## The yardstick: the framed words themselves

| Condition | Change | 95% interval | p |
|---|---|---|---|
| framed (loss + you), as read | +6.1 | +1.3 to +11.2 | 0.0179 |

## The whole-message transplant (the framed update's average state added to every token of the neutral update)

| Layer | Transplant | 95% interval | p | Share of the framed words' effect | Random vector, same size |
|---|---|---|---|---|---|
| 6 | +0.3 | -0.2 to +1.0 | 0.5668 | 5% | – |
| 12 | +0.5 | -0.0 to +0.9 | 0.1172 | 8% | +4.2 (p 0.045) |
| 18 | +2.2 | +0.8 to +4.0 | 0.0021 | 36% | +1.8 (p 0.354) |
| 24 | +2.2 | +0.6 to +4.1 | 0.0019 | 36% | – |

## The layer-18 loss direction, pushed harder

| Condition | Change | 95% interval | p | Random directions, same size (mean) |
|---|---|---|---|---|
| +loss x8 at layer 18 | +7.3 | +2.7 to +12.9 | 0.0048 | -12.6 |
| +loss x16 at layer 18 | -4.7 | -13.0 to +4.0 | 0.2891 | -14.3 |

## Sampled replies (two per moment)

| Condition | Replies | Went along | Unreadable |
|---|---|---|---|
| none | 120 | 9% | 18% |
| +loss x16 at layer 18 | 120 | 0% | 22% |
| +loss x8 at layer 18 | 120 | 2% | 22% |
| framed (loss + you), as read | 120 | 11% | 19% |
| message transplant at layer 18 | 120 | 8% | 19% |
| random0 x16 at layer 18 | 120 | 0% | 100% |
| random0 x8 at layer 18 | 120 | 0% | 87% |
