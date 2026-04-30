# DM Leptogenesis PMNS Breaking-Triplet Source Law

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
family to the mainline breaking-triplet CP channels  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_breaking_triplet_source_law.py`

## Question

On the canonical one-sided PMNS active family, what exact charged-sector
algebraic law feeds the mainline breaking-triplet CP channels?

## Bottom line

The bridge is explicit.

For the active charged-sector family

`D_act = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`

the mainline breaking-triplet channels are exactly

- `gamma = x_1 y_3 sin(delta)`
- `E1 = [(x_2^2 + y_2^2) - (x_3^2 + y_3^2) + x_2 y_1 - x_1 y_3 cos(delta)] / 2`
- `E2 = x_1^2 + y_1^2 + (x_2 y_1 + x_1 y_3 cos(delta))/2 - [(x_2^2 + y_2^2) + (x_3^2 + y_3^2)]/2 - x_3 y_2`

where `E1 = delta + rho` and `E2 = A + b - c - d` on the mainline
breaking-triplet grammar.

So the charged-sector bridge is no longer “some full-`D` value law somehow.”
It is a concrete algebraic source law for `gamma`, `E1`, and `E2`.

## Exact consequence for the canonical near-closing `N_e` sample

On the canonical off-seed PMNS `N_e` sample

- `x = (0.24, 0.38, 1.07)`
- `y = (0.09, 0.22, 0.61)`
- `delta = 1.10`

the exact charged-sector triplet channels are

- `gamma = 0.13047275751299414`
- `E1 = -0.6782032360883523`
- `E2 = -0.9742967639116479`

So the sample has

- `gamma > 0`
- `E1 < 0`
- `E2 < 0`

and therefore lies on the opposite CP sheet from the source-oriented mainline
branch, which requires

- `gamma > 0`
- `E1 > 0`
- `E2 > 0`.

## Exact consequence for the PMNS last mile

The seed pair plus the off-seed `5`-real source already fix the same channels
algorithmically:

`(xbar, ybar, xi_1, xi_2, eta_1, eta_2, delta)`
`-> (x, y, delta)`
`-> (gamma, E1, E2)`
`-> (cp1, cp2)`.

So the remaining charged-sector bridge is now a sign/slot law on the off-seed
source, not a vague search over all of `D`.

## Meaning for the live target

The constructive charged-sector target is now sharp:

- derive a microscopic full-`D` / off-seed source law that forces
  `gamma > 0`, `E1 > 0`, and `E2 > 0`

or, failing that,

- prove a stronger incompatibility theorem for that sign pattern on the current
  PMNS family.

## Scope

This note does **not** yet derive the off-seed `5`-real values themselves from
`Cl(3)` on `Z^3`.

It proves only that once those values are supplied, the charged-sector bridge
to the mainline CP channels is an explicit algebraic law.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_breaking_triplet_source_law.py
```
