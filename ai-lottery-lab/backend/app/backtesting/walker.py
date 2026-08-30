from __future__ import annotations

from typing import Callable, Dict, List


def walk_forward_backtest(history: List[int], model_predict_fn: Callable[[List[int]], List[dict]], window: int = 500) -> Dict[str, float | int]:
    if len(history) < 2:
        raise ValueError("history must contain at least two draws")

    hits_top1 = 0
    hits_top5 = 0
    hits_top10 = 0
    ranks = []
    evaluated = 0

    for idx in range(window, len(history) - 1):
        train_history = history[:idx]
        target = history[idx]
        ranking = model_predict_fn(train_history)
        ranked_numbers = [item["number"] for item in ranking]

        if target in ranked_numbers[:1]:
            hits_top1 += 1
        if target in ranked_numbers[:5]:
            hits_top5 += 1
        if target in ranked_numbers[:10]:
            hits_top10 += 1

        if target in ranked_numbers:
            ranks.append(ranked_numbers.index(target) + 1)
        else:
            ranks.append(len(ranked_numbers) + 1)
        evaluated += 1

    total = max(1, evaluated)
    mean_rank = sum(ranks) / len(ranks) if ranks else 0.0

    return {
        "model": "walk_forward",
        "period": len(history),
        "top1": round(hits_top1 / total, 4),
        "top5": round(hits_top5 / total, 4),
        "top10": round(hits_top10 / total, 4),
        "mean_rank": round(mean_rank, 4),
        "random_baseline": round(1 / 49, 4),
    }
