import json

import numpy as np

from app.core.config import Settings
from app.schemas.requests import UserPreferencesRequest
from app.services.artifact_loader import ArtifactLoader
from app.services.providers import PlaceCandidate
from app.services.ranker import RecommendationRanker
from app.services.semantic_ranker import SemanticRanker


def write_artifacts(path):
    concepts = {
        "concepts": [
            {"term": "ice cream"},
            {"term": "cake"},
            {"term": "ramen"},
            {"term": "mala"},
            {"term": "bubble tea"},
        ]
    }
    (path / "food_concepts.json").write_text(json.dumps(concepts), encoding="utf-8")
    np.savez(
        path / "food_concept_embeddings.npz",
        terms=np.array(["ice cream", "cake", "ramen", "mala", "bubble tea"]),
        embeddings=np.array(
            [
                [1.0, 0.0, 0.0],
                [0.9, 0.1, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.95, 0.05, 0.0],
            ]
        ),
    )


def test_semantic_ranker_loads_small_test_artifacts(tmp_path):
    write_artifacts(tmp_path)
    ranker = SemanticRanker(ArtifactLoader(tmp_path))

    assert ranker.available


def test_missing_artifacts_fallback_gracefully(tmp_path):
    ranker = SemanticRanker(ArtifactLoader(tmp_path))

    assert not ranker.available
    assert ranker.score(["ice cream"], [], "ice cream cafe") == ranker.neutral_score


def test_sweet_cold_craving_scores_ice_cream_above_ramen(tmp_path):
    write_artifacts(tmp_path)
    ranker = SemanticRanker(ArtifactLoader(tmp_path))

    ice = ranker.score(["ice cream", "cake"], [], "ice cream dessert cafe")
    ramen = ranker.score(["ice cream", "cake"], [], "ramen soup")

    assert ice > ramen


def test_spicy_craving_scores_mala_above_cake(tmp_path):
    write_artifacts(tmp_path)
    ranker = SemanticRanker(ArtifactLoader(tmp_path))

    mala = ranker.score(["mala"], [], "mala spicy sichuan")
    cake = ranker.score(["mala"], [], "cake dessert")

    assert mala > cake


def test_negative_bubble_tea_penalizes_candidate(tmp_path):
    write_artifacts(tmp_path)
    ranker = SemanticRanker(ArtifactLoader(tmp_path))

    plain = ranker.score(["ice cream"], [], "bubble tea dessert")
    penalized = ranker.score(["ice cream"], ["bubble tea"], "bubble tea dessert")

    assert penalized < plain


def test_neutral_score_when_candidate_has_no_matching_concepts(tmp_path):
    write_artifacts(tmp_path)
    ranker = SemanticRanker(ArtifactLoader(tmp_path))

    assert ranker.score(["ice cream"], [], "sandwich shop") == ranker.neutral_score


def test_final_ranker_uses_semantic_score_when_enabled(tmp_path):
    write_artifacts(tmp_path)
    settings = Settings(
        MODEL_ARTIFACT_DIR=str(tmp_path),
        ENABLE_SEMANTIC_RANKING=True,
        ENABLE_TRAINED_RANKER=False,
    )
    candidates = [
        PlaceCandidate("ramen", None, "Ramen House", None, 1.3001, 103.8001, ["ramen"]),
        PlaceCandidate("ice", None, "Ice Cream Cafe", None, 1.3001, 103.8001, ["ice_cream_shop"]),
    ]

    ranked = RecommendationRanker(settings).rank(
        candidates=candidates,
        positive_terms=["ice cream"],
        negative_terms=[],
        moods=["sweet"],
        request_lat=1.3,
        request_lng=103.8,
        radius_m=2000,
        user_preferences=UserPreferencesRequest(),
    )

    assert ranked[0].place.place_id == "ice"
    assert ranked[0].semantic_score is not None
