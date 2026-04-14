# Universal GR Curvature Localization Blocker Note

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / blocker note  
**Purpose:** isolate the minimal missing primitive on the straight-to-full-GR
path after the exact scalar observable generator, exact `3+1` lift, exact
tensor-valued variational candidate, and unique symmetric quotient kernel are
already in hand

## Verdict

The direct universal route is still blocked.

The current axiom-first stack gives:

- an exact scalar observable generator from the observable principle
- an exact `3+1` kinematic lift on `PL S^3 x R`
- an exact tensor-valued variational candidate on that lifted background
- an exact unique symmetric `3+1` quotient kernel on the finite prototype

It does **not** yet give:

- an exact curvature-localization operator that carries that Hessian kernel
  into the Einstein/Regge tensor law on the full `3+1` metric space

So the remaining gap is no longer a scalar or quotient-uniqueness problem.
It is the missing localization map itself.

The current runner now also checks whether that localization map can be
reconstructed from the present quotient kernel plus a choice of channel
frame. It cannot. Two valid `3+1` polarization frames give different
localized channel coefficients for the same tensor candidate, so the current
stack does not supply a canonical `Pi_curv`.

## What is exact already

### Scalar generator

The axiom-side observable principle gives the scalar generator

`W[J] = log|det(D+J)| - log|det D|`

This is exact, but scalar.

### `3+1` lift

Route 2 gives the exact kinematic background

`PL S^3 x R`.

That is exact on the current atlas, but kinematic only.

### Tensor variational candidate

The scalar generator can be lifted into a tensor-valued quadratic form by
taking its metric-source Hessian on the lifted background:

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`.

This is the exact tensor-valued variational candidate, but it is still only a
variational object until a curvature-localization map is supplied.

### Quotient uniqueness

On the symmetric `3+1` perturbation quotient, the Hessian kernel is the
unique bilinear lift of the scalar generator at quadratic order. On the finite
prototype used by the current runner, that quotient kernel is nondegenerate.

That proves uniqueness of the tensor candidate on the quotient. It does not
identify the kernel with Einstein/Regge curvature dynamics.

## Why the current stack stops here

The present data determine a unique bilinear kernel on the symmetric quotient,
but they do not specify how to localize that kernel into curvature channels on
`PL S^3 x R`.

In particular, the current stack has no exact operator that:

1. is tensor-valued and covariant on the `3+1` quotient;
2. splits the Hessian kernel into lapse, shift, and spatial trace/shear
   components;
3. identifies those components with the Einstein/Regge tensor law.

Without that operator, the Hessian remains a variational candidate, not a GR
dynamics law.

## Minimal missing primitive

The smallest honest missing object is now:

> a covariant `3+1` polarization-frame / projector bundle, with a
> distinguished connection, that canonically splits the unique symmetric
> Hessian kernel into lapse, shift, and spatial trace/shear channels before
> localization.

Equivalently, the missing primitive is still a covariant `3+1`
curvature-localization operator `Pi_curv`, but the current stack shows that
`Pi_curv` is not derivable without that extra frame primitive.

The localization operator itself would then turn the quotient kernel into a
curvature law rather than merely a bilinear form.

## Honest status

The current direct universal route is:

- exact at the scalar observable level
- exact at the `3+1` kinematic lift level
- exact at the symmetric `3+1` quotient-kernel level
- blocked at the curvature-localization level

That is the sharpest disciplined statement available on the current atlas.
