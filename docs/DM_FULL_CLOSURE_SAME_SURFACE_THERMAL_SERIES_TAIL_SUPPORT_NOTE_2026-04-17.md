# DM Full Closure Same-Surface Thermal Series/Tail Support

**Date:** 2026-04-17  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_thermal_series_tail_support.py`

## Question

Can the DM thermal layer be hardened beyond the old coarse-grid or opaque
adaptive-evaluator story, without pretending that the current-bank selector is
already theorem-grade closed?

## Answer

Yes, at support level.

The same-surface DM thermal factors admit exact positive-series
decompositions:

- `y/(1-e^{-y}) = sum_{n>=0} y e^{-n y}`
- `y/(e^{y}-1) = sum_{n>=1} y e^{-n y}`

The corresponding term integrals reduce exactly to:

- `J1(c) = ∫_0^∞ v e^{-a v^2 - c/v} dv`
- `J2(c) = ∫_0^∞ v^2 e^{-a v^2 - c/v} dv`

which are represented by exact Meijer-G expressions on the retained
`x_f = 25` slice.

The tails are controlled by exact inequalities:

- attractive tail: `tail_att(N) <= (1+y)e^{-N y}`
- repulsive tail: `tail_rep(N) <= (1+y)e^{-(N+1) y}`

so the remainder reduces again to exact `J1/J2` objects.

## Consequence

On the live DM interval, the corrected high-precision continuum evaluator is
contained inside extremely narrow exact-series/tail support intervals:

- `alpha_lo`
- `alpha_conv`
- `alpha_hi`

with ratio widths below `1e-9` on that slice.

On the live DM slice the exact-series/tail intervals are:

- `alpha_lo = 0.090667836017286`
  - `R in [5.442019867867, 5.442019867931]`
- `alpha_conv = 0.090899546858439`
  - `R in [5.447934280692, 5.447934280753]`
- `alpha_hi = 0.092264992618360`
  - `R in [5.482855571890, 5.482855571936]`

So the DM thermal layer is now materially harder than before:

- the coarse selector story is gone
- the corrected continuum evaluator agrees with an exact positive-series
  decomposition plus exact tail control

## Honest Status

- current-bank DM selector closure: still open
- admitted DM-side selector: still support, not theorem-grade closure
- remaining blocker: promote the thermal layer from support to a genuine
  theorem-grade evaluation/bounding result

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_thermal_series_tail_support.py
```
