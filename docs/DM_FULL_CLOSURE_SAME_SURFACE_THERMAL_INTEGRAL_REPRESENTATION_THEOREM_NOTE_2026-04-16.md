# DM Full Closure Same-Surface Thermal Integral Representation Theorem

**Date:** 2026-04-16  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_thermal_integral_representation_theorem.py`

## Question

What is the exact thermal object that still blocks the DM-side selector?

## Answer

On the retained freeze-out slice `x_f = 25`, the same-surface thermal
Sommerfeld average has an exact normalized continuum form:

`<S> = (2/sqrt(pi)) ∫_0^∞ S(alpha_eff*sqrt(a)/sqrt(t)) sqrt(t) e^{-t} dt`

with

- `a = x_f/4 = 25/4`
- `sqrt(a) = 5/2`

So the thermal layer is no longer an opaque 2000-point grid average. It is one
exact continuum integral target.

## Exact Moment Data

On the same slice:

- `<1/v> = 2 sqrt(a)/sqrt(pi) = 5/sqrt(pi)`
- `<1/v^2> = 2 a = 25/2`

These are exact and provide exact control of the low-order thermal expansion.

## Consequence

The DM-side selector problem is now sharply localized:

1. current-bank selector closure: still no  
2. admitted one-scalar family: still positive  
3. exact remaining thermal object:
   one continuum integral family on the same-surface slice  
4. next real closure step:
   derive, bound, or exactly evaluate that integral family rather than relying
   on the coarse retained grid

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_thermal_integral_representation_theorem.py
```
