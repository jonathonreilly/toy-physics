# DM Wilson Direct-Descendant Constructive Positive Closure Manifold Theorem

**Date:** 2026-04-18  
**Status:** exact local manifold theorem on the constructive positive exact
closure set  
**Script:** `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_2026_04_18.py`

## Question

After proving that the constructive positive branch contains multiple distinct
exact closure points, is that just a discrete multiplicity accident?

Or is the exact closure set actually locally continuous inside the constructive
positive branch?

## Bottom line

It is locally continuous.

Near the constructive positive exact closure root

```text
(a,b,c,d,e)
= (1.16845863, 0.46803892, 0.77107315, 0.05539671, 1.887338511710),
```

on the fixed native `N_e` seed surface, the closure constraint

```text
F(a,b,c,d,e) := eta_1(a,b,c,d,e) - 1 = 0
```

is regular:

```text
∂F/∂e ≠ 0.
```

Therefore, by the implicit-function form of the exact continuity argument,
there is a local `4`-real family of exact closure points inside the
constructive positive branch.

So the current exact closure set is not merely non-unique. It is locally a
positive-dimensional manifold.

This kills the whole remaining hope that:

- exact closure,
- constructive sign chamber,
- and positive projected-source branch

might still isolate a point after enough search.

They do not isolate a point even locally.

## Why this matters

This is the strongest exhaustion theorem so far on the direct-descendant
selector route.

The branch no longer just knows that there are "a few" exact constructive
positive closure points.

It now knows that near a regular root there is a whole local manifold of them.

So the final selector law, if it exists, must add at least one genuinely new
independent microscopic equation beyond:

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

## Theorem 1: the exact constructive positive closure set is locally a `4`-real manifold

At the explicit exact constructive positive root above:

1. `F = 0`,
2. `gamma > 0`, `E1 > 0`, `E2 > 0`, `Delta_src > 0`,
3. the phase derivative is nonzero:

   `∂F/∂e = 0.034474247845...`.

Therefore there is a neighborhood in the `4` free variables `(a,b,c,d)` and an
exact local function

```text
e = e(a,b,c,d)
```

such that

```text
F(a,b,c,d,e(a,b,c,d)) = 0
```

throughout that neighborhood.

Because the constructive positive inequalities are strict at the base point and
depend continuously on the same data, they remain true on a sufficiently small
neighborhood of that local solution manifold.

So the exact constructive positive closure set is locally a `4`-real manifold.

## Explicit local witness directions

The script verifies this concretely by perturbing each of the four free
coordinates independently and solving back for `e`:

- vary `a` by `±10^{-3}`,
- vary `b` by `±10^{-3}`,
- vary `c` by `±10^{-3}`,
- vary `d` by `±10^{-3}`,

and in each case recover an exact nearby root with:

- `eta_1 = 1`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

So the local exact-closure family is not just formal. It is numerically
inhabited in four independent coordinate directions.

## Theorem 2: the current projected-source scalar bank varies on that manifold

Along those nearby exact closure points, the current scalar/sign data already
change:

- `Delta_src` changes,
- `gamma` changes,
- `E1` changes,
- `E2` changes.

So these quantities are not locally constant on the exact constructive
positive-closure manifold.

Therefore:

- none of the currently isolated scalar/sign conditions is already secretly
  collapsing the manifold to a point.

## Corollary 1: exact constructive positive closure is locally non-isolated

There are infinitely many exact constructive positive closure points in a
neighborhood of the base root.

So the selector problem remains open even after imposing:

- exact transport closure,
- positive branch,
- constructive sign chamber.

## Corollary 2: the final selector law must add a new independent local condition

The final microscopic selector law, if it exists, must cut a
positive-dimensional manifold down further.

So it must contribute at least one genuinely new independent local condition on
the full right-sensitive projected-source data.

## What this closes

- the possibility that multiplicity was only a discrete accident
- the whole route "maybe exact constructive positive closure becomes unique
  locally"
- the idea that branch sign plus closure plus constructive triplet signs is
  almost enough

## What this does not close

- a finer microscopic law that actually cuts the local manifold to a point
- the final DM flagship closeout
