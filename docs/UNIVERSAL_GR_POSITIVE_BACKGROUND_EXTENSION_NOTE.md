# Universal GR Positive-Background Extension on `PL S^3 x R`

**Status:** support - positive-background extension (sign character corrected 2026-05-01)
**Date:** 2026-04-14
**Branch:** `codex/review-active`
**Role:** direct universal route / widening theorem step
**Runner:** `scripts/universal_gr_positive_background_local_closure.py` (shared with the local-closure note; validates the negative-definite Hessian and orthogonal covariance numerically)

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

The key point is that the exact direct-universal Hessian is always a
basis-free object:

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

This formula is exact on the route because it is the second variation of the
exact observable-principle generator

`W[J] = log|det(D+J)| - log|det D|`.

Note the sign: `W[J]` is **concave** on the positive cone (log-det is
concave on positive matrices), so its second variation is negative-definite
on symmetric tangents. Concretely, with `H̃ := D^{-1/2} h D^{-1/2}` (symmetric)
one has

`B_D(h,h) = -Tr(D^-1 h D^-1 h) = -Tr(H̃²) ≤ 0`,

with equality iff `h = 0`. So `H_D` is symmetric **negative-definite** on the
symmetric tangent space — not positive-definite, as an earlier draft of this
note claimed. The principal-basis weight formulas below carry the same sign:

For any real positive-symmetric background `D`, choose an orthogonal
diagonalization

`D = Q^T diag(λ_0, λ_1, λ_2, λ_3) Q`.

Then:

1. the Hessian is orthogonally covariant:

   `B_D(h,k) = B_diag(Q^T h Q, Q^T k Q)`;

2. in the background-adapted principal basis, the Hessian diagonalizes exactly
   with **negative** eigenvalues;

3. the exact channel weights are:

   - principal strains: `−λ_i^{-2}` (negative)
   - mixed channels:  `−(λ_i λ_j)^{-1}` (negative)

So the old widening gap was not a missing new primitive — it was a missing
background-adapted formulation of the already exact universal Hessian. The
orthogonal-covariance content of the extension is unaffected by the sign
correction; only the polarity label was wrong.

## Exact definite-background glued family

The exact slice generator `Lambda_R` is symmetric positive-definite on the
branch (independent calculation, unaffected by the sign correction above).

Therefore the full direct-universal glued family is

`K_GR(D) = H_D ⊗ Lambda_R`

with `H_D` the exact Hessian operator induced by

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

Because `H_D ≺ 0` and `Lambda_R ≻ 0`, the tensor product satisfies

`K_GR(D) ≺ 0`     (symmetric **negative**-definite — corrected from the earlier "SPD" claim).

For every sampled positive-symmetric background:

- `K_GR(D)` is symmetric **negative-definite** (an earlier draft labelled it
  positive-definite; that polarity was inconsistent with `B_D = -Tr(...)`).
- The boundary action `I_GR(F; D, J) = (1/2)<F, K_GR F> − <J, F>` is
  **concave**, with a unique exact stationary point `F_* = K_GR(D)^{-1} J`
  that maximizes `I_GR`. Equivalently `J_GR := −I_GR` is convex with a
  unique minimum.
- The exact quadratic completion identity holds with non-positive
  remainder:
  `I_GR(F_* + Δ) − I_GR(F_*) = (1/2) <Δ, K_GR(D) Δ> ≤ 0`,
  with equality iff `Δ = 0`.

So the direct universal route has an exact nonlinear operator family on the
full positive-symmetric background class, not only on the invariant family.
The substantive content of the extension — orthogonal covariance,
background-adapted diagonalization, principal-channel weights, existence
and uniqueness of the stationary boundary field — is unchanged by the sign
correction. Only the polarity label moves from positive-definite to
negative-definite. See
[UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md](UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md)
for the matching sign correction in the local-closure note and the shared
runner that validates the negative-definite character numerically.

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

This is the strongest exact direct-universal gravity result now on the
branch, with the operator polarity now stated correctly
(negative-definite, not positive-definite). The substantive deliverables
of the extension — orthogonal covariance, principal-basis diagonalization,
unique stationary boundary field on every positive-symmetric background —
all hold under the corrected sign analysis.

What remains, if one insists on a still stronger claim, is no longer the
local operator family itself. It would be a stronger global theorem
statement about solution classes / interpretation beyond the exact
definite-background operator-family level.
