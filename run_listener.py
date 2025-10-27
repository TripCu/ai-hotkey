#!/usr/bin/env python3
from __future__ import annotations

import sys
import time
from pathlib import Path

from run import (
    ensure_venv,
    install_dependencies,
    parse_env_file,
    start_listener,
    terminate_process,
    venv_python,
    wait_for_status,
)

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
ENV_FILE = ROOT / ".env"


def main() -> int:
    env_values = parse_env_file(ENV_FILE)
    ensure_venv(VENV_DIR)
    python_executable = venv_python(VENV_DIR)
    if not python_executable.exists():
        raise FileNotFoundError(f"Virtual environment Python not found at {python_executable}")

    install_dependencies(python_executable)

    wait_for_status(
        env_values.get("HOST", "127.0.0.1"),
        env_values.get("PORT", "8000"),
    )
    print("Backend detected. Launching listener...")

    listener_proc = start_listener(python_executable, env_values)

    try:
        while listener_proc.poll() is None:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nStopping listener...")
    finally:
        terminate_process(listener_proc, "listener")
    return 0


if __name__ == "__main__":
    sys.exit(main())
