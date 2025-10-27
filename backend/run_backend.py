#!/usr/bin/env python3
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.storage import clear_logs
from run import (
    ensure_ollama_installed,
    ensure_ollama_model,
    ensure_ollama_running,
    ensure_venv,
    install_dependencies,
    parse_env_file,
    start_backend,
    terminate_process,
    venv_python,
    wait_for_status,
)
VENV_DIR = ROOT / ".venv"
ENV_FILE = ROOT / ".env"


def main() -> int:
    env_values = parse_env_file(ENV_FILE)
    ensure_venv(VENV_DIR)
    python_executable = venv_python(VENV_DIR)
    if not python_executable.exists():
        raise FileNotFoundError(f"Virtual environment Python not found at {python_executable}")

    install_dependencies(python_executable)
    clear_logs()
    ensure_ollama_installed(env_values)
    ollama_proc = ensure_ollama_running(env_values)
    ensure_ollama_model(env_values)

    backend_proc = start_backend(python_executable, env_values)

    try:
        wait_for_status(
            env_values.get("HOST", "127.0.0.1"),
            env_values.get("PORT", "8000"),
            process=backend_proc,
        )
        print("Backend is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1.0)
            if backend_proc is not None and backend_proc.poll() is not None:
                raise RuntimeError("Backend process exited unexpectedly.")
    except KeyboardInterrupt:
        print("\nStopping backend...")
    finally:
        terminate_process(backend_proc, "backend")
        terminate_process(ollama_proc, "ollama daemon")
    return 0


if __name__ == "__main__":
    sys.exit(main())
