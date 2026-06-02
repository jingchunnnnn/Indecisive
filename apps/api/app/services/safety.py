"""Small validation helpers used outside Pydantic-bound endpoints."""

from __future__ import annotations


def validate_lat_lng(lat: float, lng: float) -> None:
    if lat < -90 or lat > 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if lng < -180 or lng > 180:
        raise ValueError("Longitude must be between -180 and 180.")


def validate_radius(radius_m: int) -> int:
    if radius_m < 100:
        raise ValueError("Radius must be at least 100 meters.")
    if radius_m > 50000:
        raise ValueError("Radius must be 50000 meters or less.")
    return radius_m


def trim_remarks(remarks: str, max_length: int = 300) -> str:
    return remarks.strip()[:max_length]
