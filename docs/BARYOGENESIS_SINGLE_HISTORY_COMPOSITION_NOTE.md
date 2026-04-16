# Baryogenesis Single-History Composition Note

**Date:** 2026-04-16
**Status:** exact current-surface coupled-history reduction with bounded target on `main`
**Script:** `scripts/frontier_baryogenesis_single_history_composition.py`

## Safe statement

On the current `main` package surface, the remaining electroweak baryogenesis
object does not need to be treated as three unrelated open functionals.

Because the three stage factors already reduce to one-lane functionals on a
causal chain of retained quotient surfaces,

- `K_EWPT = F_EWPT[χ(τ)]`
- `K_tr = F_tr[ℓ_L(τ)]`
- `K_sph = F_sph[q_+(τ)]`

the full nonperturbative electroweak object reduces exactly to one composite
functional of one retained scalar history lane:

`K_NP = F_NP[χ(τ)]`

with

`F_NP[χ] := F_EWPT[χ] * F_tr[T_L[χ]] * F_sph[T_+[T_L[χ]]]`

for the exact one-lane pushforwards

- `T_L : χ -> ℓ_L`
- `T_+ : ℓ_L -> q_+`.

So the full baryogenesis bridge can be written as

`η = J * F_NP[χ(τ)]`.

This note does **not** compute `F_NP`. It closes the weaker but important
review question:

> after the three stage-specific one-lane reductions, is the open
> baryogenesis object still three independent open functionals?

Answer:

- no
- it is one coupled-history functional on one retained scalar lane

## What is already fixed upstream

The current package already fixes:

1. the transition stage `K_EWPT` lives on one scalar thermal history lane
   `χ(τ)`
2. the transport stage `K_tr` lives on one left-handed electroweak-active
   density lane `ℓ_L(τ)`
3. the sphaleron-survival stage `K_sph` lives on one washout-active `B+L`
   charge lane `q_+(τ)`
4. the exact stage decomposition

   `K_NP = K_EWPT * K_tr * K_sph`

5. the causal stage ordering

   `χ(τ) -> ℓ_L(τ) -> q_+(τ)`.

Those ingredients are enough to collapse the full open electroweak object to
one composite functional on the scalar source lane.

## Exact coupled-history composition

The retained one-lane stage notes already say:

- the transition history produces the left-handed active source lane
- the transport stage acts on that left-handed active lane
- the sphaleron-survival stage acts on the resulting washout-active charge lane

So there are exact one-lane pushforwards

- `T_L[χ] = ℓ_L`
- `T_+[ℓ_L] = q_+`.

Substituting the three stage reductions into

`K_NP = K_EWPT * K_tr * K_sph`

gives immediately

`K_NP = F_EWPT[χ] * F_tr[T_L[χ]] * F_sph[T_+[T_L[χ]]]`.

Define the composite one-lane functional

`F_NP[χ] := F_EWPT[χ] * F_tr[T_L[χ]] * F_sph[T_+[T_L[χ]]]`.

Then exactly on the current retained surface

`K_NP = F_NP[χ(τ)]`.

Since the promoted weak-flavor factorization already gave

`η = J * K_NP`,

the full baryogenesis bridge becomes

`η = J * F_NP[χ(τ)]`.

That is the exact current-surface coupled-history reduction.

## Why this is stronger than the three separate reductions

Before this note, the package still had three distinct open function symbols:

- `F_EWPT`
- `F_tr`
- `F_sph`

each on its own one-lane surface.

This note removes the remaining ambiguity that those functionals might still
be independent open objects. They are not independent on the retained current
surface, because the downstream lanes are exact quotient images of the
upstream one.

So the whole open electroweak baryogenesis object is one composite functional
on the single retained scalar source history lane.

## Bounded target geometry

Using the retained promoted weak-flavor source and observed asymmetry
normalization,

- `η_obs = 6.12e-10`
- `J = 3.330901e-5`

the exact current-surface target for the composite functional is

`F_NP,target = K_NP,target = η_obs / J = 1.837341e-5`.

So the honest remaining baryogenesis problem is now:

> compute the single coupled-history functional `F_NP[χ(τ)]` on the retained
> scalar source lane and show it lands near `1.837341e-5`.

## What this closes

This note closes the question:

> “After the three stage-specific one-lane reductions, what is the actual
> remaining electroweak baryogenesis object?”

Answer:

- one composite one-lane functional
- `K_NP = F_NP[χ(τ)]`
- hence `η = J * F_NP[χ(τ)]`

## What remains open

This note does **not** derive:

- the scalar history `χ(τ)`
- the pushforwards `T_L` and `T_+` in explicit first-principles form
- the composite functional `F_NP`
- the final first-principles `η`

So baryogenesis remains open.

But the open electroweak object is now reduced as tightly as the current
package supports without an actual nonperturbative computation.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
  fixed the exact three-stage product
- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
  reduced the transition stage to one scalar history lane
- [BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md](./BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md)
  reduced the transport stage to one left-handed active-density lane
- [BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md](./BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md)
  reduced the sphaleron-survival stage to one active charge lane

This note is the next exact reduction:

- the whole open electroweak baryogenesis object now lives on one coupled
  scalar history lane

## Validation

- [frontier_baryogenesis_single_history_composition.py](./../scripts/frontier_baryogenesis_single_history_composition.py)
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
- [BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md](./BARYOGENESIS_KEWPT_SINGLE_ORDER_PARAMETER_NOTE.md)
- [BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md](./BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md)
- [BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md](./BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md)

Current runner state:

- `frontier_baryogenesis_single_history_composition.py`: expected `PASS>0`,
  `FAIL=0`
