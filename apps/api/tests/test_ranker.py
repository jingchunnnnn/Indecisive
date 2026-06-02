from app.core.config import Settings
from app.schemas.requests import UserPreferencesRequest
from app.services.providers import PlaceCandidate
from app.services.ranker import RecommendationRanker


def rank(candidates, positive_terms=None, negative_terms=None, prefs=None):
    settings = Settings(ENABLE_SEMANTIC_RANKING=False, ENABLE_TRAINED_RANKER=False)
    return RecommendationRanker(settings).rank(
        candidates=candidates,
        positive_terms=positive_terms or ["dessert"],
        negative_terms=negative_terms or [],
        moods=["sweet"],
        request_lat=1.3,
        request_lng=103.8,
        radius_m=2000,
        user_preferences=prefs or UserPreferencesRequest(),
    )


def test_nearby_candidate_scores_higher_than_far_candidate():
    candidates = [
        PlaceCandidate("near", None, "Dessert Near", None, 1.3005, 103.8005, ["dessert"]),
        PlaceCandidate("far", None, "Dessert Far", None, 1.35, 103.85, ["dessert"]),
    ]

    ranked = rank(candidates)

    assert ranked[0].place.place_id == "near"


def test_dessert_candidate_ranks_high_for_sweet_dessert_query():
    candidates = [
        PlaceCandidate("ramen", None, "Ramen Bowl", None, 1.3001, 103.8001, ["restaurant"]),
        PlaceCandidate("cake", None, "Tiny Cake Cafe", None, 1.3002, 103.8002, ["dessert", "cafe"]),
    ]

    ranked = rank(candidates, ["dessert", "cake", "ice cream"])

    assert ranked[0].place.place_id == "cake"


def test_bubble_tea_candidate_is_penalized_when_negative():
    candidates = [
        PlaceCandidate("boba", None, "Bubble Tea Corner", None, 1.3001, 103.8001, ["bubble_tea", "dessert"]),
        PlaceCandidate("cake", None, "Cake Cafe", None, 1.3003, 103.8003, ["dessert"]),
    ]

    ranked = rank(candidates, ["dessert", "bubble tea"], ["bubble tea"])

    assert ranked[0].place.place_id == "cake"


def test_disliked_place_id_is_penalized():
    prefs = UserPreferencesRequest(disliked_place_ids=["cake"])
    candidates = [
        PlaceCandidate("cake", None, "Cake Cafe", None, 1.3001, 103.8001, ["dessert"]),
        PlaceCandidate("other", None, "Dessert Bar", None, 1.3002, 103.8002, ["dessert"]),
    ]

    ranked = rank(candidates, ["dessert", "cake"], prefs=prefs)

    assert ranked[0].place.place_id == "other"


def test_liked_types_increase_score():
    prefs = UserPreferencesRequest(liked_types=["cafe"])
    candidates = [
        PlaceCandidate("cafe", None, "Cafe Cake", None, 1.3001, 103.8001, ["cafe", "dessert"]),
        PlaceCandidate("stall", None, "Dessert Stall", None, 1.3001, 103.8001, ["dessert"]),
    ]

    ranked = rank(candidates, ["dessert"], prefs=prefs)

    assert ranked[0].place.place_id == "cafe"


def test_selected_cuisine_is_stricter_than_generic_mood_match():
    settings = Settings(ENABLE_SEMANTIC_RANKING=False, ENABLE_TRAINED_RANKER=False)
    candidates = [
        PlaceCandidate("dessert", None, "Sweet Dessert Cafe", None, 1.3001, 103.8001, ["dessert", "cafe"]),
        PlaceCandidate("sushi", None, "Sushi Table", None, 1.3001, 103.8001, ["restaurant"]),
    ]

    ranked = RecommendationRanker(settings).rank(
        candidates=candidates,
        positive_terms=["japanese", "japanese food", "sushi", "sweet", "dessert", "cake"],
        negative_terms=[],
        moods=["sweet"],
        request_lat=1.3,
        request_lng=103.8,
        radius_m=2000,
        user_preferences=UserPreferencesRequest(),
        cuisine_terms=["japanese", "japanese food", "sushi"],
    )

    assert ranked[0].place.place_id == "sushi"
