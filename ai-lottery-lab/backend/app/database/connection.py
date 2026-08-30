from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[3] / "database" / "lottery.db"


def get_database_path() -> Path:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return DB_PATH


def get_connection() -> sqlite3.Connection:
    path = get_database_path()
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lottery_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT UNIQUE,
            draw_date TEXT,
            special_number INTEGER,
            color TEXT,
            size TEXT,
            odd_even TEXT,
            zodiac TEXT
        )
        """
    )
    conn.commit()
    return conn

