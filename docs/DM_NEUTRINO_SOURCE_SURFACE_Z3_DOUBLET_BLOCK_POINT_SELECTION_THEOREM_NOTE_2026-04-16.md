# DM Neutrino Source-Surface `Z_3` Doublet-Block Point-Selection Theorem

**Date:** 2026-04-16
**Status:** exact blocker-identification theorem on the live source-oriented sheet
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py`

## Question

Once the live source-oriented sheet is pushed through the intrinsic `Z_3`
carrier readout, where does the remaining microscopic datum actually live?

## Bottom line

It lives entirely in the `Z_3` doublet block, not in the singlet-doublet slots.

On the live source-oriented sheet, the intrinsic `Z_3` kernel

```text
K_Z3(H) = U_Z3^dag H U_Z3
```

already has exact frozen singlet-doublet slots

```text
K01 = a_*
K02 = b_*
```

with the same constant pair already isolated by the intrinsic-slot theorem.

What moves is only the doublet block:

```text
K11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3))
K22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3))
K12 = m - 4 sqrt(2)/9 + i (sqrt(3) delta - 4 sqrt(2)/3).
```

So after quotienting the spectator line `m`, the remaining mainline datum is
exactly the `2`-real `Z_3` doublet-block law

```text
q_+ = 2 sqrt(2)/9 - (K11 + K22)/2
delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3).
```

The atlas slot tools help here by showing what is **not** left:

- the singlet-doublet slots are already frozen,
- the remaining microscopic selection object lives entirely in the moving
  doublet block.

## Inputs

This note uses and sharpens:

- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)

## Exact theorem

### 1. The `Z_3` image of the live sheet has frozen slots

The intrinsic-slot theorem already gave one exact constant pair `(a_*, b_*)`.

Pushing the affine live sheet through

```text
K_Z3(H) = U_Z3^dag H U_Z3
```

shows that

```text
K01 = a_*
K02 = b_*
```

everywhere on that live sheet.

So the singlet-doublet slot pair is not the remaining microscopic datum.

### 2. The whole active motion sits in the doublet block

On the same live sheet, the moving entries are exactly

```text
K11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3))
K22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3))
K12 = m - 4 sqrt(2)/9 + i (sqrt(3) delta - 4 sqrt(2)/3).
```

So:

- `q_+` is read from the centered doublet trace,
- `delta` is read from the shifted imaginary doublet mixing,
- `m` is only the spectator real doublet-mixing / trace line.

Equivalently,

```text
q_+ = 2 sqrt(2)/9 - (K11 + K22)/2
delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)
m = Re K12 + 4 sqrt(2)/9 = Tr(K_Z3).
```

### 3. What the atlas slot tools do and do not give

The singlet-doublet CP-slot tool and the earlier slot-support theorems remain
correct structural tools. They identify the physical slot carrier and the CP
source channels.

But on the live source-oriented sheet they now help by negative information:

- the slots are already fixed,
- varying `(delta, q_+)` moves only the doublet block,
- therefore the missing microscopic law is not another slot-amplitude law.

It is the `2`-real `Z_3` doublet-block law above.

## The theorem-level statement

**Theorem (Exact `Z_3` doublet-block location of the remaining microscopic
datum).** Assume the exact post-canonical positive-polar section, the exact
singlet-doublet CP-slot tool, the exact intrinsic-slot theorem, and the exact
active affine point-selection boundary theorem. Then on the live
source-oriented sheet the intrinsic `Z_3` kernel already has exact constant
singlet-doublet slots `K01 = a_*`, `K02 = b_*`, while the remaining affine
datum appears entirely in the doublet block by the exact formulas above.
Therefore, after quotienting the spectator line `m`, the minimal remaining
mainline object is exactly the `2`-real `Z_3` doublet-block law for
`(delta, q_+)`.

## What this closes

This closes the microscopic location of the remaining datum.

The branch no longer needs to say only:

- “the missing object is the affine pair `(delta, q_+)`”

It can now say more sharply:

- the slots are already frozen,
- the remaining datum lives entirely in the `Z_3` doublet block,
- the missing law is exactly the `2`-real `Z_3` doublet-block law.

## What this does not close

This note still does **not** derive the post-canonical microscopic law that
selects that `Z_3` doublet-block pair.

It identifies only where the last datum lives and how to read it exactly.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py
```
