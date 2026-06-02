import type { PlaceDetails, RecommendRequest, RecommendResponse, Recommendation } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {})
    }
  });

  if (!response.ok) {
    let message = "Something went sideways while finding food.";
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) {
        message = payload.detail;
      }
    } catch {
      // Keep the friendly fallback.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function getApiUrl() {
  return API_URL;
}

export async function fetchRecommendations(payload: RecommendRequest): Promise<RecommendResponse> {
  return requestJson<RecommendResponse>("/recommend", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function fetchPlaceDetails(placeId: string): Promise<PlaceDetails> {
  return requestJson<PlaceDetails>(`/places/${encodeURIComponent(placeId)}`);
}

export async function sendFeedback(
  recommendation: Pick<Recommendation, "place_id" | "types">,
  action: "liked" | "not_for_me"
) {
  return requestJson<{ status: string }>("/feedback", {
    method: "POST",
    body: JSON.stringify({
      place_id: recommendation.place_id,
      action,
      types: recommendation.types
    })
  });
}
