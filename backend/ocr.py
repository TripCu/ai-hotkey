from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Iterable, List, Tuple

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None  # type: ignore[assignment]

try:
    import pytesseract
except ImportError:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore[assignment]

try:
    import cv2  # type: ignore[import-untyped]
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore[assignment]
    np = None  # type: ignore[assignment]


class OCRError(RuntimeError):
    """Base error raised when OCR processing fails."""


class OCRUnavailableError(OCRError):
    """Raised when OCR dependencies are missing."""


@dataclass(frozen=True)
class OCRSegment:
    text: str
    left: int
    top: int
    width: int
    height: int
    confidence: float


_DEPENDENCY_NOTES: List[str] = []
if Image is None:
    _DEPENDENCY_NOTES.append("Pillow not installed")
if pytesseract is None:
    _DEPENDENCY_NOTES.append("pytesseract/Tesseract not installed")

OCR_AVAILABLE = not _DEPENDENCY_NOTES


def dependency_hint() -> str:
    if not _DEPENDENCY_NOTES:
        return "OCR ready."
    return "OCR unavailable: " + ", ".join(_DEPENDENCY_NOTES)


def _preprocess_image(image: Image.Image) -> Image.Image:
    """Apply basic denoising/thresholding when OpenCV is available."""
    if cv2 is None or np is None:
        return image

    array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )
    cleaned = cv2.bitwise_not(thresh)
    return Image.fromarray(cleaned)


def extract_text_from_image(
    data: bytes,
    *,
    languages: Iterable[str] = ("eng",),
) -> Tuple[str, List[OCRSegment]]:
    if not OCR_AVAILABLE:
        raise OCRUnavailableError(dependency_hint())

    lang = "+".join(filter(None, languages)) or "eng"

    try:
        with Image.open(BytesIO(data)) as raw:
            image = raw.convert("RGB")
    except Exception as exc:  # pragma: no cover - depends on PIL
        raise OCRError(f"Unable to open image: {exc}") from exc

    processed = _preprocess_image(image)

    try:
        text = pytesseract.image_to_string(processed, lang=lang).strip()
    except Exception as exc:  # pragma: no cover - pytesseract runtime
        raise OCRError(f"OCR failed: {exc}") from exc

    segments: List[OCRSegment] = []
    try:
        data_dict = pytesseract.image_to_data(
            processed,
            lang=lang,
            output_type=pytesseract.Output.DICT,  # type: ignore[attr-defined]
        )
    except Exception:  # pragma: no cover - data output optional
        data_dict = {}

    if data_dict:
        for idx, word in enumerate(data_dict.get("text", [])):
            word = (word or "").strip()
            if not word:
                continue
            try:
                segment = OCRSegment(
                    text=word,
                    left=int(data_dict.get("left", [0])[idx]),
                    top=int(data_dict.get("top", [0])[idx]),
                    width=int(data_dict.get("width", [0])[idx]),
                    height=int(data_dict.get("height", [0])[idx]),
                    confidence=float(data_dict.get("conf", [0])[idx]),
                )
            except (ValueError, TypeError):
                continue
            segments.append(segment)

    return text, segments
