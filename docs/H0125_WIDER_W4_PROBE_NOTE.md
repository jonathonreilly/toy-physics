# Wider `h = 0.125` `phys_w = 4` Probe Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-06

This note records the cheapest width-4 continuation probe for the dense
`1/L^2 + h^2` bridge lane. The fixed-family `phys_w = 3` replay is already a
bounded negative; this narrower probe asks whether a genuinely wider box
changes the weak-field exponent enough to matter. To keep the diagnostic
tractable, the axial length is shortened to `phys_l = 2` while preserving the
width change.

## Script

- [`scripts/lattice_3d_l2_wide_h0125_w4_probe.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide_h0125_w4_probe.py)

## Status

This helper remains a scouting script, not the retained closeout surface.

- actual closeout logs:
  - [`logs/2026-04-06-h0125-wide-full-window.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window.txt)
  - [`logs/2026-04-06-h0125-wide-full-window-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window-probe.txt)

The finished retained width-4 result came from the targeted replay controls in
[`scripts/lattice_3d_l2_wide_h0125_replay.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide_h0125_replay.py),
which kept the physical family at `phys_l = 6` and still returned
`alpha = 0.499` on the full-window `z = 3.0` row. So the wider-family lane is
already a bounded no-go on the tested row, and this cheaper helper should stay
an auxiliary scout rather than the claim-carrying path.
