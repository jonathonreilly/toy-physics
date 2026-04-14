# Route 2 Exact Tensorized Action/Coupling Law on `PL S^3 x R`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Ownership:** Route 2 / action-coupling pass  
**Purpose:** try to upgrade the bounded tensorized Schur primitive and bounded
spacetime tensor carrier into an exact tensorized action/coupling law on the
route-2 background `PL S^3 x R`

## Verdict

The exact Route-2 action/coupling law is still **blocked**.

What the current route already gives is enough to define a clean bounded
candidate:

- exact `S^3` spatial closure
- exact anomaly-forced time
- exact background `PL S^3 x R`
- exact scalar Schur boundary action
- exact scalar support endpoint law on `delta_A1`
- bounded bright-channel tensor prototype `Theta_R^(0)`
- bounded spacetime tensor carrier `Xi_R^(0)`

But the exact tensor-valued support observable on
`A1 x {E_x, T1x}` is still missing. Without that exact microscopic tensor
primitive, the bounded tensorized Schur primitive and bounded spacetime
carrier remain staging tools rather than theorem-grade action/coupling laws.

## Exact ingredients already in hand

### Exact kinematic background

The background scaffold remains exact:

- `S^3` topology is closed
- anomaly-forced time is exact with a single clock
- the natural lift is `PL S^3 x R`

These are the retained route-2 kinematic tools.

### Exact scalar Schur backbone

The exact microscopic shell action is the Schur-complement boundary energy

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

with `Lambda_R` symmetric positive definite on the current restricted class.
This is the exact scalar backbone that any tensorized action must extend.

### Exact scalar support observable

On the seven-site star support, the only exact microscopic support datum that
survives the shell/junction blindness theorem is

- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

with exact projective family law

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

and exact endpoint values

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

That scalar support law is exact, but it is still scalar-only.

## Bounded tensorized primitives to keep

### Bounded tensorized Schur primitive

The cleanest current tensorized Schur completion is the bounded candidate

- `I_TS^(0)(f, a ; j) = I_R(f ; j) + 1/2 ||a - Theta_R^(0)(delta_A1(f))||^2`

with

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the bright support block

- `A1 x {E_x, T1x}`.

This is the right atlas-facing bounded action candidate. It preserves the
exact scalar Schur backbone and packages the current bright tensor response
as a source-side boundary field.

### Bounded spacetime tensor carrier

The cleanest current spacetime carrier candidate remains

- `Xi_R^(0)(t ; q) = Theta_R^(0)(q) \otimes exp(-t Lambda_R) u_*`

where `u_*` is the canonical normalized slice seed.

This is the smallest plausible route-2 spacetime tensor mediator on
`PL S^3 x R`, but it is bounded because `Theta_R^(0)` is bounded.

## Exactification attempt

The attempted exact tensorized action would need to promote the bounded
candidate above into an exact tensor action on `PL S^3 x R`, and then couple
it exactly to the slice generator `Lambda_R`.

That attempt fails for one sharp reason:

- the current exact support-side machinery is scalar/rank-one on `A1`
- the exact support Hessian has no mixed `A1`-bright block
- the exact support-to-active operator is charge-only
- the exact support scalar `delta_A1` is blind to `E_x` and `T1x`

So there is no exact tensor-valued support observable on
`A1 x {E_x, T1x}` to serve as the source-side input for an exact tensorized
action/coupling law.

## Sharp blocker

The exact blocker is now reduced to a single missing primitive:

> an exact tensor-valued support observable on `A1 x {E_x, T1x}` before
> exterior projection, with exact endpoint coefficients and an exact
> support-to-slice coupling law.

Without that primitive, the route can only produce:

- exact kinematics on `PL S^3 x R`
- exact scalar Schur dynamics on the strong-field class
- bounded tensorized action/coupling candidates

It cannot produce a theorem-grade exact tensorized action on the route-2
background.

## Atlas-facing interpretation

For the derivation atlas, the correct separation is:

- exact retained tools:
  - `I_R`
  - `delta_A1`
- bounded atlas tools to keep:
  - `Theta_R^(0)`
  - `I_TS^(0)`
  - `Xi_R^(0)`
- exact primitive still missing:
  - `Theta_R` on `A1 x {E_x, T1x}`

So the bounded tensorized Schur and spacetime carrier are real atlas tools,
but they are not yet exact closures.

## Bottom line

Route 2 does **not** yet have an exact tensorized action/coupling law on
`PL S^3 x R`.

The smallest new primitive still required is:

- an exact tensor-valued support observable on
  `A1 x {E_x, T1x}`

with exact endpoint coefficients and an exact support-to-slice coupling law.

