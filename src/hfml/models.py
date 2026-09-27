"""Model and tokenizer loading from the Hugging Face Hub (or a local checkpoint)."""

from __future__ import annotations

from transformers import AutoModelForSequenceClassification, AutoTokenizer

from hfml.config import ModelConfig


def load_model_and_tokenizer(cfg: ModelConfig):
    tokenizer = AutoTokenizer.from_pretrained(cfg.name)
    model = AutoModelForSequenceClassification.from_pretrained(cfg.name, num_labels=cfg.num_labels)
    return model, tokenizer
