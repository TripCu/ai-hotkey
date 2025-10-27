#!/usr/bin/env python3
from __future__ import annotations

import errno
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import venv
from pathlib import Path
from typing import Dict, Optional
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen, urlretrieve

from backend.storage import clear_logs

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS_FILE = ROOT / "requirements.txt"
ENV_FILE = ROOT / ".env"


def parse_env_file(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    if not path.exists():
        return env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def ensure_venv(venv_dir: Path) -> None:
    if venv_dir.exists():
        return
    print("Creating virtual environment...")
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_dir)


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def install_dependencies(python_executable: Path) -> None:
    if not REQUIREMENTS_FILE.exists():
        raise FileNotFoundError("requirements.txt not found")
    print("Installing dependencies...")
    subprocess.check_call(
        [
            str(python_executable),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        cwd=str(ROOT),
    )
    subprocess.check_call(
        [str(python_executable), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        cwd=str(ROOT),
    )


def ensure_ollama_installed(env: Dict[str, str]) -> None:
    backend = (env.get("AI_BACKEND") or "").strip().lower()
    if backend != "ollama":
        return

    if shutil.which("ollama") is not None:
        return

    system = platform.system().lower()
    print("Ollama CLI not found. Attempting automatic installation...")

    try:
        if system == "darwin":
            if shutil.which("brew") is not None:
                result = subprocess.run(
                    ["brew", "install", "ollama/tap/ollama"],
                    check=False,
                )
                if result.returncode == 0 and shutil.which("ollama") is not None:
                    print("Ollama installed via Homebrew.")
                    return
            pkg_url = "https://ollama.com/download/Ollama-darwin.pkg"
            with tempfile.TemporaryDirectory() as tmp_dir:
                pkg_path = Path(tmp_dir) / "Ollama.pkg"
                print("Downloading Ollama installer (macOS)...")
                urlretrieve(pkg_url, pkg_path)
                print("Running installer (may prompt for sudo password)...")
                subprocess.check_call([
                    "sudo",
                    "installer",
                    "-pkg",
                    str(pkg_path),
                    "-target",
                    "/",
                ])
        elif system == "windows":
            installer_url = "https://ollama.com/download/OllamaSetup.exe"
            with tempfile.TemporaryDirectory() as tmp_dir:
                installer_path = Path(tmp_dir) / "OllamaSetup.exe"
                print("Downloading Ollama installer (Windows)...")
                urlretrieve(installer_url, installer_path)
                print("Running installer (may prompt for UAC confirmation)...")
                result = subprocess.run(
                    [str(installer_path), "/S"],
                    check=False,
                )
                if result.returncode != 0:
                    print("Silent install failed, retrying without /S switch...")
                    subprocess.check_call([str(installer_path)])
            program_files = os.getenv("ProgramFiles", r"C:\\Program Files")
            candidate = Path(program_files) / "Ollama" / "ollama.exe"
            if candidate.exists():
                os.environ["PATH"] = str(candidate.parent) + os.pathsep + os.environ.get("PATH", "")
        else:
            print("Installing Ollama using official install.sh script (Linux)...")
            subprocess.check_call(
                ["/bin/sh", "-c", "curl -fsSL https://ollama.com/install.sh | sh"]
            )
    except subprocess.CalledProcessError as exc:
        print(f"Warning: Automatic Ollama installation failed ({exc}). Please install manually from https://ollama.com/download.")

    if shutil.which("ollama") is None:
        print("Ollama CLI still not found after automated attempts. Manual installation may be required before continuing.")


def ensure_ollama_model(env: Dict[str, str]) -> None:
    backend = (env.get("AI_BACKEND") or "").strip().lower()
    if backend != "ollama":
        return

    model = (env.get("OLLAMA_MODEL") or "llama3.1:8b").strip() or "llama3.1:8b"
    if shutil.which("ollama") is None:
        print("Warning: 'ollama' CLI not found. Skipping model pull.")
        return

    try:
        list_result = subprocess.run(
            ["ollama", "list"],
            check=False,
            capture_output=True,
            text=True,
        )
        if list_result.returncode == 0:
            for line in list_result.stdout.splitlines()[1:]:
                name = line.split()[0] if line.split() else ""
                if name == model:
                    print(f"Ollama model '{model}' already available.")
                    return
    except Exception as exc:
        print(f"Warning: Unable to check existing Ollama models ({exc}). Continuing with pull attempt.")

    print(f"Pulling Ollama model '{model}'...")
    pull_result = subprocess.run(["ollama", "pull", model])
    if pull_result.returncode != 0:
        print(
            "Warning: Ollama model pull failed. Ensure the Ollama daemon is running and the model name is correct."
        )
    else:
        print(f"Model '{model}' pull completed.")


def get_ollama_base_url(env: Dict[str, str]) -> str:
    url = env.get("OLLAMA_URL", "http://localhost:11434/api/generate")
    if "/api/" in url:
        return url.split("/api/", 1)[0]
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port
    scheme = parsed.scheme or "http"
    if port is None:
        port = 443 if scheme == "https" else 80
    return f"{scheme}://{host}:{port}"


def ollama_service_ready(base_url: str, timeout: float = 2.0) -> bool:
    try:
        req = Request(f"{base_url}/api/version")
        with urlopen(req, timeout=timeout) as resp:
            return resp.getcode() == 200
    except Exception:
        return False


def ensure_ollama_running(env: Dict[str, str]) -> Optional[subprocess.Popen]:
    backend = (env.get("AI_BACKEND") or "").strip().lower()
    if backend != "ollama":
        return None

    if shutil.which("ollama") is None:
        return None

    base_url = get_ollama_base_url(env)
    if ollama_service_ready(base_url):
        return None

    print("Starting Ollama daemon...")
    creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    try:
        proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )
    except FileNotFoundError:
        print("Failed to start Ollama daemon: binary not found after installation attempts.")
        return None

    start = time.monotonic()
    timeout = 30.0
    while time.monotonic() - start < timeout:
        if proc.poll() is not None:
            print("Ollama daemon exited unexpectedly during startup.")
            return None
        if ollama_service_ready(base_url):
            print("Ollama daemon is ready.")
            return proc
        time.sleep(1.0)

    print("Warning: Ollama daemon did not become ready within 30 seconds. Continuing, but LLM calls may fail.")
    return proc


def backend_available(env: Dict[str, str]) -> bool:
    host = env.get("HOST", "127.0.0.1")
    port = env.get("PORT", "8000")
    url = f"http://{host}:{port}/status"
    try:
        with urlopen(Request(url), timeout=3.0) as response:
            return response.getcode() == 200
    except URLError:
        return False


def start_backend(python_executable: Path, env: Dict[str, str]) -> Optional[subprocess.Popen]:
    host = env.get("HOST", "127.0.0.1")
    port = env.get("PORT", "8000")

    if backend_available(env):
        print(f"Backend already running on {host}:{port}, reusing existing instance.")
        return None

    cmd = [
        str(python_executable),
        "-m",
        "uvicorn",
        "backend.backend:app",
        "--host",
        host,
        "--port",
        port,
    ]
    print(f"Starting backend on {host}:{port} ...")
    creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    child_env = {**os.environ, **env}
    child_env["PYTHONPATH"] = f"{ROOT}{os.pathsep}" + child_env.get("PYTHONPATH", "")
    try:
        return subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            env=child_env,
            creationflags=creationflags,
        )
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            raise RuntimeError(
                f"Port {port} is already in use. Stop the existing service on that port or update HOST/PORT in .env."
            ) from exc
        raise


def wait_for_status(
    host: str, port: str, timeout: float = 30.0, process: Optional[subprocess.Popen] = None
) -> None:
    url = f"http://{host}:{port}/status"
    start = time.monotonic()
    while True:
        try:
            request = Request(url)
            with urlopen(request, timeout=5.0) as response:
                if response.getcode() == 200:
                    return
        except URLError:
            pass
        if process is not None and process.poll() is not None:
            raise RuntimeError("Backend process exited during startup.")
        if time.monotonic() - start > timeout:
            raise TimeoutError(f"Backend did not report healthy within {timeout} seconds")
        time.sleep(1.0)


def start_listener(python_executable: Path, env: Dict[str, str]) -> subprocess.Popen:
    print("Starting hotkey listener...")
    cmd = [str(python_executable), "-m", "client.listener"]
    creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    child_env = {**os.environ, **env}
    child_env["PYTHONPATH"] = f"{ROOT}{os.pathsep}" + child_env.get("PYTHONPATH", "")
    return subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        env=child_env,
        creationflags=creationflags,
    )


def terminate_process(proc: Optional[subprocess.Popen], name: str) -> None:
    if proc is None:
        return
    if proc.poll() is not None:
        return
    print(f"Stopping {name}...")
    try:
        if os.name == "nt":
            ctrl_break = getattr(signal, "CTRL_BREAK_EVENT", signal.SIGTERM)
            proc.send_signal(ctrl_break)
        else:
            proc.send_signal(signal.SIGINT)
        proc.wait(timeout=8)
    except Exception:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def main() -> int:
    env_values = parse_env_file(ENV_FILE)
    ensure_venv(VENV_DIR)
    python_executable = venv_python(VENV_DIR)
    if not python_executable.exists():
        raise FileNotFoundError(f"Virtual environment Python not found at {python_executable}")

    install_dependencies(python_executable)
    clear_logs()
    ensure_ollama_installed(env_values)
    ollama_proc: Optional[subprocess.Popen] = ensure_ollama_running(env_values)
    ensure_ollama_model(env_values)
    backend_proc: Optional[subprocess.Popen] = start_backend(python_executable, env_values)
    listener_proc: Optional[subprocess.Popen] = None

    try:
        wait_for_status(
            env_values.get("HOST", "127.0.0.1"),
            env_values.get("PORT", "8000"),
            process=backend_proc,
        )
        print("Backend is ready.")
        listener_proc = start_listener(python_executable, env_values)

        while True:
            time.sleep(1.0)
            if backend_proc is not None and backend_proc.poll() is not None:
                raise RuntimeError("Backend process exited unexpectedly.")
            if listener_proc.poll() is not None:
                print("Listener stopped, shutting down backend...")
                break
    except KeyboardInterrupt:
        print("\nReceived interrupt, shutting down...")
    finally:
        terminate_process(listener_proc, "listener")
        terminate_process(backend_proc, "backend")
        terminate_process(ollama_proc, "ollama daemon")
    return 0


if __name__ == "__main__":
    sys.exit(main())
