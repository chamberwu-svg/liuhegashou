from __future__ import annotations

from typing import Dict, List


def generate_features(number: int, history: List[int]) -> Dict[str, float | int]:
    """Generate a compact feature vector for a lottery number using the recent history.

    The function intentionally keeps the contract simple and deterministic so it can be
    used by statistical models and ML classifiers without a database dependency.
    """
    if not history:
        raise ValueError("history must contain at least one draw")

    history = list(history)
    recent_10 = history[-10:]
    recent_30 = history[-30:]
    recent_50 = history[-50:]
    recent_100 = history[-100:]

    frequency_10 = recent_10.count(number)
    frequency_30 = recent_30.count(number)
    frequency_100 = recent_100.count(number)

    current_missing = 0
    last_seen = None
    max_missing = 0
    total_missing = 0
    miss_counts = []

    for draw in history:
        if draw == number:
            if last_seen is not None:
                miss_counts.append(len(miss_counts))
            last_seen = draw
            current_missing = 0
        else:
            current_missing += 1
            total_missing += 1
            max_missing = max(max_missing, current_missing)

    if len(history) == 0:
        max_missing = 0

    if number in history:
        gap = 0
        seen_positions = [idx for idx, value in enumerate(history) if value == number]
        if len(seen_positions) >= 2:
            gap = seen_positions[-1] - seen_positions[-2]
        else:
            gap = len(history) - seen_positions[-1]
    else:
        gap = len(history)

    hot_score = (frequency_100 / max(1, len(recent_100)))
    color_score = 0.5
    size_score = 0.5
    odd_even_score = 0.5

    return {
        "number": number,
        "frequency_10": frequency_10,
        "frequency_30": frequency_30,
        "frequency_100": frequency_100,
        "current_missing": current_missing,
        "average_missing": total_missing / max(1, len(history)),
        "max_missing": max_missing,
        "hot_score": hot_score,
        "color_score": color_score,
        "size_score": size_score,
        "odd_even_score": odd_even_score,
        "distance_since_last_seen": gap,
    }


def extract_draw_features(history: List[int]) -> List[float]:
    """Extract a 1D tabular feature vector representing the state of all 49 numbers before the next draw.

    Features per number (1..49):
    - current missing count
    - freq in last 10
    - freq in last 30
    - freq in last 100
    Total = 49 * 4 = 196 features.
    """
    if not history:
        return [0.0] * 196

    features: List[float] = []
    recent_10 = history[-10:]
    recent_30 = history[-30:]
    recent_100 = history[-100:]

    for num in range(1, 50):
        missing = 0
        for draw in reversed(history):
            if draw == num:
                break
            missing += 1

        freq_10 = recent_10.count(num) / max(1, len(recent_10))
        freq_30 = recent_30.count(num) / max(1, len(recent_30))
        freq_100 = recent_100.count(num) / max(1, len(recent_100))

        features.extend([float(missing), float(freq_10), float(freq_30), float(freq_100)])

    return features


def build_tabular_dataset(history: List[int], min_history: int = 30) -> tuple[List[List[float]], List[int]]:
    """Build (X, y) tabular dataset for ML model training from lottery draw history."""
    X: List[List[float]] = []
    y: List[int] = []

    if len(history) <= min_history:
        min_history = max(1, len(history) - 1)

    for i in range(min_history, len(history)):
        sub_history = history[:i]
        target = history[i]
        X.append(extract_draw_features(sub_history))
        y.append(target)

    return X, y

