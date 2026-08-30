from __future__ import annotations

from typing import Dict, List, Any

from app.feature.engineering import build_tabular_dataset, extract_draw_features
from app.models.bayesian import BayesianPredictor
from app.models.markov import MarkovPredictor
from app.models.random_forest import RandomForestPredictor
from app.models.xgboost_model import XGBoostPredictor
from app.models.lightgbm_model import LightGBMPredictor
from app.models.lstm import LSTMPredictor
from app.ensemble.fusion import fuse_scores
from app.ensemble.consensus import calculate_consensus


class PredictionPipeline:
    def __init__(self, history: List[int], models_to_run: List[str] | None = None):
        self.history = history
        self.models_to_run = models_to_run or ["markov", "bayes", "rf", "xgb", "lgb", "lstm"]

    def run(self) -> List[Dict[str, Any]]:
        scores: Dict[str, Dict[int, float]] = {}

        if "markov" in self.models_to_run and len(self.history) > 1:
            try:
                markov = MarkovPredictor(order=1).train(self.history)
                scores["markov"] = markov.predict(self.history)
            except Exception:
                pass

        if "bayes" in self.models_to_run and self.history:
            try:
                bayes = BayesianPredictor().train(self.history)
                scores["bayes"] = bayes.predict()
            except Exception:
                pass

        # Prepare tabular features for ML models
        need_ml = any(m in self.models_to_run for m in ["rf", "xgb", "lgb"])
        if need_ml and len(self.history) >= 10:
            try:
                X_train, y_train = build_tabular_dataset(self.history, min_history=5)
                x_current = extract_draw_features(self.history)
                if X_train and y_train:
                    if "rf" in self.models_to_run:
                        rf = RandomForestPredictor(n_estimators=50).train(X_train, y_train)
                        scores["rf"] = rf.predict([x_current])
                    if "xgb" in self.models_to_run:
                        xgb = XGBoostPredictor().train(X_train, y_train)
                        scores["xgb"] = xgb.predict([x_current])
                    if "lgb" in self.models_to_run:
                        lgb = LightGBMPredictor().train(X_train, y_train)
                        scores["lgb"] = lgb.predict([x_current])
            except Exception:
                pass

        if "lstm" in self.models_to_run and self.history:
            try:
                lstm = LSTMPredictor(sequence_length=10).train(self.history, epochs=5)
                scores["lstm"] = lstm.predict(self.history)
            except Exception:
                pass

        if not scores:
            scores["bayes"] = {num: 1.0 / 49.0 for num in range(1, 50)}

        return fuse_scores(scores)

    @staticmethod
    def build_ranking_for_history(history: List[int]) -> list[dict]:
        return PredictionPipeline(history).run()

