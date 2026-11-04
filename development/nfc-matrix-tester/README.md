# nfc-matrix-tester

A practice harness for wiring a PN532 NFC reader to a Raspberry Pi and reading tag UIDs. Single PN532, single antenna, single tag: a Tkinter window shows the last UID read.

> **Parked.** This was written for the original design (PN532 readers with CD74HC4067 multiplexers). The project has since moved to the ST25R3916B reader and the ADG1607 multiplexer: see [`../st25r-reader-tester/`](../st25r-reader-tester/) and [`../mux-switch-tester/`](../mux-switch-tester/). The PN532 is kept only as a side experiment.
>
> The idea of growing this into an 8×8 grid view, with cells lighting up as tags are detected, still stands, and could be carried over to the new reader. It's useful for spotting cross-talk, dead antennas or bad solder joints without the chess engine or LEDs running.

## Structure

- `reader.py`: talks to the PN532 hardware. The only thing that changes when you move from I²C to SPI, or add the multiplexer.
- `models.py`: `TagRead`, the plain data shape passed from reader to display.
- `display.py`: Tkinter UI. The only thing that changes when this grows from "one label" to "8×8 grid".
- `main.py`: wires reader → display together and runs the poll loop.

## Setup (on the Pi)

```bash
cd development/nfc-matrix-tester
uv sync
```

`uv sync` creates `.venv/` and installs everything pinned in `uv.lock`.

## Run

```bash
uv run nfc-matrix-tester
```

## Checks

```bash
uv run pytest   # tests
uv run mypy     # type checking (strict mode; see [tool.mypy] in pyproject.toml)
```

## Wiring

TODO: fill in once the PN532 is wired up (interface used: I²C/SPI/UART; pins, address).
