from __future__ import annotations

from typing import Dict, Any, List


MODEL_KEY_MAP = {
    "markov": "Markov",
    "bayes": "Bayes",
    "rf": "RF",
    "xgb": "XGB",
    "lgb": "LGB",
    "lstm": "LSTM",
}


def calculate_consensus(model_scores: Dict[str, Dict[int, float]], top_k: int = 10) -> List[Dict[str, Any]]:
    """Build a dynamic model consensus report for numbers based on Top-K predictions of each model."""
    if not model_scores:
        return []

    model_top_k: Dict[str, set[int]] = {}
    for model_name, score_map in model_scores.items():
        sorted_nums = sorted(score_map.keys(), key=lambda n: score_map[n], reverse=True)
        model_top_k[model_name] = set(sorted_nums[:top_k])

    numbers = sorted({num for score_map in model_scores.values() for num in score_map})
    result: List[Dict[str, Any]] = []
    total_models = len(model_scores)

    for number in numbers:
        support: Dict[str, bool] = {}
        supported_count = 0
        for model_key, display_name in MODEL_KEY_MAP.items():
            if model_key in model_scores:
                is_supported = number in model_top_k[model_key]
                support[display_name] = is_supported
                if is_supported:
                    supported_count += 1

        score = round((supported_count / max(1, total_models)) * 100, 1)
        result.append({
            "number": number,
            "support": support,
            "consensus_count": supported_count,
            "total_models": total_models,
            "consensus": f"{supported_count}/{total_models}",
            "score": score,
        })

    return sorted(result, key=lambda item: item["score"], reverse=True)

