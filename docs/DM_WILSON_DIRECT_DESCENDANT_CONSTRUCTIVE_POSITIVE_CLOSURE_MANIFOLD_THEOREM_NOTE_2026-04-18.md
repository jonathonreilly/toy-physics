# DM Wilson Direct-Descendant Constructive Positive Closure Manifold Support

**Date:** 2026-04-18 (narrowed 2026-05-08 in response to runner-artifact audit)
**Claim type:** bounded_theorem
**Status:** support - validated-numerics evidence for a local non-isolated branch; not an exact regular-root theorem
**Scripts:**

- `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.py`
- `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_certificate_2026_04_18.py`

**Certificate:** `outputs/dm_wilson_constructive_positive_closure_manifold_certificate_2026-04-18.json`

## Question

After numerical evidence that the constructive positive branch contains
multiple distinct near-closure points, is that just a discrete multiplicity
accident?

Or is the near-closure set actually locally continuous inside the constructive
positive branch?

## Bottom line

The validated-numerics evidence is consistent with local continuity.

Near the constructive positive near-closure root

```text
(a,b,c,d,e)
= (1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.887338511710),
```

on the fixed native `N_e` seed surface, the closure constraint

```text
F(a,b,c,d,e) := eta_1(a,b,c,d,e) - 1 = 0
```

passes a validated-numerics regular-root certificate (see Section
"Validated-numerics certificate" below):

- F changes sign across an explicit bracket `[e_base - 1e-3, e_base + 1e-3]`,
  with both endpoint magnitudes about `3.4 * 10^-5`, i.e. roughly `7` orders of
  magnitude above the floating-point noise floor of the underlying
  transport-functional evaluation;
- a `21`-point discrete-slope estimate of `dF/de` over that same bracket is
  uniformly bounded away from zero, with min discrete slope about `0.034447`
  and max about `0.034501`;
- central-difference `dF/de` at multiple step sizes `h in {1e-3, 1e-4, 1e-5,
  1e-6, 1e-7}` agrees to better than `5 * 10^-9`, which is consistent with a
  regular derivative.

This validated-numerics certificate plays the role the implicit-function
theorem would play if `F` were known to be exactly differentiable at a
certified exact zero. Under the standard validated-numerics "sign-change +
uniform-slope-lower-bound" reading, this gives strong support that the
near-closure set is locally a positive-dimensional family inside the
constructive positive branch.

This note does **not** claim the exact regular-root theorem. The underlying
`F` evaluation involves an ODE solver and a numerical transport-functional
integral, neither of which is currently equipped with a rigorous interval or
analytic enclosure on this seed surface. So the strict honest reading is:

> validated-numerics evidence for a nearby non-isolated constructive positive
> near-closure branch, not a retained exact regular-root theorem.

Under that validated-numerics reading, the remaining hope that

- near-closure,
- constructive sign chamber,
- and positive projected-source branch

might still isolate a point after enough search is materially weakened: the
near-closure set already appears to be locally non-isolated.

## Why this matters

This is the strongest exhaustion-style support packet so far on the
direct-descendant selector route.

The branch no longer just observes that there are "a few" near-closure
constructive positive points. It now observes, with a validated-numerics
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

## Validated-numerics support 1: the near-closure set behaves like a local `4`-real manifold

At the explicit constructive positive base point above, the runner observes:

1. `abs(F(base)) < 10^-10` at floating-point precision, and a validated
   sign-change of `F` across an explicit `e` bracket of half-width `10^-3`;
2. `gamma > 0`, `E1 > 0`, `E2 > 0`, `Delta_src > 0` at every grid point on
   that same bracket;
3. the phase-direction discrete slope is uniformly bounded away from zero
   on that bracket:

   `min discrete slope on [e_base - 10^-3, e_base + 10^-3] = 0.034447...`,
   `max discrete slope on [e_base - 10^-3, e_base + 10^-3] = 0.034501...`,
   central-difference `dF/de = 0.034474247845...` is step-stable to `~5e-9`.

Under the validated-numerics "sign-change + uniform-slope-lower-bound"
reading, this is consistent with a regular root of `F` in the bracket and an
implicit-function-style local family

```text
e = e(a,b,c,d)
```

with

```text
F(a,b,c,d,e(a,b,c,d)) ~ 0
```

on a neighborhood. Because the constructive positive inequalities are strict
at the base point and continuous, they remain true on a small enough
neighborhood.

The honest narrowing therefore reads: the near-closure set behaves
empirically like a local `4`-real manifold inside the constructive positive
branch. This is validated-numerics support, not an exact regular-root
theorem.

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

## Validated-numerics support 2: the current projected-source scalar bank varies on that family

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

The validated-numerics evidence suggests there are infinitely many
constructive positive near-closure points in a neighborhood of the base
root.

So the selector problem remains open even after imposing:

- transport closure,
- positive branch,
- constructive sign chamber.

## Corollary 2: the final selector law plausibly must add a new independent local condition

If the final microscopic selector law exists, the validated-numerics evidence
indicates it must cut a positive-dimensional family down further.

So it plausibly must contribute at least one genuinely new independent local
condition on the full right-sensitive projected-source data.

## Validated-numerics certificate

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
  endpoints, with `F_lo ~ -3.45 * 10^-5` and `F_hi ~ +3.45 * 10^-5`;
- `bracket.sign_change_margin`: about `3.4 * 10^-5`, i.e. ~7 orders of
  magnitude above the floating-point noise floor `1e-12`;
- `uniform_slope_lower_bound.grid_min_discrete_slope`: about `0.034447`;
- `uniform_slope_lower_bound.grid_max_discrete_slope`: about `0.034501`;
- `central_fd_step_stability.span`: about `5 * 10^-9` over `h in {1e-3 ... 1e-7}`;
- `constructive_positive_branch_on_bracket`: minimum values of
  `(gamma, E1, E2, Delta_src)` over the entire bracket grid, all strictly
  positive.

The verdict line in the cache reads:

> F changes sign on the bracket and its discrete slope is uniformly bounded
> away from zero on the same bracket, so a regular root of F exists in the
> bracket. This is the validated-numerics version of the regular-root
> hypothesis used by the manifold theorem.

## What this supports

- the near-closure set is plausibly not just a discrete multiplicity
  accident
- the route "maybe constructive positive closure becomes unique locally"
  appears unlikely under validated numerics
- the idea that branch sign plus closure plus constructive triplet signs is
  almost enough is materially weakened

## What this does not establish

- a rigorous interval enclosure of the underlying ODE/transport pipeline
- a fully validated-numerics regular-root certificate at every nearby
  perturbed root (only at the base point)
- an analytic/symbolic regular-root theorem
- a finer microscopic law that actually cuts the local family to a point
- the final DM flagship closeout
