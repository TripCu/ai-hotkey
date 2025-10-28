from __future__ import annotations

import httpx

from typing import List, Optional

from backend.config import get_settings


def _render_message_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts).strip()
    return ""


async def generate(
    system_prompt: str,
    user_prompt: str,
    model: str,
    images: Optional[List[str]] = None,
) -> tuple[str, str]:
    settings = get_settings()
    headers = {"Content-Type": "application/json"}
    if settings.openai_api_key:
        headers["Authorization"] = f"Bearer {settings.openai_api_key}"

    user_content: object
    if images:
        user_parts: List[dict[str, object]] = [{"type": "text", "text": user_prompt}]
        for encoded in images:
            data_url = f"data:image/png;base64,{encoded}"
            user_parts.append({"type": "image_url", "image_url": {"url": data_url}})
        user_content = user_parts
    else:
        user_content = user_prompt

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
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
        content = _render_message_text(message.get("content"))
        return data.get("model", model), content
