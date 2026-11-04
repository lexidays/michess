"""Tkinter display for tag reads.

Today: a single window showing the last UID seen. Later: swap this
class out for a grid with one cell per square. `main.py`'s call to
`display.update(...)` shouldn't need to change either way.
"""

from __future__ import annotations

import tkinter as tk
from typing import Callable

from .models import TagRead


class TkConsole:
    """Single-label window showing the most recent tag read."""

    WINDOW_TITLE = "NFC Matrix Tester"
    WINDOW_GEOMETRY = "400x150"

    STATUS_FONT = ("monospace", 14)
    UID_FONT = ("monospace", 20, "bold")

    WAITING_TEXT = "Waiting for a tag..."
    NO_UID_TEXT = "--"

    # Default interval (ms) between polls of the reader callback.
    DEFAULT_POLL_INTERVAL_MS = 250

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.WINDOW_GEOMETRY)

        self._status = tk.Label(self.root, text=self.WAITING_TEXT, font=self.STATUS_FONT)
        self._status.pack(expand=True)

        self._uid_var = tk.StringVar(value=self.NO_UID_TEXT)
        self._uid_label = tk.Label(
            self.root, textvariable=self._uid_var, font=self.UID_FONT
        )
        self._uid_label.pack(expand=True)

    def update(self, tag_read: TagRead | None) -> None:
        if tag_read is None:
            self._status.config(text=self.WAITING_TEXT)
            return
        self._status.config(text=f"Tag seen at {tag_read.timestamp:%H:%M:%S}")
        self._uid_var.set(tag_read.uid)

    def poll(
        self,
        callback: Callable[[], TagRead | None],
        interval_ms: int = DEFAULT_POLL_INTERVAL_MS,
    ) -> None:
        """Call `callback()` every `interval_ms` and feed the result to `update`."""

        def _tick() -> None:
            self.update(callback())
            self.root.after(interval_ms, _tick)

        self.root.after(interval_ms, _tick)

    def run(self) -> None:
        self.root.mainloop()
