from app.services.query_builder import build_search_query, remove_negative_terms, unique_terms


def test_deduplicates_terms():
    assert unique_terms(["Cake", " cake ", "ice cream"]) == ["cake", "ice cream"]


def test_removes_negative_terms():
    assert remove_negative_terms(["dessert", "bubble tea"], ["bubble tea"]) == ["dessert"]


def test_falls_back_to_food():
    assert build_search_query([], []) == "food"


def test_produces_non_empty_search_query():
    assert build_search_query(["dessert", "ice cream"], []) == "dessert ice cream"
