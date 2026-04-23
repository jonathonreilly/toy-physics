# DM Neutrino CP-Kernel Deformation Necessity

**Date:** 2026-04-15
**Status:** exact necessary-condition theorem for the missing Dirac texture
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_cp_kernel_deformation_necessity.py`

## Question

Once the branch already knows:

- the exact universal Dirac bridge by itself gives zero leptogenesis
- the current CKM/NNI flavor atlas does not transfer to that bridge

what exact kind of new Dirac-side structure is still necessary before the
standard leptogenesis CP tensor can become nonzero?

## Bottom line

The missing object is sharper than just "some non-universal Yukawa texture."

Two tempting classes still fail:

1. **Pure unitary mismatch fails.** If the new structure is only another
   left/right basis rotation of `Y = y_0 I`, then `Y^dag Y` remains
   `y_0^2 I`.
2. **Pure diagonal non-universality fails.** If the new structure is only a
   diagonal singular-value split, then `Y^dag Y` remains diagonal and the
   standard CP tensor still vanishes.

So any successful exact texture must do more than either of those. It must
produce genuinely non-diagonal Hermitian kernel entries in

`H = Y^dag Y`.

Equivalently: the missing texture must be a **non-unitary off-diagonal
flavor-breaking deformation** beyond the current universal bridge.

## Inputs

This note combines:

- [DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md](./DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md)
- [DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15.md](./DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15.md)

The first note proves the current universal bridge gives zero CP tensor. The
second proves the current CKM/NNI atlas tools do not transplant to fix that.
So the remaining honest question is the minimal necessary shape of any future
successful deformation.

## Exact theorem

### 1. Pure unitary mismatch is insufficient

For

`Y = y_0 I`

and any unitary `U_L`, `U_R`,

`Y' = U_L^dag Y U_R`

still obeys

`Y'^dag Y' = y_0^2 I`.

So pure basis mismatch never creates the needed CP kernel.

### 2. Pure diagonal non-universality is insufficient

If instead

`Y = y_0 diag(a_1, a_2, a_3)`,

then

`Y^dag Y = y_0^2 diag(|a_1|^2, |a_2|^2, |a_3|^2)`

is still diagonal.

So diagonal singular-value splitting alone does not create the off-diagonal
entries needed for

`Im[(Y^dag Y)_{1j}^2] != 0`.

### 3. A nonzero CP tensor requires non-diagonal Hermitian kernel entries

The standard leptogenesis source is built from the off-diagonal entries of

`H = Y^dag Y`.

Therefore a necessary condition for nonzero asymmetry is:

- `H` must acquire off-diagonal entries
- at least one relevant off-diagonal entry must have a phase structure such
  that `Im[(H_{1j})^2] != 0`

That cannot happen on the current universal bridge, and it cannot happen from
pure basis mismatch or diagonal rescaling alone.

## The theorem-level statement

**Theorem (Necessary deformation class for a nonzero DM leptogenesis kernel).**
On the current DM denominator surface, any successful exact neutrino Dirac
texture must induce genuinely non-diagonal Hermitian kernel entries in
`H = Y^dag Y`. Pure unitary basis mismatch and pure diagonal non-universal
rescaling are both insufficient. Therefore the missing structure must be a
non-unitary off-diagonal flavor-breaking deformation beyond the current
universal bridge.

## What this closes

This closes two more fake rescue paths:

- "maybe another basis choice is enough"
- "maybe diagonal Yukawa splitting is enough"

Neither is enough.

## What this does not close

This note does **not** derive the needed deformation from the axiom surface.

It only sharpens the target:

- the missing object must be off-diagonal in flavor space at the level of
  `Y^dag Y`
- and it must be non-unitary, not just a basis change

## Safe wording

**Can claim**

- the remaining DM flavor blocker is now sharper than a vague "non-universal
  texture" request
- any successful future texture must be a non-unitary off-diagonal
  flavor-breaking deformation

**Cannot claim**

- that the framework already derives that deformation
- that every conceivable non-universal texture is already classified

## Command

```bash
python3 scripts/frontier_dm_neutrino_cp_kernel_deformation_necessity.py
```
