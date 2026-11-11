# Coil drum

A printed 57 mm chess-square tile that carries one square's read coil. The coil is wound on a 31.5 mm drum between the base plate and a thin top flange, like a cotton reel. The square's LED ring sits above the coil on four curved risers, and a small perfboard "anchor board" screws onto two posts at the front edge, where the fragile coil wire joins the lead to the multiplexer.

Everything is positioned by the print, so every square comes out the same.

## Current version: draft 3

Heights are measured from the bottom of the tile (z = 0). Draft 3 is sketched mostly with typed-in values; a parametric rebuild is planned once the design settles ([#18](https://github.com/lexidays/michess/issues/18)).

| Feature | Value | Notes |
|---|---:|---|
| Tile size | 57 mm | Spreadsheet value `square_size` |
| Base plate | 1.6 mm (0–1.6) | Flat bottom, prints without supports |
| Drum core diameter | 31.5 mm | Spreadsheet value `core_d`; up to 4.0 mm |
| Top flange | 33 mm diameter, 4.0–4.6 mm | Thin, to keep the tag close to the coil |
| Winding gap | 2.4 mm (1.6–4.0) | Room for 3–4 stacked turns of 30 AWG |
| LED ring risers | 4 curved risers, 19–25 mm radius, 6.0 mm tall | The ring sits on top, above the coil |
| LED locating pegs | 1.2 mm diameter at 32.5 mm square spacing, 2 mm above the risers | Fit the ring's 2.2 mm mounting holes |
| Anchor-board posts | Two posts, 3.0 mm tall, either side of the front notch | Wire channel for the coil tails between them |
| Anchor-board screw holes | 1.8 mm (sized for M2), at x = ±6.375 mm, y = −24.5 mm | Through the full tile height |
| Front notch | 7.5 mm wide, through the base plate | Soldering-iron access from either side |
| Corner holes | Four 2.0 mm holes at (±26.5, ±26.5) mm | Through the base plate, for fixing the tile to a frame (frame design not settled) |

Measured parts it's designed around:

| Part | Value |
|---|---|
| LED ring | 50 mm outer, 35 mm inner, 2.2 mm mounting holes at 32.5 mm square spacing |
| Perfboard | 2.54 mm (0.1 inch) pitch |

### Known issues (fixes tracked in [#17](https://github.com/lexidays/michess/issues/17))

- The prototype tiles use M3 screws, but the holes are sized for M2.
- There's only 1.4 mm between the top of the anchor board (4.6 mm) and the underside of the LED ring (6.0 mm), so the ring may rest on the screw heads rather than the risers.

## Files

- `coil-drum.FCStd`: FreeCAD 1.1 source. It may not open in FreeCAD 1.0.
- `coil-drum-Body.stl`: STL export, for printing without FreeCAD. If the FCStd changes, re-export the STL in the same commit.

## Printing

- Printer: Bambu Lab A1 (0.4 mm nozzle)
- Orientation: flat on its base
- Supports: none
- Layer height / material: not yet settled

## Building a square

- Wind 30 AWG (~0.25 mm) enamelled magnet wire on the drum, turns stacked on top of each other. Touching turns are fine: the enamel is the insulation. 3 and 4 turns have both read tags; the final count is being decided by measurement ([#14](https://github.com/lexidays/michess/issues/14)).
- Use the same winding direction, tension and tail length on every coil. Consistency between squares matters more than any one value.
- Anchor board: a 6 × 3 hole piece of perfboard. Screws go through the outer columns of the middle row; the coil wires are soldered in the middle two columns of the bottom row.
- Keep the lead's two wires twisted from the edge of the anchor board, so they don't form a loop that becomes part of the antenna.

## Revisions

- **Draft 1:** walled winding channel around the drum. Too hard to wind.
- **Draft 2:** top flange instead of the wall; friction-fit pocket for the anchor board. The pocket's roof is an unsupported bridge and printed badly.
- **Draft 3:** anchor board screwed onto two posts (no pocket), slot under it for soldering access, LED ring moved onto risers above the coil.
