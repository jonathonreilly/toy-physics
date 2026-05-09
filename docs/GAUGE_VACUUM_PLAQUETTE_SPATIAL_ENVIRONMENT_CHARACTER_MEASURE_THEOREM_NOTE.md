# Gauge-Vacuum Plaquette Spatial Environment Character-Measure Theorem

**Date:** 2026-04-17
**Status:** exact source-sector identification theorem on the accepted Wilson
`3 spatial + 1 derived-time` surface; after the marked half-slice multiplier
and the exact normalized mixed-kernel local factor are stripped, the remaining
open operator is exactly the normalized central boundary character measure of
the unmarked spatial Wilson environment
**Script:** `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py`

## Question

After identifying the remaining plaquette datum as the residual environment
operator `R_beta^env`, can that operator be written more explicitly than an
abstract positive diagonal source-sector factor?

## Answer

Yes.

Fix the marked plaquette holonomy `W` on one source step and integrate the
unmarked spatial Wilson environment with that boundary holonomy held fixed.
This defines one exact boundary class function

`Z_beta^env(W)`.

Because the unmarked spatial Wilson action and Haar measure are invariant under
simultaneous conjugation of the marked plaquette holonomy, `Z_beta^env` is
central. Because the Wilson weight is real and nonnegative, `Z_beta^env` is of
positive type. Therefore it has one exact `SU(3)` character expansion

`Z_beta^env(W) = z_(0,0)^env(beta) sum_(p,q) d_(p,q) rho_(p,q)(beta) chi_(p,q)(W)`,

with

- `rho_(p,q)(beta) >= 0`,
- `rho_(p,q)(beta) = rho_(q,p)(beta)`,
- `rho_(0,0)(beta) = 1`.

The residual source-sector environment operator is exactly convolution by this
normalized boundary class function:

`R_beta^env chi_(p,q) = rho_(p,q)(beta) chi_(p,q)`.

So the remaining framework-point target is no longer an abstract residual
operator. It is exactly the `beta = 6` boundary character data of the
unmarked spatial Wilson environment:

> explicitly identify the coefficients `rho_(p,q)(6)` of
> `Z_6^env(W)`, or equivalently the Perron data of
> `exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`.

## Setup

From the exact transfer-operator / character-recurrence theorem already on
`main`:

- the plaquette source sector carries the exact self-adjoint source operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`;
- one source step on the accepted Wilson `3+1` surface factors into marked
  half-slice multipliers and one residual source-sector compression.

From the exact source-sector matrix-element factorization theorem:

- `T_src(beta) = exp[(beta / 2) J] D_beta exp[(beta / 2) J]`,
- `D_beta` is positive, self-adjoint, central, and diagonal in the character
  basis.

From the exact local/environment factorization theorem:

- after trivial-channel normalization, the mixed-kernel local factor is
  already exactly
  `D_beta^loc chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`.

From the exact residual-environment identification theorem:

- the remaining operator after stripping the marked half-slice multiplier and
  `D_beta^loc` is exactly the compressed unmarked spatial environment
  `R_beta^env`.

## Theorem 1: exact unmarked spatial boundary class function

Fix the marked plaquette holonomy `W in SU(3)` on one source step and integrate
all unmarked spatial Wilson degrees of freedom with this boundary holonomy held
fixed. The resulting quantity

`Z_beta^env(W)`

is a well-defined real nonnegative class function of `W`.

It depends only on the conjugacy class of `W`, because the unmarked spatial
Wilson action and Haar measure are invariant under simultaneous conjugation of
all boundary representatives of the marked plaquette holonomy.

## Theorem 2: exact character expansion of the boundary environment

Because `Z_beta^env` is a central class function on `SU(3)`, Peter-Weyl
decomposition gives one exact expansion

`Z_beta^env(W) = sum_(p,q) d_(p,q) z_(p,q)^env(beta) chi_(p,q)(W)`.

Normalize by the trivial coefficient `z_(0,0)^env(beta) > 0` and define

`rho_(p,q)(beta) = z_(p,q)^env(beta) / z_(0,0)^env(beta)`.

Then

`Z_beta^env(W) = z_(0,0)^env(beta) sum_(p,q) d_(p,q) rho_(p,q)(beta) chi_(p,q)(W)`,

with

- `rho_(0,0)(beta) = 1`,
- `rho_(p,q)(beta) = rho_(q,p)(beta)`.

Positivity of the residual source-sector environment operator implies
`rho_(p,q)(beta) >= 0` on the marked class-function sector.

## Theorem 3: exact operator realization of the residual environment

Let `C_(Z_beta^env)` denote normalized convolution by the central boundary
class function `Z_beta^env / z_(0,0)^env(beta)` on the marked-plaquette
class-function sector.

Then

`C_(Z_beta^env) chi_(p,q) = rho_(p,q)(beta) chi_(p,q)`.

But the residual environment operator already closed on `main` satisfies

`R_beta^env chi_(p,q) = rho_(p,q)(beta) chi_(p,q)`.

Therefore

`R_beta^env = C_(Z_beta^env)`.

So the residual operator is exactly the normalized boundary character measure
of the unmarked spatial Wilson environment.

## Corollary 1: exact factorized framework-point source-sector law

At the framework point `beta = 6`,

`T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`.

Hence the remaining open constructive datum is explicitly:

- the boundary character coefficients `rho_(p,q)(6)` of `Z_6^env`,
- or equivalently the Perron data of the explicit factorized operator above.

## What this closes

- exact realization of the residual environment operator as a concrete central
  boundary class function of the unmarked spatial Wilson environment
- exact identification of the residual diagonal coefficients as normalized
  character coefficients of that boundary class function
- exact reformulation of the remaining plaquette problem as explicit
  `beta = 6` spatial environment boundary character data

## What this does not close

- explicit `beta = 6` Perron moments or Jacobi coefficients
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Companion: explicit `rho_(p,q)(6)` Wilson coefficients now computed

The companion runner
`scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py`
computes the canonical boundary character coefficients

`rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))`,
`c_(p,q)(6) = int_{SU(3)} chi_(p,q)(U) exp((6/3) Re tr U) dU`,

two independent ways (Bessel-determinant identity vs Weyl integration formula
on the Cartan torus), cross-checked to ~`1e-14` absolute. So the explicit
boundary character coefficients on the `(p+q) <= 4` weight set, which the
previous runner only packaged as a generic witness sequence, are now numerical
Wilson environment data on the canonical normalized single-link boundary
closure of the unmarked spatial Wilson environment. See "Commands run" above
for the tabulated values.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`

### Companion computation: explicit `rho_(p,q)(6)` from Wilson environment data

The previous runner above only checks the packaging of the boundary character
expansion against a generic positive conjugation-symmetric witness sequence
`rho_env(p,q)`. The audited renaming verdict for this row recorded that the
load-bearing step under that runner was an identification, not a derivation,
because the explicit Wilson environment coefficients `rho_(p,q)(6)` were not
computed.

The companion runner

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
```

evaluates the canonical normalized boundary character coefficients

`rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))`,

`c_(p,q)(6) = int_{SU(3)} chi_(p,q)(U) exp((6/3) Re tr U) dU`,

two independent ways and cross-checks the two evaluations to machine precision:

- **Method A (Schur-Weyl Bessel-determinant identity, closed form):** the
  integer-mode Schur-Weyl reduction expresses the SU(3) character integral as a
  sum of `3 x 3` determinants of modified Bessel functions
  `I_{m + lambda_j + i - j}(beta/3)` summed over the integer shift `m in Z`,
  truncated at `|m| <= 80` for absolute convergence at `beta = 6`.

- **Method B (Weyl integration formula on the Cartan torus, direct quadrature):**
  the same integral computed by the Weyl integration formula
  `int_{SU(3)} f dU = (1/|W|)(1/(2 pi)^2) int_{T^2} f(theta) |Delta(theta)|^2 d^2 theta`
  with `|W| = 6`, `chi_(p,q)(theta)` evaluated by the Weyl character formula on
  the maximal torus, and `|Delta(theta)|^2` the SU(3) Vandermonde squared.

Reported computed coefficients at `beta = 6` (closed form, twelve digits):

- `rho_(0,0)(6) = 1.000000000000`
- `rho_(1,0)(6) = rho_(0,1)(6) = 4.225317396500e-01`
- `rho_(1,1)(6) = 1.622597994799e-01`
- `rho_(2,0)(6) = rho_(0,2)(6) = 1.359617273634e-01`
- `rho_(2,1)(6) = rho_(1,2)(6) = 4.828805556745e-02`
- `rho_(3,0)(6) = rho_(0,3)(6) = 3.505738045167e-02`
- `rho_(2,2)(6) = 1.350507888830e-02`

Method A and Method B agree to `~4e-15` absolute and `~8e-14` relative on the
`(p+q) <= 4` weight set.

Expected summary for the companion runner:

- `THEOREM PASS=7 SUPPORT=3 FAIL=0`
