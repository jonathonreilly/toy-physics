# Planck Finite-Response No-Go Note

**Date:** 2026-04-24
**Status:** proposed_no_go / blocker closeout for the Planck-scale lane
**Runner:** `scripts/frontier_planck_finite_response_nogo.py`

## Purpose

This note closes one bounded open item left by the conditional Planck packet:
the finite-automorphism-only response route.

The result is negative. Bare finite primitive-cell automorphisms can carry
discrete symmetry bookkeeping, but they cannot by themselves produce the
infinitesimal local metric/coframe response required to identify the primitive
cell count as a gravitational boundary/action carrier.

## The no-go

Use the primitive time-locked event-cell frame with four axes:

```text
(t, x, y, z).
```

The finite frame automorphism group on this primitive real frame is the signed
permutation group:

```text
B_4 = (Z_2)^4 semidirect S_4,
|B_4| = 2^4 4! = 384.
```

In the defining four-dimensional representation, every nonidentity signed
permutation is separated from the identity by a positive Frobenius distance.
The nearest nonidentity elements are one sign flip or one coordinate swap, and
both sit at

```text
min_{g != I} ||g - I||_F = 2.
```

Therefore there is an open neighborhood of the identity containing no
nontrivial finite-frame transformation. The infinitesimal tangent available
from finite automorphisms alone is zero-dimensional.

But local metric/coframe response requires a nonzero infinitesimal response
space. Already at the linearized metric level,

```text
dim Sym^2(R^4) = 10.
```

So the finite group cannot supply the local metric-response directions. A
small symmetric perturbation such as

```text
I + epsilon h,    epsilon = 0.01,
```

is outside the finite signed-permutation orbit even though it is arbitrarily
near the identity.

The usual finite-dimensional canonical-response obstruction is independent and
points the same way:

```text
Tr([X, P]) = 0
```

for finite matrices, while a nonzero canonical commutator would require

```text
Tr(i hbar I_n) != 0.
```

Thus a finite static cell algebra cannot furnish the canonical local response
surface either.

## What this closes

This closes the fourth blocker named in the conditional Planck packet:

> A finite-automorphism-only route still needs a positive theorem deriving
> local metric/coframe response without invoking the canonical realified
> response envelope.

The positive theorem cannot exist for the finite automorphism route as stated:
the finite frame has no infinitesimal response directions.

## What remains open

This no-go does **not** close the Planck-scale derivation. It narrows the lane
by removing one bad route.

The remaining load-bearing open items are:

1. the minimal-stack absolute-scale derivation still does not follow from the
   older finite stack alone;
2. the primitive one-step boundary/worldtube count still needs to be derived
   as the microscopic carrier of the gravitational boundary/action density, or
   accepted explicitly as the Planck package carrier identification;
3. if the parent-source scalar route is used, it still needs a derived
   no-hidden-character law `delta = 0`; the carrier-only shortcut is closed
   negatively in
   [PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md](./PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md).

## Package wording

Safe wording:

> The finite-automorphism-only Planck route is closed negatively: finite
> primitive-cell automorphisms have a positive identity gap and zero
> infinitesimal tangent, so they cannot derive the local metric/coframe
> response needed for the gravitational carrier identification.

Unsafe wording:

> Finite `Cl(3)` / `Z^3` automorphisms alone force the Planck scale.

The conditional completion packet remains the current positive Planck support
statement:

> `c_cell = 1/4` and `a/l_P = 1` after the primitive boundary count is accepted
> as the microscopic gravitational boundary/action carrier.

## Verification

Run:

```bash
python3 scripts/frontier_planck_finite_response_nogo.py
```

The runner checks:

1. `|B_4| = 384`;
2. the nearest nonidentity finite-frame transform is distance `2` from the
   identity;
3. no nontrivial finite transform lies in the small identity neighborhood;
4. finite automorphisms have zero tangent dimension versus the `10` linearized
   metric directions;
5. an arbitrarily small symmetric metric perturbation is outside the finite
   signed-permutation orbit;
6. finite-dimensional canonical commutators are trace-forbidden.
