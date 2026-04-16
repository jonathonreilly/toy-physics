# DM Neutrino `K00` Bosonic Normalization Theorem

**Date:** 2026-04-15  
**Status:** exact diagonal-normalization theorem on the refreshed `main`-derived DM lane  
**Script:** `scripts/frontier_dm_neutrino_k00_bosonic_normalization_theorem.py`

## Framework sentence

In this note, "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

Once the exact source package is closed, can the remaining heavy-neutrino-basis
diagonal normalization

`K00 = (K_mass)00`

be fixed canonically from the same single-axiom source-response machinery?

## Bottom line

Yes.

The target functional `K00` has exact Frobenius-dual generator

`F00 = J3/3`

with `J3` the `3 x 3` all-ones matrix. On the source side, the exact swap-even
weak mode `tau_+ = tau_E + tau_T` lives on the row-sum generator

`J2 = [[1,1],[1,1]]`.

Since `F00` is isospectral to `(1/2) J2`, the unique additive CPT-even bosonic
observable fixes the coefficient law

`K00 = 2 tau_+`.

On the exact source-oriented branch,

- `tau_E = 1/2`
- `tau_T = 1/2`
- `tau_+ = 1`

so the exact heavy-basis diagonal normalization is

`K00 = 2`.

## Exact target formula

On the exact breaking-triplet decomposition

`H = H_core + B(delta,rho,gamma)`

with

`H_core = [[A,b,b],[b,c,d],[b,d,c]]`

and

`B = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`,

the transformed heavy-basis diagonal is

`K00 = (K_mass)00 = (A + 4b + 2c + 2d)/3`.

Equivalently,

`K00 = Tr(H F00),  F00 = J3/3`.

So `K00` is independent of the odd/even breaking triplet
`(delta,rho,gamma)` and depends only on the aligned core.

## Bosonic normalization argument

The exact source-side even mode is not the projector `(1/2) J2`; it is the
full row-sum generator `J2` with amplitude `tau_+`.

The bosonic observable principle compares exact source-deformed responses

`W[J] = log|det(D+J)| - log|det D|`.

Since `F00` and `(1/2) J2` have the same nonzero spectrum `{+1}`, they have
identical exact bosonic response on scalar baselines. Therefore the target
coefficient must compensate the factor of `2` between `J2` and `(1/2) J2`,
forcing

`K00 = 2 tau_+`.

## Consequence

This closes the diagonal normalization that the exact-source diagnostic left
open.

The refreshed branch no longer has:

- open odd transfer coefficient
- open even transfer vector
- open source amplitudes
- open heavy-basis diagonal normalization

At this point the exact source-side package is

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`
- `K00 = 2`

which is the full exact kernel input for the standard coherent leptogenesis
sum on the retained benchmark.

## Command

```bash
python3 scripts/frontier_dm_neutrino_k00_bosonic_normalization_theorem.py
```
