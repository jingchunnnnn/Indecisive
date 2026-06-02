export type ChipOption = {
  label: string;
  value: string;
};

export const MOOD_OPTIONS: ChipOption[] = [
  { label: "Sweet", value: "sweet" },
  { label: "Spicy", value: "spicy" },
  { label: "Savory", value: "savory" },
  { label: "Light", value: "light" },
  { label: "Comforting", value: "comforting" },
  { label: "Refreshing", value: "refreshing" },
  { label: "Filling", value: "filling" },
  { label: "Healthy", value: "healthy" },
  { label: "Adventurous", value: "adventurous" },
  { label: "I don't know", value: "unknown" }
];

export const PLACE_TYPE_OPTIONS: ChipOption[] = [
  { label: "Quick bite", value: "quick_bite" },
  { label: "Cafe", value: "cafe" },
  { label: "Dessert", value: "dessert" },
  { label: "Full meal", value: "full_meal" },
  { label: "Hawker / casual", value: "hawker_casual" },
  { label: "Restaurant", value: "restaurant" },
  { label: "Supper / late night", value: "supper_late_night" },
  { label: "Study-friendly", value: "study_friendly" },
  { label: "Date spot", value: "date_spot" },
  { label: "Group meal", value: "group_meal" }
];

export const CUISINE_OPTIONS: ChipOption[] = [
  { label: "Anything works", value: "any_cuisine" },
  { label: "Japanese", value: "japanese" },
  { label: "Korean", value: "korean" },
  { label: "Thai", value: "thai" },
  { label: "Chinese", value: "chinese" },
  { label: "Indian", value: "indian" },
  { label: "Malay", value: "malay" },
  { label: "Western", value: "western" },
  { label: "Italian", value: "italian" },
  { label: "Mexican", value: "mexican" },
  { label: "Local", value: "local" }
];

export const CONSTRAINT_OPTIONS: ChipOption[] = [
  { label: "Open now", value: "open_now" },
  { label: "Budget-friendly", value: "budget_friendly" },
  { label: "Halal", value: "halal_friendly" },
  { label: "Vegetarian-friendly", value: "vegetarian_friendly" },
  { label: "Air-conditioned", value: "air_conditioned" },
  { label: "Good for takeaway", value: "takeaway" },
  { label: "Not too crowded", value: "not_crowded" }
];

export const RADIUS_OPTIONS = [
  { label: "500m", value: 500 },
  { label: "1km", value: 1000 },
  { label: "2km", value: 2000 },
  { label: "5km", value: 5000 },
  { label: "Any", value: 50000 }
];

export const REMARK_PLACEHOLDERS = [
  "Something sweet and cold but not bubble tea...",
  "Quiet cafe with dessert",
  "Spicy but not too expensive",
  "Late-night comfort food",
  "Something light and refreshing"
];

export const LATEST_RESULTS_KEY = "indecisive.latestResults";
export const LATEST_REQUEST_KEY = "indecisive.latestRequest";
