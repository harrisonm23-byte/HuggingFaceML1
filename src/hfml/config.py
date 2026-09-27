"""Experiment configuration: YAML files + dotted command-line overrides."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from pathlib import Path

import yaml


@dataclass
class ModelConfig:
    name: str = "distilbert-base-uncased"
    num_labels: int = 2


@dataclass
class DataConfig:
    dataset: str = "stanfordnlp/imdb"
    subset: str | None = None
    text_column: str = "text"
    label_column: str = "label"
    train_split: str = "train"
    eval_split: str = "test"
    max_length: int = 256
    # Cap sample counts for quick iteration; None means use the full split.
    max_train_samples: int | None = None
    max_eval_samples: int | None = None


@dataclass
class TrainConfig:
    output_dir: str = "outputs"
    epochs: float = 3.0
    learning_rate: float = 2e-5
    batch_size: int = 16
    eval_batch_size: int = 32
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    fp16: bool = False
    report_to: str = "none"  # "wandb", "tensorboard", ...


@dataclass
class ExperimentConfig:
    name: str = "experiment"
    seed: int = 42
    model: ModelConfig = field(default_factory=ModelConfig)
    data: DataConfig = field(default_factory=DataConfig)
    train: TrainConfig = field(default_factory=TrainConfig)

    def to_dict(self) -> dict:
        return asdict(self)


def _build(cls, values: dict):
    known = {f.name: f for f in fields(cls)}
    unknown = set(values) - set(known)
    if unknown:
        raise KeyError(f"Unknown keys for {cls.__name__}: {sorted(unknown)}")
    kwargs = {}
    for key, value in values.items():
        default = getattr(cls(), key)
        if is_dataclass(default):
            value = _build(type(default), value)
        elif isinstance(value, str) and type(default) in (int, float):
            # YAML reads "3e-5" (no decimal point) as a string; coerce numeric fields.
            value = type(default)(float(value))
        kwargs[key] = value
    return cls(**kwargs)


def _apply_override(raw: dict, override: str) -> None:
    """Apply a `section.key=value` override; value is parsed as YAML (numbers, bools, null)."""
    if "=" not in override:
        raise ValueError(f"Override must look like key=value, got {override!r}")
    path, value = override.split("=", 1)
    *parents, leaf = path.split(".")
    node = raw
    for part in parents:
        node = node.setdefault(part, {})
    node[leaf] = yaml.safe_load(value)


def load_config(path: str | Path | None = None, overrides: list[str] | None = None) -> ExperimentConfig:
    raw = {}
    if path is not None:
        raw = yaml.safe_load(Path(path).read_text()) or {}
    for override in overrides or []:
        _apply_override(raw, override)
    return _build(ExperimentConfig, raw)


def save_config(config: ExperimentConfig, path: str | Path) -> None:
    Path(path).write_text(yaml.safe_dump(config.to_dict(), sort_keys=False))
