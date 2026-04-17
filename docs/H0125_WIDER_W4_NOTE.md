# Wider `h = 0.125` Family (`phys_w = 4`) Note

**Date:** 2026-04-06

This note tracks the first genuinely wider continuation of the retained dense
`1/L^2 + h^2` bridge family. The fixed `phys_w = 3` family is already frozen
as a bounded negative for weak-field closure; this probe asks whether widening
the box to `phys_w = 4` can move the exponent toward `1.0` or whether the
`~0.5` limit persists.

## Script

- [`scripts/lattice_3d_l2_wide_h0125_w4.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_wide_h0125_w4.py)

## Status

Finished as a bounded no-go on the retained tested row.

- finished log:
  - [`logs/2026-04-06-h0125-wide-full-window.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window.txt)
- retained width-4 row:
  - `phys_w = 4`
  - `phys_l = 6`
  - full detector window at `z = 3.0`
  - `Born = 8.01e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.010955`
  - `alpha = 0.499`

So the first genuinely wider dense-family row does not rescue the weak-field
mass-law bridge. It reproduces the same `~0.5` exponent class as the frozen
`phys_w = 3` family and should be treated as a bounded negative, not an
unresolved reopen.
