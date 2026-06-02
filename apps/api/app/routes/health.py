"""Health endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.responses import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
