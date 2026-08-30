from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class LotteryResult:
    id: Optional[int] = None
    issue: Optional[str] = None
    draw_date: Optional[date] = None
    special_number: Optional[int] = None
    color: Optional[str] = None
    size: Optional[str] = None
    odd_even: Optional[str] = None
    zodiac: Optional[str] = None
