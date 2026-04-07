# Vector Sector: Circular Orbit Handedness

**Date:** 2026-04-06
**Status:** promising positive, not yet retained — start-phase dependence needs resolution

## Artifact chain

- [`scripts/vector_sector_circular_orbit.py`](../scripts/vector_sector_circular_orbit.py)
- This note

## Question

Does an orbiting source produce a deflection that depends on the orbit
direction (handedness), with matched scalar exposure?

## Result

At f=0.02, R=4.0, s=0.004:

| Metric | CCW | CW |
| --- | ---: | ---: |
| dz | **+0.007** | **-0.008** |
| avg 1/r | 0.17724 | 0.17724 |

The dz component flips sign between CCW and CW. Scalar exposure is
exactly matched.

### What passes

- **Exposure match**: avg_1/r(CCW) = avg_1/r(CW) exactly
- **dz sign flip**: CCW gives +dz, CW gives -dz (f=0.01-0.07)
- **Nulls**: s=0 exact, f=0 gives CCW=CW exactly
- **Family portable**: 3/3 families show the flip
- **Speed dependence**: effect present at f=0.01-0.07, vanishes at f=0.10

### What doesn't pass cleanly

- **Start-phase dependence**: 3 of 5 starting phases show the dz flip,
  but 2 do not (phi0=pi/2 and phi0=3*pi/2). The handedness is not
  fully phase-independent.

## Why linear drift fails but circular orbit succeeds

Linear drift changes the scalar exposure: +v brings the source closer
(more 1/r), -v takes it farther (less 1/r). The force asymmetry is
entirely from distance change.

Circular orbit keeps the same distance at all times. The asymmetry
comes from the ORDER in which the source passes through different
positions along the beam path. CW and CCW trace the same positions
but in opposite temporal order, creating a chirality in the
accumulated phase pattern.

This is the discrete analog of the right-hand rule: a current loop
creates a magnetic field with handedness determined by the current
direction. Here, the orbiting source creates a phase pattern with
handedness determined by the orbit direction.

## Next steps before retention

1. Resolve start-phase dependence (2/5 phases fail)
2. Check if the effect is a dynamic ordering effect (time-order control)
3. Verify the dz flip is not a lattice anisotropy artifact
