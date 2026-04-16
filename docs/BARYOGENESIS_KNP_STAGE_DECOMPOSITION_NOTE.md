# Baryogenesis `K_NP` Stage-Decomposition Note

**Date:** 2026-04-16
**Status:** exact stage-decomposition theorem with bounded target geometry on `main`
**Script:** `scripts/frontier_baryogenesis_knp_stage_decomposition.py`

## Safe statement

On the current `main` package surface, the remaining baryogenesis object

`η = J * K_NP`

can be decomposed exactly into three same-surface nonperturbative stages:

`K_NP = K_EWPT * K_tr * K_sph`

where:

- `K_EWPT` is the out-of-equilibrium transition-history source factor
- `K_tr` is the transport / diffusion transfer factor into the sphaleron-active
  region
- `K_sph` is the baryon-conversion / survival factor through sphaleron
  freeze-out

This does **not** compute the stages. It fixes the correct object-level
decomposition and the target geometry each future same-surface computation must
hit.

## What is derived here

The current package already fixes:

1. exact weak-flavor factorization

   `η = J * K_NP`

2. the surviving route class as genuinely nonperturbative electroweak
   transition / sphaleron / transport dynamics

Once those two statements are in place, the remaining object has a unique
review-safe stage decomposition.

## Exact stage decomposition

Let:

- `n_L^src` be the left-handed CP-odd density created by the electroweak
  transition history, normalized by the exact weak-flavor source `J`
- `n_L^act` be the portion delivered into the sphaleron-active region
- `η_f` be the final frozen baryon-to-photon ratio

Define the three real CP-even stage factors by successive ratios:

- `K_EWPT = n_L^src / J`
- `K_tr = n_L^act / n_L^src`  when `n_L^src != 0`, else `0`
- `K_sph = η_f / n_L^act`     when `n_L^act != 0`, else `0`

Then the exact telescoping identity is

`η_f = J * K_EWPT * K_tr * K_sph`.

So on the current package surface,

`K_NP = K_EWPT * K_tr * K_sph`.

That is the exact remaining baryogenesis object.

## Structural meaning of the three factors

### 1. Transition-history factor `K_EWPT`

This is the CP-even source-history functional of the time-dependent
electroweak order-parameter background.

It vanishes if there is no relevant out-of-equilibrium transition history.

### 2. Transport factor `K_tr`

This is the CP-even transfer factor carrying the created chiral density into
the sphaleron-active region.

It vanishes if no relevant transport / diffusion channel is active.

### 3. Sphaleron-survival factor `K_sph`

This is the CP-even conversion-and-freeze-out factor mapping the transported
chiral density into the final frozen baryon asymmetry.

It vanishes if there is no effective `B+L` conversion or if complete washout
erases the generated asymmetry.

## Exact consequence

This means the open baryogenesis lane is no longer one undifferentiated symbol.

It is one exact three-stage object:

`η = J * K_EWPT * K_tr * K_sph`.

The flavor part is already closed in `J`.
The electroweak part is already decomposed into the three computations that
still need to be done.

## Target geometry on the current surface

Using the retained target

`K_NP,target = 1.837341e-5`,

the stage product target is

`K_EWPT * K_tr * K_sph = 1.837341e-5`.

This immediately gives useful benchmark geometries:

### Equal three-stage split

If the three stages contribute equally under an efficiency normalization, then

`K_EWPT = K_tr = K_sph = K_NP^(1/3) = 2.638740e-2`.

### One ideal stage, two equal stages

If one stage is effectively ideal and the other two contribute equally, then

`K_other = sqrt(K_NP) = 4.286422e-3`.

### Two ideal stages, one limiting stage

If two stages are effectively ideal, the remaining limiting stage must carry
the whole target:

`K_limit = K_NP = 1.837341e-5`.

## Reviewer-safe reading

This note does **not** say:

- that the three stage factors are already computed
- that they are all independently bounded by a theorem on the current surface
- that the electroweak transition is already closed

It does say:

- the open object is exactly decomposed into the right three stages
- the exact target product is fixed
- future same-surface work now knows which stage is failing once any one of
  them is computed

## What this closes

This note closes the question:

> “What exactly is the nonperturbative electroweak object we still need to
> compute?”

Answer:

- not a single opaque symbol anymore
- exactly the three-stage product

  `K_NP = K_EWPT * K_tr * K_sph`

on the retained lattice surface.

## What remains open

This note does **not** derive:

- `K_EWPT`
- `K_tr`
- `K_sph`
- the final first-principles `η`

So baryogenesis remains open.

But the open object is now decomposed as tightly as the current package
supports.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md](./BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md)
  isolated the surviving route class
- [BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md](./BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md)
  isolated the exact weak-flavor source `J`
- this note isolates the exact electroweak-stage decomposition of the
  remaining functional `K_NP`

The next same-surface reduction of the transition-history stage is recorded in
[BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md),
which shows that `K_EWPT` lives on one exact scalar thermal history lane.
The complementary same-surface reduction of the transport stage is recorded in
[BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md](./BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md),
which shows that `K_tr` lives on one exact left-handed active density lane.
The complementary same-surface reduction of the sphaleron-survival stage is
recorded in
[BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md](./BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md),
which shows that `K_sph` lives on one exact washout-active `B+L` charge lane.
Those three stage-specific one-lane reductions compose further into the single
coupled-history reduction recorded in
[BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md](./BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md),
which shows that the whole open electroweak object reduces to
`K_NP = F_NP[χ(τ)]`.

## Validation

- [frontier_baryogenesis_knp_stage_decomposition.py](./../scripts/frontier_baryogenesis_knp_stage_decomposition.py)
- [BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md](./BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md)
- [BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md](./BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md)
- [BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md)

Current runner state:

- `frontier_baryogenesis_knp_stage_decomposition.py`: expected `PASS>0`,
  `FAIL=0`
