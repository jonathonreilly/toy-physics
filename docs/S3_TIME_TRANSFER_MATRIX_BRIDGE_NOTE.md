# `S^3` + Anomaly-Forced Time: Transfer-Matrix Bridge Candidate

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Purpose:** bounded transfer-matrix / discrete-action bridge from the retained `S^3` + anomaly-forced-time stack to slice dynamics on `PL S^3 x R`

## Verdict

**The route has a clean bounded bridge candidate, but not an exact GR dynamics theorem.**

The current retained stack already supplies:

- exact `S^3` spatial closure
- exact anomaly-forced time with a single clock, `d_t = 1`
- exact microscopic Schur-complement boundary action on the current strong-field class

Those ingredients are enough to define a natural slice transfer generator on
the `PL S^3 x R` background:

- the spatial slice is exact
- the clock step is exact
- the slice Hamiltonian is exact on the current bridge surface

What is still missing is the theorem that identifies that slice generator
with the full Einstein/Regge metric dynamics.

## Exact ingredients already available

### `S^3` compactification

[`S3_GENERAL_R_DERIVATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
already gives the retained spatial background candidate:

- the cone-capped cubical ball is PL homeomorphic to `S^3` for all `R >= 2`

### Anomaly-forced time

[`ANOMALY_FORCES_TIME_THEOREM.md`](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)
already gives the retained temporal background candidate:

- anomaly cancellation plus chirality plus the one-clock Cauchy requirement force `d_t = 1`

So the clean kinematic background remains:

- `PL S^3 x R`

### Exact boundary Hamiltonian

[`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
already gives the exact microscopic boundary action on the current strong-field class:

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

with `Lambda_R` the exact Schur-complement Dirichlet-to-Neumann matrix.

The companion Dirichlet principle note shows that the shell trace is the unique
minimum of that exact boundary energy on the current strong-field class.

## Clean bounded bridge candidate

If `d_t = 1` is the exact clock step, the natural one-step Euclidean transfer
operator on the boundary-trace space is

- `T_R := exp(-Lambda_R)`

with the associated one-slice quadratic generator

- `H_R := Lambda_R`.

This is the cleanest slice-to-slice candidate the retained stack supports
without inventing a new dynamical postulate.

Why it is the right bounded candidate:

1. `Lambda_R` is exact on the current bridge surface.
2. `Lambda_R` is symmetric positive definite on the audited source classes.
3. `exp(-Lambda_R)` is therefore a positive self-adjoint contraction.
4. The anomaly theorem supplies the unique clock direction, so the step
   size is fixed by the route-2 background rather than by an extra ad hoc
   time choice.

So Route 2 does yield a well-defined discrete transfer-matrix bridge:

> exact spatial slice + exact one-clock time + exact boundary Hamiltonian
>  => bounded slice transfer operator on `PL S^3 x R`

## What this bridge does

The transfer matrix candidate is strong enough to say:

- the route has a canonical slice evolution operator
- the exact shell action can be propagated slice-by-slice
- the current `PL S^3 x R` background is not just a kinematic label; it
  supports a real transfer operator on the current strong-field class

That is enough to make Route 2 a genuine discrete-action bridge candidate,
not just a background theorem.

## What this bridge does not do

This candidate still does **not** prove:

1. a full pointwise Einstein/Regge dynamics theorem
2. an exact lapse/shift or kinetic term on `PL S^3 x R`
3. a unique metric law forced by the retained stack alone

So the bridge is bounded, not closed.

## Sharp blocker

The atlas still lacks an exact theorem that turns the exact slice generator
`Lambda_R` into a full dynamics bridge:

> there is no exact derivation of the Einstein metric law from the retained
> `PL S^3 x R` slice generator alone

Equivalently:

- the retained stack gives the exact slice Hamiltonian
- it does not yet give the exact time-coupling / curvature law that makes
  the bridge theorem-grade

## Runnable summary

The companion runner checks:

- `S^3` topology is exact
- anomaly-forced time is exact
- the Schur boundary generator is symmetric positive definite
- the induced transfer operator `T_R = exp(-Lambda_R)` is a positive
  contraction on the current bridge surface
- the atlas still does not contain an exact GR dynamics bridge

## Bottom line

Route 2 now has a clean bounded transfer-matrix bridge candidate:

- exact background: `PL S^3 x R`
- exact generator: `Lambda_R`
- exact one-step transfer operator: `T_R = exp(-Lambda_R)`

That is a real discrete-action bridge on the current strong-field class, but
it is still not an exact GR closure theorem.
