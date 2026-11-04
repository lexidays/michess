# development

Throwaway, learning-focused test harnesses used to practice wiring hardware, try out libraries, and de-risk pieces of the design before they get built into the real [`software/`](../software/) stack.

Nothing here is production code. It's not expected to be reused directly: the goal is to fail fast and cheaply while learning the hardware, then carry the *lessons* into `software/`, not necessarily the code itself.

Each subfolder is an independent [uv](https://docs.astral.sh/uv/) project: its own `pyproject.toml`, virtual environment, and lockfile. They don't share code with each other or with `software/`.

## Harnesses

| Folder | Purpose |
|---|---|
| [`st25r-reader-tester/`](st25r-reader-tester/) | Bring up an ST25R3916B MINI over SPI: chip ID check, then tag reads and antenna amplitude/phase (fingerprint) measurements via ST's RFAL driver |
| [`mux-switch-tester/`](mux-switch-tester/) | Drive the ADG1607 multiplexer from the Pi: a switching test on every channel, and holding a channel while reading tags through the mux |
| [`nfc-matrix-tester/`](nfc-matrix-tester/) | Parked. A single PN532 reader + tag, from the original PN532 design |
