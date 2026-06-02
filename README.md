# Indecisive

**Not sure what to eat?**

Indecisive is a cute, clean full-stack food recommendation app for people who cannot decide what to eat. Users answer a short food mood survey, optionally add remarks, share location, and receive ranked nearby food/place recommendations with clear explanations.

Screenshot placeholder: add an app screenshot here after the first local run.

## Features

- Next.js App Router frontend with a polished single-page craving survey.
- FastAPI backend with Pydantic v2 validation.
- Google Places API New Text Search through a backend-only API key.
- Clear service-unavailable errors when `GOOGLE_PLACES_API_KEY` is missing.
- Rule-based ranking with distance, craving, negative terms, and local preferences.
- Optional semantic reranking from lightweight exported embedding artifacts.
- Optional Colab training workflow for `ranker.pkl`.
- Docker setup for local full-stack runs.
- Vercel frontend and Render Docker backend deployment paths.

## Architecture

```text
User
 ↓
Next.js frontend on Vercel
 ↓
FastAPI backend
 ↓
Craving parser + query builder
 ↓
Google Places Text Search
 ↓
Rule-based ranker + semantic reranker
 ↓
Explanations
 ↓
Recommendation cards
```

## Tech Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, browser geolocation, `localStorage`.
- Backend: Python 3.11+, FastAPI, Pydantic v2, `pydantic-settings`, `httpx`, `numpy`.
- ML: local embedding artifact generation, optional Colab-trained ranker, inference-only backend.
- Tests: `pytest` and tiny semantic artifacts created in tests.

## Local Setup

Backend:

```bash
cd apps/api
pip install -r requirements.txt
PYTHONPATH=.:../../packages/recommender uvicorn app.main:app --reload
```

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

Default URLs:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Health: `http://localhost:8000/health`

## Docker

```bash
docker compose up --build
```

The backend requires a Google key for recommendation searches. The frontend uses `NEXT_PUBLIC_API_URL=http://localhost:8000`.

## Google Places Setup

Set `GOOGLE_PLACES_API_KEY` only in backend environments. The frontend never receives this secret.

The MVP uses:

- Places API New Text Search: one request per recommendation.
- Place Details only on the detail page.
- Strict field masks.
- No photos, reviews, ratings, opening hours, price level, website URI, or generative summaries.

Set Google Cloud budget alerts and daily quotas before using real mode.

## Environment Variables

See `.env.example`, `apps/api/.env.example`, and `apps/web/.env.local.example`.

```text
GOOGLE_PLACES_API_KEY=
FRONTEND_ORIGIN=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
ENV=development
ENABLE_SEMANTIC_RANKING=true
ENABLE_TRAINED_RANKER=false
MODEL_ARTIFACT_DIR=/app/models
```

## Recommendation Logic

The backend parses selected moods, place types, constraints, remarks, and browser-local preferences. It builds a search query, fetches places from Google or the mock provider, computes distance itself, penalizes negative terms such as `not bubble tea`, applies liked/disliked local preferences, optionally adds semantic similarity, then returns ranked recommendations with deterministic explanations.

## ML Workflow

Normal app development runs locally on a Mac M1 using VS Code. Colab is only for optional model training and is not connected to VS Code.

Generate semantic embeddings locally:

```bash
cd training
pip install -r requirements.txt
python generate_food_concept_embeddings.py
```

Optional trained ranker artifacts can be created in `training/colab_train_ranker.ipynb` and manually copied into `models/`.

The deployed backend performs inference only. It never trains models. If ML artifacts are unavailable, the app falls back to deterministic ranking.

## Tests

```bash
cd apps/api
PYTHONPATH=.:../../packages/recommender pytest
```

## Deployment

Frontend on Vercel:

- Root directory: `apps/web`
- Env var: `NEXT_PUBLIC_API_URL=https://your-backend-url`

Backend on Render Free:

- Dockerfile path: `apps/api/Dockerfile`
- Env vars: `GOOGLE_PLACES_API_KEY`, `FRONTEND_ORIGIN`, `ENV=production`, `ENABLE_SEMANTIC_RANKING=true`, `ENABLE_TRAINED_RANKER=false`, `MODEL_ARTIFACT_DIR=/app/models`

Render Free services may sleep when inactive.

## Missing API Key

When `GOOGLE_PLACES_API_KEY` is missing, recommendation and place-detail requests return a friendly `503 Service Unavailable` error instead of fake places. This avoids showing random fallback recommendations to users.

## Future Improvements

- Add map view.
- Add optional ratings/photos with clear cost-control.
- Add user accounts and saved preferences.
- Add better dietary filters backed by reliable data.
- Add opening-hours support with careful field masks.
- Add restaurant clustering for diversity.
- Add offline evaluation dashboard.
- Improve semantic matching with richer concept vocabulary.
- Train a better learning-to-rank model from real feedback.
- Add privacy-preserving analytics.
