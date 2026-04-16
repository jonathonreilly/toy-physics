# DM Leptogenesis `N_e` Charged Source-Response Reduction

**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact source-response reduction theorem on the refreshed DM branch.

This note sharpens the PMNS-assisted flavored DM route one step further and
quantifies exactly how much of the old `5.3x` denominator miss survives once
the charged-lepton projected Hermitian source law is supplied.

## Question

After the PMNS projector-interface, active-block localization, exact flavored
column selector, and `N_e` projected-source-law derivation, what is the
smallest remaining PMNS-side object on the DM branch?

And numerically, how far off is the PMNS-assisted route compared with the old
exact one-flavor `5.3x` miss?

## Bottom line

The PMNS-assisted flavored DM route now reduces to one object:

- the charged-lepton projected Hermitian source law `dW_e^H`

More precisely:

1. `dW_e^H` is the exact charged-sector Schur pushforward of the microscopic
   charge-`-1` source-response law
2. `dW_e^H` reconstructs `H_e` exactly
3. on `N_e`, `H_e` determines the transport packet `|U_e|^2^T`
4. the exact DM transport selector then picks the relevant column algorithmically

So the old exact one-flavor miss

- `eta_obs / eta = 5.297004933778`

collapses, on the PMNS-assisted `dW_e^H`-conditioned route, to

- `eta_obs / eta = 1.010598444417`

which is only about

- `1.04872954%`

low.

## Exact reduction

### 1. `dW_e^H` is an exact charged-sector Schur pushforward

On the charge-preserving microscopic class,

`D = D_0 ⊕ D_- ⊕ D_+`.

A source supported on the charged-lepton support `E_e ⊂ E_-` factors exactly
through the charge-`-1` Schur complement

`L_e = Schur_{E_e}(D_-)`.

So `dW_e^H` is not an ad hoc PMNS data object. It is the charged-sector
microscopic source-response law on the retained support.

### 2. `dW_e^H` reconstructs `H_e`

The nine Hermitian linear responses on the charged support reconstruct `H_e`
exactly.

### 3. `H_e` determines the `N_e` packet

On the charged-lepton-active branch,

`|U_PMNS|^2 = |U_e|^2^T`.

So once `H_e` is known, the full `N_e` transport packet is already fixed.

### 4. Exact transport selects the column

The exact one-source flavored selector

`F_K(P) = Σ_alpha Psi_K(P_alpha)`

then selects the same middle column as before and gives

- `eta/eta_obs = 0.989512704600`

on the canonical `N_e` sample.

## Comparison to the old `5.3x` miss

The exact theorem-native one-flavor branch gave

- `eta/eta_obs = 0.188785929502`
- miss factor `eta_obs/eta = 5.297004933778`

The PMNS-assisted `dW_e^H`-conditioned route gives

- `eta/eta_obs = 0.989512704600`
- miss factor `eta_obs/eta = 1.010598444417`

So the PMNS-assisted improvement factor is

- `5.241453678302`

and the residual miss is only about

- `1.05%`.

## Consequence

This is the cleanest current statement of the PMNS-assisted DM repair route.

What is no longer the right target:

- the raw active five-real PMNS source
- the selected `N_e` column by itself
- any new transport ansatz

What is now the right target:

- evaluate the charged-lepton projected Hermitian source law `dW_e^H`
  from `Cl(3)` on `Z^3`

equivalently:

- evaluate the microscopic charge-`-1` operator `D_-` and its Schur pushforward

because once that is done, the remaining PMNS-assisted DM chain is already
algorithmic.

## What this does not close

This note does **not** yet evaluate `D_-` or `dW_e^H` from the sole axiom.

It proves only that once `dW_e^H` is supplied, the old `5.3x` miss is reduced
to a residual `1.01x` miss.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_charged_source_response_reduction.py
```
