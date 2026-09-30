# HuggingFaceML1

Behavioral evaluations and interpretability research on pretrained open models (Gemma + Gemma Scope).
Nothing is trained: we run pretrained models, read their internal features with sparse autoencoders (SAEs),
and turn features up or down to see what changes. Experiments run in **Google Colab** on a GPU.

**Start here:** [`designs/rd2/OVERVIEW.md`](designs/rd2/OVERVIEW.md), the main design: a framing push followed over a long agent task.
**Its single-decision pilot:** [`designs/rd1/OVERVIEW.md`](designs/rd1/OVERVIEW.md), the "You" attention question.

## Layout

```
designs/
  rd1/            The "You" attention question: single-decision study (formerly RD1)
    OVERVIEW.md   start here: one-page summary to share
    PART1_*.md, PART2_*.md   the core experiments
    DESIGN.md     question, hypotheses, models, experiment plan
    NOTES.md      dated lab notebook
    E*_*.md       exploratory side experiments
  rd2/            The main design: the push at the top of a long agent run
    OVERVIEW.md
    NOTES.md
notebooks/        Colab notebooks, numbered in run order
```

## Getting started (Colab)

1. Open `notebooks/01_gemma_hello.ipynb` in Colab: *File → Open notebook → GitHub*, then paste this repo's URL.
2. *Runtime → Change runtime type →* **T4 GPU**.
3. Accept the Gemma licence at https://huggingface.co/google/gemma-3-1b-it.
4. Add your Hugging Face token under **Secrets** (key icon) as `HF_TOKEN`, with notebook access on.
5. *Runtime → Run all*. When the model answers "Paris", setup is done.
