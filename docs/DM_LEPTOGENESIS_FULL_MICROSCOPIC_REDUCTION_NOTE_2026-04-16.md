# DM Leptogenesis Full Microscopic Reduction

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_full_microscopic_reduction.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact final reduction theorem for the PMNS-assisted flavored DM route on the
refreshed branch.

## Question

After the PMNS projector-interface theorem, active-block reduction, exact
flavored selector, `N_e` projected-source-law derivation, and charged
source-response reduction, what is the smallest remaining science object on the
PMNS-assisted DM repair route?

## Bottom line

It is the actual microscopic charge-preserving operator `D`.

The exact chain is now:

`D`
`-> D_-`
`-> dW_e^H`
`-> H_e`
`-> |U_e|^2^T`
`->` selected transport column
`-> eta`

So once the full microscopic charge-preserving operator `D` is supplied, the
PMNS-assisted near-closing DM value is algorithmic.

This means the old “derive the PMNS source” phrasing is no longer the clean
remaining target. The remaining target is the actual microscopic value law of
`D` from `Cl(3)` on `Z^3`.

## Exact result

On the canonical charged-lepton-active sample used by the PMNS-assisted DM
lane:

- from full `D`, the charge-`-1` sector `D_-` is extracted canonically
- `dW_e^H` factors exactly through the Schur value `L_e = Schur_{E_e}(D_-)`
- `L_e` reproduces the canonical charged-lepton Hermitian block `H_e`
- `H_e` gives the exact `N_e` packet
- the exact DM flavored selector chooses the same middle near-closing column

So the PMNS-assisted route is no longer blocked on:

- projector construction
- column selection
- PMNS pair reconstruction
- charged Hermitian source response reduction

It is blocked only on:

- the actual full microscopic operator values of `D`

## Numerical comparison to the old `5.3x` miss

Exact theorem-native one-flavor branch:

- `eta/eta_obs = 0.188785929502`
- miss factor `eta_obs/eta = 5.297004933778`

Full-`D` PMNS-assisted route:

- `eta/eta_obs = 0.989512704600`
- miss factor `eta_obs/eta = 1.010598444417`

So the PMNS-assisted full-microscopic route reduces the old miss by a factor
of about

- `5.241453678303`

and leaves only a residual

- `1.04872954%`

low.

## Consequence

The PMNS-assisted DM route is now reduced as far as it can honestly go without
deriving the full microscopic operator values themselves.

The remaining exact target is:

- the actual microscopic value law of the full charge-preserving operator `D`
  from `Cl(3)` on `Z^3`

not:

- a new transport law
- a new PMNS carrier
- a new flavored column theorem
- a new charged-Hermitian reduction

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_full_microscopic_reduction.py
```
