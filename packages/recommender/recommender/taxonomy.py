"""Food taxonomy used by the parser, query builder, and ranker."""

MOOD_TO_TERMS = {
    "sweet": ["dessert", "cake", "ice cream", "waffles", "bingsu", "bubble tea"],
    "spicy": ["mala", "thai food", "sichuan", "korean food", "curry", "mexican food"],
    "savory": ["rice bowl", "noodles", "burger", "pasta", "grill"],
    "light": ["salad", "sushi", "poke bowl", "sandwich", "soup"],
    "comforting": ["ramen", "soup", "porridge", "hotpot", "pasta", "rice bowl"],
    "refreshing": ["smoothie", "juice", "bingsu", "ice cream", "salad"],
    "filling": ["rice bowl", "burger", "noodles", "pasta", "hotpot"],
    "healthy": ["salad", "grain bowl", "poke bowl", "vegetarian", "soup"],
    "adventurous": ["fusion food", "korean food", "thai food", "japanese food", "mexican food"],
    "unknown": ["food", "restaurant", "cafe"],
}

PLACE_TYPE_TO_TERMS = {
    "quick_bite": ["fast food", "quick bite", "snack"],
    "cafe": ["cafe", "coffee", "brunch", "pastry"],
    "dessert": ["dessert", "ice cream", "cake", "waffles", "bingsu"],
    "full_meal": ["restaurant", "rice bowl", "noodles", "pasta"],
    "hawker_casual": ["hawker", "food court", "casual food"],
    "restaurant": ["restaurant"],
    "supper_late_night": ["supper", "late night food", "24 hour food"],
    "study_friendly": ["cafe", "coffee", "quiet cafe"],
    "date_spot": ["restaurant", "cafe", "dessert"],
    "group_meal": ["restaurant", "hotpot", "bbq", "zi char"],
}

CUISINE_TO_TERMS = {
    "any_cuisine": [],
    "japanese": ["japanese", "japanese food", "sushi", "ramen", "donburi"],
    "korean": ["korean", "korean food", "kimchi", "bbq", "bibimbap"],
    "thai": ["thai", "thai food", "tom yum", "pad thai", "green curry"],
    "chinese": ["chinese", "chinese food", "noodles", "dim sum", "zi char"],
    "indian": ["indian", "indian food", "curry", "biryani", "prata"],
    "malay": ["malay", "malay food", "nasi lemak", "satay", "mee rebus"],
    "western": ["western", "western food", "burger", "steak", "pasta"],
    "italian": ["italian", "italian food", "pasta", "pizza", "risotto"],
    "mexican": ["mexican", "mexican food", "tacos", "burritos", "quesadilla"],
    "local": ["local", "local food", "hawker", "chicken rice", "laksa"],
}

CONSTRAINT_TO_TERMS = {
    "halal_friendly": ["halal food", "halal restaurant"],
    "vegetarian_friendly": ["vegetarian food", "vegetarian restaurant"],
    "air_conditioned": ["mall food", "cafe", "restaurant"],
    "takeaway": ["takeaway food", "quick bite"],
    "not_crowded": ["quiet cafe", "small restaurant"],
    "budget_friendly": ["cheap food", "hawker", "food court"],
    "open_now": [],
}

REMARK_KEYWORDS = {
    "cold": ["ice cream", "bingsu", "smoothie", "bubble tea", "cold dessert"],
    "sweet": ["dessert", "cake", "ice cream", "waffles", "bingsu"],
    "spicy": ["mala", "thai food", "sichuan", "korean food", "curry"],
    "quiet": ["quiet cafe", "cafe", "study-friendly cafe"],
    "study": ["quiet cafe", "coffee", "cafe"],
    "late night": ["supper", "late night food", "24 hour food"],
    "supper": ["supper", "late night food", "24 hour food"],
    "cheap": ["cheap food", "hawker", "food court"],
    "budget": ["cheap food", "hawker", "food court"],
    "healthy": ["salad", "grain bowl", "poke bowl", "vegetarian food"],
    "light": ["salad", "soup", "sandwich", "poke bowl"],
    "filling": ["rice bowl", "burger", "noodles", "pasta"],
    "vegetarian": ["vegetarian food", "vegetarian restaurant"],
    "halal": ["halal food", "halal restaurant"],
    "dessert": ["dessert", "cake", "ice cream", "bingsu"],
    "cafe": ["cafe", "coffee", "brunch", "pastry"],
    "coffee": ["coffee", "cafe"],
    "ramen": ["ramen", "noodles", "soup"],
    "mala": ["mala", "spicy food", "sichuan"],
    "not too expensive": ["cheap food", "hawker", "food court"],
}

NEGATIVE_HINTS = ("not", "no", "avoid", "without", "skip", "exclude")


def all_known_terms() -> list[str]:
    """Return a sorted list of known food terms and aliases."""

    terms: set[str] = set(REMARK_KEYWORDS.keys())
    for mapping in (MOOD_TO_TERMS, PLACE_TYPE_TO_TERMS, CUISINE_TO_TERMS, CONSTRAINT_TO_TERMS):
        for values in mapping.values():
            terms.update(values)
    for values in REMARK_KEYWORDS.values():
        terms.update(values)
    return sorted(terms, key=lambda term: (-len(term), term))
