# New Microscopic Tensor Primitive Attempt

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Last audited against atlas:** 2026-04-14

## Question

Can the remaining gravity gap be closed by a genuinely new exact microscopic
tensor primitive from the axiom/atlas, replacing `eta_floor_tf` and yielding a
nonzero exact tensor observable on

`A1 x {E_x, T1x}`?

## Best exact candidate primitive

The cleanest axiom-side candidate is the exact microscopic Dirichlet / Schur
boundary functional on the current strong-field bridge surface:

`I_R(f; j) = 1/2 f^T Lambda_R f - j^T f`

with `Lambda_R` the exact discrete DtN matrix of the lattice Laplacian.

This is the exact primitive that already closes the scalar shell law on the
current restricted class.

## Exact test result

On the retained atlas stack, this primitive does **not** generate a nonzero
tensor observable on the bright block.

The exact support Hessian is block diagonal in the adapted basis

- `A1(center)`
- `A1(shell)`
- `E`
- `T1`

and the mixed `A1`-bright block is identically zero to machine precision.

Equivalently, the candidate tensor observable obtained by projecting the exact
support Hessian onto

- `A1 = span{e0, s}`
- `bright = span{E_x, T1x}`

vanishes:

`P_A1^T G_S P_bright = 0`.

The exact support-to-active correction operator is also rank one and charge
only, so it annihilates the bright channels as well.

## Why this fails as a tensor primitive

The exact scalar support datum survives:

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`

and on the canonical projective family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

it obeys the exact law

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

But that scalar is blind to the bright channels. Its directional derivatives
into `E_x` and `T1x` vanish on the tested projective family, so it cannot lift
the tensor endpoint coefficients.

## Sharp blocker

The atlas-supported exact primitives available on the current support block are
still scalar/rank-one:

1. exact Schur/Dirichlet boundary action
2. exact shell amplitude factorization
3. exact support-side scalar `delta_A1`
4. exact support-to-active operator factoring through total charge

None of these generates a nonzero exact tensor observable on
`A1 x {E_x, T1x}`.

Therefore the broader axiom-side observable/action route does **not** supply a
new exact microscopic tensor primitive on the current retained stack.

## Practical conclusion

Route 1 is exhausted.

To replace `eta_floor_tf`, the theory needs either:

- a new microscopic tensor operator not present in the current atlas, or
- a different full-GR architecture from `FULL_GR_AXIOM_FIRST_PATHS_NOTE.md`

The exact support-side Dirichlet/Schur primitive is not enough.
