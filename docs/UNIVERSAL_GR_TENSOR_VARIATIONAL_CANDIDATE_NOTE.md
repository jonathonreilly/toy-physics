# Universal GR Tensor Variational Candidate on `PL S^3 x R`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / theorem step  
**Purpose:** identify the first exact tensor-valued `3+1` variational candidate
from the axiom-side observable principle and the exact `3+1` kinematic lift

## Verdict

The direct universal route is still not closed, but it now has a concrete
tensor-valued variational candidate and a sharper quotient-uniqueness
statement on the current `3+1` perturbation space.

The exact scalar observable principle gives the generator

`W[J] = log|det(D+J)| - log|det D|`

and Route 2 gives the exact `3+1` kinematic background

`PL S^3 x R`.

The first exact tensor-valued variational candidate on that lifted background
is the metric-source Hessian of `W` at the lifted background point.

In other words, if `g_*` denotes the exact lifted background metric source and
`h_{ab}` a symmetric `3+1` metric perturbation, then the candidate quadratic
form is

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`.

This is the first direct-universal object that is:

- tensor-valued
- variational by construction
- grounded in the exact scalar observable principle
- defined on the exact `3+1` background scaffold

## Why this is the right next object

The current blocker was not a missing scalar generator and not a missing
`3+1` lift.

The missing object was the first exact tensor-valued variational object that
could sit on top of both.

The Hessian is the minimal exact lift of the scalar generator into tensor
source space:

`B(h, k) := D^2 W[g_*](h, k)`

with

`B(h, k) = B(k, h)`.

So the direct universal route now has a precise candidate action family rather
than just a generic blocker.

## Exact structure of the candidate

On the current lifted background, the candidate behaves as:

1. scalar generator exact: `W[J]` is the unique additive scalar observable
   generator on the axiom-side Grassmann surface
2. `3+1` lift exact: `PL S^3 x R` is the background scaffold
3. tensor candidate exact as a construction: the second variation of `W`
   is a symmetric bilinear form on `3+1` metric sources

This is enough to define a legitimate tensor-valued variational candidate.

It is **not** yet enough to prove that the candidate equals the Einstein/Regge
action on the full metric space.

## Strongest exact identification result

The current route now gives more than a bare candidate:

1. the candidate is the exact second variation of the scalar observable
   generator on the lifted background;
2. on the symmetric `3+1` perturbation quotient, the Hessian is the unique
   bilinear lift of the scalar generator at quadratic order;
3. on the finite `3+1` prototype used by the current runner, the symmetric
   quotient kernel is nondegenerate, so there are no extra null directions
   hiding a second tensor degree of freedom.

That is the strongest honest identification currently available on the atlas.
It pins down the tensor kernel itself. It does **not** yet identify that kernel
with Einstein/Regge curvature dynamics.

## What remains open

The remaining theorem is now sharply localized:

1. identify the unique symmetric `3+1` Hessian kernel with the local
   Einstein/Regge tensor law, or
2. derive an exact tensor-valued uniqueness theorem forcing that
   identification, or
3. prove the candidate cannot be promoted without a new curvature-localization
   primitive

So the direct universal route is now one step more concrete:

> scalar observable principle + exact `3+1` lift + exact tensor-valued
> variational candidate + unique symmetric `3+1` quotient kernel

but it is still not a full closure theorem.

## Honest status

The current direct-universal theorem step is:

- exact scalar observable generator in hand
- exact `3+1` kinematic lift in hand
- exact tensor-valued variational candidate in hand
- exact symmetric `3+1` quotient kernel in hand
- exact Einstein/Regge identification still missing

That is the cleanest statement available on the current atlas.
