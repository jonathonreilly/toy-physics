# Universal GR Tensor Quotient Uniqueness Candidate on `PL S^3 x R`

**Date:** 2026-04-14
**Branch:** `codex/review-active`
**Role:** direct universal route / theorem step
**Purpose:** isolate the unique symmetric `3+1` quotient kernel carried by the
exact tensor-valued variational candidate

## Verdict

The direct universal route is still not closed, but the tensor-valued
variational candidate is now pinned down more sharply than before.

The exact scalar observable principle gives the generator

`W[J] = log|det(D+J)| - log|det D|`

and Route 2 gives the exact `3+1` kinematic background

`PL S^3 x R`.

The exact tensor-valued candidate

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`

now has a sharper status:

- on the symmetric `3+1` perturbation quotient, it is the unique bilinear lift
  of the scalar generator at quadratic order;
- on the finite `3+1` prototype used by the current runner, that quotient
  kernel is nondegenerate;
- there is no extra tensor-bilinear freedom hiding in the scalar observable
  principle on the current prototype.

This is the strongest exact identification result currently available on the
direct universal path.

## What the runner checks

The current audit runner evaluates the Hessian candidate on a finite symmetric
`3+1` perturbation basis and checks that:

1. the bilinear form is symmetric;
2. the symmetric quotient basis has full rank;
3. the scalar line restriction matches the same Hessian construction;
4. there are no hidden null directions on the prototype symmetric quotient.

That is enough to justify the uniqueness-candidate language.

## What this does not prove

This does **not** prove that the kernel is Einstein/Regge dynamics.

The remaining task is a curvature-localization map:

> a map that identifies the unique symmetric `3+1` Hessian kernel with the
> Einstein/Regge tensor law on the `PL S^3 x R` background

If that map is derived, the direct universal route advances from tensor
candidate to genuine metric dynamics.

## Honest status

The current direct-universal route is:

- exact at the scalar observable level
- exact at the `3+1` kinematic lift level
- exact at the symmetric `3+1` quotient-kernel level
- blocked at the curvature-localization level

That is the sharpest disciplined statement available on the current atlas.
