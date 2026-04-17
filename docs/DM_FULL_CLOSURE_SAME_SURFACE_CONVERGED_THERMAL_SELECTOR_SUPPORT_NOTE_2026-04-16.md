# DM Full Closure Same-Surface Converged Thermal Selector Support

**Date:** 2026-04-16  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_converged_thermal_selector_support.py`

## Question

After rejecting the unstable coarse thermal runner, does the admitted
one-scalar same-surface DM family still close on a numerically stable thermal
evaluation?

## Answer

Yes, at support level.

Using a corrected high-precision continuum thermal evaluator on the same-surface DM
family, the one-scalar admitted family still has a unique interior closure
crossing:

- `sigma_conv = 0.145077095756643`
- `alpha_conv = 0.090899546858439`
- `R_conv = 5.447934280746`
- `Omega_DM = 0.268000000000`

## Consequence

This does two useful things:

1. it preserves the positive one-scalar DM-side admitted family;  
2. it kills the fake `9/62` selector collapse.

The converged selector differs materially from both:

- the coarse retained runner:
  - `sigma_base = 0.145161097420491`
- the coarse structural clue:
  - `sigma_9/62 = 0.145161290322581`

## Honest Status

- current-bank DM selector closure: still no
- one-scalar admitted DM family: still yes
- selector law on that family:
  - positive support from the converged thermal evaluator
  - not theorem-grade exact yet

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_converged_thermal_selector_support.py
```
