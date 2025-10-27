import os
from pathlib import Path
import pandas as pd
from skyfare.pipeline import TrainPipeline, PredictPipeline
from skyfare.logger import get_logger

# ============================================================
# CONFIGURATION
# ============================================================
CONFIG_PATH = "config/default_config.yaml"
TRAIN_FILE = "data/train.xlsx"
TEST_FILE = "data/test.xlsx"
ARTIFACT_PATH = "artifacts/skyfare_model.joblib"
PRED_OUTPUT = "artifacts/predictions.xlsx"

log = get_logger("main")


# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def ensure_directories():
    """Ensure required directories exist."""
    Path("data").mkdir(exist_ok=True)
    Path("artifacts").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)


def check_files():
    """Check that training and test files exist."""
    if not Path(TRAIN_FILE).exists():
        raise FileNotFoundError(f"Training file not found: {TRAIN_FILE}")
    if not Path(TEST_FILE).exists():
        log.warning(f"Test file not found ({TEST_FILE}). Predictions will be skipped.")
        return False
    return True


# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    log.info("🚀 Starting SkyFareAI — End-to-End Flight Price Prediction")

    ensure_directories()
    has_test = check_files()

    # 1️⃣ TRAINING PHASE
    log.info("📦 Loading training pipeline configuration...")
    trainer = TrainPipeline(CONFIG_PATH)

    log.info("🧠 Training model using training data...")
    metrics = trainer.run(TRAIN_FILE, ARTIFACT_PATH)
    log.info("✅ Model training complete!")
    log.info(f"📊 Validation & Test Metrics: {metrics}")

    # 2️⃣ PREDICTION PHASE
    if has_test:
        log.info("📄 Loading trained model artifact for prediction...")
        predictor = PredictPipeline(ARTIFACT_PATH)

        log.info(f"🔮 Predicting flight prices for {TEST_FILE}...")
        preds_df = predictor.run(TEST_FILE)

        # Save as Excel
        preds_df.to_excel(PRED_OUTPUT, index=False)
        log.info(f"✅ Predictions saved successfully to: {PRED_OUTPUT}")

        print("\n=========== SAMPLE PREDICTIONS ===========")
        print(preds_df.head())
        print("==========================================\n")

    else:
        log.warning("⚠️ Skipping prediction: test.xlsx not found.")

    log.info("🏁 SkyFareAI pipeline finished successfully!")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
