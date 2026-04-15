# Phase-Lift Candidate for the Common Polarization Bridge

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** minimal exact extension of the common bridge that carries the residual dark-plane angle

## Verdict

The common bridge can be extended exactly to carry the last connected `SO(2)`
angle.

The minimal exact extension is:

`K_R^phase(q) := (u_E, u_T, delta_A1 u_E, delta_A1 u_T, d_y, d_z)`

where `(d_y, d_z)` is the exact support-side dark pair on the residual dark
`T1` plane.

Equivalently, the extension can be written using:

- `rho_R := sqrt(d_y^2 + d_z^2)`
- `vartheta_R := atan2(d_z, d_y)`

So the current exact common bridge does admit an exact angle-carrying
extension.

## Exact lifted bridge

The current common exact bridge triple is:

`B_R = (K_R, I_TB, Xi_TB)`.

The minimal exact angle-carrying extension is:

`B_R^phase := (K_R^phase, I_TB^phase, Xi_TB^phase)`

with:

- `K_R^phase = (K_R, D_R)`
- `I_TB^phase = I_R + 1/2 ||a - K_R^phase||^2`
- `Xi_TB^phase = vec(K_R^phase) \otimes exp(-t Lambda_R) u_*`

This is exact as a construction because:

- `K_R` is exact;
- `D_R = (d_y, d_z)` is exact on the support side;
- the semigroup factor `exp(-t Lambda_R)` is exact.

## Transformation law

Under the residual connected dark-plane `SO(2)` rotation:

- the bright block `K_R` is unchanged;
- the dark pair rotates covariantly;
- `rho_R` is invariant;
- `vartheta_R` shifts by the gauge angle.

Therefore `vartheta_R` trivializes the connected orbit locally wherever
`rho_R != 0`.

## What this changes

This sharpens the frontier again.

Before:

> the common exact bridge is blind to the dark angle.

Now:

> the current common bridge is blind to the dark angle, but it has a minimal
> exact extension that carries it.

So the remaining issue is no longer the existence of an angle-carrying common
object. It is:

> whether the phase-lifted bridge `B_R^phase` has a canonical
> curvature-localization interpretation on the universal side.

## Remaining gap

The phase-lifted bridge is exact on the support / semigroup side, but the
current atlas still does not prove that its dark-phase coordinates define a
canonical curvature-localization section or a full Einstein/Regge dynamics law.

So the remaining theorem target is:

> canonically lift `vartheta_R` from the support-side phase-lifted bridge into
> the universal curvature-localization bundle.

## Bottom line

The all-out push has now separated two questions:

1. Does an exact angle-carrying bridge exist?
   - **Yes.** `B_R^phase` is the minimal exact candidate.
2. Does that exact angle-carrying bridge already close GR?
   - **No.** The remaining gap is its canonical curvature interpretation.
