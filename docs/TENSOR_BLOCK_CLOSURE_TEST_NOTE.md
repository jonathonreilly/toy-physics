# Tensor Block Closure Test

**Date:** 2026-04-14  
**Script:** `scripts/frontier_tensor_block_closure_test.py` (PASS=6 FAIL=0 on current main; classified PASS lines for the bounded no-go now emitted: local sufficiency on each family, cross-family kernel/eta/a_star mismatches, non-universality)
**Status:** bounded - bounded or caveated result note

## Question

The current gravity branch already proves that the scalar shell trace is not
enough:

- scalar trace data are unchanged across scalar, vector, tensor, and mixed
  probes
- shift-like and traceless-shear channels generate independent Einstein
  residuals
- the scalar-only completion route is therefore dead

The remaining question is narrower:

> if we keep the minimal tensor block `(a_vec, a_tf)`, can a plausible
> source-driven `eta` map together with a symmetric `K_tensor` close the
> restricted class as a single universal theorem?

This note tests that directly on the exact local `O_h` and finite-rank source
families already retained on the branch.

## Candidate closure ansatz

Use the smallest tensor boundary action compatible with the retained stack:

`I_tensor(f, a_vec, a_tf ; j, eta) = I_scalar(f ; j)
  + 1/2 [a_vec, a_tf] K_tensor [a_vec, a_tf]^T - eta^T [a_vec, a_tf]`

with:

- `f` the exact scalar shell trace
- `a_vec` the shift-like tensor boundary coordinate
- `a_tf` the traceless-shear boundary coordinate
- `K_tensor` a symmetric positive-definite `2 x 2` tensor kernel
- `eta` a scalar-derived drive

The most conservative scalar-derived drive on the retained stack is:

- `eta_vec = 0`
- `eta_tf = base traceless Einstein floor`

This is the least aggressive tensor source map consistent with the current
bridge package.

## What the test checks

For each audited family, the runner extracts:

1. the pure vector and pure traceless-shear tensor response channels
2. a symmetric `K_tensor` from those two probe directions
3. the scalar-derived `eta`
4. the implied completion amplitudes `a_star = K_tensor^{-1} eta`

Then it compares the fitted tensor kernel and the required amplitudes across
the two audited restricted families:

- exact local `O_h`
- broader finite-rank

## Quantitative result

The two families both support the minimal rank-two tensor block locally.
That part is real.

But the fitted kernel and source-drive map are not universal:

- the symmetric tensor kernel differs by `2.621449e-01` in relative Frobenius
  norm between the exact local `O_h` and finite-rank classes
- the scalar-derived tensor-drive coefficient differs by `7.180115e-02`
- the required completion amplitudes differ much more strongly:
  `a_star = (-1.064685e-03, 9.419596e-03)` on the exact local `O_h` class
  versus `a_star = (-2.788652e-03, 9.160748e-02)` on the finite-rank class
- the mixed-pulse additivity remains excellent on both classes, with residual
  errors `O(10^-8)` to `O(10^-11)`, so the local rank-two block itself is
  sensible; the failure is universality of the source map and kernel, not the
  existence of two tensor channels

So the minimal tensor block is **not** promoted as a single family-universal
closure theorem on the audited restricted class.

## Verdict

- **Local sufficiency on each family:** yes
- **Single universal rank-two tensor closure across both families:** no
- **Scalar-only completion:** still ruled out by the earlier no-go

So the sharpest remaining gravity statement is:

> the current restricted strong-field class admits a minimal rank-two tensor
> completion locally on each audited family, but the source-to-channel map and
> tensor kernel remain family-sensitive, so a universal tensor completion law
> is still missing.
