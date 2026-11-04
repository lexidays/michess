"""Data shapes shared between the reader and display layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TagRead:
    """A single NFC tag observation.

    `square` is optional because today there's only one antenna; once
    `mux.py` exists it will be populated per-scan (e.g. "a1", "b4").
    """

    uid: str
    square: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
