from fastapi import HTTPException

from app.core.config import Settings
from app.routes.recommend import get_places_provider


def test_missing_google_api_key_returns_service_unavailable():
    settings = Settings(GOOGLE_PLACES_API_KEY=None)

    try:
        get_places_provider(settings)
    except HTTPException as exc:
        assert exc.status_code == 503
        assert "Google Places API key is not configured" in exc.detail
    else:
        raise AssertionError("Expected missing API key to raise HTTPException")
