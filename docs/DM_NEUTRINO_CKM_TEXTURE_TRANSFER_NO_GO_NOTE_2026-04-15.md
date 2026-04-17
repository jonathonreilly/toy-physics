# DM Neutrino CKM Texture Transfer No-Go

**Date:** 2026-04-15  
**Status:** exact no-transfer theorem for the current CKM/NNI atlas tools on
the universal Dirac bridge  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_ckm_texture_transfer_nogo.py`

## Question

Can the current flavor atlas tools on `main`:

- CKM from mass hierarchy
- CKM Schur-complement theorem
- CKM mass-basis NNI route
- Jarlskog phase companion

be transplanted directly onto the exact universal neutrino Dirac bridge

`Y = y_0 I`

to derive the non-universal neutrino Dirac flavor texture needed for
leptogenesis?

## Bottom line

No on the current stack.

The current exact DM Dirac bridge is universal. After any unitary left/right
basis changes,

`Y' = U_L^dag (y_0 I) U_R`,

the Hermitian kernel remains

`Y'^dag Y' = y_0^2 I`,

and the singular-value spectrum remains exactly triple-degenerate:

`(y_0, y_0, y_0)`.

That kills the present CKM/NNI transfer routes one by one:

1. **Mass-hierarchy / GST transfer fails.** There is no singular-value
   hierarchy to feed the GST relations; all ratios are exactly `1`.
2. **Mass-basis NNI transfer fails.** The CKM mass-basis suppression factors
   `sqrt(m_i/m_j)` all collapse to `1`, so the normalization map becomes the
   identity.
3. **Schur-complement transfer fails.** The Schur identity
   `c_13 = c_12 c_23` can still hold algebraically on a degenerate seed, but
   it no longer generates the Wolfenstein-style hierarchy because the mass-basis
   suppression factors are trivial.
4. **Phase-only transfer fails.** `Z_3`/Jarlskog phase insertions do not make
   `Y^dag Y` non-diagonal, so the leptogenesis CP tensor still vanishes.

So the current CKM/NNI atlas tools are useful analogies, not a current
theorem-grade neutrino texture derivation.

## Inputs

This note combines:

- [DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md](./DM_LEPTOGENESIS_UNIVERSAL_YUKAWA_NO_GO_NOTE_2026-04-15.md)
- [CKM_FROM_MASS_HIERARCHY_NOTE.md](./CKM_FROM_MASS_HIERARCHY_NOTE.md)
- [CKM_SCHUR_COMPLEMENT_THEOREM.md](./CKM_SCHUR_COMPLEMENT_THEOREM.md)
- [CKM_MASS_BASIS_NNI_NOTE.md](./CKM_MASS_BASIS_NNI_NOTE.md)
- [JARLSKOG_PHASE_BOUND_NOTE.md](./JARLSKOG_PHASE_BOUND_NOTE.md)

The DM note already proves the exact universal bridge by itself gives zero
leptogenesis CP tensor. The flavor notes define the strongest current CKM/NNI
atlas mechanisms that might look transplantable.

## Exact theorem

### 1. Unitary transfer preserves the universal Hermitian kernel

If

`Y = y_0 I`,

then for any unitary `U_L`, `U_R`,

`Y' = U_L^dag Y U_R`

still satisfies

`Y'^dag Y' = y_0^2 I`.

So the Hermitian leptogenesis kernel stays exactly diagonal.

### 2. The singular spectrum stays triple-degenerate

Because `Y'` is a scalar times a unitary, its singular values are exactly

`s_1 = s_2 = s_3 = y_0`.

So the current DM Dirac bridge carries no intrinsic flavor hierarchy on this
surface.

### 3. The mass-hierarchy / GST route collapses

The CKM mass-hierarchy row needs nontrivial ratios like

`sqrt(m_1/m_2)`, `sqrt(m_2/m_3)`, `sqrt(m_1/m_3)`.

On the universal Dirac bridge these become

`sqrt(s_1/s_2) = sqrt(s_2/s_3) = sqrt(s_1/s_3) = 1`.

So the GST hierarchy machinery has no nontrivial small parameter to work with.

### 4. The mass-basis NNI route collapses

The CKM mass-basis route uses

`c_ij^phys = c_ij^geom * sqrt(m_i/m_j)`.

On the universal Dirac bridge all those factors are exactly `1`, so

`c_ij^phys = c_ij^geom`.

The decisive quark-side hierarchy improvement therefore disappears.

### 5. The Schur-complement route does not rescue the hierarchy

The Schur-complement identity

`c_13 = c_12 c_23`

can still hold algebraically on a degenerate seed, but with all mass-basis
factors equal to `1` it only reorganizes `O(1)` coefficients. It does not
generate the `lambda`, `A lambda^2`, `A lambda^3` suppression chain.

### 6. The phase-only companion does not rescue the CP kernel

Phase insertions can change `Y'` itself, but not the exact kernel

`Y'^dag Y' = y_0^2 I`.

So the standard leptogenesis tensor still obeys

`Im[(Y'^dag Y')_{1j}^2] = 0`.

## The theorem-level statement

**Theorem (CKM/NNI no-transfer on the universal Dirac bridge).**
On the current DM denominator surface, where the exact Dirac neutrino Yukawa is
still the universal bridge `Y = y_0 I`, the present CKM/NNI atlas tools do not
transfer to a theorem-grade non-universal neutrino Dirac texture. Unitary basis
changes preserve `Y^dag Y = y_0^2 I`, the singular spectrum remains
triple-degenerate, the CKM mass-hierarchy and mass-basis-normalization tools
collapse to trivial identities, and phase-only companions leave the
leptogenesis CP tensor identically zero.

## What this closes

This closes an honest escape hatch:

- the branch should no longer treat the current CKM/NNI atlas rows as a live
  near-term source of the missing neutrino Dirac flavor texture

## What this does not close

This note does **not** prove the needed non-universal texture is impossible in
principle.

It leaves open:

- a future exact neutrino-side flavor-breaking mechanism
- a future non-universal Dirac operator family beyond the current universal
  bridge
- a future exact local-to-generation map that is not just a CKM/NNI transplant

## Safe wording

**Can claim**

- the current CKM/NNI atlas tools do not transfer to the universal neutrino
  Dirac bridge
- the remaining DM denominator blocker is not "reuse CKM flavor machinery as
  is"

**Cannot claim**

- that no exact neutrino flavor texture can ever be derived
- that the framework can never produce non-universal Dirac structure

## Command

```bash
python3 scripts/frontier_dm_neutrino_ckm_texture_transfer_nogo.py
```
