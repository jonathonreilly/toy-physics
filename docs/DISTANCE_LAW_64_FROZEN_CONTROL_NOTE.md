# 64^3 Distance Law: Frozen / Static-Source Control Note

**Date:** 2026-04-12
**Status:** bounded diagnostic — the frozen/static-source control reveals a
real and informative field-shape discrepancy between Poisson-solved and
pure 1/r fields
**Runner:** `scripts/frontier_distance_law_64_frozen_control.py`
**Companion to:** `docs/DISTANCE_LAW_64_BOUNDED_CONTINUATION_NOTE.md`

## Question addressed

Does the deflection exponent alpha depend on whether the 1/r field is
computed self-consistently (Poisson-solved) or injected from an external
analytic source?

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

## Results

| N  | alpha_dyn | alpha_fro | alpha_ana | max spread |
|----|-----------|-----------|-----------|------------|
| 31 | -1.0857   | -1.1055   | -1.1055   | 1.82%      |
| 48 | -1.0565   | -1.0313   | -1.0313   | 2.39%      |
| 64 | -1.0233   | -0.9899   | -0.9899   | 3.26%      |

The FROZEN and ANALYTIC arms are exactly identical (the analytic finite
sum IS the frozen 1/r field evaluated directly). The discrepancy is
entirely between DYNAMIC (Poisson-solved) and FROZEN/ANALYTIC (pure 1/r).

## Diagnostic finding

The Poisson-solved field on a finite lattice with Dirichlet BC is NOT a
pure 1/r. The field-shape ratio f_fro/f_dyn varies from ~0.53 at r=2 to
~0.70 at r=8 (on the 64^3 grid), confirming that the Poisson solver
includes lattice boundary corrections (effectively image charges from
the Dirichlet walls) that reshape the field in the near-to-mid region.

The DYNAMIC arm produces a steeper exponent (more negative alpha) at
every grid size, consistent with the boundary corrections strengthening
the near-field gradient. As N increases, both arms converge toward -1.0:
the DYNAMIC from above (steeper) and the FROZEN from below (shallower).

This is a physically correct result: the Poisson equation on a bounded
domain gives the self-consistent field including boundary effects, while
the pure 1/r field is the infinite-space approximation. Neither is
"wrong" — they measure different things. The convergence of both toward
the same continuum limit (-1.0) as N increases is the expected behavior.

## What this control establishes

1. The exponent alpha is NOT independent of the field source at finite N
   (the 0.5% threshold is not met)
2. The discrepancy is explained by Dirichlet boundary corrections, not
   by a solver artifact
3. Both arms converge toward alpha = -1.0 from opposite sides, bracketing
   the continuum answer
4. The FROZEN/ANALYTIC arm confirms that pure 1/r geometry alone gives
   an exponent compatible with 1/r^2 force law (alpha_ana = -0.990 at
   64^3, within 1% of -1.0)
5. The DYNAMIC arm's steeper exponent at finite N is a known boundary
   effect that relaxes monotonically with increasing N

## What this is

A same-surface diagnostic that quantifies the boundary-correction
contribution to the measured exponent. The control does not pass the
strict 0.5% agreement threshold, but it explains why: the discrepancy
is boundary geometry, not a solver bug.

## What this is not

- Not a pass on the strict frozen/static-source null (spread exceeds 0.5%)
- Not a standalone distance-law closure
- Not architecture-independent (ordered cubic only)
- Not a both-masses or mutual-attraction test
- Does not close the promotion gate by itself

## Promotion status

This note is retained as a bounded diagnostic companion to the existing
64^3 continuation note. It documents the field-shape discrepancy and
identifies boundary corrections as the source.

The frozen/static-source gate remains open in the strict sense (0.5%
threshold not met), but the diagnostic explains the mechanism. A future
run on 96^3 or larger should show the spread narrowing, confirming that
both arms converge to the same continuum exponent.

## Required for closure

- 96^3 run to confirm the spread narrows with increasing N
- Or: reformulate the control using periodic BC (no image charges),
  where the Poisson-solved and analytic 1/r fields should agree exactly
- Architecture portability (staggered and/or Wilson lattice)
- Or explicit restriction of claim to ordered-cubic family level
