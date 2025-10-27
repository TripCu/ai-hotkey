from __future__ import annotations

import asyncio
import json
import logging
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

BACKEND_ROOT = Path(__file__).resolve().parent
DATA_DIR = BACKEND_ROOT / "data"
LOG_FILE = DATA_DIR / "ai_output.jsonl"
DB_PATH = DATA_DIR / "ai_logs.db"

logger = logging.getLogger("backend.storage")


def ensure_data_paths() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "tmp").mkdir(exist_ok=True)
    legacy = DATA_DIR / "ai_output.txt"
    if legacy.exists() and not LOG_FILE.exists():
        legacy.rename(LOG_FILE)
    LOG_FILE.touch(exist_ok=True)
    _ensure_sqlite_schema()


@dataclass
class LogEntry:
    id: str
    created_at: datetime
    backend: str
    model: str
    prompt: str
    response: str
    final_answer: Optional[str]
    elapsed_ms: int
    domain: Optional[str]


async def persist(entry: LogEntry) -> None:
    await asyncio.gather(
        asyncio.to_thread(_write_jsonl, entry),
        asyncio.to_thread(_safe_write_sqlite, entry),
    )


def clear_logs() -> None:
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    if DB_PATH.exists():
        DB_PATH.unlink()
    ensure_data_paths()


def get_recent_entries(limit: int = 5) -> list[dict[str, str]]:
    if not DB_PATH.exists():
        return []
    results: list[dict[str, str]] = []
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT prompt, response FROM logs ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        for row in reversed(rows):
            results.append({"prompt": row["prompt"], "response": row["response"]})
    return results


def _write_jsonl(entry: LogEntry) -> None:
    payload = asdict(entry)
    payload["created_at"] = entry.created_at.isoformat()
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _safe_write_sqlite(entry: LogEntry) -> None:
    try:
        _write_sqlite(entry)
    except sqlite3.OperationalError as exc:
        logger.warning("SQLite write failed (will continue with JSONL only): %s", exc)
    except sqlite3.DatabaseError as exc:  # pragma: no cover
        logger.warning("SQLite database error: %s", exc)


def _write_sqlite(entry: LogEntry) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
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
                final_answer TEXT,
                elapsed_ms INTEGER NOT NULL,
                domain TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT OR REPLACE INTO logs (
                id,
                created_at,
                backend,
                model,
                prompt,
                response,
                final_answer,
                elapsed_ms,
                domain
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.id,
                entry.created_at.isoformat(),
                entry.backend,
                entry.model,
                entry.prompt,
                entry.response,
                entry.final_answer,
                entry.elapsed_ms,
                entry.domain,
            ),
        )
        connection.commit()


def _ensure_sqlite_schema() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
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
                final_answer TEXT,
                elapsed_ms INTEGER NOT NULL,
                domain TEXT
            )
            """
        )
        columns = {row[1] for row in connection.execute("PRAGMA table_info('logs')")}
        if "final_answer" not in columns:
            connection.execute("ALTER TABLE logs ADD COLUMN final_answer TEXT")
        connection.commit()
