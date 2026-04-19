# PMNS Microscopic `ΔD` Seed Law

**Date:** 2026-04-15  
**Status:** exact positive seed-patch value law  
**Script:** `scripts/frontier_pmns_microscopic_delta_d_seed_law.py`

## Question

On the exact weak-axis seed patch, can the active microscopic deformation
`ΔD = D - I` already be written explicitly?

## Bottom line

Yes.

If the weak-axis split is `diag(A,B,B)` and the compatibility condition
`A <= 4B` holds, then the canonical active realization lies on the symmetric
slice

`D_seed = x I + y C`

or on its exchange sheet

`D_seed' = y I + x C`.

Therefore the deformation is

- `ΔD_seed = (x-1) I + y C`
- `ΔD_seed' = (y-1) I + x C`

with exact coefficients

- `x_± = (sqrt(A) ± sqrt((4B-A)/3)) / 2`
- `y_± = (sqrt(A) ∓ sqrt((4B-A)/3)) / 2`.

## Consequence

So the aligned seed patch is not just structurally reduced. It is positively
closed at the `D` level.

What remains open is only the generic off-seed channel coefficients in the
deformation carrier

`ΔD = U + V C + W C^2`.

## Boundary

This note does **not** derive the generic off-seed coefficients. It only closes
the aligned weak-axis seed patch exactly.

## Command

```bash
python3 scripts/frontier_pmns_microscopic_delta_d_seed_law.py
```
