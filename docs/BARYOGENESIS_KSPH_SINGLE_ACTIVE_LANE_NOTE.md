# Baryogenesis `K_sph` Single-Active-Lane Note

**Date:** 2026-04-16
**Status:** exact current-surface sphaleron-stage reduction with bounded target geometry on `main`
**Script:** `scripts/frontier_baryogenesis_ksph_single_active_lane.py`

## Safe statement

On the current `main` package surface, the sphaleron-survival stage of the
remaining baryogenesis bridge

`K_NP = K_EWPT * K_tr * K_sph`

does not live on a multidirectional baryon/lepton washout space.

It reduces exactly to one real functional

`K_sph = F_sph[q_+(τ)]`

of one unique washout-active charge-history lane `q_+(τ)` represented by the
`B+L` direction after quotienting out the exact protected `B-L` spectator
direction on the retained taste surface.

This note does **not** compute `F_sph`. It closes the weaker but important
review question:

> on current `main`, does the sphaleron-survival stage live on a large
> baryon/lepton charge space or on one exact active quotient lane?

Answer:

- one active quotient lane
- not a multidirectional same-surface washout space

## What is already fixed upstream

The current package already fixes:

1. the retained electroweak `SU(2)` channel carries the native
   `B+L`-violating / `B-L`-protecting structure
2. the baryon/lepton charge plane on the one-generation taste surface is
   generated exactly by `B` and `L`
3. the exact baryogenesis stage decomposition

   `K_NP = K_EWPT * K_tr * K_sph`

4. the surviving route class is generation blind on the electroweak side

Those ingredients are enough to reduce the sphaleron-survival configuration
space to one active quotient lane.

## Exact charge-plane reduction

Let the retained baryon/lepton charge plane be

`C = span{B, L}`.

On the one-generation taste surface:

- `dim C = 2`
- `B = ((B+L) + (B-L)) / 2`
- `L = ((B+L) - (B-L)) / 2`

so the same plane can be written exactly as

`C = span{B+L, B-L}`.

The existing retained baryogenesis bookkeeping already says:

- `B+L` is the washout-active electroweak direction
- `B-L` remains protected

Therefore the physically relevant sphaleron-survival stage does not depend on
the full two-dimensional charge plane. It depends on the one-dimensional
quotient

`C / span{B-L}`

which is represented by the class of `B+L`.

So the washout-active baryon/lepton history is one scalar lane `q_+(τ)`,
and the sphaleron-survival stage can be written as

`K_sph = F_sph[q_+(τ)]`.

## Why this is only one lane

Any retained same-surface baryon/lepton charge history can be written as

`q_B(τ) B + q_L(τ) L = q_+(τ) (B+L) + q_-(τ) (B-L)`

with

- `q_+(τ) = (q_B(τ) + q_L(τ)) / 2`
- `q_-(τ) = (q_B(τ) - q_L(τ)) / 2`

Because `q_-(τ)` multiplies the exact protected spectator direction, the
sphaleron-survival stage only needs the active quotient coordinate `q_+(τ)`.

That is the exact current-surface reduction.

## Bounded target geometry

Using the retained promoted weak-flavor source and observed asymmetry
normalization,

- `η_obs = 6.12e-10`
- `J = 3.330901e-5`
- `K_NP,target = η_obs / J = 1.837341e-5`

the sphaleron stage inherits the following exact benchmark geometry:

### If transition and transport stages were ideal

`K_sph = K_NP,target = 1.837341e-5`

### Equal three-stage split

`K_sph = (K_NP,target)^(1/3) = 2.638740e-2`

### If `K_EWPT = K_tr = 0.1`

`K_sph = K_NP,target / (0.1 * 0.1) = 1.837341e-3`

These are not derived values of `K_sph`. They are the correct same-surface
target geometry once the stage decomposition is fixed.

## What this closes

This note closes the question:

> “What charge-space does the sphaleron-survival factor `K_sph` actually live
> on, on current `main`?”

Answer:

- one exact washout-active quotient lane represented by `B+L`
- one real functional `F_sph[q_+(τ)]`
- not a hidden multidirectional same-surface baryon/lepton washout space

## What remains open

This note does **not** derive:

- the active history `q_+(τ)`
- the functional `F_sph`
- `K_tr`
- the final first-principles `η`

So baryogenesis remains open.

But the sphaleron-survival stage is now reduced as tightly as the current
package supports.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md](./BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md)
  fixed the exact weak-flavor source `J`
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
  fixed the exact three-stage product
- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
  reduced the transition stage to one scalar thermal history lane

This note is the complementary next reduction:

- the sphaleron-survival stage now lives on one washout-active charge lane

## Validation

- [frontier_baryogenesis_ksph_single_active_lane.py](./../scripts/frontier_baryogenesis_ksph_single_active_lane.py)
- [BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md)
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
- [PROTON_LIFETIME_DERIVED_NOTE.md](./PROTON_LIFETIME_DERIVED_NOTE.md)

Current runner state:

- `frontier_baryogenesis_ksph_single_active_lane.py`: expected `PASS>0`,
  `FAIL=0`
