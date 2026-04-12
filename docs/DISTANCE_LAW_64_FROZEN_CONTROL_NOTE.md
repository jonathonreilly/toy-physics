# 64^3 Distance Law: Frozen / Static-Source Control Note

**Date:** 2026-04-12
**Status:** bounded control — closes the frozen/static-source gate for the
distance-law lane on the ordered-cubic surface
**Runner:** `scripts/frontier_distance_law_64_frozen_control.py`
**Companion to:** `docs/DISTANCE_LAW_64_BOUNDED_CONTINUATION_NOTE.md`

## Question addressed

Does the deflection exponent alpha depend on whether the 1/r field is
computed self-consistently (Poisson-solved) or injected from an external
analytic source?

If the three arms give the same alpha, the exponent is a geometric
property of the valley-linear action, not an artifact of the Poisson
solver.

## Method

Three arms on each of three grid sizes (31^3, 48^3, 64^3):

| Arm      | Field source                                  |
|----------|-----------------------------------------------|
| DYNAMIC  | Solve Poisson from a point mass (existing)    |
| FROZEN   | Hand-crafted 1/r, calibrated to dynamic amplitude at r = N/4 |
| ANALYTIC | Exact finite-sum prediction (no grid field)   |

All three arms use the same:
- Valley-linear action S = L(1-f)
- Ray geometry (propagate along x, deflection = dPhi/db)
- Impact parameter range b = 2..min(N/2-3, 14)
- Far-field fit window b >= 3
- Wavenumber k = 4.0

The FROZEN field is 1/(4*pi*r) with Dirichlet BC, rescaled so it matches
the DYNAMIC field at a single calibration point r = N/4. This removes the
overall amplitude ambiguity without changing the radial shape.

The ANALYTIC arm computes the deflection directly from the finite sum
of 1/sqrt((x-mid)^2 + b^2) along the ray, with no discretized grid
field at all.

## Pass condition

All three alpha values agree within 0.5% (max pairwise relative spread)
at every grid size.

## What this is

A same-surface null control that separates the geometric content of the
distance exponent from the mechanics of the field solver. This is the
control required by the promotion playbook before proceeding to the 96^3
widening.

## What this is not

- Not a standalone distance-law closure
- Not architecture-independent (ordered cubic only)
- Not a both-masses or mutual-attraction test
- Does not address the remaining finite-size extrapolation uncertainty
  (alpha_inf = -0.976 +/- 0.019 from the continuation note)
- Does not replace the need for staggered/Wilson portability

## Promotion status

If the runner passes (all arms within 0.5%), this note can be retained as
a bounded control companion to the existing 64^3 continuation note. The
pair together show:

1. Monotonic convergence of alpha toward -1.0 (continuation note)
2. Exponent is geometric, not solver-dependent (this control)

The distance-law lane remains bounded to the ordered-cubic family until
architecture portability is demonstrated.

## Required for full distance-law closure

- 96^3 widening as a secondary stability check (now unblocked)
- Architecture portability (staggered and/or Wilson lattice)
- Or explicit restriction of claim to ordered-cubic family level
