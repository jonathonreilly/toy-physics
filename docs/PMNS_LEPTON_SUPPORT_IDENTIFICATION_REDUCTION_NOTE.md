# PMNS Lepton Support Identification Reduction

**Date:** 2026-04-15  
**Status:** exact reduction theorem on the remaining PMNS derivation target  
**Script:** `scripts/frontier_pmns_lepton_support_identification_reduction.py`

## Question

After the Schur/source-law reduction, the remaining target was:

- derive the effective lepton blocks
- derive one active probe direction

Is the block-identification part really still a support-selection problem?

Or does the retained matter/generation closure already identify the lepton
supports, leaving only the effective operator law on those fixed supports?

## Bottom line

The lepton supports are already identified.

Combining:

- one-generation matter closure
- retained three-generation matter structure

the framework already fixes the lepton family support pair

- `E_nu = span{nu_0, nu_1, nu_2}`
- `E_e  = span{e_0,  e_1,  e_2}`.

So the remaining PMNS object is **not**:

- discover which support subspaces carry the neutrino and charged-lepton data

It is:

- derive the effective operators on those already fixed supports.

Combined with the canonical sheet-probe reduction, the independent remaining
target is therefore just:

- derive the effective lepton operators / Hermitian blocks on
  `E_nu` and `E_e`.

## Exact reduction

### 1. Species labels already fix the lepton channels

The retained one-generation matter closure already distinguishes the two lepton
species:

- `nu`
- `e`

So the PMNS lane does not have to solve a species-identification problem from
scratch.

### 2. Generation closure already lifts each lepton species to a triplet

The retained three-generation matter structure already fixes the physical
triplet reading of the generation sectors.

Therefore each lepton species already carries a canonical three-dimensional
generation support:

- `nu_0, nu_1, nu_2`
- `e_0,  e_1,  e_2`.

### 3. What remains is operator-valued

Once the support projectors onto `E_nu` and `E_e` are fixed, different
effective finite operators simply give different block values on the same
supports.

So the remaining freedom is operator-valued:

- `L_nu`
- `L_e`

not support-valued.

## Theorem-level statement

**Theorem (Lepton support identification reduction).** Assume the retained
one-generation matter closure and the retained three-generation matter
structure. Then:

1. the lepton family support pair is already fixed as
   `E_nu ⊕ E_e = span{nu_0,nu_1,nu_2} ⊕ span{e_0,e_1,e_2}`
2. any remaining PMNS freedom on the effective finite Gaussian is operator-
   valued on those fixed supports rather than support-valued
3. combined with the canonical sheet-probe reduction, the independent
   remaining PMNS target is to derive the effective lepton operators on those
   fixed supports

Therefore the remaining PMNS derivation target is not support selection. It is
the effective block law on the already-identified lepton supports.

## What this closes

This closes the support-identification loophole.

The remaining independent target is no longer:

- identify the lepton blocks
- derive a separate probe direction

It is:

- derive the effective lepton operators / Hermitian blocks on `E_nu` and `E_e`

because the supports are already fixed and the sheet-reading probe is already
a downstream construction from the active block.

## What this does not close

This note does **not** derive the effective operators themselves from
`Cl(3)` on `Z^3`.

It sharpens the remaining target to its cleanest exact form.

## Command

```bash
python3 scripts/frontier_pmns_lepton_support_identification_reduction.py
```
