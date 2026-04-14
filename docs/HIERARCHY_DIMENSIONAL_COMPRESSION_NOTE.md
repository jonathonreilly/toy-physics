# Hierarchy Dimensional Compression Note

**Date:** 2026-04-13  
**Script:** `scripts/frontier_hierarchy_dimensional_compression.py`

## Question

If the hierarchy route really carries an `alpha_LM^{16}` structure, should the
remaining `L_t`-block normalization residual compress with a **sixteenth** root?

## Short answer

Only if the physical correction multiplies the **scale directly**.

If the physical order parameter is instead a **dimension-4 effective potential
density**, then the correct compression is a **fourth** root, not a sixteenth
root.

That distinction matters numerically.

## Input numbers

From the Codex intensive-order-parameter diagnostics:

- condensate-density ratio
  `R = cond(L_t=10) / cond(L_t=2) ~= 1.15469`
- current hierarchy prediction
  `v_pred ~= 253.4 GeV`
- observed electroweak scale
  `v_obs = 246.22 GeV`
- required prefactor
  `C_obs = v_obs / v_pred ~= 0.97167`

## Compression candidates

Using the same residual ratio `R`:

- direct scale-like (`1/16` root):
  - `R^(-1/16) ~= 0.99105`
  - too small to explain the full `253 -> 246` shift

- dimension-4 effective-potential-like (`1/4` root):
  - `R^(-1/4) ~= 0.96468`
  - this is in the right **few-percent** range

So the hierarchy residual is numerically much more consistent with a
dimension-4 intensive observable than with a direct sixteenth-root correction.

## Interpretation

This does **not** prove the hierarchy theorem.

It does sharpen the remaining surface:

1. the raw `alpha_LM^{16}` structure still looks like the right exponent
2. the final normalization should probably **not** be thought of as a direct
   `16`th-root correction to the scale
3. the more plausible route is:
   - derive the intensive effective potential / free-energy density
   - show how the `L_t > 2` block normalization enters that density
   - then extract `v` as a dimension-4 scale

## Practical conclusion

If the remaining theorem closes through the effective-potential density, the
size of the observed `~3%` discrepancy is no longer mysterious. The magnitude
is already in the right range.

What is still open:

- the exact sign / placement of that normalization in the physical formula
- the derivation of the order parameter itself
- the full determinant-to-VEV theorem
