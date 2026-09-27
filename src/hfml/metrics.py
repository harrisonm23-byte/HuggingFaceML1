"""Metrics passed to the Hugging Face Trainer."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def classification_metrics(eval_pred) -> dict:
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1_macro": f1_score(labels, preds, average="macro"),
    }
