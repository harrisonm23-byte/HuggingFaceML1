# Part 2 (core): Tracing "you" through the model, gain vs. loss

**Notebook:** [`notebooks/04_tracing_you.ipynb`](../../notebooks/04_tracing_you.ipynb)
**Model:** `google/gemma-3-4b-it` (34 layers; main target) or `google/gemma-3-1b-it` (26 layers), with Gemma Scope 2 SAEs
**Status:** Ready to run (about 5 minutes on 1B; longer on 4B, mostly for patching)
**Hypothesis:** H-core-mechanism (see [`DESIGN.md`](DESIGN.md))
*(Formerly "E3".)*

## Question
**When "you" is attached to a loss statement versus a gain statement, how does attention on "you" differ? Tracing that through the forward pass, what gets activated, and does it drive the change in the decision?**

Part 1 asks *whether* ownership ("…down to **you**" vs. "…down to **us**") changes how strongly framing moves the decision. Part 2 asks *how*. It uses **the same 96 prompts**, and every measure is averaged over all 24 matched sets, not one example.

## Core concept
In a transformer, each word builds its meaning by **attending** to earlier words. The prompts put "you"/"us" **last** in the manager's message ("If this quarter is weak, we lose $5 million and 40 people lose their jobs, and that is down to **you**."), so by the middle layers that word can have absorbed the entire loss or gain statement: the stakes, the jobs, the bonuses.

*(An earlier version traced the "you" in "it's on you: **you**'ll cost us…". That "you" came before "cost", "$5 million" and "jobs", so it couldn't see them. Putting the owner word last fixes this.)*

We follow attention in both directions:

| Direction | Question | What it shows |
|---|---|---|
| **Into "you"** (statement → "you") | How much of "you"'s attention comes from the loss or gain statement, and at which layers? | How the framing gets *into* "you" |
| **Onto "you"** ("you" → decision) | How much does the decision point (where the model answers YES/NO) look back at "you"? | How "you" gets *used* |

"Us" is the comparison throughout: same position, same statement, different owner.

## Methods
All are averaged over the 24 matched sets.

0. **Decision.** P(buy) in each of the four cells, and the interaction, as in Part 1.
1. **Attention into "you":** the words the traced word attends to most (for one example), then the share of its attention coming from the statement before it, at every layer, for loss/you, gain/you, loss/us and gain/us. The first token (`<bos>`) is left out because it absorbs attention as a "rest position".
2. **Attention onto "you":** at every layer, the share of the decision point's attention that goes to the traced word.
3. **Tracing through the forward pass:** at each layer, the cosine similarity between the loss and gain versions of the traced word (1.00 = identical), for "you" and for "us". At layer 0 they're the same word; where similarity drops is where the framing enters.
4. **Activation patching:** run the gain prompt, but at one layer swap in the traced word's vector from the loss prompt, and report the **share of the loss−gain gap** that this recovers, for "you" and for "us".
5. **Attention knockout** (the most direct test): block attention at every layer, recompute all 96 P(buy) values and the interaction.
   - **Cut into "you":** the traced word can't look at the statement, so it never absorbs the framing.
   - **Cut onto "you":** nothing after the traced word can look at it, so the decision can't read it.
   - The same cut is applied to "us".
6. **Mixed-frame contest:** the manager states **both** the loss and the gain, pinning one on "you" and the other on "us", in both orders. Which frame wins?
7. **Gemma Scope 2 features:** for every SAE feature on the traced word, the feature's own interaction, (loss − gain on "you") − (loss − gain on "us"), with Neuronpedia links for the top features in each direction.
   - SAEs: `sae_lens` release `gemma-scope-2-1b-it-res` (layers 7, 13, 17, 22) or `gemma-scope-2-4b-it-res` (layers 9, 17, 22, 29), width 16k, L0 medium.
   - Neuronpedia: `https://www.neuronpedia.org/<model>/<layer>-gemmascope-2-res-16k/<feature>`.

## How to read the results
| Result | Interpretation |
|---|---|
| "You" draws more from a loss statement than a gain statement (vs. "us") | Framing flows into "you" asymmetrically |
| Similarity drops at some layer, more for "you" than "us" | That's where "you" absorbs the framing, and it absorbs more of it than "us" |
| The decision attends to "you" more after loss than gain | The decision reads "you" differently depending on the framing |
| Patching recovers a large share of the gap for "you" | The "you" vector carries framing information the decision uses |
| **Knockout shrinks the interaction toward 0** | **That path carries the amplification.** This is the strongest evidence |
| Knockout barely changes the interaction | Framing reaches the decision by other routes; "you" isn't the channel |
| Contest: P(buy) higher when "you" owns the loss, in both orders | Ownership decides which frame dominates |
| Features with a large interaction and clear Neuronpedia examples | Candidates for steering |

## Caveats
- **Attention isn't causation.** Patching and knockout are the causal tests.
- **Knockouts can disturb the model generally.** Compare the interaction, not the raw P(buy) levels.
- **A small gap means unstable patching shares.** If Part 1 finds almost no loss−gain gap, patching shares are unstable; record that.
- **Token alignment.** Loss and gain versions are word-matched but may differ by a token. The notebook reports how many pairs line up exactly, and patching works either way.
- **Neuronpedia labels are automated guesses.** Read the example texts.
- **The last layer's similarity** is after the final normalization step, so it's on a slightly different scale.

## Results
_To fill in after running._

| Date | Model | Interaction | Into "you": peak layer and share (loss/you vs. gain/you vs. us) | Onto "you": peak layer and share | Divergence layer | Patching: best layer (you / us) | Knockout interaction (into / onto) | Contest | Notable features |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Next
- **Steering:** turn down a feature that tracks blame or desperation on "you", rerun Part 1, and see whether the amplification disappears (RD1's suppression question).
