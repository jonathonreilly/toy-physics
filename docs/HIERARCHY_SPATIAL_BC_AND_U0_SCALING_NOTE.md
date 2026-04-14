# Hierarchy Spatial-BC And `u_0`-Scaling Note

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_hierarchy_spatial_bc_and_u0_scaling.py`

## Question

Can the two remaining support objections be narrowed on the exact minimal
`3+1` hierarchy block?

1. Why spatial APBC on even `L_s = 2`?
2. Why the native tadpole scaling should carry exactly one power of `u_0` per
   hopping amplitude rather than two?

## Exact result

Yes.

With temporal APBC fixed, both spatial BC choices on the minimal cube admit
exact determinant formulas:

- spatial APBC:
  `|det(D+m)| = prod_omega [m^2 + u_0^2 (3 + sin^2 omega)]^4`
- spatial PBC:
  `|det(D+m)| = prod_omega [m^2 + u_0^2 sin^2 omega]^4`

So the zero-mass determinant has the same exact coupling power in both cases:

`|det D| propto u_0^(8 L_t)`

In particular on the minimal temporal block:

`|det D| propto u_0^16`

That retires the old claim that spatial APBC is needed to get the exponent.
It is **not** needed for the exponent.

## What spatial APBC is needed for

The real distinction appears on the **intensive 3+1 effective-potential**
surface.

The exact small-m coefficient is:

`Delta f(L_t, m) = A(L_t) m^2 + O(m^4)`

For spatial APBC:

- `A_2 = 1 / (8 u_0^2)`
- `A_inf = 1 / (4 sqrt(3) u_0^2)`

so the intensive temporal average is finite.

For spatial PBC:

`A_PBC(L_t) = L_t / (4 u_0^2)`

exactly, so the would-be intensive temporal average grows linearly with `L_t`
and has **no finite `3+1` limit**.

That is the clean selection rule:

> spatial APBC is not selected by exponent counting; it is selected by the
> existence of a finite intensive `3+1` order-parameter limit on the minimal
> hierarchy block.

## Native `u_0` scaling

The exact free-energy density satisfies:

`Delta f(L_t, u_0, m) = Delta f(L_t, 1, m / u_0)`

for both spatial BC choices.

So the local hierarchy observable depends on `u_0` only through the ratio
`m / u_0`.

Equivalently, the small-m coefficient scales exactly as:

`A(L_t, u_0) propto u_0^(-2)`

This is the exact local statement that the hierarchy observable carries **one
power of `u_0` per field insertion pair / hopping amplitude**, not two. A
quadratic `u_0^(-2)` tadpole factor at the link level would oversubtract the
exact local scaling.

In that precise sense, the framework-native tadpole normalization is linear in
`1 / u_0`, which is the exact power-counting content behind the `alpha_LM`
route.

## What this closes

1. the exponent `16` is spatial-BC independent on the minimal block
2. spatial APBC is selected by finiteness of the intensive `3+1` hierarchy
   observable, not by raw determinant power
3. the exact local hierarchy observable has linear `1 / u_0` tadpole scaling,
   not quadratic

## What is still open

This still does **not** finish the full hierarchy theorem.

The remaining load-bearing step is now even narrower:

> derive why the physical electroweak order parameter uses the exact
> dimension-4 intensive normalization on the minimal `L_t = 2` block, or a
> derived function of the exact endpoint pair `{L_t = 2, L_t -> infinity}`.

So the spatial-BC and `u_0`-power objections are now support-level. The only
real remaining theorem is the final **intensive order-parameter selection**
step.
