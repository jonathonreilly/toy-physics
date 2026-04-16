# Baryogenesis Homogeneous Source-Lift Note

**Date:** 2026-04-16
**Status:** exact retained-source-geometry reduction on the APBC/Higgs lane
**Script:** `scripts/frontier_baryogenesis_homogeneous_source_lift.py`

## Safe statement

On the current `main` baryogenesis package, the remaining same-surface source
lift does not require a general local matrix-valued scalar source.

Because:

1. the transition stage already reduces to one retained scalar history lane
   `χ(τ)`,
2. the scalar observable principle already fixes local scalar sources as

   `J = sum_x j_x P_x`,

3. the physical order parameter is local, bosonic, and CPT-even, so its
   temporal support must lie on the unique resolved Klein-four APBC orbit at
   `L_t = 4`,
4. the spatial hierarchy surface is selected by the existence of a finite
   intensive `3+1` order-parameter limit,

the admissible retained same-surface source lifts collapse to the one-
dimensional homogeneous scalar family

`J_χ = j(χ) I`.

So the source side sharpens from

`S_src[χ] = W[J_χ]`

to

`S_src[χ] = W[j(χ) I]`

and the viable positive-branch baryogenesis bridge becomes

`η = J * exp[W(j(χ) I) - I_damp[χ]]`.

This note does **not** derive the scalar reparameterization `j(χ)` or the
damping functional `I_damp[χ]`. It removes the remaining matrix-valued lift
ambiguity.

## What is already fixed upstream

The current package already fixes:

1. the transition stage lives on one unique scalar history lane

   `K_EWPT = F_EWPT[χ(τ)]`

2. the exact scalar observable generator

   `W[J] = log|det(D+J)| - log|det D|`

3. the exact source pullback law

   `S_src[χ] = W[J_χ]`

4. the physical order parameter is local, bosonic, and CPT-even, with unique
   resolved APBC temporal orbit `L_t = 4`
5. the hierarchy source surface is intensive in `3+1`, so the retained
   scalar lane does not carry independent spatial site labels.

Those ingredients are enough to reduce the remaining source lift to the
homogeneous scalar family.

## Exact temporal fixed-subspace theorem

On the resolved APBC orbit at `L_t = 4`, let the four temporal support
coefficients be arranged as a vector

`v = (v_1, v_2, v_3, v_4)^T`.

The bosonic-bilinear selector says the physical order parameter is closed under

- sign: `z -> -z`
- conjugation: `z -> z*`.

These two operations generate the Klein-four permutation action on the
resolved orbit. The common fixed subspace of that action is exactly
one-dimensional:

`Fix(Klein_4) = span{(1,1,1,1)^T}`.

So any admissible retained temporal source profile on the resolved orbit is
uniform.

This removes all temporally inhomogeneous same-surface lift freedom on the
retained orbit.

## Exact homogeneous lift

The observable principle already allows local scalar sources of the form

`J = sum_x j_x P_x`.

But the current baryogenesis reduction permits only one retained scalar lane,
not a family of independent local source coordinates.

The spatial hierarchy surface is already selected by the existence of a finite
intensive `3+1` order-parameter limit, so the retained scalar lane does not
carry independent spatial site labels. And the temporal fixed-subspace theorem
above removes all non-uniform temporal labels on the resolved orbit.

Therefore the admissible retained source lift is exactly the homogeneous
scalar family

`J_χ = j(χ) I`

for one real scalar reparameterization `j(χ)`.

Substituting into the exact source-pullback law gives

`S_src[χ] = W[j(χ) I]`.

So the viable positive-branch bridge sharpens to

`η = J * exp[W(j(χ) I) - I_damp[χ]]`.

## Exact homogeneous APBC family

On the exact homogeneous APBC family the scalar generator is already explicit:

`W_Lt(j) = 4 sum_ω log(1 + j^2 / [u_0^2 (3 + sin^2 ω)])`.

So the retained baryogenesis source side is now reduced to one scalar
reparameterization into a known exact source family, not to a general
matrix-valued local-source problem.

On the viable positive branch one may take `j(χ) >= 0`, since `W_Lt(j)` is
even in `j`.

## What this closes

This note closes the question:

> “After the source-pullback theorem, does baryogenesis still need a general
> same-surface matrix-valued source lift?”

Answer:

- no
- the retained source lift is exactly homogeneous

  `J_χ = j(χ) I`

- so the source side is reduced to one scalar reparameterization into the
  exact homogeneous APBC source family.

## What remains open

This note does **not** derive:

- the scalar reparameterization `j(χ)`
- the damping functional `I_damp[χ]`
- the scalar history `χ(τ)`
- the final first-principles `η`.

So baryogenesis remains open.

But the source-side lift is now reduced as tightly as the current retained
surface supports: the remaining freedom is one scalar reparameterization, not
an arbitrary matrix-valued local source.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
  reduced the transition stage to one scalar history lane
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  fixed the exact scalar generator and the local scalar source family
- [BARYOGENESIS_SOURCE_PULLBACK_NOTE.md](./BARYOGENESIS_SOURCE_PULLBACK_NOTE.md)
  identified the source logarithm as the pullback of that generator

This note is the next exact reduction:

- it shows that the retained source lift itself is exactly homogeneous on the
  APBC/Higgs lane.

## Validation

- [frontier_baryogenesis_homogeneous_source_lift.py](./../scripts/frontier_baryogenesis_homogeneous_source_lift.py)
- [BARYOGENESIS_SOURCE_PULLBACK_NOTE.md](./BARYOGENESIS_SOURCE_PULLBACK_NOTE.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](./HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
- [HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md](./HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)

Current runner state:

- `frontier_baryogenesis_homogeneous_source_lift.py`: expected `PASS>0`,
  `FAIL=0`
