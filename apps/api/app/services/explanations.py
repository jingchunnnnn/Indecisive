"""Deterministic recommendation explanations."""

from __future__ import annotations

from app.services.providers import PlaceCandidate


def build_reason(
    *,
    place: PlaceCandidate,
    moods: list[str],
    positive_terms: list[str],
    semantic_score: float | None,
    distance_m: float | None,
    radius_m: int,
) -> str:
    pieces: list[str] = []

    place_text = " ".join([place.name, place.primary_type or "", *place.types]).lower().replace("_", " ")
    if semantic_score is not None and semantic_score >= 0.62:
        pieces.append("semantically matches your craving")
    elif moods:
        pieces.append(f"fits your {' and '.join(moods[:2])} mood")
    else:
        pieces.append("is a good nearby fallback option")

    matched_focus = _matched_focus(place_text, positive_terms, place)
    if matched_focus:
        pieces.append(matched_focus)

    if distance_m is not None and distance_m <= radius_m:
        pieces.append("is within your selected distance")
    elif distance_m is not None:
        pieces.append("is a bit farther away but still relevant")

    return "Recommended because it " + ", ".join(pieces) + "."


def _matched_focus(place_text: str, positive_terms: list[str], place: PlaceCandidate) -> str | None:
    for term in positive_terms:
        normalized = term.replace("_", " ").lower()
        if normalized in place_text:
            if "dessert" in normalized or "ice cream" in normalized or "bingsu" in normalized:
                return "matches dessert-related terms"
            if "cafe" in normalized or "coffee" in normalized:
                return "matches cafe-related terms nearby"
            if "spicy" in normalized or "mala" in normalized or "sichuan" in normalized:
                return "matches spicy terms"
            if "healthy" in normalized or "salad" in normalized or "juice" in normalized:
                return "matches lighter food terms"
            return f"matches {normalized}-related terms"

    if place.primary_type:
        return f"matches {place.primary_type.replace('_', ' ')}-related terms"
    return None
