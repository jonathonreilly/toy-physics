# Exact Support-Side Tensor-Observable Attack on `A1 x {E_x, T1x}`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** exact blocker from support-side machinery

## Goal

Attack the last gravity blocker directly using only the retained axiom-side
machinery:

- exact seven-site `A1` support reduction
- exact support Green matrix / support Schur data
- exact shell-amplitude factorization
- exact support-to-active response operator

The question is whether that support-side stack already contains an exact
tensor observable on the bright block

- `A1 x {E_x, T1x}`

without falling back to the numerical `eta_floor_tf` residual pipeline.

## Exact support-side result

The answer on the retained stack is negative.

The exact support Hessian of the quadratic support energy is the support Green
matrix `G_S`, and in the adapted basis

- `A1(center)`,
- `A1(shell)`,
- `E`,
- `T1`

it is block diagonal to machine precision. In particular, the mixed
`A1`-bright block relevant for `A1 x {E_x, T1x}` vanishes.

The exact candidate tensor observable obtained by projecting the support
Hessian onto

- `A1 = span{e0, s}`
- `bright = span{E_x, T1x}`

is therefore identically zero on the retained support surface:

`H_mix = P_A1^T G_S P_bright = 0`

up to machine precision.

## Support-side scalar observable is still exact

The scalar support datum survives exactly:

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

and on the canonical projective family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

it is

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

But the directional derivatives of that exact support scalar into the bright
channels are zero at the tested projective `A1` points. So the exact support
scalar does not generate a nonzero tensor observable on
`A1 x {E_x, T1x}`.

## Support-to-active operator

The exact support-to-active correction operator is rank one and factors
through total renormalized support charge. It annihilates the bright channels
as well.

So even after the exact shell-amplitude law is factored out, the retained
support-side machinery still provides only scalar `A1` data, not an exact
tensor observable on the bright block.

## Sharp blocker

The remaining tensor endpoint coefficients are still not derivable from the
retained support-side machinery alone because:

1. the exact support Hessian has no mixed `A1`-bright block,
2. the exact support scalar `delta_A1` is blind to the bright channels,
3. the exact support-to-active operator is rank one and charge-only.

Therefore the current exact support-side stack cannot produce a nonzero exact
tensor observable on `A1 x {E_x, T1x}`.

The tensor coefficients still require either:

- the numerical `eta_floor_tf` pipeline, or
- a genuinely new microscopic tensor operator beyond the current support
  machinery.

## Practical conclusion

This is the cleanest blocker statement available from the retained axiom-side
surface:

> the exact support-side machinery is scalar/rank-one on the current `A1`
> block, so it cannot by itself close the tensor observable on
> `A1 x {E_x, T1x}`.

