# Route 2 Exact Tensorized Action from the Bilinear Carrier

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** exact carrier/action/coupling construction; final GR identification still open

## Verdict

Once the exact bilinear support carrier `K_R` is admitted, Route 2 no longer
lacks an exact tensorized construction.

The exact scalar Schur backbone and exact Route-2 kinematic scaffold are
already in hand, so they can be combined with `K_R` into an exact tensorized
action/coupling candidate.

## Exact inputs

Already exact on the current restricted class:

- `S^3` spatial compactification
- anomaly-forced single-clock time
- background `PL S^3 x R`
- scalar Schur boundary action
  - `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`
- exact bilinear support carrier
  - `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

## Exact tensorized construction

The minimal exact tensor extension is

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`.

This is exact because every input is exact:

- `I_R` is exact
- `vec K_R` is exact
- the quadratic penalty is purely algebraic

## Exact spacetime carrier

Let

- `u_*` be the canonical normalized slice seed
- `V_R(t) = exp(-t Lambda_R) u_*`

Then the exact Route-2 spacetime carrier is

`Xi_TB(t ; q) = vec K_R(q) \otimes V_R(t)`.

This is the tensor analogue of the earlier bounded `Xi_R^(0)` construction,
but now built from an exact microscopic carrier rather than the bounded
`Theta_R^(0)` readout.

## What is now closed

On the current Route-2 build program:

- exact tensor primitive: closed
- exact endpoint carrier law: closed
- exact tensorized action/coupling construction: closed as a construction

## What is still open

What is **not** yet closed is the last theorem:

> prove that the exact tensorized carrier/action `K_R`, `I_TB`, and `Xi_TB`
> are the Einstein/Regge tensor dynamics law on the current restricted class.

So the blocker has moved from:

- “there is no exact tensor primitive”

to:

- “the exact carrier has not yet been identified uniquely with the GR tensor
  law.”

## Bottom line

Route 2 now has an exact tensor carrier and an exact tensorized action/coupling
construction on `PL S^3 x R`.

The remaining GR gap is the final dynamics identification, not the absence of
an exact tensor primitive.
