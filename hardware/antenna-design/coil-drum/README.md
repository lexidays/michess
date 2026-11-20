# Coil drum

A printed 57 mm chess-square tile that carries one square's read coil. The coil is wound on a 31.5 mm drum between the base plate and a thin top flange, like a cotton reel. The square's LED ring sits flat on the base plate around the coil, and the coil connector board screws on underneath at the front edge, where the fragile coil wire joins the lead to the multiplexer.

Everything is positioned by the print, so every square comes out the same.

## Current version: draft 4

Heights are measured from the bottom of the tile (z = 0). Positions are from the centre of the tile; negative y is the front edge (the coil connector board's side). Values in `code` are cells in the FreeCAD spreadsheet. Some sketches still use typed-in values; a full parametric rebuild is planned once the design settles ([#18](https://github.com/lexidays/michess/issues/18)).

| Feature | Value | Notes |
|---|---:|---|
| Tile size | 57 mm | `square_size`. Tile is 5.0 mm tall overall |
| Base plate | 2.0 mm (0–2.0) | `base_t`. Flat bottom, prints without supports |
| Front gap | 7.5 mm wide (x ±3.75), from the edge to y −16.5 | Lets the coil connector board sit flush, and gives access to its coil pads |
| Side and back gaps | 14 mm wide (±7.0), from the edge to 16.5 mm from the centre | Access to the back of the LED ring to solder its wires, so the wiring can leave in any direction |
| Drum core | 31.5 mm diameter, up to 4.4 mm | `core_d` |
| Winding gap | 2.4 mm (2.0–4.4) | `drum_wind_gap`. Room for 3–4 stacked turns of 30 AWG |
| Top flange | 33 mm diameter, 0.6 mm thick (4.4–5.0) | `drum_flange_t`. Thin, to keep the tag close to the coil. Must pass through the LED ring's 35 mm hole |
| LED ring | Sits flush on the base plate (from z = 2.0) | No risers |
| LED locating pegs | Four 2.0 mm pegs, 4.0 mm tall (2 mm above the plate), at 33 mm square spacing | `led_loc_peg_dist`, `led_loc_peg_dia` (ring hole 2.2 mm minus 0.2 mm clearance) |
| Coil connector board screw holes | 2.6 mm, at x = ±6.35, y = −21.15 | Through the base plate. Sized for an M3 to cut its own thread |
| Corner notches | 5.2 mm radius quarter circles at each corner | Clear the frame's 10 mm bosses ([#26](https://github.com/lexidays/michess/issues/26)) |

Because of the gaps, the base plate is four corner pieces joined through the drum.

Measured parts it's designed around:

| Part | Value |
|---|---|
| LED ring | 50 mm outer, 35 mm inner, 2.2 mm mounting holes at 33 mm square spacing |
| Coil connector board | 20.32 × 12.7 × 1.6 mm, M3 holes 12.7 mm apart. See [`hardware/pcb/coil-connector-board/`](../../pcb/coil-connector-board/) |

### Still to settle (tracked in [#17](https://github.com/lexidays/michess/issues/17))

- **The LED ring is level with the coil**, its copper about 1–1.5 mm from the winding. A metal ring next to a coil can act as a shorted turn and reduce read distance. Test the first tile with the ring off, on but unpowered, and on and powered, before winding more.
- **Which way round the coil connector board goes.** Its screw holes are halfway front to back, so it fits either way. With the pads towards the drum, each pad's hole is about two-thirds clear of the front gap (workable, but fiddly). Turned round, the pads are fully in the gap, but the socket opens under the middle of the tile.
- **Stiffness:** the corner pieces only join through the drum. Check a print doesn't flex or warp.

## Files

- `coil-drum.FCStd`: FreeCAD 1.1 source. It may not open in FreeCAD 1.0.
- `coil-drum-Body.stl`: STL export, for printing without FreeCAD. If the FCStd changes, re-export the STL in the same commit.

## Printing

- Printer: Bambu Lab A1, 0.4 mm nozzle (the 2.0 mm pegs, the screw holes and the 0.6 mm flange need the fine detail)
- Orientation: flat on its base
- Supports: none
- Layer height: 0.2 mm (the 2.0, 4.4 and 5.0 mm heights are all whole layers)
- Material: not yet settled

## Building a square

- Wind 30 AWG (~0.25 mm) enamelled magnet wire on the drum, turns stacked on top of each other. Touching turns are fine: the enamel is the insulation. 3 and 4 turns have both read tags; the final count is being decided by measurement ([#14](https://github.com/lexidays/michess/issues/14)).
- Use the same winding direction, tension and tail length on every coil. Consistency between squares matters more than any one value.
- Screw the coil connector board to the underside with two **M3×3** screws, socket hanging below. The board (1.6 mm) and the plate (2.0 mm) add up to 3.6 mm, and the screws sit under the LED ring, so anything longer than 3 mm would poke up into the ring.
- Strip the enamel from the coil ends, bring them down through the front gap into the board's two plated holes, and solder. The **start of the winding goes to the square pad** (pin 1, coil A) on every square. A coil has no polarity; this just keeps the squares the same.
- A dab of glue or nail varnish over the 30 AWG afterwards takes the strain off it.
- Connect the square with a 300 mm twisted-pair lead (JST PH, pin 1 to pin 1). Keep the twist the same on every lead, so the leads don't form loops that become part of the antenna.
- Fit the LED ring over the pegs.

## Revisions

- **Draft 1:** walled winding channel around the drum. Too hard to wind.
- **Draft 2:** top flange instead of the wall; friction-fit pocket for the anchor board. The pocket's roof is an unsupported bridge and printed badly.
- **Draft 3:** perfboard anchor board screwed onto two posts (no pocket), slot under it for soldering access, LED ring moved onto risers above the coil. The coil connector board, which replaced the perfboard, was too deep to fit beside the drum at these heights.
- **Draft 4:** coil connector board screwed underneath the base plate; LED ring flush on the plate, located by pegs; access gaps at the middle of each edge; 2.0 mm base plate; corner notches for the frame's bosses, replacing draft 3's corner holes.