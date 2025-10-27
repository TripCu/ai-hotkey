from __future__ import annotations

from pathlib import Path
from typing import Dict

import yaml

SERVER_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = SERVER_DIR / "prompts"
BASE_PROMPT_FILE = PROMPTS_DIR / "base.md"
DOMAINS_FILE = PROMPTS_DIR / "domains.yaml"


def load_base_prompt() -> str:
    if BASE_PROMPT_FILE.exists():
        return BASE_PROMPT_FILE.read_text(encoding="utf-8").strip()
    return "You are a helpful AI assistant."


def load_domain_prompts() -> Dict[str, str]:
    if not DOMAINS_FILE.exists():
        return {}
    data = yaml.safe_load(DOMAINS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}

