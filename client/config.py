from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _float(value: str | None, default: float) -> float:
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def _int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


@dataclass(frozen=True)
class ClientConfig:
    host: str
    port: int
    api_key: str
    start_key: str
    exit_key: str
    clipboard_key: str
    screenshot_key: str
    screenshot_prompt: str
    question_domain: str
    overlay_enabled: bool
    overlay_duration: float
    overlay_opacity: float
    overlay_width: int


def load_client_config() -> ClientConfig:
    data = dotenv_values(ENV_FILE)
    return ClientConfig(
        host=data.get("HOST", "127.0.0.1"),
        port=_int(data.get("PORT"), 8000),
        api_key=data.get("API_KEY", "local-dev-key"),
        start_key=data.get("START_KEY", "`"),
        exit_key=data.get("EXIT_KEY", "ESC"),
        clipboard_key=data.get("CLIPBOARD_KEY", "\\"),
        screenshot_key=data.get("SCREENSHOT_KEY", "]"),
        screenshot_prompt=data.get("SCREENSHOT_PROMPT", "Summarize the captured screenshot."),
        question_domain=(data.get("QUESTION_DOMAIN") or "").strip(),
        overlay_enabled=_bool(data.get("OVERLAY_ENABLED"), True),
        overlay_duration=_float(data.get("OVERLAY_DURATION"), 15.0),
        overlay_opacity=_float(data.get("OVERLAY_OPACITY"), 0.9),
        overlay_width=_int(data.get("OVERLAY_WIDTH"), 480),
    )
