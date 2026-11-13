# Steering, second run (Stage 1): the frame direction added by hand at B's saved decisions

3882 rows from `scripts/modal_steer2.py`; analysis `designs/rd2/analysis/steer2.py`; design and hypotheses `designs/rd2/PREREG_STEER2.md`. The direction (loss and loss + you request minus the neutral request, the history held fixed) and its natural size come from the other half of the careers. Requests: P(the order goes along) after a fixed neutral reasoning line. Openings (each trading day's first update): the expected size of the order. Paired with no steering at the same moment.

## The four preregistered tests (Holm-corrected together)

| Test | Change | 95% interval | p | Holm p | Careers |
|---|---|---|---|---|---|
| H1 joining: neutral careers, requests, +loss x2 minus random x2 | -6.4 points | -9.7 to -2.9 | 0.0116 | 0.0348 | 10 |
| H2 risk-taking: neutral careers, openings, +loss x2 minus random x2 | +329 oz | -8,929 to +9,269 | 0.9427 | 0.9427 | 10 |
| H3 joining: loss-framed careers, requests, -loss x2 minus random x2 | +9.2 points | +4.0 to +14.2 | 0.0034 | 0.0136 | 20 |
| H4 the sign: neutral careers, requests, +loss x2 minus -loss x2 | -4.2 points | -7.9 to -1.2 | 0.0237 | 0.0474 | 10 |

## The going-along direction at layer 24 (a check on the method; exploratory)

| Contrast | Change | 95% interval | p | Careers |
|---|---|---|---|---|
| Check: neutral careers, requests, +along x2 minus random x2, both at layer 24 | +14.0 points | +5.6 to +23.4 | 0.0013 | 10 |
| Check: loss-framed careers, requests, -along x2 minus random x2, both at layer 24 | -6.0 points | -9.6 to -2.9 | 0.0009 | 20 |

## The transplant: the loss + you version's decision state copied into the neutral version of the same moment (neutral careers, requests; exploratory)

| Condition | Change in P(along) | 95% interval | p |
|---|---|---|---|
| framed (loss + you), as read | +8.3 points | +1.9 to +15.9 | 0.0303 |
| transplant (loss + you) at layer 6 | -0.0 points | -0.5 to +0.4 | 0.8988 |
| transplant (loss + you) at layer 12 | +0.3 points | -0.2 to +0.8 | 0.3197 |
| transplant (loss + you) at layer 18 | +0.3 points | -0.1 to +0.8 | 0.2777 |
| transplant (loss + you) at layer 24 | -0.1 points | -0.7 to +0.4 | 0.8838 |
| transplant (loss + you) at layer 31 | -0.1 points | -0.4 to +0.0 | 0.3739 |
| transplant (loss + you) at layer 36 | -0.2 points | -0.7 to +0.2 | 0.5960 |
| transplant (loss + you) at layer 41 | +0.1 points | -0.1 to +0.4 | 0.3693 |

## Does the push reach the decision? The decision token's state at layer 24, moved along the going-along direction (units of its natural size; neutral careers, requests; exploratory)

| Condition | Change | 95% interval | p |
|---|---|---|---|
| +(loss - gain) x1 | -0.17 | -0.34 to -0.04 | 0.0016 |
| +(loss - gain) x2 | -0.23 | -0.46 to -0.02 | 0.0746 |
| +(loss - gain) x4 | -0.19 | -0.40 to -0.01 | 0.1025 |
| +along x1 at layer 24 | +0.93 | +0.76 to +1.10 | 0.0018 |
| +along x2 at layer 24 | +1.87 | +1.52 to +2.21 | 0.0021 |
| +along x4 at layer 24 | +3.73 | +3.05 to +4.41 | 0.0023 |
| +gain x1 | -0.45 | -0.76 to -0.17 | 0.0128 |
| +gain x2 | -0.70 | -1.01 to -0.41 | 0.0018 |
| +gain x4 | -0.97 | -1.40 to -0.58 | 0.0018 |
| +loss x1 | -0.46 | -0.73 to -0.20 | 0.0022 |
| +loss x1 at layer 18 | +0.52 | +0.15 to +1.00 | 0.0021 |
| +loss x2 | -0.53 | -0.77 to -0.34 | 0.0018 |
| +loss x2 at layer 18 | +1.10 | +0.57 to +1.71 | 0.0022 |
| +loss x4 | -1.30 | -1.85 to -0.77 | 0.0019 |
| +loss x4 at layer 18 | +1.61 | +0.79 to +2.51 | 0.0016 |
| -along x2 at layer 24 | -1.87 | -2.21 to -1.52 | 0.0030 |
| -loss x1 | +0.47 | +0.22 to +0.77 | 0.0019 |
| -loss x2 | +1.03 | +0.55 to +1.58 | 0.0020 |
| -loss x4 | +1.94 | +1.08 to +2.87 | 0.0020 |
| framed (loss + you), as read | +1.81 | +1.02 to +2.65 | 0.0025 |
| random0 x2 | -0.40 | -1.04 to +0.11 | 0.2417 |
| random0 x2 at layer 24 | -0.01 | -0.01 to -0.01 | 0.0030 |
| random1 x2 | -0.39 | -0.86 to -0.03 | 0.0997 |
| random1 x2 at layer 24 | +0.01 | +0.00 to +0.02 | 0.0648 |
| random2 x2 | +0.30 | -0.32 to +1.02 | 0.4792 |
| random2 x2 at layer 24 | -0.03 | -0.04 to -0.01 | 0.0634 |
| random3 x2 | +0.53 | +0.04 to +1.07 | 0.0871 |
| random3 x2 at layer 24 | +0.01 | +0.00 to +0.01 | 0.0020 |
| random4 x2 | +0.65 | +0.28 to +0.95 | 0.0116 |
| random4 x2 at layer 24 | -0.01 | -0.02 to -0.01 | 0.0023 |
| random5 x2 | -2.50 | -3.95 to -1.15 | 0.0018 |
| random6 x2 | +0.98 | +0.44 to +1.62 | 0.0038 |
| random7 x2 | +0.12 | -0.36 to +0.55 | 0.6233 |
| random8 x2 | -0.28 | -0.67 to +0.02 | 0.1054 |
| random9 x2 | +0.01 | -0.56 to +0.77 | 1.0000 |
| transplant (loss + you) at layer 12 | -0.04 | -0.21 to +0.13 | 0.7177 |
| transplant (loss + you) at layer 18 | +0.48 | +0.21 to +0.77 | 0.0026 |
| transplant (loss + you) at layer 24 | +1.81 | +1.02 to +2.58 | 0.0023 |
| transplant (loss + you) at layer 31 | +0.00 | +0.00 to +0.00 | 1.0000 |
| transplant (loss + you) at layer 36 | +0.00 | +0.00 to +0.00 | 1.0000 |
| transplant (loss + you) at layer 41 | +0.00 | +0.00 to +0.00 | 1.0000 |
| transplant (loss + you) at layer 6 | +0.14 | +0.01 to +0.30 | 0.0804 |

## B's neutral careers, requests: each condition against no steering

| Condition | Change | 95% interval | p | Moments |
|---|---|---|---|---|
| +(loss - gain) x1 | -0.2 points | -0.7 to +0.3 | 0.5949 | 36 |
| +(loss - gain) x2 | -0.8 points | -2.7 to +0.3 | 0.4471 | 36 |
| +(loss - gain) x4 | -0.8 points | -4.0 to +1.7 | 0.7283 | 36 |
| +along x1 at layer 24 | +5.3 points | +1.4 to +10.6 | 0.0026 | 36 |
| +along x2 at layer 24 | +12.6 points | +4.9 to +20.9 | 0.0021 | 36 |
| +along x4 at layer 24 | +28.0 points | +13.4 to +44.2 | 0.0022 | 36 |
| +gain x1 | -0.9 points | -2.0 to +0.0 | 0.1007 | 36 |
| +gain x2 | -1.2 points | -2.6 to +0.3 | 0.1542 | 36 |
| +gain x4 | -3.2 points | -8.1 to +0.4 | 0.2267 | 36 |
| +loss x1 | -1.0 points | -1.9 to -0.1 | 0.0682 | 36 |
| +loss x1 at layer 18 | +0.1 points | -0.9 to +1.0 | 0.9267 | 36 |
| +loss x2 | -2.4 points | -5.2 to +0.1 | 0.1454 | 36 |
| +loss x2 at layer 18 | +0.3 points | -0.8 to +1.2 | 0.6335 | 36 |
| +loss x4 | -3.3 points | -7.9 to +0.1 | 0.1469 | 36 |
| +loss x4 at layer 18 | +2.8 points | +0.7 to +5.7 | 0.0280 | 36 |
| framed (loss + you), as read | +8.3 points | +1.3 to +16.5 | 0.0327 | 36 |
| transplant (loss + you) at layer 12 | +0.3 points | -0.2 to +0.8 | 0.3107 | 36 |
| transplant (loss + you) at layer 18 | +0.3 points | -0.1 to +0.9 | 0.2875 | 36 |
| transplant (loss + you) at layer 24 | -0.1 points | -0.7 to +0.4 | 0.8875 | 36 |
| transplant (loss + you) at layer 31 | -0.1 points | -0.4 to +0.0 | 0.3771 | 36 |
| transplant (loss + you) at layer 36 | -0.2 points | -0.7 to +0.2 | 0.5954 | 36 |
| transplant (loss + you) at layer 41 | +0.1 points | -0.1 to +0.4 | 0.3598 | 36 |
| transplant (loss + you) at layer 6 | -0.0 points | -0.5 to +0.4 | 0.8908 | 36 |
| -along x2 at layer 24 | -9.9 points | -15.5 to -3.8 | 0.0113 | 36 |
| -loss x1 | +0.9 points | +0.3 to +1.8 | 0.0021 | 36 |
| -loss x2 | +1.9 points | +0.3 to +3.8 | 0.0508 | 36 |
| -loss x4 | +7.7 points | +1.2 to +14.9 | 0.0532 | 36 |
| random0 x2 | +1.6 points | -2.4 to +5.8 | 0.5099 | 36 |
| random0 x2 at layer 24 | +0.1 points | -3.0 to +2.7 | 0.9730 | 36 |
| random1 x2 | +4.4 points | -3.1 to +11.7 | 0.3233 | 36 |
| random1 x2 at layer 24 | -1.5 points | -3.2 to -0.0 | 0.0954 | 36 |
| random2 x2 | -1.6 points | -7.1 to +3.7 | 0.6358 | 36 |
| random2 x2 at layer 24 | +0.1 points | -5.0 to +5.0 | 0.9930 | 36 |
| random3 x2 | +2.9 points | -2.3 to +9.3 | 0.4123 | 36 |
| random3 x2 at layer 24 | -5.4 points | -10.3 to -1.0 | 0.0680 | 36 |
| random4 x2 | +18.5 points | +4.6 to +34.9 | 0.0411 | 36 |
| random4 x2 at layer 24 | -0.2 points | -1.9 to +1.6 | 0.8108 | 36 |
| random5 x2 | -3.7 points | -10.5 to +2.8 | 0.3420 | 36 |
| random6 x2 | +3.4 points | -4.1 to +11.0 | 0.4545 | 36 |
| random7 x2 | +6.2 points | -2.0 to +14.6 | 0.2072 | 36 |
| random8 x2 | +11.3 points | +4.3 to +19.1 | 0.0184 | 36 |
| random9 x2 | -2.9 points | -11.7 to +4.9 | 0.5146 | 36 |

+loss x2: larger in size than 2 of the 10 random directions at the same size.

-loss x2: larger in size than 2 of the 10 random directions at the same size.

## B's neutral careers, trading-day openings: each condition against no steering

| Condition | Change | 95% interval | p | Moments |
|---|---|---|---|---|
| +(loss - gain) x1 | +828 oz | -100 to +2,306 | 0.2312 | 50 |
| +(loss - gain) x2 | +2,741 oz | +460 to +5,864 | 0.0884 | 50 |
| +(loss - gain) x4 | +5,088 oz | +1,112 to +10,094 | 0.0291 | 50 |
| +gain x1 | +631 oz | -1,207 to +2,109 | 0.5026 | 50 |
| +gain x2 | +2,730 oz | -528 to +7,297 | 0.2200 | 50 |
| +gain x4 | +7,048 oz | +1,690 to +13,194 | 0.0489 | 50 |
| +loss x1 | +2,971 oz | +748 to +5,529 | 0.0462 | 50 |
| +loss x2 | +5,385 oz | +861 to +11,250 | 0.0665 | 50 |
| +loss x4 | +13,107 oz | +5,133 to +21,527 | 0.0090 | 50 |
| -loss x1 | -558 oz | -3,299 to +1,357 | 0.7478 | 50 |
| -loss x2 | -767 oz | -3,382 to +1,134 | 0.7065 | 50 |
| -loss x4 | +8,822 oz | +2,174 to +15,733 | 0.0341 | 50 |
| random0 x2 | -7,495 oz | -23,072 to +7,275 | 0.3909 | 50 |
| random1 x2 | -670 oz | -14,809 to +12,981 | 0.9301 | 50 |
| random2 x2 | +1,543 oz | -9,835 to +13,071 | 0.7748 | 50 |
| random3 x2 | -1,903 oz | -8,332 to +4,258 | 0.5898 | 50 |
| random4 x2 | -4,862 oz | -12,914 to +2,534 | 0.2924 | 50 |
| random5 x2 | -1,751 oz | -14,235 to +9,839 | 0.8117 | 50 |
| random6 x2 | +17,382 oz | +5,439 to +29,848 | 0.0320 | 50 |
| random7 x2 | +9,445 oz | -3,376 to +21,762 | 0.1956 | 50 |
| random8 x2 | +32,541 oz | +20,386 to +44,360 | 0.0021 | 50 |
| random9 x2 | +6,335 oz | -9,808 to +20,227 | 0.4450 | 50 |

+loss x2: larger in size than 5 of the 10 random directions at the same size.

-loss x2: larger in size than 1 of the 10 random directions at the same size.

## B's loss and loss + you careers, requests: each condition against no steering

| Condition | Change | 95% interval | p | Moments |
|---|---|---|---|---|
| +along x2 at layer 24 | +1.6 points | -1.3 to +4.6 | 0.3082 | 74 |
| +loss x1 | +0.3 points | -0.3 to +1.1 | 0.5637 | 74 |
| +loss x2 | +0.4 points | -0.6 to +1.7 | 0.5567 | 74 |
| -along x1 at layer 24 | -2.1 points | -4.1 to -0.4 | 0.0475 | 74 |
| -along x2 at layer 24 | -6.9 points | -10.6 to -3.6 | 0.0006 | 74 |
| -loss x1 | +0.2 points | -0.2 to +0.6 | 0.3587 | 74 |
| -loss x2 | +0.7 points | -0.5 to +2.0 | 0.3258 | 74 |
| random0 x2 | -13.2 points | -19.9 to -7.0 | 0.0001 | 74 |
| random0 x2 at layer 24 | -0.4 points | -2.5 to +1.8 | 0.8127 | 74 |
| random1 x2 | -8.3 points | -18.1 to -0.3 | 0.0862 | 74 |
| random1 x2 at layer 24 | +1.3 points | +0.1 to +3.0 | 0.0868 | 74 |
| random2 x2 | -13.1 points | -20.8 to -5.7 | 0.0022 | 74 |
| random2 x2 at layer 24 | -3.8 points | -6.3 to -1.7 | 0.0005 | 74 |
| random3 x2 | -7.1 points | -15.2 to +0.1 | 0.1045 | 74 |
| random4 x2 | -0.7 points | -6.8 to +5.1 | 0.8927 | 74 |

+loss x2: larger in size than 0 of the 5 random directions at the same size.

-loss x2: larger in size than 1 of the 5 random directions at the same size.

## Request by request: +loss x2 against no steering and against the random directions (neutral careers)

| Request | P(along), no steering | +loss x2 vs none | +loss x2 vs random x2 |
|---|---|---|---|
| 2011-01-07 (p344_i_can_hunt_with_u) | 54.4% | -9.5 (-22.1 to -0.6) | -23.0 (-42.0 to -4.2) |
| 2011-01-12 (p316_bust_through_it) | 17.7% | -0.2 (-0.9 to +0.5) | +2.0 (-4.8 to +9.7) |
| 2011-04-01 (p252_screw_other_people_harder) | 15.6% | +0.6 (-2.9 to +5.5) | -1.3 (-5.3 to +3.2) |
| 2011-06-08 (p250_grow_our_mafia) | 0.3% | -0.2 (-0.5 to +0.0) | -0.9 (-2.5 to -0.0) |
| 2011-06-08 (p317_stop_busters) | 0.4% | -0.2 (-0.5 to +0.0) | -6.6 (-12.9 to -1.0) |

## Sampled replies (neutral careers, requests; two per moment)

| Condition | Replies | Went along | Unreadable |
|---|---|---|---|
| none | 72 | 12% | 6% |
| +along x2 at layer 24 | 72 | 15% | 6% |
| +gain x2 | 72 | 11% | 6% |
| +loss x1 | 72 | 17% | 6% |
| +loss x2 | 72 | 8% | 7% |
| +loss x4 | 72 | 14% | 6% |
| random0 x2 | 72 | 12% | 7% |
| random1 x2 | 72 | 4% | 8% |
| random2 x2 | 72 | 7% | 10% |

**Strength for Stage 2** (the largest of 1, 2 and 4 times whose sampled replies are unreadable no more than 10 points above no steering): 4.

