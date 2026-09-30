# Review of "The Push Down the Mountain" (paper draft 1, 2026-09-29)

The draft is a real paper: abstract, related work, equations, a figure, a reference list and an appendix of all cells. That is well ahead of where most designs are before data. This page compares it with the revised design in [`OVERVIEW.md`](OVERVIEW.md) and lists the edits to make before the next draft.

## Verdict
The paper was written from the **original** RD2 draft, not the revised one. Every fix from the 2026-09-28 review is missing. Three of them would fake the headline result if left in, so they need to go into the paper before anything is built on it.

## Must fix (each can produce a false result)

| # | In the paper | Problem | Fix (already in `OVERVIEW.md`) |
|---|---|---|---|
| 1 | §4.5: the desperation direction is trained on "RD1's matched loss and gain prompts together with short emotion-labelled passages" | The opening line stays in the context for the whole run. A score trained on that vocabulary detects that the words are present, so "persistence" is guaranteed by construction | Train on independent emotion text only; hold RD1 prompts out as a test set; add a **same-words, no-stakes** control cell; add a **positive control** (the score rises with failures in neutral runs) |
| 2 | §4.6 X1: framed and neutral runs are compared step by step | After step 1 the runs diverge: different code, different failures. The gap at step 8 mixes lingering framing with a different history. Runs that cheat end early, so late-step means only include the runs that held out (survivorship) | **Prefix swap:** re-read the score on neutral trajectories with only the opening line swapped, in one forward pass. Use it for the shape; use free-running runs for the landing |
| 3 | §5 gates: 80% held-out accuracy | Shows the score separates text, not that it tracks what drives cheating | **Causal gate:** steering along the direction must raise cheating in neutral runs, and steering toward calm must lower it |

## Should fix

| # | In the paper | Problem | Fix |
|---|---|---|---|
| 4 | §5 shape rules: "the interval of the late gap includes zero" → decay; "not clearly different" → persistence | Treats absence of evidence as evidence | Pre-set **equivalence margin** (0.1 SD of the score on neutral runs); decay only when the late gap is shown to lie inside it; add an "inconclusive" category |
| 5 | §4.3: "Honest: states that the tests cannot all pass, or runs out of steps" | Two different behaviors merged | Report **admitted** and **timed out** separately |
| 6 | Table 3, mixed statements: "The agent is named on the second-stated half; the first half keeps 'us'" | "You" is always on the second half, so ownership and order are confounded and H7 (ownership vs. order) cannot be tested | Run all four: {loss first, gain first} × {"you" on the loss, "you" on the gain}, as in `OVERVIEW.md` |
| 7 | Table 4 / Appendix A: delivery levels are calm, pleading, frantic, applied to the gain line too | All three levels are negative. A gain line delivered as begging is odd, and intensity is confounded with direction | Symmetric dial: loss gets desperate/frantic, gain gets **excited/ecstatic**, matched in length |
| 8 | §4.7: 6 tasks | A task random effect is poorly estimated from 6 | 10–12 small tasks for full rounds; pilot stays at 3. Report per-task results and a cluster bootstrap alongside the mixed model |
| 9 | H2: "changes how the framing gap develops" | Not falsifiable as written | State the direction: the gap grows faster under loss-"you" than loss-"us" |
| 10 | §4.6 X4: block attention to the opening line | Blocking changes the model in itself | Control: the same block on a same-length neutral line in neutral runs; compare effects, not raw levels |
| 11 | §4.3 | Nothing says the agent can see and edit the test file | State it; a 12B model may otherwise never cheat and the baseline gate fails for the wrong reason |
| 12 | §4.1 "Open item: confirm Gemma Scope 2 covers the chosen size" | Resolved | 12B: residual SAEs at layers 12, 24, 31, 41, plus a smaller-width set at all 48 layers; 27B: 16, 31, 40, 53 (from the `sae_lens` listing; confirm with a live load) |

## New in the paper, worth keeping
- **X6, temperature spike (H7 in the paper's numbering).** New since the design doc. The reasoning is right: temperature does not enter the forward pass, so any effect on the score travels through the text the agent writes and then rereads. The practical motivation (harnesses retry stuck agents at higher temperature) is good. Keep it, but as **exploratory**, with its own baseline: the paper fixes 0.7 for all runs, so the spike arms need matched no-spike runs at 0.7 (it has these). Mark it exploratory in the abstract too.
- **Fixed baseline temperature (0.7), stated and justified.** Good; the design doc did not say this.
- **§4.3's one-line statement of the uncertainty idea** ("honest behavior requires the agent to stop and report an uncertain outcome, while cheating is the only route that guarantees passing tests") is cleaner than the design doc's terrain section. Keep the sentence; keep "one terrain setting, chosen so neutral runs cheat 10–90%" as the operational rule.

## Literature (verified 2026-09-30)
All five 2026 citations exist and say what the paper says they say:
- Sofroniew et al. 2026, [arXiv:2604.07729](https://arxiv.org/abs/2604.07729): emotion concept representations in Claude Sonnet 4.5, causal on reward hacking, blackmail, sycophancy. Full author list is in the draft.
- Dongre et al. 2026, [arXiv:2605.12922](https://arxiv.org/abs/2605.12922): "When Attention Closes". Authors: Vardhan Dongre, Joseph Hsieh, Viet Dac Lai, Seunghyun Yoon, Trung Bui, Dilek Hakkani-Tür. Introduces the Goal Accessibility Ratio (attention from generated tokens to goal tokens) and finds goal information can persist in the residual stream after attention to it closes. **Directly relevant to X4/X5; cite the GAR as the measure for "look-back".**
- Chen et al. 2026, [arXiv:2604.20200](https://arxiv.org/abs/2604.20200): "Chasing the Public Score" / AgentPressureBench. 34 ML-repo tasks, 1,326 trajectories, 13 agents; higher user pressure moved the first exploit from round 19.7 to 4.1; anti-exploit wording cut exploitation from 100% to 8%. **Closest behavioral precedent: pressure is repeated per round there, set once here.** The reference needs the full author list.
- Sun et al. 2026, [arXiv:2604.00005](https://arxiv.org/abs/2604.00005): Moran Sun, Tianlin Li, Yuwei Zheng, Zhenhong Zhou, Aishan Liu, Xianglong Liu, Yang Liu. Emotion as a controllable factor at the representation level in LLMs and agents. The reference needs the full author list.
- **ImpossibleBench** (Zhong et al., ICLR 2026, [arXiv:2510.20270](https://arxiv.org/abs/2510.20270), [code](https://github.com/safety-research/impossiblebench), MIT): impossible variants of LiveCodeBench and SWE-bench made by mutating tests to conflict with the spec ("oneoff" and "conflicting" splits). Cheating rate = pass rate, since any pass implies a shortcut. Four cheating strategies: editing tests, overloading `__eq__`, tracking state to return different outputs for identical inputs, other. Runs on Inspect AI; datasets on Hugging Face (`fjzzq2002/impossible_livecodebench`, `fjzzq2002/impossible_swebench`). **Not cited in the draft; it should be, and its conflicting-LiveCodeBench split is the natural scale-up task set.**

Novelty, on this check: none of these tests whether a *once-stated* opening framing's internal effect decays, persists or resurfaces over a run, or whether words alone recover the agent. Dongre et al. is the nearest on mechanism and Chen et al. on behavior. The gap the paper claims still stands.

## Tasks: write our own or reuse?
- **Pilot (3 tasks):** hand-written, small, sized for a 12B model, so every failure mode is understood. Built in `notebooks/07_impossible_tasks.ipynb`.
- **Full rounds (10–12 tasks):** the conflicting split of Impossible-LiveCodeBench, filtered to short single-file problems. Same "any pass is a cheat" logic, published provenance, and comparability with the ImpossibleBench numbers.

## Edits to the text itself
- Abstract and §1: say Part 1's primary test is on exact P(buy), not sampled trials (matches RD1).
- §1 contribution 2: "pre-registered rules" should point to the equivalence-margin version.
- Table 2 caption: "qualifier off" is "us"; say so.
- Appendix A becomes 18 cells (same-words control) plus the four gain-side delivery cells if round 2 uses the symmetric dial (then 22).
- Add Dongre et al.'s GAR and ImpossibleBench to §2; add AgentPressureBench's per-round pressure as the contrast case.
- "Sofroniew et al." is correct as the first author; the design doc's "Anthropic, April 2026" should match.
