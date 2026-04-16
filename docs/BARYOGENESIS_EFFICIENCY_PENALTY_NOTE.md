# Baryogenesis Efficiency-Penalty Note

**Date:** 2026-04-16
**Status:** exact current-surface contractive semigroup theorem with additive penalty form on the viable positive branch
**Script:** `scripts/frontier_baryogenesis_efficiency_penalty.py`

## Safe statement

On the retained positive-orientation branch relevant to the observed positive
baryon asymmetry and the promoted `J > 0` package, the transport and
sphaleron-survival stages of the remaining baryogenesis bridge

`K_NP = K_EWPT * K_tr * K_sph`

are exact contractive efficiency factors on their retained one-lane surfaces.

So on that branch:

- `0 <= K_tr <= 1`
- `0 <= K_sph <= 1`
- `0 <= K_NP <= K_EWPT`

and, whenever `K_tr > 0` and `K_sph > 0`, there are exact nonnegative penalty
functionals

- `I_tr := -log K_tr >= 0`
- `I_sph := -log K_sph >= 0`

such that

`K_NP = K_EWPT * exp[-I_tr - I_sph]`.

Pulled back through the current single-history reduction, this becomes

`F_NP[χ] = F_EWPT[χ] * exp[-I_tr[χ] - I_sph[χ]]`.

Equivalently, defining one combined nonnegative damping functional

`I_damp[χ] := I_tr[χ] + I_sph[χ] >= 0`

gives the sharper one-source / one-damping form

`F_NP[χ] = F_EWPT[χ] * exp[-I_damp[χ]]`.

This note does **not** evaluate `I_tr` or `I_sph`. It derives the exact
geometry of the transport / washout part of the open baryogenesis object.

## What is already fixed upstream

The current package already fixes:

1. exact weak-flavor factorization

   `η = J * K_NP`

2. exact stage decomposition

   `K_NP = K_EWPT * K_tr * K_sph`

3. one-lane reductions

   - `K_EWPT = F_EWPT[χ(τ)]`
   - `K_tr = F_tr[ℓ_L(τ)]`
   - `K_sph = F_sph[q_+(τ)]`

4. exact downstream quotient extractors on the coupled-history surface

   - `ℓ_L(τ) = Tr(P_L ρ_χ(τ)) / 8`
   - `q_+(τ) = Tr(Q_{ℓ_L}(τ)) / 4`.

Those ingredients are enough to derive the exact contractive / penalty
structure of the transport and sphaleron stages on the viable positive branch.

## Exact contractive stage geometry

Fix the retained orientation relevant to the observed positive asymmetry and
promoted `J > 0`. On that branch let:

- `n_L^src >= 0` be the source magnitude created by the transition history
- `n_L^act >= 0` be the magnitude delivered into the sphaleron-active region
- `η_f >= 0` be the final frozen asymmetry magnitude

with the exact stage definitions

- `K_EWPT = n_L^src / J`
- `K_tr = n_L^act / n_L^src`
- `K_sph = η_f / n_L^act`.

Because `n_L^act` is by definition the portion of the created source delivered
into the active region,

`0 <= n_L^act <= n_L^src`.

Because `η_f` is by definition the surviving asymmetry after conversion /
freeze-out from the active source,

`0 <= η_f <= n_L^act`.

Therefore

- `0 <= K_tr <= 1`
- `0 <= K_sph <= 1`.

Multiplying by `K_EWPT >= 0` gives

`0 <= K_NP = K_EWPT * K_tr * K_sph <= K_EWPT`.

So transport and sphaleron stages cannot amplify the source on the viable
positive branch. They can only preserve it partially or suppress it.

## Exact semigroup / telescoping structure

Insert any intermediate same-surface transport magnitude `n_L^mid` with

`n_L^src >= n_L^mid >= n_L^act >= 0`.

Then exactly

`K_tr = n_L^act / n_L^src`
`     = (n_L^mid / n_L^src) * (n_L^act / n_L^mid)`.

So the transport efficiency telescopes multiplicatively across any
same-surface partition.

Likewise insert any intermediate surviving asymmetry magnitude `η_mid` with

`n_L^act >= η_mid >= η_f >= 0`.

Then exactly

`K_sph = η_f / n_L^act`
`      = (η_mid / n_L^act) * (η_f / η_mid)`.

So the sphaleron-survival efficiency also telescopes multiplicatively across
any same-surface partition.

That is the exact semigroup geometry of the suppressive stages.

## Exact additive penalty form

On the nonzero branch where `K_tr > 0` and `K_sph > 0`, define

- `I_tr := -log K_tr`
- `I_sph := -log K_sph`.

Since `0 < K_tr <= 1` and `0 < K_sph <= 1`, these obey

- `I_tr >= 0`
- `I_sph >= 0`.

Then exactly

`K_tr = exp[-I_tr]`
`K_sph = exp[-I_sph]`

and therefore

`K_NP = K_EWPT * exp[-I_tr - I_sph]`.

Using the single-history reduction, pull these penalties back to the retained
scalar lane:

- `I_tr[χ] := -log F_tr[Π_L[ρ_χ]]`
- `I_sph[χ] := -log F_sph[Π_+[Q_{ℓ_L}]]`

whenever the corresponding stage factors are positive.

So on the viable nonzero branch the full coupled-history functional obeys

`F_NP[χ] = F_EWPT[χ] * exp[-I_tr[χ] - I_sph[χ]]`.

Equivalently

`F_NP[χ] = F_EWPT[χ] * exp[-I_damp[χ]]`

with

`I_damp[χ] := I_tr[χ] + I_sph[χ] >= 0`.

This is the exact additive-penalty form of the open electroweak object on the
current package surface.

## Immediate target consequence

The current retained target is

`K_NP,target = 1.837341e-5`.

Since `K_NP <= K_EWPT` on the viable positive branch, any successful same-surface
route must satisfy the exact source floor

`K_EWPT >= 1.837341e-5`.

If transport or sphaleron survival are significantly suppressive, then the
required source factor must be correspondingly larger.

## What this closes

This note closes the question:

> “After the one-lane reductions and quotient extractors, what exact relation
> between the remaining baryogenesis functionals is derivable without any
> nonperturbative evaluation?”

Answer:

- transport and sphaleron stages are exact contractive efficiencies
- they telescope multiplicatively under same-surface partition
- equivalently they contribute nonnegative additive penalties
- the coupled-history functional can therefore be written as

  `F_NP[χ] = F_EWPT[χ] * exp[-I_tr[χ] - I_sph[χ]]`

  on the viable nonzero branch
- equivalently the same branch carries only one source functional and one
  combined nonnegative damping functional:

  `F_NP[χ] = F_EWPT[χ] * exp[-I_damp[χ]]`.

## What remains open

This note does **not** derive:

- the source functional `F_EWPT[χ]`
- the penalty functionals `I_tr[χ]`, `I_sph[χ]`
- the scalar history `χ(τ)`
- the final first-principles `η`

So baryogenesis remains open.

But the transport / washout part of the open object is now reduced from two
arbitrary multiplicative factors to two nonnegative additive penalty
functionals, equivalently one combined nonnegative damping functional, on the
retained scalar-history surface.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
  fixed the exact three-stage product
- [BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md](./BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md)
  reduced the transport stage to one left-handed active lane
- [BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md](./BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md)
  reduced the sphaleron-survival stage to one active charge lane
- [BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md](./BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md)
  reduced the whole electroweak object to one coupled-history functional

This note is the next exact reduction:

- it proves the transport / washout part of that coupled-history functional is
  an additive penalty rather than an arbitrary unconstrained multiplier.

## Validation

- [frontier_baryogenesis_efficiency_penalty.py](./../scripts/frontier_baryogenesis_efficiency_penalty.py)
- [BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md](./BARYOGENESIS_KNP_STAGE_DECOMPOSITION_NOTE.md)
- [BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md](./BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md)
- [BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md](./BARYOGENESIS_KTR_SINGLE_LEFT_HANDED_LANE_NOTE.md)
- [BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md](./BARYOGENESIS_KSPH_SINGLE_ACTIVE_LANE_NOTE.md)

Current runner state:

- `frontier_baryogenesis_efficiency_penalty.py`: expected `PASS>0`, `FAIL=0`
