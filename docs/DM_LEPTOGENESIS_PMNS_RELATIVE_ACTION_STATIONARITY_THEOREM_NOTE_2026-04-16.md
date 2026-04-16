# DM Leptogenesis PMNS Relative-Action Stationarity Theorem

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem.py`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Question

After the PMNS-assisted `N_e` flavored-DM route was reduced to the fixed seed
surface plus one off-seed selector, was the remaining selector law still an
extra postulate?

More sharply:

- the exact observable principle already gives the scalar generator
  `W = log|det(D+J)| - log|det D|`
- the fixed native `N_e` seed pair is already derived
- the favored closure column is already fixed on the current branch
- exact closure is reached by minimizing

`S_rel(H_e || H_seed) = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3`

The remaining issue was whether this stationarity/minimization step was merely
an extra selector ansatz.

## Bottom line

On the current branch, no.

The seed-relative bosonic action is the exact Legendre-dual effective action
of the sole-axiom scalar observable generator on the positive charged block.
So constrained minimization of `S_rel` is not an imported information
principle. It is the native effective-action selector attached to the exact
observable grammar.

On the fixed `N_e` seed surface and the already-derived favored closure column,
sampled constrained solves expose more than one stationary branch, but only one
branch is the unique lowest-action closure branch among all sampled feasible
starts. That branch is a strict local minimum under sampled near-exact
closure-preserving perturbations.

## Exact effective-action identity

Write the seed-normalized charged Hermitian block as

`Y = H_seed^(-1/2) H_e H_seed^(-1/2)`.

Then the seed-relative bosonic action is

`S_rel(Y) = Tr(Y) - log det(Y) - 3`.

For Hermitian source matrices `K > -I`, define the seed-normalized scalar
observable generator

`W_rel(K) = log det(I + K)`.

Then

`S_rel(Y) = sup_K [ W_rel(K) - Tr(KY) ]`

with unique maximizer

`K_* = Y^(-1) - I`.

So `S_rel` is the exact Legendre dual / effective action of the sole-axiom
observable generator on the positive charged block.

This is the key closure step. The selector objective is no longer a separate
principle. It is the effective action already implied by the exact source
generator.

## Closure-surface stationarity

On the refreshed DM branch:

1. the fixed native charged seed surface is exact
2. the favored closure column on that surface is fixed by the exact transport
   extremal class
3. the flavored closure condition is exact:

`eta_{i_*}(H_e) / eta_obs = 1`

The selected PMNS-assisted closure source is then the constrained minimum of
the effective action:

`delta[ S_rel(H_e || H_seed) - lambda (eta_{i_*}(H_e)/eta_obs - 1) ] = 0`,

with the physically selected branch being the **lowest-action** solution of
this equation.

The script verifies:

- the constrained Euler-Lagrange equation
- positive tangent Hessian on the selected closure branch
- more than one sampled stationary branch
- uniqueness of the lowest-action branch across all sampled feasible starts
- strict local minimality under sampled near-exact closure-preserving
  perturbations

## Numerical result on the current branch

The stationary source is the same observable-relative-action closure source:

- `x_stat = (0.471675, 0.553811, 0.664514)`
- `y_stat = (0.208063, 0.464383, 0.247554)`
- `delta_stat ~ 0`

and it gives exact closure on the favored column:

- `eta / eta_obs = (1.0, 0.75917896, 0.48458840)`

So the old exact one-flavor miss

- `eta_obs / eta = 5.297004933778`

is gone on this PMNS-assisted route. The selector is now tied to the exact
observable grammar itself.

## What this closes

This closes the “is the minimization rule extra?” loophole on the current
branch.

The current branch now has:

- exact scalar observable generator from `Cl(3)` on `Z^3`
- exact seed-relative effective action on the charged block
- exact closure surface
- constrained effective-action selector on that surface

So the selector principle is no longer a free import. The exact law is:

> choose the lowest-action closure branch of the exact seed-relative effective
> action.

## What this does not claim

This note does **not** claim:

1. a branch-global analytic proof that no second disconnected closure component
   exists anywhere else on the full seed surface
2. a full PMNS microscopic solve beyond the current branch

The current theorem is:

- exact at the effective-action reduction level
- branch-exact at the closure equation level
- uniqueness of the lowest-action branch / local-minimum verified directly on
  the current closure patch

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem.py
```
