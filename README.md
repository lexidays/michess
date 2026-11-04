# michess ♟️

An open-source NFC-based smart chess board powered by a Raspberry Pi. Place any piece on any square and the board knows exactly what it is and where it is - no setup routine, no special starting position required.

The board uses LEDs embedded behind a wood veneer to indicate the chess engine's moves, creating a clean physical interface for playing against a computer opponent.

---

## Features

- **Full piece identification** - NFC tags in each piece base, detected by a matrix of antennas under the board
- **Arbitrary position recognition** - pick up mid-game, set up a puzzle, analyse a position
- **LED move indicators** - subtle lighting behind the veneer shows the engine's chosen move
- **Stockfish integration** - plays via the standard UCI chess engine interface
- **Open design** - all hardware designs and software are freely available

---

## How It Works

64 NFC antennas sit beneath the board, one per square, managed by a hierarchical multiplexer system. A Raspberry Pi 4 scans the full board in under 2 seconds, determines the game state, passes it to Stockfish, and lights up the appropriate squares.

See [`docs/architecture/`](docs/architecture/) for full system diagrams.

---

## Repository Structure

```
michess/
├── hardware/               # Schematics, PCB layouts, BOM, antenna designs
├── firmware/               # Low-level microcontroller code (if applicable)
├── software/
│   ├── board_reader/       # NFC matrix scanning
│   ├── chess_engine/       # Stockfish/UCI integration
│   └── led_controller/     # LED matrix control
├── development/            # Throwaway hardware/learning test harnesses
├── docs/
│   └── architecture/       # System diagrams and design notes
└── tests/
```

---

## Hardware Requirements

| Component | Quantity | Notes |
|---|---|---|
| Raspberry Pi 4 | 1 | Main controller |
| PN532 NFC reader modules | 8 | One per 8-square group |
| CD74HC4067 16-channel multiplexers | 4 | For antenna switching |
| NFC tags (13.56 MHz) | 32 | Embedded in piece bases |
| Custom loop antennas | 64 | One per square, ~1–2 μH |
| WS2812B LEDs | 64+ | For move indication |

See [`hardware/bom/`](hardware/bom/) for a full bill of materials with UK suppliers and current pricing.

---

## Getting Started

### Software Setup

```bash
# Clone the repo
git clone https://github.com/steve-birch/michess.git
cd michess

# Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python software/main.py
```

### Hardware Setup

See [`docs/setup.md`](docs/setup.md) for full wiring instructions and assembly guide.

---

## Licences

This project uses different licences for different parts:

| Part | Licence |
|---|---|
| Software | [GPL-3.0](LICENSE) |
| Hardware designs | [CERN-OHL-S v2](hardware/LICENSE) |
| Documentation | [CC BY-SA 4.0](docs/LICENSE) |

In short: you are free to use, modify, and build on michess for any purpose - including building your own board - but you must share any changes under the same terms. Commercial use is permitted, but derived works cannot be closed source.

---

## Contributing

Contributions are very welcome - whether that's hardware improvements, software features, bug fixes, or documentation. Please open an issue first to discuss larger changes.

---

## Project Status

🚧 **Early development** - currently prototyping the NFC matrix on a 2×2 test board.
