# DM Wilson Direct-Descendant Transport-Fiber Spectral Completion Theorem

**Date:** 2026-04-19
**Status:** support - structural or confirmatory support note
fiber theorem. The remaining `3`-real source ambiguity above the canonical
favored transport column is already an explicit microscopic spectral object,
not an undifferentiated source-side blur.

**Primary runner:**
`scripts/frontier_dm_wilson_direct_descendant_transport_fiber_spectral_completion_theorem_2026_04_19.py`
(`PASS=12 FAIL=0`).

## Question

After the canonical transport-column fiber theorem, the current branch knew
that transport fixes a unique favored-column orbit but leaves a local `3`-real
source fiber unresolved. The honest next question is:

> can that fiber be cut further by an explicit law local to `L_e`, or is it
> still only a vague residual source family?

## Bottom line

Yes. On the current constructive transport plateau, the residual canonical
column fiber is already locally completed by three explicit spectral scalars of
the projected Hermitian response

```text
H_e = (L_e^(-1) + (L_e^(-1))^*) / 2.
```

A canonical choice is

```text
sigma(H_e) = (Tr(H_e), Tr(H_e^2), det(H_e)).
```

At every known plateau witness `W0`, `W1`, `W2`, `W3`, the augmented map

```text
source5 -> (col_1, col_2, Tr(H_e), Tr(H_e^2), det(H_e))
```

has full rank `5`.

Equivalently:

- the favored transport column carries the expected `2` independent reals;
- the remaining `3` local directions are fully seen by the three spectral
  invariants of `H_e`.

So the open DM object is no longer “some unknown `3`-real source law.” It is
already a concrete **3-scalar microscopic spectral law on `L_e`**.

## What the theorem proves

### 1. The constructive plateau still lies over one canonical favored-column orbit

The same four plateau witnesses from the canonical transport-column theorem are
still pairwise separated in source coordinates, but their favored columns agree
up to the same canonical transport orbit.

So the new theorem does not weaken the previous result. It starts exactly from
the established one-column picture.

### 2. The plateau witnesses have distinct local Hermitian spectra

Although the plateau witnesses share the same favored-column orbit, their
projected Hermitian responses `H_e` do not share the same spectrum. The runner
checks:

- simple spectrum at every plateau witness;
- pairwise separated spectral invariant vectors
  `(Tr(H_e), Tr(H_e^2), det(H_e))`.

So transport nonuniqueness is already spectrally visible on the current
branch.

### 3. The three spectral invariants span the local canonical-column fiber

Write the local source surface in the native `5`-real coordinates

```text
(x1, x2, y1, y2, delta).
```

Use the two independent favored-column coordinates `(col_1, col_2)`. Their
Jacobian has rank `2`, so the local canonical-column fiber is `3`-real.

The theorem then checks that the Jacobian of

```text
sigma(H_e) = (Tr(H_e), Tr(H_e^2), det(H_e))
```

restricted to that `3`-real column-fiber kernel has rank `3`.

Therefore the residual transport fiber is locally coordinatized by these three
spectral scalars.

### 4. Transport plus spectral data already gives a local point selector

Because the augmented map

```text
(col_1, col_2, Tr(H_e), Tr(H_e^2), det(H_e))
```

has full rank `5`, it is a local coordinate system on the fixed seed source
surface at each known plateau witness.

So once a microscopic law supplies those three spectral scalars, the local
source is fixed.

## Why this matters

This is a real refinement of the same-day `3`-real source-fiber theorem.

Before this theorem, the remaining DM statement was:

> transport fixes the canonical column but leaves a local `3`-real source
> fiber.

After this theorem, the sharper statement is:

> transport fixes the canonical column, and the entire residual local fiber is
> already an explicit spectral-invariant fiber of `H_e`, hence of `L_e`.

That is a much tighter frontier target. The missing law is not an arbitrary
new source prescription. It is specifically a **three-scalar spectral law** on
the local Schur-side object.

## What this closes

- the idea that the `3`-real fiber is still only a vague source-space
  nonuniqueness;
- the idea that additional transport optimization is the right next move;
- the possibility that the current plateau witnesses are spectrally
  indistinguishable.

## What this does not close

- a retained-physics derivation of those three spectral scalars from Wilson
  data;
- a proof that a smaller canonical subset of those scalars is already fixed by
  reviewer-grade microscopic structure;
- the final DM flagship lane.

## Relation to the earlier same-day DM theorems

This note sits immediately downstream of:

1. `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`
2. `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`
3. `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

The first note identifies the unresolved object as a local `3`-real source
fiber above the canonical favored column. The second note localizes the live
projected Hermitian response to `L_e`. The new theorem combines those facts:
the residual fiber is already a local spectral-invariant fiber of that same
`L_e`-controlled Hermitian object.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_transport_fiber_spectral_completion_theorem_2026_04_19.py
```

Expected:

- `PASS=12 FAIL=0`
