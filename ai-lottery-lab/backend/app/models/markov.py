from __future__ import annotations

import json
from collections import defaultdict, Counter
from typing import Any, Dict, List


class MarkovPredictor:
    def __init__(self, order: int = 1):
        self.order = order
        self.transition: Dict[tuple[int, ...], Counter] = defaultdict(Counter)
        self.base_probs: Counter = Counter()
        self.is_trained = False

    def train(self, history: List[int]):
        if len(history) <= self.order:
            raise ValueError("history must be longer than the Markov order")

        self.transition.clear()
        self.base_probs.clear()

        for idx in range(len(history) - self.order):
            context = tuple(history[idx : idx + self.order])
            next_value = history[idx + self.order]
            self.transition[context][next_value] += 1
            self.base_probs[next_value] += 1

        self.is_trained = True
        return self

    def predict(self, recent_numbers: List[int]) -> Dict[int, float]:
        if not self.is_trained:
            raise ValueError("model must be trained before prediction")

        result = {number: 0.0 for number in range(1, 50)}
        context = tuple(recent_numbers[-self.order :]) if recent_numbers else tuple()

        if not context or context not in self.transition:
            if not self.base_probs:
                return {number: 1 / 49.0 for number in range(1, 50)}
            total = sum(self.base_probs.values())
            for number in range(1, 50):
                result[number] = self.base_probs.get(number, 0) / total
            return result

        total = sum(self.transition[context].values())
        for number in range(1, 50):
            result[number] = self.transition[context].get(number, 0) / total
        return result

    def save(self, path: str):
        payload = {"order": self.order, "transition": {str(k): dict(v) for k, v in self.transition.items()}, "base_probs": dict(self.base_probs), "is_trained": self.is_trained}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)

    def load(self, path: str):
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        self.order = payload["order"]
        self.transition = defaultdict(Counter, {tuple(map(int, k.strip("() ").split(","))) if k.strip() else tuple(): Counter(v) for k, v in payload.get("transition", {}).items()})
        self.base_probs = Counter(payload.get("base_probs", {}))
        self.is_trained = payload.get("is_trained", False)
        return self
