# Baryogenesis `K_tr` Single-Left-Handed-Lane Note

**Date:** 2026-04-16
**Status:** exact current-surface transport-stage reduction with bounded target geometry on `main`
**Script:** `scripts/frontier_baryogenesis_ktr_single_left_handed_lane.py`

## Safe statement

On the current `main` package surface, the transport stage of the remaining
baryogenesis bridge

`K_NP = K_EWPT * K_tr * K_sph`

does not live on a mixed left/right-handed transport space.

It reduces exactly to one real functional

`K_tr = F_tr[ℓ_L(τ)]`

of one retained left-handed electroweak-active density-history lane `ℓ_L(τ)`
after quotienting out the exact right-handed singlet spectator sector on the
full-framework one-generation surface.

This note does **not** compute `F_tr`. It closes the weaker but important
review question:

> on current `main`, does the transport stage live on a large mixed-chirality
> transport space or on one exact left-handed active lane?

Answer:

- one left-handed active lane
- not a mixed-chirality same-surface transport space

## What is already fixed upstream

The current package already fixes:

1. the selected-axis surface gives the left-handed Standard Model doublet
   content

   `Q_L : (2,3)_{+1/3}`, `L_L : (2,1)_{-1}`

2. the full-framework one-generation closure adds the right-handed singlet
   completion on the `4D` chirality surface
3. the `4D` chirality operator splits

   `C^16 = C^8_L + C^8_R`

4. weak `SU(2)` is chiral and acts only on left-handed states
5. the exact baryogenesis stage decomposition already defines
   `K_tr = n_L^act / n_L^src`
   in terms of left-handed densities

Those ingredients are enough to reduce the transport-stage configuration
space to one retained left-handed active lane.

## Exact chirality-plane reduction

Let the retained chirality plane be

`C_χ = span{P_L, P_R}`

with

- `P_L = (I + γ_5)/2`
- `P_R = (I - γ_5)/2`

on the full-framework `4D` staggered surface.

The existing one-generation closure already gives:

- `dim C_χ = 2`
- `P_L + P_R = I`
- `P_L P_R = 0`
- `Tr P_L = Tr P_R = 8`

The weak interaction boundary then fixes:

- left-handed states are electroweak active doublets
- right-handed states are electroweak singlet spectators

Therefore the physically relevant transport stage does not depend on the full
two-dimensional chirality plane. It depends on the one-dimensional quotient

`C_χ / span{P_R}`

which is represented by the class of `P_L`.

So the transport-relevant chirality history is one scalar lane `ℓ_L(τ)`,
and the transport stage can be written as

`K_tr = F_tr[ℓ_L(τ)]`.

## Why this is only one lane

Any retained same-surface chirality-resolved density history can be written as

`ρ(τ) = ℓ_L(τ) P_L + r_R(τ) P_R`

with

- `ℓ_L(τ)` the left-handed active coordinate
- `r_R(τ)` the right-handed spectator coordinate

Because `r_R(τ)` multiplies the exact electroweak-singlet spectator sector,
the transport stage only needs the active quotient coordinate `ℓ_L(τ)`.

That is the exact current-surface reduction.

## Relation to the stage decomposition

The exact stage-decomposition note defines

- `n_L^src` as the left-handed CP-odd density created by the transition stage
- `n_L^act` as the portion delivered into the sphaleron-active region

So even before any numerical transport computation, the current package already
chooses the correct transport variable class: one left-handed scalar density
lane. The chirality-plane reduction above shows why this is exact on the
retained one-generation surface rather than just convenient notation.

Hence

`K_tr = n_L^act / n_L^src = F_tr[ℓ_L(τ)]`.

## Bounded target geometry

Using the retained promoted weak-flavor source and observed asymmetry
normalization,

- `η_obs = 6.12e-10`
- `J = 3.330901e-5`
- `K_NP,target = η_obs / J = 1.837341e-5`

the transport stage inherits the following exact benchmark geometry:

### If transition and sphaleron stages were ideal

`K_tr = K_NP,target = 1.837341e-5`

### Equal three-stage split

`K_tr = (K_NP,target)^(1/3) = 2.638740e-2`

### If `K_EWPT = K_sph = 0.1`

`K_tr = K_NP,target / (0.1 * 0.1) = 1.837341e-3`

These are not derived values of `K_tr`. They are the correct same-surface
target geometry once the stage decomposition is fixed.

## What this closes

This note closes the question:

> “What transport-space does the baryogenesis factor `K_tr` actually live on,
> on current `main`?”

Answer:

- one exact left-handed electroweak-active quotient lane
- one real functional `F_tr[ℓ_L(τ)]`
- not a hidden mixed-chirality same-surface transport space

## What remains open

This note does **not** derive:

- the active history `ℓ_L(τ)`
- the functional `F_tr`
- the final first-principles `η`

So baryogenesis remains open.

But the transport stage is now reduced as tightly as the current package
supports.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
  fixed the exact three-stage product
- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
  reduced the transition stage to one scalar history lane
- [BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md](./BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md)
  reduced the sphaleron-survival stage to one active charge lane

This note is the remaining complementary reduction:

- the transport stage now lives on one left-handed active density lane

## Validation

- [frontier_baryogenesis_ktr_single_left_handed_lane.py](./../scripts/frontier_baryogenesis_ktr_single_left_handed_lane.py)
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)

Current runner state:

- `frontier_baryogenesis_ktr_single_left_handed_lane.py`: expected `PASS>0`,
  `FAIL=0`
