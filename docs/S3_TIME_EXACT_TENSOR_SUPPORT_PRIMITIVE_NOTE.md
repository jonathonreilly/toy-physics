# Exact Tensor Support Primitive Attempt on `A1 x {E_x, T1x}`

Superseded on 2026-04-14 by
[S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](./S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md).

This note is still the correct obstruction for the **linear** support-observable
attempt. The current frontier is the exact bilinear carrier `K_R`, which avoids
that linear-support no-go.

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** microscopic support block `A1 x {E_x, T1x}`  
**Status:** exact blocker from the current support-side machinery

## Goal

Starting from the exact support-side scalar `delta_A1`, the bounded tensor
prototype `Theta_R^(0)`, and the bounded response Jacobian
`Xi_R^(0) = d Theta_R^(0) / d delta_A1`, ask whether the retained Route-2
stack already contains a genuinely new exact microscopic tensor primitive
before exterior projection on

- `A1 x {E_x, T1x}`.

The answer is no.

## Exact blocker

The current exact support-side machinery is scalar/rank-one on the current
`A1` block. It therefore cannot produce a nonzero exact tensor observable on
`A1 x {E_x, T1x}`.

The sharp obstruction is the simultaneous vanishing of the tensor-carrying
support blocks:

1. the exact support Green / Schur Hessian has no mixed `A1`-bright block,
2. the exact support-to-active response operator is rank one and charge-only,
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`.

So any exact tensor primitive built from the current exact support stack
factors through the scalar center-excess data only, and the bright block sees
nothing.

## Exact support-side facts used

The exact surviving scalar on the current support block is

- `delta_A1(q) = phi_support(center) / Q - phi_support(arm_mean) / Q`.

Its exact endpoint values are

- `delta_A1(e0) = 1/6`,
- `delta_A1(s / sqrt(6)) = 0`,

and on the canonical projective `A1` family,

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

That law is exact, but it is scalar-only. It does not generate a nonzero exact
tensor observable on the bright channels.

## Bounded comparison surface

The best current comparison object is still the bounded bright-channel pair

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block

- `A1 x {E_x, T1x}`.

The bounded response Jacobian extracted from that prototype is

- `Xi_R^(0) = d Theta_R^(0) / d delta_A1`.

This object is nonzero and structurally clean, but it is only a response
Jacobian of the bounded prototype. It is not an exact support-side tensor
observable.

## Why the exact closure fails

The new bounded tools do not repair the exact obstruction:

- `delta_A1` remains blind to the bright channels,
- `Theta_R^(0)` remains a bounded staging object,
- `Xi_R^(0)` is the derivative of that bounded staging object,
- the exact support algebra still has no mixed `A1`-bright block.

So the current stack cannot exactify the tensor support observable itself.

## What an exact tensor primitive would have to do

Any future exact microscopic tensor primitive on this route must introduce a
new support-side tensor operator before exterior projection. It cannot be
constructed by differentiating the current scalar support law or by
tensorizing the current rank-one support response.

That means the missing object is not another evaluation of `delta_A1`, nor a
better fit for `Theta_R^(0)`, nor a support-side rewrite of `Xi_R^(0)`. It is
a genuinely new microscopic tensor primitive.

## Practical conclusion

The sharpest exact obstruction on the current Route-2 support stack is:

> the exact support-side algebra is scalar/rank-one on `A1`, so it cannot
> produce a nonzero exact tensor observable on `A1 x {E_x, T1x}`.

The bounded objects

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`,
- `Xi_R^(0) = d Theta_R^(0) / d delta_A1`,

remain useful comparison surfaces, but the exact tensor support primitive is
still absent.
