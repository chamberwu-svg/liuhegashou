from __future__ import annotations

import pickle
from typing import Dict, List

from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


class XGBoostPredictor:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = XGBClassifier(
            n_estimators=30,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.8,
            random_state=random_state,
            eval_metric='mlogloss',
        )
        self.encoder = LabelEncoder()
        self.is_trained = False

    def train(self, X: List[List[float]], y: List[int]):
        self.model = XGBClassifier(
            n_estimators=30,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.8,
            random_state=self.random_state,
            eval_metric='mlogloss',
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
        prob_map = {int(cls): float(val) for cls, val in zip(self.encoder.classes_, proba)}
        result = {num: prob_map.get(num, 0.0) for num in range(1, 50)}
        total = sum(result.values())
        if total > 0:
            return {num: val / total for num, val in result.items()}
        return {num: 1.0 / 49.0 for num in range(1, 50)}

    def walk_forward_validate(self, X: List[List[float]], y: List[int], step: int = 500):
        results = []
        for train_end in range(step, len(X) - 1):
            X_train, X_test = X[:train_end], X[train_end]
            y_train, y_test = y[:train_end], y[train_end]
            encoder = LabelEncoder()
            y_train_enc = encoder.fit_transform(y_train)
            model = XGBClassifier(
                n_estimators=30,
                max_depth=4,
                learning_rate=0.05,
                random_state=42,
                eval_metric='mlogloss',
            )
            model.fit(X_train, y_train_enc)
            y_pred = model.predict_proba(X_test.reshape(1, -1))[0]
            pred_idx = y_pred.argmax()
            pred_cls = int(encoder.classes_[pred_idx]) if pred_idx < len(encoder.classes_) else 1
            results.append({"actual": int(y_test), "probability": float(max(y_pred)), "predicted": pred_cls})
        return results

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


