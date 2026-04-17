# DM Neutrino Positive-Polar Aligned-Core No-Go

**Date:** 2026-04-15  
**Status:** exact Hermitian-core no-go after the positive-polar-section bridge  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_polar_aligned_core_nogo.py`

## Question

Once the generic full-rank post-canonical bridge is made intrinsic from

`H = Y Y^dag`

by the positive polar section, does the exact residual-`Z_2` aligned
Hermitian core already supply the needed DM CP support?

## Bottom line

No.

On the aligned active Hermitian core

```text
H_act =
[ a  b  b ]
[ b  c  d ]
[ b  d  c ]
```

the `Z_3`-basis singlet-doublet slots are exactly equal and real:

`(U_Z3^dag H_act U_Z3)_01 = (U_Z3^dag H_act U_Z3)_02 = (a+b-c-d)/3`.

So after the exact real Majorana doublet rotation:

- one physical singlet-doublet mass-basis entry vanishes exactly
- the other remains purely real

and therefore

- `Im[(K_mass)_01^2] = 0`
- `Im[(K_mass)_02^2] = 0`.

So the aligned Hermitian core is intrinsically CP-empty even on the positive
section.

## Inputs

This note combines:

- [DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md:1)

The PMNS note supplies the aligned active Hermitian core. This note evaluates
the DM post-canonical positive-section bridge on that exact core.

## Exact aligned-core law

If

```text
H_act =
[ a  b  b ]
[ b  c  d ]
[ b  d  c ],
```

then a direct `Z_3` transform gives

```text
K_Z3 = U_Z3^dag H_act U_Z3 =
[ (a+4b+2c+2d)/3      q                     q                   ]
[ q                   (a-2b+2c-d)/3        (a-2b-c+2d)/3       ]
[ q                   (a-2b-c+2d)/3        (a-2b+2c-d)/3       ]
```

with

`q = (a+b-c-d)/3`.

So the two singlet-doublet slot entries are equal and real.

After the exact real Majorana rotation,

- `(K_mass)_01 = 0`
- `(K_mass)_02 = sqrt(2) q in R`

and the standard leptogenesis tensor vanishes exactly.

## The theorem-level statement

**Theorem (Positive-section aligned-core no-go for DM CP support).**
Assume the exact DM post-canonical positive-polar-section theorem and the
exact residual-`Z_2` aligned active Hermitian core

`H_act = [[a,b,b],[b,c,d],[b,d,c]]`

with `a,b,c,d in R`. Then the intrinsic `Z_3`-basis singlet-doublet slot pair
is

`a_slot(H_act) = b_slot(H_act) = (a+b-c-d)/3 in R`.

Therefore after the exact real Majorana doublet rotation one physical
singlet-doublet mass-basis entry vanishes and the other is purely real, so the
heavy-neutrino-basis CP tensor vanishes:

`Im[(K_mass)_01^2] = Im[(K_mass)_02^2] = 0`.

So the aligned Hermitian core is intrinsically CP-empty on the positive
section.

## What this closes

This removes the last ambiguity left by the positive-section theorem.

It is now exact that:

- the raw right-frame blocker is gone on the generic full-rank patch
- but the residual-`Z_2` aligned Hermitian core still does **not** close DM
- the remaining blocker has moved fully onto the Hermitian-data side

The honest last-mile object is now:

> derive the Hermitian symmetry-breaking law away from the aligned core.

Equivalently, on the active seven-coordinate Hermitian grammar, derive the
three explicit breaking slots away from

- `d_2 = d_3`
- `r_12 = r_31`
- `phi = 0`.

## What this does not close

This note does **not** prove that the current branch is forced to stay on the
aligned core.

It proves only that:

- if the active Hermitian data remain on that exact aligned core,
- then the intrinsic positive-section DM bridge is still CP-empty.

So the remaining theorem target is now sharper than “derive the bridge”:

- derive the Hermitian symmetry-breaking slots, or
- prove the current stack cannot generate them.

## Command

```bash
python3 scripts/frontier_dm_neutrino_polar_aligned_core_nogo.py
```
