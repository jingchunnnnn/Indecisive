# Indecisive API

FastAPI backend for craving parsing, Google Places or mock search, ranking, semantic reranking, and deterministic explanations.

## Local Run

```bash
cd apps/api
pip install -r requirements.txt
PYTHONPATH=.:../../packages/recommender uvicorn app.main:app --reload
```

## Tests

```bash
cd apps/api
PYTHONPATH=.:../../packages/recommender pytest
```

The API uses `MockPlacesProvider` when `GOOGLE_PLACES_API_KEY` is not set.
