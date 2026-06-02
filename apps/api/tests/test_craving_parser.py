from app.services.craving_parser import parse_craving


def test_sweet_refreshing_expands_to_dessert_and_cold_terms():
    parsed = parse_craving(["sweet", "refreshing"], [], [], [], "")

    assert "dessert" in parsed.positive_terms
    assert "ice cream" in parsed.positive_terms
    assert "bingsu" in parsed.positive_terms


def test_remarks_sweet_and_cold_adds_terms():
    parsed = parse_craving([], [], [], [], "something sweet and cold")

    assert "dessert" in parsed.positive_terms
    assert "ice cream" in parsed.positive_terms
    assert "bingsu" in parsed.positive_terms


def test_not_bubble_tea_is_negative():
    parsed = parse_craving(["sweet"], [], [], [], "something sweet and cold but not bubble tea")

    assert "bubble tea" in parsed.negative_terms


def test_negative_terms_are_removed_from_positive_terms():
    parsed = parse_craving(["sweet"], [], [], [], "not bubble tea")

    assert "bubble tea" in parsed.negative_terms
    assert "bubble tea" not in parsed.positive_terms


def test_unknown_survey_values_are_ignored():
    parsed = parse_craving(["space_noodles", "sweet"], ["moon_cuisine"], ["moon_cafe"], ["open_now"], "")

    assert parsed.moods == ["sweet"]
    assert "space_noodles" not in parsed.positive_terms


def test_cuisine_expands_to_search_terms():
    parsed = parse_craving([], ["japanese"], [], [], "")

    assert parsed.cuisines == ["japanese"]
    assert parsed.cuisine_terms[:2] == ["japanese", "japanese food"]
    assert "japanese food" in parsed.positive_terms
    assert "ramen" in parsed.positive_terms
    assert parsed.search_query.startswith("japanese food")


def test_remarks_extract_explicit_dish_and_cuisine_terms():
    parsed = parse_craving([], [], [], [], "i feel like sushi or donburi")

    assert "sushi" in parsed.positive_terms
    assert "donburi" in parsed.positive_terms
    assert "japanese food" in parsed.positive_terms


def test_remarks_not_oily_adds_light_terms_and_negative_oily():
    parsed = parse_craving([], [], [], [], "something cozy but not too oily, maybe noodles")

    assert "quiet cafe" in parsed.positive_terms
    assert "noodles" in parsed.positive_terms
    assert "oily" in parsed.negative_terms
    assert "oily" not in parsed.positive_terms
