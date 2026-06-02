"""Application settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    google_places_api_key: str | None = Field(default=None, alias="GOOGLE_PLACES_API_KEY")
    frontend_origin: str | None = Field(default="http://localhost:3000", alias="FRONTEND_ORIGIN")
    env: str = Field(default="development", alias="ENV")
    enable_semantic_ranking: bool = Field(default=True, alias="ENABLE_SEMANTIC_RANKING")
    enable_trained_ranker: bool = Field(default=False, alias="ENABLE_TRAINED_RANKER")
    model_artifact_dir: str = Field(default="../../models", alias="MODEL_ARTIFACT_DIR")
    feedback_log_path: str = Field(default="../../data/feedback.jsonl", alias="FEEDBACK_LOG_PATH")
    google_timeout_s: float = 8.0

    @property
    def artifact_path(self) -> Path:
        path = Path(self.model_artifact_dir)
        if path.is_absolute():
            return path
        cwd_path = (Path.cwd() / path).resolve()
        if cwd_path.exists():
            return cwd_path
        repo_root = Path(__file__).resolve().parents[4]
        return (repo_root / "models").resolve()

    @property
    def resolved_feedback_log_path(self) -> Path:
        path = Path(self.feedback_log_path)
        if path.is_absolute():
            return path
        cwd_path = (Path.cwd() / path).resolve()
        if cwd_path.parent.exists():
            return cwd_path
        repo_root = Path(__file__).resolve().parents[4]
        return (repo_root / "data" / "feedback.jsonl").resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
