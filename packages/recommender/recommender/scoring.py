"""Deterministic scoring primitives."""

from __future__ import annotations

from .query_expansion import normalize_term, unique_terms


def text_blob(*parts: object) -> str:
    values: list[str] = []
    for part in parts:
        if part is None:
            continue
        if isinstance(part, list):
            values.extend(str(item) for item in part)
        else:
            values.append(str(part))
    return normalize_term(" ".join(values))


def term_match_score(terms: list[str], text: str) -> float:
    normalized_terms = unique_terms(terms)
    if not normalized_terms:
        return 0.0

    hits = 0.0
    for term in normalized_terms:
        if term in text:
            hits += 1.0
            continue
        words = term.split()
        if len(words) > 1 and any(word in text for word in words):
            hits += 0.35
    return min(1.0, hits / max(1, min(6, len(normalized_terms))))


def negative_penalty(negative_terms: list[str], text: str) -> float:
    penalty = 0.0
    for term in unique_terms(negative_terms):
        if term in text:
            penalty += 0.25
    return min(0.7, penalty)


def distance_score(distance_m: float | None, radius_m: int) -> float:
    if distance_m is None:
        return 0.25
    if radius_m <= 0:
        return 0.0
    return max(0.0, 1.0 - min(distance_m / radius_m, 1.0))
