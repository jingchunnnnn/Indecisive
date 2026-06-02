"""Query construction helpers."""

from __future__ import annotations


def normalize_term(term: str) -> str:
    return " ".join(term.strip().lower().split())


def unique_terms(terms: list[str]) -> list[str]:
    seen: set[str] = set()
    cleaned: list[str] = []
    for term in terms:
        normalized = normalize_term(term)
        if normalized and normalized not in seen:
            seen.add(normalized)
            cleaned.append(normalized)
    return cleaned


def remove_negative_terms(positive_terms: list[str], negative_terms: list[str]) -> list[str]:
    negatives = set(unique_terms(negative_terms))
    return [term for term in unique_terms(positive_terms) if term not in negatives]


def build_search_query(positive_terms: list[str], negative_terms: list[str] | None = None) -> str:
    terms = remove_negative_terms(positive_terms, negative_terms or [])
    if not terms:
        return "food"
    return " ".join(terms[:8])
