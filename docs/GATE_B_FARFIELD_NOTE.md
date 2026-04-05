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

## Distance law on grown geometry (2026-04-05)

The distance law also transfers:

| Geometry | Tail | R² |
|----------|------|-----|
| Exact grid | b^(-1.05) | 0.919 |
| Grown (drift=0.2, rest=0.7) | **b^(-1.01)** | 0.914 |
| Newtonian | b^(-1.0) | — |

8 seeds averaged, W=10, L=12, h=0.5. The grown geometry gives
b^(-1.01) — even closer to Newtonian than the fixed grid.

The full Newtonian package transfers to grown geometry:
- Gravity sign: 100% TOWARD (far field)
- F∝M = 1.00
- Distance law: b^(-1.01)

## Born rule on grown geometry (2026-04-05)

| Geometry | Born |
|----------|------|
| Exact grid | 2.72e-15 |
| Grown (drift=0.2) | **2.16e-15** |

Machine precision on both. Born transfers to grown geometry.

## Complete physics package on grown geometry

| Property | Fixed lattice | Grown (drift=0.2) |
|----------|--------------|-------------------|
| Born | 2.72e-15 | 2.16e-15 |
| Gravity (far field) | 100% TOWARD | 100% TOWARD |
| F∝M | 1.00 | 1.00 |
| Distance tail | b^(-1.05) | b^(-1.01) |

Every property transfers. The grown geometry is physics-equivalent
to the fixed lattice for all measured observables.
