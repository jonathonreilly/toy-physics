# Exact `Z_3` Texture-Factor Theorem

**Date:** 2026-04-15
**Status:** exact positive overlap theorem on the retained `Z_3` basis bridge
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_z3_texture_factor_theorem.py`

## Question

Is the `1/3` texture factor used in the reduced leptogenesis estimate only a
heuristic, or is it exact on the retained `Z_3` basis bridge?

## Bottom line

It is exact on that bridge.

The canonical `Z_3` basis-change matrix is the `3 x 3` discrete Fourier
transform

`U_Z3 = (1/sqrt(3)) [[1,1,1],[1,omega,omega^2],[1,omega^2,omega]]`.

Every entry has modulus `1/sqrt(3)`, so every overlap square between a
`Z_3` charge eigenstate and a flavor/site basis vector is exactly

`1/3`.

Therefore the reduced leptogenesis texture factor is not a fitted or
heuristic coefficient on the retained `Z_3` bridge.

## Inputs

This note reuses:

- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)
- [NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md)

Those notes already retain:

1. the three-generation matter structure
2. the `Z_3` singlet + doublet decomposition
3. the standard `Z_3` basis bridge between the flavor/site basis and the
   charge-eigenstate basis

So the only remaining honest question is whether that bridge gives a uniform
overlap weight or not.

## Exact theorem

### 1. The `Z_3` bridge is the discrete Fourier transform

The canonical basis bridge is

`U_Z3 = (1/sqrt(3)) F_3`,

with the usual cube-root phases `{1, omega, omega^2}`.

### 2. Every entry has the same modulus

Because each entry differs only by a unit complex phase,

`| (U_Z3)_{ij} | = 1/sqrt(3)`

for all `i,j`.

So

`| (U_Z3)_{ij} |^2 = 1/3`

for all `i,j`.

### 3. The reduced texture factor is exact

Any reduced estimate that uses the overlap square between one retained `Z_3`
mode and one flavor/site basis direction therefore picks up the exact factor

`1/3`.

## The theorem-level statement

**Theorem (Exact democratic `Z_3` texture factor on the retained bridge).**
On the canonical `Z_3` basis bridge, every overlap square between a
generation-charge eigenstate and a flavor/site basis vector is exactly `1/3`.
Therefore the `1/3` factor in the reduced leptogenesis estimate is exact on
that bridge.

## What this closes

This closes one real denominator-side placeholder:

- the reduced `1/3` texture factor no longer needs to be treated as a rough
  approximation on the retained `Z_3` bridge

## What this does not close

This note still does **not** derive:

- the full CP-asymmetry tensor `Im[(Y^\dagger Y)_{1j}^2]`
- the exact relative sign/interference between the `N_2` and `N_3`
  contributions
- full PMNS closure

So the remaining blocker moves downstream to the CP-asymmetry kernel itself.

## Safe wording

**Can claim**

- the `1/3` texture factor is exact on the retained `Z_3` basis bridge
- the reduced leptogenesis estimate no longer needs to treat that factor as a
  fit or a heuristic

**Cannot claim**

- that the full `epsilon_1` tensor is already derived
- that all leptogenesis approximations are gone

## Command

```bash
python3 scripts/frontier_dm_z3_texture_factor_theorem.py
```
