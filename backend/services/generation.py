from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

from fastapi import HTTPException

from backend.clients import ollama_client, openai_client
from backend.config import get_settings
from backend.storage import LogEntry, persist


def extract_final_answer(text: str) -> Optional[str]:
    final_line: Optional[str] = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("answer:"):
            final_line = stripped
    return final_line


async def invoke_llm(prompt: str, system_prompt: str, model_override: Optional[str]) -> Tuple[str, str]:
    settings = get_settings()
    backend = settings.ai_backend
    if backend == "ollama":
        model = model_override or settings.ollama_model
        user_prompt = f"{system_prompt}\n\nUser:\n{prompt.strip()}\n"
        return await ollama_client.generate(user_prompt, model)
    if backend == "openai_compatible":
        model = model_override or settings.openai_model
        return await openai_client.generate(system_prompt, prompt.strip(), model)
    raise HTTPException(status_code=500, detail=f"Unsupported backend '{backend}'")


async def archive_response(
    *,
    request_id: str,
    prompt: str,
    response: str,
    final_answer: Optional[str],
    elapsed_ms: int,
    domain: Optional[str],
    model: str,
) -> None:
    settings = get_settings()
    log_entry = LogEntry(
        id=request_id,
        created_at=datetime.now(timezone.utc),
        backend=settings.ai_backend,
        model=model,
        prompt=prompt,
        response=response,
        final_answer=final_answer,
        elapsed_ms=elapsed_ms,
        domain=domain,
    )
    await persist(log_entry)


async def generate_response(
    *,
    prompt: str,
    system_prompt: str,
    domain: Optional[str],
    model_override: Optional[str],
) -> Dict:
    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    model_name, response_text = await invoke_llm(prompt, system_prompt, model_override)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    final_answer = extract_final_answer(response_text)
    return {
        "id": request_id,
        "model": model_name,
        "response": response_text,
        "final_answer": final_answer,
        "elapsed_ms": elapsed_ms,
    }
