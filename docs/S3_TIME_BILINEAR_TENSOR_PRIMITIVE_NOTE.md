# Route 2 Exact Bilinear Tensor Primitive

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** exact new microscopic tensor primitive derived

## Verdict

The previous exact blocker was too narrow. What fails on the current support
stack is a **linear** tensor observable produced by the scalar/rank-one
support Green / Schur machinery.

What does exist exactly is a **bilinear** microscopic tensor carrier on the
support block.

## Exact ingredients

On the seven-site star support:

- the exact scalar background datum is
  - `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`
- the exact aligned bright coordinates are
  - `u_E(q) = <E_x, q>`
  - `u_T(q) = <T1x, q>`

The key exact decoupling fact is:

> `delta_A1` is exactly blind to all non-`A1` perturbations, including
> `E_x`, `T1x`, `E_perp`, `T1y`, and `T1z`.

So the scalar background coordinate and the aligned bright coordinates factor
cleanly.

## Exact primitive

Define the exact microscopic tensor carrier

`K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]]`.

Equivalently, as a 4-vector:

`vec K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

This carrier is:

- exact
- microscopic
- support-side
- prior to any metric/curvature readout

## Exact endpoint law

For the canonical `A1` background family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

the exact background scalar is

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

For unit aligned perturbations, the carrier columns are exact:

- `K_R(q_A1 + E_x) - K_R(q_A1) = [[1,0],[delta_A1(r),0]]`
- `K_R(q_A1 + T1x) - K_R(q_A1) = [[0,1],[0,delta_A1(r)]]`

So the endpoint coefficient theorem is now exact on the carrier itself:

- at `e0`: bright column = `(1, 1/6)`
- at `s / sqrt(6)`: bright column = `(1, 0)`

## Relation to the old bounded prototype

The prior bounded tensor pair

`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

is not the exact primitive. It is a bounded linear readout of the exact
carrier.

On the canonical `A1` family, the current bounded projection is

- `gamma_E = a_E u_E + b_E delta_A1 u_E`
- `gamma_T = a_T u_T + b_T delta_A1 u_T`

with the coefficients `a_E, b_E, a_T, b_T` fixed by the two bounded endpoint
values already measured from the old `eta_floor_tf` pipeline.

So the exact carrier is now separated cleanly from the bounded numerical
readout.

## What this changes

This removes the earlier blocker:

> “Route 2 lacks any exact microscopic tensor primitive.”

That statement is no longer true.

What remains open is narrower:

> identify the exact bilinear carrier `K_R` with the final Einstein/Regge
> tensor dynamics law on the current restricted class.

## Bottom line

The exact new microscopic tensor primitive is:

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

The missing theorem is no longer the existence of an exact tensor carrier. It
is the final dynamics identification of that exact carrier.
