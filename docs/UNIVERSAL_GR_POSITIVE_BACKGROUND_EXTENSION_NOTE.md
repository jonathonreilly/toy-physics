# Universal GR Positive-Background Extension on `PL S^3 x R`

**Status:** support - positive-background extension
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / widening theorem step

## Verdict

The direct universal route now extends beyond the `SO(3)`-invariant family

`D = diag(a,b,b,b)`

to the full **real positive-symmetric background family**.

So the earlier “widening beyond the invariant family” gap is no longer live at
the local operator-family level.

## Why widening is needed at all

The earlier invariant-family theorem closed the direct universal route only on
the spatially isotropic stratum. That was already a real result, but not yet a
universal background statement, because general positive symmetric backgrounds
need not lie on that stratum.

So “widening” meant:

> show that the exact universal operator family is not confined to the
> invariant `diag(a,b,b,b)` slice, but extends to generic positive symmetric
> backgrounds.

That widening is now discharged.

## Exact mechanism of the extension

The key point is that the exact direct-universal Hessian was always a
basis-free object:

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

This formula is exact on the route because it is the second variation of the
exact observable-principle generator

`W[J] = log|det(D+J)| - log|det D|`.

For any real positive-symmetric background `D`, choose an orthogonal
diagonalization

`D = Q^T diag(λ_0, λ_1, λ_2, λ_3) Q`.

Then:

1. the Hessian is orthogonally covariant:

   `B_D(h,k) = B_diag(Q^T h Q, Q^T k Q)`;

2. in the background-adapted principal basis, the Hessian diagonalizes exactly;

3. the exact channel weights are simply:

   - principal strains: `-λ_i^-2`
   - mixed channels: `-(λ_i λ_j)^-1`

So the old widening gap was not a missing new primitive. It was a missing
background-adapted formulation of the already exact universal Hessian.

## Exact positive-background glued family

The exact slice generator `Lambda_R` is already symmetric positive definite on
the branch.

Therefore the full direct-universal glued family is

`K_GR(D) = H_D ⊗ Lambda_R`

with `H_D` the exact Hessian operator induced by

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

For every sampled positive-symmetric background:

- `K_GR(D)` is symmetric positive definite;
- the boundary action has a unique exact stationary point;
- the exact quadratic completion identity holds.

So the direct universal route now has an exact nonlinear operator family on the
full positive-symmetric background class, not only on the invariant family.

## What this changes

This removes the last previously stated widening gap on the direct universal
route.

The branch now has:

- exact scalar observable generator
- exact `3+1` lift `PL S^3 x R`
- exact tensor variational candidate
- exact quotient uniqueness
- exact canonical/invariant localization on the isotropic stratum
- exact isotropic glue operator
- exact invariant-family nonlinear completion
- exact positive-background extension by orthogonal covariance

## Honest status

This is the strongest exact direct-universal gravity result now on the branch.

What remains, if one insists on a still stronger claim, is no longer the local
operator family itself. It would be a stronger global theorem statement about
solution classes / interpretation beyond the exact positive-background
operator-family level.
