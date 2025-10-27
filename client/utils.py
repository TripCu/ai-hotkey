from __future__ import annotations

import platform
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class ScreenshotError(RuntimeError):
    """Raised when a screenshot cannot be captured."""


def capture_screenshot(prefix: str = "screenshot") -> Path:
    """Capture a screenshot to a temporary PNG file and return the path."""

    system = platform.system().lower()

    tmp_dir = Path(tempfile.gettempdir())
    tmp_dir.mkdir(parents=True, exist_ok=True)
    output_path = tmp_dir / f"{prefix}-{next(tempfile._get_candidate_names())}.png"  # type: ignore[attr-defined]

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
            from PIL import ImageGrab  # type: ignore[import-untyped]

            image = ImageGrab.grab()
            image.save(output_path, format="PNG")
        else:
            try:
                subprocess.run([
                    "scrot",
                    "-s",
                    str(output_path),
                ], check=True)
            except FileNotFoundError:
                raise ScreenshotError("scrot not installed. Install it or configure a custom capture command.")
    except Exception as exc:
        raise ScreenshotError(f"Failed to capture screenshot: {exc}")

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise ScreenshotError("Screenshot capture produced no output.")

    return output_path
