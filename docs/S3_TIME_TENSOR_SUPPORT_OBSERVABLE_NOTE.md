# Route 2 Tensor Support Observable: Exact Blocker and Bounded Prototype

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** microscopic support block `A1 x {E_x, T1x}`  
**Status:** exact blocker from the current support-side machinery

## Goal

Derive the exact tensor-valued support observable

- `Theta_R`

on the microscopic support block

- `A1 x {E_x, T1x}`

using the current route-2 primitive chain as fixed input.

The current route-2 chain supplies:

- exact `S^3`
- exact anomaly-forced time
- exact background `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer bridge `T_R = exp(-Lambda_R)`
- exact support-side scalar `delta_A1`

The question is whether those exact support-side ingredients already contain a
nonzero exact tensor observable on the bright block.

## Exact blocker

They do not.

The retained exact support machinery is scalar/rank-one on the current
`A1` block:

1. the exact support Hessian has no mixed `A1`-bright block,
2. the exact support-to-active operator is rank one and charge-only,
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`.

So the current exact support-side stack cannot produce a nonzero exact tensor
observable on

- `A1 x {E_x, T1x}`.

That is the exact obstruction.

## Exact support-side facts used

The exact support-side scalar observable is:

- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

with exact endpoint values:

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

and exact canonical projective law:

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

This is exact support-side structure, but it is scalar only.

## Bounded prototype

The clean bounded staging object is still:

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

where `gamma_E` and `gamma_T` are the aligned `E_x` and `T1x` bright-channel
coefficients after exact shell-amplitude normalization.

This prototype is useful, but it is not an exact tensor observable.

## Exact missing sub-primitive

The exact missing sub-primitive is now sharply identified:

> a new microscopic tensor operator beyond the current support machinery,
> before exterior projection, capable of producing a nonzero tensor observable
> on `A1 x {E_x, T1x}`.

The current support-side Dirichlet/Schur stack is insufficient.

## Practical conclusion

Route 2 does not yet have an exact tensor-valued support observable.

What it has instead is:

- exact scalar support data
- exact support-side blindness to the remaining projective `A1` datum
- a bounded tensor prototype `Theta_R^(0)`
- a sharp no-go for deriving `Theta_R` from the current exact support stack

So the next real Route-2 tool is not another support rewrite. It is a new
microscopic tensor primitive.
