from __future__ import annotations

import httpx

from backend.config import get_settings


async def generate(prompt: str, model: str) -> tuple[str, str]:
    settings = get_settings()
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=120.0)) as client:
        response = await client.post(
            settings.ollama_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("model", model), data.get("response", "").strip()
