"""Request schemas for the Indecisive API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SurveyRequest(BaseModel):
    moods: list[str] = Field(default_factory=list)
    cuisines: list[str] = Field(default_factory=list)
    place_types: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    radius_m: int = Field(default=2000, ge=100, le=50000)

    @field_validator("moods", "cuisines", "place_types", "constraints", mode="before")
    @classmethod
    def default_lists(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        return []


class LocationRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)


class UserPreferencesRequest(BaseModel):
    liked_place_ids: list[str] = Field(default_factory=list)
    disliked_place_ids: list[str] = Field(default_factory=list)
    liked_types: list[str] = Field(default_factory=list)
    disliked_types: list[str] = Field(default_factory=list)
    disliked_terms: list[str] = Field(default_factory=list)

    @field_validator(
        "liked_place_ids",
        "disliked_place_ids",
        "liked_types",
        "disliked_types",
        "disliked_terms",
        mode="before",
    )
    @classmethod
    def normalize_lists(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []


class RecommendRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    survey: SurveyRequest = Field(default_factory=SurveyRequest)
    remarks: str = Field(default="", max_length=300)
    location: LocationRequest
    user_preferences: UserPreferencesRequest = Field(default_factory=UserPreferencesRequest)

    @model_validator(mode="after")
    def reject_empty_request(self) -> "RecommendRequest":
        if not (
            self.survey.moods
            or self.survey.cuisines
            or self.survey.place_types
            or self.survey.constraints
            or self.remarks.strip()
        ):
            raise ValueError("Pick at least one craving option or add a short remark.")
        return self


class FeedbackRequest(BaseModel):
    place_id: str = Field(min_length=1, max_length=200)
    action: Literal["liked", "disliked", "not_for_me"]
    types: list[str] = Field(default_factory=list)


class PlaceDetailsPath(BaseModel):
    place_id: str = Field(min_length=1, max_length=200)
