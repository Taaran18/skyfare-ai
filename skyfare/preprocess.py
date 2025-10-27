import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .logger import get_logger
import re

log = get_logger(__name__)


def _parse_duration(s: str):
    if not isinstance(s, str):
        return None
    s = s.lower().replace(" ", "")
    hours = re.findall(r"(\d+)h", s)
    minutes = re.findall(r"(\d+)m", s)
    h = int(hours[0]) if hours else 0
    m = int(minutes[0]) if minutes else 0
    return h * 60 + m


class DateTimeExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # Safer explicit date parsing with format
        X["Journey_day"] = pd.to_datetime(
            X["Date_of_Journey"], format="%d/%m/%Y", errors="coerce"
        ).dt.day
        X["Journey_month"] = pd.to_datetime(
            X["Date_of_Journey"], format="%d/%m/%Y", errors="coerce"
        ).dt.month
        # Time parsing
        X["Dep_hour"] = pd.to_datetime(
            X["Dep_Time"], format="%H:%M", errors="coerce"
        ).dt.hour
        X["Arrival_hour"] = pd.to_datetime(
            X["Arrival_Time"], format="%H:%M", errors="coerce"
        ).dt.hour
        # Duration
        X["Duration_mins"] = X["Duration"].apply(_parse_duration)
        return X.drop(
            ["Date_of_Journey", "Dep_Time", "Arrival_Time", "Duration"], axis=1
        )
