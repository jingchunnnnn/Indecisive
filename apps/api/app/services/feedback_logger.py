"""Append-only feedback event logging for future ranker training."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from app.schemas.requests import FeedbackRequest


class FeedbackLogger:
    def __init__(self, path: Path):
        self.path = path

    def append(self, payload: FeedbackRequest) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "logged_at": datetime.now(UTC).isoformat(),
            **payload.model_dump(mode="json"),
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=True, sort_keys=True))
            handle.write("\n")
