"""
michess bring-up step 3: prove the ADG1607 switches.

No RF here. The Pi drives the address lines (A0-A2) and EN, and you
measure each channel with the multimeter on the ohms range. Your
readings are saved to a CSV so every channel has a number on record.

Wiring (breakout pin -> Pi):
  1  VDD -> 3.3 V        12 GND -> GND        27 VSS -> GND
  17 A0  -> GPIO17       16 A1  -> GPIO27     15 A2  -> GPIO22
  18 EN  -> GPIO23       (3, 13, 14 not connected)

Pinout used for the prompts:
  DA = 28, DB = 2
  S1A..S8A = pins 19..26
  S1B..S8B = pins 11..4
"""

import csv
from datetime import datetime

from gpiozero import DigitalOutputDevice

A0 = DigitalOutputDevice(17)
A1 = DigitalOutputDevice(27)
A2 = DigitalOutputDevice(22)
EN = DigitalOutputDevice(23)


def select(channel: int) -> None:
    """Channel 1-8 -> 3-bit address (channel 1 = 000, channel 8 = 111)."""
    code = channel - 1
    A0.value = code & 1
    A1.value = (code >> 1) & 1
    A2.value = (code >> 2) & 1


def a_pin(channel: int) -> int:
    return 18 + channel  # S1A = 19 ... S8A = 26


def b_pin(channel: int) -> int:
    return 12 - channel  # S1B = 11 ... S8B = 4


def ask(prompt: str) -> str:
    return input(prompt).strip() or "-"


def main() -> None:
    rows = []
    EN.off()

    print("\n=== Lead check ===")
    lead = ask("Touch the probes together. Ohms shown (lead resistance): ")
    rows.append(["leads", "", "probes shorted", lead])

    print("\n=== EN LOW: everything should be off ===")
    select(1)
    r = ask("Ohms from pin 19 (S1A) to pin 28 (DA), expect OL: ")
    rows.append(["EN low", "000", "19-28", r])

    for ch in range(1, 9):
        select(ch)
        EN.on()
        code = format(ch - 1, "03b")
        other = ch % 8 + 1  # the next channel round, should be off

        print(f"\n=== Channel {ch} selected (A2 A1 A0 = {code}), EN HIGH ===")
        ra = ask(f"  Pin {a_pin(ch)} (S{ch}A) to pin 28 (DA), expect low ohms: ")
        rb = ask(f"  Pin {b_pin(ch)} (S{ch}B) to pin 2 (DB),  expect low ohms: ")
        ro = ask(f"  Pin {a_pin(other)} (S{other}A) to pin 28 (DA), expect OL:  ")

        rows.append([f"ch{ch} on", code, f"{a_pin(ch)}-28", ra])
        rows.append([f"ch{ch} on", code, f"{b_pin(ch)}-2", rb])
        rows.append([f"ch{ch} on, ch{other} should be off", code,
                     f"{a_pin(other)}-28", ro])

    EN.off()
    print("\n=== EN LOW again ===")
    r = ask("Ohms from pin 26 (S8A) to pin 28 (DA), expect OL: ")
    rows.append(["EN low (after)", "111", "26-28", r])

    filename = f"mux_results_{datetime.now():%Y%m%d_%H%M}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["state", "A2A1A0", "pins", "reading"])
        writer.writerows(rows)
    print(f"\nSaved to {filename}")


if __name__ == "__main__":
    try:
        main()
    finally:
        EN.off()  # always leave every switch off
