import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from .logger import get_logger

log = get_logger(__name__)


class FeatureEngineer:
    """
    Automatically encodes categorical and scales numerical columns.
    """

    def __init__(self):
        self.ct = None
        self.cat_cols = []
        self.num_cols = []

    def fit(self, X, y=None):  # <-- add y=None here
        X = X.copy()
        self.cat_cols = [c for c in X.columns if X[c].dtype == "object"]
        self.num_cols = [c for c in X.columns if c not in self.cat_cols]

        cat_tf = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        num_tf = StandardScaler()

        self.ct = ColumnTransformer(
            [("cat", cat_tf, self.cat_cols), ("num", num_tf, self.num_cols)]
        )
        self.ct.fit(X, y)
        log.info(
            f"Fitted with {len(self.cat_cols)} categorical and {len(self.num_cols)} numerical columns."
        )
        return self

    def transform(self, X):
        return self.ct.transform(X)
