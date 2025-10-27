from __future__ import annotations

import re
from pathlib import Path
from typing import List

from backend.config import get_settings

MARKDOWN_EXTENSIONS = {".md", ".markdown", ".mdx"}
MAX_NOTE_CHARS = 1200


def gather_relevant_notes(query: str, limit: int = 3) -> List[str]:
    settings = get_settings()
    notes_root = settings.notes_path
    if not notes_root:
        return []

    base_path = (Path(notes_root) if Path(notes_root).is_absolute() else Path(__file__).resolve().parents[1] / notes_root)
    if not base_path.exists() or not base_path.is_dir():
        return []

    query_terms = _tokenize(query)
    if not query_terms:
        return []

    scored: list[tuple[int, Path]] = []
    for path in base_path.rglob("*"):
        if path.is_file() and path.suffix.lower() in MARKDOWN_EXTENSIONS:
            score = _score_file(path, query_terms)
            if score > 0:
                scored.append((score, path))

    scored.sort(key=lambda item: item[0], reverse=True)
    excerpts: List[str] = []
    for _, path in scored[:limit]:
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue
        snippets = content.strip().splitlines()
        snippet_text = "\n".join(snippets[: MAX_NOTE_CHARS // 80])
        excerpts.append(f"### Note: {path.name}\n{snippet_text[:MAX_NOTE_CHARS].strip()}")
    return excerpts


def _tokenize(text: str) -> set[str]:
    return {token for token in re.split(r"\W+", text.lower()) if token}


def _score_file(path: Path, terms: set[str]) -> int:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return 0
    lowered = content.lower()
    score = 0
    for term in terms:
        if term in lowered:
            score += lowered.count(term)
    return score
