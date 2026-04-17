# Gauge-Vacuum Plaquette Source-Sector Matrix-Element Factorization Theorem

**Date:** 2026-04-17
**Status:** exact source-sector factorization theorem on the finite Wilson `3 spatial + 1 derived-time` source surface; the exact diagonal mixed-kernel character coefficients at `beta = 6` are now locally factored, but the residual environment-response sequence still remains open
**Script:** `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py`

## Question

Can the previously open `beta = 6` source-sector transfer generator / matrix
elements be written explicitly on the accepted Wilson `3+1` source surface?

## Answer

Yes, at the factorized source-sector level.

Let `J` be the exact plaquette source operator already closed on `main`,

`J = (chi_(1,0) + chi_(0,1)) / 6`,

acting on the marked-plaquette class-function sector.

Then the exact `beta = 6` source-sector transfer operator has the factorized
form

`T_src(6) = exp(3 J) D_6 exp(3 J)`,

where:

- `exp(3 J)` is the exact half-slice spatial plaquette multiplier on the marked
  plaquette,
- `D_6` is the exact positive self-adjoint diagonal operator of the compressed
  mixed-plaquette kernel in the `SU(3)` character basis:
  `D_6 chi_(p,q) = kappa_(p,q)(6) chi_(p,q)`.

So the source-sector matrix elements are now explicit:

`(T_src(6))_(lambda,mu)
 = sum_nu (exp(3 J))_(lambda,nu) kappa_nu(6) (exp(3 J))_(nu,mu)`.

This closes the previously open “explicit source-sector matrix element” step.

What remains open is narrower:

> identify the residual environment-response sequence inside
> `kappa_(p,q)(6) = a_(p,q)(6)^4 epsilon_(p,q)(6)`,
> after the exact local Wilson marked-link factor `a_(p,q)(6)^4` is removed,
> and therefore the exact Perron state of this now-explicit factorized
> operator.

## Setup

From the exact transfer-operator / character-recurrence theorem already on
`main`:

- the finite Wilson partition function factors as one exact positive
  self-adjoint one-clock transfer operator,
- the local marked plaquette source is exactly the class function
  `X = (chi_(1,0) + chi_(0,1)) / 6`,
- multiplication by `X` closes exactly on the `SU(3)` dominant-weight graph.

From the exact Perron-state reduction theorem already on `main`:

- the large-derived-time state on every finite Wilson `3+1` source surface
  reduces exactly to the Perron state of that transfer operator.

So the only missing constructive object was the source-sector matrix-element
law for the transfer operator itself.

## Theorem 1: exact half-slice marked-plaquette multiplier

On one time step, the marked spatial plaquette enters the Wilson kernel with
half weight on the incoming slice and half weight on the outgoing slice:

`exp[(beta / 6) Re Tr W] = exp[(beta / 2) X(W)]`.

Since `J` is exactly multiplication by `X`, the marked half-slice factor on the
source sector is exactly

`M_(beta/2) = exp[(beta / 2) J]`.

At the framework point `beta = 6`,

`M_3 = exp(3 J)`.

## Theorem 2: exact mixed-kernel compression is central and diagonal in characters

Strip off the two exact marked half-slice multipliers from the one-clock Wilson
kernel and compress the remaining mixed-plaquette part to the marked-plaquette
class-function sector. Call the resulting operator `C_beta`.

Because the Wilson mixed-plaquette weight is real, positive, and invariant
under simultaneous conjugation of the marked plaquette holonomies, `C_beta` is:

- positive,
- self-adjoint,
- central on the marked-plaquette class-function sector.

By the Peter-Weyl / character decomposition of central operators on class
functions, `C_beta` is diagonal in the irreducible character basis:

`C_beta chi_(p,q) = kappa_(p,q)(beta) chi_(p,q)`,

with real nonnegative coefficients `kappa_(p,q)(beta)`.

Conjugation symmetry gives

`kappa_(p,q)(beta) = kappa_(q,p)(beta)`.

## Corollary 1: exact source-sector matrix elements

Combining the exact marked half-slice multipliers and the exact diagonal
mixed-kernel compression,

`T_src(beta) = exp[(beta / 2) J] D_beta exp[(beta / 2) J]`,

where `D_beta chi_(p,q) = kappa_(p,q)(beta) chi_(p,q)`.

Therefore at `beta = 6`,

`T_src(6) = exp(3 J) D_6 exp(3 J)`,

and in the dominant-weight character basis,

`(T_src(6))_(lambda,mu)
 = sum_nu (exp(3 J))_(lambda,nu) kappa_nu(6) (exp(3 J))_(nu,mu)`.

So the exact source-sector transfer matrix elements are now explicit.

## Corollary 2: exact remaining constructive datum

The remaining plaquette operator problem is no longer:

- an arbitrary positive transfer generator on the source sector,
- an arbitrary positive Perron/Jacobi realization,
- or a generic abstract source-sector matrix element problem.

It is now exactly:

- the positive diagonal coefficient sequence `kappa_(p,q)(6)`,
- or equivalently the Perron state of `exp(3 J) D_6 exp(3 J)`.

The new local/environment factorization theorem on `main` sharpens that one
step further:

- the exact four marked-link Wilson contribution is explicit:
  `kappa_(p,q)(6) = a_(p,q)(6)^4 epsilon_(p,q)(6)`;
- so the remaining open object is the residual environment-response sequence
  `epsilon_(p,q)(6)`, not the whole mixed-kernel coefficient stack.

That is the sharply reduced constructive target.

## What this closes

- exact `beta = 6` half-slice multiplier on the marked plaquette:
  `exp(3 J)`
- exact source-sector factorization of the Wilson transfer operator
- exact source-sector matrix-element formula at `beta = 6`
- exact narrowing of the remaining constructive datum to one positive diagonal
  character-coefficient sequence `kappa_(p,q)(6)`

## What this does not close

- explicit values of the residual environment-response coefficients
  `epsilon_(p,q)(6)`
- explicit `beta = 6` Perron moments or Jacobi coefficients
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`
