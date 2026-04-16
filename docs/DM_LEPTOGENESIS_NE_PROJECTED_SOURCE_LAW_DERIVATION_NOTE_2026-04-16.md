# DM Leptogenesis `N_e` Projected-Source-Law Derivation

**Date:** 2026-04-16  
**Branch:** `codex/dm-main-refresh`  
**Script:** `scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Status

Exact positive derivation transplant from the PMNS microscopic source-response
lane onto the refreshed DM branch.

This note upgrades the flavored-PMNS DM reduction.

The earlier DM reduction said the remaining PMNS-side object was the active
five-real source. That was true if one only used:

- branch/orientation,
- seed averages,
- support pattern,
- and the exact transport selector.

But the PMNS microscopic source-response theorem is stronger than that.

## Question

On the charged-lepton-active branch `N_e`, what is the smallest PMNS-side
object actually needed to derive the transport-relevant flavored DM column?

Do we still need the full active five-real source

`(xi_1, xi_2, eta_1, eta_2, delta)`?

Or is there a smaller exact source-response object that already determines the
relevant column?

## Bottom line

There is a smaller exact object.

On `N_e`, the selected transport column is derivable from the charged-lepton
projected Hermitian source law alone:

`dW_e^H`.

The logic is exact:

1. `dW_e^H` reconstructs the active charged-lepton Hermitian block `H_e`
2. on `N_e`, the PMNS packet is exactly `|U_e|^2^T`
3. the exact DM transport selector `F_K` acts on the three packet columns
4. therefore the selected flavored transport column is algorithmic once
   `dW_e^H` is known

So for the PMNS-assisted DM repair route, we do **not** need the raw active
five-real source as the final target.

We need the projected Hermitian charged-lepton source law.

## Exact reduction

### 1. Projected Hermitian source pack determines `H_e`

For a `3 x 3` Hermitian block, the nine real linear responses

`X -> Re Tr(X H_e)`

on the standard Hermitian basis determine `H_e` exactly.

So the charged-lepton projected Hermitian source law `dW_e^H` fixes `H_e`
exactly.

### 2. `H_e` determines the `N_e` packet

On the one-sided charged-lepton-active branch, the passive side is monomial and
contributes only ordering/permutation data already fixed elsewhere.

Therefore the active packet is exactly

`|U_PMNS|^2 = |U_e|^2^T`.

So `H_e` alone determines the `N_e` packet.

### 3. The exact transport selector determines the column

The DM branch already has the exact one-source flavored selector

`F_K(P) = Σ_alpha Psi_K(P_alpha)`.

Applying this to the three columns of the `N_e` packet selects the relevant
column exactly.

On the canonical `N_e` sample, this reproduces the same near-closing value:

`eta/eta_obs = 0.989512597197`.

## Consequence

This changes the honest last-mile PMNS/DM target.

What is no longer the right final target:

- the raw active five-real source law

What is now the right final target:

- the charged-lepton projected Hermitian source law `dW_e^H`

because once `dW_e^H` is known:

- `H_e` is known
- the `N_e` packet is known
- the transport-relevant column is known

So the remaining PMNS contribution to the DM flavored-repair route is smaller
and more source-response-native than the earlier five-real formulation.

## What this closes

This closes the target-shape question on the PMNS-assisted DM lane more tightly
than the previous active-projector reduction.

The flavored `N_e` repair path no longer needs a theorem for the raw PMNS
corner-source coordinates as such. It needs the projected charged-lepton
Hermitian source law.

## What this does not close

This note does **not** yet evaluate `dW_e^H` from `Cl(3)` on `Z^3`.

It proves only that once `dW_e^H` is available, the selected `N_e` transport
column and the near-closing DM flavored value are both downstream algorithmic.

So the live remaining gap is now:

- derive `dW_e^H` on `E_e` from `Cl(3)` on `Z^3`

not:

- derive the full active five-real PMNS source law.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py
```
