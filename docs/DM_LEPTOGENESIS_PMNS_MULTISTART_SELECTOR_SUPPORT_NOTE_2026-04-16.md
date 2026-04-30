# DM Leptogenesis PMNS Multistart Selector Support

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16
**Script:** `scripts/frontier_dm_leptogenesis_pmns_multistart_selector_support.py`
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

The current broad multistart scan gives strong reduced-surface support for the
same low-action PMNS-assisted `N_e` branch, but this file is not treated as a
live theorem-grade closure result.

Broad multistart enumeration of exact closure starts on the fixed native `N_e`
seed surface yields two dominant stationary closure branches:

1. a low-action branch
2. a high-action branch

These are separated by a finite action gap.

Later strengthened reduced-surface support on the same branch reveals one
additional higher-action stationary branch beyond this broad multistart pair.
That stronger support does not change the physical selector branch; it only
sharpens the recovered branch count on the reduced surface.

The broad scan currently isolates the same low-action branch already seen in
the later reduced-surface support pass. That branch gives:

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
multistart constrained scan, it is the unique physical selector branch within
the recovered dominant pair; the later reduced-surface support pass recovers
the same branch as the lowest-action branch in a three-branch set.

## Status

This is now read as **support**, not live closure authority:

- it is a broad multistart constrained scan on the fixed native `N_e` seed
  surface
- it recovers a low-action and high-action stationary pair with a large action
  gap
- it is useful evidence for branch structure on the reduced surface
- it is not, by itself, a theorem-grade global selector

## Numerical consequence

Relative to the old theorem-native one-flavor miss

- `eta_obs / eta = 5.297004933778`

the selected PMNS-assisted branch gives

- `eta / eta_obs = 1`

So the old `5.3x` miss is gone on the full-closure selector branch.

## Scope

This note should be used as broad-scan selector support only. The later
reduced-surface support pass is stronger on the same branch set, and the live
authority path keeps both passes below theorem-grade promotion.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_multistart_selector_support.py
```
