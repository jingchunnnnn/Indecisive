from app.services.craving_parser import parse_craving


def test_sweet_refreshing_expands_to_dessert_and_cold_terms():
    parsed = parse_craving(["sweet", "refreshing"], [], [], "")

    assert "dessert" in parsed.positive_terms
    assert "ice cream" in parsed.positive_terms
    assert "bingsu" in parsed.positive_terms


def test_remarks_sweet_and_cold_adds_terms():
    parsed = parse_craving([], [], [], "something sweet and cold")

    assert "dessert" in parsed.positive_terms
    assert "ice cream" in parsed.positive_terms
    assert "bingsu" in parsed.positive_terms


def test_not_bubble_tea_is_negative():
    parsed = parse_craving(["sweet"], [], [], "something sweet and cold but not bubble tea")

    assert "bubble tea" in parsed.negative_terms


def test_negative_terms_are_removed_from_positive_terms():
    parsed = parse_craving(["sweet"], [], [], "not bubble tea")

    assert "bubble tea" in parsed.negative_terms
    assert "bubble tea" not in parsed.positive_terms


def test_unknown_survey_values_are_ignored():
    parsed = parse_craving(["space_noodles", "sweet"], ["moon_cafe"], ["open_now"], "")

    assert parsed.moods == ["sweet"]
    assert "space_noodles" not in parsed.positive_terms
