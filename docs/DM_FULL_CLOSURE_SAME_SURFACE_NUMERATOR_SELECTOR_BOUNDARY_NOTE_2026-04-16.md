# DM Full Closure Same-Surface Numerator Selector Boundary

**Date:** 2026-04-16  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_numerator_selector_boundary.py`

## Question

Does the current exact DM bank already furnish a theorem-grade selector on the
live same-surface numerator interval?

## Answer

No.

The current exact DM bank gives two exact same-surface endpoint observables:

- `alpha_lo = alpha_LM = alpha_bare/u_0 = 0.090667836017286`
- `alpha_hi = alpha_short = -log(P_1)/c_1 = 0.092264992618360`

Those exact endpoints induce distinct DM outputs on the corrected continuum
support map:

- `R_lo = 5.442019867924`
- `R_hi = 5.482855571931`

and therefore

- `Omega_DM_lo = 0.267709052541`
- `Omega_DM_hi = 0.269717881596`

So the current bank gives an interval, not a selector.

## Why This Closes The Current-Bank Question

The same-surface DM lane already has:

1. exact endpoint observables;
2. an exact structural prefactor `R_base = 31/9`;
3. a corrected continuum same-surface support map that sends those endpoints to distinct
   outputs.

What it does **not** have is any further exact scale-selection law on that DM
lane. So there is no theorem-grade current-bank selector closure.

## Consequence

The current-bank DM selector question is now settled:

- **current bank:** no selector closure
- **next honest science target:** theorem-grade evaluation or bounding of the
  same-surface thermal map, not a claim that the current bank already selects
  a unique numerator value

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_numerator_selector_boundary.py
```
