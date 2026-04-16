# Baryogenesis Source Pullback Note

**Date:** 2026-04-16
**Status:** exact current-surface source-law reduction on the retained APBC/Higgs lane
**Script:** `scripts/frontier_baryogenesis_source_pullback.py`

## Safe statement

On the current `main` baryogenesis package, the surviving positive-branch
source logarithm is no longer a free new functional.

The transition-history stage is already fixed upstream as a CP-even scalar
source-history functional on the unique retained APBC/Higgs scalar lane
`χ(τ)`, while the hierarchy observable-principle stack already fixes the
unique additive CPT-even scalar generator

`W[J] = log|det(D+J)| - log|det D|`.

Therefore, on the retained same-surface scalar source lift `χ -> J_χ`,

`S_src[χ] = W[J_χ]`

and hence

`F_EWPT[χ] = exp[W[J_χ]]`.

So on the viable positive branch the baryogenesis bridge sharpens further to

`η = J * exp[W[J_χ] - I_damp[χ]]`.

This note does **not** derive the damping functional `I_damp[χ]`, and it does
not yet derive the scalar reparameterization inside the retained source lift.
The next exact reduction on the current surface is recorded in
[BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md](./BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md),
which shows that the lift itself collapses to the homogeneous family
`J_χ = j(χ) I`.

## What is already fixed upstream

The current package already fixes:

1. the transition-history factor `K_EWPT` is the CP-even source-history
   functional of the time-dependent electroweak order-parameter background
2. `K_EWPT` lives on one unique retained scalar history lane

   `K_EWPT = F_EWPT[χ(τ)]`

3. the exact scalar observable principle on the APBC/Higgs surface

   `W[J] = log|det(D+J)| - log|det D|`

4. the positive-branch logarithmic balance

   `η = J * exp[S_src[χ] - I_damp[χ]]`.

Those ingredients are enough to identify the baryogenesis source logarithm as
the pullback of the exact scalar generator.

## Exact source-pullback law

The transition-history stage is already defined as a CP-even scalar
source-history functional on the retained order-parameter lane `χ(τ)`.

The observable-principle stack already says there is a unique additive
CPT-even scalar generator on the same surface:

`W[J] = log|det(D+J)| - log|det D|`.

Let `ι_src` denote the retained same-surface scalar source lift from the
scalar history lane into the scalar source family:

`ι_src : χ -> J_χ`.

Then the source logarithm is not a separate new object. It is exactly the
pullback of `W` along `ι_src`:

`S_src[χ] := (W ∘ ι_src)[χ] = W[J_χ]`.

Exponentiating gives the source factor itself:

`F_EWPT[χ] = exp[S_src[χ]] = exp[W[J_χ]]`.

Substituting this into the positive-branch source-damping balance yields the
sharper exact bridge

`η = J * exp[W[J_χ] - I_damp[χ]]`.

So the current source-side open content is no longer “find a source law.”
The source law is fixed. The remaining open source-side content is only the
scalar reparameterization inside the homogeneous lift `J_χ = j(χ) I`.

## Exact homogeneous slice family

On the exact homogeneous scalar source family `J = j I` on the minimal APBC
block, the observable-principle note already gives

`W_Lt(j) = 4 sum_ω log(1 + j^2 / [u_0^2 (3 + sin^2 ω)])`.

So on this exact retained slice family:

- `W_Lt(-j) = W_Lt(j)`
- `W_Lt(0) = 0`
- `W_Lt(j) > 0` for every real `j != 0`
- `W_Lt(j)` is strictly increasing in `|j|`.

The small-source curvature of this exact slice family reproduces the already
derived APBC hierarchy coefficient:

`W_Lt(j) = 8 Lt A(Lt) j^2 + O(j^4)`.

So the baryogenesis source-side functional is not only fixed abstractly. On
the exact retained homogeneous APBC slices it is already a concrete lattice
generator with explicit positivity and curvature structure.

## Immediate source-side consequence

On any retained homogeneous positive-source slice,

`S_src = W_Lt(j) >= 0`.

Combining this with the exact target balance

`S_src[χ] - I_damp[χ] = log(η_obs / J) = -10.904606206411`

gives the exact slice-family damping bound

`I_damp >= 10.904606206411`.

This is not yet a full history-level theorem, because the explicit lift
`χ -> J_χ` is still open. It is an exact retained consequence on the
homogeneous positive slice family of the same source surface.

## What this closes

This note closes the question:

> “After the logarithmic source-damping balance, is the source logarithm still
> a separate undefined baryogenesis object?”

Answer:

- no
- it is the exact pullback of the already-derived scalar generator

  `S_src[χ] = W[J_χ]`

- so the positive-branch bridge sharpens to

  `η = J * exp[W[J_χ] - I_damp[χ]]`.

## What remains open

This note does **not** derive:

- the scalar reparameterization `j(χ)` inside the homogeneous lift
- the damping functional `I_damp[χ]`
- the scalar history `χ(τ)`
- the final first-principles `η`.

So baryogenesis remains open.

But the source side is now reduced one step further: the observable law is
exactly fixed, and the remaining openness is localized to the scalar
reparameterization / history data and the damping functional.

## Relation to the existing baryogenesis notes

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  fixed the unique additive CPT-even scalar generator
- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
  reduced the transition stage to one scalar history lane
- [BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md](./BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md)
  rewrote the surviving positive-branch problem as one exact logarithmic
  balance

This note is the next exact reduction:

- it identifies the source logarithm in that balance as the pullback of the
  exact lattice scalar generator.

The next exact source-geometry reduction is recorded in
[BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md](./BARYOGENESIS_HOMOGENEOUS_SOURCE_LIFT_NOTE.md),
which shows that the retained source lift itself is exactly homogeneous.

## Validation

- [frontier_baryogenesis_source_pullback.py](./../scripts/frontier_baryogenesis_source_pullback.py)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
- [BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md](./BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md)

Current runner state:

- `frontier_baryogenesis_source_pullback.py`: expected `PASS>0`, `FAIL=0`
