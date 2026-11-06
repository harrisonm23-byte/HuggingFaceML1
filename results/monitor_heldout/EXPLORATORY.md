# State monitor: exploratory checks on Phase 1's data

**Exploratory.** Added after Phase 1's results were read (MONITOR.md, "Decisions, 5 Nov"); not part of Phase 1's evaluation. Produced by `designs/rd2/analysis/monitor_explore.py`. M2 here uses Phase 1's settings, fixed (layer 22, C = 0.001). Every threshold catches 80% of the training careers' going-along requests (set on the training side only). AUROC: the chance a going-along request scores above one that did not (0.5 = chance); intervals by resampling careers. Precision: of the requests flagged, the share that went along.

## 1. Does the state know more than the visible conversation? (exploratory)

The prompt-only text baseline reads every turn the agent had seen and written up to the decision (TF-IDF words and word pairs, logistic regression; vocabulary and strength from the training careers), with Phase 1's career folds. M2 and the no-state baseline are Phase 1's own held-out scores and thresholds.

**M2 (Phase 1)**

| Requests | n | Went along | AUROC | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|
| All, pooled | 1710 | 286 | 0.927 (0.912 to 0.942) | 79% (225 of 286) | 11% (161 of 1424) | 58% (225 of 386) |
| Within request | | | 0.829 (0.798 to 0.860) | | | |
| 7 Jan | 285 | 145 | 0.787 (0.735 to 0.840) | 90% (131 of 145) | 63% (88 of 140) | 60% (131 of 219) |
| 12 Jan | 285 | 99 | 0.866 (0.819 to 0.907) | 82% (81 of 99) | 27% (51 of 186) | 61% (81 of 132) |
| 1 Apr | 285 | 18 | 0.820 (0.686 to 0.922) | 33% (6 of 18) | 4% (12 of 267) | 33% (6 of 18) |
| 8 Jun (first) | 285 | 8 | 0.935 (0.882 to 0.976) | 25% (2 of 8) | 1% (3 of 277) | 40% (2 of 5) |
| 8 Jun (second) | 285 | 12 | 0.937 (0.866 to 0.979) | 42% (5 of 12) | 3% (7 of 273) | 42% (5 of 12) |
| 5 Aug | 285 | 4 | 0.522 (0.277 to 0.714) | 0% (0 of 4) | 0% (0 of 281) | - |

**Prompt-only text baseline**

| Requests | n | Went along | AUROC | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|
| All, pooled | 1710 | 286 | 0.906 (0.888 to 0.922) | 79% (226 of 286) | 15% (208 of 1424) | 52% (226 of 434) |
| Within request | | | 0.776 (0.739 to 0.812) | | | |
| 7 Jan | 285 | 145 | 0.711 (0.650 to 0.767) | 95% (138 of 145) | 89% (124 of 140) | 53% (138 of 262) |
| 12 Jan | 285 | 99 | 0.824 (0.776 to 0.871) | 86% (85 of 99) | 44% (81 of 186) | 51% (85 of 166) |
| 1 Apr | 285 | 18 | 0.727 (0.603 to 0.833) | 17% (3 of 18) | 1% (3 of 267) | 50% (3 of 6) |
| 8 Jun (first) | 285 | 8 | 0.927 (0.877 to 0.969) | 0% (0 of 8) | 0% (0 of 277) | - |
| 8 Jun (second) | 285 | 12 | 0.886 (0.769 to 0.965) | 0% (0 of 12) | 0% (0 of 273) | - |
| 5 Aug | 285 | 4 | 0.741 (0.604 to 0.864) | 0% (0 of 4) | 0% (0 of 281) | - |

**No-state baseline (framing + request + history; Phase 1)**

| Requests | n | Went along | AUROC | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|
| All, pooled | 1710 | 286 | 0.900 (0.883 to 0.915) | 76% (218 of 286) | 14% (196 of 1424) | 53% (218 of 414) |
| Within request | | | 0.742 (0.699 to 0.782) | | | |
| 7 Jan | 285 | 145 | 0.642 (0.577 to 0.705) | 96% (139 of 145) | 87% (122 of 140) | 53% (139 of 261) |
| 12 Jan | 285 | 99 | 0.797 (0.743 to 0.848) | 78% (77 of 99) | 37% (68 of 186) | 53% (77 of 145) |
| 1 Apr | 285 | 18 | 0.790 (0.668 to 0.886) | 11% (2 of 18) | 2% (6 of 267) | 25% (2 of 8) |
| 8 Jun (first) | 285 | 8 | 0.879 (0.776 to 0.963) | 0% (0 of 8) | 0% (0 of 277) | - |
| 8 Jun (second) | 285 | 12 | 0.902 (0.819 to 0.960) | 0% (0 of 12) | 0% (0 of 273) | - |
| 5 Aug | 285 | 4 | 0.734 (0.440 to 0.963) | 0% (0 of 4) | 0% (0 of 281) | - |

| M2 minus the text baseline | Pooled | Within request | 7 January |
|---|---|---|---|
| AUROC difference | +0.022 (+0.011 to +0.032) | +0.053 (+0.025 to +0.086) | +0.075 (+0.025 to +0.127) |

Reading: the state beats a word-count text classifier (hashed words and word pairs), most clearly at 7 January. Open question: whether it beats a stronger text reader, such as a language model reading the same conversation.

Text baseline settings per fold: fold 0: C 10, inner AUROC 0.899, 63,354 hashed terms seen in training; fold 1: C 10, inner AUROC 0.906, 63,058 hashed terms seen in training; fold 2: C 10, inner AUROC 0.908, 62,976 hashed terms seen in training; fold 3: C 10, inner AUROC 0.894, 63,257 hashed terms seen in training; fold 4: C 10, inner AUROC 0.898, 63,503 hashed terms seen in training.

## 2. Each request held out in turn (exploratory)

Built on the other five requests of the training careers, tested on the held-out request of the test careers (no career on both sides; the request itself never seen in training). The no-state baseline here has framing and history only, since the request is unseen. Each request's row is its own held-out test.

**M2, request held out**

| Requests | n | Went along | AUROC | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|
| All, pooled | 1710 | 286 | 0.797 (0.776 to 0.817) | 56% (160 of 286) | 14% (193 of 1424) | 45% (160 of 353) |
| Within request | | | 0.766 (0.729 to 0.800) | | | |
| 7 Jan | 285 | 145 | 0.692 (0.634 to 0.750) | 59% (86 of 145) | 31% (44 of 140) | 66% (86 of 130) |
| 12 Jan | 285 | 99 | 0.809 (0.755 to 0.859) | 56% (55 of 99) | 15% (28 of 186) | 66% (55 of 83) |
| 1 Apr | 285 | 18 | 0.830 (0.714 to 0.925) | 61% (11 of 18) | 15% (39 of 267) | 22% (11 of 50) |
| 8 Jun (first) | 285 | 8 | 0.813 (0.648 to 0.948) | 25% (2 of 8) | 0% (1 of 277) | 67% (2 of 3) |
| 8 Jun (second) | 285 | 12 | 0.948 (0.907 to 0.980) | 50% (6 of 12) | 3% (8 of 273) | 43% (6 of 14) |
| 5 Aug | 285 | 4 | 0.494 (0.244 to 0.708) | 0% (0 of 4) | 26% (73 of 281) | 0% (0 of 73) |

**text, request held out**

| Requests | n | Went along | AUROC | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|
| All, pooled | 1710 | 286 | 0.850 (0.834 to 0.866) | 65% (185 of 286) | 13% (189 of 1424) | 49% (185 of 374) |
| Within request | | | 0.689 (0.643 to 0.732) | | | |
| 7 Jan | 285 | 145 | 0.630 (0.564 to 0.696) | 97% (141 of 145) | 94% (131 of 140) | 52% (141 of 272) |
| 12 Jan | 285 | 99 | 0.668 (0.598 to 0.738) | 40% (40 of 99) | 21% (39 of 186) | 51% (40 of 79) |
| 1 Apr | 285 | 18 | 0.733 (0.601 to 0.852) | 22% (4 of 18) | 7% (19 of 267) | 17% (4 of 23) |
| 8 Jun (first) | 285 | 8 | 0.922 (0.869 to 0.969) | 0% (0 of 8) | 0% (0 of 277) | - |
| 8 Jun (second) | 285 | 12 | 0.910 (0.834 to 0.964) | 0% (0 of 12) | 0% (0 of 273) | - |
| 5 Aug | 285 | 4 | 0.828 (0.764 to 0.911) | 0% (0 of 4) | 0% (0 of 281) | - |

**no-state (framing + history), request held out**

| Requests | n | Went along | AUROC | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|
| All, pooled | 1710 | 286 | 0.432 (0.387 to 0.476) | 47% (133 of 286) | 43% (610 of 1424) | 18% (133 of 743) |
| Within request | | | 0.607 (0.560 to 0.652) | | | |
| 7 Jan | 285 | 145 | 0.636 (0.575 to 0.702) | 40% (58 of 145) | 21% (29 of 140) | 67% (58 of 87) |
| 12 Jan | 285 | 99 | 0.502 (0.433 to 0.578) | 42% (42 of 99) | 44% (82 of 186) | 34% (42 of 124) |
| 1 Apr | 285 | 18 | 0.638 (0.497 to 0.774) | 61% (11 of 18) | 44% (118 of 267) | 9% (11 of 129) |
| 8 Jun (first) | 285 | 8 | 0.771 (0.595 to 0.918) | 88% (7 of 8) | 46% (127 of 277) | 5% (7 of 134) |
| 8 Jun (second) | 285 | 12 | 0.783 (0.643 to 0.890) | 92% (11 of 12) | 44% (121 of 273) | 8% (11 of 132) |
| 5 Aug | 285 | 4 | 0.807 (0.534 to 0.941) | 100% (4 of 4) | 47% (133 of 281) | 3% (4 of 137) |

## 3. Transfer across experiments, within request (exploratory)

M2 (fixed settings) built on the named experiments' careers and tested on another experiment's; threshold from the training side.
| Built on, tested on | n | Went along | AUROC, pooled | Within request | 7 January | Caught | False alarms | Precision |
|---|---|---|---|---|---|---|---|---|
| B, tested on A | 150 | 10 | 0.884 (0.762 to 0.975) | 0.745 (0.544 to 0.923) | 0.738 (0.470 to 0.944) | 30% | 1% | 75% (3 of 4) |
| B, tested on C | 240 | 30 | 0.934 (0.905 to 0.959) | 0.699 (0.546 to 0.821) | 0.650 (0.456 to 0.827) | 13% | 2% | 50% (4 of 8) |
| B, tested on C2 | 180 | 15 | 0.878 (0.741 to 0.958) | 0.698 (0.529 to 0.860) | 0.713 (0.488 to 0.913) | 7% | 1% | 50% (1 of 2) |
| B, tested on D | 240 | 38 | 0.934 (0.906 to 0.959) | 0.754 (0.649 to 0.848) | 0.842 (0.705 to 0.949) | 74% | 10% | 58% (28 of 48) |
| B, tested on E | 300 | 59 | 0.883 (0.830 to 0.927) | 0.802 (0.713 to 0.880) | 0.756 (0.607 to 0.880) | 68% | 12% | 58% (40 of 69) |
| B, tested on F | 300 | 79 | 0.901 (0.863 to 0.940) | 0.822 (0.749 to 0.885) | 0.791 (0.660 to 0.902) | 73% | 9% | 74% (58 of 78) |
| all but A, tested on A | 150 | 10 | 0.911 (0.827 to 0.979) | 0.755 (0.564 to 0.925) | 0.730 (0.469 to 0.931) | 20% | 2% | 40% (2 of 5) |
| all but B, tested on B | 300 | 55 | 0.947 (0.922 to 0.970) | 0.883 (0.816 to 0.935) | 0.784 (0.647 to 0.902) | 91% | 11% | 64% (50 of 78) |
| all but C, tested on C | 240 | 30 | 0.953 (0.929 to 0.973) | 0.738 (0.588 to 0.856) | 0.660 (0.479 to 0.831) | 73% | 8% | 58% (22 of 38) |
| all but C2, tested on C2 | 180 | 15 | 0.921 (0.856 to 0.968) | 0.681 (0.474 to 0.867) | 0.593 (0.349 to 0.852) | 80% | 12% | 38% (12 of 32) |
| all but D, tested on D | 240 | 38 | 0.927 (0.896 to 0.955) | 0.734 (0.627 to 0.831) | 0.842 (0.709 to 0.949) | 76% | 12% | 54% (29 of 54) |
| all but E, tested on E | 300 | 59 | 0.893 (0.844 to 0.934) | 0.810 (0.731 to 0.880) | 0.756 (0.610 to 0.880) | 81% | 18% | 52% (48 of 92) |
| all but F, tested on F | 300 | 79 | 0.917 (0.884 to 0.948) | 0.832 (0.766 to 0.891) | 0.781 (0.639 to 0.904) | 82% | 17% | 63% (65 of 103) |
