# st25r-reader-tester

Bring-up harness for the Elechouse **ST25R3916B MINI** reader on a Raspberry Pi. This is step 1 of the 4-square prototype plan: prove the reader, SPI link, IRQ line and driver work using only the stock hardware, so any later failure can only be caused by the custom hardware (coils, mux).

## Running it again

- In `development/st25r-reader-tester`, run `uv run id_check.py`. Expect `ID=0x31 type=6`.
- From `vendor/ST25R3916_v2.8.0_Linux_demo_v1.0/linux_demo/build`, run `sudo ./demo/nfc_demo_st25r3916b`; this runs the reader demo, which reads tags with whichever antenna is plugged in. It needs `sudo` (without it: "Error assigning high priority to polling thread"). Press `Ctrl+C` to stop it; stop it before swapping antennas.
- `vendor/` is git-ignored, so after a fresh clone you need the unpack, edit and build steps later in this document before the demo will run.

## Results

| Check | Result |
|---|---|
| 5V safety check on signal lines | ✅ Pass |
| Chip ID over SPI (Python) | ✅ `type=6` (ST25R3916B) |
| ST RFAL driver builds and runs on Trixie | ✅ |
| Read an NTAG213 tag | ✅ |
| Baseline read distance (stock antenna) | ✅ ~31 mm |
| Does the MINI have AAT varicaps? | ✅ No — fixed matching network, AAT_A/AAT_B unconnected |

## Hardware setup

- Raspberry Pi 4 Model B Rev 1.5, Debian 13 (trixie)
- Connected via a GPIO extension board (T-cobbler) on a breadboard. This is fine for SPI; the breadboard only matters for antenna leads at 13.56 MHz.
- Reader: ST25R3916B MINI with its bundled 52 × 5.5 mm antenna (10 cm cable)

### Wiring

⚠️ The cable colours do **not** follow the usual convention. Red is IRQ, not 5V. Black is CS, not GND. Wire by label, not by colour.

| Wire | Module signal | Pi (cobbler label) | Physical pin |
|---|---|---|---|
| Red | IRQ | GPIO25 | 22 |
| Black | CS | CE0 (GPIO8) | 24 |
| Yellow | SCLK | SCLK (GPIO11) | 23 |
| Green | MOSI | MOSI (GPIO10) | 19 |
| Blue | MISO | MISO (GPIO9) | 21 |
| White | 5V | 5V | 2 |
| Orange | GND | GND | 6 |

IRQ is on **GPIO25**, not GPIO7 as in ST's instructions. GPIO7 is the Pi's second SPI chip-select (CE1), which the SPI driver claims (`/dev/spidev0.1`).

### 5V safety check

The module takes a 5V supply, and the Pi's GPIO pins are not 5V tolerant. So, before connecting any signal wires, the module was powered with only 5V and GND connected, and each signal wire was measured against GND.

| Wire | Reading |
|---|---|
| White (5V) | 5.07 V |
| Red (IRQ) | 0 V |
| Black (CS) | 0.56 V |
| Yellow (SCLK) | 0 V |
| Green (MOSI) | 0.50 V |
| Blue (MISO) | 0 V |

All signal lines were well under 3.3V. Pass.

## Chip ID check (Python)

This is a uv project with `spidev` as its only dependency. SPI must be enabled first (`sudo raspi-config nonint do_spi 0`, then reboot).

```
uv run id_check.py
```

Result: `ID=0x31 type=6 rev=1`. Type 6 means ST25R3916B. `0x00` or `0xFF` would indicate a wiring problem.

## ST RFAL driver (C)

- Source: ST **STSW-ST25R013** from st.com (free account needed), which unpacks to `ST25R3916_v2.8.0_Linux_demo_v1.0`
- It lives in `vendor/`, which is **git-ignored**. ST's licence may not allow redistribution, so re-download it rather than committing it.
- The download file lost its `.tar` extension. To unpack: `unxz STSW-ST25R013.xz`, then `tar -xvf STSW-ST25R013 -C vendor/`

### Local modification (lost on re-extract, so re-apply it)

`linux_demo/platform/st25r3916b/rfal_platform.h`, line 126:

```
#define ST25R_INT_PIN   7   →   25
```

### Build

```
cd vendor/ST25R3916_v2.8.0_Linux_demo_v1.0/linux_demo
mkdir -p build && cd build
cmake -DRFAL_VARIANT=st25r3916b ..
make
```

Gotcha: without the leading `-` on `-D`, CMake silently ignores the setting and builds the **non-B** variant. That build uses the unedited header, so IRQ ends up back on GPIO7. Check that cmake prints `Building st25r3916b Reader/Writer demo`. If you rebuild, delete `build/` first, because CMake caches old settings.

Harmless warnings: the CMake deprecation notice, and a pointer-to-int cast in `rfal_isoDep.c`. The cast is in card-emulation code, which we don't use.

### Run

```
sudo ./demo/nfc_demo_st25r3916b
```

Output with a tag on the antenna:

```
ISO14443A/NFC-A card found. UID: 538D0400A40001
 Read Block: OK Data: 538D045200A40001A5480000E1101200
```

The driver worked on Trixie without changes, apart from the IRQ pin.

## Baseline read distance

| Setup | Result |
|---|---|
| NTAG213 25 mm sticker, flat on the bundled 52 × 5.5 mm antenna, lifted straight up until reads stop | **~31 mm** |

This is the reference for comparing custom coils ([#14](https://github.com/lexidays/michess/issues/14)). Elechouse quote ~5 cm with a full-size card, so ~31 mm with a small sticker is in line.

Note: the tag's data block (`E1 10 12 00`) confirms an NDEF-formatted tag with NTAG213 memory size. However, genuine NXP UIDs usually start with `04`, and this one starts with `53`, so it may be a compatible chip from another maker. That's fine for now, but worth remembering if tag performance seems inconsistent.

## Antenna tuning: no AAT on the MINI

The ST25R3916B chip supports automatic antenna tuning (AAT), but only when the board maker fits variable capacitors driven by its AAT_A/AAT_B outputs. Elechouse confirmed (October 2026) that the MINI has none: AAT_A and AAT_B are unconnected, the matching network is fixed and designed for the bundled ~700 nH antenna, and no schematic is published.

So each custom coil is wound to behave like the stock antenna. The chip can still measure the antenna's amplitude and phase, which is used as a "fingerprint" to compare each coil against the stock antenna. Recording the stock antenna's reference values is tracked in [#13](https://github.com/lexidays/michess/issues/13). RFAL may provide `rfalChipMeasureAmplitude` / `rfalChipMeasurePhase` (unverified until checked in the vendor headers).
