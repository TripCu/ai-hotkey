from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values
from pydantic import BaseModel, Field, PositiveInt, ValidationError, model_validator


ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseModel):
    ai_backend: str = Field(default="ollama", alias="AI_BACKEND")
    ollama_url: str = Field(default="http://localhost:11434/api/generate", alias="OLLAMA_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_vision_model: str = Field(default="llava:13b", alias="OLLAMA_VISION_MODEL")

    openai_base_url: str = Field(default="http://localhost:1234/v1", alias="OPENAI_BASE_URL")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    openai_vision_model: str = Field(default="gpt-4o", alias="OPENAI_VISION_MODEL")

    api_key: str = Field(default="local-dev-key", alias="API_KEY")
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: PositiveInt = Field(default=8000, alias="PORT")
    question_domain: str = Field(default="", alias="QUESTION_DOMAIN")
    notes_path: Optional[str] = Field(default=None, alias="NOTES_PATH")
    vision_enabled: bool = Field(default=False, alias="VISION_ENABLED")

    model_config = {"populate_by_name": True, "extra": "ignore"}

    @model_validator(mode="after")
    def normalise_backend(self) -> "Settings":
        backend = self.ai_backend.lower().strip()
        if backend not in {"ollama", "openai_compatible"}:
            raise ValueError("AI_BACKEND must be 'ollama' or 'openai_compatible'")
        self.ai_backend = backend
        self.question_domain = self.question_domain.strip()
        if self.notes_path:
            self.notes_path = self.notes_path.strip()
            if not self.notes_path:
                self.notes_path = None
        return self


def _load_raw_env() -> dict[str, Optional[str]]:
    return {k: v for k, v in dotenv_values(ROOT / ".env").items() if v is not None}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    raw = _load_raw_env()
    try:
        return Settings.model_validate(raw)
    except ValidationError as exc:  # pragma: no cover
        raise RuntimeError(f"Invalid configuration: {exc}") from exc
