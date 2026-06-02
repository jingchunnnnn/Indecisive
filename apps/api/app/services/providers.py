"""Places provider abstraction and deterministic mock data."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class PlaceCandidate:
    place_id: str
    resource_name: str | None
    name: str
    address: str | None
    lat: float | None
    lng: float | None
    types: list[str] = field(default_factory=list)
    primary_type: str | None = None
    google_maps_uri: str | None = None


class PlacesProviderError(RuntimeError):
    """Raised when an upstream places provider fails."""


class PlacesProvider(Protocol):
    async def search(
        self,
        *,
        query: str,
        lat: float,
        lng: float,
        radius_m: int,
        open_now: bool = False,
    ) -> list[PlaceCandidate]:
        ...

    async def details(self, place_id: str) -> PlaceCandidate | None:
        ...


class MockPlacesProvider:
    """Deterministic, nearby demo provider used when no Google API key is set."""

    def _places(self, lat: float, lng: float) -> list[PlaceCandidate]:
        return [
            PlaceCandidate(
                place_id="mock_ice_cream_cafe",
                resource_name="places/mock_ice_cream_cafe",
                name="Scoop & Smile Ice Cream Cafe",
                address="12 Sundae Lane",
                lat=lat + 0.0022,
                lng=lng + 0.0018,
                types=["cafe", "dessert", "ice_cream_shop"],
                primary_type="cafe",
                google_maps_uri="https://maps.google.com/?q=Scoop%20%26%20Smile%20Ice%20Cream%20Cafe",
            ),
            PlaceCandidate(
                place_id="mock_bingsu_dessert",
                resource_name="places/mock_bingsu_dessert",
                name="Snowy Spoon Bingsu",
                address="4 Frost Street",
                lat=lat + 0.004,
                lng=lng - 0.001,
                types=["dessert", "cafe"],
                primary_type="dessert",
                google_maps_uri="https://maps.google.com/?q=Snowy%20Spoon%20Bingsu",
            ),
            PlaceCandidate(
                place_id="mock_mala_bowl",
                resource_name="places/mock_mala_bowl",
                name="Mala Warm Bowl",
                address="88 Pepper Walk",
                lat=lat - 0.003,
                lng=lng + 0.002,
                types=["restaurant", "spicy_food", "sichuan"],
                primary_type="restaurant",
                google_maps_uri="https://maps.google.com/?q=Mala%20Warm%20Bowl",
            ),
            PlaceCandidate(
                place_id="mock_quiet_chapter",
                resource_name="places/mock_quiet_chapter",
                name="Quiet Chapter Coffee",
                address="29 Study Nook",
                lat=lat + 0.001,
                lng=lng - 0.002,
                types=["cafe", "coffee", "study_friendly"],
                primary_type="cafe",
                google_maps_uri="https://maps.google.com/?q=Quiet%20Chapter%20Coffee",
            ),
            PlaceCandidate(
                place_id="mock_hawker_comfort",
                resource_name="places/mock_hawker_comfort",
                name="Happy Hawker Comfort Rice",
                address="51 Market Row",
                lat=lat - 0.0015,
                lng=lng - 0.0015,
                types=["hawker", "food_court", "rice_bowl"],
                primary_type="restaurant",
                google_maps_uri="https://maps.google.com/?q=Happy%20Hawker%20Comfort%20Rice",
            ),
            PlaceCandidate(
                place_id="mock_green_bowl",
                resource_name="places/mock_green_bowl",
                name="Green Bowl & Juice",
                address="7 Garden Arcade",
                lat=lat + 0.0028,
                lng=lng - 0.0028,
                types=["healthy_food", "salad", "juice_bar"],
                primary_type="restaurant",
                google_maps_uri="https://maps.google.com/?q=Green%20Bowl%20%26%20Juice",
            ),
            PlaceCandidate(
                place_id="mock_bubble_tea",
                resource_name="places/mock_bubble_tea",
                name="Bubbly Tea Corner",
                address="3 Pearl Plaza",
                lat=lat + 0.0008,
                lng=lng + 0.003,
                types=["bubble_tea", "dessert", "drink"],
                primary_type="cafe",
                google_maps_uri="https://maps.google.com/?q=Bubbly%20Tea%20Corner",
            ),
        ]

    async def search(
        self,
        *,
        query: str,
        lat: float,
        lng: float,
        radius_m: int,
        open_now: bool = False,
    ) -> list[PlaceCandidate]:
        return self._places(lat, lng)

    async def details(self, place_id: str) -> PlaceCandidate | None:
        for place in self._places(1.2966, 103.7764):
            if place.place_id == place_id:
                return place
        return None
