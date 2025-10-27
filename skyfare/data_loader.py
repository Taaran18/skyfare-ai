import pandas as pd
from pathlib import Path
from .logger import get_logger

log = get_logger(__name__)


class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def load(self) -> pd.DataFrame:
        log.info(f"Loading data from: {self.file_path}")
        ext = self.file_path.suffix.lower()

        if ext in [".csv"]:
            df = pd.read_csv(self.file_path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        log.info(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns.")
        return df
