# Gauge-Vacuum Plaquette Residual Environment Identification Theorem

**Date:** 2026-04-17 (residual-env structural identification);
2026-05-16 (witness replaced by computed Wilson coefficients on finite box)
**Status:** structural source-sector identification theorem on the accepted
Wilson `3 spatial + 1 derived-time` surface; after the marked half-slice
multiplier and the exact normalized mixed-kernel local factor are stripped,
the remaining factor is structurally a positive central diagonal
conjugation-symmetric operator R_beta^env on the marked-plaquette
class-function sector. The runner now derives the finite-box residual
coefficients rho_(p,q)(6) directly from the canonical single-link SU(3)
Wilson character integral by the Schur-Weyl Bessel-determinant identity,
rather than injecting a witness sequence, on the finite 0<=p,q<=NMAX box.
**Claim type:** open_gate (all-weight equality of the stripped residual with
the unmarked spatial Wilson environment compression is *not* closed)
**Script:** `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py`
**Bounded coefficient companion:**
[`GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md`](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md)
**Prior audit:** `audited_conditional` at fresh_context (codex-gpt-5.5); the
auditor flagged that the runner verified algebraic properties for a generic
positive symmetric witness rather than computing the actual residual
environment. The runner has been updated to compute rho_(p,q)(6) from the
canonical Wilson character integral on the finite box, so the structural
identification at this scope is now paired with a derivation, not a witness
injection. The all-weight equality remains the open gate.

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

- the all-weight or full tensor-transfer coefficients of the actual unmarked
  spatial Wilson environment; the companion note computes only a bounded
  finite single-link Wilson boundary table
- explicit `beta = 6` Perron moments or Jacobi coefficients
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Bounded companion: finite `rho_(p,q)(6)` Wilson coefficients

The companion note
[`GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md`](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md)
and runner
`scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py`
compute bounded normalized single-link Wilson boundary coefficients

`rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))`,
`c_(p,q)(6) = int_{SU(3)} chi_(p,q)(U) exp((6/3) Re tr U) dU`,

via two independent integrators:

- the Schur-Weyl Bessel-determinant identity, and
- direct Weyl integration on the SU(3) Cartan torus with Vandermonde squared.

The two integrators agree to ~`1e-14` absolute on the finite `0 <= p,q <= 4`
box. The runner then verifies diagonal action when these computed coefficients
are inserted,
`R_6^env chi_(p,q) = rho_(p,q)(6) chi_(p,q)`, and checks that the factorized
framework-point witness
`exp(3 J) D_6^loc R_6^env exp(3 J)` remains self-adjoint, conjugation-symmetric,
and Perron-positive on the finite truncation.

This is bounded support for replacing the prior arbitrary witness on the
computed finite box. It does not by itself close the parent residual-environment
gate or promote this note.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py
```

Expected summary after the 2026-05-16 update (witness replaced by computed
finite-box Wilson coefficients):

- `THEOREM PASS=6 SUPPORT=3 FAIL=0`

The new theorem-grade checks now include:

- the residual coefficients `rho_(p,q)(6)` come from the canonical normalized
  single-link Wilson character integral, computed by the Schur-Weyl
  Bessel-determinant identity in-runner, not from a hand-picked witness;
- `rho_(0,0)(6) = 1` exactly (normalization) and the computed sequence
  differs from the retired witness sequence by `~4.2e-1` in max norm, so the
  runner certifies that the previous witness has actually been replaced;
- `R_6^env chi_(p,q) = rho_(p,q)(6) chi_(p,q)` with the computed values
  (eigen-action error `0.0` on the finite box);
- the factorized framework-point law `exp(3 J) D_6^loc R_6^env exp(3 J)` is
  self-adjoint, conjugation-symmetric, and positivity-improving on the
  truncated source sector with the computed `rho_env`.

## Scope and what remains open

This update closes the *witness-injection* defect on the finite computed
box, but does **not** promote the parent claim to retained-grade. In
particular it does not derive:

- that the stripped residual factor equals the compressed unmarked spatial
  Wilson environment operator on *all* dominant weights (the all-weight
  equality remains the open gate);
- the full unmarked spatial Wilson environment tensor-transfer / Perron
  closure;
- analytic `P(6)`.

The residual factor's *structural* class (positive, self-adjoint, central,
diagonal in the SU(3) character basis, conjugation-symmetric) follows from
the cited source-sector and local/environment factorization notes; the
*numerical* finite-box coefficients are now computed from the canonical
Wilson character integral directly. The all-weight identification of those
two objects (stripped residual vs. unmarked spatial environment compression)
is the precise step the parent gate still needs.

### Companion computation: bounded `rho_(p,q)(6)` from single-link Wilson data

The runner above now computes `rho_(p,q)(6)` directly from the canonical
single-link SU(3) Wilson character integral via the Schur-Weyl
Bessel-determinant identity, replacing the previously injected witness
sequence on the finite computed box.

For independent cross-verification of those same coefficients by a
different integrator (Weyl integration on the Cartan torus with
Vandermonde-squared measure), the bounded companion note and runner

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
```

evaluate the canonical normalized single-link boundary character coefficients

`rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))`,

`c_(p,q)(6) = int_{SU(3)} chi_(p,q)(U) exp((6/3) Re tr U) dU`,

two independent ways on the finite `0 <= p,q <= 4` box:

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
finite box. The companion runner then verifies that
`R_6^env chi_(p,q) = rho_(p,q)(6) chi_(p,q)` with these computed values, and
that the factorized framework-point law
`exp(3 J) D_6^loc R_6^env exp(3 J)` retains the self-adjoint /
conjugation-symmetric / Perron-positive structural gates that the previous
witness-injection runner required.

The all-weight coefficient law and full unmarked spatial environment
tensor-transfer/Perron closure remain outside this bounded companion.

Expected summary for the companion runner:

- `THEOREM PASS=7 SUPPORT=3 FAIL=0`
