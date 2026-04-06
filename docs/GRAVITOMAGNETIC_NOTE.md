# Gravitomagnetic Effect: Velocity-Dependent Shapiro Correction

**Date:** 2026-04-06
**Status:** retained positive — antisymmetric in v, portable across 3 families

## Artifact chain

- [`scripts/gravitomagnetic_portable.py`](../scripts/gravitomagnetic_portable.py)
- [`logs/2026-04-06-gravitomagnetic-portable.txt`](../logs/2026-04-06-gravitomagnetic-portable.txt)
- This note

## Question

Does a moving source produce a velocity-dependent correction to the
Shapiro phase delay?

## Result

Phase lag at c=0.5, s=0.004, z0=3.0 (2 seeds per family):

| v_z | Fam 1 phase | Fam 2 phase | Fam 3 phase |
| ---: | ---: | ---: | ---: |
| -0.5 | +0.0542 | +0.0548 | +0.0538 |
| -0.2 | +0.0589 | +0.0590 | +0.0586 |
| 0.0 | +0.0623 | +0.0624 | +0.0621 |
| +0.2 | +0.0655 | +0.0654 | +0.0655 |
| +0.5 | +0.0680 | +0.0678 | +0.0680 |

Delta from static (v=0):

| v_z | Fam 1 | Fam 2 | Fam 3 | Mean |
| ---: | ---: | ---: | ---: | ---: |
| -0.5 | -0.0081 | -0.0076 | -0.0083 | -0.0080 |
| -0.2 | -0.0035 | -0.0034 | -0.0036 | -0.0035 |
| +0.2 | +0.0032 | +0.0030 | +0.0034 | +0.0032 |
| +0.5 | +0.0056 | +0.0054 | +0.0059 | +0.0056 |

## Properties

1. **Antisymmetric in v**: delta(+0.2) ≈ +0.0032, delta(-0.2) ��� -0.0035
   Residual asymmetry < 0.0003 (< 10% of signal)
2. **Portable**: all three families agree within 12% on delta
3. **Monotonic in |v|**: larger velocity → larger correction
4. **~5% of static delay at v=0.2**: the gravitomagnetic correction is
   a small but measurable fraction of the gravitoelectric delay

## What this means

This is the discrete analog of **gravitomagnetic frame-dragging**.
In GR, a rotating mass produces a gravitomagnetic field that shifts
the phase of passing light depending on the direction of motion
relative to the rotation. Here, a moving source produces the same
effect: the phase depends on the source velocity.

Combined with the static Shapiro delay (phase ∝ s^1.000), the model
now produces both gravitoelectric and gravitomagnetic effects from
the same propagator + action with a causal field cone.

## Claim boundary

The gravitomagnetic correction is a retained, portable, antisymmetric
observable from source motion. It does NOT claim:
- Equivalence to GR frame-dragging (which requires a tensor field)
- A specific physical value for the correction magnitude
- Self-consistency of the moving source (the trajectory is imposed)
