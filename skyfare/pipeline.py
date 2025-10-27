from __future__ import annotations
from pathlib import Path
import pandas as pd
from .logger import get_logger
from .config import load_config
from .data_loader import DataLoader
from .model import SkyFareRegressor
from .utils import save_joblib, load_joblib

log = get_logger(__name__)


# ============================================================
# TRAINING PIPELINE
# ============================================================
class TrainPipeline:
    def __init__(self, config_path: str):
        self.cfg = load_config(config_path)

    def run(
        self, data_path: str, artifact_path: str = "artifacts/skyfare_model.joblib"
    ):
        log.info(f"🔧 TrainingPipeline started for {data_path}")
        df = DataLoader(data_path).load()

        reg = SkyFareRegressor(
            model_name=self.cfg.model.name,
            params=getattr(self.cfg.model, self.cfg.model.name, {}),
            random_state=self.cfg.random_state,
        )

        metrics = reg.fit(df)
        save_joblib(reg.pipeline, artifact_path)
        log.info(f"✅ Model artifact saved to {artifact_path}")
        return metrics


# ============================================================
# PREDICTION PIPELINE
# ============================================================
class PredictPipeline:
    def __init__(self, artifact_path: str):
        self.artifact_path = artifact_path
        self.pipeline = load_joblib(artifact_path)

    def run(self, input_path: str, output_path: str | None = None):
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Detect Excel or CSV
        ext = path.suffix.lower()
        if ext in [".csv"]:
            df = pd.read_csv(path, encoding="utf-8", errors="ignore")
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        log.info(f"Loaded inference data: {df.shape[0]} rows × {df.shape[1]} columns")

        preds = self.pipeline.predict(df)
        df["Predicted_Price"] = preds

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.suffix.lower() in [".xlsx", ".xls"]:
                df.to_excel(out, index=False)
            else:
                df.to_csv(out, index=False)
            log.info(f"Predictions saved to {out}")

        return df
