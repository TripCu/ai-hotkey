# AI Hotkey Assistant

Trigger a local LLM with a global hotkey. `run.py` bootstraps everything: creates a virtual environment, installs dependencies, ensures Ollama is installed, launches the backend, and starts the listener plus overlay. The backend can also call an OpenAI-compatible endpoint, performs optional OCR, and enriches prompts with recent chat history and Markdown notes.

---

## Highlights
- One-command startup (`python run.py`) across macOS, Windows, and Linux.
- Neon floating overlay + console output, with configurable hotkeys (capture, clipboard paste, exit).
- Context-aware prompting: merges recent chat history and relevant Markdown/Obsidian notes.
- FastAPI backend with API-key auth, `/generate-with-image`, and pluggable Ollama/OpenAI backends.
- All paths are relative; move the folder anywhere and it still works.

## Repository Layout
```
ai-hotkey/
  run.py
  requirements.txt
  README.md
  .env
  notes/
    README.md          # drop Markdown notes here (or point NOTES_PATH elsewhere)

  client/
    __init__.py
    config.py
    listener.py
    overlay.py

  backend/
    __init__.py
    backend.py
    data/
      tmp/
    config.py
    clients/
      __init__.py
      ollama_client.py
      openai_client.py
    notes.py
    prompts/
      base.md
      domains.yaml
    prompts_loader.py
    services/
      __init__.py
      generation.py
    storage.py
    telemetry.py
```

## Requirements
- Python 3.9+
  - Windows installers **must** use Python 3.9–3.12 (Pillow wheels are not yet available for 3.13/3.14 on Windows).
- Ollama (auto-installed on macOS/Linux; Windows uses the official installer run by `run.py`)
- Optional: Tesseract OCR binary for `/generate-with-image`
- Optional: OpenCV (`opencv-python`) for improved OCR preprocessing

## Quick Start

## Quick Start

> **One-Time Bootstrap (all platforms)**
```bash
git clone https://github.com/your-org/ai-hotkey.git
cd ai-hotkey
python -m venv .venv  # use `python3` on macOS/Linux
```

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python run.py
```

Or automate everything with the bundled helper:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned  # first time only
PowerShell -ExecutionPolicy Bypass -File scripts/setup_windows.ps1 -Mode full
```

Use `-Mode backend` or `-Mode listener` for the one-off scripts.

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py

### What `python run.py` does
1. Creates/updates the virtualenv and installs Python dependencies.
2. Installs Ollama if missing (Homebrew/pkg on macOS, install script on Linux; Windows uses the official installer).
3. Starts (or reuses) the Ollama daemon and pulls `OLLAMA_MODEL`.
4. Clears previous chat logs for a fresh session.
5. Launches the FastAPI backend on `HOST:PORT`.
6. Waits for `/status` to report healthy, then starts the listener + overlay.

### Backend or Listener Only
- `python backend/run_backend.py` — start only the API backend (plus Ollama daemon). The script stays running until you press Ctrl+C.
- `python client/run_listener.py` — start only the hotkey listener/overlay. Ensure the backend is already reachable on `HOST:PORT` before launching.

### Single-User vs Multi-User
- **Solo workflow**: run `python run.py` on your machine — it launches both backend and listener locally.
- **Shared workflow**:
  1. On the host machine (where the LLM and notes live):
     - Set `.env:HOST=0.0.0.0` (or a specific interface IP).
     - Ensure `API_KEY` is a secret value.
    - Run `python backend/run_backend.py` and keep it running. Open TCP port `PORT` (default `8000`) in your firewall.
  2. On each client machine:
     - Copy the repo (or distribute a packaged release).
     - In `.env`, set `HOST=<server-ip>` and use the same `API_KEY`.
    - Run `python client/run_listener.py` to connect to the shared backend.

Clients inherit the same overlay, clipboard key, and note-search behaviour, but only the host needs the Ollama installation and Markdown vault.
```

First launch may prompt for admin rights (Ollama install) and will download the default model (`llama3.1:8b`). Subsequent runs reuse cached models/daemon if available.

## Hotkeys & Overlay
1. Press the start key (default backtick `) to begin capture.
2. Type your prompt and hit Enter — or press the clipboard key (default `\`) to send your clipboard instantly.
3. Responses appear in the terminal and in a neon overlay pinned to the top‑right. Click or press Esc to dismiss; it auto-hides after `OVERLAY_DURATION` seconds.
4. Press the exit key (default `ESC`) to stop the listener and shut everything down.

## Configuration (`.env`)
| Key | Description |
|-----|-------------|
| `AI_BACKEND` | `ollama` (default) or `openai_compatible` |
| `OLLAMA_MODEL` | Model tag to pull/use (default `llama3.1:8b`) |
| `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` | Set when using an OpenAI-compatible backend |
| `HOST`, `PORT` | Backend bind host/port |
| `API_KEY` | Required `x-api-key` header value |
| `START_KEY`, `EXIT_KEY`, `CLIPBOARD_KEY` | Hotkeys for capture/exit/clipboard |
| `OVERLAY_ENABLED`, `OVERLAY_DURATION`, `OVERLAY_OPACITY`, `OVERLAY_WIDTH` | Overlay settings |
| `QUESTION_DOMAIN` | Optional domain hint (e.g., `networking`) |
| `NOTES_PATH` | Relative or absolute folder containing Markdown notes |

All prompts/responses are logged locally (JSONL + SQLite) in `backend/data/`. Each run wipes previous logs, so every session is clean. 

## Notes Integration
Add Markdown files to `notes/` (or point `NOTES_PATH` elsewhere). The backend scores the files for keyword overlap and injects the most relevant snippets into the LLM context. Large files are truncated to ~1,200 characters per response. To keep proprietary notes private, store them in a nested folder like `notes/private/` (already ignored in `.gitignore`).

## Backend Options
- **Ollama**: default. `run.py` will attempt to install/start Ollama if needed and pull the configured model.
- **OpenAI-compatible**: set `AI_BACKEND=openai_compatible` and supply base URL, API key, and model in `.env`.

## Image Notes
`POST /generate-with-image` accepts multipart uploads (prompt + images). If Pillow + pytesseract + Tesseract OCR are available, the backend extracts text from the images and appends it to the prompt; otherwise it returns a response noting OCR is unavailable.

## Security Notice
The listener installs a global keyboard hook; run it only on trusted machines and disable it when entering sensitive information. No data leaves your machine unless your chosen backend sends prompts to a remote service.

## Contributing / Publishing Checklist
- Remove secrets from `.env` before committing.
- Update `requirements.txt` if you add dependencies.
- Add tests or smoke scripts where possible (`pytest` recommended).
- Consider enabling GitHub Actions (lint/test) before making the repo public.

Happy automating!
