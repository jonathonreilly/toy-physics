# DM Neutrino Source-Bank `Z_3` Doublet-Block Selection Obstruction Theorem

**Date:** 2026-04-16  
**Status:** exact atlas-supported obstruction theorem on the live source-oriented sheet  
**Script:** `scripts/frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem.py`

## Question

After checking the reusable atlas tools, does the current exact source bank
determine the remaining right-sensitive `Z_3` doublet-block point
`(delta, q_+)` on the live source-oriented sheet?

## Bottom line

No.

The atlas-supported upstream source side is already closed to the fixed sharp
tuple

- `a_sel = 1/2`
- `tau_+ = 1`
- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`.

But the live target still moves in the exact `2`-real active pair

- `(delta, q_+)`

equivalently in the `Z_3` doublet block through

- `q_+ = 2 sqrt(2)/9 - (K11 + K22)/2`
- `delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)`.

There are distinct live-sheet points with different `(delta, q_+)` and
different `Z_3` doublet blocks that carry exactly the same current-bank
signature

- `(gamma, E1, E2, cp1, cp2, a_*, b_*, T_slot)`.

So no deterministic selector that factors only through the current exact
atlas-supported source bank can choose the active point.

The minimal missing object is therefore:

- a **new right-sensitive `2`-real datum**,

equivalently:

- the `Z_3` doublet-block law itself.

## Atlas tools actually used

This note reuses the existing atlas rows that matter for the live gate:

- [DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md)
- [DM_NEUTRINO_WEAK_TRIPLET_COEFFICIENT_AXIOM_BOUNDARY_NOTE_2026-04-15.md](./DM_NEUTRINO_WEAK_TRIPLET_COEFFICIENT_AXIOM_BOUNDARY_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md)

The point is not to reopen those routes. It is to combine them into the exact
obstruction statement for the remaining live object.

## Exact theorem

### 1. The current exact upstream source bank is already a fixed point

The source-amplitude theorem already fixes

- `a_sel = 1/2`
- `tau_+ = 1`.

The coefficient-closure theorem then gives

- `gamma = a_sel = 1/2`
- `E1 = sqrt(8/3) tau_+ = sqrt(8/3)`
- `E2 = (sqrt(8)/3) tau_+ = sqrt(8)/3`.

So the current exact source bank is not an open carrier with live continuous
degrees of freedom on the sharp source-oriented branch. It is already one
exact source tuple.

### 2. The live active target is still a genuine `2`-real object

The active-half-plane and doublet-block theorems already show that the live
target is the exact `2`-real bundle

- `(delta, q_+)`,

equivalently the moving `Z_3` doublet block

- centered trace giving `q_+`
- shifted imaginary doublet mixing giving `delta`.

So the live target is still not a fixed point. It moves in two independent
real directions.

### 3. The same exact current-bank signature occurs at different target points

Take live-sheet points with

- different `delta` at fixed `q_+`
- different `q_+` at fixed `delta`.

For those points, the current exact bank remains unchanged:

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`
- intrinsic CP pair `(cp1, cp2)`
- intrinsic slot pair `(a_*, b_*)`
- slot torsion `T_slot = Im(a_* b_*)`.

But the `Z_3` doublet block changes, and therefore `(delta, q_+)` changes.

So the current bank is exact but point-blind.

### 4. Consequence: no selector through the current exact bank

If two distinct active points carry the same exact current-bank signature,
then no deterministic selector that factors only through that signature can
output both points correctly.

Therefore the current exact atlas-supported source bank cannot determine the
live active point.

## The theorem-level statement

**Theorem (Current source-bank obstruction to `Z_3` doublet-block point
selection).** Assume the exact source-amplitude theorem, the exact
weak-triplet coefficient closure, the exact active-half-plane theorem, and the
exact `Z_3` doublet-block location/blindness theorems. Then the current exact
upstream source bank already closes to the fixed sharp tuple
`(a_sel, tau_+, gamma, E1, E2) = (1/2, 1, 1/2, sqrt(8/3), sqrt(8)/3)`, while
the live target still moves in the exact `2`-real pair `(delta, q_+)`,
equivalently in the `Z_3` doublet block. There exist distinct live-sheet
points with different `(delta, q_+)` but identical exact current-bank
signature `(gamma, E1, E2, cp1, cp2, a_*, b_*, T_slot)`. Therefore no
deterministic selector that factors only through the current exact
atlas-supported source bank can determine the active point. The minimal
missing object is a new right-sensitive `2`-real datum, equivalently the
`Z_3` doublet-block law itself.

## What this closes

This closes the next fake-positive route.

The branch can no longer honestly say:

- “maybe the existing atlas source bank already picks the active point if we
  package it better”
- “maybe the remaining object is only a hidden one-real normalization”
- “maybe the old source closures already determine the live doublet block”

The sharper statement is:

- the old source closures are already exact,
- they already collapse to a fixed upstream tuple,
- and they still do **not** choose `(delta, q_+)`.

## What this does not close

This note still does **not** derive the missing new datum.

It proves only that the datum is genuinely new and genuinely `2`-real on the
current branch.

So the next constructive theorem, if it exists, must introduce or derive:

- a new right-sensitive `2`-real source datum,

or directly:

- the microscopic `Z_3` doublet-block law.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem.py
```
