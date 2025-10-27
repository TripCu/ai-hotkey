from __future__ import annotations

import asyncio
import json
import logging
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
import yaml
from dotenv import dotenv_values
from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, PositiveInt, ValidationError, model_validator

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None  # type: ignore[assignment]

try:
    import pytesseract
except ImportError:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore[assignment]

# Paths ----------------------------------------------------------------------

SERVER_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
LOG_FILE = DATA_DIR / "ai_output.txt"
DB_PATH = DATA_DIR / "ai_logs.db"
PROMPTS_DIR = SERVER_DIR / "prompts"
DOMAINS_FILE = PROMPTS_DIR / "domains.yaml"
BASE_PROMPT_FILE = PROMPTS_DIR / "base.md"

# Logging --------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")
logger = logging.getLogger("app.server.backend")


# Settings -------------------------------------------------------------------

class Settings(BaseModel):
    ai_backend: str = Field(default="ollama", alias="AI_BACKEND")
    ollama_url: str = Field(default="http://localhost:11434/api/generate", alias="OLLAMA_URL")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")

    openai_base_url: str = Field(default="http://localhost:1234/v1", alias="OPENAI_BASE_URL")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    api_key: str = Field(default="local-dev-key", alias="API_KEY")
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: PositiveInt = Field(default=8000, alias="PORT")
    question_domain: str = Field(default="", alias="QUESTION_DOMAIN")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
    }

    @model_validator(mode="after")
    def normalize_backend(self) -> "Settings":
        backend = self.ai_backend.lower().strip()
        if backend not in {"ollama", "openai_compatible"}:
            raise ValueError("AI_BACKEND must be 'ollama' or 'openai_compatible'")
        self.ai_backend = backend
        self.question_domain = self.question_domain.strip()
        return self


def load_settings() -> Settings:
    raw = dotenv_values(ROOT / ".env")
    filtered = {k: v for k, v in raw.items() if v is not None}
    try:
        return Settings.model_validate(filtered)
    except ValidationError as exc:  # pragma: no cover - surfaced at runtime
        logger.error("Invalid configuration: %s", exc)
        raise


SETTINGS = load_settings()


# Prompt loading -------------------------------------------------------------


def ensure_data_paths() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "tmp").mkdir(exist_ok=True)
    LOG_FILE.touch(exist_ok=True)


ensure_data_paths()


def load_base_prompt() -> str:
    if BASE_PROMPT_FILE.exists():
        return BASE_PROMPT_FILE.read_text(encoding="utf-8").strip()
    logger.warning("Base prompt file missing at %s", BASE_PROMPT_FILE)
    return "You are a helpful AI assistant."


def load_domain_prompts() -> Dict[str, str]:
    if not DOMAINS_FILE.exists():
        logger.warning("Domain prompt file missing at %s", DOMAINS_FILE)
        return {}
    data = yaml.safe_load(DOMAINS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        logger.warning("Domain prompts file is not a mapping.")
        return {}
    return {str(k): str(v) for k, v in data.items()}


BASE_PROMPT = load_base_prompt()
DOMAIN_PROMPTS = load_domain_prompts()
UNIVERSAL_INSTRUCTION = (
    "Respond with concise, numbered reasoning when helpful and finish with a single line "
    "that begins with 'Answer:' followed by the final result when a definitive answer exists."
)


# Models ---------------------------------------------------------------------


class GenerateContext(BaseModel):
    question_type: Optional[str] = None


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    context: GenerateContext = Field(default_factory=GenerateContext)
    model: Optional[str] = None


class GenerateResponse(BaseModel):
    status: str
    id: str
    model: str
    response: str
    final_answer: Optional[str]
    elapsed_ms: int
    valid: Optional[bool] = None
    validation: Optional[Dict[str, Any]] = None


# Dependencies ----------------------------------------------------------------


async def verify_api_key(x_api_key: Optional[str] = Header(default=None, alias="x-api-key")) -> None:
    if not x_api_key or x_api_key != SETTINGS.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")


# Utility functions -----------------------------------------------------------


def compose_system_prompt(domain_key: Optional[str]) -> str:
    parts: List[str] = [BASE_PROMPT]
    if domain_key:
        prompt = DOMAIN_PROMPTS.get(domain_key)
        if prompt:
            parts.append(prompt.strip())
    parts.append(UNIVERSAL_INSTRUCTION)
    return "\n\n".join(parts)


def extract_final_answer(text: str) -> Optional[str]:
    final_line: Optional[str] = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("answer:"):
            final_line = stripped
    return final_line


async def write_logs(entry: Dict[str, Any]) -> None:
    def _write() -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        prompt = entry["prompt"]
        response = entry["response"]
        model = entry["model"]
        backend = entry["backend"]
        domain = entry.get("domain") or ""
        valid = entry.get("valid")
        validation = entry.get("validation")
        elapsed_ms = entry["elapsed_ms"]

        with LOG_FILE.open("a", encoding="utf-8") as log_file:
            log_file.write(
                f"[{timestamp}] backend={backend} model={model} domain={domain}\n"
                f"Prompt:\n{prompt}\n\nResponse:\n{response}\n\n---\n"
            )

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    backend TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    elapsed_ms INTEGER NOT NULL,
                    domain TEXT,
                    valid INTEGER,
                    validation TEXT
                )
                """
            )
            connection.execute(
                """
                INSERT OR REPLACE INTO logs (
                    id, created_at, backend, model, prompt, response,
                    elapsed_ms, domain, valid, validation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["id"],
                    timestamp,
                    backend,
                    model,
                    prompt,
                    response,
                    elapsed_ms,
                    domain or None,
                    int(valid) if isinstance(valid, bool) else None,
                    json.dumps(validation, ensure_ascii=False) if validation else None,
                ),
            )
            connection.commit()

    await asyncio.to_thread(_write)


async def call_ollama(prompt: str, model: str) -> Tuple[str, str]:
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=120.0)) as client:
        response = await client.post(
            SETTINGS.ollama_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data.get("model", model), data.get("response", "").strip()


async def call_openai(system_prompt: str, user_prompt: str, model: str) -> Tuple[str, str]:
    headers = {"Content-Type": "application/json"}
    if SETTINGS.openai_api_key:
        headers["Authorization"] = f"Bearer {SETTINGS.openai_api_key}"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
    }
    url = SETTINGS.openai_base_url.rstrip("/") + "/chat/completions"
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=120.0)) as client:
        response = await client.post(url, json={**payload}, headers=headers)
        response.raise_for_status()
        data = response.json()
        first_choice = data.get("choices", [{}])[0]
        message = first_choice.get("message", {})
        return data.get("model", model), str(message.get("content", "")).strip()


async def invoke_llm(
    request: GenerateRequest, system_prompt: str, domain: Optional[str]
) -> Tuple[str, str]:
    model_override = request.model.strip() if request.model else ""
    backend = SETTINGS.ai_backend
    if backend == "ollama":
        resolved_model = model_override or SETTINGS.ollama_model
        user_prompt = f"{system_prompt}\n\nUser:\n{request.prompt.strip()}\n"
        return await call_ollama(user_prompt, resolved_model)
    if backend == "openai_compatible":
        resolved_model = model_override or SETTINGS.openai_model
        return await call_openai(system_prompt, request.prompt.strip(), resolved_model)
    raise HTTPException(status_code=500, detail=f"Unsupported backend '{backend}'")


def run_validator(domain: Optional[str], final_answer: Optional[str]) -> Tuple[Optional[bool], Optional[Dict[str, Any]]]:
    if domain != "subnetting":
        return None, None
    if not final_answer:
        return False, {"reason": "Final answer missing for subnetting validation."}
    try:
        from app.server.validators.ip_network import validate_answer
    except Exception as exc:  # pragma: no cover - should not happen
        logger.warning("Unable to load subnet validator: %s", exc)
        return False, {"reason": "Validator unavailable."}
    try:
        result = validate_answer(final_answer)
    except Exception as exc:  # pragma: no cover
        logger.exception("Subnet validator raised an error: %s", exc)
        return False, {"reason": "Validator error"}
    return bool(result.get("ok")), result


async def append_ocr_context(files: Optional[List[UploadFile]]) -> Tuple[str, List[str]]:
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
                    extracted_segments.append(
                        f"Text from {file.filename or 'image'}:\n{text}"
                    )
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


# FastAPI application ---------------------------------------------------------

app = FastAPI(title="AI Hotkey Backend", version="1.0.0")


@app.get("/status")
async def get_status() -> Dict[str, Any]:
    return {
        "ok": True,
        "backend": SETTINGS.ai_backend,
        "model": (
            SETTINGS.ollama_model if SETTINGS.ai_backend == "ollama" else SETTINGS.openai_model
        ),
    }


@app.post("/generate", response_model=GenerateResponse, dependencies=[Depends(verify_api_key)])
async def generate(request: GenerateRequest) -> JSONResponse:
    domain = (request.context.question_type or "").strip() or None
    if not domain and SETTINGS.question_domain:
        domain = SETTINGS.question_domain
    system_prompt = compose_system_prompt(domain)
    request_id = str(uuid.uuid4())
    started = time.perf_counter()

    try:
        model_name, response_text = await invoke_llm(request, system_prompt, domain)
    except httpx.HTTPError as exc:
        logger.exception("LLM request failed")
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    final_answer = extract_final_answer(response_text)
    is_valid, validation = run_validator(domain, final_answer)

    entry = {
        "id": request_id,
        "prompt": request.prompt,
        "response": response_text,
        "backend": SETTINGS.ai_backend,
        "model": model_name,
        "elapsed_ms": elapsed_ms,
        "domain": domain,
        "valid": is_valid,
        "validation": validation,
    }
    await write_logs(entry)

    payload = GenerateResponse(
        status="ok",
        id=request_id,
        model=model_name,
        response=response_text,
        final_answer=final_answer,
        elapsed_ms=elapsed_ms,
        valid=is_valid,
        validation=validation,
    )
    return JSONResponse(content=payload.model_dump())


@app.post(
    "/generate-with-image",
    response_model=GenerateResponse,
    dependencies=[Depends(verify_api_key)],
)
async def generate_with_image(
    prompt: str = Form(...),
    files: Optional[List[UploadFile]] = File(default=None),
) -> JSONResponse:
    request = GenerateRequest(prompt=prompt, context=GenerateContext())
    domain = SETTINGS.question_domain or None
    system_prompt = compose_system_prompt(domain)

    ocr_summary, extracted_segments = await append_ocr_context(files)

    extended_prompt_parts = [prompt]
    if extracted_segments:
        extended_prompt_parts.append(
            "Additional OCR context:\n" + "\n\n".join(extracted_segments)
        )
    if ocr_summary:
        extended_prompt_parts.append(f"[Notes]\n{ocr_summary}")
    request.prompt = "\n\n".join(extended_prompt_parts)
    if domain:
        request.context.question_type = domain

    request_id = str(uuid.uuid4())
    started = time.perf_counter()

    try:
        model_name, response_text = await invoke_llm(request, system_prompt, domain)
    except httpx.HTTPError as exc:
        logger.exception("LLM request with image failed")
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}") from exc

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    final_answer = extract_final_answer(response_text)
    is_valid, validation = run_validator(domain, final_answer)

    entry = {
        "id": request_id,
        "prompt": request.prompt,
        "response": response_text,
        "backend": SETTINGS.ai_backend,
        "model": model_name,
        "elapsed_ms": elapsed_ms,
        "domain": domain,
        "valid": is_valid,
        "validation": validation,
    }
    await write_logs(entry)

    payload = GenerateResponse(
        status="ok",
        id=request_id,
        model=model_name,
        response=response_text,
        final_answer=final_answer,
        elapsed_ms=elapsed_ms,
        valid=is_valid,
        validation=validation,
    )
    return JSONResponse(content=payload.model_dump())
