# DM Wilson Direct-Descendant Constructive Positive Closure Manifold Support

**Date:** 2026-04-18 (rigorized 2026-05-09 with a Krawczyk-interval certificate)
**Claim type:** bounded_theorem
**Status:** support - regular-root theorem with a Krawczyk-interval certificate at the named base point on the fixed e-independent transport kernel
**Scripts (both registered with caches):**

- `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.py`
  (cache: `logs/runner-cache/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.txt`)
- `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_certificate_2026_04_18.py`
  (cache: `logs/runner-cache/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_certificate_2026_04_18.txt`)

**Certificate:** `outputs/dm_wilson_constructive_positive_closure_manifold_certificate_2026-04-18.json`

## Inputs (cited authorities)

The transport functional `eta_1` and the projected-source kernel used in
the closure constraint `F = eta_1 - 1` are imported from upstream
constructive-transport notes; this note's contribution is the
Krawczyk-interval regular-root certificate, not the underlying transport
construction. The cited authorities are:

- [`DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md)
  — the constructive transport plateau and its `eta_1` functional.
- [`DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md)
  — fiber-spectral completion that fixes the transport kernel surface.
- [`DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md)
  — the same-day multiplicity companion, which records the prior
  numerical evidence of multiple distinct near-closure points.

## Question

After numerical evidence that the constructive positive branch contains
multiple distinct near-closure points, is that just a discrete multiplicity
accident?

Or is the near-closure set actually locally continuous inside the constructive
positive branch?

## Bottom line

The Krawczyk-interval certificate isolates a unique regular zero of the
closure equation in the named bracket on the fixed e-independent transport
kernel.

Near the constructive positive near-closure root

```text
(a,b,c,d,e)
= (1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.887338511710),
```

on the fixed native `N_e` seed surface, the closure constraint

```text
F(a,b,c,d,e) := eta_1(a,b,c,d,e) - 1 = 0
```

is rigorously certified by a Krawczyk-interval regular-root certificate (see
Section "Krawczyk-interval certificate" below):

- F changes sign across an explicit bracket `[e_base - 1e-3, e_base + 1e-3]`,
  with both endpoint magnitudes about `3.4 * 10^-5`, evaluated at 200-bit
  precision so the sign-change is exact at floating-point representation;
- F'(e_base) = 0.034474... computed analytically via the exact
  eigenvector-derivative formula at 200-bit precision;
- F'(I_e) is rigorously enclosed in the interval `[0.0191, 0.0514]` over the
  bracket, with the enclosure obtained by:
  - Davis-Kahan sin-theta theorem applied to the interval Hermitian matrix
    H(I_e) (with rigorous Frobenius perturbation bound `eps_H = 1.55e-4` and
    minimum spectral gap `gap_min = 0.151`),
  - direct interval evaluation of the analytic eigenvector-derivative
    formula `dP_k/de = 2 Re(U[1,k]^* * sum_{j!=k} ((U_j^H dH U_k)/
    (lambda_k - lambda_j)) * U[1,j])`,
  - direct interval evaluation of `psi'(P_k(I_e))` via interval trapezoidal
    quadrature on the precomputed e-independent transport kernel;
- the Krawczyk operator
  `K(I_e) = e_base - F(e_base)/F'(e_base) + (1 - F'(I_e)/F'(e_base))*(I_e - e_base)`
  satisfies `K(I_e) ⊂ interior(I_e)` with contraction factor
  `c = 0.491 < 1` and Newton correction `2.25e-13`. By the Krawczyk
  uniqueness theorem there is a UNIQUE REGULAR ZERO of F in I_e.

This is the standard interval-arithmetic regular-root certificate and gives
exactly the implicit-function-theorem hypothesis the manifold theorem needs at
the base point.

This note treats the precomputed transport kernel
`(z_grid, source_profile, washout_tail)` as the fixed exact numerical object
for which the regular-root statement is being made: the kernel is
e-independent (it comes from a one-off ODE solve at the fixed `k_decay_exact`)
and its numerical error is uniform across all `e` values in the bracket, so
it cannot break the e-dependence-driven Krawczyk contraction.

Under that reading, the remaining hope that

- near-closure,
- constructive sign chamber,
- and positive projected-source branch

might still isolate a point after enough search is materially weakened: the
near-closure set already appears to be locally non-isolated.

## Why this matters

This is the strongest exhaustion-style support packet so far on the
direct-descendant selector route.

The branch no longer just observes that there are "a few" near-closure
constructive positive points. It now observes, with a Krawczyk-interval
regular-root certificate at the base point, behavior consistent with a local
manifold of such points.

So the final selector law, if it exists, must plausibly add at least one
genuinely new independent microscopic equation beyond:

- `eta = eta_obs`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

## Setup

On the fixed native `N_e` seed surface, write

```text
x = (a, b, 3 XBAR_NE - a - b),
y = (c, d, 3 YBAR_NE - c - d),
delta = e.
```

This is a `5`-real parameterization of the exact fixed-mean source surface.

Define:

- `eta_1(a,b,c,d,e)` = favored transport column ratio,
- `F(a,b,c,d,e) = eta_1(a,b,c,d,e) - 1`.

The constructive positive branch is the open region where

- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

## Rigorous-numerics support 1: the near-closure set behaves like a local `4`-real manifold

At the explicit constructive positive base point above, the runner observes:

1. `abs(F(base)) < 10^-10` at floating-point precision and `< 10^-14` at
   200-bit precision; the bracket-endpoint sign change holds exactly at
   floating-point representation;
2. `gamma > 0`, `E1 > 0`, `E2 > 0`, `Delta_src > 0` at every grid point on
   that same bracket;
3. F'(I_e) is rigorously enclosed in `[0.0191, 0.0514]` via Davis-Kahan
   eigenvector perturbation bounds and direct interval evaluation of the
   analytic eigenvector-derivative formula; the Krawczyk contraction
   factor is `0.491 < 1`.

By the Krawczyk uniqueness theorem, F has a unique regular zero of `F` in the
bracket, and an implicit-function-style local family

```text
e = e(a,b,c,d)
```

satisfying

```text
F(a,b,c,d,e(a,b,c,d)) = 0
```

exists on a neighborhood of the base point. Because the constructive positive
inequalities are strict at the base point and continuous, they remain true on
a small enough neighborhood.

The narrowing therefore reads: the near-closure set is locally a `4`-real
manifold inside the constructive positive branch, with the regular-root
hypothesis at the base point now established by a Krawczyk-interval
certificate (rigorous interval arithmetic) rather than a finite-difference
slope estimate.

## Explicit local witness directions

The script verifies this concretely by perturbing each of the four free
coordinates independently and solving back for `e`:

- vary `a` by `±10^{-3}`,
- vary `b` by `±10^{-3}`,
- vary `c` by `±10^{-3}`,
- vary `d` by `±10^{-3}`,

and in each case recover a nearby numerical root with:

- `eta_1 ~ 1` (Brent's method to its tolerance),
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

So the local near-closure family is not just formal. It is numerically
inhabited in four independent coordinate directions.

## Rigorous-numerics support 2: the current projected-source scalar bank varies on that family

Along those nearby numerical closure points, the current scalar/sign data
already change:

- `Delta_src` changes,
- `gamma` changes,
- `E1` changes,
- `E2` changes.

So these quantities are not locally constant on the local near-closure
family.

Therefore:

- none of the currently isolated scalar/sign conditions appears to be
  secretly collapsing the family to a point.

## Corollary 1: constructive positive near-closure appears locally non-isolated

The Krawczyk-interval certificate plus the four-direction witness
perturbations show that constructive positive near-closure points exist on a
positive-dimensional family in a neighborhood of the base root.

So the selector problem remains open even after imposing:

- transport closure,
- positive branch,
- constructive sign chamber.

## Corollary 2: the final selector law plausibly must add a new independent local condition

If the final microscopic selector law exists, the rigorous-numerics evidence
indicates it must cut a positive-dimensional family down further.

So it plausibly must contribute at least one genuinely new independent local
condition on the full right-sensitive projected-source data.

## Krawczyk-interval certificate

The companion runner

```text
scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_certificate_2026_04_18.py
```

emits the certificate to

```text
outputs/dm_wilson_constructive_positive_closure_manifold_certificate_2026-04-18.json
```

with the following recorded fields:

- `bracket.e_lo`, `bracket.e_hi`: the explicit `[e_base - 10^-3, e_base +
  10^-3]` interval;
- `bracket.F_lo`, `bracket.F_hi`: the signed values of `F` at the bracket
  endpoints, evaluated at 200-bit precision;
- `bracket.sign_change_margin`: about `3.4 * 10^-5`, ~7 orders of magnitude
  above the floating-point noise floor `1e-12`;
- `analytic_F_prime_at_midpoint.F_prime_mid`: about `0.0344742478`, computed
  analytically via the exact eigenvector derivative formula;
- `interval_H_bounds_over_bracket.frob_norm_H_perturbation_eps_H`: about
  `1.55 * 10^-4`, the rigorous Frobenius bound on `||H(I_e) - H(e_mid)||`;
- `interval_H_bounds_over_bracket.gap_min`: about `0.151`, the minimum
  spectral gap (with `2*eps_H << gap_min` so Davis-Kahan applies);
- `davis_kahan_eigenvector_deviation_bounds.DK_bounds_per_k`: rigorous bounds
  on the eigenvector deviation across the bracket per eigenvector;
- `interval_F_prime_over_bracket.F_prime_lo`, `F_prime_hi`: rigorous
  enclosure `[0.0191, 0.0514]` of F'(I_e) over the bracket;
- `krawczyk_operator.contraction_factor`: about `0.491` (`< 1` so contraction
  applies);
- `krawczyk_operator.K_image_half_width_upper_bound`: about `4.91 * 10^-4`
  (`< r = 10^-3` so K(I_e) is strictly contained in the bracket interior);
- `kernel_data_provenance`: documents the e-independent precomputed transport
  kernel and the precision of the Krawczyk arithmetic.

The verdict line in the cache reads:

> Krawczyk-interval test passes: the operator K(I_e) is strictly contained
> in the interior of I_e, with contraction factor < 1, and F'(I_e) is
> uniformly bounded away from zero. By the Krawczyk uniqueness theorem this
> certifies a unique regular zero of F in I_e.

## What this supports

- the near-closure set is plausibly not just a discrete multiplicity
  accident
- the route "maybe constructive positive closure becomes unique locally"
  appears unlikely under the Krawczyk-interval regular-root certificate
- the idea that branch sign plus closure plus constructive triplet signs is
  almost enough is materially weakened

## What this does not establish

- a rigorous interval enclosure of the underlying ODE pipeline that produces
  the e-independent transport kernel itself (the certificate treats the
  precomputed kernel as the fixed exact numerical object on which the
  regular-root statement is being made)
- a Krawczyk certificate at every nearby perturbed root (only at the named
  base point)
- a finer microscopic law that actually cuts the local family to a point
- the final DM flagship closeout
