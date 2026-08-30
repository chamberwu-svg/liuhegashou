from __future__ import annotations

from fastapi import APIRouter
from app.database.seed import load_history_from_db_or_seed
from app.services.pipeline import PredictionPipeline

router = APIRouter(tags=["prediction"])


@router.get("/predict")
def predict():
    history = load_history_from_db_or_seed(limit=500)
    ranking = PredictionPipeline(history).run()
    return {"ranking": [{"number": item["number"], "score": item["score"], "consensus": f"{item['consensus']}"} for item in ranking]}

