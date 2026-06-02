import asyncio

from app.services.providers import MockPlacesProvider
from recommender.distance import haversine_distance_m


def test_mock_provider_returns_deterministic_results():
    provider = MockPlacesProvider()

    first = asyncio.run(provider.search(query="dessert", lat=1.3, lng=103.8, radius_m=2000))
    second = asyncio.run(provider.search(query="dessert", lat=1.3, lng=103.8, radius_m=2000))

    assert first == second


def test_mock_provider_results_contain_required_fields():
    provider = MockPlacesProvider()
    results = asyncio.run(provider.search(query="dessert", lat=1.3, lng=103.8, radius_m=2000))

    place = results[0]
    assert place.place_id
    assert place.name
    assert place.lat is not None
    assert place.lng is not None
    assert place.types


def test_mock_provider_results_are_close_to_requested_location():
    provider = MockPlacesProvider()
    results = asyncio.run(provider.search(query="dessert", lat=1.3, lng=103.8, radius_m=2000))

    distances = [haversine_distance_m(1.3, 103.8, place.lat, place.lng) for place in results]
    assert max(distances) < 700
