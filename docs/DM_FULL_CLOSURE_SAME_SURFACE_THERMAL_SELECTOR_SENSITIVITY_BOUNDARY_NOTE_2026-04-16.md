# DM Full Closure Same-Surface Thermal Selector Sensitivity Boundary

**Date:** 2026-04-16  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_thermal_selector_sensitivity_boundary.py`

## Question

Is the apparent structural collapse clue

- `sigma ~= 1/(2 R_base) = 9/62`

actually robust on the retained same-surface DM kernel?

## Answer

No, not yet.

On the coarse retained thermal runner, the admitted-family selector appears to
land extremely close to

- `sigma = 9/62`.

But refining the thermal quadrature shifts the selector root by much more than
the apparent `9/62` residual itself. In particular:

- coarse retained root:
  - `sigma_2000 = 0.145161097420491`
- refined uniform-grid roots:
  - `sigma_4000 = 0.145600347860581`
  - `sigma_8000 = 0.145584750712540`
  - `sigma_16000 = 0.145580852564623`
- structural candidate:
  - `sigma_9/62 = 0.145161290322581`

So the near-coincidence with `9/62` is not stable under thermal refinement.

## Consequence

The branch must not promote `9/62` as a DM selector law.

The exact rational/group skeleton remains interesting:

- `R_base = 31/9`
- exact channel fractions `8/9`, `1/9`
- exact low-`z` weighted coefficients `7/12`, `19/144`

But the retained thermal layer is still too unstable to support selector
collapse from those exact ingredients.

## Honest Endpoint

The remaining DM-side problem is now clear:

1. current-bank selector closure: still no
2. minimal admitted one-scalar DM family: yes
3. structural `9/62` collapse claim: not yet justified
4. next real task:
   replace the retained thermal average with a converged or exact thermal
   theorem before trying to collapse the DM-side scalar further

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_thermal_selector_sensitivity_boundary.py
```
