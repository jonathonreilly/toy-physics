# Route 2 New Tensor Primitive: Sharp Blocker on the Current Support Stack

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** Route 2 microscopic support block `A1 x {E_x, T1x}`  
**Status:** exact blocker from the current exact support machinery

## Purpose

Route 2 has already fixed the kinematic background exactly:

- `S^3`
- anomaly-forced single-clock time
- `PL S^3 x R`
- exact slice generator `Lambda_R`
- bounded transfer bridge `T_R = exp(-Lambda_R)`

The remaining question is whether the current exact support-side stack already
contains the smallest microscopic tensor primitive needed before exterior
projection.

The answer is no.

## Exact blocker

The current exact support machinery is scalar/rank-one on the `A1` block.

That is the sharp obstruction:

1. the exact support Hessian has no mixed `A1`-bright block,
2. the exact support-to-active operator is rank one and charge-only,
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`,
4. the shell/junction stack is projectively blind to the last `A1` shape
   datum at fixed total charge.

Therefore the current exact support-side stack cannot generate a nonzero exact
tensor observable on

- `A1 x {E_x, T1x}`.

## Exact support-side primitive already in hand

The exact surviving microscopic support scalar is

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

It has exact endpoint values

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

and the exact projective law

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

That support scalar is exact and reusable, but it is still scalar only.

## Bounded tensor staging object

The clean bounded staging object on the tensor side is still

`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`.

It is useful because the current tensor boundary drive is bright only on the
aligned channels `E_x` and `T1x`, but it is not an exact tensor observable.

## Exact missing sub-primitive

The exact missing sub-primitive is now sharply identified:

> a new microscopic tensor operator beyond the current support machinery,
> before exterior projection, capable of producing a nonzero tensor
> observable on `A1 x {E_x, T1x}`.

This is the smallest exact Route-2 primitive that is not already present in the
current atlas.

## Practical conclusion

Route 2 does not yet have an exact tensor-valued support observable.

What it has instead is:

- exact scalar support data
- exact support-side blindness to the remaining projective `A1` datum
- a bounded tensor prototype `Theta_R^(0)`
- a sharp no-go for deriving `Theta_R` from the current exact support stack

So the next real Route-2 tool is not another support rewrite. It is a new
microscopic tensor primitive before exterior projection.
