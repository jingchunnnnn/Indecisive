"""Deterministic craving parser. No LLMs in the MVP path."""

from __future__ import annotations

import re
from dataclasses import dataclass

from recommender.query_expansion import build_search_query, remove_negative_terms, unique_terms
from recommender.taxonomy import (
    CONSTRAINT_TO_TERMS,
    CUISINE_TO_TERMS,
    MOOD_TO_TERMS,
    NEGATIVE_HINTS,
    PLACE_TYPE_TO_TERMS,
    REMARK_KEYWORDS,
    all_known_terms,
)


@dataclass(frozen=True)
class ParsedCraving:
    moods: list[str]
    cuisines: list[str]
    cuisine_terms: list[str]
    positive_terms: list[str]
    negative_terms: list[str]
    search_query: str


def _extract_remark_terms(remarks: str) -> list[str]:
    text = remarks.lower()
    terms: list[str] = []
    for keyword, expansions in REMARK_KEYWORDS.items():
        if keyword in text:
            terms.extend(expansions)
    terms.extend(_extract_known_food_terms(remarks))
    return terms


def _extract_known_food_terms(remarks: str) -> list[str]:
    text = f" {remarks.lower()} "
    ignored_terms = {"food", "restaurant", "cafe"}
    terms: list[str] = []

    for term in all_known_terms():
        normalized = term.lower()
        if normalized in ignored_terms:
            continue
        escaped = re.escape(normalized)
        if re.search(rf"(?<!\w){escaped}(?!\w)", text):
            terms.append(normalized)
    return terms


def _extract_negative_terms(remarks: str) -> list[str]:
    text = f" {remarks.lower()} "
    negatives: list[str] = []
    known_terms = [*all_known_terms(), "oily", "greasy"]

    for term in known_terms:
        escaped = re.escape(term)
        for hint in NEGATIVE_HINTS:
            pattern = rf"\b{hint}\s+(?:any\s+|too\s+|too\s+much\s+|more\s+)?{escaped}\b"
            if re.search(pattern, text):
                negatives.append(term)
                break

    # Common phrasing: "not bubble tea", "not bbt", and "no boba".
    alias_map = {
        "bbt": "bubble tea",
        "boba": "bubble tea",
        "milk tea": "bubble tea",
    }
    for alias, canonical in alias_map.items():
        for hint in NEGATIVE_HINTS:
            if re.search(rf"\b{hint}\s+{re.escape(alias)}\b", text):
                negatives.append(canonical)
    return unique_terms(negatives)


def parse_craving(
    moods: list[str],
    cuisines: list[str],
    place_types: list[str],
    constraints: list[str],
    remarks: str,
    disliked_terms: list[str] | None = None,
) -> ParsedCraving:
    known_moods = [mood for mood in moods if mood in MOOD_TO_TERMS]
    known_cuisines = [cuisine for cuisine in cuisines if cuisine in CUISINE_TO_TERMS]
    known_place_types = [place_type for place_type in place_types if place_type in PLACE_TYPE_TO_TERMS]
    known_constraints = [constraint for constraint in constraints if constraint in CONSTRAINT_TO_TERMS]

    cuisine_terms: list[str] = []
    for cuisine in known_cuisines:
        cuisine_terms.extend(CUISINE_TO_TERMS[cuisine])

    positive_terms: list[str] = []
    positive_terms.extend([term for term in cuisine_terms if term not in known_cuisines])
    for mood in known_moods:
        positive_terms.extend(MOOD_TO_TERMS[mood])
    for place_type in known_place_types:
        positive_terms.extend(PLACE_TYPE_TO_TERMS[place_type])
    for constraint in known_constraints:
        positive_terms.extend(CONSTRAINT_TO_TERMS[constraint])
    positive_terms.extend(_extract_remark_terms(remarks))

    negative_terms = unique_terms([*(disliked_terms or []), *_extract_negative_terms(remarks)])
    positive_terms = remove_negative_terms(positive_terms, negative_terms)
    search_query = build_search_query(positive_terms, negative_terms)

    return ParsedCraving(
        moods=known_moods,
        cuisines=known_cuisines,
        cuisine_terms=unique_terms(cuisine_terms),
        positive_terms=positive_terms,
        negative_terms=negative_terms,
        search_query=search_query,
    )
