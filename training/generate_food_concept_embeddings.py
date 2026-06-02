"""Generate small local food concept embeddings.

Run from the repo root after installing training requirements:

    python training/generate_food_concept_embeddings.py
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
CONCEPTS_PATH = MODELS_DIR / "food_concepts.json"
OUTPUT_PATH = MODELS_DIR / "food_concept_embeddings.npz"
METADATA_PATH = MODELS_DIR / "embedding_metadata.json"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main() -> None:
    payload = json.loads(CONCEPTS_PATH.read_text(encoding="utf-8"))
    concepts = payload["concepts"]
    terms = [item["term"] for item in concepts]
    texts = [f"{item['term']}: {item.get('description', item['term'])}" for item in concepts]

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, normalize_embeddings=True)
    np.savez(OUTPUT_PATH, terms=np.array(terms), embeddings=np.asarray(embeddings, dtype=np.float32))
    METADATA_PATH.write_text(
        json.dumps(
            {
                "model": MODEL_NAME,
                "generated_at": datetime.now(UTC).isoformat(),
                "concept_count": len(terms),
                "embedding_dimensions": int(np.asarray(embeddings).shape[1]),
                "normalized": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {len(terms)} concepts.")
    print(f"Wrote {METADATA_PATH.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
