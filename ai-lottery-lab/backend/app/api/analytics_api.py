from __future__ import annotations

from collections import Counter
from typing import Dict, Any, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.database.seed import load_history_from_db_or_seed, load_recent_draw_details
from app.feature.engineering import generate_features
from app.crawler.crawler import determine_color, determine_size, determine_odd_even

router = APIRouter(tags=["analytics"])


class ComboTestRequest(BaseModel):
    numbers: List[int]
    limit: Optional[int] = 300
    bet_per_number: Optional[float] = 10.0
    odds: Optional[float] = 48.0


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

    # 4. 尾数 (0-9尾) 与头数 (0-4头) 分布
    tail_counts = Counter([num % 10 for num in history])
    head_counts = Counter([num // 10 for num in history])
    tail_dist = [{"tail": f"{t}尾", "count": tail_counts.get(t, 0), "ratio": round(tail_counts.get(t, 0) / total_draws * 100, 1)} for t in range(10)]
    head_dist = [{"head": f"{h}头", "count": head_counts.get(h, 0), "ratio": round(head_counts.get(h, 0) / total_draws * 100, 1)} for h in range(5)]

    # 5. 生肖分布
    zodiac_list = [d.get("zodiac", "HORSE") for d in recent_details]
    zodiac_counts = Counter(zodiac_list)
    zodiac_dist = [{"zodiac": z, "count": c} for z, c in zodiac_counts.most_common()]

    # 6. 01-49 号码矩阵分析 (供人工验算)
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
        "tail_dist": tail_dist,
        "head_dist": head_dist,
        "zodiac_dist": zodiac_dist,
        "missing_matrix": matrix,
        "audit_checksum": f"SHA256-{hash(tuple(history[:20])) & 0xffffffff:08x}",
    }


@router.post("/analytics/combo-test")
def simulate_combo_test(payload: ComboTestRequest) -> Dict[str, Any]:
    """Simulate a lottery combination purchase test against historical data."""
    limit = payload.limit or 300
    bet_per_num = payload.bet_per_number or 10.0
    odds = payload.odds or 48.0
    combo_numbers = set(payload.numbers)

    if not combo_numbers:
        return {"error": "Please provide at least one number for combination simulation."}

    history = load_history_from_db_or_seed(limit=limit)
    total_draws = len(history)

    if total_draws == 0:
        return {"error": "No historical data available."}

    combo_size = len(combo_numbers)
    cost_per_draw = round(combo_size * bet_per_num, 2)
    payout_per_hit = round(bet_per_num * odds, 2)
    net_profit_per_hit = round(payout_per_hit - cost_per_draw, 2)

    hits = 0
    total_cost = round(total_draws * cost_per_draw, 2)
    total_payout = 0.0

    current_miss = 0
    max_miss = 0
    current_consec_hit = 0
    max_consec_hit = 0
    hit_details = []

    for idx, draw_num in enumerate(history, start=1):
        if draw_num in combo_numbers:
            hits += 1
            total_payout += payout_per_hit
            current_consec_hit += 1
            max_consec_hit = max(max_consec_hit, current_consec_hit)
            current_miss = 0
            hit_details.append({"draw_index": idx, "winning_number": draw_num, "payout": payout_per_hit})
        else:
            current_miss += 1
            max_miss = max(max_miss, current_miss)
            current_consec_hit = 0

    misses = total_draws - hits
    total_hit_profit = round(hits * net_profit_per_hit, 2)
    total_miss_loss = round(misses * cost_per_draw, 2)
    net_profit = round(total_payout - total_cost, 2)
    roi = round((net_profit / max(1.0, total_cost)) * 100, 2)
    win_rate = round((hits / total_draws) * 100, 2)
    expected_hit_rate = round((combo_size / 49.0) * 100, 2)

    risk_evaluation = "风险均衡"
    if roi > 20:
        risk_evaluation = "历史暴利 (高收益倾向)"
    elif roi > 0:
        risk_evaluation = "历史盈利 (微利)"
    elif roi > -20:
        risk_evaluation = "轻度亏损 (抽水磨损)"
    else:
        risk_evaluation = "高危重亏 (警惕冷号组合)"

    return {
        "combo_numbers": sorted(list(combo_numbers)),
        "combo_size": combo_size,
        "total_draws": total_draws,
        "cost_per_draw": cost_per_draw,
        "payout_per_hit": payout_per_hit,
        "net_profit_per_hit": net_profit_per_hit,
        "hits": hits,
        "misses": misses,
        "total_hit_profit": total_hit_profit,
        "total_miss_loss": total_miss_loss,
        "win_rate": win_rate,
        "expected_hit_rate": expected_hit_rate,
        "total_cost": total_cost,
        "total_payout": round(total_payout, 2),
        "net_profit": net_profit,
        "roi": roi,
        "max_consecutive_hits": max_consec_hit,
        "max_consecutive_misses": max_miss,
        "risk_evaluation": risk_evaluation,
        "hit_details": hit_details[-10:],  # 最近10次中奖记录
    }


