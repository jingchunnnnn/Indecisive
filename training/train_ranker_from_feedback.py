"""Train the optional ranker from local feedback events.

Run from the repo root after collecting feedback:

    python training/train_ranker_from_feedback.py

The script reads data/feedback.jsonl and writes models/ranker.pkl plus
models/ranker_metadata.json. It refuses to train until there is enough signal.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEEDBACK_PATH = ROOT / "data" / "feedback.jsonl"
MODELS_DIR = ROOT / "models"
MIN_EVENTS = 20


def target_for(action: str) -> float | None:
    if action == "liked":
        return 1.0
    if action in {"not_for_me", "disliked"}:
        return 0.0
    return None


def distance_feature(event: dict[str, Any]) -> float:
    distance_m = event.get("distance_m")
    radius_m = (((event.get("request") or {}).get("survey") or {}).get("radius_m")) or 2000
    if distance_m is None:
        return 0.25
    return max(0.0, 1.0 - min(float(distance_m) / max(float(radius_m), 1.0), 1.0))


def load_training_rows(path: Path) -> tuple[np.ndarray, np.ndarray]:
    features: list[list[float]] = []
    targets: list[float] = []

    if not path.exists():
        return np.empty((0, 3)), np.empty((0,))

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        target = target_for(str(event.get("action") or ""))
        score = event.get("score")
        if target is None or score is None:
            continue
        features.append([float(score), distance_feature(event), 0.5])
        targets.append(target)

    return np.asarray(features, dtype=np.float32), np.asarray(targets, dtype=np.float32)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feedback", type=Path, default=DEFAULT_FEEDBACK_PATH)
    parser.add_argument("--min-events", type=int, default=MIN_EVENTS)
    args = parser.parse_args()

    features, targets = load_training_rows(args.feedback)
    if len(targets) < args.min_events:
        raise SystemExit(f"Need at least {args.min_events} usable feedback events; found {len(targets)}.")
    if len(set(targets.tolist())) < 2:
        raise SystemExit("Need both positive and negative feedback before training.")

    model = RandomForestRegressor(n_estimators=80, random_state=42, max_depth=5, min_samples_leaf=2)
    model.fit(features, targets)

    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODELS_DIR / "ranker.pkl")
    (MODELS_DIR / "ranker_metadata.json").write_text(
        json.dumps(
            {
                "trained_at": datetime.now(UTC).isoformat(),
                "source": str(args.feedback.relative_to(ROOT) if args.feedback.is_relative_to(ROOT) else args.feedback),
                "training_events": int(len(targets)),
                "positive_events": int(np.sum(targets == 1.0)),
                "negative_events": int(np.sum(targets == 0.0)),
                "feature_order": ["base_score", "distance_score", "semantic_score"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Wrote models/ranker.pkl and models/ranker_metadata.json")


if __name__ == "__main__":
    main()
