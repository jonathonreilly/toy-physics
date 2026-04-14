# Tensor Endpoint Coefficients: Exact Support Law, Blocked Tensor Lift

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** exact support endpoint theorem plus sharp tensor blocker

## Exact part

On the microscopic `A1` support block, the exact surviving support-side scalar
is

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

The exact endpoint coefficients are:

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

Therefore the support-side affine law

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

is exact.

## Blocked part

The current retained stack does **not** yet provide an exact tensor observable
on `A1 x {E_x, T1x}`.

What we currently have instead is the bounded numerical tensor frontier:

- `eta_floor_tf`
- `gamma_E`
- `gamma_T`

Those coefficients still come from the sampled Einstein-residual pipeline, not
from an exact support-side operator or exact tensor boundary Hessian.

So the exact tensor endpoint coefficients at

- `e0`
- `s / sqrt(6)`

remain blocked at the tensor level.

## Exact blocker

The shell/junction stack is exact, but projectively blind to `r`.
The support-side `A1` center-excess law is exact, but it only produces the
scalar datum `delta_A1`.

What is still missing is the exact tensor-side operator that maps this support
datum into the bright `E_x` and `T1x` channels without going through the
current numerical `eta_floor_tf` construction.

## Verdict

The support-side endpoint theorem is complete.
The tensor endpoint theorem is still blocked.
