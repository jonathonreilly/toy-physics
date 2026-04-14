# `S^3` + Anomaly-Forced Time: Kinetic Lift Candidate

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Purpose:** bounded kinetic/time law candidate on `PL S^3 x R` derived from
the exact static-constraint lift and the exact Schur boundary action

## Verdict

**The route has a clean bounded kinetic-lift candidate, but not an exact GR
dynamics theorem.**

The current retained stack already gives:

- exact `S^3` spatial closure
- exact anomaly-forced time with a single clock, `d_t = 1`
- exact shell-to-`3+1` static-constraint lift on the current bridge surface
- exact microscopic Schur-complement boundary action on the same source
  classes

Taken together, those ingredients canonically induce a one-step boundary
evolution operator on the route-2 slice space:

- exact slice generator: `Lambda_R`
- bounded kinetic lift: `T_R = exp(-Lambda_R)`

That is the cleanest kinetic/time law the current atlas supports without
introducing a new dynamical postulate.

## Exact inputs already available

### `S^3` compactification

[`S3_GENERAL_R_DERIVATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
already gives the retained spatial background candidate:

- the cone-capped cubical ball is PL homeomorphic to `S^3` for all `R >= 2`

### Anomaly-forced time

[`ANOMALY_FORCES_TIME_THEOREM.md`](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)
already gives the retained temporal background candidate:

- anomaly cancellation plus chirality plus the one-clock Cauchy requirement
  force `d_t = 1`

So the clean kinematic background remains:

- `PL S^3 x R`

### Exact static shell-to-`3+1` lift

[`OH_STATIC_CONSTRAINT_LIFT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_STATIC_CONSTRAINT_LIFT_NOTE.md)
already closes the static bridge on the current source class:

- exact shell source on the sewing band
- unique same-charge bridge
- exact local static conformal constraints

### Exact microscopic boundary action

[`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
already gives the exact microscopic shell-boundary action:

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

with `Lambda_R` the exact Schur-complement Dirichlet-to-Neumann matrix.

## Kinetic lift candidate

With `d_t = 1`, the natural one-step Euclidean transfer operator on the
boundary trace space is

- `T_R := exp(-Lambda_R)`

with one-slice generator

- `H_R := Lambda_R`.

This is the precise kinetic/time law candidate obtained by lifting the exact
static shell action into the anomaly-forced time direction.

Why this is the right bounded candidate:

1. `Lambda_R` is exact on the current bridge surface.
2. `Lambda_R` is symmetric positive definite on the audited source classes.
3. `exp(-Lambda_R)` is therefore a positive self-adjoint contraction.
4. The anomaly theorem fixes the clock direction, so the step size is not an
   ad hoc extra parameter.

So Route 2 does yield a canonical discrete kinetic law:

> exact spatial slice + exact one-clock time + exact boundary Hamiltonian
> => bounded slice transfer operator on `PL S^3 x R`

## What this closes

This closes the kinetic-lift ambiguity on the current route surface:

> the exact static shell lift and exact Schur boundary action induce a
> canonical bounded transfer-matrix law on `PL S^3 x R`

That is stronger than the previous purely kinematic background statement,
because the route now has a real time-step generator.

## What this still does not close

This note still does **not** close:

1. a full pointwise Einstein/Regge theorem beyond the current static conformal
   bridge
2. an exact lapse/shift or curvature law on `PL S^3 x R`
3. a unique metric law forced by the retained stack alone

## Sharp blocker

The atlas still lacks an exact theorem that turns the exact slice generator
`Lambda_R` into a full dynamics bridge:

> there is no exact derivation of the Einstein metric law from the retained
> `PL S^3 x R` slice generator alone

Equivalently:

- the retained stack gives the exact slice Hamiltonian
- it does not yet give the exact time-coupling / curvature law that makes the
  bridge theorem-grade

## Runnable summary

The companion runner checks:

- `S^3` topology is exact
- anomaly-forced time is exact
- the exact static shell lift is closed on the current restricted class
- the Schur boundary generator is symmetric positive definite
- the induced transfer operator `T_R = exp(-Lambda_R)` is a positive
  contraction on the current bridge surface
- the atlas still does not contain an exact GR dynamics bridge

## Bottom line

Route 2 now has a clean bounded kinetic-lift candidate:

- exact background: `PL S^3 x R`
- exact slice generator: `Lambda_R`
- exact one-step transfer operator: `T_R = exp(-Lambda_R)`

That is a real kinetic/time law on the current strong-field class, but it is
still not an exact GR closure theorem.
