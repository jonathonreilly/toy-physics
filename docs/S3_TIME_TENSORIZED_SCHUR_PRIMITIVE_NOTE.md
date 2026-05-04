# Route 2 Tensorized Schur/Dirichlet Primitive

**Status:** bounded - tensorized Schur/Dirichlet primitive candidate
**Date:** 2026-04-14  
**Purpose:** build the smallest tensorized Schur/Dirichlet boundary primitive
**Primary runner:** [`scripts/frontier_s3_time_tensorized_schur_primitive.py`](../scripts/frontier_s3_time_tensorized_schur_primitive.py) (PASS=7/0, slow ~200s)
compatible with the current exact scalar Schur backbone and the existing
bounded two-channel tensor prototype

## Verdict

The exact tensor carrier is still absent on the current support stack.

But the current Route-2 frontier is now strong enough to define a genuine
tensorized Schur/Dirichlet primitive candidate that does **not** repeat the
no-go:

- exact scalar Schur boundary action
- exact scalar support endpoint law on `A1`
- bounded bright tensor prototype on the two aligned channels
  - `E_x`
  - `T1x`

The smallest tensor extension that survives the current evidence is therefore
not a new bulk metric ansatz. It is a **source-centered two-channel boundary
completion** attached to the exact scalar Schur action.

## Exact scalar backbone

The route-2 scalar backbone stays exact:

- exact `S^3` spatial closure
- exact anomaly-forced time with `d_t = 1`
- exact background `PL S^3 x R`
- exact slice generator `Lambda_R`
- exact microscopic Schur boundary action

The scalar boundary action is the exact Dirichlet/Schur quadratic

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

with `Lambda_R` symmetric positive definite on the current restricted class.

This exact scalar backbone is unchanged by the tensor extension below.

## Exact scalar support reduction

On the seven-site star support, the surviving exact scalar on the current
`A1` block is

- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

The exact projective family law is

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

The exact endpoint values are

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`.

That scalar support law is exact and stays the only exact support datum the
current support-side Schur stack can produce.

## Bounded tensor prototype

The current bounded tensor prototype remains the bright-channel pair

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block

- `A1 x {E_x, T1x}`.

This prototype is bounded, not exact, because it still comes from the current
tensor-boundary-drive frontier rather than from an exact tensor-valued support
observable.

The canonical source-side comparison surface is:

- `Theta_R^(0)(e0) = (-3.772329e-04, +3.359952e-04)`
- `Theta_R^(0)(s / sqrt(6)) = (-2.010572e-04, +4.031968e-04)`

and the current affine fit in `delta_A1` tracks the canonical `A1` family and
the audited `O_h` / finite-rank baselines at the already-observed bounded
accuracy.

## Tensorized Schur/Dirichlet primitive candidate

The smallest tensor extension consistent with the current evidence is the
source-centered quadratic completion

- `I_TS^(0)(f, a ; j) = I_R(f ; j) + 1/2 ||a - Theta_R^(0)(delta_A1(f))||^2`

where:

- `f` is the exact scalar shell trace
- `a = (a_E, a_T)` is the two-channel bright boundary vector
- `Theta_R^(0)(delta_A1(f))` injects the bounded tensor prototype as the
  source-side tensor carrier

Equivalently, this is the block-diagonal tensorized boundary action

- `I_TS^(0)(f, a ; j) = 1/2 f^T Lambda_R f - j^T f + 1/2 (a - Theta_R^(0))^T (a - Theta_R^(0))`

with a minimal positive-definite tensor kernel

- `K_TS = I_2`.

This is the smallest tensorized Schur/Dirichlet primitive that adds a genuine
two-channel tensor boundary sector without pretending the exact tensor carrier
already exists.

## Why this is the right bounded extension

The current exact support-side machinery is scalar/rank-one on `A1`:

1. the exact support Hessian has no mixed `A1`-bright block
2. the exact support-to-active operator is rank one and charge-only
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`

Therefore the exact tensor carrier is absent.

But the frontier also shows that the tensor boundary drive itself is already
bright on exactly two aligned source channels:

- `E_x`
- `T1x`

So the smallest useful tensorization is precisely a two-channel boundary
completion around the exact scalar Schur action, not a larger bulk ansatz.

## What the candidate does

The candidate primitive does three useful things:

1. it preserves the exact scalar Schur/Dirichlet backbone
2. it packages the existing bright tensor prototype as a boundary field
3. it gives the cleanest possible tensorized comparison surface for future
   exact work

In other words, it is the minimal tensorized Schur primitive worth keeping on
the Route-2 frontier until a genuine exact tensor carrier is derived.

## What it does not do

This note still does **not** claim:

1. an exact tensor-valued support observable on `A1 x {E_x, T1x}`
2. an exact tensor endpoint coefficient theorem
3. an exact support-to-slice time-coupling law
4. full GR on Route 2

The exact tensor carrier is still missing. This note gives the smallest
bounded tensorized Schur/Dirichlet primitive compatible with the current
evidence.

## Atlas-facing interpretation

This object is the right future atlas tool candidate for Route 2:

- exact scalar Schur boundary action: retained tool
- tensorized Schur/Dirichlet primitive: bounded candidate
- exact tensor carrier: still missing

That separation matters. The atlas should reuse the exact scalar backbone and
the bounded tensor completion separately, not collapse them into one ambiguous
claim.

## Bottom line

The smallest tensorized Schur/Dirichlet primitive currently supported by the
Route-2 frontier is:

- exact scalar boundary action `I_R`
- plus a two-channel boundary completion centered on
  `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

It is bounded, not exact, but it is the cleanest new tensor extension of the
Schur/Dirichlet machinery that the current atlas supports.
