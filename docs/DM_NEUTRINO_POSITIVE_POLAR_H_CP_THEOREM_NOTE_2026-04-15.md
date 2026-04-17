# DM Neutrino Positive-Polar Hermitian CP Theorem

**Date:** 2026-04-15  
**Status:** exact Hermitian-data theorem for the intrinsic DM CP tensor  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_positive_polar_h_cp_theorem.py`

## Question

Once the post-canonical DM bridge is made intrinsic from

`H = Y Y^dag`

by the positive polar section, can the physical heavy-neutrino-basis CP tensor
be written exactly on the active seven-coordinate Hermitian grammar?

## Bottom line

Yes.

On the canonical active Hermitian grammar

```text
H =
[ d1              r12               r31 e^{-i phi} ]
[ r12             d2                r23            ]
[ r31 e^{i phi}   r23               d3             ]
```

the intrinsic positive-section CP tensor is exactly

- `Im[(K_mass)01^2] = -r31 (d2-d3+r12-r31 cos(phi)) sin(phi) / 3`
- `Im[(K_mass)02^2] =  r31 (2 d1-d2-d3+r12-2 r23+r31 cos(phi)) sin(phi) / 3`

So the remaining DM object is now formula-level precise on `H` itself. It is
no longer a vague request to “break the aligned core somehow.”

## Inputs

This note sharpens:

- [DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POLAR_ALIGNED_CORE_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_POLAR_ALIGNED_CORE_NO_GO_NOTE_2026-04-15.md)

The positive-polar-section note makes the bridge intrinsic from `H`. This note
computes that bridge exactly on the active Hermitian grammar.

## Exact formula

Let

`K_Z3(H) = U_Z3^dag H U_Z3`

and

`K_mass(H) = R^T K_Z3(H) R`

with the exact real Majorana doublet rotation `R`.

Direct algebra on the seven-coordinate Hermitian grammar gives:

- `Im[(K_mass(H))01^2] = -r31 (d2-d3+r12-r31 cos(phi)) sin(phi) / 3`
- `Im[(K_mass(H))02^2] =  r31 (2 d1-d2-d3+r12-2 r23+r31 cos(phi)) sin(phi) / 3`

So the intrinsic positive-section DM tensor depends on:

1. the phase slot `phi`
2. the two real coefficient combinations
   - `B1 = d2-d3+r12-r31 cos(phi)`
   - `B2 = 2 d1-d2-d3+r12-2 r23+r31 cos(phi)`.

## Aligned-core corollary

On the exact residual-`Z_2` aligned core

- `d2 = d3`
- `r12 = r31`
- `phi = 0`

the formula gives

- `Im[(K_mass)01^2] = 0`
- `Im[(K_mass)02^2] = 0`

So the earlier aligned-core no-go is now an exact corollary of the Hermitian
CP formula.

## The theorem-level statement

**Theorem (Exact positive-polar DM CP tensor on the active Hermitian grammar).**
Assume the exact DM post-canonical positive-polar-section theorem and the
active Hermitian grammar

`H = [[d1,r12,r31 e^{-i phi}],[r12,d2,r23],[r31 e^{i phi},r23,d3]]`.

Then the intrinsic heavy-neutrino-basis CP tensor is exactly

- `Im[(K_mass)01^2] = -r31 (d2-d3+r12-r31 cos(phi)) sin(phi) / 3`
- `Im[(K_mass)02^2] =  r31 (2 d1-d2-d3+r12-2 r23+r31 cos(phi)) sin(phi) / 3`.

Therefore the remaining DM denominator object is the exact `H`-side law for
`phi`, `B1`, and `B2`, not an unspecified right-frame quantity.

## What this closes

This closes the last vague wording around the new Hermitian-data endpoint.

It is now exact that:

- the right-frame blocker is gone on the generic full-rank patch
- the aligned-core no-go is a direct corollary of the Hermitian formula
- the remaining DM object is the exact `H`-side phase/breaking law

## What this does not close

This note does **not** derive the actual branch values of

- `phi`
- `B1`
- `B2`.

It tells us exactly what must now be derived.

## Command

```bash
python3 scripts/frontier_dm_neutrino_positive_polar_h_cp_theorem.py
```
