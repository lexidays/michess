# mux-switch-tester

Bring-up **step 3**: prove the Analog Devices **ADG1607** multiplexer switches
to the right channel when the Raspberry Pi tells it to.

This is a DC test only. No RF, no coils and no reader in the signal path. The
Pi drives the mux's address and enable pins, and each channel is checked with
a multimeter on the resistance (Ω) range. The aim is to test one new thing
(GPIO control of the mux) before any antenna goes through it.

## The chip in one paragraph

The ADG1607 is a differential 8:1 switch: 8 pairs of switches (S1A/S1B …
S8A/S8B) sharing one output pair (DA and DB). Address pins A0, A1 and A2 form
a 3-bit number that picks which pair is closed (channel 1 = `000` …
channel 8 = `111`). EN is the master switch and is **active high**: when it's
low, every switch is open whatever the address says.

## Hardware

- ADG1607 (marked `ADG1607B #2315`) on an Adafruit SOIC-28/TSSOP-28 breakout,
  header pins fitted, sitting in a breadboard
- Raspberry Pi 4, Debian 13 (trixie), via a GPIO T-cobbler
- UNI-T UT61B+ multimeter

A breadboard is fine for this test because it's GPIO only. **Take the breakout
off the breadboard before any coil is connected:** no breadboard in the antenna
path.

## Pinout (TSSOP-28)

Pin 1 is the corner marked with a circle. Pins 1–14 run down the left side;
pins 15–28 run up the right side.

```
   1  VDD            28  DA
   2  DB             27  VSS
   3  (NC)           26  S8A
   4  S8B            25  S7A
   5  S7B            24  S6A
   6  S6B            23  S5A
   7  S5B            22  S4A
   8  S4B            21  S3A
   9  S3B            20  S2A
  10  S2B            19  S1A
  11  S1B            18  EN
  12  GND            17  A0
  13  (NC)           16  A1
  14  (NC)           15  A2
```

## Wiring

| Breakout pin | Connects to | Pi header pin |
|---|---|---|
| 1 VDD | 3.3 V | 1 or 17 |
| 12 GND | GND | any GND |
| 27 VSS | GND | any GND |
| 17 A0 | GPIO17 | 11 |
| 16 A1 | GPIO27 | 13 |
| 15 A2 | GPIO22 | 15 |
| 18 EN | GPIO23 | 16 |

The mux runs from the Pi's **3.3 V, not 5 V**, so nothing on it can ever sit
above what the Pi's GPIO pins can take. (The ADG1607 works from a 3.3–16 V
single supply with 3 V logic-compatible inputs.) This supply is only for the
switching test; the supply for RF use is a separate question for step 5.

These GPIOs keep clear of every pin ST's reader demo uses, so the reader can
stay wired and the demo can run at the same time as the mux scripts:

- SPI: GPIO 7–11
- IRQ: GPIO25
- Status LEDs for ST's own expansion boards: GPIO 5, 6, 13, 19, 26 and 24
  (from `linux_demo/platform/st25r3916b/rfal_platform.h`). The demo claims
  these even with no LEDs fitted.

GPIO18 is also left free, as the usual pin for driving NeoPixels later.

**History:** step 3 was first run on GPIO 5, 6, 13 and 19. The switching
test passed, but those turned out to be four of the demo's LED pins: with
`mux_select.py` holding them, the demo stopped with `GPIO init failed`, and
without it the demo would have driven the mux address lines itself. The mux
was moved to GPIO 17, 27, 22 and 23 the same evening.

## Procedure

1. **Short check, nothing connected:** meter on Ω, measure pin 1 to pin 12.
   OL (or kΩ and above) is a pass. Near 0 Ω means a short between the supply
   pins: stop.
2. **Power only, Pi off:** wire pins 1, 12 and 27. Power on and measure pin 1
   to pin 12 on V⎓. Expect about 3.3 V.
3. **Pi off again:** add A0, A1, A2 and EN.
4. **Run the script:**

   ```
   uv sync
   uv run mux_test.py
   ```

   It selects each channel in turn, tells you which pins to probe and saves
   your readings to `mux_results_<date>_<time>.csv`. For each channel it asks
   for the A side, the B side, and one neighbouring channel that should be off.
   It always sets EN low on exit.

### Meter notes

- Use the Ω setting, not the beep, so every channel gets a number.
- Touch the probes together first to check lead resistance.
- Readings take about a second to settle while the meter auto-ranges.
- **OL** ("overload") on Ω means open circuit: no measurable connection. It's
  what an off switch should show.
- An off channel may show a high reading (kΩ or MΩ) instead of OL with the
  probes one way round. That's the chip's protection diodes, not a fault;
  swap the probes.

### If it fails

- Nothing connects even with EN high: check EN, VDD and both grounds.
- Every address gives the same channel: an address wire isn't connected.
- Channels answer in the wrong order: two address wires are swapped.

## Results (29 October 2026): pass

| Check | Result |
|---|---|
| Pin 1 to pin 12, unconnected | OL |
| VDD (pin 1 to pin 12), powered | 3.29 V |
| Lead resistance (probes shorted) | 0.0 Ω |

| Channel | A2 A1 A0 | SnA → DA (Ω) | SnB → DB (Ω) | Next channel's A side |
|---|---|---|---|---|
| 1 | 000 | 9.2 | 9.3 | OL |
| 2 | 001 | 9.4 | 9.5 | OL |
| 3 | 010 | 9.5 | 9.4 | OL |
| 4 | 011 | 9.3 | 9.4 | OL |
| 5 | 100 | 9.4 | 9.4 | OL |
| 6 | 101 | 9.3 | 9.3 | OL |
| 7 | 110 | 9.4 | 9.3 | OL |
| 8 | 111 | 9.2 | 9.4 | OL |

EN low, before and after the run: OL.

**Conclusions**

- Every channel switches on both the A and B sides, and the right channel
  answers for every address, so all four control lines are wired correctly.
- On-resistance is **9.2–9.5 Ω** across all 16 switches (average about
  9.4 Ω). The spread is only 0.3 Ω, about 3%, which matters more for michess
  than the absolute value, because every channel needs to behave the same.
- That's about double the datasheet's ~4.5 Ω headline. Expected: analog
  switches have higher on-resistance at lower supply voltages, and 3.3 V is
  the bottom of the ADG1607's range. It feeds into the step 5 supply question.
- EN low switches everything off.

(The raw CSV from this run recorded OL as `0`; the table above shows it as
OL.)
