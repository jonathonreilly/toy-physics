# Wider `h = 0.125` Replay Note

**Date:** 2026-04-06

This note records the widened-family diagnostic for the retained 3D dense
`1/L^2 + h^2` bridge lane. It is intentionally narrower than the existing
fixed-family bridge note.

## Question

Does widening the physical box at `h = 0.125` rescue the weak-field mass-law
bridge, or does the fixed-family `F~M ~ 0.5` limit persist?

## Diagnostic

- new replay script:
  - [`scripts/lattice_3d_l2_wide_h0125_replay.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide_h0125_replay.py)
- comparison families:
  - `phys_w = 3`
  - `phys_w = 4`
- shared setup:
  - `phys_l = 6`
  - `h = 0.125`
  - `z_mass = 3`
  - primary weak-field sweep over `s = 10^-7 ... 5 x 10^-6`
  - confirmatory probe sweep over `s = 10^-7, 10^-6, 5 x 10^-6`
- observables:
  - Born
  - `k = 0` null
  - gravity sign
  - `F~M` exponent

## Interpretation target

- if `phys_w = 4` moves the exponent toward `1.0`, the bridge may still be
  open on a truly wider family
- if `phys_w = 4` stays near the fixed-family `0.5` slope, the fixed-family
  negative is likely structural rather than a detector-window artifact

## Status

Finished bounded no-go on the retained tested row.

- comparison log:
  - [`logs/2026-04-06-h0125-wide-full-window.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window.txt)
- retained baseline:
  - `phys_w = 3`, `phys_l = 6`, `z = 3.0`, full window
  - `Born = 6.59e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.009417`
  - `alpha = 0.500`
- genuinely wider row:
  - `phys_w = 4`, `phys_l = 6`, `z = 3.0`, full window
  - `Born = 8.01e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.010955`
  - `alpha = 0.499`
- confirmatory probe log:
  - [`logs/2026-04-06-h0125-wide-full-window-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window-probe.txt)
  - same `phys_w = 4`, `phys_l = 6`, `z = 3.0`, full-window row
  - same `alpha = 0.499` on the reduced three-strength sweep

On this first genuinely wider full-window replay, the weak-field exponent does
not move toward `1.0`; it stays pinned to the fixed-family `~0.5` class. That
makes the wider-family `h = 0.125` continuation a bounded negative rather than
a retained rescue.
