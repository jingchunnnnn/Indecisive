export type RecommendRequest = {
  survey: {
    moods: string[];
    cuisines: string[];
    place_types: string[];
    constraints: string[];
    radius_m: number;
  };
  remarks: string;
  location: {
    lat: number;
    lng: number;
  };
  user_preferences: {
    liked_place_ids: string[];
    disliked_place_ids: string[];
    liked_types: string[];
    disliked_types: string[];
    disliked_terms: string[];
  };
};

export type RecommendResponse = {
  interpreted_craving: {
    moods: string[];
    cuisines: string[];
    cuisine_terms: string[];
    positive_terms: string[];
    negative_terms: string[];
    search_query: string;
  };
  recommendations: Recommendation[];
};

export type Recommendation = {
  place_id: string;
  resource_name?: string | null;
  name: string;
  address: string | null;
  lat: number | null;
  lng: number | null;
  distance_m: number | null;
  types: string[];
  primary_type?: string | null;
  google_maps_uri: string | null;
  score: number;
  reason: string;
};

export type PlaceDetails = Omit<Recommendation, "distance_m" | "score" | "reason">;
