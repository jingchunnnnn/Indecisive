# Architecture

Indecisive is a root-level monorepo with a Next.js frontend, FastAPI backend, shared Python recommendation package, training utilities, model artifacts, and deployment docs.

## Frontend

The frontend in `apps/web` owns the survey UI, browser geolocation prompt, session result storage, and browser-local personalization. It stores saved and rejected places in `localStorage` under `indecisive.preferences.v1` and sends those preferences with future recommendation requests.

## Backend

The backend in `apps/api` validates requests, parses cravings, builds Google-safe search queries, fetches candidates, ranks results, and returns explanations. It never stores user location server-side.

## Provider Abstraction

`GooglePlacesProvider` is used for live recommendations. If `GOOGLE_PLACES_API_KEY` is missing, the API returns a friendly `503 Service Unavailable` error rather than showing fake fallback places. `MockPlacesProvider` remains available for isolated tests.

## Google Places Flow

The backend calls Places API New Text Search with a strict field mask and `locationBias`. It parses `place.id` as `place_id`, `place.name` as optional `resource_name`, and `place.displayName.text` as the human-readable name. The backend computes distance itself and uses radius during ranking.

## Ranking Pipeline

```text
Survey + remarks + local preferences
 ↓
Craving parser
 ↓
Search query
 ↓
Google Places or mock places
 ↓
Distance + term matching + preference penalties
 ↓
Optional semantic score
 ↓
Optional trained ranker inference
 ↓
Deterministic explanation
```

## Semantic Ranking

Semantic ranking uses exported food concept embeddings from `models/food_concept_embeddings.npz`. If artifacts are missing or invalid, the ranker continues with deterministic rule-based scoring.

## Secret Handling

The Google API key stays backend-only because frontend environment variables are visible to users. The frontend calls only the FastAPI backend.

## No Backend Training

FastAPI never trains models. Training happens locally or in Colab, and exported artifacts are copied into `models/` for inference.
