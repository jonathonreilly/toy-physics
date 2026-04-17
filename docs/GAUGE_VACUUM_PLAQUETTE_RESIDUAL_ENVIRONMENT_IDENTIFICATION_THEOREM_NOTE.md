# Gauge-Vacuum Plaquette Residual Environment Identification Theorem

**Date:** 2026-04-17
**Status:** exact source-sector identification theorem on the accepted Wilson
`3 spatial + 1 derived-time` surface; after the marked half-slice multiplier
and the exact normalized mixed-kernel local factor are stripped, the remaining
open object is exactly the compressed unmarked spatial environment operator on
the marked-plaquette class-function sector
**Script:** `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py`

## Question

Once the marked half-slice factor and the normalized mixed-kernel local factor
are both explicit, is the remaining plaquette object still just an abstract
positive diagonal datum, or can its exact origin be identified more sharply?

## Answer

It can be identified more sharply.

The exact transfer/source-sector factorization theorem already closes

`T_src(beta) = exp[(beta / 2) J] D_beta exp[(beta / 2) J]`.

The exact local/environment factorization theorem already closes that the
normalized mixed-kernel part is exactly the local Wilson four-link factor

`D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`.

Therefore the still-open factor is not hidden mixed-kernel freedom. It is
exactly the residual source-sector operator obtained by compressing the
unmarked spatial Wilson environment to the marked-plaquette class-function
sector after the local mixed-kernel factor is removed.

So the remaining target may be written explicitly as

`T_src(beta) = exp[(beta / 2) J] D_beta^loc R_beta^env exp[(beta / 2) J]`,

where `R_beta^env` is the compressed unmarked spatial environment operator.

At `beta = 6`, the remaining constructive problem is therefore:

> explicitly identify the character coefficients or Perron data of
> `R_6^env`, not the whole source-sector transfer law and not the already-fixed
> mixed-kernel local factor.

## Setup

From the exact transfer-operator / character-recurrence theorem already on
`main`:

- the plaquette source sector carries the exact self-adjoint source operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`;
- the one-clock Wilson transfer law is positive and self-adjoint on the
  accepted source sector.

From the exact source-sector matrix-element factorization theorem:

- the exact marked half-slice multiplier is `exp[(beta / 2) J]`;
- after stripping those two marked half-slice multipliers, the residual
  source-sector compression is central and diagonal in the character basis.

From the exact local/environment factorization theorem:

- in temporal gauge, the mixed one-step Wilson kernel factorizes over the
  spatial links;
- after trivial-channel normalization, every non-marked mixed-link factor acts
  only by the identity on the marked class-function sector;
- the full normalized mixed-kernel compression is therefore exactly the local
  Wilson four-link factor `D_beta^loc`.

## Theorem 1: exact residual factor after local mixed-kernel stripping

Let `K_beta^src` denote the exact one-step Wilson source-sector kernel on the
marked-plaquette class-function sector.

Strip off:

1. the incoming marked half-slice multiplier `exp[(beta / 2) J]`,
2. the outgoing marked half-slice multiplier `exp[(beta / 2) J]`,
3. the exact normalized mixed-kernel local factor `D_beta^loc`.

What remains is exactly the compression of the unmarked spatial Wilson
environment on the marked source sector. Call this operator `R_beta^env`.

Then:

`K_beta^src = exp[(beta / 2) J] D_beta^loc R_beta^env exp[(beta / 2) J]`.

So the open operator is identified exactly as the residual unmarked spatial
environment compression.

## Theorem 2: exact structural class of the residual environment operator

Because the unmarked spatial Wilson environment is real, positive, and
invariant under simultaneous conjugation of the marked plaquette holonomy,
`R_beta^env` is:

- positive,
- self-adjoint,
- central on the marked-plaquette class-function sector,
- diagonal in the `SU(3)` character basis,
- conjugation-symmetric under `(p,q) <-> (q,p)`.

Therefore

`R_beta^env chi_(p,q) = rho_(p,q)(beta) chi_(p,q)`,

with

- `rho_(p,q)(beta) >= 0`,
- `rho_(p,q)(beta) = rho_(q,p)(beta)`.

## Corollary 1: the remaining plaquette target is no longer abstract

The remaining framework-point target is no longer:

- the full source-sector transfer operator,
- the mixed-kernel coefficient stack,
- the marked half-slice multiplier,
- or the local Wilson four-link factor.

It is exactly:

- the compressed unmarked spatial environment operator `R_6^env`,
- equivalently its character coefficients `rho_(p,q)(6)`,
- or equivalently the Perron state / moments of
  `exp(3 J) D_6^loc R_6^env exp(3 J)`.

## What this closes

- exact identification of the still-open plaquette operator as the compressed
  unmarked spatial environment operator
- exact separation between the already-fixed normalized mixed-kernel local
  factor and the still-open environment factor
- exact reformulation of the remaining plaquette problem as explicit
  environment compression data at `beta = 6`

## What this does not close

- explicit coefficients `rho_(p,q)(6)` of the residual environment operator
- explicit `beta = 6` Perron moments or Jacobi coefficients
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`
