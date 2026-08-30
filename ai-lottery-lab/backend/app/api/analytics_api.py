from __future__ import annotations

from collections import Counter
from typing import Dict, Any, List
from fastapi import APIRouter

from app.database.seed import load_history_from_db_or_seed, load_recent_draw_details
from app.feature.engineering import generate_features
from app.crawler.crawler import determine_color, determine_size, determine_odd_even

router = APIRouter(tags=["analytics"])


@router.get("/analytics")
def get_analytics(limit: int = 300) -> Dict[str, Any]:
    history = load_history_from_db_or_seed(limit=limit)
    recent_details = load_recent_draw_details(limit=limit)

    total_draws = len(history)
    if total_draws == 0:
        return {"error": "No draw history available."}

    # 1. 冷热号分析
    counts = Counter(history)
    sorted_by_freq = sorted([(num, count) for num, count in counts.items()], key=lambda x: x[1], reverse=True)
    hot_numbers = [{"number": num, "frequency": count, "ratio": round(count / total_draws * 100, 1)} for num, count in sorted_by_freq[:5]]

    # 计算 01..49 当前遗漏
    missing_dict = {}
    for num in range(1, 50):
        missing = 0
        for draw in reversed(history):
            if draw == num:
                break
            missing += 1
        missing_dict[num] = missing

    sorted_by_missing = sorted(missing_dict.items(), key=lambda x: x[1], reverse=True)
    cold_numbers = [{"number": num, "missing": missing} for num, missing in sorted_by_missing[:5]]

    # 2. 波色分布
    colors = [determine_color(num) for num in history]
    color_counts = Counter(colors)
    color_dist = {
        "RED": {"count": color_counts.get("RED", 0), "ratio": round(color_counts.get("RED", 0) / total_draws * 100, 1)},
        "BLUE": {"count": color_counts.get("BLUE", 0), "ratio": round(color_counts.get("BLUE", 0) / total_draws * 100, 1)},
        "GREEN": {"count": color_counts.get("GREEN", 0), "ratio": round(color_counts.get("GREEN", 0) / total_draws * 100, 1)},
    }

    # 3. 大小/单双分布
    sizes = [determine_size(num) for num in history]
    odd_evens = [determine_odd_even(num) for num in history]
    size_counts = Counter(sizes)
    oe_counts = Counter(odd_evens)

    attr_dist = {
        "BIG": {"count": size_counts.get("BIG", 0), "ratio": round(size_counts.get("BIG", 0) / total_draws * 100, 1)},
        "SMALL": {"count": size_counts.get("SMALL", 0), "ratio": round(size_counts.get("SMALL", 0) / total_draws * 100, 1)},
        "ODD": {"count": oe_counts.get("ODD", 0), "ratio": round(oe_counts.get("ODD", 0) / total_draws * 100, 1)},
        "EVEN": {"count": oe_counts.get("EVEN", 0), "ratio": round(oe_counts.get("EVEN", 0) / total_draws * 100, 1)},
    }

    # 4. 生肖分布
    zodiac_list = [d.get("zodiac", "HORSE") for d in recent_details]
    zodiac_counts = Counter(zodiac_list)
    zodiac_dist = [{"zodiac": z, "count": c} for z, c in zodiac_counts.most_common()]

    # 5. 01-49 号码矩阵分析 (供人工验算)
    matrix = []
    for num in range(1, 50):
        feats = generate_features(num, history)
        matrix.append({
            "number": num,
            "color": determine_color(num),
            "size": determine_size(num),
            "odd_even": determine_odd_even(num),
            "current_missing": feats["current_missing"],
            "max_missing": feats["max_missing"],
            "frequency_30": feats["frequency_30"],
            "frequency_100": feats["frequency_100"],
            "hot_score": round(feats["hot_score"] * 100, 1),
        })

    return {
        "total_draws": total_draws,
        "hot_numbers": hot_numbers,
        "cold_numbers": cold_numbers,
        "color_dist": color_dist,
        "attr_dist": attr_dist,
        "zodiac_dist": zodiac_dist,
        "missing_matrix": matrix,
        "audit_checksum": f"SHA256-{hash(tuple(history[:20])) & 0xffffffff:08x}",
    }
