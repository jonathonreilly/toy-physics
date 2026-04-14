# Route 2 Exact Endpoint Coefficients: Scalar Support Theorem Closed, Tensor Lift Blocked

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_s3_time_exact_endpoint_coefficients.py`  
**Status:** exact scalar endpoint theorem plus sharp tensor blocker

## Purpose

Route 2 has already been reduced to:

- exact `S^3` spatial closure
- exact anomaly-forced single-clock time
- exact background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer / kinetic semigroup `T_R = exp(-Lambda_R)`

The exact support-side scalar on the surviving `A1` block is

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

The exact question for the present note is narrower:

> can the endpoint coefficients of the first Route-2 tensor primitive be
> forced axiom-first from `delta_A1`, the two exact `A1` endpoints
> `e0` and `s / sqrt(6)`, and the bounded prototype ladder `Theta_R^(0)`?

## Exact part: the support-side endpoint theorem is complete

On the exact seven-site star support, the two unit-charge `A1` endpoints are:

- `e0 = A1(center)`
- `s / sqrt(6) = A1(shell-average)` normalized to unit total charge

The exact endpoint coefficients are:

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

Therefore the exact projective `A1` family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

has the exact support-side law

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

This is the strongest exact endpoint-coefficient theorem currently available on
Route 2.

## Bounded part: the tensor prototype ladder

The current first tensor primitive prototype is the bounded bright pair

`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block

`A1 x {E_x, T1x}`.

Its endpoint values are explicit but bounded prototype data:

- `Theta_R^(0)(e0) = (-3.772329e-04, +3.359952e-04)`
- `Theta_R^(0)(s / sqrt(6)) = (-2.010572e-04, +4.031968e-04)`

Using the exact scalar support law, the bounded response Jacobian is

`Xi_R^(0) = d Theta_R^(0) / d delta_A1`.

This bounded ladder reconstructs the canonical `A1` family and the audited
exact-local and finite-rank baselines at bounded accuracy, but it is not an
exact tensor endpoint theorem.

## What can be forced axiom-first

The exact support theorem can be forced axiom-first:

- exact scalar endpoint coefficients at `e0` and `s / sqrt(6)`
- exact projective support law `delta_A1(r)`

The bounded prototype ladder can then be organized axiom-first around that
exact scalar variable:

- `Theta_R^(0)(q)`
- `Xi_R^(0)`
- affine reconstruction in `delta_A1`

That is the strongest endpoint-coefficient structure currently supported by
the Route-2 stack.

## Sharp blocker

The exact tensor endpoint theorem is still blocked because the retained exact
support machinery is scalar/rank-one on `A1`.

In particular:

- the exact shell/junction stack is projectively blind to the remaining
  `A1` ratio `r = s / e0`
- the exact support-to-active operator has no mixed `A1`-bright block
- the surviving scalar `delta_A1` does not produce a nonzero exact tensor
  observable on `A1 x {E_x, T1x}`

So the current route cannot force exact tensor endpoint coefficients at

- `e0`
- `s / sqrt(6)`

from the present exact support-side primitives alone.

## Missing datum/operator

The exact missing object is:

> an exact tensor-valued support observable on `A1 x {E_x, T1x}`

equivalently, the exact mixed support operator that would lift the scalar
endpoint theorem into an exact tensor endpoint theorem.

Without that operator, the tensor endpoint coefficients remain bounded
prototype data only.

## Practical conclusion

The route-2 endpoint situation is now completely separated into:

1. exact scalar endpoint theorem on `delta_A1`
2. bounded tensor prototype endpoint ladder `Theta_R^(0)`
3. exact tensor endpoint theorem blocked by the missing tensor-valued support
   observable

That is the strongest honest endpoint-coefficient result currently available
for Route 2.
