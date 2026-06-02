import json

from app.schemas.requests import FeedbackRequest, LocationRequest, RecommendRequest, SurveyRequest
from app.services.feedback_logger import FeedbackLogger


def test_feedback_logger_appends_training_event(tmp_path):
    path = tmp_path / "feedback.jsonl"
    payload = FeedbackRequest(
        place_id="place_123",
        action="liked",
        types=["restaurant", "japanese_restaurant"],
        rank=1,
        score=0.91,
        distance_m=320.0,
        reason="Recommended because it matches your cuisine pick.",
        request=RecommendRequest(
            survey=SurveyRequest(moods=["comforting"], cuisines=["japanese"], place_types=["restaurant"]),
            remarks="ramen please",
            location=LocationRequest(lat=1.3, lng=103.8),
        ),
    )

    FeedbackLogger(path).append(payload)

    rows = path.read_text(encoding="utf-8").splitlines()
    assert len(rows) == 1
    event = json.loads(rows[0])
    assert event["place_id"] == "place_123"
    assert event["action"] == "liked"
    assert event["request"]["survey"]["cuisines"] == ["japanese"]
    assert event["distance_m"] == 320.0
    assert event["logged_at"]
