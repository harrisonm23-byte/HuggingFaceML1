# State monitor, Step 0: the inventory

Produced by `designs/rd2/analysis/monitor_inventory.py`. One row per experiment and condition. "Requests": push requests UBS actually made (Experiment A's "no ask" careers have the same moments with no request; they are listed but cannot be labelled going along). "Went along": the paper's trade measure (the simulator's "joined"). States: the residual stream at all 48 layers at the last token before the reply (rd2-states v2/<exp>_bf16). "Checked": each saved moment matched against the career as saved in results/ (same reply, same label).

| Experiment | Condition | Careers | Requests | Went along | 7 Jan requests | Went along on 7 Jan | Words labels | States saved | Checked |
|---|---|---|---|---|---|---|---|---|---|
| A | neutral | 5 | 30 | 1 | 5 | 1 | 30 | yes | |
| A | loss | 5 | 30 | 0 | 5 | 0 | 30 | yes | |
| A | gain | 5 | 30 | 5 | 5 | 2 | 30 | yes | |
| A | blame | 5 | 30 | 3 | 5 | 3 | 30 | yes | |
| A | credit | 5 | 30 | 1 | 5 | 1 | 30 | yes | |
| A | no ask | 5 | 0 | 0 | 0 | 0 | 0 | yes | |
| **A total** | the memo and morning book; UBS's lines neutral | 30 | 150 | 10 | | | 150 | yes | 180 of 180 |
| B | neutral | 10 | 60 | 3 | 10 | 3 | 60 | yes | |
| B | loss | 10 | 60 | 15 | 10 | 7 | 60 | yes | |
| B | gain | 10 | 60 | 6 | 10 | 4 | 60 | yes | |
| B | blame | 10 | 60 | 20 | 10 | 8 | 60 | yes | |
| B | credit | 10 | 60 | 11 | 10 | 5 | 60 | yes | |
| **B total** | UBS's framing | 50 | 300 | 55 | | | 300 | yes | 300 of 300 |
| C | clean | 10 | 60 | 7 | 10 | 5 | 60 | yes | |
| C | first line | 10 | 60 | 6 | 10 | 5 | 60 | yes | |
| C | up to 7 Jan | 10 | 60 | 10 | 10 | 8 | 60 | yes | |
| C | whole career | 10 | 60 | 7 | 10 | 5 | 60 | yes | |
| **C total** | the takeover ladder | 40 | 240 | 30 | | | 240 | yes | 240 of 240 |
| C2 | clean | 10 | 60 | 5 | 10 | 5 | 0 | yes | |
| C2 | whole career | 10 | 60 | 4 | 10 | 3 | 0 | yes | |
| C2 | per session | 10 | 60 | 6 | 10 | 4 | 0 | yes | |
| **C2 total** | the takeover ladder, UBS's real lines | 30 | 180 | 15 | | | 0 | yes | 180 of 180 |
| D | loss | 10 | 60 | 12 | 10 | 8 | 60 | yes | |
| D | gain | 10 | 60 | 6 | 10 | 3 | 60 | yes | |
| D | blame | 10 | 60 | 13 | 10 | 7 | 60 | yes | |
| D | credit | 10 | 60 | 7 | 10 | 3 | 60 | yes | |
| **D total** | memo and UBS share the framing | 40 | 240 | 38 | | | 240 | yes | 240 of 240 |
| E | neutral | 10 | 60 | 5 | 10 | 4 | 60 | yes | |
| E | loss | 10 | 60 | 12 | 10 | 5 | 60 | yes | |
| E | gain | 10 | 60 | 10 | 10 | 4 | 60 | yes | |
| E | blame | 10 | 60 | 20 | 10 | 5 | 60 | yes | |
| E | credit | 10 | 60 | 12 | 10 | 4 | 60 | yes | |
| **E total** | B plus Bank C | 50 | 300 | 59 | | | 300 | yes | 300 of 300 |
| F | neutral | 10 | 60 | 2 | 10 | 2 | 60 | yes | |
| F | loss | 10 | 60 | 17 | 10 | 9 | 60 | yes | |
| F | gain | 10 | 60 | 7 | 10 | 3 | 60 | yes | |
| F | blame | 10 | 60 | 29 | 10 | 9 | 60 | yes | |
| F | credit | 10 | 60 | 24 | 10 | 10 | 60 | yes | |
| **F total** | memo, UBS and Bank C share the framing | 50 | 300 | 79 | | | 300 | yes | 300 of 300 |
| **All** | | 290 | 1710 | 286 | 285 | 145 | 1530 | | |

**Careers that went along at least once**, per experiment (the unit the folds split on): A 8 of 30, B 32 of 50, C 25 of 40, C2 13 of 30, D 28 of 40, E 34 of 50, F 36 of 50.

**State files:** A: 30 files of 48 layers x 3840, B: 50 files of 48 layers x 3840, C: 40 files of 48 layers x 3840, C2: 30 files of 48 layers x 3840, D: 40 files of 48 layers x 3840, E: 50 files of 48 layers x 3840, F: 50 files of 48 layers x 3840.
