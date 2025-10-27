from __future__ import annotations

import httpx

from backend.config import get_settings


async def generate(system_prompt: str, user_prompt: str, model: str) -> tuple[str, str]:
    settings = get_settings()
    headers = {"Content-Type": "application/json"}
    if settings.openai_api_key:
        headers["Authorization"] = f"Bearer {settings.openai_api_key}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
    }
    url = settings.openai_base_url.rstrip("/") + "/chat/completions"
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=120.0)) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        first_choice = data.get("choices", [{}])[0]
        message = first_choice.get("message", {})
        return data.get("model", model), str(message.get("content", "")).strip()
