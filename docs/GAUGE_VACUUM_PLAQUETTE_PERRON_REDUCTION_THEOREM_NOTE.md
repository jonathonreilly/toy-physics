# Gauge-Vacuum Plaquette Perron-State Reduction Theorem

**Date:** 2026-04-16
**Status:** exact transfer-state reduction theorem on the finite Wilson `3 spatial + 1 derived-time`
source surface; explicit Perron / Jacobi data at `beta = 6` still open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py`

## Question

After making the plaquette generating object explicit at the operator level, can
the remaining `beta = 6` state-identification problem be reduced exactly to a
smaller object?

## Answer

Yes.

On every finite Wilson `L_s^3 x L_t` source surface with `beta > 0`, the exact
one-clock transfer operator `T_(L_s,beta)` has a strictly positive symmetric
kernel on the compact gauge-invariant spatial configuration space.

Therefore:

- `T_(L_s,beta)` is compact and self-adjoint,
- `T_(L_s,beta)` is positivity-improving,
- its spectral radius `lambda_0(L_s,beta)` is simple,
- there is one unique normalized strictly positive Perron vector
  `psi_0(L_s,beta)`.

For every bounded Borel function `f` of the local plaquette source operator
`J`, the exact transfer-state law satisfies

`lim_(L_t -> infty) Tr[T_(L_s,beta)^(L_t) f(J)] / Tr[T_(L_s,beta)^(L_t)]
 = <psi_0(L_s,beta), f(J) psi_0(L_s,beta)>`.

So the framework-point plaquette problem is no longer:

- identify an abstract spectral measure,
- or identify a full thermal trace state.

It is now exactly:

> identify the Perron vector `psi_0(L_s,6)`, equivalently the Jacobi data of the
> explicit plaquette source operator `J` in that Perron state.

That is the right reduced target.

## Setup

From the exact transfer-operator / character-recurrence theorem already on
`main`:

- the finite Wilson partition function factors as
  `Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]`,
- `T_(L_s,beta)` is a positive self-adjoint one-clock transfer operator,
- the local plaquette source is the explicit self-adjoint class-function
  operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`
  on the source-cyclic class-function subspace.

So the only remaining state data lives in the positive transfer state induced by
`T_(L_s,beta)`.

## Theorem 1: exact Perron reduction of the transfer state

For `beta > 0`, the kernel of `T_(L_s,beta)` is pointwise strictly positive.
Because the spatial configuration space is compact and the kernel is continuous,
`T_(L_s,beta)` is Hilbert-Schmidt and therefore compact.

By symmetry of the kernel, `T_(L_s,beta)` is self-adjoint.

By positivity improvement and the compact self-adjoint Perron-Jentzsch theorem:

- the spectral radius `lambda_0(L_s,beta)` is an eigenvalue,
- that eigenvalue is simple,
- the corresponding normalized eigenvector `psi_0(L_s,beta)` can be chosen
  strictly positive and is then unique up to sign.

So there is one exact Perron state for the finite Wilson transfer problem.

## Corollary 1: exact zero-temperature / large-derived-time reduction

Let

`rho_(L_s,L_t,beta)(f)
 = Tr[T_(L_s,beta)^(L_t) f(J)] / Tr[T_(L_s,beta)^(L_t)]`.

Using the spectral decomposition of `T_(L_s,beta)` and simplicity of
`lambda_0`, one gets

`rho_(L_s,L_t,beta)(f) -> <psi_0(L_s,beta), f(J) psi_0(L_s,beta)>`

as `L_t -> infty` for every bounded Borel `f`.

Therefore the transfer-state identification problem reduces exactly to the
Perron vector.

## Theorem 2: exact symmetry reduction of the Perron state

Any unitary symmetry `S` that commutes with `T_(L_s,beta)` must preserve the
one-dimensional Perron eigenspace.

Hence

`S psi_0(L_s,beta) = c_S psi_0(L_s,beta)`

for some phase `c_S`.

But `psi_0(L_s,beta)` is strictly positive and `S` preserves positivity, so
`c_S = 1`.

Therefore the Perron state is exactly invariant under every positivity-preserving
symmetry commuting with the transfer operator, including the class-function
conjugation symmetry on the plaquette source sector.

So the remaining unknown is not a generic vector in the full Hilbert space. It
already lies in the positive symmetry-reduced sector.

## Corollary 2: exact Jacobi-data reduction

Let `mu_(L_s,beta)^P` be the spectral measure of `J` in the Perron vector:

`mu_(L_s,beta)^P(B) = <psi_0(L_s,beta), E_J(B) psi_0(L_s,beta)>`.

Then

`<psi_0(L_s,beta), J^n psi_0(L_s,beta)>
 = integral x^n dmu_(L_s,beta)^P(x)`

for all `n >= 0`.

By the spectral theorem and orthogonal-polynomial construction, this measure is
equivalent to one unique Jacobi operator on the source-cyclic subspace generated
by `psi_0` under repeated application of `J`.

So explicit framework-point plaquette closure is now equivalent to explicit
framework-point Jacobi data:

- diagonal coefficients `a_n(6)`,
- off-diagonal coefficients `b_n(6)`,
- or equivalently the Perron moments of `J`.

## What this closes

- exact reduction of the transfer-state problem to one unique strictly positive
  Perron vector on each finite Wilson `3+1` source surface
- exact large-derived-time reduction from thermal trace state to Perron state
- exact symmetry reduction of that Perron state on the source sector
- exact reformulation of the remaining `beta = 6` problem as Perron / Jacobi
  data for the explicit operator `J`

## What this does not close

- explicit construction of `psi_0(L_s,6)`
- explicit Jacobi coefficients at `beta = 6`
- explicit infinite-volume control in `L_s`
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=3 FAIL=0`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

The conditional verdict flagged a missing cited retained dependency for the exact transfer-operator / character-recurrence theorem proving strict positivity of `T_(L_s,beta)`. That authority is supplied by:

- [gauge_vacuum_plaquette_transfer_operator_character_recurrence_note](GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md)
