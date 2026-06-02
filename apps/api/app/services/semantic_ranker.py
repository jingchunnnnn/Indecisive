"""Small artifact-based semantic scoring."""

from __future__ import annotations

import numpy as np

from app.services.artifact_loader import ArtifactLoader, EmbeddingArtifacts
from recommender.query_expansion import unique_terms
from recommender.scoring import negative_penalty


class SemanticRanker:
    neutral_score = 0.5

    def __init__(self, loader: ArtifactLoader | None):
        self.artifacts: EmbeddingArtifacts | None = loader.load_food_embeddings() if loader else None
        self._term_to_index = {
            term.lower(): index for index, term in enumerate(self.artifacts.terms)
        } if self.artifacts else {}

    @property
    def available(self) -> bool:
        return self.artifacts is not None

    def score(self, positive_terms: list[str], negative_terms: list[str], candidate_text: str) -> float:
        if not self.artifacts:
            return self.neutral_score

        query_vector = self._average_vector(positive_terms)
        candidate_terms = [term for term in self.artifacts.terms if term.lower() in candidate_text]
        candidate_vector = self._average_vector(candidate_terms)
        if query_vector is None or candidate_vector is None:
            return self.neutral_score

        similarity = self._cosine(query_vector, candidate_vector)
        normalized = (similarity + 1.0) / 2.0
        return float(max(0.0, min(1.0, normalized - negative_penalty(negative_terms, candidate_text))))

    def _average_vector(self, terms: list[str]) -> np.ndarray | None:
        if not self.artifacts:
            return None

        vectors: list[np.ndarray] = []
        for term in unique_terms(terms):
            index = self._term_to_index.get(term.lower())
            if index is not None:
                vectors.append(self.artifacts.embeddings[index])
        if not vectors:
            return None
        return np.mean(np.stack(vectors), axis=0)

    def _cosine(self, left: np.ndarray, right: np.ndarray) -> float:
        denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
        if denominator == 0:
            return 0.0
        return float(np.dot(left, right) / denominator)
