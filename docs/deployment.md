# Deployment

## Vercel Frontend

Create a Vercel project with:

```text
Root directory: apps/web
```

Set:

```text
NEXT_PUBLIC_API_URL=https://your-backend-url
```

## Render Backend

Deploy as a Docker service.

```text
Dockerfile path: apps/api/Dockerfile
```

Set:

```text
GOOGLE_PLACES_API_KEY=<secret>
FRONTEND_ORIGIN=https://your-vercel-app-url
ENV=production
ENABLE_SEMANTIC_RANKING=true
ENABLE_TRAINED_RANKER=false
MODEL_ARTIFACT_DIR=/app/models
```

Free Render services may sleep when inactive, so the first request after idle time can be slow.

## Smoke Checks

- `GET /health` returns `{ "status": "ok" }`.
- Frontend can submit the survey.
- Missing-key mode returns a friendly `503 Service Unavailable`.
- Real mode works when `GOOGLE_PLACES_API_KEY` is set.
