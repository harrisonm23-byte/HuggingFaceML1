import pytest

from hfml.config import ExperimentConfig, load_config, save_config


def test_defaults():
    cfg = load_config()
    assert isinstance(cfg, ExperimentConfig)
    assert cfg.model.num_labels == 2


def test_rd1_configs_load():
    for name in ("baseline", "smoke"):
        cfg = load_config(f"designs/rd1/configs/{name}.yaml")
        assert cfg.name == f"rd1-{name}"


def test_overrides_parse_types():
    cfg = load_config(
        "designs/rd1/configs/baseline.yaml",
        ["train.learning_rate=3e-5", "train.fp16=true", "data.max_train_samples=10", "seed=7"],
    )
    assert cfg.train.learning_rate == pytest.approx(3e-5)
    assert cfg.train.fp16 is True
    assert cfg.data.max_train_samples == 10
    assert cfg.seed == 7


def test_unknown_key_rejected():
    with pytest.raises(KeyError):
        load_config(overrides=["train.lr=1e-3"])


def test_round_trip(tmp_path):
    cfg = load_config("designs/rd1/configs/smoke.yaml")
    save_config(cfg, tmp_path / "c.yaml")
    assert load_config(tmp_path / "c.yaml") == cfg
