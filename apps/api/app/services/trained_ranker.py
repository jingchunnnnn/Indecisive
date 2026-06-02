"""Optional inference-only trained ranker loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib


class TrainedRanker:
    def __init__(self, artifact_dir: Path, enabled: bool):
        self.enabled = enabled
        self.model: Any | None = None
        if enabled:
            self.model = self._load(artifact_dir / "ranker.pkl")

    @property
    def available(self) -> bool:
        return self.model is not None

    def predict_score(self, features: list[float]) -> float | None:
        if not self.model:
            return None
        try:
            prediction = self.model.predict([features])[0]
            return float(prediction)
        except Exception:
            return None

    def _load(self, path: Path) -> Any | None:
        if not path.exists():
            return None
        try:
            return joblib.load(path)
        except Exception:
            return None
