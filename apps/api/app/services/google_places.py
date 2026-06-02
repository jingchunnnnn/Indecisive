"""Google Places API New provider."""

from __future__ import annotations

import httpx

from app.core.config import Settings
from app.services.providers import PlaceCandidate, PlacesProviderError

TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
DETAILS_URL = "https://places.googleapis.com/v1/places/{place_id}"

TEXT_SEARCH_FIELD_MASK = (
    "places.id,places.name,places.displayName,places.formattedAddress,"
    "places.location,places.types,places.primaryType,places.googleMapsUri"
)

DETAILS_FIELD_MASK = "id,displayName,formattedAddress,location,types,primaryType,googleMapsUri"


class GooglePlacesProvider:
    def __init__(self, settings: Settings):
        if not settings.google_places_api_key:
            raise ValueError("Google Places API key is required.")
        self.api_key = settings.google_places_api_key
        self.timeout_s = settings.google_timeout_s

    async def search(
        self,
        *,
        query: str,
        lat: float,
        lng: float,
        radius_m: int,
        open_now: bool = False,
    ) -> list[PlaceCandidate]:
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": TEXT_SEARCH_FIELD_MASK,
        }
        body: dict[str, object] = {
            "textQuery": query or "food",
            "locationBias": {
                "circle": {
                    "center": {"latitude": lat, "longitude": lng},
                    "radius": float(radius_m),
                }
            },
        }
        if open_now:
            body["openNow"] = True

        try:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                response = await client.post(TEXT_SEARCH_URL, json=body, headers=headers)
        except httpx.TimeoutException as exc:
            raise PlacesProviderError("Google Places timed out. Please try again.") from exc
        except httpx.HTTPError as exc:
            raise PlacesProviderError("Google Places could not be reached.") from exc

        if response.status_code >= 400:
            raise PlacesProviderError("Google Places returned an error for this search.")

        payload = response.json()
        return [self._parse_place(place) for place in payload.get("places", [])]

    async def details(self, place_id: str) -> PlaceCandidate | None:
        headers = {
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": DETAILS_FIELD_MASK,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                response = await client.get(DETAILS_URL.format(place_id=place_id), headers=headers)
        except httpx.TimeoutException as exc:
            raise PlacesProviderError("Google Place Details timed out. Please try again.") from exc
        except httpx.HTTPError as exc:
            raise PlacesProviderError("Google Place Details could not be reached.") from exc

        if response.status_code == 404:
            return None
        if response.status_code >= 400:
            raise PlacesProviderError("Google Place Details returned an error.")
        return self._parse_place(response.json())

    def _parse_place(self, place: dict[str, object]) -> PlaceCandidate:
        display_name = place.get("displayName")
        if isinstance(display_name, dict):
            name = str(display_name.get("text") or "Unnamed place")
        else:
            name = "Unnamed place"

        location = place.get("location") if isinstance(place.get("location"), dict) else {}
        lat = location.get("latitude") if isinstance(location, dict) else None
        lng = location.get("longitude") if isinstance(location, dict) else None

        types = place.get("types")
        parsed_types = [str(item) for item in types] if isinstance(types, list) else []

        place_id = str(place.get("id") or "")
        return PlaceCandidate(
            place_id=place_id,
            resource_name=str(place.get("name")) if place.get("name") else None,
            name=name,
            address=str(place.get("formattedAddress")) if place.get("formattedAddress") else None,
            lat=float(lat) if lat is not None else None,
            lng=float(lng) if lng is not None else None,
            types=parsed_types,
            primary_type=str(place.get("primaryType")) if place.get("primaryType") else None,
            google_maps_uri=str(place.get("googleMapsUri")) if place.get("googleMapsUri") else None,
        )
