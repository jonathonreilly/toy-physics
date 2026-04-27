# Structured Mirror Born-Safe Scan Note

**Date:** 2026-04-03  
**Status:** no proposed_retained Born-safe structured-mirror pocket found in the scanned linear family

This note freezes the bounded search for a review-safe structured-mirror
variant using the strictly linear propagator.

Artifacts:
- [`scripts/structured_mirror_bornsafe_scan.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_bornsafe_scan.py)

## Search Question

Starting from the structured mirror growth family, is there a parameter set
that keeps meaningful decoherence and gravity while also passing the corrected
three-slit Born harness?

## Search Family

The scan used the 3D structured mirror growth geometry from
[`scripts/structured_mirror_growth.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_growth.py),
with the strictly linear propagator imported from
[`scripts/mirror_born_audit.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_born_audit.py).

Scanned parameters:

- `d_growth = 2`
- `N = 25, 30, 40`
- `npl_half = 8, 12, 16, 20`
- `connect_radius = 2.5, 3.0, 3.5, 4.0, 4.5`
- `grid_spacing = 1.0, 1.25, 1.5`
- `layer_jitter = 0.0, 0.15, 0.3`
- `2` seeds per config in the broad sweep
- a follow-up `6`-seed confirmation on the best near-Born candidate

The scan measured:

- `d_TV`
- `pur_cl`
- `S_norm`
- gravity
- corrected Born `|I3|/P`
- `k=0` gravity control

## Result

No scanned structured-mirror configuration reached the corrected Born
threshold of machine precision.

The best near-Born candidate in the broad sweep was:

- `N = 40`
- `npl_half = 12`
- `connect_radius = 3.0`
- `grid_spacing = 1.25`
- `layer_jitter = 0.0`
- `d_TV = 0.1208`
- `pur_cl = 0.9992`
- `S_norm = 0.0009`
- gravity `+0.3811`
- Born `8.79e-03`
- `k=0 = 0.00e+00`

That candidate was then re-run with `6` seeds and kept the same Born
readout, so it is not a seed fluke.

## Interpretation

- The structured mirror growth family still produces interesting geometry and
  a nontrivial gravity read.
- But under the scanned linear-propagator configurations, it does **not**
  retain a Born-safe pocket.
- The practical conclusion is negative: this family is not the current
  Born-safe structured-mirror successor.

## Bottom Line

- exact mirror and `Z2 x Z2` remain the review-safe symmetry lanes
- structured mirror growth is a useful negative control, not a retained
  Born-safe replacement
