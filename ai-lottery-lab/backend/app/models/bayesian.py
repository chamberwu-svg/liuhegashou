from __future__ import annotations

import json
from collections import Counter
from typing import Dict, List


class BayesianPredictor:
    def __init__(self):
        self.history: List[int] = []
        self.is_trained = False

    def train(self, history: List[int]):
        self.history = list(history)
        self.is_trained = True
        return self

    def predict(self) -> Dict[int, float]:
        if not self.is_trained:
            raise ValueError("model must be trained before prediction")

        counts = Counter(self.history)
        total = max(1, len(self.history))
        probabilities = {number: counts.get(number, 0) / total for number in range(1, 50)}

        recent_window = self.history[-100:]
        recent_counts = Counter(recent_window)
        recent_total = max(1, len(recent_window))

        for number in range(1, 50):
            prior = probabilities[number]
            recent = recent_counts.get(number, 0) / recent_total
            score = (0.6 * prior) + (0.4 * recent)
            probabilities[number] = score

        total_score = sum(probabilities.values())
        if total_score == 0:
            return {number: 1 / 49.0 for number in range(1, 50)}

        return {number: value / total_score for number, value in probabilities.items()}

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"history": self.history, "is_trained": self.is_trained}, fh)

    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        self.history = payload.get("history", [])
        self.is_trained = payload.get("is_trained", False)
        return self
