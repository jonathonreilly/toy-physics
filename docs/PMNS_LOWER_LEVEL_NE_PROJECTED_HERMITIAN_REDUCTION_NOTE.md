# PMNS Lower-Level `N_e` Projected-Hermitian Reduction

**Date:** 2026-04-16  
**Status:** exact lower-level interface reduction theorem  
**Script:** `scripts/frontier_pmns_lower_level_ne_projected_hermitian_reduction.py`

## Question

On the charged-lepton-active `N_e` lane, what exactly survives from the new
lower-level PMNS theorems into the transport-facing DM/leptogenesis interface?

## Bottom line

Once the lower-level effective active/passive blocks are fixed, the
transport-facing projected Hermitian source object is already fixed exactly.

The logic is now:

- the partition-response theorem makes the lower-level response pack native
  once the lower-level baselines are fixed
- the Schur-pushforward theorem shows microscopic sector completions are
  quotient data on PMNS support
- the lower-level end-to-end closure then fixes the active Hermitian slot
  exactly on `N_e`
- the projected Hermitian source pack reconstructs that active Hermitian slot
  exactly
- the `N_e` transport packet is then exactly `|U_active|^2^T`

So the lower-level PMNS lane now reaches the same transport-facing object as
the DM `dW_e^H` reduction without any extra PMNS-side ansatz.

On the current lower-level pair convention, this active Hermitian slot is
stored as `H_nu` on the charged-lepton-active branch, while `H_e` stores the
passive monomial block.

## Exact theorem

On the canonical charged-lepton-active `N_e` sample:

- lower-level closure recovers the canonical active/passive Hermitian slots
  exactly
- two distinct microscopic completions with the same effective active/passive
  blocks give the same active Hermitian slot
- the nine projected Hermitian responses reconstruct that active slot exactly
- those projected Hermitian responses are identical across microscopic
  completions
- the derived transport packet is completion-invariant and matches the
  canonical `N_e` packet
- the selected column still gives
  `eta/eta_obs = 0.989512597197`

So on `N_e`, the exact chain

`effective blocks -> lower-level response pack -> active Hermitian slot -> projected Hermitian source law -> |U_active|^2^T -> eta`

is already fixed once the effective blocks are fixed.

## What this closes

This removes two more fake open objects from the observation-free `N_e` lane:

- the lower-level response pack
- the microscopic sector completion

Neither is the live remaining gap anymore.

## What remains open

The live remaining `N_e` gap is now exactly:

> the effective active/passive block law, equivalently the exact active
> Hermitian source law from `Cl(3)` on `Z^3`

So the normalization lane no longer needs to be phrased as a response-pack or
microscopic-completion problem.

## Command

```bash
python3 scripts/frontier_pmns_lower_level_ne_projected_hermitian_reduction.py
```
