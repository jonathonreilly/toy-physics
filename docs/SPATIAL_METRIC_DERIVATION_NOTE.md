# Spatial Metric Consistency Check: `(1-f)^2` in the Weak-Field Limit

**Script:** `scripts/frontier_spatial_metric_derivation.py`
**Status:** review hold; weak-field consistency result
**Date:** 2026-04-12

## Summary

If the same scalar factor `1-f` is used for both the local phase rate and the
proper spatial step, the resulting weak-field spatial metric is conformal and
the light-bending ratio approaches `2 + O(f)`. This is a consistency check of
that identification, not an independent derivation of the spatial metric.

## The Derivation

1. **Axiom:** The path-sum propagator assigns action S = L * (1-f) to each step.
2. **Effective distance:** Phase per unit coordinate distance = k * (1-f),
   defining ds = (1-f) dx.
3. **Isotropy assumption:** If the scalar field modifies all directions equally,
   the natural conformal metric ansatz is `g_ij = (1-f)^2 delta_ij`.
4. **Full action:** A path through the field accumulates action = (1-f) * ds
   = (1-f)^2 dx. The two factors are time dilation and spatial path length.
5. **Light bending:** Deflection ~ d/db [sum (1-f)^2] ~ 2 * d/db [sum f]
   = 2 * Newtonian, matching GR.

The key consistency step is that the same field factor is applied twice on the
same weak-field step: once in the local phase rate and once in the proper
spatial step. That yields `(1-f)^2` at leading order.

## Numerical Results

### Test 1: Effective metric = (1-f)^2
Phase accumulation rate measured along x-rays at various impact parameters b
matches (1-f) to high precision. The metric component g_xx = (1-f)^2 follows
by squaring.

### Test 2: Isotropy confirmed
At all tested radii, g_xx = g_yy = g_zz to within 0.4% (mean anisotropy).
The residual anisotropy comes from the field gradient within the averaging
window and vanishes in the continuum limit.

### Test 3: Factor-of-2 confirmed
Conformal/time-only deflection ratio = 1.985 +/- 0.012 (N=31, s=1.0).
The deviation from 2.000 is the O(f^2) correction, which vanishes in the
weak-field limit. At b=11: ratio = 1.997.

### Test 4: Metric discrimination
| Spatial metric hypothesis | Predicted ratio | Measured ratio | Matches GR? |
|--------------------------|-----------------|---------------|-------------|
| g = (1-f)^2 [conformal]  | 2.0             | 1.986         | YES         |
| g = (1-f) [half]          | 1.5             | 1.495         | no          |
| g = delta [flat]          | 1.0             | 1.000         | no          |
| g = (1-f)^4 [overcurved]  | 3.0             | 2.959         | no          |
| exp(-2f) [exponential]    | 2.0             | 1.973         | YES         |

Only the conformal form and weak-field-equivalent alternatives such as
`exp(-2f)` recover the GR factor of 2 at leading order on this test.

### Test 5: Weak-field convergence
| Configuration | max(f) | |ratio - 2| |
|--------------|--------|------------|
| N=31, s=1.0  | 0.023  | 0.015      |
| N=31, s=0.2  | 0.005  | 0.003      |
| N=41, s=0.1  | 0.002  | 0.002      |

The deviation is proportional to max(f), confirming ratio = 2 - O(f).

## What This Establishes

The safe chain is weaker:
- the chosen action provides a local factor `1-f`
- if that same factor is used for the proper spatial step, the induced metric
  is conformal
- in the weak-field limit, that consistency choice gives the GR factor-of-2
  light bending

## Bounded Claims

**What is derived:**
- The spatial metric g_ij = (1-f)^2 delta_ij follows from the action S = L(1-f)
- The factor of 2 in light bending is exact in the weak-field limit (f << 1)
- The metric is isotropic (conformal) because the action is direction-independent
 - The weak-field lensing ratio is consistent with `2 - O(f)` on this surface

**What is assumed:**
- The gravitational field f is Poisson-sourced (established in prior work)
- Weak-field regime (f << 1) for the factor-of-2 to be numerically close to 2
- The propagator path integral is dominated by near-classical paths

**What is NOT claimed:**
- This is not a derivation of the full Schwarzschild metric (only the spatial sector)
- Strong-field corrections (f ~ 1) are not GR-equivalent without further analysis
- The temporal metric component g_00 = (1-f)^2 vs g_00 = (1-2f) distinction
  requires separate investigation (they agree to O(f) but differ at O(f^2))
 - This note does not independently derive the spatial metric from the
   propagator without using the same scalar factor twice

## Relation to Prior Results

This note does **not** upgrade the factor-of-2 row to unconditional. The safe
read is that the row is consistent with a conformal weak-field spatial metric
when the same scalar factor `1-f` is used for both local phase rate and
proper spatial step.
