# Causal Propagating Field

**Date:** 2026-04-06
**Status:** proposed_retained positive — dynamic causal cone produces distinct observable

## Artifact chain

- [`scripts/causal_propagating_field.py`](../scripts/causal_propagating_field.py)
- This note

## Question

Does a causally propagating field (expanding cone from the source)
produce a measurably different beam response than a static field?

## Result

Three field types on grown geometry (drift=0.2, restore=0.7):

| Field | Deflection ratio | Escape | Mechanism |
| --- | ---: | ---: | --- |
| Instantaneous | 1.000 | 1.030 | Full 1/r everywhere |
| Forward-only | 0.63 | 1.018 | 1/r only at layers >= source |
| Dynamic (c=1) | 0.63 | 1.008 | 1/r within cone, c*dt reach |
| Dynamic (c=0.5) | **0.45** | 1.003 | 1/r within narrow cone |

### Stability

- Forward-only ratio: 0.63 stable across s=0.001-0.016 and seeds 0-5
- Dynamic (c=0.5) ratio: 0.45 stable across seeds (0.456 vs 0.450)
- Theoretical prediction for forward-only: (NL-gl)/NL = 0.667 (matches to 5%)

### What the dynamic cone adds

At c=1: the causal cone fills the full transverse space by the time it
matters, so dynamic ≈ forward-only. The cone shape doesn't change the physics.

At c=0.5: the narrow cone restricts the field to a smaller transverse
region. The beam sees a WEAKER field along its path. This produces 28%
less deflection than forward-only (0.45 vs 0.63).

The **dynamic/instantaneous ratio is a direct measure of the field
propagation speed c**. If c were measurable, this would distinguish
the model from instantaneous Newtonian gravity.

## Claim boundary

The causal propagating field produces a distinct, stable, geometry-independent
observable (the dynamic ratio). This is a property of the field's spatial
structure, not of the propagator or action.

This does NOT claim:
- A self-consistent propagating field (the cone is imposed, not derived)
- A specific physical value for c
- Equivalence to GR gravitational waves (which require tensor perturbations)
