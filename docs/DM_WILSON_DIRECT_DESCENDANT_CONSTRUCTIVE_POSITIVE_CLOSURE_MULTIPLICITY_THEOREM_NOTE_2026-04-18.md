# DM Wilson Direct-Descendant Constructive Positive Closure Multiplicity Theorem

**Date:** 2026-04-18  
**Status:** exact multiplicity theorem on the constructive positive branch of
the PMNS-assisted DM route  
**Script:** `scripts/frontier_dm_wilson_direct_descendant_constructive_positive_closure_multiplicity_theorem_2026_04_18.py`

## Question

After proving that:

- the constructive sign chamber is nonempty,
- the constructive chamber contains an exact `eta / eta_obs = 1` point,
- the positive projected-source branch `Delta_src > 0` is compatible with that
  exact closure point,

is the exact closure point at least unique inside the constructive positive
branch?

Or do multiple distinct exact closure points already exist there?

## Bottom line

Multiple distinct exact closure points already exist.

On the fixed native `N_e` seed surface there are at least **three distinct**
one-parameter constructive positive witness families on which the favored
transport column crosses exact closure.

Therefore the constructive positive branch already contains at least three
distinct exact points with all of:

- `eta / eta_obs = 1`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

So not only is

- `Delta_src > 0` plus constructive triplet signs

insufficient as a selector. Even

- exact closure `eta = eta_obs`,
- plus the constructive sign chamber,
- plus the positive projected-source branch

is still not enough to choose a unique physical point.

This exhausts the whole "constructive positive closure by itself might already
select the point" direction.

## Why this matters

This is the sharpest exhaustion result on the current constructive route.

The branch can no longer hope that the remaining selector law is simply:

- “choose the positive constructive branch,”
- or “choose the exact `eta = 1` point inside that branch.”

That object is still non-unique.

So the final retained selector law, if it exists, must be finer than:

- branch sign,
- constructive triplet signs,
- and exact transport closure.

## What is already exact

### 1. The constructive chamber contains an exact closure point

From
[DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md](./DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md):

- there exists an exact constructive point with `eta_1 = 1`,
- and with `gamma > 0`, `E1 > 0`, `E2 > 0`.

### 2. The current conditional branch rule is an explicit projected-source scalar

From
[DM_WILSON_DIRECT_DESCENDANT_PROJECTED_SOURCE_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_DIRECT_DESCENDANT_PROJECTED_SOURCE_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-18.md):

- `Delta_src(dW_e^H) = det(H_e)`,
- so the positive branch is `Delta_src > 0`.

### 3. Positive branch plus constructive signs is not already a point selector

From
[DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md):

- the exact closure point lies on `Delta_src > 0`,
- but nearby points on the same positive constructive branch already have
  different transport values.

This left one remaining loophole:

- perhaps exact closure itself becomes unique once the positive constructive
  branch is imposed.

The present theorem closes that loophole negatively.

## Theorem 1: the constructive positive branch contains at least three distinct exact closure points

Fix the native-seed means

- `xbar = XBAR_NE`,
- `ybar = YBAR_NE`.

Use the fixed-mean parameterization

```text
x = (a, b, 3 XBAR_NE - a - b),
y = (c, d, 3 YBAR_NE - c - d),
delta = e.
```

Then there exist at least three distinct witness families, each varying only in
the single phase coordinate `e`, such that:

1. the family stays on the fixed native `N_e` seed surface,
2. both endpoints lie in the constructive positive branch
   `gamma > 0`, `E1 > 0`, `E2 > 0`, `Delta_src > 0`,
3. the favored transport value `eta_1` is below `1` at one endpoint and above
   `1` at the other.

Therefore, by continuity, each family contains an exact root with

- `eta_1 = 1`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

The three witness families are disjoint in their `e`-intervals, so the three
exact roots are distinct.

## Explicit witness families

The script verifies the following three fixed-mean families:

### Family A

Fix

- `a = 1.16845863`
- `b = 0.46803892`
- `c = 0.77107315`
- `d = 0.05539671`

and vary

- `e in [1.88233895, 1.89233895]`.

At the left endpoint:

- `eta_1 = 0.999827290444... < 1`.

At the right endpoint:

- `eta_1 = 1.000172032332... > 1`.

All endpoint constructive and positive-branch inequalities remain strict.

### Family B

Fix

- `a = 0.86088785`
- `b = 0.32714819`
- `c = 0.71367707`
- `d = 0.10440906`

and vary

- `e in [1.59150180, 1.60150180]`.

At the left endpoint:

- `eta_1 = 1.000355171609... > 1`.

At the right endpoint:

- `eta_1 = 0.999645825117... < 1`.

Again all endpoint constructive and positive-branch inequalities remain strict.

### Family C

Fix

- `a = 1.00731313`
- `b = 0.30177597`
- `c = 0.79591855`
- `d = 0.02985850`

and vary

- `e in [2.19435677, 2.20435677]`.

At the left endpoint:

- `eta_1 = 1.000210552142... > 1`.

At the right endpoint:

- `eta_1 = 0.999789986336... < 1`.

All endpoint constructive and positive-branch inequalities again remain strict.

The `e`-intervals are pairwise disjoint, so the three continuity roots are
pairwise distinct.

## Corollary 1: exact closure plus positive constructive branch is still not a selector

This is now theorem-grade, not just heuristic.

There is no unique point selected by the conjunction

- `eta = eta_obs`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`

on the current constructive route.

## Corollary 2: the final unexhausted target is finer than exact closure itself

The remaining positive selector law, if it exists, must distinguish among
multiple exact constructive positive closure points.

So the final unexhausted target is strictly finer than:

- transport closure,
- branch sign,
- and the constructive sign chamber.

It must act on additional full-pack right-sensitive microscopic data on
`L_e / dW_e^H`.

## What this closes

- the loophole that exact closure might already become unique on the positive
  constructive branch
- the whole "constructive positive exact-closure by itself is enough" route
- any remaining hope that branch sign plus closure plus triplet signs already
  chooses the physical point

## What this does not close

- a finer retained selector law among the multiple exact constructive positive
  closure points
- the final DM flagship closeout
