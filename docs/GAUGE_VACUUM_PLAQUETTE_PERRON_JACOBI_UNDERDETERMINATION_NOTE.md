# Gauge-Vacuum Plaquette Perron/Jacobi Underdetermination

**Date:** 2026-04-17
**Status:** exact obstruction theorem inside the now-explicit factorized
source-sector transfer class; explicit `beta = 6` Perron / Jacobi data still not forced
**Script:** `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py`

## Question

Do the exact plaquette theorems now on `main` already force the symmetry-reduced
Jacobi coefficients, or equivalently the Perron moments of the explicit source
operator `J`, at the framework point `beta = 6`?

## Answer

No.

The live stack now closes:

- the explicit source operator `J`,
- the exact transfer-operator / character-recurrence realization,
- the exact Perron-state reduction,
- the conjugation-symmetry reduction of the Perron state,
- and the exact source-sector matrix-element factorization law
  `T_src(6) = exp(3 J) D_6 exp(3 J)`.

But those facts do **not** yet determine the explicit `beta = 6` Perron moments
or Jacobi coefficients.

Even inside the new exact factorized class, distinct positive
conjugation-symmetric diagonal coefficient sequences `D_6` can still induce
different Perron moments and therefore different Jacobi data for the same
explicit source operator `J`.

So the current exact stack still does **not** force the explicit framework-point
Jacobi coefficients.

## Setup

Let `J` be the explicit self-adjoint plaquette source operator on the
source-cyclic class-function sector already closed in the transfer-operator /
character-recurrence theorem.

Let `S` be the exact conjugation-symmetry involution `(p,q) <-> (q,p)` on the
dominant-weight basis.

From the exact source-sector matrix-element factorization theorem already on
`main`, every admissible `beta = 6` source-sector transfer operator has the
form

`T_src(6) = M D_6 M`,

with

`M = exp(3 J)`,

with:

- `M = M^* > 0`,
- `D_6` diagonal in the character basis,
- `D_6 > 0`,
- `S D_6 = D_6 S`.

Every such `T` satisfies the same structural boundary now closed on `main`:

- positivity-improving,
- one simple strictly positive Perron state,
- Perron-state symmetry reduction under `S`.

## Theorem 1: the current exact factorized class does not determine a unique diagonal coefficient sequence

Choose two distinct positive conjugation-symmetric diagonal coefficient
sequences

`D_A != D_B`

on the same explicit source sector.

Then

`T_A = M D_A M`,
`T_B = M D_B M`

are both positivity-improving self-adjoint transfer operators with unique
strictly positive Perron states `psi_A`, `psi_B`.

Both lie inside the current exact factorized source-sector boundary already
closed on `main`.

## Theorem 2: distinct admissible diagonal coefficient sequences can induce distinct Perron moments for the same source operator

For the same explicit plaquette source operator `J`, define the Perron moments

`m_n^(A) = <psi_A, J^n psi_A>`,
`m_n^(B) = <psi_B, J^n psi_B>`.

Because `psi_A` and `psi_B` need not coincide, these moment sequences need not
coincide either.

The runner exhibits two explicit admissible positive diagonal coefficient
sequences with

`m_1^(A) != m_1^(B)`

and higher moments differing as well.

Therefore the current exact plaquette operator stack does **not** determine a
unique Perron moment sequence at `beta = 6`.

## Corollary 1: the symmetry-reduced Jacobi coefficients are not yet forced

By the spectral theorem and orthogonal-polynomial construction, the Jacobi
coefficients are uniquely determined by the Perron moments of `J`.

So if two admissible transfer generators on the current structural boundary
produce different Perron moments, they also produce different Jacobi data.

Therefore:

> the current exact plaquette operator stack does not yet force the explicit
> symmetry-reduced Jacobi coefficients at `beta = 6`.

## What this closes

- exact proof that explicit source-operator realization plus Perron reduction
  still do **not** force a unique framework-point Perron measure
- exact proof that symmetry-reduced Jacobi coefficients are still open on the
  current stack
- exact clarification of what new theorem object is actually needed next:
  the explicit `beta = 6` transfer generator / matrix elements on the
  source-cyclic factorized operator, or an equivalent exact Perron
  eigenvector construction

## What this does not close

- explicit Jacobi coefficients at `beta = 6`
- explicit Perron moments at `beta = 6`
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`
