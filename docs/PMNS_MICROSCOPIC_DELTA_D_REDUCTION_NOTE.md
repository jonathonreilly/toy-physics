# PMNS Microscopic `ΔD` Reduction

**Date:** 2026-04-15  
**Status:** exact deformation-carrier reduction  
**Script:** `scripts/frontier_pmns_microscopic_delta_d_reduction.py`

## Question

Once the native free microscopic core is derived,

`D_free|_{E_nu ⊕ E_e} = I_6`,

what is the exact form of the remaining PMNS-relevant deformation

`ΔD = D - D_free`

on the retained triplet sectors?

## Bottom line

It is not a generic `3 x 3` perturbation.

On each retained triplet sector, the deformation lives in the exact
diagonal-circulant channel family

`ΔD = U + V C + W C^2`

with `U,V,W` diagonal and `C` the forward `3`-cycle.

So the remaining microscopic value law is not “all matrix entries.” It is only
the diagonal coefficient data on the three exact channels `I`, `C`, and `C^2`.

## Exact channel basis

Let

- `I` be the identity
- `C` the forward cyclic permutation
- `C^2` the backward cyclic permutation

Then the retained triplet operators already fit into:

- single-Higgs diagonal lane: `diag(a)`
- single-Higgs forward cyclic lane: `diag(a) C`
- single-Higgs backward cyclic lane: `diag(a) C^2`
- canonical two-Higgs lane: `A + B C`

So all retained triplet-sector operators lie in the same exact
diagonal-circulant carrier.

## Consequence for the deformation

Subtracting the native free core `I` gives:

- diagonal lane: `ΔD = (diag(a) - I)`
- forward cyclic lane: `ΔD = -I + diag(a) C`
- backward cyclic lane: `ΔD = -I + diag(a) C^2`
- canonical two-Higgs lane: `ΔD = (A - I) + B C`

Therefore `ΔD` is an affine diagonal-circulant deformation, not a generic
matrix perturbation.

## One-sided PMNS classes

On one-sided minimal PMNS classes:

- the active sector occupies the exact `I + C` subfamily
- the passive sector occupies exactly one of the three single-channel lanes

So once the branch is fixed, the full microscopic lepton deformation is reduced
to branch-conditioned diagonal channel data.

## Weak-axis seed patch

On the aligned weak-axis seed patch, the active operator is

- `x I + y C`

or its exchange sheet

- `y I + x C`.

So the deformation reduces further to a two-parameter slice plus one residual
sheet bit:

- `ΔD = (x-1) I + y C`
- or `ΔD = (y-1) I + x C`.

## What remains

This note does **not** derive the values of the diagonal channel coefficients
from `Cl(3)` on `Z^3`.

It proves the narrower exact statement:

> the remaining PMNS microscopic value law is exactly the value law of the
> diagonal channel coefficients on `I`, `C`, and `C^2`.

## Command

```bash
python3 scripts/frontier_pmns_microscopic_delta_d_reduction.py
```
