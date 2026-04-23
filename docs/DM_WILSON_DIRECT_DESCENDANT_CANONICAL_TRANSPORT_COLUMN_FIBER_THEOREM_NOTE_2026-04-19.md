# DM Wilson Direct-Descendant Canonical Transport-Column Fiber Theorem

**Date:** 2026-04-19
**Status:** exact current-branch theorem sharpening the DM transport-side
selector object. Exact flavored transport on the probability-simplex column
space already selects a unique current-branch maximizer orbit

```text
(0.0356443..., 0.0356443..., 0.9287114...)
```

up to flavor permutation. All currently known constructive transport-plateau
witnesses realize that same favored-column orbit. But on the fixed native
`N_e` seed surface, the direct-descendant source -> favored-column map has
rank `2` on a `5`-real source surface, so transport still leaves a local
`3`-real source fiber unresolved.

So the remaining DM issue is no longer “what favored column does transport
want?” The branch now answers that. The remaining issue is the **microscopic
law that selects a source in the fiber over that canonical column orbit.**

**Primary runner:**
`scripts/frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19.py`
(`PASS=16 FAIL=0`).

## Question

After the new constructive transport plateau theorem, the remaining ambiguity
could still have been read in two different ways:

1. maybe transport had not yet fixed the correct favored PMNS column
   tightly enough; or
2. maybe transport had already fixed the favored column, and the unresolved
   ambiguity lived entirely in the source-side realizations of that column.

This theorem distinguishes those two possibilities.

## Bottom line

Transport is already as closed as it is going to get on the current branch.

It does **not** leave the favored column ambiguous. Instead, it fixes a unique
current-branch favored-column **orbit** on the simplex, represented by

```text
col_* = (0.0356443..., 0.0356443..., 0.9287114...)
```

up to row permutation.

But that does **not** fix a unique direct-descendant source. The fixed-seed
source surface is `5`-real, while the favored column carries only `2`
independent reals, and the exact Jacobian at the constructive witness has rank
`2`. So the unresolved object is now concrete:

> a local `3`-real source fiber above the canonical favored transport column.

That is the science left.

## What the theorem proves

### 1. The transport-optimal column orbit is unique on the simplex

Deterministic global search plus independent local refinements all collapse to
the same ordered simplex maximizer orbit. Its ordered representative is

```text
col_* = (q_small, q_small, 1 - 2 q_small)
      = (0.0356443..., 0.0356443..., 0.9287114...).
```

The theorem also checks the exact current-branch stationarity conditions:

- the interior simplex KKT equations hold;
- the restricted Hessian on the simplex tangent space is negative definite.

So, on the branch’s exact flavored transport functional, the favored column is
already canonical up to flavor permutation.

### 2. The constructive plateau witnesses all realize that same column orbit

The four same-day constructive transport-extremal witnesses `W0`, `W1`, `W2`,
`W3` all have favored columns whose sorted multisets agree with `col_*` to
current-branch precision.

Equivalently:

```text
sort(col_1(W0)) = sort(col_1(W1)) = sort(col_1(W2)) = sort(col_1(W3)) = col_*.
```

One of the witnesses reaches the same orbit by a nontrivial row permutation,
which is exactly invisible to the transport functional because the transport
readout depends only on the unordered column entries.

So the constructive plateau is not just optimizer noise. It already sits above
a structurally transport-blind column orbit.

### 3. The remaining ambiguity is a source fiber, not a transport ambiguity

At the constructive witness, the exact Jacobian of

```text
(x1, x2, y1, y2, delta)  ->  favored transport column
```

has rank `2`. Since the fixed native seed surface is `5`-real, the local
fiber dimension is therefore

```text
5 - 2 = 3.
```

So even after transport has fixed the canonical favored column, there remain
locally three source-side degrees of freedom invisible to transport alone.

The current constructive plateau already intersects that fiber in multiple
pairwise separated sources, with minimum source separation

```text
0.417121011662...
```

while their favored-column multisets agree to `O(10^-8)`.

## Why this matters

This is the cleanest same-day compression of the remaining DM science.

Before this theorem, one could still phrase the gap vaguely:

- maybe the branch still needed “the transport law”;
- maybe transport itself had not singled out the right transport object.

After this theorem, that is no longer the honest reading.

The branch now knows:

- the canonical favored transport column orbit;
- the fact that the constructive plateau already lies over that orbit;
- the exact local size of the remaining unresolved source-side fiber.

So the remaining science is now sharply identified as:

> derive the microscopic law on `L_e` (or an equivalent retained-physics law)
> that selects a point in the `3`-real fixed-seed source fiber over
> `col_*`.

## Relation to the earlier same-day DM theorems

This theorem sits downstream of four already-landed same-day sharpenings:

1. **local Schur branch-discriminant theorem**
   The branch sign is already local to `L_e = Schur_{E_e}(D_-)`.
2. **local observable-coordinate theorem**
   `(eta_1, gamma, E1, E2, Delta_src)` already gives local coordinates.
3. **canonical path-selector theorem**
   the branch carries an explicit path-selected law candidate.
4. **constructive transport plateau theorem**
   constructive transport extremality alone does not pick a unique endpoint.

The new theorem explains that last obstruction structurally:

- transport **does** fix a canonical column;
- but source-side nonuniqueness survives above that column as a real fiber.

## What this closes

- the idea that transport ambiguity still lives at the column level;
- the hope that more transport optimization alone would uniquely select the
  direct-descendant source;
- the possibility that the remaining DM gap is still “which favored column?”

## What this does not close

- the microscopic value law on `L_e`;
- a reviewer-grade derivation of the direct-descendant source from retained
  physics;
- the final DM flagship lane.

## Cross-references

- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19.py
```

Expected:

- `PASS=16 FAIL=0`
