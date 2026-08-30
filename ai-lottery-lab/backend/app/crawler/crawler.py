"""Crawler module for fetching historical lottery draw data from external APIs."""

from __future__ import annotations

import logging
from datetime import datetime, date
from typing import Any, Dict, List, Optional
import httpx

logger = logging.getLogger(__name__)

# Macau Jockey Club / General Lottery Open API endpoints
MACAUJC_API_URL = "https://macaujc.com/api/history"
KJ1868_API_URL = "https://www.kj1868.cc/api/drawHistory"


def determine_color(number: int) -> str:
    """Return color (RED, BLUE, GREEN) for number 1..49 under standard Liuhe rules."""
    red_balls = {1, 2, 7, 8, 12, 13, 18, 19, 23, 24, 29, 30, 34, 35, 40, 45, 46}
    blue_balls = {3, 4, 9, 10, 14, 15, 20, 25, 26, 31, 32, 36, 37, 41, 42, 47, 48}
    if number in red_balls:
        return "RED"
    elif number in blue_balls:
        return "BLUE"
    return "GREEN"


def determine_size(number: int) -> str:
    """Return BIG if number >= 25 else SMALL."""
    return "BIG" if number >= 25 else "SMALL"


def determine_odd_even(number: int) -> str:
    """Return ODD if number % 2 != 0 else EVEN."""
    return "ODD" if number % 2 == 0 else "EVEN"


class LotteryDataCrawler:
    """Crawler service that attempts fetching real draw history from external APIs."""

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    def fetch_from_macaujc(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch history draw results from macaujc.com API."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(f"{MACAUJC_API_URL}?limit={limit}")
                if res.status_code == 200:
                    data = res.json()
                    results = []
                    raw_list = data.get("data", []) if isinstance(data, dict) else data
                    for item in raw_list:
                        sp_num = int(item.get("special_number") or item.get("specialNumber") or item.get("sp", 0))
                        if 1 <= sp_num <= 49:
                            results.append({
                                "issue": str(item.get("issue") or item.get("period")),
                                "draw_date": str(item.get("draw_date") or item.get("date") or date.today().isoformat()),
                                "special_number": sp_num,
                                "color": determine_color(sp_num),
                                "size": determine_size(sp_num),
                                "odd_even": determine_odd_even(sp_num),
                                "zodiac": item.get("zodiac", "UNKNOWN"),
                            })
                    return results
        except Exception as e:
            logger.warning(f"Failed to fetch from MacauJC API: {e}")
        return []

    def fetch_from_kj1868(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch history draw results from kj1868 open API."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(f"{KJ1868_API_URL}?pageSize={limit}")
                if res.status_code == 200:
                    data = res.json()
                    results = []
                    raw_list = data.get("rows") or data.get("data") or []
                    for item in raw_list:
                        sp_num = int(item.get("specialNum") or item.get("number") or item.get("ball", 0))
                        if 1 <= sp_num <= 49:
                            results.append({
                                "issue": str(item.get("issue") or item.get("period")),
                                "draw_date": str(item.get("openTime") or item.get("date") or date.today().isoformat()),
                                "special_number": sp_num,
                                "color": determine_color(sp_num),
                                "size": determine_size(sp_num),
                                "odd_even": determine_odd_even(sp_num),
                                "zodiac": item.get("shengxiao") or item.get("zodiac") or "UNKNOWN",
                            })
                    return results
        except Exception as e:
            logger.warning(f"Failed to fetch from KJ1868 API: {e}")
        return []

    def fetch_draw_data(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Try fetching from primary source (MacauJC), fallback to secondary (KJ1868)."""
        data = self.fetch_from_macaujc(limit=limit)
        if not data:
            data = self.fetch_from_kj1868(limit=limit)
        return data
