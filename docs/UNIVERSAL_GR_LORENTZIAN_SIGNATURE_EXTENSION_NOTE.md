# Universal GR Lorentzian Signature-Class Extension on `PL S^3 x R`

**Status:** support - Lorentzian signature-class extension
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / signature-class extension
**Primary runner:** [`scripts/frontier_universal_gr_lorentzian_signature_extension.py`](../scripts/frontier_universal_gr_lorentzian_signature_extension.py) (PASS=6/0)

## Verdict

The direct-universal route extends exactly from the positive-symmetric
background family to the full **nondegenerate Lorentzian `3+1` background
class**.

This is the correct next strengthening beyond positive-background local
closure. The exact universal Hessian never needed positivity for its algebraic
definition. Positivity was only used to get convexity. Once that is separated
out, the route already supports a broader theorem:

> on every nondegenerate Lorentzian background, the direct-universal local
> action remains exact and nondegenerate, and therefore still carries a unique
> exact stationary bridge field for every boundary source.

So the loss of positivity is **not** the loss of closure. It is only the loss
of convexity.

## Exact mechanism

The exact local bilinear form is still

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`.

This formula is defined whenever `D` is invertible.

For Lorentzian signature, `D` is real symmetric and nondegenerate with inertia
`(1,3)` on the current `3+1` route. By exact congruence covariance,

`B_{S^T D S}(S^T h S, S^T k S) = B_D(h,k)`

for every invertible frame change `S`.

So the local universal Hessian is not confined to the positive cone. It is an
exact congruence-covariant object on the whole Lorentzian signature class.

## Exact Lorentzian local operator family

Let `H_D` be the exact operator induced by `B_D`, and let `Lambda_R` be the
exact symmetric positive slice generator already present on the branch.

Then the direct-universal local operator remains

`K_GR(D) = H_D ⊗ Lambda_R`.

On the Lorentzian class:

- `H_D` is no longer positive definite;
- `H_D` remains exactly nondegenerate;
- therefore `K_GR(D)` remains exactly nondegenerate.

So for every Lorentzian background `D` and every boundary source `J`, the
stationary bridge field

`F_* = K_GR(D)^-1 J`

still exists uniquely.

The exact completion identity

`I_GR(F_* + Δ ; D, J) - I_GR(F_* ; D, J)
 = 1/2 <Δ, K_GR(D) Δ>`

still holds. What changes is that the quadratic form is indefinite, as it
should be on a Lorentzian signature class.

## Why this matters

This discharges the last positivity-only restriction on the direct-universal
route.

The branch no longer stops at:

- invariant positive backgrounds;
- generic positive backgrounds;
- local positive-background closure.

It now reaches:

> exact Lorentzian signature-class local closure.

That is a substantial increase in scope, and it is the first direct-universal
statement that actually sits on the physically relevant `3+1` signature class
rather than only on the positive cone.

## Honest status

The direct-universal route is now exact at:

- scalar observable level
- exact `PL S^3 x R` lift level
- exact tensor variational / quotient-kernel level
- exact canonical block-localization level
- exact isotropic glue / nonlinear / positive-background extension level
- exact Lorentzian signature-class local closure level

What remained after the positive-background theorem was a stronger global
solution-class statement. This note does not yet claim that global step by
itself.
