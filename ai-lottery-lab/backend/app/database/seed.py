from __future__ import annotations

import random
from typing import List, Dict, Any
from app.database.connection import get_connection
from app.crawler.crawler import LotteryDataCrawler, determine_color, determine_size, determine_odd_even


def generate_history(length: int = 500, seed: int = 42) -> List[int]:
    """Generate synthetic lottery draw sequence if database is empty."""
    rng = random.Random(seed)
    history: List[int] = []
    for _ in range(length):
        number = rng.randint(1, 49)
        history.append(number)
    return history


def load_history_from_db_or_seed(limit: int = 500) -> List[int]:
    """Load special_number history from SQLite database; fallback to synthetic seed if empty."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT special_number FROM lottery_results ORDER BY id ASC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        return [row[0] for row in rows]

    # Try fetching from Crawler
    crawler = LotteryDataCrawler()
    crawled_data = crawler.fetch_draw_data(limit=limit)
    if crawled_data:
        save_draw_data(crawled_data)
        return [d["special_number"] for d in reversed(crawled_data)]

    return generate_history(length=limit)


def save_draw_data(records: List[Dict[str, Any]]) -> int:
    """Save lottery draw records into DB with IGNORE on duplicate issues."""
    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0
    for r in records:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO lottery_results (issue, draw_date, special_number, color, size, odd_even, zodiac)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r.get("issue"),
                    r.get("draw_date"),
                    r.get("special_number"),
                    r.get("color") or determine_color(r.get("special_number", 1)),
                    r.get("size") or determine_size(r.get("special_number", 1)),
                    r.get("odd_even") or determine_odd_even(r.get("special_number", 1)),
                    r.get("zodiac", "HORSE"),
                ),
            )
            if cursor.rowcount > 0:
                inserted += 1
        except Exception:
            pass
    conn.commit()
    conn.close()
    return inserted

