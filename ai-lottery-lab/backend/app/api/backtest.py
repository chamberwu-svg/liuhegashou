from __future__ import annotations

from fastapi import APIRouter

from app.backtesting.walker import walk_forward_backtest
from app.database.seed import load_history_from_db_or_seed
from app.services.pipeline import PredictionPipeline

router = APIRouter(tags=["backtest"])


@router.get("/backtest")
def backtest():
    history = load_history_from_db_or_seed(limit=100)

    def predict_fn(train_history):
        return PredictionPipeline(train_history, models_to_run=["markov", "bayes", "rf"]).run()

    metrics = walk_forward_backtest(history, predict_fn, window=80)
    return {
        "model": "ensemble",
        "top1": metrics["top1"],
        "top5": metrics["top5"],
        "top10": metrics["top10"],
        "mean_rank": metrics["mean_rank"],
        "random_baseline": metrics["random_baseline"],
    }


