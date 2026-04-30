# Universal GR Supermetric Normal Form on `PL S^3 x R`

**Status:** unknown (pending author classification)
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / post-localization theorem step

## Verdict

The direct universal Hessian is now pinned down more sharply than
"block-localized."

On the exact `SO(3)`-invariant lifted background

`D = diag(a,b,b,b)`,

the unique universal Hessian is exactly the inverse-metric contraction on
symmetric `3+1` perturbations.

Equivalently, in the canonical lapse / shift / trace / shear basis, the
Hessian is already the exact local supermetric normal form

`H = -a^-2 P_lapse - (ab)^-1 P_shift - b^-2 P_trace - b^-2 P_shear`.

So the direct universal route is no longer open at the level of local tensor
normal form.

## What is now exact

The direct universal route already had:

- exact scalar observable generator
- exact `3+1` lift `PL S^3 x R`
- exact unique symmetric quotient kernel
- exact canonical block localization
- exact invariant-background Schur localization

The new step identifies what that localized Hessian actually is:

> it is exactly the inverse-metric supermetric pairing on the invariant
> background.

In other words, the local algebraic tensor form is already fixed.

## Exact formula

For symmetric perturbations `h, k` on the invariant background
`D = diag(a,b,b,b)`, the universal Hessian is

`B(h,k) = -Tr(D^-1 h D^-1 k)`.

That is exactly the inverse-metric contraction pairing.

In the canonical symmetric basis, this gives the exact diagonal block
weights:

- lapse: `-a^-2`
- shift: `-(ab)^-1`
- trace: `-b^-2`
- shear: `-b^-2`

with no cross-block leakage.

## What this changes

This removes another layer of ambiguity.

Before:

> maybe the remaining issue was still local block normalization or local
> tensor matching.

Now:

> the local tensor form is already exact. The direct universal Hessian is
> already the canonical isotropic supermetric normal form.

So the remaining GR gap is no longer local.

## What is still open

This still does **not** by itself prove full GR.

The remaining missing theorem is now:

> the exact dynamical gluing law that identifies this local supermetric
> normal form with the full Einstein/Regge operator on `PL S^3 x R`,
> using the route-2 slice dynamics rather than only the local Hessian.

Equivalently:

- local supermetric form: exact
- slice generator / transfer law: present separately
- exact Einstein/Regge glue between them: still missing

That is the current sharp frontier.

## Honest status

The direct universal route is now:

- exact at the scalar observable level
- exact at the `3+1` lift level
- exact at the quotient-kernel level
- exact at the canonical block-localization level
- exact at the invariant-background Schur-localization level
- exact at the local isotropic supermetric-normal-form level
- still open only at the final dynamical gluing / Einstein-Regge identification step
