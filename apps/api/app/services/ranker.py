"""Rule-based ranker with optional semantic and trained-ranker inference."""

from __future__ import annotations

from dataclasses import dataclass

from app.core.config import Settings
from app.schemas.requests import UserPreferencesRequest
from app.services.artifact_loader import ArtifactLoader
from app.services.explanations import build_reason
from app.services.providers import PlaceCandidate
from app.services.semantic_ranker import SemanticRanker
from app.services.trained_ranker import TrainedRanker
from recommender.distance import haversine_distance_m
from recommender.query_expansion import unique_terms
from recommender.scoring import distance_score, negative_penalty, term_match_score, text_blob


@dataclass(frozen=True)
class ScoredPlace:
    place: PlaceCandidate
    score: float
    reason: str
    distance_m: float | None
    semantic_score: float | None


class RecommendationRanker:
    def __init__(self, settings: Settings):
        loader = ArtifactLoader(settings.artifact_path)
        self.semantic_ranker = (
            SemanticRanker(loader) if settings.enable_semantic_ranking else SemanticRanker(None)
        )
        self.trained_ranker = TrainedRanker(settings.artifact_path, settings.enable_trained_ranker)

    def rank(
        self,
        *,
        candidates: list[PlaceCandidate],
        positive_terms: list[str],
        negative_terms: list[str],
        moods: list[str],
        request_lat: float,
        request_lng: float,
        radius_m: int,
        user_preferences: UserPreferencesRequest,
        cuisine_terms: list[str] | None = None,
    ) -> list[ScoredPlace]:
        scored: list[ScoredPlace] = []
        for candidate in candidates:
            distance_m = self._distance(candidate, request_lat, request_lng)
            if distance_m is not None and distance_m > radius_m:
                continue

            candidate_text = text_blob(
                candidate.name,
                candidate.address,
                candidate.primary_type,
                [item.replace("_", " ") for item in candidate.types],
            )

            semantic_score = (
                self.semantic_ranker.score(positive_terms, negative_terms, candidate_text)
                if self.semantic_ranker.available
                else None
            )
            score = self._rule_score(
                candidate=candidate,
                candidate_text=candidate_text,
                positive_terms=positive_terms,
                cuisine_terms=cuisine_terms or [],
                negative_terms=negative_terms,
                distance_m=distance_m,
                radius_m=radius_m,
                user_preferences=user_preferences,
                semantic_score=semantic_score,
            )
            trained_score = self.trained_ranker.predict_score(
                self._features(score, distance_m, radius_m, semantic_score)
            )
            if trained_score is not None:
                score = (score * 0.65) + (max(0.0, min(1.0, trained_score)) * 0.35)

            reason = build_reason(
                place=candidate,
                moods=moods,
                positive_terms=positive_terms,
                cuisine_terms=cuisine_terms or [],
                semantic_score=semantic_score,
                distance_m=distance_m,
                radius_m=radius_m,
            )
            scored.append(
                ScoredPlace(
                    place=candidate,
                    score=round(max(0.0, min(1.0, score)), 4),
                    reason=reason,
                    distance_m=round(distance_m, 1) if distance_m is not None else None,
                    semantic_score=semantic_score,
                )
            )

        return sorted(scored, key=lambda item: item.score, reverse=True)[:8]

    def _rule_score(
        self,
        *,
        candidate: PlaceCandidate,
        candidate_text: str,
        positive_terms: list[str],
        cuisine_terms: list[str],
        negative_terms: list[str],
        distance_m: float | None,
        radius_m: int,
        user_preferences: UserPreferencesRequest,
        semantic_score: float | None,
    ) -> float:
        keyword_score = term_match_score(positive_terms, candidate_text)
        cuisine_score = self._cuisine_score(cuisine_terms, candidate_text)
        proximity_score = distance_score(distance_m, radius_m)
        preference_score = self._preference_score(candidate, user_preferences)
        score = 0.2 + (0.42 * keyword_score) + (0.28 * proximity_score) + preference_score
        if cuisine_terms:
            score += 0.26 * cuisine_score
            if cuisine_score == 0:
                score -= 0.22

        if semantic_score is not None:
            score += (semantic_score - 0.5) * 0.28

        score -= negative_penalty(negative_terms, candidate_text)
        score += self._place_id_preference(candidate, user_preferences)
        return score

    def _cuisine_score(self, cuisine_terms: list[str], candidate_text: str) -> float:
        terms = unique_terms(cuisine_terms)
        if not terms:
            return 0.0
        for term in terms:
            if term in candidate_text:
                return 1.0
        for term in terms:
            words = [word for word in term.split() if len(word) > 3 and word != "food"]
            if any(word in candidate_text for word in words):
                return 0.45
        return 0.0

    def _preference_score(self, candidate: PlaceCandidate, prefs: UserPreferencesRequest) -> float:
        candidate_types = {item.lower() for item in candidate.types}
        liked_types = {item.lower() for item in prefs.liked_types}
        disliked_types = {item.lower() for item in prefs.disliked_types}
        score = 0.0
        if candidate_types & liked_types:
            score += 0.12
        if candidate_types & disliked_types:
            score -= 0.18
        return score

    def _place_id_preference(self, candidate: PlaceCandidate, prefs: UserPreferencesRequest) -> float:
        if candidate.place_id in prefs.disliked_place_ids:
            return -0.5
        if candidate.place_id in prefs.liked_place_ids:
            return 0.15
        return 0.0

    def _distance(self, candidate: PlaceCandidate, request_lat: float, request_lng: float) -> float | None:
        if candidate.lat is None or candidate.lng is None:
            return None
        return haversine_distance_m(request_lat, request_lng, candidate.lat, candidate.lng)

    def _features(
        self,
        score: float,
        distance_m: float | None,
        radius_m: int,
        semantic_score: float | None,
    ) -> list[float]:
        return [
            score,
            distance_score(distance_m, radius_m),
            semantic_score if semantic_score is not None else 0.5,
        ]
