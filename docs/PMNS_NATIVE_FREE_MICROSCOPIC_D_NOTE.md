# PMNS Native Free Microscopic `D` Law

**Date:** 2026-04-15  
**Status:** exact native-free theorem  
**Script:** `scripts/frontier_pmns_native_free_microscopic_d.py`

## Question

Before any Higgs / electroweak-breaking deformation is added, what does the
native `Cl(3)` on `Z^3` construction itself give for the PMNS-relevant
microscopic lepton operator?

## Bottom line

It is trivial.

On the exact native free surface:

1. the three generations are the exact `hw=1` Brillouin-corner modes
2. exact lattice translation invariance makes the free generation operator
   diagonal in that corner basis
3. exact `hw=1` degeneracy makes that diagonal operator scalar
4. unbroken weak `SU(2)` makes the neutrino/electron fiber block scalar

Therefore the fully derived native free microscopic operator on the retained
lepton surface is

`D_free|_{E_nu ⊕ E_e} = I_6`

in the normalized units used on the generation lane, equivalently

- `D_0^{trip,free} = I_3`
- `D_-^{trip,free} = I_3`.

## Exact chain

### 1. Generation basis

The retained three-generation surface is the exact `hw=1` corner triplet:

- `(pi,0,0)`
- `(0,pi,0)`
- `(0,0,pi)`.

These carry distinct lattice momenta, hence distinct translation characters.

### 2. Translation invariance

Any native free microscopic operator commutes with lattice translations.

In the exact corner basis, translations are diagonal. So for any two distinct
corner characters `lambda_i != lambda_j`,

`(lambda_i - lambda_j) M_ij = 0`,

hence the free generation operator has no off-diagonal entries.

### 3. `hw=1` degeneracy

The normalized free energy of each `hw=1` corner is exactly the same:

`m_* = 1`.

So the diagonal generation operator is not merely diagonal but scalar:

`m_* I_3 = I_3`.

### 4. Weak doublet scalarity

Before EWSB, the lepton fiber is an unbroken weak doublet. Any free lepton
operator commuting with the weak `su(2)` must be scalar on that `2`-dimensional
fiber.

So the same scalar triplet operator appears on both `E_nu` and `E_e`.

## Consequence

The native free microscopic core is already fully derived, and it does **not**
carry PMNS structure.

Therefore the remaining PMNS science is exactly:

- derive the deformation away from the native free core

rather than:

- derive the native free core itself.

## Boundary

This note identifies the fully derived native free microscopic operator only.

It does **not** derive the Higgs/EWSB deformation that would move the operator
away from the trivial identity core and produce nontrivial masses and mixing.

## Command

```bash
python3 scripts/frontier_pmns_native_free_microscopic_d.py
```
