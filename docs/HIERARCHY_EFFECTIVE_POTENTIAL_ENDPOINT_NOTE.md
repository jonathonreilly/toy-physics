# Hierarchy Effective-Potential Endpoint Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-13  
**Script:** `scripts/frontier_hierarchy_effective_potential_endpoint.py`

## Question

Given the exact Matsubara decomposition on the minimal `L_s = 2` APBC block,
can the remaining Part 3 normalization problem be stated exactly on the
**dimension-4 effective-potential density** side rather than as a vague
"prefactor"?

## Exact result

Yes.

Starting from the exact free-energy density formula:

`Delta f(L_t, m) = (1 / (2 L_t)) sum_omega ln(1 + m^2 / [u_0^2 (3 + sin^2 omega)])`

the small-m expansion is:

`Delta f(L_t, m) = A(L_t) m^2 + O(m^4)`

with exact coefficient:

`A(L_t) = (1 / (2 L_t u_0^2)) sum_omega 1 / (3 + sin^2 omega)`

This coefficient is the cleanest intensive candidate for the temporal
normalization surface, because it is directly extracted from the exact
dimension-4 effective-potential density.

## Exact endpoint formulas

The APBC endpoints are now explicit:

- `A_2 = 1 / (8 u_0^2)`
- `A_4 = 1 / (7 u_0^2)`
- `A_inf = 1 / (4 sqrt(3) u_0^2)`

So the exact full temporal-averaging correction between the minimal UV block
and the `L_t -> infinity` temporal average is:

`A_inf / A_2 = 2 / sqrt(3) ~= 1.154700538`

This is the exact analytic version of the earlier numerical `1.15469...`
ratio.

## Why this matters

If the physical normalization sits on a **dimension-4** effective-potential
density, the corresponding scale correction is the fourth root:

`C_inf^(4D) = (A_2 / A_inf)^(1/4) = (sqrt(3) / 2)^(1/4) = (3/4)^(1/8)`

Numerically:

- `C_inf^(4D) ~= 0.964678630`
- observed hierarchy prefactor
  `C_obs = 246.22 / 254.643210673818 ~= 0.966921519`

So the observed prefactor lies **inside the exact 3+1 endpoint band**
between:

- no temporal normalization correction: `1`
- full `L_t -> infinity` dimension-4 correction: `0.964678630`

That is much sharper than the old "maybe a prefactor" language.

## What is now closed

1. the small-m effective-potential coefficient is exact
2. the `L_t = 2` endpoint coefficient is exact
3. the `L_t -> infinity` coefficient is exact
4. the full temporal normalization ratio is exact

## What is still open

This still does **not** close the full hierarchy theorem.

The remaining Part 3 question is now:

> where, between the exact `L_t = 2` UV endpoint and the exact temporal
> average, does the physical EWSB normalization live?

Equivalently:

1. why the physical order parameter should pick the `L_t = 2` endpoint,
   or a derived function of this exact endpoint pair
2. how that exact intensive normalization enters the `det -> v` map
3. whether the remaining `~0.22%` difference is then just the plaquette / `u_0`
   input uncertainty

## Honest conclusion

The hierarchy route is still **not fully closed**.

But the open surface is now very tight:

- the exponent `16` is structural
- the temporal algebra is exact
- the relevant intensive endpoint normalization is exact

So the only real remaining theorem is the physical selection / insertion of
that exact dimension-4 temporal normalization into the electroweak scale map.
