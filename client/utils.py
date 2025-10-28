from __future__ import annotations

import platform
import subprocess
import tempfile
import uuid
from pathlib import Path


class ScreenshotError(RuntimeError):
    """Raised when a screenshot cannot be captured."""


def capture_screenshot(prefix: str = "screenshot") -> Path:
    """Capture a screenshot to a temporary PNG file and return the path."""

    system = platform.system().lower()

    tmp_dir = Path(tempfile.gettempdir())
    tmp_dir.mkdir(parents=True, exist_ok=True)
    output_path = tmp_dir / f"{prefix}-{uuid.uuid4().hex}.png"

    try:
        if system == "darwin":
            subprocess.run([
                "/usr/sbin/screencapture",
                "-i",
                "-t",
                "png",
                str(output_path),
            ], check=True)
        elif system == "windows":
            try:
                import pyautogui  # type: ignore[import-untyped]
            except ImportError:
                try:
                    from PIL import ImageGrab  # type: ignore[import-untyped]
                except ImportError as exc:  # pragma: no cover - optional dep
                    raise ScreenshotError("Install Pillow or pyautogui for screenshot support on Windows.") from exc
                image = ImageGrab.grab()
            else:
                image = pyautogui.screenshot()
            image.save(output_path, format="PNG")
        else:
            try:
                import pyautogui  # type: ignore[import-untyped]
            except ImportError:
                try:
                    subprocess.run([
                        "scrot",
                        "-s",
                        str(output_path),
                    ], check=True)
                except FileNotFoundError:
                    raise ScreenshotError(
                        "Install pyautogui or scrot to enable screenshot capture on this platform."
                    )
            else:
                image = pyautogui.screenshot()
                image.save(output_path, format="PNG")
    except Exception as exc:
        raise ScreenshotError(f"Failed to capture screenshot: {exc}")

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise ScreenshotError("Screenshot capture produced no output.")

    return output_path
