from __future__ import annotations

import asyncio
import logging
from io import BytesIO
from typing import Any, Dict, List, Optional

import httpx
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None  # type: ignore[assignment]

try:
    import pytesseract
except ImportError:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore[assignment]

from app.server.config import get_settings
from app.server.prompts_loader import load_base_prompt, load_domain_prompts
from app.server.services.generation import archive_response, generate_response
from app.server.storage import ensure_data_paths, get_recent_entries
from app.server.notes import gather_relevant_notes
from app.server.telemetry import monitor_resources, record_request, get_metrics

logger = logging.getLogger("app.server.backend")
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


def run_validator(domain: Optional[str], final_line: Optional[str]) -> tuple[Optional[bool], Optional[dict]]:
    if domain != "subnetting":
        return None, None
    if not final_line:
        return False, {"reason": "Final answer missing for subnetting validation."}
    try:
        from app.server.validators.ip_network import validate_answer
    except Exception as exc:  # pragma: no cover
        logger.warning("Unable to load subnet validator: %s", exc)
        return False, {"reason": "Validator unavailable."}
    try:
        result = validate_answer(final_line)
    except Exception as exc:  # pragma: no cover
        logger.exception("Subnet validator raised an error: %s", exc)
        return False, {"reason": "Validator error"}
    return bool(result.get("ok")), result


async def append_ocr_context(files: Optional[List[UploadFile]]) -> tuple[str, List[str]]:
    if not files:
        return "", []

    notes: List[str] = []
    extracted_segments: List[str] = []

    if pytesseract is None or Image is None:
        notes.append("OCR not available; install Tesseract and Pillow to enable text extraction.")
        return "\n".join(notes), extracted_segments

    for file in files:
        try:
            content = await file.read()
            if not content:
                continue
            with Image.open(BytesIO(content)) as img:
                text = pytesseract.image_to_string(img).strip()
                if text:
                    extracted_segments.append(f"Text from {file.filename or 'image'}:\n{text}")
                else:
                    notes.append(f"OCR found no text in {file.filename or 'image'}.")
        except Exception as exc:
            notes.append(f"OCR failed for {file.filename or 'image'}: {exc}")
        finally:
            await file.close()

    if extracted_segments:
        notes.append("OCR extracted text from provided images.")
    elif not notes:
        notes.append("Images processed but no OCR text extracted.")

    return "\n".join(notes), extracted_segments


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

    ocr_summary, extracted_segments = await append_ocr_context(files)
    extended_prompt_parts = [prompt]
    if extracted_segments:
        extended_prompt_parts.append("Additional OCR context:\n" + "\n\n".join(extracted_segments))
    if ocr_summary:
        extended_prompt_parts.append(f"[Notes]\n{ocr_summary}")
    payload.prompt = "\n\n".join(extended_prompt_parts)

    return await _handle_generation(payload, request)


class GenerationContext(BaseModel):
    question_type: Optional[str] = Field(default=None)


class GenerationPayload(BaseModel):
    prompt: str = Field(..., min_length=1)
    context: GenerationContext = Field(default_factory=GenerationContext)
    model: Optional[str] = Field(default=None)

    model_config = {"extra": "ignore"}


async def _handle_generation(payload: GenerationPayload, http_request: Optional[Request]) -> JSONResponse:
    domain = (payload.context.question_type or "").strip() or None
    if not domain and SETTINGS.question_domain:
        domain = SETTINGS.question_domain
    system_prompt = compose_system_prompt(domain)

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
        )
    except httpx.HTTPError as exc:
        logger.exception("LLM request failed")
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc

    valid, validation = run_validator(domain, result["final_answer"])
    await archive_response(
        request_id=result["id"],
        prompt=payload.prompt,
        response=result["response"],
        final_answer=result["final_answer"],
        elapsed_ms=result["elapsed_ms"],
        domain=domain,
        valid=valid,
        validation=validation,
        model=result["model"],
    )

    payload = {
        "status": "ok",
        **result,
        "valid": valid,
        "validation": validation,
    }
    return JSONResponse(content=payload)
