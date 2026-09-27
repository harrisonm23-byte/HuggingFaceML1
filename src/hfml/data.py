"""Dataset loading and tokenization."""

from __future__ import annotations

from datasets import DatasetDict, load_dataset

from hfml.config import DataConfig


def load_splits(cfg: DataConfig, seed: int) -> DatasetDict:
    ds = load_dataset(cfg.dataset, cfg.subset)
    splits = DatasetDict(train=ds[cfg.train_split], eval=ds[cfg.eval_split])
    for split, cap in (("train", cfg.max_train_samples), ("eval", cfg.max_eval_samples)):
        if cap is not None and cap < len(splits[split]):
            splits[split] = splits[split].shuffle(seed=seed).select(range(cap))
    return splits


def tokenize_splits(splits: DatasetDict, tokenizer, cfg: DataConfig) -> DatasetDict:
    def tokenize(batch):
        return tokenizer(batch[cfg.text_column], truncation=True, max_length=cfg.max_length)

    tokenized = splits.map(tokenize, batched=True)
    if cfg.label_column != "labels":
        tokenized = tokenized.rename_column(cfg.label_column, "labels")
    keep = {"input_ids", "attention_mask", "token_type_ids", "labels"}
    return tokenized.remove_columns([c for c in tokenized["train"].column_names if c not in keep])
