"""Optional local demo ranker training.

This script trains a tiny synthetic learning-to-rank regressor and exports
artifacts. It is not used by FastAPI unless ENABLE_TRAINED_RANKER=true.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def main() -> None:
    rng = np.random.default_rng(42)
    base_score = rng.uniform(0.1, 0.95, size=300)
    distance_score = rng.uniform(0.0, 1.0, size=300)
    semantic_score = rng.uniform(0.2, 0.95, size=300)
    features = np.column_stack([base_score, distance_score, semantic_score])
    target = (0.55 * base_score) + (0.25 * distance_score) + (0.2 * semantic_score)

    model = RandomForestRegressor(n_estimators=30, random_state=42, max_depth=4)
    model.fit(features, target)

    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODELS_DIR / "ranker.pkl")
    (MODELS_DIR / "ranker_metadata.json").write_text(
      json.dumps(
          {
              "trained_at": datetime.now(UTC).isoformat(),
              "feature_order": ["base_score", "distance_score", "semantic_score"],
              "source": "synthetic optional demo data"
          },
          indent=2
      ),
      encoding="utf-8"
    )
    print("Wrote models/ranker.pkl and models/ranker_metadata.json")


if __name__ == "__main__":
    main()
