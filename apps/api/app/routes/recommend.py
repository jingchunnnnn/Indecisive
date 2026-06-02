"""Recommendation and feedback endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import Settings, get_settings
from app.schemas.requests import FeedbackRequest, RecommendRequest
from app.schemas.responses import InterpretedCraving, Recommendation, RecommendResponse, StatusResponse
from app.services.craving_parser import parse_craving
from app.services.google_places import GooglePlacesProvider
from app.services.providers import PlacesProvider, PlacesProviderError
from app.services.ranker import RecommendationRanker

router = APIRouter()


def get_places_provider(settings: Settings) -> PlacesProvider:
    if settings.google_places_api_key:
        return GooglePlacesProvider(settings)
    raise HTTPException(
        status_code=503,
        detail="Food search is temporarily unavailable because the Google Places API key is not configured.",
    )


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(
    request: RecommendRequest,
    settings: Settings = Depends(get_settings),
) -> RecommendResponse:
    parsed = parse_craving(
        moods=request.survey.moods,
        place_types=request.survey.place_types,
        constraints=request.survey.constraints,
        remarks=request.remarks,
        disliked_terms=request.user_preferences.disliked_terms,
    )

    provider = get_places_provider(settings)
    try:
        places = await provider.search(
            query=parsed.search_query,
            lat=request.location.lat,
            lng=request.location.lng,
            radius_m=request.survey.radius_m,
            open_now="open_now" in request.survey.constraints,
        )
    except PlacesProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    ranker = RecommendationRanker(settings)
    scored_places = ranker.rank(
        candidates=places,
        positive_terms=parsed.positive_terms,
        negative_terms=parsed.negative_terms,
        moods=parsed.moods,
        request_lat=request.location.lat,
        request_lng=request.location.lng,
        radius_m=request.survey.radius_m,
        user_preferences=request.user_preferences,
    )

    return RecommendResponse(
        interpreted_craving=InterpretedCraving(
            moods=parsed.moods,
            positive_terms=parsed.positive_terms,
            negative_terms=parsed.negative_terms,
            search_query=parsed.search_query,
        ),
        recommendations=[
            Recommendation(
                place_id=item.place.place_id,
                resource_name=item.place.resource_name,
                name=item.place.name,
                address=item.place.address,
                lat=item.place.lat,
                lng=item.place.lng,
                distance_m=item.distance_m,
                types=item.place.types,
                primary_type=item.place.primary_type,
                google_maps_uri=item.place.google_maps_uri,
                score=item.score,
                reason=item.reason,
            )
            for item in scored_places
            if item.place.place_id
        ],
    )


@router.post("/feedback", response_model=StatusResponse)
async def feedback(payload: FeedbackRequest) -> StatusResponse:
    return StatusResponse(status="ok")
