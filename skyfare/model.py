import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from .features import FeatureEngineer
from .preprocess import DateTimeExtractor
from .logger import get_logger

log = get_logger(__name__)


class SkyFareRegressor:
    def __init__(self, model_name="random_forest", params=None, random_state=42):
        self.model_name = model_name
        self.params = params or {}
        self.random_state = random_state
        self.pipeline = None

    def _get_model(self):
        if self.model_name == "random_forest":
            return RandomForestRegressor(**self.params)
        if self.model_name == "grad_boost":
            return GradientBoostingRegressor(**self.params)
        raise ValueError(f"Unknown model: {self.model_name}")

    def fit(self, df, target="Price"):
        X = df.drop(columns=[target])
        y = df[target]
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state
        )

        pre = DateTimeExtractor()
        fe = FeatureEngineer()
        model = self._get_model()

        self.pipeline = Pipeline([("pre", pre), ("fe", fe), ("model", model)])

        self.pipeline.fit(X_train, y_train)
        preds = self.pipeline.predict(X_val)

        metrics = {
            "MAE": mean_absolute_error(y_val, preds),
            "RMSE": np.sqrt(mean_squared_error(y_val, preds)),
            "R2": r2_score(y_val, preds),
        }
        log.info(f"Validation metrics: {metrics}")
        return metrics

    def predict(self, df):
        return self.pipeline.predict(df)
