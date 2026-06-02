"""Distance utilities."""

from __future__ import annotations

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_M = 6_371_000


def haversine_distance_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Return great-circle distance in meters."""

    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    rlat1 = radians(lat1)
    rlat2 = radians(lat2)
    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_M * c
