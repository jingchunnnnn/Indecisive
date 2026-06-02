"""Load lightweight ML artifacts for inference-only ranking."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True)
class EmbeddingArtifacts:
    terms: list[str]
    embeddings: np.ndarray


class ArtifactLoader:
    def __init__(self, artifact_dir: Path):
        self.artifact_dir = artifact_dir

    def load_food_embeddings(self) -> EmbeddingArtifacts | None:
        concepts_path = self.artifact_dir / "food_concepts.json"
        embeddings_path = self.artifact_dir / "food_concept_embeddings.npz"
        if not concepts_path.exists() or not embeddings_path.exists():
            return None

        try:
            concepts_payload = json.loads(concepts_path.read_text(encoding="utf-8"))
            with np.load(embeddings_path, allow_pickle=False) as payload:
                embeddings = np.asarray(payload["embeddings"], dtype=float)
                if "terms" in payload.files:
                    terms = [str(item) for item in payload["terms"].tolist()]
                else:
                    terms = self._terms_from_concepts(concepts_payload)
        except (OSError, KeyError, ValueError, json.JSONDecodeError):
            return None

        if embeddings.ndim != 2 or len(terms) != embeddings.shape[0]:
            return None
        return EmbeddingArtifacts(terms=terms, embeddings=embeddings)

    def _terms_from_concepts(self, payload: Any) -> list[str]:
        if isinstance(payload, dict):
            payload = payload.get("concepts", [])
        terms: list[str] = []
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, str):
                    terms.append(item)
                elif isinstance(item, dict) and item.get("term"):
                    terms.append(str(item["term"]))
        return terms
