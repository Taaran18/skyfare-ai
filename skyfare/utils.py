import joblib
from pathlib import Path


def save_joblib(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)


def load_joblib(path):
    return joblib.load(path)
