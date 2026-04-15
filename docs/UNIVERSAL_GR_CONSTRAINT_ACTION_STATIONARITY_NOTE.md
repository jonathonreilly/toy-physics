# Universal GR Constraint / Action-Stationarity Test on `PL S^3 x R`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / constraint-style bypass test  
**Purpose:** test whether an action-stationarity or constraint-style theorem
can bypass the complement-frame selection problem on the exact universal
`A1`-anchored quotient-kernel route

## Verdict

The direct universal route does **not** gain a canonical curvature-localization
section from action stationarity alone.

The strongest constraint-style bypass candidate is still the exact
`A1`-anchored quadratic candidate built from the universal tensor Hessian,
together with the exact invariant section:

`S_constraint^cand[h] := 1/2 * D^2 W[g_*](Pi_A1 h, Pi_A1 h)`.

Here:

- `W[J] = log|det(D+J)| - log|det D|` is the exact scalar observable
  generator;
- `Pi_A1` is the exact rank-2 invariant projector onto lapse and spatial
  trace;
- `g_*` is the exact `PL S^3 x R` lifted background source.

This candidate is exact as a construction, and it is lambda-free by the same
reason the direct universal bypass route was lambda-free: it never invokes the
phase-lift mixing family.

But the constraint/stationarity audit shows that this candidate is orbit-flat
on the valid `3+1` polarization-frame orbit. The complement coefficients move,
but the action-like invariants do not pick a unique section.

So the direct universal route bypasses the phase-lift `lambda` obstruction,
but not the complement-frame ambiguity.

## What is exact already

### Scalar generator

The axiom-side observable principle gives the scalar generator

`W[J] = log|det(D+J)| - log|det D|`.

That part is exact.

### `3+1` lift

Route 2 gives the exact kinematic background

`PL S^3 x R`.

That part is exact.

### Tensor variational candidate

The scalar generator lifts to the tensor-valued quadratic form

`S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`.

That is exact as a construction.

### Exact invariant selector

The strongest exact projector latent in the current universal stack is the
rank-2 `A1` projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

It selects lapse and spatial trace exactly.

### Exact orbit family

The complementary `E \oplus T1` channels still form an `SO(3)` orbit bundle
over the valid `3+1` frames. The orbit is exact, but the current stack does
not supply a distinguished connection or canonical section.

## What the constraint test checks

The runner audits a fixed universal test tensor across several valid spatial
frame rotations and checks:

1. the `A1` core is frame-invariant;
2. the total quadratic action on the response coefficients is orbit-flat;
3. the complement coefficients still move under valid frame rotations;
4. the complement norm is still orbit-flat, so minimizing a norm-like
   constraint cannot choose a unique section;
5. the residual obstruction is therefore the same complement-frame ambiguity
   already recorded in the universal blocker notes.

## Strongest concrete bypass candidate

The strongest candidate on the direct universal route is still the exact
`A1`-anchored action/quotient-kernel object.

But the audit shows:

> action stationarity and constraint-style minimization do not break the
> `SO(3)` complement-frame gauge.

That means the best candidate is a bypass of `lambda`, not a bypass of the
final complement-frame problem.

## Honest conclusion

The direct universal route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- lambda-free in the `A1`-anchored action candidate;
- still blocked at the complement-frame / curvature-localization level.

So the answer to the question is negative:

> constraint-style stationarity does not canonically select the complement
> frame; the universal route still collapses onto the same `SO(3)` orbit
> ambiguity on the `E \oplus T1` channels.
