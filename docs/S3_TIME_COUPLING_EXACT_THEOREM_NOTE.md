# Exact Time-Coupling Law on `PL S^3 x R`: Blocker and Required Primitive

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** Final-law committee, Route 2 / time-coupling pass  
**Scope:** start from the exact slice generator `Lambda_R` and the bounded
transfer bridge `T_R = exp(-Lambda_R)`; determine whether Route 2 upgrades to
an exact time-coupling theorem on `PL S^3 x R`

## Verdict

**The retained stack does not yet supply an exact time-coupling law.**

What it does supply is a clean bounded transfer-matrix bridge:

- exact `S^3` spatial closure
- exact anomaly-forced time with a single clock, `d_t = 1`
- exact microscopic Schur-complement boundary action on the current strong-field class
- exact slice generator `Lambda_R`
- bounded one-step transfer operator `T_R = exp(-Lambda_R)`

That is enough to define a real slice evolution on the current bridge surface,
but it is still only a bounded discrete-time transfer law. It is not yet an
exact theorem-grade dynamics bridge to the GR metric law.

## Atlas support

The derivation atlas already certifies the ingredients Route 2 needs:

- [Anomaly-forced time](/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md) is an exact zero-input structural tool
- [S^3 boundary-link closure](/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md) and [S^3 cap uniqueness](/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md) are reusable topology tools
- [Restricted strong-field closure synthesis](/Users/jonreilly/Projects/Physics/docs/publication/ci3_z3/DERIVATION_ATLAS.md) gives the exact Schur boundary action on the strong-field class

The atlas does **not** contain a row that turns those exact kinematic tools
into an exact `PL S^3 x R` dynamics law.

## Exact ingredients already available

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

### Exact boundary Hamiltonian

[`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
already gives the exact microscopic boundary action on the current strong-field
class:

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

with `Lambda_R` the exact Schur-complement Dirichlet-to-Neumann matrix.

The companion Dirichlet principle note shows that the shell trace is the unique
minimum of that exact boundary energy on the current strong-field class.

## What `Lambda_R` and `T_R` do

With `d_t = 1`, the natural one-step Euclidean transfer operator on the
boundary-trace space is:

- `T_R := exp(-Lambda_R)`

and the associated one-slice quadratic generator is:

- `H_R := Lambda_R`

That is the cleanest bounded route-2 bridge the retained stack supports.

It is mathematically consistent because:

1. `Lambda_R` is exact on the current bridge surface.
2. `Lambda_R` is symmetric positive definite on the audited source classes.
3. `exp(-Lambda_R)` is therefore a positive self-adjoint contraction.
4. The anomaly theorem supplies the unique clock direction, so the step size
   is fixed by the route-2 background rather than by an extra ad hoc time
   choice.

So Route 2 does yield a real bounded transfer-matrix bridge:

> exact spatial slice + exact one-clock time + exact boundary Hamiltonian
> `=>` bounded slice transfer operator on `PL S^3 x R`

## Why this still does not close GR

The key point is that `Lambda_R` is a **static** slice Hamiltonian. It does
not, by itself, determine an exact time-coupling law or an Einstein/Regge
metric action.

The current atlas still lacks an exact theorem that upgrades the slice
generator into a full dynamics bridge:

> there is no exact derivation of the Einstein metric law from the retained
> `PL S^3 x R` slice generator alone

Equivalently:

- the retained stack gives the exact slice Hamiltonian
- it does not yet give the exact time-coupling / curvature law that makes the
  bridge theorem-grade

## Exact additional primitive still required

The additional primitive needed to close Route 2 is not another transfer
matrix. It is one exact dynamics carrier on `PL S^3 x R`, namely one of:

1. an exact `PL S^3 x R` action whose Euler-Lagrange equations reproduce the
   GR metric law
2. an exact spacetime-lift observable that reconstructs metric response
3. a uniqueness theorem forcing Einstein dynamics as the only compatible lift

In the atlas language, the missing object is:

> a theorem-grade time-coupling primitive that is exact on `PL S^3 x R`
> and carries the metric/curvature response, not merely the static shell
> boundary energy.

## Runnable summary

The companion runner checks:

- `S^3` topology is exact
- anomaly-forced time is exact
- the Schur boundary generator is symmetric positive definite
- the induced transfer operator `T_R = exp(-Lambda_R)` is a positive
  contraction on the current bridge surface
- the atlas still does not contain an exact `PL S^3 x R` dynamics bridge

So the exact time-coupling law is not yet derivable from the current retained
stack. The exact extra primitive required is a new route-2 dynamics carrier.

## Bottom line

Route 2 has:

- exact background: `PL S^3 x R`
- exact generator: `Lambda_R`
- exact one-step transfer operator: `T_R = exp(-Lambda_R)`

But it still does **not** have:

- an exact time-coupling law
- an exact dynamics bridge
- an exact GR closure theorem

That is the sharp blocker.
