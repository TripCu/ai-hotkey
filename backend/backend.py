from __future__ import annotations

import asyncio
import base64
import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.config import get_settings
from backend.prompts_loader import load_base_prompt, load_domain_prompts
from backend.services.generation import archive_response, generate_response
from backend.storage import ensure_data_paths, get_recent_entries
from backend.notes import gather_relevant_notes
from backend.telemetry import monitor_resources, record_request, get_metrics

logger = logging.getLogger("backend.backend")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")

SETTINGS = get_settings()
ensure_data_paths()

BASE_PROMPT = load_base_prompt()
DOMAIN_PROMPTS = load_domain_prompts()
UNIVERSAL_INSTRUCTION = (
    "Respond with concise, numbered reasoning when helpful and finish with a single line that begins "
    "with 'Answer:' followed by the final result when a definitive answer exists."
)


def compose_system_prompt(domain_key: Optional[str]) -> str:
    parts: List[str] = [BASE_PROMPT]
    if domain_key:
        prompt = DOMAIN_PROMPTS.get(domain_key)
        if prompt:
            parts.append(prompt.strip())
    parts.append(UNIVERSAL_INSTRUCTION)
    return "\n\n".join(parts)


async def verify_api_key(x_api_key: Optional[str] = Header(default=None, alias="x-api-key")) -> None:
    if not x_api_key or x_api_key != SETTINGS.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")


app = FastAPI(title="AI Hotkey Backend", version="1.2.0")


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(monitor_resources())


@app.get("/status")
async def get_status() -> Dict[str, Any]:
    return {
        "ok": True,
        "backend": SETTINGS.ai_backend,
        "model": SETTINGS.ollama_model if SETTINGS.ai_backend == "ollama" else SETTINGS.openai_model,
    }


@app.get("/telemetry")
async def get_telemetry() -> Dict[str, Any]:
    return get_metrics()


@app.post("/generate", response_model=None, dependencies=[Depends(verify_api_key)])
async def generate(request: Request, payload: Dict[str, Any]) -> JSONResponse:
    generation_payload = GenerationPayload.model_validate(payload)
    return await _handle_generation(generation_payload, request)


@app.post("/generate-with-image", response_model=None, dependencies=[Depends(verify_api_key)])
async def generate_with_image(
    request: Request,
    prompt: str = Form(...),
    files: Optional[List[UploadFile]] = File(default=None),
) -> JSONResponse:
    payload = GenerationPayload(prompt=prompt, context=GenerationContext())
    if SETTINGS.question_domain:
        payload.context.question_type = SETTINGS.question_domain

    collected: List[bytes] = []
    if files:
        for file in files:
            try:
                data = await file.read()
                if data:
                    collected.append(data)
            finally:
                await file.close()

    if collected:
        if not SETTINGS.vision_enabled:
            raise HTTPException(status_code=400, detail="Vision support is disabled. Set VISION_ENABLED=1 and configure a vision model.")
        payload.images = [base64.b64encode(data).decode("ascii") for data in collected]
        payload.prompt_prefix = "Image(s) attached with the request."

    return await _handle_generation(payload, request)


class GenerationContext(BaseModel):
    question_type: Optional[str] = Field(default=None)


class GenerationPayload(BaseModel):
    prompt: str = Field(..., min_length=1)
    context: GenerationContext = Field(default_factory=GenerationContext)
    images: Optional[List[str]] = Field(default=None, description="Base64-encoded images for OCR.")
    prompt_prefix: Optional[str] = Field(default=None, description="Optional extra text prepended to the prompt.")
    model: Optional[str] = Field(default=None)

    model_config = {"extra": "ignore"}


async def _handle_generation(payload: GenerationPayload, http_request: Optional[Request]) -> JSONResponse:
    domain = (payload.context.question_type or "").strip() or None
    if not domain and SETTINGS.question_domain:
        domain = SETTINGS.question_domain
    system_prompt = compose_system_prompt(domain)

    if payload.images and not SETTINGS.vision_enabled:
        raise HTTPException(
            status_code=400,
            detail="Vision support is disabled. Set VISION_ENABLED=1 and configure a vision-capable model.",
        )

    prompt_parts: List[str] = []
    if payload.prompt_prefix:
        prompt_parts.append(payload.prompt_prefix.strip())
    prompt_parts.append(payload.prompt.strip())
    prompt_text = "\n\n".join(part for part in prompt_parts if part)
    payload.prompt = prompt_text

    history_entries = get_recent_entries(limit=5)
    history_section = ""
    if history_entries:
        history_blocks = [
            f"User: {item['prompt'].strip()}\nAssistant: {item['response'].strip()}"
            for item in history_entries
        ]
        history_section = (
            "Here is the recent conversation history between the user and assistant:\n"
            + "\n\n".join(history_blocks)
            + "\n\n"
        )

    notes_section = ""
    notes_snippets = gather_relevant_notes(payload.prompt)
    if notes_snippets:
        notes_section = (
            "Relevant notes extracted from the knowledge base:\n"
            + "\n\n".join(notes_snippets)
            + "\n\n"
        )

    prompt_body = (
        history_section
        + notes_section
        + "Respond to the user's latest request while referencing prior context when helpful:\n"
        + payload.prompt.strip()
    )

    client_ip = "unknown"
    api_key = ""
    if http_request is not None:
        client = http_request.client
        client_ip = client.host if client else "unknown"
        api_key = http_request.headers.get("x-api-key", "")
    record_request(client_ip, api_key, len(prompt_body))

    try:
        result = await generate_response(
            prompt=prompt_body,
            system_prompt=system_prompt,
            domain=domain,
            model_override=payload.model,
            images=payload.images if SETTINGS.vision_enabled else None,
        )
    except httpx.HTTPError as exc:
        logger.exception("LLM request failed")
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc

    await archive_response(
        request_id=result["id"],
        prompt=payload.prompt,
        response=result["response"],
        final_answer=result["final_answer"],
        elapsed_ms=result["elapsed_ms"],
        domain=domain,
        model=result["model"],
    )

    payload = {
        "status": "ok",
        **result,
    }
    return JSONResponse(content=payload)
