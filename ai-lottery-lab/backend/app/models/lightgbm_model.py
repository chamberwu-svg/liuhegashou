from __future__ import annotations

import pickle
from typing import Dict, List

from sklearn.preprocessing import LabelEncoder
from lightgbm import LGBMClassifier


class LightGBMPredictor:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = LGBMClassifier(
            n_estimators=30,
            learning_rate=0.05,
            max_depth=-1,
            num_leaves=31,
            random_state=random_state,
            objective='multiclass',
            verbosity=-1,
        )
        self.encoder = LabelEncoder()
        self.is_trained = False

    def train(self, X: List[List[float]], y: List[int]):
        self.model = LGBMClassifier(
            n_estimators=30,
            learning_rate=0.05,
            max_depth=-1,
            num_leaves=31,
            random_state=self.random_state,
            objective='multiclass',
            verbosity=-1,
        )
        self.encoder = LabelEncoder()
        y_encoded = self.encoder.fit_transform(y)
        self.model.fit(X, y_encoded)
        self.is_trained = True
        return self

    def predict_proba(self, X: List[List[float]]) -> List[List[float]]:
        if not self.is_trained:
            raise ValueError("model must be trained before prediction")
        return self.model.predict_proba(X)

    def predict(self, X: List[List[float]]) -> Dict[int, float]:
        if not self.is_trained:
            raise ValueError("model must be trained before prediction")
        proba = self.model.predict_proba(X)[0]
        prob_map = {int(cls): float(prob) for cls, prob in zip(self.encoder.classes_, proba)}
        result = {num: prob_map.get(num, 0.0) for num in range(1, 50)}
        total = sum(result.values())
        if total > 0:
            return {num: val / total for num, val in result.items()}
        return {num: 1.0 / 49.0 for num in range(1, 50)}

    def save(self, path: str):
        with open(path, "wb") as fh:
            pickle.dump({"model": self.model, "encoder": self.encoder}, fh)

    def load(self, path: str):
        with open(path, "rb") as fh:
            data = pickle.load(fh)
            self.model = data["model"]
            self.encoder = data["encoder"]
        self.is_trained = True
        return self


