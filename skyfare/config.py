from dataclasses import dataclass, field
from typing import Dict, Any
import yaml
from pathlib import Path
from .logger import get_logger

log = get_logger(__name__)


@dataclass
class ModelConfig:
    name: str = "random_forest"
    random_forest: Dict[str, Any] = field(default_factory=dict)
    grad_boost: Dict[str, Any] = field(default_factory=dict)
    xgboost: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PreprocessingConfig:
    drop_columns: list = field(default_factory=list)
    fill_values: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AppConfig:
    random_state: int = 42
    test_size: float = 0.15
    val_size: float = 0.15
    model: ModelConfig = field(default_factory=ModelConfig)
    preprocessing: PreprocessingConfig = field(default_factory=PreprocessingConfig)


def load_config(path: str) -> AppConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    model_cfg = ModelConfig(**raw.get("model", {}))
    pre_cfg = PreprocessingConfig(**raw.get("preprocessing", {}))
    cfg = AppConfig(
        random_state=raw.get("random_state", 42),
        test_size=raw.get("test_size", 0.15),
        val_size=raw.get("val_size", 0.15),
        model=model_cfg,
        preprocessing=pre_cfg,
    )
    log.info(f"Loaded config from {path}")
    return cfg
