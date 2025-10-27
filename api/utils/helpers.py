from datetime import datetime, timedelta
from pathlib import Path
import joblib

MODEL_PATH = Path("artifacts/skyfare_model_compressed.joblib.gz")


def load_model():
    """Load trained model artifact."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Please train using main.py first.")
    return joblib.load(MODEL_PATH)


def compute_duration(dep_time: str, arr_time: str) -> str:
    """Compute duration like '2h 45m', handles overnight flights."""
    fmt = "%H:%M"
    dep = datetime.strptime(dep_time, fmt)
    arr = datetime.strptime(arr_time, fmt)
    if arr < dep:
        arr += timedelta(days=1)
    diff = arr - dep
    hours, remainder = divmod(diff.seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m"
