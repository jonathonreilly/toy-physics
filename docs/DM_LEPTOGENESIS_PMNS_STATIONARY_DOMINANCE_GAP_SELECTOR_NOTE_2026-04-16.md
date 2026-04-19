# DM Leptogenesis PMNS Stationary Dominance-Gap Selector

**Date:** 2026-04-16  
**Status:** exact packet-level selector theorem on the currently recovered
reduced `N_e` stationary set  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_stationary_dominance_gap_selector.py`

## Question

Once the exact reduced `N_e` stationary set is in hand, what actually selects
the physical low-action branch from the nearby stationary competitors?

## Bottom line

The favored closure column alone does not.

The full packet does.

On the currently recovered reduced `N_e` stationary set:

- the low and nearby middle branches carry essentially the same favored closure
  column up to permutation
- their favored-column transport value is therefore the same to numerical
  precision
- so favored-column closure by itself does not choose the physical branch

But the full packet does:

- the physical low branch uniquely minimizes non-favored transport spill
- equivalently it uniquely maximizes the favored-column dominance gap

So the exact selector on the stationary candidate set is:

> choose the branch with maximal favored-column dominance gap
> `G = F_{i_*} - max_{j != i_*} F_j`,

equivalently minimal non-favored spill

> `S_spill = sum_{j != i_*} F_j`.

## Exact theorem

Using the currently recovered three reduced-surface stationary branches:

- low branch
- nearby middle branch
- high branch

all three satisfy favored-column closure on `i_* = 0`.

However:

- the low favored column is almost the same as the middle favored column up to
  permutation
- both therefore realize essentially the same exact favored-column transport
  value

So the selector must look at the whole packet, not the favored column alone.

When the exact transport functional is evaluated on all three columns:

- the low branch has the smallest non-favored spill
- the low branch has the largest dominance gap
- the middle branch is second
- the high branch is worst

Therefore the physical low branch is the unique most one-source-exclusive
stationary packet on the current reduced `N_e` stationary set.

## What this closes

This closes the remaining exact branch-selection question on the current
stationary candidate set.

What is no longer true:

- “the low branch is still only a numerically preferred stationary point”

What is now true:

- the low branch is the unique maximum-dominance-gap / minimum-spill branch on
  the exact stationary candidate set already recovered on this branch

## Boundary

This is not yet a full observation-free selector theorem on the entire reduced
closure surface.

It is a theorem on the exact currently recovered stationary set. A broader
global theorem would still need a closure-surface certificate beyond the
stationary candidates.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_stationary_dominance_gap_selector.py
```
