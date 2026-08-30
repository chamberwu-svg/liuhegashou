from __future__ import annotations

import json
from typing import Dict, List, Any

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class PyTorchLSTM(nn.Module):
    def __init__(self, num_classes: int = 49, hidden_dim: int = 64):
        super().__init__()
        self.embedding = nn.Embedding(50, 16)
        self.lstm = nn.LSTM(16, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        embeds = self.embedding(x)
        out, _ = self.lstm(embeds)
        last_out = out[:, -1, :]
        logits = self.fc(last_out)
        return torch.softmax(logits, dim=-1)


class LSTMPredictor:
    def __init__(self, sequence_length: int = 20):
        self.sequence_length = sequence_length
        self.is_trained = False
        self.model = PyTorchLSTM(num_classes=49, hidden_dim=32)

    def train(self, history: List[int], epochs: int = 15):
        if len(history) <= self.sequence_length:
            self.is_trained = True
            return self

        sequences, targets = [], []
        for i in range(len(history) - self.sequence_length):
            seq = history[i : i + self.sequence_length]
            target = history[i + self.sequence_length] - 1  # 0-indexed for 49 classes
            sequences.append(seq)
            targets.append(target)

        X_tensor = torch.tensor(sequences, dtype=torch.long)
        y_tensor = torch.tensor(targets, dtype=torch.long)

        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        criterion = nn.CrossEntropyLoss()

        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            output = self.model(X_tensor)
            loss = criterion(output, y_tensor)
            loss.backward()
            optimizer.step()

        self.is_trained = True
        return self

    def predict(self, history: List[int]) -> Dict[int, float]:
        if not self.is_trained:
            raise ValueError("model must be trained before prediction")

        if len(history) < self.sequence_length:
            padding = [1] * (self.sequence_length - len(history))
            seq = padding + history
        else:
            seq = history[-self.sequence_length :]

        self.model.eval()
        with torch.no_grad():
            inp = torch.tensor([seq], dtype=torch.long)
            probs = self.model(inp)[0].numpy()

        return {number: float(prob) for number, prob in enumerate(probs, start=1)}

    def build_sequences(self, history: List[int], sequence_length: int) -> np.ndarray:
        windows = []
        for idx in range(len(history) - sequence_length + 1):
            window = history[idx : idx + sequence_length]
            windows.append(np.asarray(window, dtype=float))
        return np.asarray(windows)

    def save(self, path: str):
        torch.save({"state_dict": self.model.state_dict(), "sequence_length": self.sequence_length, "is_trained": self.is_trained}, path)

    def load(self, path: str):
        data = torch.load(path)
        self.sequence_length = data.get("sequence_length", self.sequence_length)
        self.model = PyTorchLSTM(num_classes=49, hidden_dim=32)
        self.model.load_state_dict(data["state_dict"])
        self.is_trained = data.get("is_trained", False)
        return self

