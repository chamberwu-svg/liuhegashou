from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.crawler.crawler import LotteryDataCrawler
from app.database.seed import save_draw_data, load_history_from_db_or_seed

router = APIRouter(tags=["crawler"])


class SyncRequest(BaseModel):
    limit: Optional[int] = 100


@router.post("/api/sync")
def sync_lottery_data(payload: SyncRequest):
    crawler = LotteryDataCrawler()
    records = crawler.fetch_draw_data(limit=payload.limit or 100)
    saved_count = 0
    if records:
        saved_count = save_draw_data(records)

    total_in_db = len(load_history_from_db_or_seed(limit=1000))
    return {
        "status": "success",
        "fetched": len(records),
        "new_records": saved_count,
        "total_records": total_in_db,
        "message": f"Fetched {len(records)} records from external API ({'MacauJC / KJ1868' if records else 'Fallback to seed'}).",
    }
