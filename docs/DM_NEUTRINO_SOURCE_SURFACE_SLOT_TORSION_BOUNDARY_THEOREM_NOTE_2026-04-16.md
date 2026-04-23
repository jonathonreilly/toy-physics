# DM Neutrino Source-Surface Slot-Torsion Boundary Theorem

**Date:** 2026-04-16
**Status:** exact atlas-supported boundary theorem on the live source-oriented sheet
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_source_surface_slot_torsion_boundary_theorem.py`

## Question

After reducing the live post-canonical `H`-side problem to the exact
source-oriented sheet and its constant intrinsic slot pair `(a_*, b_*)`, can
the current exact one-phase real-slot family from the atlas

```text
a = (u+v) e^{-i phi}
b = (u-v) e^{+i phi}
u,v in R
```

still populate that live sheet?

Equivalently: can the old source-faithful slot-family route still be used as
the constructive mainline selector after the new `H`-side reductions?

## Bottom line

No.

The one-phase real-slot family has exact slot torsion

```text
T_slot(a,b) = Im(a b) = 0
```

because

```text
a b = (u+v)(u-v) = u^2 - v^2 in R.
```

But on the live source-oriented sheet the intrinsic slot pair is already the
exact constant pair `(a_*, b_*)`, and it carries

```text
T_slot(a_*, b_*) = Im(a_* b_*) = (sqrt(2) + sqrt(6)) / 9 != 0.
```

Therefore the live source-oriented sheet lies outside the current exact
one-phase real-slot family.

In particular, it lies outside the exact source-faithful character-transfer
branches `lambda in {-1,0,+1}` with `phi = lambda 2 pi / 3`.

So the old one-phase source-faithful slot family is comparison/support only on
the current mainline branch. It is not the constructive selector for the live
post-canonical `H`-side sheet.

## Inputs

This note reuses and sharpens:

- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [DM_NEUTRINO_Z3_CHARACTER_TRANSFER_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_CHARACTER_TRANSFER_THEOREM_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md)

## Exact theorem

### 1. One-phase real-slot families have zero slot torsion

On the atlas slot family

```text
a = (u+v) e^{-i phi}
b = (u-v) e^{+i phi}
u,v in R,
```

the slot product is

```text
a b = (u+v)(u-v) = u^2 - v^2.
```

So it is always real, and therefore

```text
T_slot(a,b) := Im(a b) = 0.
```

This is an exact necessary condition for one-phase real-slot realizability.

### 2. The live source-oriented slot pair has fixed nonzero torsion

The live source-oriented intrinsic slot theorem already gives

```text
a_* = E2/3 - sqrt(3) gamma/6 + i(E2 + gamma/2)
b_* = E2/3 + sqrt(3) gamma/6 + i(gamma/2 - E2)
```

with

```text
gamma = 1/2
E2 = sqrt(8)/3.
```

Multiplying gives

```text
a_* b_* = 293/324 + i (sqrt(2) + sqrt(6)) / 9,
```

so

```text
T_slot(a_*, b_*) = (sqrt(2) + sqrt(6)) / 9.
```

That is nonzero.

Therefore `(a_*, b_*)` cannot lie on the one-phase real-slot family.

### 3. Corollary: exact source-faithful character branches fail too

The exact `Z_3` character-transfer theorem already says the old source-faithful
phase-lift family is restricted to the discrete local branches

```text
lambda in {-1,0,+1},
phi = lambda 2 pi / 3.
```

But the obstruction above is stronger: the live slot pair does not admit any
one-phase real-slot decomposition at all.

So it certainly does not admit one on those exact source-faithful branches.

## The theorem-level statement

**Theorem (Exact slot-torsion boundary for the live source-oriented sheet).**
Assume the exact singlet-doublet CP-slot theorem, the exact `Z_3`
character-transfer theorem, and the exact source-surface intrinsic-slot
theorem. Then the current atlas one-phase real-slot family satisfies the exact
necessary condition `Im(a b) = 0`, while the live source-oriented intrinsic slot
pair satisfies
`Im(a_* b_*) = (sqrt(2) + sqrt(6)) / 9 != 0`. Therefore the live
source-oriented sheet lies outside the current exact one-phase real-slot family,
and in particular outside the exact source-faithful character-transfer branches
`lambda in {-1,0,+1}`.

## What this closes

This closes a tempting but now incorrect reuse path.

The branch can no longer honestly treat the old one-phase source-faithful slot
family as a constructive selector for the live post-canonical `H`-side sheet.

The sharper statement is:

- the live intrinsic slot pair is already fixed
- it carries nonzero exact slot torsion
- so the old one-phase real-slot family is not the missing mainline law

## What this does not close

This note still does **not** derive the post-canonical law that selects the
remaining exact 2-real active carrier bundle over `(delta, r31)`.

It only says that this law cannot be obtained by reusing the old exact
one-phase source-faithful slot family.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_slot_torsion_boundary_theorem.py
```
