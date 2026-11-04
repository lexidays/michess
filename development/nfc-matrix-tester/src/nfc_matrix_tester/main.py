"""Entry point: poll a single PN532 reader and show results in a Tkinter window."""

from __future__ import annotations

from .display import TkConsole
from .reader import PN532Reader


def main() -> None:
    reader = PN532Reader()
    display = TkConsole()
    display.poll(reader.read_tag)
    display.run()


if __name__ == "__main__":
    main()
