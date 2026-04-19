# DM Leptogenesis PMNS Selector Coincidence Theorem

**Date:** 2026-04-16  
**Status:** exact selector-coincidence theorem on the current reduced `N_e`
stationary set  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_selector_coincidence_theorem.py`

## Question

On the current exact reduced `N_e` stationary set, is there still any real
selector ambiguity between the framework-internal observable-relative-action
law and the physical packet-level branch readout?

## Bottom line

No.

They select the same branch.

More precisely:

- the exact observable-relative-action law selects the low branch
- the exact packet-level dominance-gap law selects the same low branch
- that branch is also the unique lowest-action branch on the current exact
  reduced stationary set

So selector ambiguity is closed on the current reduced stationary set.

## Exact theorem

The observable-relative-action law already gives the exact closure source

- `x = (0.471675, 0.553811, 0.664514)`
- `y = (0.208063, 0.464383, 0.247554)`
- `delta ~ 0`
- `S_rel = 0.240906701369`

This matches the exact low branch from the reduced stationary-set analysis.

Separately, the packet-level dominance-gap theorem shows that on the same exact
stationary set:

- the low branch uniquely maximizes the favored-column dominance gap
- the low branch uniquely minimizes non-favored spill

Therefore the internal observable selector and the physical packet selector
coincide.

## What this closes

This closes the remaining exact selector ambiguity on the current reduced
stationary set.

What is no longer live:

- “maybe the physical branch and the observable-relative-action branch differ”

What is now exact:

- the physical branch is the observable-relative-action branch on the current
  reduced stationary set

## Boundary

This does not by itself upgrade the broader reduced-surface search into a
fully validated interval-global certification theorem.

So the live residual issue is computational certification scope, not a science
ambiguity about which branch is physical once the stationary set is in hand.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_selector_coincidence_theorem.py
```
