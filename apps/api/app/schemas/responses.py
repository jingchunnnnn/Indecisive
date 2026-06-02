"""Response schemas for the Indecisive API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class InterpretedCraving(BaseModel):
    moods: list[str] = Field(default_factory=list)
    cuisines: list[str] = Field(default_factory=list)
    cuisine_terms: list[str] = Field(default_factory=list)
    positive_terms: list[str] = Field(default_factory=list)
    negative_terms: list[str] = Field(default_factory=list)
    search_query: str


class Recommendation(BaseModel):
    place_id: str
    resource_name: str | None = None
    name: str
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    distance_m: float | None = None
    types: list[str] = Field(default_factory=list)
    primary_type: str | None = None
    google_maps_uri: str | None = None
    score: float
    reason: str


class RecommendResponse(BaseModel):
    interpreted_craving: InterpretedCraving
    recommendations: list[Recommendation] = Field(default_factory=list)


class PlaceDetailsResponse(BaseModel):
    place_id: str
    resource_name: str | None = None
    name: str
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    types: list[str] = Field(default_factory=list)
    primary_type: str | None = None
    google_maps_uri: str | None = None


class StatusResponse(BaseModel):
    status: str = "ok"
