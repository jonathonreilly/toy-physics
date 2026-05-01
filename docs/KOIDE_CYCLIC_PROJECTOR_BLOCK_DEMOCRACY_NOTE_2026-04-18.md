# Koide Cyclic-Projector Block Democracy

**Date:** 2026-04-18
**Status:** bounded - bounded or caveated result note
lane
**Runner:** `scripts/frontier_koide_cyclic_projector_block_democracy.py`

## Question

The charged-lepton Koide lane now has an explicit cyclic Wilson-descendant law:

- exact cyclic basis
  `B0 = I`, `B1 = C + C^2`, `B2 = i(C - C^2)`,
- exact cyclic responses
  `(r0, r1, r2)`,
- exact cyclic target reconstruction,
- exact response-space Koide equation
  `2 r0^2 = r1^2 + r2^2`.

What is the cleanest **fresh first-principles selector candidate** for that
equation?

The old best candidate was the real-irrep block-democracy / block-log-volume
language. That is still important. But there is an even simpler way to state
the same structure directly from the exact cyclic projector.

## Bottom line

The cleanest fresh selector candidate is:

> **equal cyclic block power** between the unique `C_3`-fixed real line and the
> canonical real `2`-dimensional doublet in the cyclic image.

This gives Koide immediately.

## Exact setup

On the cyclic Hermitian image, the canonical basis is
```
B0 = I,
B1 = C + C^2,
B2 = i(C - C^2).
```

The cyclic descendant law writes the target as
```
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.
```

This image carries an exact canonical `1 ⊕ 2` real block decomposition:
```
span_R{B0}  ⊕  span_R{B1, B2}.
```

That split is not ad hoc:

- `B0` spans the scalar / trace line inside the cyclic Hermitian image;
- `B1, B2` span the traceless cyclic plane, equivalently the real and
  imaginary slots of the nontrivial character mode;
- the real-trace metric gives the exact norms
  ```
  ||B0||^2 = 3,
  ||B1||^2 = ||B2||^2 = 6,
  ```
  with all cross terms zero.

So the cyclic image already comes with a canonical block geometry from the
axiom surface itself.

## The selector law

Define:
```
H_+    = (r0/3) B0,
H_perp = (r1/6) B1 + (r2/6) B2.
```

Then the exact block powers are
```
E_+    = Re Tr(H_+^2)    = r0^2 / 3,
E_perp = Re Tr(H_perp^2) = (r1^2 + r2^2) / 6.
```

Demand equal block power:
```
E_+ = E_perp.
```

This is exactly
```
r0^2 / 3 = (r1^2 + r2^2) / 6
```
which is equivalent to
```
2 r0^2 = r1^2 + r2^2.
```

That is precisely the Koide selector equation on the cyclic responses.

## Why this is cleaner than the older language

The older candidate phrasing was:

- unweighted real-irrep block democracy,
- or the maximum of unweighted block log-volume.

That remains mathematically correct and useful.

But the cyclic-projector statement is cleaner as a first-principles candidate
because it starts directly from:

- the exact cyclic projector image,
- the canonical scalar-versus-traceless split on that image,
- the exact canonical trace norms of the `1 ⊕ 2` split.

So the fresh selector candidate is not:

- “maximize a later information-theoretic functional somehow.”

It is:

- “the exact cyclic source law lands at equal power in the canonical `1`-block
  and `2`-block.”

That is much closer to the axiom surface.

## Bridge to the older Koide language

Write
```
H_cyc = a B0 + x B1 + y B2.
```

Since
```
a = r0/3,
x = r1/6,
y = r2/6,
```
the cyclic-projector block-democracy equation becomes
```
a^2 = 2(x^2 + y^2).
```

Equivalently, if
```
b = x + i y,
```
then
```
3 a^2 = 6 |b|^2.
```

So this is exactly the same Koide selector law already seen in the circulant
coordinates and in the older character-space note. The new contribution is
only the cleaner first-principles wording.

## Observed charged-lepton witness

The runner verifies that the observed charged-lepton amplitude operator built
from the PDG `√m` spectrum satisfies this equal-block-power law to Koide
precision.

So the selector is not only formally correct. It lands on the actual target.

## Consequence

This is now the cleanest fresh axiom-first selector candidate on the Koide
lane:

1. derive the microscopic cyclic source law for `(r0, r1, r2)`,
2. derive or justify equal cyclic block power
   `E_+ = E_perp`,
3. then Koide follows immediately.

## What this does not yet close

This note does **not** yet derive:

- the microscopic source law for `(r0, r1, r2)`,
- the dynamical reason equal cyclic block power should hold,
- the final charged-lepton readout primitive.

But it does replace a vaguer selector question with a very clean first-
principles target.

## Bottom line

The best fresh axiom-only selector candidate is now:

> on the exact cyclic projector image, demand equal power in the canonical
> scalar line and the canonical traceless cyclic plane.

That is exactly the Koide law.
