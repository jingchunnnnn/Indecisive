# AGENTS.md

## Project

This repo contains Indecisive, a full-stack craving-based nearby food recommender.

Users answer a short survey, optionally add remarks, share location, and get ranked nearby food recommendations.

## Structure

- apps/web: Next.js frontend
- apps/api: FastAPI backend
- packages/recommender: shared recommendation logic
- training: local embedding generation and optional Colab model training
- models: exported ML artifacts
- docs: architecture, ML, Google Places, and deployment docs

## Frontend commands

cd apps/web
npm install
npm run dev
npm run lint
npm run build

## Backend commands

cd apps/api
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest

## Local embedding generation

cd training
pip install -r requirements.txt
python generate_food_concept_embeddings.py

## Docker command

docker compose up --build

## Rules

- Never expose Google Places API keys in frontend code.
- Never commit .env files.
- Keep Google Places field masks minimal.
- Do not request photos, reviews, ratings, opening hours, price level, website URI, or generative summaries in MVP.
- Do not fabricate ratings, photos, reviews, price, opening hours, halal status, vegetarian status, or crowd levels.
- Use Google place.id as place_id.
- Use Google place.name only as optional resource_name.
- Use Google place.displayName.text as the human-readable name.
- Use locationBias for Google search, but always compute distance in backend.
- Keep recommendation logic deterministic and testable.
- Use MockPlacesProvider when GOOGLE_PLACES_API_KEY is missing.
- Normal development must work on Mac M1 using VS Code.
- Colab is only for optional model training.
- FastAPI must never train models.
- FastAPI must fallback gracefully when ML artifacts are missing.
- Update docs when architecture, ML workflow, or environment variables change.
