# LED ring tester

Lights one LED ring from the Pi, so a tile can be tested with its ring off, powered but dark, and lit.

## Hardware

- Ring: **WCMCU-2812B-12**, 12 × WS2812B, 50 mm outer / 35 mm inner. Pads on the back: `DI`, `5V`, `GND`, `DO`.
- Powered from the Pi's 5 V pin. The script caps brightness at 64/255 (worst case ~180 mA).

## Wiring

| Ring pad | Pi | Header pin |
|---|---|---|
| `GND` | GND | 14 (any GND) |
| `5V` | 5 V | 4 (pin 2 feeds the mux board) |
| `DI` | GPIO18 (PWM0) | 12 |
| `DO` | not connected | — |

Wire with the Pi off. Before connecting, check `5V` to `GND` on the ring isn't a short.

The Pi drives `DI` at 3.3 V, below the WS2812B's specified 0.7 × 5 V = 3.5 V. On a short wire it usually works; if the colours are wrong or the LEDs flicker, the fix is a 3.3 → 5 V level shifter on `DI`.

## Setup

GPIO18's PWM is shared with the Pi's analogue audio, so turn the audio off: in `/boot/firmware/config.txt`, change `dtparam=audio=on` to `dtparam=audio=off`, then reboot.

```
uv sync
```

`rpi-ws281x` builds a small C extension. If that fails, install the build tools: `sudo apt install python3-dev build-essential`.

## Run

The library needs root for the PWM hardware. `uv` usually isn't on root's path, so run the project's own Python:

```
sudo .venv/bin/python led_ring.py                      # white, brightness 32
sudo .venv/bin/python led_ring.py --colour red --brightness 64
```

Ctrl+C switches the ring off.

It uses GPIO18 only, which doesn't clash with the reader (SPI, GPIO25), the mux (GPIO 17, 27, 22, 23) or the pins ST's demo claims (5, 6, 13, 19, 24, 26), so it can run alongside `mux_select.py` and the demo.
