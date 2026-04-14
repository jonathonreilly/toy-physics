# Projective `A1` Compatibility of the Bright Tensor Law

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_a1_projective_compatibility.py`  
**Status:** bounded positive narrowing

## Purpose

The local tensor notes already showed that the remaining bright coefficients are
controlled mainly by the scalar `A1` shape ratio

- `r = s/e0`

This note checks whether the actual audited families already lie on one common
projective `A1` shape law, or whether there is still visible family-dependent
structure after the `A1` reduction.

## Test

For each audited family:

1. extract the scalar `A1` baseline
2. compute its projective coordinate `r`
3. compute the normalized bright coefficients `(gamma_E, gamma_T)`
4. compare them with the canonical projective background
   `q_A1(r; Q=1)`

## Result

### Exact local `O_h`

- `r = 0.681702361049`
- actual:
  - `gamma_E = -2.674831460910e-04`
  - `gamma_T = +3.779088432251e-04`
- projective-shape background:
  - `gamma_E = -2.670405539236e-04`
  - `gamma_T = +3.780360420935e-04`
- differences:
  - `gamma_E`: `4.426e-07`
  - `gamma_T`: `1.272e-07`

### Finite-rank

- `r = 1.648760111184`
- actual:
  - `gamma_E = -2.394023266207e-04`
  - `gamma_T = +3.940496005983e-04`
- projective-shape background:
  - `gamma_E = -2.360191438642e-04`
  - `gamma_T = +3.898661776763e-04`
- differences:
  - `gamma_E`: `3.383e-06`
  - `gamma_T`: `4.183e-06`

## Interpretation

This does not give an exact theorem yet. But it is strong bounded evidence that
the remaining bright tensor coefficients are already largely controlled by one
projective `A1` shape law, not by deeper family-specific data.

So the current best gravity read is now:

> the remaining open problem is not family dependence. It is the exact
> axiom-first derivation of the scalar projective `A1` law itself.
