# DM Neutrino Exact H-Side Source-Surface Theorem

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_exact_h_source_surface_theorem.py`

## Question

Once the exact source-oriented package is fixed and the intrinsic positive-polar
CP tensor is exact on `H`, what mainline object actually remains?

## Bottom line

The triplet values themselves are no longer the open object on the sharp
source-oriented branch.

They already pull back to an exact `H`-side source surface:

- `r31 sin(phi) = 1/2`
- `d2 - d3 + r12 - r31 cos(phi) = 2 sqrt(8/3)`
- `2 d1 - d2 - d3 + r12 - 2 r23 + r31 cos(phi) = 2 sqrt(8)/3`

Equivalently:

- `gamma = 1/2`
- `B1 = 2 sqrt(8/3)`
- `B2 = 2 sqrt(8)/3`

So the remaining mainline object is the post-canonical mixed-bridge / `H`-side
law whose image lands on that exact source surface, not the triplet values
themselves.

## Why this is sharper

The exact source-amplitude theorem had already fixed

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`

and the positive-polar `H`-side CP theorem had already fixed the exact
Hermitian meaning of those quantities.

This theorem fuses those two endpoints.

## Exact constructive witness

The exact source surface is nonempty. One explicit positive Hermitian witness
is:

- `(d1,d2,d3) = (5, 5, 5)`
- `phi = pi/6`
- `r31 = 1`
- `r12 = 2 sqrt(8/3) + cos(pi/6)`
- `r23 = (r12 + cos(pi/6) - 2 sqrt(8)/3)/2`

For that witness:

- the smallest eigenvalue is positive
- `gamma = 1/2`
- `B1 = 2 sqrt(8/3)`
- `B2 = 2 sqrt(8)/3`
- the direct intrinsic CP pair equals the exact package pair

`(-0.544331053952, +0.314269680527)`.

## Exact consequence

So the remaining mainline object is narrower than “derive the triplet values.”

Those values are already fixed on the sharp source-oriented branch.

What still remains is:

- derive the post-canonical mixed-bridge / `H`-side law whose image lands on
  this exact source surface

That is the honest mainline baryogenesis blocker now.

## Command

```bash
python3 scripts/frontier_dm_neutrino_exact_h_source_surface_theorem.py
```
