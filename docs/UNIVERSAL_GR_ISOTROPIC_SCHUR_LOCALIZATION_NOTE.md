# Universal GR Isotropic Schur Localization on `PL S^3 x R`

**Status:** support - exact isotropic Schur-localization step
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / isotropic background theorem step

## Verdict

The direct universal branch is stronger than the recent anisotropic
prototype audit suggested.

On the exact `PL S^3 x R` route, the lifted background is spatially
`SO(3)`-invariant. That forces the background source to lie entirely in the
exact `A1` core:

- lapse
- spatial trace

Equivalently, any invariant lifted background has the form

`diag(a,b,b,b)`.

On that exact invariant background, the universal Hessian candidate

`B(h,k) = D^2 W[g_*](h,k)`

Schur-localizes exactly under the canonical block projectors

- `P_lapse`
- `P_shift`
- `P_trace`
- `P_shear`

and the old `trace <-> shear` mixer disappears identically.

So the previous rank-1 trace-shear obstruction was a feature of the
anisotropic toy prototype `diag(2,3,5,7)`, not the invariant direct
universal background.

## Exact invariant-background theorem

The direct universal route already had:

- exact scalar generator `W[J] = log|det(D+J)| - log|det D|`
- exact `3+1` lift `PL S^3 x R`
- exact invariant `A1` projector
- exact Casimir block split into lapse / shift / trace / shear

The missing step was to apply the route's own spatial symmetry to the
background point.

Under valid spatial rotations, the fixed subspace on the symmetric `3+1`
source representation is exactly the 2D `A1` core. Therefore any
`SO(3)`-invariant lifted background must be of the form

`diag(a,b,b,b)`.

That is the only spatially isotropic background family compatible with the
direct universal route.

## Exact Schur localization

For `D = diag(a,b,b,b)`, the universal Hessian candidate on the canonical
symmetric `3+1` basis satisfies:

- `P_lapse H = H P_lapse`
- `P_shift H = H P_shift`
- `P_trace H = H P_trace`
- `P_shear H = H P_shear`

and all cross-block leakages vanish:

- lapse `↔` shift = `0`
- shift `↔` shear = `0`
- trace `↔` shear = `0`

So the canonical block split is exact on the invariant background.

The shift and shear blocks are also exact scalar Schur blocks.

## Closed-form block coefficients

On `D = diag(a,b,b,b)`, the block coefficients are exactly:

- `alpha_lapse = -a^-2`
- `alpha_shift = -(ab)^-1`
- `alpha_trace = -b^-2`
- `alpha_shear = -b^-2`

So the entire direct-universal Hessian takes the exact block form

`H = alpha_lapse P_lapse + alpha_shift P_shift + alpha_trace P_trace + alpha_shear P_shear`.

In particular:

- the shift block is exact and isotropic
- the traceless-shear block is exact and isotropic
- the trace and shear coefficients already agree exactly on the invariant
  background

## What this changes

This removes the strongest recent direct-universal blocker.

Before:

> the universal branch still had a rank-1 `trace <-> shear` mixer.

Now:

> on the correct `SO(3)`-invariant lifted background, the universal Hessian
> already Schur-localizes exactly into lapse / shift / trace / shear.

So the direct universal route is no longer blocked by complement
canonicalization or by trace-shear leakage on the invariant background.

## Remaining open issue

This still does **not** finish full GR.

What remains is smaller:

> identify the already-localized isotropic universal Hessian with the
> Einstein/Regge operator, including the final normalization/sign
> interpretation on the invariant `PL S^3 x R` background.

That is now an operator-identification problem, not a localization problem.

## Honest status

The current direct universal route is now:

- exact at the scalar observable level
- exact at the `3+1` lift level
- exact at the quotient-kernel level
- exact at the canonical block-localization level
- exact at the invariant-background Schur-localization level
- still open only at the final Einstein/Regge operator identification level
