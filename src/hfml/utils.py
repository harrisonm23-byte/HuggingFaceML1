"""Reproducibility and run-directory helpers."""

from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path

import numpy as np


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def make_run_dir(output_dir: str, name: str) -> Path:
    """Create outputs/<name>/<timestamp>/ so runs never overwrite each other."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(output_dir) / name / stamp
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_json(data: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, indent=2, default=float))
