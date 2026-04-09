# Analysis: Distance Law Exponent on 3D 1/L^2 Lattice

## Date
2026-04-04

## Observation
At matched lattice width (W=10), the distance tail exponent:
- h=0.5: b^(-0.82) (peak z=5, 5-point tail)
- h=0.25: b^(-0.52) (peak z=4, 6-point tail)

The exponent gets SHALLOWER with finer h. This is the OPPOSITE of
convergence toward Newtonian -2.

## Beam width check
Beam RMS width at detector: 2.86 (h=0.5) vs 2.97 (h=0.25).
Nearly identical — NOT a beam-width artifact. The normalized
deflection (delta/rms) INCREASES with finer h.

## Continuum theory prediction
The spent-delay action S = dl - sqrt(dl^2 - L^2) at weak field f:
  S ≈ L(1 - sqrt(2f))

The field-dependent part: delta_S ≈ -L*sqrt(2f) ∝ sqrt(f)

This sqrt(f) is the SAME mechanism that gives F∝M = 0.50 (sqrt(M)):
  delta_S ∝ sqrt(s) → deflection ∝ sqrt(field_strength) ∝ sqrt(M)

For the distance law, the continuum ray-deflection integral
d/db[∫ sqrt(f(r)) dx] gives exponent ~-1.0 (Newtonian in 3D).
But the lattice gives ~-0.5.

## Why the lattice differs from continuum ray theory
The lattice centroid shift involves the FULL path-sum interference,
not just a classical ray deflection. The interference of many paths
(625+ edges per node, ~50 layers) creates a redistribution pattern
that differs from the single-ray approximation.

The lattice result (-0.52 at h=0.25) may be the true model prediction,
converging to some non-Newtonian value. Or it may still be a
lattice artifact at this coarse resolution.

## What is clear
1. F∝M = 0.50 comes from sqrt(f) in the spent-delay action (DERIVED)
2. The distance exponent converges to something near -0.5 (MEASURED)
3. The beam width is NOT the explanation (TESTED)
4. The continuum single-ray prediction is ~-1.0 (COMPUTED)

## What is unclear
1. Why the lattice path-sum gives -0.5 instead of the ray prediction -1.0
2. Whether -0.5 is the true continuum limit or still h-dependent
3. Whether a different action (e.g., S = Lf, linear) would give -1.0

## Novel prediction
If the exponent is set by the sqrt(f) in the action, then switching to
a LINEAR action S = L*f should give a steeper distance law closer
to the Newtonian prediction. Specifically:
- sqrt action (S ~ sqrt(f)): distance ~ b^(-0.5), F∝M ~ M^0.5
- linear action (S ~ f): distance ~ b^(-1), F∝M ~ M^1.0

This is testable on the same lattice by replacing the action formula.

## Status
PROPOSED — the sqrt(f) → sqrt-distance connection is plausible but
the factor of 2 discrepancy between ray theory (-1.0) and lattice
measurement (-0.5) is unexplained.
