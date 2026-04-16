# Baryogenesis Source-Damping Balance Note

**Date:** 2026-04-16
**Status:** exact positive-branch logarithmic balance theorem with fixed target on `main`
**Script:** `scripts/frontier_baryogenesis_source_damping_balance.py`

## Safe statement

On the viable positive branch of the current `main` baryogenesis package, the
remaining electroweak object can be written exactly as one source functional
times one nonnegative damping functional:

`F_NP[χ] = F_EWPT[χ] * exp[-I_damp[χ]]`

with `I_damp[χ] >= 0`.

Defining the source logarithm

`S_src[χ] := log F_EWPT[χ]`

whenever `F_EWPT[χ] > 0`, the full baryogenesis bridge becomes

`η = J * exp[S_src[χ] - I_damp[χ]]`.

Using the retained observed normalization,

`η_obs / J = 1.837340707514e-5`,

the exact target balance is

`S_src[χ] - I_damp[χ] = log(η_obs / J) = -10.904606206411`.

This note does **not** derive `S_src` or `I_damp`. It derives the exact
balance law they must satisfy.

## What is already fixed upstream

The current package already fixes:

1. exact flavor factorization

   `η = J * K_NP`

2. exact single-history reduction

   `K_NP = F_NP[χ(τ)]`

3. exact positive-branch damping form

   `F_NP[χ] = F_EWPT[χ] * exp[-I_damp[χ]]`

with `I_damp[χ] >= 0`.

Those ingredients are enough to derive the exact logarithmic source-damping
balance.

## Exact logarithmic balance law

On the branch where `F_EWPT[χ] > 0`, define

`S_src[χ] := log F_EWPT[χ]`.

Substituting the positive-branch damping form into the flavor-factorized
baryogenesis bridge gives

`η = J * F_EWPT[χ] * exp[-I_damp[χ]]`
`  = J * exp[S_src[χ] - I_damp[χ]]`.

So the baryogenesis problem on the viable positive branch is no longer an
unstructured functional equation. It is one exact logarithmic balance between:

- a source logarithm `S_src[χ]`
- a nonnegative damping functional `I_damp[χ]`.

## Exact observed target

Using

- `η_obs = 6.12e-10`
- `J = 3.330901e-5`

the retained target is

`K_NP,target = η_obs / J = 1.837340707514e-5`.

Taking the logarithm gives the exact target balance

`S_src[χ] - I_damp[χ] = log K_NP,target = -10.904606206411`.

So any viable first-principles route must satisfy that one exact scalar
balance law on the retained scalar history lane.

## Immediate consequences

Because `I_damp[χ] >= 0`, the source logarithm obeys the exact floor

`S_src[χ] >= log K_NP,target = -10.904606206411`.

Equivalently,

`F_EWPT[χ] >= K_NP,target = 1.837340707514e-5`.

And once a candidate source functional is derived, the required damping is
fixed exactly by

`I_damp[χ] = S_src[χ] - log K_NP,target`
`          = S_src[χ] + 10.904606206411`.

So the source and damping pieces are no longer independently unconstrained.

## Log-geometry benchmarks

The exact equal three-stage split gives

`K_EWPT = K_tr = K_sph = K_NP,target^(1/3) = 2.638740087825e-2`.

On the positive branch this means

- `S_src = log K_EWPT = -3.634868735470`
- `I_tr = -log K_tr = 3.634868735470`
- `I_sph = -log K_sph = 3.634868735470`
- `I_damp = I_tr + I_sph = 7.269737470941`

and indeed

`S_src - I_damp = -10.904606206411`.

This is not a derived physical evaluation of the three stages. It is the exact
logarithmic benchmark geometry of the retained target.

## What this closes

This note closes the question:

> “After the damping theorem, what exact relation between the remaining source
> and damping pieces is derivable without evaluating the nonperturbative
> dynamics?”

Answer:

- the open baryogenesis object is governed by one exact logarithmic balance

  `η = J * exp[S_src[χ] - I_damp[χ]]`

- with fixed target

  `S_src[χ] - I_damp[χ] = -10.904606206411`.

## What remains open

This note does **not** derive:

- the source logarithm `S_src[χ]`
- the damping functional `I_damp[χ]`
- the scalar history `χ(τ)`
- the final first-principles `η`

So baryogenesis remains open.

But the open problem is now sharpened to one exact balance law on one retained
scalar history lane.

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md](./BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md)
  reduced the electroweak object to one coupled-history functional
- [BARYOGENESIS_EFFICIENCY_PENALTY_NOTE.md](./BARYOGENESIS_EFFICIENCY_PENALTY_NOTE.md)
  rewrote the transport / washout part as one nonnegative damping functional

This note is the next exact step:

- it turns the surviving positive-branch problem into one exact logarithmic
  balance between source and damping.

## Validation

- [frontier_baryogenesis_source_damping_balance.py](./../scripts/frontier_baryogenesis_source_damping_balance.py)
- [BARYOGENESIS_EFFICIENCY_PENALTY_NOTE.md](./BARYOGENESIS_EFFICIENCY_PENALTY_NOTE.md)
- [BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md](./BARYOGENESIS_SINGLE_HISTORY_COMPOSITION_NOTE.md)
- [BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md)

Current runner state:

- `frontier_baryogenesis_source_damping_balance.py`: expected `PASS>0`,
  `FAIL=0`
