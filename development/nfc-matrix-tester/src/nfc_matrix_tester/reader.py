"""Interface to a single PN532 NFC reader.

Today this talks to one PN532 over one antenna via I2C. When the
multiplexer is introduced, `mux.py` will sit in front of this and
switch antenna channels between calls to `read_tag()`. This module
shouldn't need to change for that.

Wiring assumed: PN532 in I2C mode, connected to the Pi's SCL/SDA pins.
If you've wired it for SPI or UART instead, swap the import and the
constructor body below for the matching adafruit_pn532 class.
"""

from __future__ import annotations

import board
import busio
from adafruit_pn532.i2c import PN532_I2C

from .models import TagRead


class PN532Reader:
    """Thin wrapper around the PN532 driver for a single antenna."""

    # Default timeout (seconds) used when polling for a tag. Lives on the
    # class rather than the module so other reader classes added later
    # (e.g. once the multiplexer arrives) can set their own default.
    DEFAULT_READ_TIMEOUT = 0.5

    def __init__(self) -> None:
        i2c = busio.I2C(board.SCL, board.SDA)
        self._pn532 = PN532_I2C(i2c, debug=False)
        self._pn532.SAM_configuration()

    def read_tag(self, timeout: float = DEFAULT_READ_TIMEOUT) -> TagRead | None:
        """Poll the antenna once. Returns None if no tag is present."""
        uid = self._pn532.read_passive_target(timeout=timeout)
        if uid is None:
            return None
        return TagRead(uid=uid.hex())
