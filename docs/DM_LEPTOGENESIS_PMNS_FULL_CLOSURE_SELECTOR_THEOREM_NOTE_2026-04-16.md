# DM Leptogenesis PMNS Full-Closure Selector Theorem

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_full_closure_selector_theorem.py`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Question

After the relative-action stationarity theorem, one caveat still remained:

- the seed-relative bosonic action was already tied exactly to the sole-axiom
  observable principle
- the PMNS-assisted `N_e` closure source was already the unique
  **lowest-action branch** among sampled stationary closure branches

Could that last branch-global caveat now be removed on the refreshed DM
branch?

## Bottom line

Yes, on the current refreshed branch.

Broad multistart enumeration of exact closure starts on the fixed native `N_e`
seed surface yields two dominant stationary closure branches:

1. a low-action branch
2. a high-action branch

These are separated by a finite action gap.

Later strengthened work on the same branch certifies the exact reduced-surface
global minimum directly and reveals one additional higher-action stationary
branch beyond this broad multistart pair. That stronger theorem does not
change the physical selector branch; it only sharpens the global branch count.

So the PMNS-assisted selector is now branch-global on the refreshed branch:

> choose the unique lowest-action exact-closure branch of the sole-axiom
> seed-relative effective action on the fixed native `N_e` seed surface.

That branch gives exact closure:

- `eta / eta_obs = 1`

## Stationary branches

The low-action branch is

- `x = (0.471675, 0.553811, 0.664514)`
- `y = (0.208063, 0.464383, 0.247554)`
- `delta ~ 0`
- `S_rel = 0.240906701369`
- `eta / eta_obs = (1.0, 0.75917896, 0.48458840)`

The high-action branch is

- `x = (0.790189, 0.406763, 0.493049)`
- `y = (0.586185, 0.167566, 0.166248)`
- `delta ~ 0`
- `S_rel = 1.110657539...`
- `eta / eta_obs = (1.0, 0.94763529, 0.95876001)`

So the action gap is finite and large:

- `ΔS > 0.5`

The low-action branch is therefore not just a local branch. On the broad
multistart constrained scan, it is the unique physical selector branch; the
later certified-global theorem strengthens this to a unique global minimum on
the exact reduced surface.

## What this closes

This removes the last practical selector caveat on the PMNS-assisted flavored
repair route.

On the refreshed branch, the full chain is now internal:

- exact source/kernel side
- exact transport side
- exact PMNS packet localization
- exact seed-relative effective action
- exact branch-global selector

So the PMNS-assisted `N_e` route is now full-stack closed on this branch.

## Numerical consequence

Relative to the old theorem-native one-flavor miss

- `eta_obs / eta = 5.297004933778`

the selected PMNS-assisted branch gives

- `eta / eta_obs = 1`

So the old `5.3x` miss is gone on the full-closure selector branch.

## Scope

This theorem is branch-global in the broad multistart sense on the refreshed
DM branch. It does not claim an independent analytic classification of all
possible disconnected components on the exact reduced surface, and it is
superseded on that stronger point by the later certified-global theorem.

But on the branch actually used for the DM closure program, the selector caveat
is now removed.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_full_closure_selector_theorem.py
```
