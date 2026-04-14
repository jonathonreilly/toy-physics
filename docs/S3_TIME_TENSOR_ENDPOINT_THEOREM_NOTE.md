# Route 2 Tensor Endpoint Coefficients: Exact Support Endpoint Law, Blocked Tensor Lift

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_s3_time_tensor_endpoint_theorem.py`  
**Status:** exact support endpoint theorem plus sharp tensor blocker

## Purpose

Route 2 has already been reduced to:

- exact `S^3` spatial closure
- exact anomaly-forced single-clock time
- exact background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer / kinetic semigroup `T_R = exp(-Lambda_R)`

The remaining question is now sharply localized:

> can the first Route-2 tensor primitive have exact endpoint coefficients at
> the two exact `A1` endpoints `e0` and `s / sqrt(6)`, or is the current
> stack still missing the primitive that would make those coefficients exact?

This note answers that question in the narrowest honest form.

## Exact part: the support-side endpoint theorem is complete

On the exact seven-site star support, the surviving exact microscopic scalar is

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

For the two unit-charge `A1` endpoints:

- `e0 = A1(center)`
- `s / sqrt(6) = A1(shell-average)` normalized to unit total charge

the exact endpoint coefficients are:

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

Therefore the exact projective `A1` family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

has the exact support-side law

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

This is the exact endpoint theorem that the current support stack can prove.

## Bounded part: the first Route-2 tensor primitive prototype

The current first tensor primitive prototype is

`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block

`A1 x {E_x, T1x}`.

Its endpoint data are explicit, but they are still numerical prototype data,
not exact tensor theorem data:

- `Theta_R^(0)(e0) = (-3.772329e-04, +3.359952e-04)`
- `Theta_R^(0)(s / sqrt(6)) = (-2.010572e-04, +4.031968e-04)`

The current affine support law in `delta_A1` reproduces the canonical `A1`
family and the audited exact-local and finite-rank `A1` baselines at bounded
accuracy, but that does not upgrade the tensor endpoint coefficients to exact.

## Sharp blocker

The retained exact shell/junction stack is now known to be projectively blind
to the remaining `A1` ratio `r = s / e0` at fixed total charge.

That means:

- the exact shell-side observables cannot distinguish the two tensor endpoint
  backgrounds beyond total charge
- the remaining tensor coefficients still come from the numerical
  `eta_floor_tf` pipeline
- the current exact support stack produces only the scalar
  `delta_A1`, not an exact tensor-valued observable on
  `A1 x {E_x, T1x}`

So the tensor endpoint coefficients at

- `e0`
- `s / sqrt(6)`

remain blocked as exact theorem data.

## Practical conclusion

The correct split on the current route-2 surface is:

1. exact support endpoint theorem
2. bounded tensor primitive endpoint prototype
3. sharp blocker for exact tensor endpoint coefficients

The exact next theorem target is not another shell-side refinement. It is an
exact tensor-valued support observable on `A1 x {E_x, T1x}` that can lift the
support endpoint law into a theorem-grade tensor endpoint law.
