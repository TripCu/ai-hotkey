from __future__ import annotations

import asyncio
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Deque, Dict, Optional

import psutil

logger = logging.getLogger("backend.telemetry")


@dataclass
class RequestEvent:
    timestamp: datetime
    client_ip: str
    api_key: str
    prompt_length: int


@dataclass
class TelemetryState:
    total_requests: int = 0
    last_request_at: Optional[datetime] = None
    events: Deque[RequestEvent] = field(default_factory=lambda: deque(maxlen=50))
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_used_mb: float = 0.0
    disk_percent: float = 0.0

    def snapshot(self) -> Dict[str, object]:
        return {
            "total_requests": self.total_requests,
            "last_request_at": self.last_request_at.isoformat() if self.last_request_at else None,
            "recent_requests": [
                {
                    "timestamp": event.timestamp.isoformat(),
                    "client_ip": event.client_ip,
                    "api_key": event.api_key,
                    "prompt_length": event.prompt_length,
                }
                for event in list(self.events)
            ],
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_used_mb": round(self.memory_used_mb, 2),
            "disk_percent": self.disk_percent,
        }


state = TelemetryState()


def record_request(client_ip: str, api_key: str, prompt_length: int) -> None:
    state.total_requests += 1
    state.last_request_at = datetime.now(timezone.utc)
    state.events.append(RequestEvent(state.last_request_at, client_ip, api_key, prompt_length))
    logger.info("Telemetry | request #%s from %s (key=%s) length=%s", state.total_requests, client_ip, api_key or "<none>", prompt_length)


async def monitor_resources(interval: float = 10.0) -> None:
    process = psutil.Process()
    while True:
        try:
            state.cpu_percent = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            state.memory_percent = mem.percent
            state.memory_used_mb = mem.used / (1024 * 1024)
            try:
                disk = psutil.disk_usage(str(process.cwd()))
                state.disk_percent = disk.percent
            except Exception:  # pragma: no cover
                state.disk_percent = 0.0
        except Exception as exc:  # pragma: no cover
            logger.warning("Telemetry monitor error: %s", exc)
        await asyncio.sleep(interval)


def get_metrics() -> Dict[str, object]:
    return state.snapshot()
