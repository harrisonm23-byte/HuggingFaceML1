"""Fine-tune a model from a YAML config.

Usage:
    python -m hfml.train --config designs/rd1/configs/baseline.yaml
    python -m hfml.train --config designs/rd1/configs/baseline.yaml train.learning_rate=3e-5
"""

from __future__ import annotations

import argparse

from dotenv import load_dotenv
from transformers import DataCollatorWithPadding, Trainer, TrainingArguments

from hfml.config import load_config, save_config
from hfml.data import load_splits, tokenize_splits
from hfml.metrics import classification_metrics
from hfml.models import load_model_and_tokenizer
from hfml.utils import make_run_dir, set_seed, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", required=True, help="Path to experiment YAML")
    parser.add_argument("overrides", nargs="*", help="Dotted overrides, e.g. train.epochs=1")
    args = parser.parse_args()

    load_dotenv()
    cfg = load_config(args.config, args.overrides)
    set_seed(cfg.seed)
    run_dir = make_run_dir(cfg.train.output_dir, cfg.name)
    save_config(cfg, run_dir / "config.yaml")
    print(f"Run directory: {run_dir}")

    model, tokenizer = load_model_and_tokenizer(cfg.model)
    splits = tokenize_splits(load_splits(cfg.data, cfg.seed), tokenizer, cfg.data)

    t = cfg.train
    training_args = TrainingArguments(
        output_dir=str(run_dir / "checkpoints"),
        num_train_epochs=t.epochs,
        learning_rate=t.learning_rate,
        per_device_train_batch_size=t.batch_size,
        per_device_eval_batch_size=t.eval_batch_size,
        weight_decay=t.weight_decay,
        warmup_steps=float(t.warmup_ratio),  # a float in [0, 1) is a ratio of total steps
        fp16=t.fp16,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        logging_steps=50,
        report_to=t.report_to,
        run_name=f"{cfg.name}-{run_dir.name}",
        seed=cfg.seed,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=splits["train"],
        eval_dataset=splits["eval"],
        processing_class=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=classification_metrics,
    )
    trainer.train()
    metrics = trainer.evaluate()
    write_json(metrics, run_dir / "metrics.json")
    trainer.save_model(str(run_dir / "model"))
    print(metrics)


if __name__ == "__main__":
    main()
