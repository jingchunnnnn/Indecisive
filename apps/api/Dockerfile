FROM python:3.11-slim

WORKDIR /app

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api/app ./app
COPY packages/recommender ./packages/recommender
COPY models ./models

ENV PYTHONPATH=/app:/app/packages/recommender
ENV MODEL_ARTIFACT_DIR=/app/models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
