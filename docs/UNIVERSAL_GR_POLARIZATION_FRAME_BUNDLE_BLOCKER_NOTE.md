# Universal GR Polarization-Frame Bundle Blocker Note

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / blocker note  
**Purpose:** isolate the smallest missing primitive on the straight-to-full-GR
path after the exact scalar observable generator, exact `3+1` lift, exact
tensor-valued variational candidate, and unique symmetric quotient kernel are
already in hand

## Verdict

The direct universal route is still blocked, and the block is now exact.

The current axiom-first stack gives:

- an exact scalar observable generator from the observable principle
- an exact `3+1` kinematic lift on `PL S^3 x R`
- an exact tensor-valued variational candidate on that lifted background
- an exact unique symmetric `3+1` quotient kernel on the finite prototype

It does **not** yet give:

- a covariant `3+1` polarization-frame / projector bundle that canonically
  splits the symmetric Hessian kernel into lapse, shift, and spatial
  trace/shear channels before localization
- an exact curvature-localization operator `Pi_curv` derivable from the
  current stack alone

So the remaining gap is no longer a scalar, quotient-uniqueness, or generic
action problem. It is the missing covariant frame / projector bundle itself.

The current runner checks whether a canonical `Pi_curv` can be reconstructed
from the present quotient kernel by comparing two valid `3+1` polarization
frames. It cannot. The localized channel coefficients move under frame
rotation, so the current stack does not canonically fix the lapse/shift/shear
splitting.

The strongest exact object available here is the associated orbit of
localized channels over the valid `3+1` polarization frames. That orbit is
exact, but the stack does not supply a distinguished connection or horizontal
distribution that picks a canonical section.

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

In particular, the current stack has no exact object that:

1. is tensor-valued and covariant on the `3+1` quotient;
2. splits the Hessian kernel into lapse, shift, and spatial trace/shear
   components;
3. identifies those components with the Einstein/Regge tensor law.

Without that object, the Hessian remains a variational candidate, not a GR
dynamics law.

## Minimal missing primitive

The smallest honest missing object is now:

> a covariant `3+1` polarization-frame / projector bundle, equipped with a
> distinguished connection, that canonically selects one section from the
> exact orbit of localized channels and splits the unique symmetric Hessian
> kernel into lapse, shift, and spatial trace/shear channels before
> localization.

Equivalently, the missing primitive is still a covariant `3+1`
curvature-localization operator `Pi_curv`, but the current stack shows that
`Pi_curv` is not derivable without that extra frame primitive. The exact
structure available today is the frame-orbit family of candidate
localizations, not a canonical projector bundle.

## Honest status

The current direct universal route is:

- exact at the scalar observable level
- exact at the `3+1` kinematic lift level
- exact at the symmetric `3+1` quotient-kernel level
- blocked at the curvature-localization level

That is the sharpest disciplined statement available on the current atlas.
