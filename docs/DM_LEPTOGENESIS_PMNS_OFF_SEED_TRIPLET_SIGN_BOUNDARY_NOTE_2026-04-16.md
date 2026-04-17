# DM Leptogenesis PMNS Off-Seed Triplet Sign Boundary

**Date:** 2026-04-16  
**Status:** exact off-seed PMNS sign-boundary theorem for the charged-sector
comparator lane  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_off_seed_triplet_sign_boundary.py`

## Question

Once the PMNS side has already been reduced to the off-seed `5`-real source

`(xi_1, xi_2, eta_1, eta_2, delta)`,

what exact constructive sign boundary remains for a source-oriented mainline CP
witness?

## Bottom line

The open PMNS constructive gate is now an explicit `5`-real inequality system,
not a vague full-`D` search.

On the fixed native `N_e` seed surface with

`X = XBAR_NE`

`Y = YBAR_NE`

the off-seed source reconstructs the active family by

`x = (X + xi_1, X + xi_2, X - xi_1 - xi_2)`

`y = (Y + eta_1, Y + eta_2, Y - eta_1 - eta_2)`.

The mainline triplet channels are therefore exact functions of the same
`5` reals:

`gamma = (X + xi_1) (Y - eta_1 - eta_2) sin(delta)`

`E1 = [ (X + xi_2)^2 + (Y + eta_2)^2 - (X - xi_1 - xi_2)^2 - (Y - eta_1 - eta_2)^2`

`      + (X + xi_2)(Y + eta_1) - (X + xi_1)(Y - eta_1 - eta_2) cos(delta) ] / 2`

`E2 = (X + xi_1)^2 + (Y + eta_1)^2`

`      + [ (X + xi_2)(Y + eta_1) + (X + xi_1)(Y - eta_1 - eta_2) cos(delta) ] / 2`

`      - [ (X + xi_2)^2 + (Y + eta_2)^2 + (X - xi_1 - xi_2)^2 + (Y - eta_1 - eta_2)^2 ] / 2`

`      - (X - xi_1 - xi_2)(Y + eta_2)`.

## Exact constructive consequence

On the positive interior of the fixed seed surface we already have

`X + xi_1 > 0`

`Y - eta_1 - eta_2 > 0`.

So the prefactor in `gamma` is positive, and therefore

`gamma > 0  <=>  sin(delta) > 0`.

That is the exact phase-orientation boundary.

So a constructive PMNS witness must satisfy the explicit `5`-real sign system

- `sin(delta) > 0`
- `E1 > 0`
- `E2 > 0`

on the same off-seed source.

## What this closes

This closes the next ambiguity after the PMNS last-mile reduction.

Before this theorem, the PMNS-side open object was known to be only the
off-seed `5`-real source, but the constructive target on that object was still
described too vaguely.

Now it is explicit:

- the open PMNS comparator is not “some full-`D` improvement”
- it is not “some better selector packaging”
- it is the exact `5`-real inequality system above

## Canonical sample read

On the canonical near-closing `N_e` sample:

- `gamma > 0`
- but `E1 < 0`
- and `E2 < 0`

So the canonical PMNS comparator already has the right phase orientation but
still misses the constructive mainline sheet on the two real interference
channels.

## Consequence for the live target

If a positive PMNS-side bridge is still wanted, the next exact comparator task
is:

- derive a full-`D` / off-seed source law that lands on
  `sin(delta) > 0`, `E1 > 0`, `E2 > 0`

or else

- prove a stronger exact no-go showing that this `5`-real sign system cannot
  be realized on the current PMNS branch.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_off_seed_triplet_sign_boundary.py
```
