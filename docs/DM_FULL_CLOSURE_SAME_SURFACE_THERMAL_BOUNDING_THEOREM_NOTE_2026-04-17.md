# DM Full Closure Same-Surface Thermal Bounding Theorem

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-17  
**Branch:** `codex/dm-thermal-review-2026-04-17`  
**Script:** `scripts/frontier_dm_full_closure_same_surface_thermal_bounding_theorem.py`

## Question

Can the same-surface DM thermal layer now be promoted from support status to a
rigorous evaluation/bounding result?

## Answer

Yes.

The thermal layer is now closed at theorem-grade **evaluation/bounding**
strength by combining:

1. the exact continuum integral representation on the retained `x_f = 25`
   slice,
2. the exact monotonicity theorem in the selected coupling `alpha`,
3. the exact positive-series / exact tail enclosure machinery.

## Certified Current-Bank Output

On the exact current-bank same-surface endpoints:

- `alpha_lo = 0.090667836017286`
- `alpha_hi = 0.092264992618360`

the exact thermal ratio is enclosed rigorously by:

- `R(alpha_lo) in [5.442019867867, 5.442019867931]`
- `R(alpha_hi) in [5.482855571890, 5.482855571936]`

Therefore, after fixing `Omega_b` from `eta_obs`,

- `Omega_DM(alpha_lo) in [0.267709052538, 0.267709052541]`
- `Omega_DM(alpha_hi) in [0.269717881594, 0.269717881596]`

and the current-bank no-go is rigorous:

- the current bank carries distinct exact endpoint images,
- the target lies between them,
- but the current bank still does not furnish a selector law.

## Certified One-Scalar DM-Family Root

On the one-scalar same-surface admitted family

`alpha(sigma) = alpha_lo + sigma (alpha_hi - alpha_lo)`,

exact monotonicity plus the certified endpoint/bisection enclosures force a
unique root interval:

- `sigma in [0.145076095756643, 0.145078095756643]`
- equivalently
  `alpha in [0.090899545261282, 0.090899548455595]`

with a narrow certified width produced by the theorem runner.

So the DM-side admitted family is no longer only numerically supported; it has
a certified unique root interval on the thermal layer itself.

## Honest Status

- current-bank selector closure: still **no**
- thermal layer: now **rigorous evaluation/bounding**, not just support
- admitted one-scalar DM-side family: now has a **certified unique root interval**
- remaining flagship question:
  whether the current exact bank itself can be made to select a value, or
  whether the DM-side one-scalar family must remain an admitted extension

## Command

```bash
python3 scripts/frontier_dm_full_closure_same_surface_thermal_bounding_theorem.py
```
