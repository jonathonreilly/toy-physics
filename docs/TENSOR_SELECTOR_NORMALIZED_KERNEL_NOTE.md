# Selector-Normalized Tensor Kernel on the Retained Gravity Class

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_selector_normalized_kernel.py`  
**Status:** bounded positive narrowing: the missing gravity principle now looks
much more like a normalization/selector law than a new tensor kernel shape law

## Purpose

The raw universal-kernel theorem just failed on the current restricted gravity
class:

- no family-universal positive raw `K_tensor`
- exact local `O_h` and finite-rank families require materially different raw
  kernel entries and raw completion amplitudes

That still left one important possibility open:

> perhaps the family dependence lives mostly in the missing normalization law,
> while the tensor kernel **shape** is already nearly universal.

This note tests that possibility.

## Selector-normalized variables

The current retained tensor stack already provides two natural local scales:

1. the dominant traceless-shear response `eta_11`
2. the scalar Schur action magnitude `|I_scalar|`

Using those, define:

- normalized tensor kernel shape
  - `K_hat = K_tensor / eta_11`
- normalized source map
  - `eta_hat = eta / eta_11`
- scalar-derived tensor drive coefficient
  - `c_eta = eta_floor_tf / |I_scalar|`
- normalized completion coordinate
  - `a_tilde = (eta_11 / |I_scalar|) a`

If the missing principle is mainly a selector/coarse-graining law, these
normalized objects should be much closer across families than the raw kernel.

## Result

They are.

Raw family mismatch:

- raw kernel relative difference: `2.621449e-01`
- raw source-map relative difference: `2.623630e-01`
- raw completion-amplitude relative difference: `8.969562e-01`

Selector-normalized family mismatch:

- normalized kernel-shape relative difference: `4.262383e-02`
- normalized source-map relative difference: `4.545992e-02`
- scalar-derived tensor-drive coefficient relative difference: `7.180115e-02`
- normalized completion-coordinate relative difference: `1.208005e-01`

So the branch is no longer saying merely:

> there is no universal tensor kernel.

It can now say something sharper:

> there is no universal **raw** positive `K_tensor`, but after normalizing by
> the dominant tensor-channel scale and the scalar Schur action, the kernel
> shape and source map become close to universal on the audited restricted
> class.

## Common normalized candidate

Taking the average normalized kernel and the average scalar-derived drive
coefficient gives:

- positive normalized kernel eigenvalues:
  - `(1.012109e-01, 1.000073e+00)`
- common predicted normalized completion coordinate:
  - `a_tilde = [-2.752395e-04, 3.447720e-03]`

Prediction error:

- vs exact local `O_h`: `5.122663e-02`
- vs finite-rank: `6.555167e-02`

That is not an exact theorem. But it is strong bounded evidence that the
remaining gap is a normalization/selector law, not a wildly different tensor
kernel family by family.

## Interpretation

This is the cleanest positive gravity narrowing on the branch since the
scalar-only no-go.

The current best read is:

1. raw universal `K_tensor` is obstructed
2. local rank-two tensor completion is real
3. after selector normalization, the tensor kernel shape is nearly universal
4. therefore the missing principle is most likely:
   - a local shell selector
   - a coarse-graining law
   - or a microscopic source law
   that fixes the normalization of the tensor channels

That is a substantially narrower target than “derive a whole new tensor
kernel.”

## What this does and does not close

This **does** close:

- the question of whether the raw obstruction is totally structureless
- the question of whether a meaningful universal tensor shape is already
  visible after retained local normalization

This does **not** close:

1. a theorem that the selector normalization is uniquely forced
2. a microscopic derivation of the selector normalization from the axiom alone
3. full nonlinear GR in full generality

## Practical next step

The remaining positive gravity route is now:

> derive the selector/coarse-graining/source law that fixes the tensor-channel
> normalization, then lift the bounded normalized kernel-shape universality into
> a theorem.
