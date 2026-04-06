# Adaptive / Coevolving Geometry Scout No-Go

**Date:** 2026-04-05  
**Status:** compact no-go / not retained

## One-line read

The existing distinguishability-weighted node-placement machinery does
produce geometry that evolves rather than being imposed, but the smallest
weak-field scout we tried did **not** give a robust retained gravity
signal. The sign is seed-sensitive and changes with placement strength, so
this lane is not yet a clear positive.

## What was tested

The probe reused the current generated-geometry machinery in
[`scripts/node_placement_emergence.py`](/Users/jonreilly/Projects/Physics/scripts/node_placement_emergence.py):

- geometry evolves via distinguishability-weighted post-barrier placement
- weak-field observable only: far-field mass-induced centroid shift
- comparison against the flat-field control for the same geometry

The quick check swept `alpha ∈ {0, 1, 2, 4, 8}` over a small seed set and
measured the mean gravity shift sign.

## Quick probe read

The sign is mixed rather than stable:

- `alpha = 0.0`: `13/18` TOWARD, mean shift `+0.855`
- `alpha = 1.0`: `10/18` TOWARD, mean shift `+0.176`
- `alpha = 2.0`: `10/17` TOWARD, mean shift `+0.580`
- `alpha = 4.0`: `6/15` TOWARD, mean shift `-0.069`
- `alpha = 8.0`: `5/10` TOWARD, mean shift `+0.073`

The baseline is already noisy, and the evolving-geometry rows do not
improve the sign stability in a way that would justify a retained claim.

## Safe conclusion

- geometry-evolves-not-imposed is real in the placement rule
- the smallest weak-field scout did **not** produce a clean adaptive-geometry
  positive
- this is currently a **bounded no-go**, not a publishable retention point

## Next if revisited

If this lane comes back, it should not be a broader sweep. It should be a
single new control law that directly regulates the geometry observable
itself, rather than only biasing distinguishability.
