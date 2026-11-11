# mux-switch-tester

Drives the Analog Devices **ADG1607** multiplexer from a Raspberry Pi. Two
scripts:

- `mux_test.py`: bring-up **step 3**. Proves the mux switches to the right
  channel when the Pi tells it to. A DC test only: no RF, no coils and no
  reader in the signal path. Each channel is checked with a multimeter on the
  resistance (Ω) range, so GPIO control of the mux is tested on its own
  before any antenna goes through it.
- `mux_select.py`: holds the mux on one channel while ST's reader demo runs in
  another terminal, for reading tags through the mux (see
  [Reading tags through the mux](#reading-tags-through-the-mux)).

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

A breadboard is fine for the switching test because it's GPIO only. It isn't
fine for measuring anything with coils connected: breadboard rows and loose
leads pass RF to each other. A mux board to take the antenna path off the
breadboard is tracked in [#12](https://github.com/lexidays/michess/issues/12).

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

If the demo stops with `GPIO init failed`, something else is holding one of
its pins. Check every new pin against the list above.

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

Record a resistance for every channel rather than just checking for a beep:
the readings are what show whether all channels behave the same. On the Ω
range, an off switch should read open circuit (OL on most meters). A high
reading (kΩ or MΩ) on an off channel with the probes one way round is the
chip's protection diodes, not a fault; swap the probes.

### If it fails

- Nothing connects even with EN high: check EN, VDD and both grounds.
- Every address gives the same channel: an address wire isn't connected.
- Channels answer in the wrong order: two address wires are swapped.

## Reading tags through the mux

Wiring is **single-ended**: one wire of each coil goes through the mux, and
the other wires all join on a common return straight back to the reader.

| From | To |
|---|---|
| Reader antenna port, red | pin 28 (DA) |
| Reader antenna port, black | common return |
| Coil *n*, wire A | S*n*A (coil 1 → pin 19, coil 2 → pin 20, …) |
| Coil *n*, wire B | common return |

The common return is **not** ground. Both antenna wires carry the RF signal;
tying either one to the Pi's ground would short half of the reader's antenna
driver.

The reader's antenna port has no polarity, so "red through the mux" is a
convention, kept the same on every channel.

To run:

1. In one terminal: `uv run mux_select.py`. Type 1–8 to select a channel,
   0 to switch everything off, q to quit. Each change opens all switches,
   sets the new address, then closes only the new channel.
2. In another: ST's demo (`sudo ./demo/nfc_demo_st25r3916b`, see
   [`../st25r-reader-tester/`](../st25r-reader-tester/)). The demo keeps
   working when the channel is changed while it runs.

The mux was powered from **5 V** (pin 1 only) for the first RF test, for more
headroom for the RF signal. The Pi only drives the mux's control inputs, so
5 V on the mux can't reach a Pi pin. Whether the RF signal stays within the
mux's supply rails is still open ([#16](https://github.com/lexidays/michess/issues/16)), and cross-talk is being characterised
([#15](https://github.com/lexidays/michess/issues/15)).

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
  the bottom of the ADG1607's range. It feeds into the supply question ([#16](https://github.com/lexidays/michess/issues/16)).
- EN low switches everything off.

(The raw CSV from this run recorded OL as `0`; the table above shows it as
OL.)
