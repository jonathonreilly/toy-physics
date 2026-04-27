# Planck Parent-Source Hidden-Character No-Go Note

**Date:** 2026-04-24
**Status:** proposed_retained no-go / blocker closeout for the Planck-scale lane
**Runner:** `scripts/frontier_planck_parent_source_hidden_character_nogo.py`

## Purpose

This note closes another bounded route left open by the conditional Planck
packet: the unconstrained parent-source scalar promotion route.

The result is negative. A carrier-level diagram can commute while an additive
parent-source scalar remains free. Therefore the Schur/event scalar equality
cannot be derived from carrier data alone. Promotion still needs a
no-hidden-character law or a direct gravitational carrier-identification
theorem.

## The obstruction

Write a minimal parent-source fiber as

```text
parent = (c_cell, delta),
```

where `c_cell = 1/4` is the primitive event coefficient and `delta` is a hidden
affine scalar character.

The carrier-level map sees only

```text
C(parent) = c_cell.
```

So every point on the affine fiber

```text
(c_cell, delta)
```

has the same carrier data.

But the Schur/parent scalar can read

```text
p_Schur(parent) = c_cell + delta,
```

while the event scalar is

```text
p_event(parent) = c_cell.
```

Hence

```text
p_Schur = p_event    iff    delta = 0.
```

The hidden direction `(0,1)` is invisible to the carrier map but visible to
the Schur/event scalar equality. That proves the carrier-level diagram alone
cannot force the scalar equality.

## Why this matters for Planck normalization

The conditional Planck packet uses the event coefficient

```text
c_cell = 1/4
```

and then matches it to the gravitational area/action density:

```text
c_cell / a^2 = 1 / (4 l_P^2).
```

If the Schur/parent scalar is allowed to shift to `c_cell + delta`, then the
same algebra would instead give

```text
a/l_P = sqrt(4 (c_cell + delta)).
```

For example:

```text
delta = 0       -> a/l_P = 1,
delta = 0.10    -> a/l_P = sqrt(1.4) = 1.183215956620...
```

So the hidden scalar is not harmless bookkeeping if the parent-source scalar is
used as the Planck coefficient.

## What this closes

This closes the carrier-only parent-source scalar route negatively:

> A carrier-level Schur/event diagram by itself promotes the Planck
> conditional completion.

It does not. Carrier commutation is compatible with an affine hidden scalar.
Any carrier-only function takes one value on the whole fiber, while the Schur
scalar takes different values when `delta` changes.

## What remains open

This note does **not** prove that no future no-hidden-character law can be
derived. It isolates the exact positive target:

1. derive `delta = 0` from a parent-source law, or
2. avoid the parent-source scalar route and derive the primitive
   one-step boundary/worldtube count directly as the microscopic
   gravitational boundary/action carrier.

Those are now the honest positive Planck-scale targets.

## Package wording

Safe wording:

> The unconstrained parent-source scalar route is closed negatively: carrier
> data alone leave an affine hidden character `delta`, and Schur/event scalar
> equality is equivalent to the extra law `delta = 0`.

Unsafe wording:

> The Schur/event carrier diagram alone derives the Planck coefficient.

## Verification

Run:

```bash
python3 scripts/frontier_planck_parent_source_hidden_character_nogo.py
```

The runner checks:

1. the hidden direction lies in the carrier kernel;
2. two parent-source points with identical carrier data can have different
   Schur scalars;
3. no carrier-only function can recover the Schur scalar on the hidden fiber;
4. Schur/event equality is equivalent to `delta = 0`;
5. a nonzero hidden scalar changes the Planck normalization if used as the
   coefficient.
