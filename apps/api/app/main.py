"""Indecisive FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.cors import configure_cors
from app.routes import health, places, recommend


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Indecisive API",
        version="0.1.0",
        description="Craving-based nearby food recommendations.",
    )
    configure_cors(app, settings)
    app.include_router(health.router)
    app.include_router(recommend.router)
    app.include_router(places.router)

    @app.exception_handler(ValueError)
    async def value_error_handler(_, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    return app


app = create_app()
