# DM Neutrino Source-Surface Shift-Quotient Bundle Theorem

**Date:** 2026-04-16  
**Status:** exact mainline blocker-reduction theorem on the live source-oriented sheet  
**Script:** `scripts/frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem.py`

## Question

On the live source-oriented `H`-side sheet, what exact inverse-image object
remains after quotienting by the common diagonal shift?

## Bottom line

The live source-oriented preimage bundle already has an exact shift-quotient
gauge over three `H`-side invariants

- `m     = d1 - (d2 + d3)/2`
- `delta = (d2 - d3)/2`
- `r31   >= 1/2`

with source-oriented branch

- `phi_+(r31) = asin(1 / (2 r31))`
- `d1 = m`
- `d2 = delta`
- `d3 = -delta`
- `r12 = 2 sqrt(8/3) - 2 delta + r31 cos(phi_+)`
- `r23 = m - delta + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi_+)`

Every point on the live source-oriented bundle is exactly shift-equivalent to
one point in that gauge, and every such quotient point has a positive
representative after adding a sufficiently large common diagonal shift.

So the remaining mainline object is an explicit `3`-real `H`-side quotient
bundle over `(m, delta, r31)`, equivalently the carrier-normal-form bundle on
the live source-oriented sheet.

## Exact content

### 1. Exact shift quotient

On the source-oriented `+` sheet, the exact preimage bundle is initially
parameterized by free data

- `(d1, d2, d3, r31)`

with `r31 >= 1/2`.

The common diagonal shift

- `(d1, d2, d3) -> (d1 + lambda, d2 + lambda, d3 + lambda)`

is an exact tangent direction of the bundle. The three shift-invariant `H`-side
coordinates are therefore

- `m = d1 - (d2 + d3)/2`
- `delta = (d2 - d3)/2`
- `r31`

and every bundle point is shift-equivalent to the quotient gauge

- `d1 = m`
- `d2 = delta`
- `d3 = -delta`.

### 2. Exact quotient-gauge formulas

On that quotient gauge the source-oriented branch is explicit:

- `phi_+(r31) = asin(1 / (2 r31))`
- `r12 = 2 sqrt(8/3) - 2 delta + r31 cos(phi_+)`
- `r23 = m - delta + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi_+)`

and the exact source-oriented channels become

- `gamma = 1/2`
- `delta = delta`
- `rho = sqrt(8/3) - delta`

so `delta + rho = sqrt(8/3)` is automatic.

### 3. Positivity is inherited after spectral shift

Each quotient-gauge Hermitian point is still only defined up to the same common
diagonal shift. If a chosen representative is not positive, adding

- `lambda I`

with sufficiently large `lambda` shifts every eigenvalue upward by `lambda`
without changing

- `gamma`
- `B1`
- `B2`
- the intrinsic CP pair.

So positivity is not an extra obstruction after passing to the quotient bundle:
every quotient point already represents a positive `H`-side class.

### 4. Carrier-side equivalent

The quotient bundle feeds the live carrier normal form exactly. On positive
representatives from the quotient gauge,

- `gamma = 1/2`
- `delta + rho = sqrt(8/3)`
- `sigma sin(2v) = 8/9`

and the quotient coordinate `delta` is exactly the carrier-side `delta`
coordinate.

So the explicit `H`-side quotient bundle and the carrier-side normal form are
equivalent descriptions of the same live mainline object.

## Consequence

The remaining mainline blocker is now sharper than a generic “find an `H`-law”
statement and sharper than a generic carrier-population statement.

It is the post-canonical mixed-bridge law that selects a point on the explicit
shift-quotient bundle

- `(m, delta, r31)`

on the live source-oriented sheet, equivalently on the associated carrier
normal-form bundle.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem.py
```
