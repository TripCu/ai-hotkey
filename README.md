# AI Hotkey Assistant

A portable Python project that lets you trigger a local LLM helper with a single hotkey.  
The bootstrap script spins up a FastAPI backend, a global keyboard listener, and handles
prompt routing to Ollama or any OpenAI-compatible server.

## Highlights

- Cross-platform bootstrap (`run.py`) that builds a local virtualenv, installs dependencies, and launches both backend and listener.
- FastAPI backend with API-key protection, text-and-image generation endpoints, logging to SQLite and plain text.
- Hotkey-driven client built on `pynput`, configurable start/exit keys, and domain-aware prompting.
- Optional subnetting validator with structured feedback.
- Native support for locally hosted Ollama models (`llama3.1:8b` by default) plus OpenAI-compatible endpoints.
- Pure relative paths so the folder can be moved between machines unchanged.

## Folder Layout

```
ai-hotkey/
  run.py
  requirements.txt
  README.md
  .env

  app/
    client/
      listener.py
    server/
      backend.py
      prompts/
        base.md
        domains.yaml
      validators/
        ip_network.py

  data/
    ai_output.txt
    ai_logs.db
    tmp/
```

## Prerequisites

- Python 3.9 or newer on macOS, Windows, or Linux.
- Optional for image prompts: Tesseract OCR binary on your PATH.

## Configuration

Edit `.env` to adjust backend selection, hotkeys, ports, or default domain hints.  
The project reads configuration directly from the file; exporting environment variables is not required.

## Running the App

```bash
python run.py
```

The script will create `.venv/`, install dependencies, attempt to install Ollama (macOS via Homebrew/pkg, Windows via the official installer, Linux via install.sh), pull the configured model, launch the Ollama daemon if needed, start the backend on the requested host/port, wait until it reports healthy, then connect the hotkey listener. Some steps may prompt for administrative credentials when package managers or system installers require them.

## Using the Hotkey Listener

1. Focus any window where you can type text.
2. Press the start key (` by default) to begin capture.
3. Type your prompt and press Enter.
4. The full response appears both in the console and in a floating overlay window (click or press Esc on the overlay to dismiss). The overlay auto-hides after the configured timeout.
5. Press the exit key (ESC by default) to stop the listener and shut everything down gracefully.

All prompts and responses are appended (one JSON object per line) to `data/ai_output.jsonl` and stored in SQLite (`data/ai_logs.db`).

## Recommended Ollama Models

The default backend uses Ollama. Suggested models:

- General-purpose coding & troubleshooting: `ollama run llama3.1:8b` (balanced quality and speed).
- Lightweight helper for lower-powered machines: `ollama run phi3:3.8b`.
- Networking and infrastructure reasoning with larger context: `ollama run mistral-large:latest` (requires more RAM/VRAM).
- Multimodal/image-ready options for future `/generate-with-image` support: `ollama run llama3.2-vision`, `ollama run llava:13b`, or `ollama run bakllava:7b`. These models can read images once you enable OCR/payload handling on the backend.

Install a model by running `ollama pull <model-name>`. Update `.env` `OLLAMA_MODEL` to match the tag you pulled.

## Switching Model Backends

- `ollama` (default): Call a local Ollama REST API (`OLLAMA_URL` / `OLLAMA_MODEL`, defaults to `llama3.1:8b`).
- `openai_compatible`: Send chat completions to any OpenAI-style endpoint.
- Optional: set `QUESTION_DOMAIN=networking` to bias prompt hints and validator usage.
- Overlay controls:
  - `OVERLAY_ENABLED` (default `true`)
  - `OVERLAY_DURATION` in seconds before auto-dismiss (default `15`)
  - `OVERLAY_OPACITY` between `0` and `1`
  - `OVERLAY_WIDTH` in pixels for text wrapping

You can override the default model per request by including `"model": "..."` in the JSON payload.

## Image Notes

The `/generate-with-image` endpoint accepts multipart form uploads. If Pillow and pytesseract are installed and Tesseract is available, the backend will OCR the images and append the text to the prompt before calling the LLM. Otherwise it reports that OCR is unavailable while still returning a model response.

## Security Notice

The hotkey listener installs a global keyboard hook. Only run the tool on machines you trust and disable it before entering sensitive information.

<!--
Acceptance Tests
1. python run.py creates .venv if missing, installs deps, starts backend, then starts listener.
2. GET /status returns JSON with ok=true within 10 seconds of boot.
3. Trigger hotkey, type “What’s 2+2? End with Answer line.” Then press Enter → console prints a response and a line FINAL: 4 (or similar); data/ai_output.txt is appended.
4. Set .env:AI_BACKEND=openai_compatible and OPENAI_BASE_URL to a local proxy (or leave default); server still runs and responds (if upstream reachable).
5. Set .env:QUESTION_DOMAIN=subnetting and ask a subnetting question → response contains steps and an Answer: with CIDR-style outputs; validator populates valid and validation.
6. /generate-with-image succeeds even if OCR isn’t available, returning a response that notes OCR absence.
-->
