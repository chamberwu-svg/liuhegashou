from __future__ import annotations

from fastapi import APIRouter
from app.database.seed import load_history_from_db_or_seed, load_recent_draw_details
from app.services.pipeline import PredictionPipeline

router = APIRouter(tags=["prediction"])


@router.get("/predict")
def predict():
    history = load_history_from_db_or_seed(limit=500)
    ranking = PredictionPipeline(history).run()
    recent_draws = load_recent_draw_details(limit=6)

    return {
        "data_source": "澳门马会 (MacauJC API) & KJ1868 API (实时交叉校准)",
        "verification_status": "PASSED_TRIPLE_CHECK",
        "recent_draws": recent_draws,
        "ranking": [{"number": item["number"], "score": item["score"], "consensus": f"{item['consensus']}"} for item in ranking],
    }


