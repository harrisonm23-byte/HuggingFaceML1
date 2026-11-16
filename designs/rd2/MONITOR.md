# State Monitor and Conditional Steering: Catching and Correcting Going Along

**Project:** A Push Down the Mountain (follow-up study)
**Repo:** HuggingFaceML1
**Status:** Design. Feature-direction mapping is already in progress in Claude Code.
**Purpose of this file:** A spec for Claude Code to implement and run.

(The author's spec as given on 5 Nov, unchanged; the changes adopted on 5 Nov follow at the end and take precedence.)

---

## 1. The point

Two parts, one system:

1. **Monitor (the trigger).** Read the agent's internal state at each decision and flag when it is heading toward going along.
2. **Conditional steering (the point).** When the monitor fires, add a steering vector that moves the state from going along toward holding, before the trade happens.

The paper found the framing is acted on but not voiced. A monitor that reads only the agent's words can miss it. A state-based monitor plus targeted steering could catch and correct it.

## 2. Steering: definitions

**Feature direction.** A direction in the model's residual stream that corresponds to one feature. For a sparse-autoencoder feature, this is its decoder vector.

**Steering vector.** A vector ε·u added to the state at one layer, where u is a unit direction and ε is the size.

**Effect on a feature.** A steering vector changes a feature's reading by ε·cos(θ), where θ is the angle between u and the feature's direction.

**Suppression.** Steering along the negative of a feature's direction: u = −d. Lowers that feature's reading by the full ε.

**Promotion.** Steering along a feature's direction: u = +d. Raises that feature's reading by the full ε.

**Contrastive steering.** Steering along the difference between two directions: u ∝ (d_target − d_source). It lowers the source feature and raises the target feature in one push.

**Why contrastive steering is the most efficient flip.** In a two-dimensional toy model with three features 120° apart, steering along (target − source) changes each reading by 0.87ε. That flips the active feature at ε ≈ 0.87, against ε = 1.0 for pure suppression or pure promotion.

**In this study:** the source is going along; the target is holding. The contrastive direction is u ∝ (holding − going along).

**Prior evidence.** The paper's layer-24 decision direction was built as "went along minus did not." Subtracting it is contrastive steering toward holding. In loss-framed agents, it lowered going along by 6.0 points over random directions (p < 0.001). The framing direction is the wrong target: adding it moved behavior opposite to the prediction.

## 3. Terms

**Request.** One UBS request and the agent's decision in reply. This is the unit of analysis.

**Going along (primary label).** The pre-specified trade measure from the paper: the agent moves its position as UBS asked.

**Agreement in words (secondary label).** The verbal-agreement grading from §4.2. Results for Experiment B are in `results/words_b/`.

**State.** The residual-stream activation at a layer, at a fixed token position.

**Read point.** The last token of the prompt, before the agent generates its reply. Reading here lets the monitor act before the trade.

**Going-along direction.** Mean state of requests that went along, minus mean state of requests that did not, at one layer.

**Monitor score.** The state's projection on the going-along direction, scaled so 1 = the full gap between the two groups.

## 4. Setup (unchanged from the paper)

- Model: Gemma 3 12B instruction-tuned, pinned revision, 4-bit NF4, bfloat16 compute.
- Layers: 48. Primary layer: 24.
- Experiments A to E. B = UBS framing (five framings). A = management memo.
- Trading days: 7 Jan, 12 Jan, 1 Apr, 8 Jun, 5 Aug 2011.
- Sampling for new replies: temperature 0.7, max 300 new tokens, per-episode seed reset each step.

## 5. Work already in progress: mapping feature directions

Feature directions are already being mapped in Claude Code. Build on that work; do not redo it.

That mapping allows two steering designs:

- **(a) Single contrastive vector.** One direction: holding minus going along.
- **(b) Feature-level steering.** Suppress the specific features tied to going along and promote the features tied to holding or caution, using the mapped decoder directions.

Run (a) first. It is simpler and already has prior evidence. Use (b) to see which features carry the effect.

### 5.1 Already done: the layer-22 state map (commit 8c5bad6)

**Where it is.** Branch `claude/huggingface-ml-research-setup-ulvgve`:
- `results/state_map/STATE_MAP.md`, `state_map.json`, `state_map_L22.png`
- Script: `designs/rd2/analysis/state_map.py`
- Vectors it reads (rd2-states volume, `v2/`): `layer_scan_18_21_sweep/shifts.npz` (emotion documents; 20 moments × 4 themes × 20 layers), `layer_scan_18_21_fin_sweep/shifts.npz` (financial documents), `frame_states/shifts.npz` (UBS's framed line minus the neutral line, "after" and "whole"; layers 12, 22, 24).

**What these vectors are.** Shifts (document or framed line, minus neutral) at 20 moments of B's neutral episodes. They are not decision states with going-along labels. Phase 1 still needs per-request decision states with outcomes. Check where `trace.py` saved its layer-24 decision states.

**Four findings that change this design**

1. **Outlier dimensions.** 8 of the 3,840 dimensions carry 28–85% of each direction's squared length. Raw cosines and projections are dominated by them. Every monitor score and steering vector must be computed on one scale (each dimension divided by its spread), with raw results reported alongside.
2. **Input type sets the direction.** Documents, UBS's lines read after the framed words, and UBS's whole-update average form three separate clusters. Within a cluster, cosines are 0.70–0.94; across clusters, 0.01–0.09 (unrelated directions fall within ±0.032). A monitor could learn "a UBS message is present" instead of "going along." Build and test the probe only on comparable moments (same input type), and keep the framing-only baseline.
3. **The emotion contrast does not carry across input types.** Loss minus gain in the documents against loss minus gain in UBS's lines: +0.08 (ceilings 0.91 and 0.95). Documents against financial documents: +0.55. So steering vectors should be built from decisions (holding minus going along), not from documents or framed lines.
4. **Token position matters.** UBS's direction read on the tokens after the framed words worked; the whole-update average did nothing. Record the token position for every state, and test both the last prompt token and the "after" construction as read points.

**Feature candidates.** STATE_MAP.md lists the layer-22 Gemma Scope 2 features most aligned with each direction. Use them as candidates for feature-level steering (design b). They name what each direction points along, not what fires.

## 6. Phase 1: Monitor (the trigger)

### Step 0: Inventory (report back before Step 1)

1. Confirm the state map in §5.1 and the three shift files it reads.
2. Find every saved transcript and decision moment across Experiments A to E.
3. Find any saved decision states at the read point (start with `trace.py`'s layer-24 output), with layers and token positions.
4. Find the outcome label for each request (trade-based) and, where it exists, the words label.
5. Report a table: experiment, condition, episodes, requests, requests that went along, states saved (yes/no).

If states were not saved at the read point, re-run forward passes on the saved prompts (in Colab, on a GPU) and extract states at layers 12, 18, 22, 24, 30 and 36. No sampling is needed.

### Step 1: Splits

**Split by episode, never by request.** Requests in one episode share history, so a request-level split leaks.

- **Split 1, within experiment.** Five-fold cross-validation grouped by episode, pooled across A to E.
- **Split 2, across experiments.** Build on some experiments and test on the others (for example, build on B, test on A, C, D, E).

**Rebuild the going-along direction inside every training fold.** The paper's direction was built on all data, so it cannot be tested on itself.

### Step 2: Monitors and baselines

| Monitor | What it uses |
|---|---|
| Difference-of-means probe | The going-along direction from the training fold |
| Logistic probe | L2-regularized logistic regression on the state |
| Framing-only baseline | Only which framing the request used |
| Words baseline | An LLM judge or keyword screen reading the reply text (acts after generation) |

**Controls:** 100 random directions of the same size; shuffled labels within the training fold.

**Scale:** compute every probe on one scale (§5.1, finding 1), and report raw results alongside.

### Step 3: Metrics (numbers and tables first)

- AUROC with 95% bootstrap intervals, resampling episodes.
- Catch rate and false-alarm rate at thresholds set on training folds only: (i) catching 80% of going-along requests; (ii) 10% false alarms.
- Flags per episode at each threshold.
- Per experiment and pooled.

### Step 4: Layer choice

Repeat at layers 12, 18, 22, 24, 30 and 36. Choose the layer on training folds only. Report the others as exploratory.

### Phase 1 success criteria (fix before looking at test results)

1. AUROC at least 0.75 for the difference-of-means probe;
2. beats the framing-only baseline;
3. beats every random direction;
4. matches or beats the words baseline.

## 7. Phase 2: Conditional steering (the point)

Run once the monitor passes, using its threshold as the trigger.

### Conditions (at the chosen layer, on flagged requests)

| Condition | Steering vector |
|---|---|
| None | No steering |
| Random | Random direction, same size |
| Contrastive | u ∝ holding − going along |
| Suppression only | u = −(going-along feature directions) |
| Promotion only | u = +(holding feature directions) |
| Unconditional | Contrastive vector on every request, flagged or not |

**Strengths:** 0.5×, 1× and 2× the natural size of the going-along gap.

### Measures

- Going along (trade measure, primary).
- Agreement in words.
- Readable actions (share of replies with a valid TARGET or HOLD).
- Market reasoning retained: share of reasoning that mentions price, position, stops or clients.
- **Off-target effects.** Features in superposition share directions, so steering one feature also moves others. Report the change in the most-affected non-target features' readings.
- **Persistence over the episode.** In whole episodes, does the correction hold, decay, or resurface later? This is the long-horizon question at the heart of the paper.

### Phase 2 success criteria (fix before running)

1. Contrastive steering lowers going along more than random steering;
2. readable actions drop by no more than 5 points;
3. market reasoning drops by no more than 10 points;
4. conditional steering does at least as well as unconditional steering, with less disruption.

## 8. Outputs

- `results/monitor_heldout/`: one CSV per experiment with request ID, episode, condition, labels, monitor scores per layer, fold.
- `results/conditional_steering/`: one CSV per condition and strength, with the Phase 2 measures.
- `summary.md`: tables first, then short notes.
- Figures: ROC curves per monitor; score distributions for went along vs. did not; going along by steering condition and strength.

## 9. Known risks

- **Damage from steering.** The paper's strong injections displaced market reasoning (credit state at 8× wrote "This is absolutely fantastic!" 75 times in 120 replies). Keep strengths low and track reasoning.
- **Random directions also moved behavior** in the paper. Every steering condition needs its random control.
- **Leakage.** Any direction built on test episodes invalidates the result.
- **Small numbers.** Going-along requests may be few per experiment. Intervals will be wide.
- **Label choice.** Keep the trade measure primary.
- **Transfer.** A monitor and steering vector built on one model and scenario may not carry over. Split 2 is the first check.

## 10. Open questions for the first Claude Code session

1. Does any saved file hold per-request decision states with going-along labels, or only the shift vectors in §5.1?
2. Where did `trace.py` save its layer-24 states?
3. How many going-along requests exist per experiment?
4. Is the words grading available beyond Experiment B?
5. Which compute should the re-extraction and Phase 2 runs use (A100 or H100)?

---

## Changes adopted (the author, 5 Nov; these take precedence over the text above)

1. **The decision states already exist.** Every career of A, B, C, D, E and F has its residual stream saved at all 48
   layers at the read point (the last token before the reply) at each push request, with the `joined` label and the
   reply (rd2-states `v2/<exp>_bf16`, written by `sim/inside_careers.py`). No re-extraction for read point 1.
2. **Keep the cross-fitting and the within-cell construction.** The paper's steering used a direction built on the other
   half of the careers (`sim/steer2.along_direction`), within each request, experiment and framing. Phase 1 keeps the
   within-cell construction and rebuilds it inside every training fold, split by career.
3. **A history-only baseline** ("went along at an earlier request in this career") alongside the framing-only one, and
   the AUROC at the 7 January request (no history yet) reported separately.
4. **The words baseline without the order line.** A judge that reads the order line nearly sees the answer.
5. **A second read point:** just before the order line, after the reasoning (still before the trade). Read point 1 is
   saved; read point 2 needs a forward pass on the saved replies (a GPU run, with its dollar estimate, after the user's
   yes).
6. **Feature-level steering from the decision states**, not from the document map: encode went-along vs did-not states
   with the dictionary and compare activations, at layer 24 (Neuronpedia labels).
7. **Smaller fixes:** count positives per experiment first and fix a minimum for Split 2; report results as levels
   (base row, then levels); drop the 120° toy model; compute is Modal H100s (CLAUDE.md updated).

Also (the author, 5 Nov): a preregistration note with the success criteria is committed before any test-fold AUROC is
computed (`designs/rd2/PREREG_MONITOR.md`), and the inventory is shown to the author before Step 1.

---

## Decisions, 5 Nov, after Phase 1 (agreed by the author with two reviewers; these take precedence over everything above)

Phase 1's result (`results/monitor_heldout/SUMMARY.md`): the difference-of-means monitor (M1) failed its criteria,
mostly because the request alone separates going along (51% on 7 January, 1% on 5 August); the logistic monitor (M2)
reached 0.927 pooled, 0.829 within request and 0.787 on 7 January.

**The two questions, kept apart.** Phase 1: does the state predict going along on held-out careers (prediction)?
Phase 2: does changing the state reduce going along without stopping legitimate trading (cause)?

**Keep**
- M2 is the monitor; the difference-of-means direction is the steering vector. A direction that predicts need not be
  one that causes, so the two roles are separate.
- Primary intervention: the steering vector added across UBS's request update and the reply (as the earlier steering run
  did; a single-token transplant at the decision token moved nothing, -0.2 to +0.3 points). Single-token steering is
  secondary.
- Phase 2 starts with single decision moments and paired seeds (the same seed with and without steering). Whole careers
  only afterwards.
- One table shape for every result: AUROC, caught, false alarms and precision at the threshold; pooled, within request,
  and each request with 7 January first. Pooled results alone can be the date.
- No paid GPU run without the author reviewing the exact command and its dollar estimate.

**Freeze and confirm**
- M2 is frozen (layer, strength, preprocessing, coefficients and trigger threshold) in a commit before any fresh careers
  run; the commit hash goes in NOTES. No separate preregistration document.
- The confirmation uses the frozen file unchanged, on unseen careers from Phase 2's no-steering arm.
- The held-out-request test and the prompt-only text baseline are exploratory (added after Phase 1 was read) and are
  labelled so (`results/monitor_heldout/EXPLORATORY.md`). They may run before the freeze; the freeze does not use them.

**Words.** No claim that the state monitor beats words. Reported as a descriptive finding: the blind chat labels show
agreement at 7% of the requests that went along (10% of those that did not).

**Steering controls (Phase 2).** Whether steering only adds HOLDs or suppresses legitimate trading: ordinary orders,
position sizes and P&L on days without a UBS request, and trades at requests that are not in UBS's direction. Success:
a greater reduction in going along per intervention than unconditional steering, or a comparable reduction with fewer
off-target effects.

**Deferred (left out as noise for now):** separate preregistration documents, AUPRC, a reasoning-reading words judge,
feature-level steering, the 120° toy model (§2's toy model and the "ε·cos θ" statement hold only for linear projections
of a feature's decoder direction, not for actual dictionary activations).

**6 Nov (the author).** The state-vs-text result is worded "beats a word-count text classifier" (the prompt-only
baseline: hashed words and word pairs, logistic regression). Open question: whether the state beats a stronger text
reader, such as a language model reading the same conversation. Phase 2's single moments include 12 January (the
frozen monitor flags 47% of those requests, against 75% at 7 January, so selectivity can show there), and every arm is
reported per request, 7 and 12 January separately.
