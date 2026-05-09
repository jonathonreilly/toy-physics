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

- explicit `beta = 6` Perron moments or Jacobi coefficients
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Companion: explicit `rho_(p,q)(6)` Wilson coefficients now computed

The companion runner
`scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py`
computes the canonical residual-environment character coefficients

`rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))`,
`c_(p,q)(6) = int_{SU(3)} chi_(p,q)(U) exp((6/3) Re tr U) dU`,

via two independent integrators:

- the Schur-Weyl Bessel-determinant identity (closed form), and
- direct Weyl integration on the SU(3) Cartan torus with Vandermonde squared.

The two integrators agree to ~`1e-14` absolute on the `(p+q) <= 4` weight set.
The runner then verifies that the residual environment operator
`R_6^env chi_(p,q) = rho_(p,q)(6) chi_(p,q)` reproduces the identification of
this note, and that the factorized framework-point law
`exp(3 J) D_6^loc R_6^env exp(3 J)` remains self-adjoint, conjugation-symmetric,
and Perron-positive when the previous witness injection is replaced by the
computed Wilson coefficients. See the companion-runner section below for the
tabulated coefficient values.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`

### Companion computation: explicit `rho_(p,q)(6)` from Wilson environment data

The previous runner above checks the structural class (positive, self-adjoint,
central, diagonal, conjugation-symmetric) of the residual environment operator
`R_6^env` against a generic positive conjugation-symmetric diagonal witness
sequence `rho_env(p,q)`. The audited renaming verdict for this row recorded
that the load-bearing step under that runner was an identification, not a
derivation, because the explicit Wilson environment coefficients
`rho_(p,q)(6)` were not computed.

The companion runner

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
```

evaluates the canonical normalized boundary character coefficients

`rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))`,

`c_(p,q)(6) = int_{SU(3)} chi_(p,q)(U) exp((6/3) Re tr U) dU`,

two independent ways:

- **Method A (Schur-Weyl Bessel-determinant identity, closed form):** the
  integer-mode Schur-Weyl reduction expresses the SU(3) character integral as
  a sum of `3 x 3` determinants of modified Bessel functions
  `I_{m + lambda_j + i - j}(beta/3)`, summed over the integer shift `m in Z`,
  truncated at `|m| <= 80` for absolute convergence at `beta = 6`.

- **Method B (Weyl integration formula on the Cartan torus, direct quadrature):**
  the same integral computed by the Weyl integration formula
  `int_{SU(3)} f dU = (1/|W|)(1/(2 pi)^2) int_{T^2} f(theta) |Delta(theta)|^2 d^2 theta`
  with `|W| = 6`, `chi_(p,q)(theta)` evaluated by the Weyl character formula
  on the maximal torus, and `|Delta(theta)|^2` the SU(3) Vandermonde squared.

Reported computed coefficients at `beta = 6` (closed form, twelve digits):

- `rho_(0,0)(6) = 1.000000000000`
- `rho_(1,0)(6) = rho_(0,1)(6) = 4.225317396500e-01`
- `rho_(1,1)(6) = 1.622597994799e-01`
- `rho_(2,0)(6) = rho_(0,2)(6) = 1.359617273634e-01`
- `rho_(2,1)(6) = rho_(1,2)(6) = 4.828805556745e-02`
- `rho_(3,0)(6) = rho_(0,3)(6) = 3.505738045167e-02`
- `rho_(2,2)(6) = 1.350507888830e-02`

Method A and Method B agree to `~4e-15` absolute and `~8e-14` relative on the
`(p+q) <= 4` weight set. The companion runner then verifies that
`R_6^env chi_(p,q) = rho_(p,q)(6) chi_(p,q)` with these computed values, and
that the factorized framework-point law
`exp(3 J) D_6^loc R_6^env exp(3 J)` retains the self-adjoint /
conjugation-symmetric / Perron-positive structural gates that the previous
witness-injection runner required.

Expected summary for the companion runner:

- `THEOREM PASS=7 SUPPORT=3 FAIL=0`
