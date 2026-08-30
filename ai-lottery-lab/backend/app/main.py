from fastapi import FastAPI
from app.api.prediction import router as prediction_router
from app.api.training import router as training_router
from app.api.backtest import router as backtest_router
from app.api.crawler_api import router as crawler_router

app = FastAPI(
    title="AI Lottery Prediction Lab",
    description="Multi-model lottery probability analysis platform",
    version="1.0.0",
)

app.include_router(prediction_router, prefix="/api")
app.include_router(training_router, prefix="/api")
app.include_router(backtest_router, prefix="/api")
app.include_router(crawler_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-lottery-lab"}

