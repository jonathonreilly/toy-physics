# Route 2 Mixed Support Operator: Exact Blocker on `A1 x {E_x, T1x}`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** microscopic support Green / resolvent / operator layer  
**Status:** exact blocker from the current support algebra

## Goal

Look for an exact mixed support operator on the microscopic support block

- `A1 x {E_x, T1x}`

that survives before exterior projection and could underlie the missing tensor
observable for Route 2.

The candidate operator is the mixed support block

- `M_mix = P_A1^T G_S P_bright`

where `G_S` is the exact support Green matrix in the adapted basis, `P_A1`
selects the `A1` block, and `P_bright` selects the bright tensor channels
`{E_x, T1x}`.

## Exact blocker

On the current exact support stack, this mixed operator is zero to machine
precision.

The retained exact support machinery is still scalar/rank-one on the current
`A1` block:

1. the exact support Green matrix has no mixed `A1`-bright block,
2. the exact support-to-active operator is rank one and charge-only,
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`.

So the current exact support algebra cannot produce a nonzero mixed operator
on

- `A1 x {E_x, T1x}`

before exterior projection.

## Exact support-side facts used

The exact scalar support observable is

- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

with exact endpoint values

- `delta_A1(e0) = 1/6`
- `delta_A1(s / sqrt(6)) = 0`

and exact canonical projective law

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

This is exact support-side structure, but it is scalar only.

## Bounded prototype

The clean bounded staging object remains

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

where `gamma_E` and `gamma_T` are the aligned `E_x` and `T1x` bright-channel
coefficients after exact shell-amplitude normalization.

This prototype is useful, but it is not an exact tensor observable.

## Practical conclusion

Route 2 does not yet have an exact mixed support operator on the microscopic
`A1 x {E_x, T1x}` block.

What it has instead is:

- exact scalar support data
- exact support-side blindness to the remaining projective `A1` datum
- a bounded tensor prototype `Theta_R^(0)`
- a sharp no-go for deriving the missing tensor observable from the current
  exact support stack

So the next real Route-2 tool is not another support rewrite. It is a new
microscopic tensor primitive beyond the current support algebra.
