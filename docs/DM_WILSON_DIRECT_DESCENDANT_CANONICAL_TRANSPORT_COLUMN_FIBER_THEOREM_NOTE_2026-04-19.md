# DM Wilson Direct-Descendant Canonical Transport-Column Fiber Theorem

**Date:** 2026-04-19  
**Status:** exact current-branch source-fiber reduction theorem. Exact flavored
transport on the probability-simplex column space already selects a unique
current-branch maximizer orbit

```text
(0.0356443..., 0.0356443..., 0.9287114...)
```

up to flavor permutation. All currently known constructive transport-plateau
witnesses realize that same favored-column orbit. On the fixed native `N_e`
seed surface, the direct-descendant source -> favored-column map has rank `2`
on a `5`-real source surface, so transport leaves a local `3`-real source
fiber unresolved.

The new sharpened point is this:

- on each known local representative of that canonical column fiber, the
  direct-descendant triplet values `(gamma, E1, E2)` already have full rank
  `3` on the residual `3`-real fiber, so an exact direct-descendant
  triplet-value law would locally pick a unique source;
- but the currently retained exact source-oriented triplet package
  `(1/2, sqrt(8/3), sqrt(8)/3)` does **not** land on the direct-descendant
  fixed-seed surface at all.

So the remaining DM issue is no longer “what favored column does transport
want?” and it is not “find some extra transport optimization.” It is:

> derive the **compatible direct-descendant triplet-value law** on
> `L_e / dW_e^H / (gamma, E1, E2)` above the canonical favored-column orbit.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19.py`
(`PASS=22 FAIL=0`).

## Question

After the new constructive transport plateau theorem, the remaining ambiguity
could still have been read in three different ways:

1. maybe transport had not yet fixed the correct favored PMNS column
   tightly enough; or
2. maybe transport had already fixed the favored column, and the unresolved
   ambiguity lived entirely in the source-side realizations of that column; or
3. maybe the already-retained exact triplet package from the older
   source-oriented lane was already the missing microscopic law on that fiber.

This theorem distinguishes all three possibilities.

## Bottom line

Transport is already as closed as it is going to get on the current branch.

It does **not** leave the favored column ambiguous. Instead, it fixes a unique
current-branch favored-column **orbit** on the simplex, represented by

```text
col_* = (0.0356443..., 0.0356443..., 0.9287114...)
```

up to row permutation.

That still does **not** fix a unique direct-descendant source. The fixed-seed
source surface is `5`-real, while the favored column carries only `2`
independent reals, and the exact Jacobian at the constructive witness has rank
`2`. So the unresolved object is first reduced to:

> a local `3`-real source fiber above the canonical favored transport column.

But the theorem sharpens it one step further.

On every currently known local representative of that fiber, the
direct-descendant map

```text
source -> (favored column, gamma, E1, E2)
```

has full rank `5`, and the restricted triplet map

```text
fiber -> (gamma, E1, E2)
```

has full rank `3`.

So the remaining local selector object is exactly:

> the direct-descendant triplet-value law on the canonical source fiber.

That is real progress. But it still does **not** close the branch, because the
currently retained exact source-oriented triplet package

```text
(gamma, E1, E2) = (1/2, sqrt(8/3), sqrt(8)/3)
```

has no preimage on the direct-descendant fixed-seed source surface. So it
cannot be the missing source law here.

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

### 4. On that local fiber, the direct-descendant triplet values are already a complete coordinate system

Fix any of the four currently certified canonical-column witnesses `W0-W3`.
At each witness, the exact Jacobian of

```text
source -> (favored column, gamma, E1, E2)
```

has full rank `5`.

Equivalently, after restricting to the local `3`-real fiber over the raw
favored-column representative, the triplet map

```text
fiber -> (gamma, E1, E2)
```

has rank `3`.

So if the branch had an exact **direct-descendant** triplet-value law on that
fiber, it would locally pick a unique source. The local codimension gap is not
larger than the triplet itself.

### 5. The currently retained exact source-oriented triplet package is not that law

The older retained source-oriented lane already fixes the exact triplet

```text
(gamma, E1, E2) = (1/2, sqrt(8/3), sqrt(8)/3).
```

The runner now performs a deterministic global search over the full fixed
native `N_e` seed surface and finds that this target is not attained anywhere.
The closest direct-descendant triplet still misses by

```text
||(gamma, E1, E2) - (1/2, sqrt(8/3), sqrt(8)/3)|| = 0.568319...
```

with componentwise errors

```text
(-0.499881..., -0.182635..., -0.199374...).
```

So the currently retained exact triplet package from the source-oriented lane
does **not** collapse the canonical direct-descendant source fiber. It is not
even compatible with the direct-descendant source surface.

## Why this matters

This is the cleanest same-day compression of the remaining DM science.

Before this theorem, one could still phrase the gap vaguely:

- maybe the branch still needed “the transport law”;
- maybe transport itself had not singled out the right transport object.

After this theorem, that is no longer the honest reading.

The branch now knows:

- the canonical favored transport column orbit;
- the fact that the constructive plateau already lies over that orbit;
- the exact local size of the remaining unresolved source-side fiber;
- and the exact local observable type that would close it if its values were
  known.

That is a materially sharper answer than the old generic “microscopic value
law on `L_e`” wording.

The remaining science is now sharply identified as:

> derive the **compatible direct-descendant triplet-value law**
> `(gamma, E1, E2)` on `L_e / dW_e^H` above the canonical favored-column orbit,
> or an equivalent `3`-real microscopic law of the same strength.

And it also closes a tempting but false shortcut:

> import the already-retained source-oriented exact triplet package.

That package is real science on its own lane, but it is **not** the missing
selector on this direct-descendant source surface.

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
5. **exact-kernel / source-oriented triplet package**  
   the older source-oriented lane already fixes
   `(gamma, E1, E2) = (1/2, sqrt(8/3), sqrt(8)/3)`.

The new theorem explains the remaining obstruction structurally:

- transport **does** fix a canonical column;
- source-side nonuniqueness survives above that column as a real fiber;
- direct-descendant triplet values are locally the right coordinates on that
  fiber;
- but the old exact source-oriented triplet values are not the right values
  for this lane.

## What this closes

- the idea that transport ambiguity still lives at the column level;
- the hope that more transport optimization alone would uniquely select the
  direct-descendant source;
- the possibility that the remaining DM gap is still “which favored column?”
- the shortcut claim that the already-retained exact source-oriented triplet
  package automatically closes the direct-descendant source fiber.

## What this does not close

- the compatible direct-descendant triplet-value law on `L_e`;
- a reviewer-grade derivation of the direct-descendant source from retained
  physics;
- the final DM flagship gate.

## Cross-references

- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_PATH_SELECTOR_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md`
- `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_SCHUR_ENTROPY_CANDIDATE_NO_GO_NOTE_2026-04-19.md`

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_2026_04_19.py
```

Expected:

- `PASS=22 FAIL=0`
