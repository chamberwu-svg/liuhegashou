from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.database.seed import load_history_from_db_or_seed
from app.feature.engineering import build_tabular_dataset
from app.models.bayesian import BayesianPredictor
from app.models.markov import MarkovPredictor
from app.models.random_forest import RandomForestPredictor
from app.models.xgboost_model import XGBoostPredictor
from app.models.lightgbm_model import LightGBMPredictor
from app.models.lstm import LSTMPredictor

router = APIRouter(tags=["training"])


class TrainingRequest(BaseModel):
    dataset: str
    models: list[str]


@router.post("/train")
def train_model(payload: TrainingRequest):
    dataset_size = int(payload.dataset)
    history = load_history_from_db_or_seed(limit=dataset_size)
    X_train, y_train = build_tabular_dataset(history)

    trained = []
    for model_name in payload.models:
        m_lower = model_name.lower()
        if m_lower == "markov":
            MarkovPredictor(order=1).train(history)
            trained.append("markov")
        elif m_lower in ["bayes", "bayesian"]:
            BayesianPredictor().train(history)
            trained.append("bayes")
        elif m_lower in ["rf", "random_forest"]:
            RandomForestPredictor(n_estimators=50).train(X_train, y_train)
            trained.append("rf")
        elif m_lower in ["xgb", "xgboost"]:
            XGBoostPredictor().train(X_train, y_train)
            trained.append("xgb")
        elif m_lower in ["lgb", "lightgbm"]:
            LightGBMPredictor().train(X_train, y_train)
            trained.append("lgb")
        elif m_lower == "lstm":
            LSTMPredictor(sequence_length=15).train(history, epochs=5)
            trained.append("lstm")

    return {
        "status": "completed",
        "dataset": dataset_size,
        "models": payload.models,
        "history_length": len(history),
        "trained_models": sorted(trained),
        "message": "Training completed for selected ML and statistical models.",
    }


