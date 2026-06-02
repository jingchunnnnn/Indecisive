"""Place details endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import Settings, get_settings
from app.routes.recommend import get_places_provider
from app.schemas.responses import PlaceDetailsResponse
from app.services.providers import PlacesProviderError

router = APIRouter()


@router.get("/places/{place_id}", response_model=PlaceDetailsResponse)
async def place_details(
    place_id: str,
    settings: Settings = Depends(get_settings),
) -> PlaceDetailsResponse:
    provider = get_places_provider(settings)
    try:
        place = await provider.details(place_id)
    except PlacesProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    if place is None:
        raise HTTPException(status_code=404, detail="Place details are not available.")

    return PlaceDetailsResponse(
        place_id=place.place_id,
        resource_name=place.resource_name,
        name=place.name,
        address=place.address,
        lat=place.lat,
        lng=place.lng,
        types=place.types,
        primary_type=place.primary_type,
        google_maps_uri=place.google_maps_uri,
    )
