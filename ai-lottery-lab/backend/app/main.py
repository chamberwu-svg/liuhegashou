import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

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


# Locate Vue 3 compiled static dist folder
frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if not frontend_dist.exists():
    frontend_dist = Path(__file__).resolve().parents[3] / "ai-lottery-lab" / "frontend" / "dist"

if frontend_dist.exists() and (frontend_dist / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")


@app.get("/")
async def read_root():
    if frontend_dist.exists() and (frontend_dist / "index.html").exists():
        return FileResponse(frontend_dist / "index.html")
    return RedirectResponse(url="/docs")


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api") or full_path.startswith("docs") or full_path == "openapi.json" or full_path == "health":
        return None
    if frontend_dist.exists():
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    return RedirectResponse(url="/docs")


