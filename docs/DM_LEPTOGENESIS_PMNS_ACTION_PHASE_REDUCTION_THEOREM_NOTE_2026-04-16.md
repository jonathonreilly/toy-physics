# DM Leptogenesis PMNS Action Phase-Reduction Theorem

**Date:** 2026-04-16  
**Status:** exact action-side phase theorem on the fixed native `N_e` seed surface  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_action_phase_reduction_theorem.py`

## Question

On the fixed native `N_e` seed surface, what does the exact
observable-relative action do with the residual cycle phase `delta`?

## Bottom line

At fixed positive `x` and `y`, the exact action is a strictly decreasing
function of `cos(delta)`.

So:

- the unique action-minimizing phase is `delta = 0 mod 2*pi`
- `delta = pi` is the worst aligned phase on the same support data
- nonzero-phase branches are automatically higher-action side branches
  relative to their real-phase counterparts

## Exact content

For the canonical charged active block

`Y(delta) = diag(x) + diag(y_1, y_2, y_3 e^{i delta}) C`

with `H(delta) = Y(delta) Y(delta)^*`, the exact relative action is

`S_rel(H || H_seed) = Tr(H_seed^{-1} H) - log det(H_seed^{-1} H) - 3`.

Both terms depend on `delta` only through `cos(delta)`:

- `Tr(H_seed^{-1} H(delta))`
  is affine in `cos(delta)` because only the `(1,3)` / `(3,1)` matrix entries
  carry the cycle phase
- `det(H(delta))`
  is exactly
  `|x_1 x_2 x_3 + y_1 y_2 y_3 e^{i delta}|^2`

Therefore

`d S_rel / d cos(delta) < 0`

for every strictly positive `x` and `y` on the current branch.

## Why this matters

This does **not** by itself certify the full `eta_{i_*} = 1` closure manifold.
The closure functional still has to be handled separately.

But it does settle one exact structural point:

- any action-based winner has a real-phase representative
- nonzero-phase closure branches, when they exist, are action-disfavored side
  branches rather than hidden lower-action competitors

So the remaining reduced-surface problem is legitimately concentrated on the
real `delta = 0` chart when the goal is the physical low-action selector lane.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_action_phase_reduction_theorem.py
```
