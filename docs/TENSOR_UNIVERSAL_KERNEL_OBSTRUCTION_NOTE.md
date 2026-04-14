# Tensor Universal Kernel Obstruction on the Retained Gravity Class

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_universal_kernel.py`  
**Status:** sharp obstruction: no family-universal positive `K_tensor` on the
current audited restricted class without an additional selector / coarse-graining
/ microscopic source law

## Purpose

The retained gravity stack has already narrowed the full-GR problem to a tensor
completion question:

- the scalar shell trace / Schur boundary action is exact on the current class
- scalar-only completion is ruled out
- the minimal tensor block is rank two
- the local `O_h` and finite-rank families both admit that minimal tensor block
  locally

The remaining question is whether that local rank-two completion can be made
**family-universal** with one positive-definite `2 x 2` tensor kernel
`K_tensor`.

This note answers that question on the audited restricted class.

## What is being tested

The candidate universal closure would need one common tensor boundary action of
the form

`I_tensor(f, a_vec, a_tf ; j, eta) = I_scalar(f ; j)
  + 1/2 [a_vec, a_tf] K_tensor [a_vec, a_tf]^T - eta^T [a_vec, a_tf]`

with:

- `f` the exact scalar shell trace
- `a_vec` the shift-like boundary coordinate
- `a_tf` the traceless-shear boundary coordinate
- `K_tensor` symmetric positive definite
- `eta` a single microscopic source-to-channel drive

The key universality claim would be:

> the same positive `K_tensor` and the same source law should work on both the
> exact local `O_h` and finite-rank source families.

## Exact result on the audited families

The two audited families each support the minimal rank-two tensor block locally.
That part is real.

But the fitted kernel and source map are family-sensitive:

- kernel relative difference between the exact local `O_h` and finite-rank
  classes: `2.621449e-01`
- scalar-derived tensor-drive coefficient relative difference:
  `7.180115e-02`
- required completion amplitude relative difference:
  `8.969562e-01`

The local mixed-pulse additivity is excellent on both families:

- exact local `O_h`
  - `dG_0i` additivity error: `3.059e-08`
  - `dG_TF` additivity error: `8.023e-18`
- finite-rank
  - `dG_0i` additivity error: `6.850e-08`
  - `dG_TF` additivity error: `6.191e-11`

So the rank-two block itself is locally sensible. The failure is universality.

## Best common positive candidate still fails

A natural universal candidate is the symmetric average of the two fitted
kernels. It remains positive definite, but it does not collapse the family
dependence:

- average kernel eigenvalues remain positive
- the family-completion amplitudes still differ strongly under the shared
  kernel
- the relative completion mismatch remains about `9.242957e-01`

So even the best shared positive candidate does not turn the current restricted
class into one family-universal tensor completion theorem.

## Why this is an obstruction

This is not merely a fit-quality annoyance.

The retained stack now shows:

1. the scalar shell trace alone is insufficient
2. the minimal tensor block is only locally sufficient
3. the source-to-channel map and kernel vary between the audited restricted
   families
4. therefore no single positive `K_tensor` closes both families on the current
   class without an additional principle that identifies an effective selector
   or coarse-graining law

That means the universal-kernel route is obstructed on the current branch.

## Verdict

- **Family-local rank-two tensor completion:** yes
- **Family-universal positive `K_tensor` on the current audited class:** no
- **Scalar-only completion:** still ruled out

The sharpest remaining gravity statement is now:

> the current restricted strong-field class admits only family-local tensor
> completion; a universal positive `K_tensor` does not exist on the audited
> class unless an additional selector / coarse-graining / microscopic source
> law is supplied.

## What remains open

This does **not** close:

1. a selector principle that could make the kernel universal
2. a microscopic derivation of such a selector
3. full nonlinear GR in full generality

