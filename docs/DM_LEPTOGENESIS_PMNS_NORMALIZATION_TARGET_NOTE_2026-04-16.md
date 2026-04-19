# DM Leptogenesis PMNS Normalization Target

**Date:** 2026-04-16  
**Status:** exact coefficient-target theorem for the missing native
normalization law on the post-retained `N_e` lane  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_normalization_target.py`

## Question

If the only live scientific weakness on the positive post-retained `N_e` lane
is the missing observation-free normalization/value law, what exact coefficient
must that law hit, and what easy routes are already ruled out?

## Bottom line

The missing law must derive the exact coefficient

`a_* = 0.518479949928...`

in the observation-free free-energy family

`Phi_a(H_e) = log F_{i_*}(H_e) - a S_rel(H_e || H_seed)`.

On the current branch this target is already fixed exactly by the local closure
data:

- it is the reciprocal KKT multiplier of the observational closure problem
- equivalently, it is the projection coefficient in
  `grad log F_{i_*} = a_* grad S_rel`
  at the exact closure source

So the missing theorem is not “find some better packet” or “search harder.”
It is a coefficient law.

## What the branch already rules out

### 1. Transport-only normalization

`a = 0`

is not the target. The exact branch already shows transport extremality
overshoots the closure value.

### 2. Unit-scale free-energy normalization

`a = 1`

is not the target either. The exact unit-scale law underproduces and collapses
toward a low-action near-seed source.

### 3. Endpoint matching

The simple seed-to-closure secant coefficient

`a_endpoint = (log F_* - log F_seed) / (S_* - S_seed)`

is

`a_endpoint = 3.473706414287...`,

far from `a_*`.

So the missing normalization is not just “equalize seed and closure free
energies.”

### 4. Isotropic Hessian matching

On the exact closure tangent space, the Hessian of `log F_{i_*}` is **not** a
scalar multiple of the Hessian of `S_rel`.

So the missing law is not a naive uniform quadratic-curvature rescaling on the
reduced `N_e` cone either.

## Consequence

This makes the next scientific move exact.

The live theorem to derive is:

> a canonical first-order normalization law for the favored-column transport
> observable `log F_{i_*}` against the exact Legendre-dual effective action
> `S_rel` on the reduced `N_e` family.

That is the right target because:

- the carrier is already fixed
- the reduced domain is already fixed
- the selector structure is already fixed
- the remaining ambiguity is exactly the coefficient `a`

## Recommended line of attack

The best route is now:

1. identify the physically admissible transport observable family whose
   first-order response on the reduced `N_e` closure source is canonical
2. show that this canonical response coefficient equals
   `a_* = 0.518479949928...`
3. then lift the existing observational closure lane to an observation-free
   normalization law

So the next theorem is not a new global search. It is a canonical
normalization theorem.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_normalization_target.py
```
