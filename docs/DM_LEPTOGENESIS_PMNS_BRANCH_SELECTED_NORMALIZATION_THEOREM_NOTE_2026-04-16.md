# DM Leptogenesis PMNS Branch-Selected Normalization Theorem

**Date:** 2026-04-16  
**Status:** exact branch-selected normalization theorem on the reduced `N_e`
closure surface  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_branch_selected_normalization_theorem.py`

## Question

After fixing the exact reduced `N_e` selector structure, is the missing
normalization coefficient still diffuse, or is it already fixed on the
selected physical branch?

## Bottom line

It is fixed on the selected branch.

Each exact closure stationary branch carries its own unique first-order
normalization coefficient `a_branch`, defined by

`grad log F_{i_*} = a_branch grad S_rel`

at that branch point.

On the current branch:

- the low-action physical branch has
  `a_phys ≈ 0.51847995`
- the higher branch has
  `a_high ≈ 0.18948974`

So the coefficient is **not** universal across the closure surface.
But it **is** exact on the physical branch already selected by the current
reduced-surface theorem stack.

## Exact consequence

This closes one more layer of the normalization lane.

What is no longer open:

- the branch-selected coefficient on the physical reduced `N_e` closure branch

What is still open:

- the observation-free law that selects that branch without using the
  `eta/eta_obs = 1` surface

So the live next theorem is no longer “find the coefficient.” It is:

> derive the observation-free branch-selection normalization law that picks the
> physical branch and thereby lifts the exact branch-selected coefficient into
> a full native value law.

## Why this matters

This rules out a common remaining ambiguity.

The normalization problem is not:

- “maybe the coefficient is still wandering across the exact closure surface”

It is:

- “the coefficient is fixed on the selected branch, but the branch-selection
  law is still observational.”

That is a much smaller and cleaner target.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_branch_selected_normalization_theorem.py
```
