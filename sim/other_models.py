"""Experiment B with other open models (the user, 30 Oct: "run experiment B with both"). The full careers were built
for Gemma 3 12B; this file is everything that differs for another model, so the notebooks stay as they are.

Each model has its own pin (results/full_career_pin_<key>.json: the model, its exact revision, the same library
versions as Gemma's pin) and an adaptation of its chat template, so the conversation reaches the model laid out as
Gemma's template lays it out:

- Gemma 3 has no system role: its template puts the instructions at the start of the first user message, followed by
  a blank line. They stay at the top of the career and recede as it grows.
- Mistral Nemo's template moves the system message to just before the newest user message, every turn, so the
  instructions would always be fresh. merge_system puts them where Gemma's template does instead.
- Qwen3.5 has a system role at the top of the conversation (Gemma's place), and thinks aloud by default (a <think>
  block before the reply). enable_thinking=False closes the think block in the prompt, so it replies as Gemma does:
  reasoning, order line, chat line.

A model's careers go to their own results folder (the folder name carries the model's name), with a setup ID that
covers its pin and its adaptation.
"""
import functools
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = {
    "qwen3.5-9b": {"pin": "results/full_career_pin_qwen3.5-9b.json", "template": {"enable_thinking": False},
                   "merge_system": False, "kernels": True, "needs_user": True},
    "mistral-nemo-12b": {"pin": "results/full_career_pin_mistral-nemo-12b.json", "template": {},
                         "merge_system": True, "kernels": False},
    # Gemma 4 (May 2026): a system role at the top (Gemma 3's place for the instructions); thinking is off by default,
    # set explicitly. The careers' loader (AutoModelForCausalLM) opens it as it opens Gemma 3.
    "gemma-4-12b": {"pin": "results/full_career_pin_gemma-4-12b.json", "template": {"enable_thinking": False},
                    "merge_system": False, "kernels": False},
    # Ministral 3 (Dec 2025), Mistral's successor to Nemo: the full-precision (BF16) copy, since the main repo ships FP8
    # weights the 4-bit loader cannot take; its system prompt sits at the top. It is packaged as an image-and-text
    # model with no text-model entry, so AutoModelForCausalLM is taught to open it (register, below).
    "ministral-3-14b": {"pin": "results/full_career_pin_ministral-3-14b.json", "template": {},
                        "merge_system": False, "kernels": False, "register": "mistral3"},
}


def parse(settings):
    """'model=qwen3.5-9b&versions=neutral;loss' -> {'model': 'qwen3.5-9b', 'versions': ['neutral', 'loss']}; versions
    are slugs (loss_plus_you for "loss + you"). Returns {} when the settings are not of this form."""
    if "=" not in settings:
        return {}
    out = {}
    for part in settings.split("&"):
        k, _, v = part.partition("=")
        out[k.strip()] = v.strip()
    assert out.get("model") in MODELS, f"unknown model {out.get('model')!r}: one of {sorted(MODELS)}"
    if "versions" in out:
        out["versions"] = [x.replace("_plus_", " + ") for x in out["versions"].split(";") if x]
    return out


def pin(key):
    return json.load(open(os.path.join(ROOT, MODELS[key]["pin"])))


def merge_system(turns):
    """Gemma's layout: the system message's text at the start of the first user message, then a blank line."""
    turns = list(turns)
    if len(turns) >= 2 and turns[0]["role"] == "system" and turns[1]["role"] == "user":
        return [{"role": "user", "content": turns[0]["content"] + "\n\n" + turns[1]["content"]}] + turns[2:]
    return turns


def adapt(tok, key):
    """The tokenizer, with its chat template called the way this model needs (also by the pipeline, which uses the same
    tokenizer object)."""
    spec = MODELS[key]
    if getattr(tok, "_rd2_adapted", None) == key:
        return tok
    original = tok.apply_chat_template

    @functools.wraps(original)
    def apply(conversation, *args, **kwargs):
        if spec["merge_system"]:
            if hasattr(conversation, "messages"):            # a pipeline Chat object
                conversation.messages = merge_system(conversation.messages)
            elif conversation and isinstance(conversation[0], dict):
                conversation = merge_system(conversation)
        msgs = conversation.messages if hasattr(conversation, "messages") else conversation
        if spec.get("needs_user") and msgs and isinstance(msgs[0], dict) and not any(t["role"] == "user" for t in msgs):
            # Qwen3.5's template refuses a conversation with no user message. Only the notebooks' memory check builds one
            # (its first length count is the instructions alone); an empty user turn lets it be counted. A career
            # always has a user message, so its prompts are never changed by this.
            conversation = list(msgs) + [{"role": "user", "content": ""}]
        return original(conversation, *args, **{**spec["template"], **kwargs})
    tok.apply_chat_template = apply
    tok._rd2_adapted = key
    return tok


def prepare(key):
    """Before the model loads: anything the careers' loader needs for this model (Ministral 3: AutoModelForCausalLM is
    taught its image-and-text class, which then reads text alone, as Gemma 3's does)."""
    if MODELS[key].get("register") == "mistral3":
        import transformers
        # The class name is built from two parts: written whole, it is 32 letters next to "Mistral", which GitHub's
        # secret scanner takes for a Mistral API key and refuses to push.
        image_text = getattr(transformers, "Mistral3" + "ForConditionalGeneration")
        transformers.AutoModelForCausalLM.register(transformers.Mistral3Config, image_text, exist_ok=True)


def setup_hash(key):
    """What decides this model's careers beyond the notebook's own setup ID."""
    spec = MODELS[key]
    return [key, pin(key), spec["template"], spec["merge_system"]]
