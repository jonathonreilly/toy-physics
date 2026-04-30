# DM Neutrino Triplet Character-Source Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_triplet_character_source_theorem.py`

## Question

Once the exact weak-only `Z_3` source phase is transferred onto the canonical
active neutrino branch, where does the nontrivial character enter the DM
Hermitian carrier?

## Bottom line

Uniquely through `gamma`.

Under character conjugation `phi -> -phi`, the Hermitian law splits as:

- odd part: `H_odd = gamma T_gamma`
- even part: `H_even = H_core + delta T_delta + rho T_rho`

So the nontrivial weak `Z_3` character lands exactly on the CP-odd triplet slot
`gamma`. The remaining triplet/core data are character-even response data.

## Why this matters

This closes the **direction** part of the missing law.

The branch no longer has to say only:

- “there is some missing triplet law”

It can now say:

- the source-direction part is exact
- the weak character enters the Hermitian carrier only through `gamma`
- what remains is the even response sector and its normalization

## What this does not close

This note does **not** derive the magnitude of `gamma`, `delta`, or `rho`.

It only fixes the source-direction map:

`weak Z_3 character -> gamma T_gamma`.

## Command

```bash
python3 scripts/frontier_dm_neutrino_triplet_character_source_theorem.py
```
