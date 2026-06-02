"""Backend wrapper around shared query expansion helpers."""

from __future__ import annotations

from recommender.query_expansion import build_search_query, remove_negative_terms, unique_terms

__all__ = ["build_search_query", "remove_negative_terms", "unique_terms"]
