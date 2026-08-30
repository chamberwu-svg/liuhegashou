from __future__ import annotations

from typing import Dict, List
from app.ensemble.consensus import calculate_consensus


DEFAULT_WEIGHTS = {
    "markov": 0.10,
    "bayes": 0.15,
    "rf": 0.15,
    "xgb": 0.20,
    "lgb": 0.20,
    "lstm": 0.20,
}


def fuse_scores(model_scores: Dict[str, Dict[int, float]], weights: Dict[str, float] | None = None) -> List[Dict[str, float | int | str]]:
    weights = weights or DEFAULT_WEIGHTS
    numbers = set().union(*(scores.keys() for scores in model_scores.values()))
    if not numbers:
        numbers = set(range(1, 50))

    active_weight_total = sum(weights.get(m, 0.0) for m in model_scores if m in weights)
    if active_weight_total == 0:
        active_weight_total = 1.0

    consensus_list = calculate_consensus(model_scores, top_k=10)
    consensus_map = {item["number"]: item["consensus"] for item in consensus_list}

    fused: Dict[int, float] = {}
    for number in sorted(numbers):
        total = 0.0
        for model_name, score_map in model_scores.items():
            model_weight = weights.get(model_name, 0.0) / active_weight_total
            total += score_map.get(number, 0.0) * model_weight
        fused[number] = total

    ranked = sorted(fused.items(), key=lambda item: item[1], reverse=True)
    result = []
    total_models = len(model_scores) or 6

    for number, score in ranked[:10]:
        c_str = consensus_map.get(number, f"0/{total_models}")
        result.append({
            "number": number,
            "score": round(score * 100, 1),
            "consensus": c_str,
        })
    return result


def build_ensemble_ranking(model_scores: Dict[str, Dict[int, float]], weights: Dict[str, float] | None = None) -> List[Dict[str, float | int | str]]:
    return fuse_scores(model_scores, weights)

