# Gate B Far-Field: Grown Geometry at h=0.5

**Date:** 2026-04-05
**Status:** frozen bounded positive on far-field rows

## Artifact chain

- [`scripts/gate_b_farfield_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_farfield_harness.py)
- [`logs/2026-04-05-gate-b-farfield-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-farfield-harness.txt)

## Result

| drift | restore | TOWARD | F∝M |
|-------|---------|--------|-----|
| 0.3 | 0.5 | 36/36 (100%) | 1.00 |
| 0.2 | 0.7 | 36/36 (100%) | 1.00 |
| 0.1 | 0.9 | 36/36 (100%) | 1.00 |
| 0.0 | 1.0 | 36/36 (100%) | 1.00 |

12 seeds × 3 z-masses (z=3,4,5) = 36 tests per row.

## Growth rule

Template previous layer + Gaussian drift + restoring force toward grid +
NN connectivity from grid labels. Valley-linear action S=L(1-f), 1/L^2
kernel with h^2 measure.

## Bounded interpretation

In the far field (z ≥ 3, well past the slits), the grown-geometry
lattice gives 100% TOWARD gravity with Newtonian F∝M=1.00 at all
tested drift/restore levels including the noisiest (drift=0.3, rest=0.5).

This does NOT close Gate B for the full parameter space: the v6
frozen replay at near-field parameters (z=1.0-2.0) remains mixed
(67-92%). The far-field rows are clean; the near-field rows are not.

## What this says about Gate B

The growth rule successfully generates geometry that gives Newtonian
gravity in the far field. The near-field mixing is a property of the
beam optics at close mass positions, not a growth-rule failure — the
same mixing appears on the fixed lattice at near-field z-values.

The honest Gate B read: **far-field passed, near-field mixed, same
as the fixed lattice.**
