# DM Wilson Direct-Descendant Local Observable-Coordinate Theorem

**Date:** 2026-04-19
**Status:** exact local differential theorem on the open DM selector gate. On
the fixed native `N_e` seed surface, the projected-source observable pack

`(eta_1, gamma, E1, E2, Delta_src)`

already has full local rank at the constructive positive exact-closure root.
So the remaining selector gap is **not** a hidden-coordinate problem. It is a
missing value-law problem: current conditions impose one exact equality
`eta_1 = 1` together with four open sign conditions, and that semantic package
does not isolate a point.
**Primary runner:**
`scripts/frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19.py`
(`PASS=10 FAIL=0`).

## Question

After the constructive positive branch theorem, multiplicity theorem, manifold
theorem, and the new local-Schur branch-discriminant theorem, what exactly is
still missing on the DM direct-descendant selector route?

Is the problem that the current scalar pack still misses some local coordinate
on the right-sensitive projected-source data?

Or is the problem already sharper: the present observables are locally enough,
but the current semantics are too weak?

## Bottom line

The problem is already the second one.

At the constructive positive exact-closure root on the fixed native `N_e` seed
surface, the `5 x 5` Jacobian of

`(eta_1, gamma, E1, E2, Delta_src)`

with respect to the local `5`-real source coordinates is non-singular and
stable across finite-difference scales. By the inverse-function theorem, this
observable pack is already a local coordinate chart.

Restricting to the exact-closure manifold `eta_1 = 1`, the residual `4`-pack

`(gamma, E1, E2, Delta_src)`

still has full rank on the `4`-real tangent space. So those four observables
already coordinatize the exact-closure manifold itself.

Therefore the live insufficiency is not:

- missing local observables.

It is:

- missing value laws for observables that already exist.

Current semantics are only:

- `eta_1 = 1`,
- `gamma > 0`,
- `E1 > 0`,
- `E2 > 0`,
- `Delta_src > 0`.

That is one equality plus four open inequalities. It selects an open region of
the exact-closure manifold, not a point.

## The theorem

Write the fixed native `N_e` seed surface in local `5`-real coordinates

`(a, b, c, d, e)`.

Define the exact projected-source observable map

```text
O(a,b,c,d,e)
  = (eta_1, gamma, E1, E2, Delta_src).
```

Let `p_*` be the explicit constructive positive exact-closure root already
certified by the manifold theorem.

> **Theorem.**
>
> 1. `D O(p_*)` has full rank `5`;
> 2. therefore `O` is a local coordinate system near `p_*`;
> 3. on the exact-closure manifold `eta_1 = 1`, the restricted `4`-pack
>    `(gamma, E1, E2, Delta_src)` has full rank `4`;
> 4. therefore the current semantics
>    `eta_1 = 1`, `gamma > 0`, `E1 > 0`, `E2 > 0`, `Delta_src > 0`
>    define a local open region, not a point-selector law.

So the remaining selector gap is exactly a missing observable-value law on a
pack that is already locally complete.

## Why this matters

This changes the interpretation of the open DM gate.

Before this theorem, one could still suspect that the remaining difficulty was
local coordinate incompleteness: perhaps the current scalar pack did not yet
see enough of the projected-source data to phrase the selector properly.

That loophole is now closed locally.

The branch already has enough local observables. What it lacks is stronger
selection content.

In particular, a future selector cannot close the point just by repeating the
current semantic form with a nicer explanation. It has to add real value
conditions.

## Consequence for the remaining law

Locally near the certified root:

- `eta_1 = 1` removes one real dimension;
- the sign conditions are open and remove no local dimension;
- the exact-closure manifold is still `4`-real;
- the four-pack `(gamma, E1, E2, Delta_src)` already parametrizes it.

So any future scalar-equation selector that still aims to isolate a point by
observable conditions must effectively provide **four more real equations**
beyond `eta_1 = 1`, or an equivalent vector-valued law of the same local
strength.

That is the sharpest local codimension statement now available on this route.

## Relation to the previous same-day theorem

The earlier same-day theorem

- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`

proved that the branch scalar is already local to `L_e`:

`Delta_src(dW_e^H) = det(H_e(L_e))`.

The present theorem adds the complementary local statement:

- the current observable pack is already locally complete,
- but the present semantic constraints on that pack are still too weak.

Together, these two results say:

1. the source-side object is already local to the descended block;
2. the observable pack on that block is already a local coordinate system;
3. what remains missing is a stronger value law on those observables.

## What this closes

- the loophole that the open selector gap might still be local observable
  incompleteness;
- the idea that current sign semantics might almost isolate the point if one
  only changed the framing;
- the ambiguity between "missing coordinates" and "missing values" on the DM
  direct-descendant route.

## What this does not close

- the actual value law selecting the physical point;
- the final DM flagship lane;
- a global uniqueness theorem away from the local neighborhood of the
  constructive positive root.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_POSITIVE_BRANCH_COMPATIBILITY_AND_INSUFFICIENCY_THEOREM_NOTE_2026-04-18.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MULTIPLICITY_THEOREM_NOTE_2026-04-18.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MANIFOLD_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MANIFOLD_THEOREM_NOTE_2026-04-18.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md)

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19.py
```

Expected:

- `PASS=10 FAIL=0`
