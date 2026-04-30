# DM Full Closure Same-Surface Thermal Monotonicity Theorem

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-17  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_thermal_monotonicity_theorem.py`

## Question

What part of the DM-side selector problem can already be closed exactly, before
the thermal integral itself is fully derived?

## Answer

The exact same-surface thermal DM ratio is **strictly increasing** in the
selected coupling `alpha`.

The key exact identities are:

- `f_att'(y) - 1/2 = h(y) / (2 (e^y - 1)^2)`
- `f_rep'(y) + 1/2 = h(y) / (2 (e^y - 1)^2)`

with

- `h(y) = e^(2y) - 2 y e^y - 1`

and

- `h(0)=0`
- `h'(y) = 2 e^y (e^y - 1 - y) > 0` for `y>0`

so

- `f_att'(y) >= 1/2`
- `f_rep'(y) >= -1/2`

for all `y>0`.

On the same-surface DM channel weights, this yields the pointwise derivative
bound

- `64 f_att'(8y) + f_rep'(y) > 63/2`

and therefore the exact same-surface thermal DM ratio is strictly increasing in
`alpha`.

## Consequence

This closes one exact part of the DM-side selector problem:

- the remaining blocker is **not** monotonicity
- the remaining blocker is only exact evaluation or exact bounding of the
  thermal integral itself

So on any admitted one-scalar `alpha` family:

- there can be at most one closure root

The remaining work is to close the thermal integral, not to prove root
uniqueness.

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_thermal_monotonicity_theorem.py
```
