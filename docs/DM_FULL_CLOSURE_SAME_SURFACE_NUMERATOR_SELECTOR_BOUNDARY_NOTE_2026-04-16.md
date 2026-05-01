# DM Full Closure Same-Surface Numerator Selector Boundary

**Status:** bounded - bounded or caveated result note
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

Those exact endpoints induce distinct certified DM outputs on the corrected
same-surface thermal map:

- `R(alpha_lo) in [5.442019867867, 5.442019867931]`
- `R(alpha_hi) in [5.482855571890, 5.482855571936]`

and therefore

- `Omega_DM(alpha_lo) in [0.267709052538, 0.267709052541]`
- `Omega_DM(alpha_hi) in [0.269717881594, 0.269717881596]`

So the current bank gives an interval, not a selector.

## Why This Closes The Current-Bank Question

The same-surface DM lane already has:

1. exact endpoint observables;
2. an exact structural prefactor `R_base = 31/9`;
3. a certified same-surface thermal evaluation/bounding result that sends those
   endpoints to distinct outputs.

What it does **not** have is any further exact scale-selection law on that DM
lane. So there is no theorem-grade current-bank selector closure.

## Consequence

The current-bank DM selector question is now settled:

- **current bank:** no selector closure
- **next honest science target:** theorem-grade evaluation or bounding of the
  current-bank DM lane is now satisfied on this branch
- **remaining honest science target:** whether the current bank itself can
  supply a selector, or whether the one-scalar DM-side family must remain an
  admitted extension

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_numerator_selector_boundary.py
```
