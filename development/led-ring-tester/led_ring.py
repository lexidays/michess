"""
Light the WCMCU-2812B-12 LED ring (12 x WS2812B) from the Pi, for the
LED ring / coil tests: ring off, ring powered but dark, ring lit.

All 12 LEDs are set to one colour and held until Ctrl+C, then switched off.
Brightness is capped, because the ring is powered from the Pi's 5 V pin.

Wiring: ring DI -> GPIO18 (header pin 12), 5V -> 5 V (pin 4), GND -> GND.
Needs root for the PWM/DMA hardware:  sudo .venv/bin/python led_ring.py
"""

import argparse
import time

from rpi_ws281x import Color, PixelStrip

LED_COUNT = 12
LED_PIN = 18          # GPIO18 = PWM0. Kept free for NeoPixels; not claimed by ST's demo.
MAX_BRIGHTNESS = 64   # of 255 (25%). Worst case ~12 x 60 mA x 0.25 = ~180 mA from the Pi.

COLOURS = {
    "white": Color(255, 255, 255),
    "red": Color(255, 0, 0),
    "green": Color(0, 255, 0),
    "blue": Color(0, 0, 255),
    "off": Color(0, 0, 0),
}


def fill(strip: PixelStrip, colour: int) -> None:
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colour)
    strip.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--colour", choices=COLOURS, default="white")
    parser.add_argument(
        "--brightness",
        type=int,
        default=32,
        help=f"0-{MAX_BRIGHTNESS} (default 32, about 12%%)",
    )
    args = parser.parse_args()
    brightness = max(0, min(args.brightness, MAX_BRIGHTNESS))

    strip = PixelStrip(LED_COUNT, LED_PIN, brightness=brightness)
    strip.begin()
    fill(strip, COLOURS[args.colour])
    print(f"Ring {args.colour} at brightness {brightness}/255. Ctrl+C to switch off.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        fill(strip, COLOURS["off"])
        print("Ring off.")


if __name__ == "__main__":
    main()
