import type { Recommendation } from "./types";

export type LocalPreferences = {
  liked_place_ids: string[];
  disliked_place_ids: string[];
  liked_types: string[];
  disliked_types: string[];
  disliked_terms: string[];
};

export const PREFERENCES_KEY = "indecisive.preferences.v1";

export const emptyPreferences: LocalPreferences = {
  liked_place_ids: [],
  disliked_place_ids: [],
  liked_types: [],
  disliked_types: [],
  disliked_terms: []
};

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

export function getLocalPreferences(): LocalPreferences {
  if (typeof window === "undefined") {
    return emptyPreferences;
  }

  try {
    const raw = window.localStorage.getItem(PREFERENCES_KEY);
    if (!raw) {
      return emptyPreferences;
    }
    const parsed = JSON.parse(raw) as Partial<LocalPreferences>;
    return {
      liked_place_ids: unique(parsed.liked_place_ids || []),
      disliked_place_ids: unique(parsed.disliked_place_ids || []),
      liked_types: unique(parsed.liked_types || []),
      disliked_types: unique(parsed.disliked_types || []),
      disliked_terms: unique(parsed.disliked_terms || [])
    };
  } catch {
    return emptyPreferences;
  }
}

export function saveLocalPreferences(preferences: LocalPreferences) {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(PREFERENCES_KEY, JSON.stringify(preferences));
}

export function saveRecommendation(recommendation: Recommendation) {
  const preferences = getLocalPreferences();
  saveLocalPreferences({
    ...preferences,
    liked_place_ids: unique([...preferences.liked_place_ids, recommendation.place_id]),
    disliked_place_ids: preferences.disliked_place_ids.filter((placeId) => placeId !== recommendation.place_id),
    liked_types: unique([...preferences.liked_types, ...recommendation.types]),
    disliked_types: preferences.disliked_types.filter((type) => !recommendation.types.includes(type))
  });
}

export function rejectRecommendation(recommendation: Recommendation) {
  const preferences = getLocalPreferences();
  saveLocalPreferences({
    ...preferences,
    liked_place_ids: preferences.liked_place_ids.filter((placeId) => placeId !== recommendation.place_id),
    disliked_place_ids: unique([...preferences.disliked_place_ids, recommendation.place_id]),
    liked_types: preferences.liked_types.filter((type) => !recommendation.types.includes(type)),
    disliked_types: unique([...preferences.disliked_types, ...recommendation.types])
  });
}

export function clearRecommendationFeedback(recommendation: Recommendation) {
  const preferences = getLocalPreferences();
  saveLocalPreferences({
    ...preferences,
    liked_place_ids: preferences.liked_place_ids.filter((placeId) => placeId !== recommendation.place_id),
    disliked_place_ids: preferences.disliked_place_ids.filter((placeId) => placeId !== recommendation.place_id),
    liked_types: preferences.liked_types.filter((type) => !recommendation.types.includes(type)),
    disliked_types: preferences.disliked_types.filter((type) => !recommendation.types.includes(type))
  });
}

export function resetLocalPreferences() {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.removeItem(PREFERENCES_KEY);
}
