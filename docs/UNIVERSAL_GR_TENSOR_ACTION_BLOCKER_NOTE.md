# Universal GR Tensor Action Blocker Note

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / blocker note  
**Purpose:** identify the minimal missing primitive on the straight-to-full-GR path

## Verdict

The direct universal GR route is still **blocked**.

The current axiom-first stack gives:

- an exact scalar observable generator from the axiom-side observable principle
- an exact `3+1` kinematic lift on `PL S^3 x R`
- an exact tensor-valued variational candidate on that lifted background

It does **not** yet give:

- an exact tensor-valued `3+1` action identified with Einstein/Regge dynamics
  at the full metric level
- an exact tensor-valued uniqueness theorem forcing that identification

So the current theorem step is not a closure claim. It is the exact minimal
missing identification for the direct universal route.

## What is exact already

### Scalar observable generator

The axiom-side observable principle gives the scalar generator

`W[J] = log|det(D+J)| - log|det D|`

This is the unique additive CPT-even scalar generator on the exact Grassmann
Gaussian surface. It is exact, but it is scalar.

### Route-2 kinematic lift

The retained spacetime side gives an exact kinematic background predicate:

`O_lift = 1[S^3 closed] * 1[d_t = 1]`

That is exact on the current atlas. It selects the clean `PL S^3 x R`
background scaffold.

This is a kinematic statement, not a metric carrier.

### Tensor variational candidate

The scalar generator can be lifted into a tensor-valued quadratic form by
taking its metric-source Hessian on the lifted background:

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`

This is the first exact tensor-valued variational candidate on the direct
route. It is exact as a construction, but not yet identified with
Einstein/Regge dynamics.

### Symmetric quotient kernel

The strongest current identification result is that the Hessian kernel is the
unique symmetric bilinear lift of the scalar generator on the `3+1`
perturbation quotient. On the finite prototype used by the current runner, that
quotient kernel is nondegenerate, so the route has no extra tensor bilinear
freedom hiding in the scalar observable principle.

## What is missing

The direct universal route still lacks the first exact tensor-valued object
that could upgrade the scalar generator into a full `3+1` metric law.

The remaining missing primitive can now be stated more sharply:

1. a curvature-localization map that identifies the unique symmetric `3+1`
   Hessian kernel with the Einstein/Regge tensor law on the full metric space
2. if that fails, one additional primitive that makes that localization exact

Without one of those, the observable principle remains scalar-only at the
closure level and the direct universal route cannot close full GR.

## Why the current route survey points here

The route survey already ranks the observable-principle effective-action route
first, with the discrete `3+1` variational action as the concrete theorem
form.

That remains the right architecture.

What the survey now makes explicit is the failure mode:

- the scalar generator is exact
- the `3+1` kinematic lift is exact
- but the Einstein/Regge identification of the tensor Hessian has not yet been
  made exact

So the universal route is not wrong. It is incomplete at exactly one
localization primitive.

## Minimal missing primitive

The smallest honest missing object is now:

> a curvature-localization map that carries the unique symmetric `3+1`
> Hessian kernel to the Einstein/Regge tensor law on the `PL S^3 x R`
> background

This is the thing that must be derived or axiomatized next.

If that primitive lands, the direct universal route can advance from scalar
observable principle plus `3+1` kinematics to a genuine metric dynamics law.

If it does not, the route remains a clean blocker rather than a closure claim.

## Honest status

The current direct universal route is:

- exact at the scalar observable level
- exact at the `3+1` kinematic lift level
- blocked at the tensor-valued action / uniqueness level

That is the sharpest disciplined statement available on the current atlas.
