"""CORS setup."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings


def configure_cors(app: FastAPI, settings: Settings) -> None:
    origins = {"http://localhost:3000"}
    if settings.frontend_origin:
        origins.add(settings.frontend_origin)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=sorted(origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
