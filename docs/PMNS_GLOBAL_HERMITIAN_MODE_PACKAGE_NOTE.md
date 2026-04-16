# PMNS Global Hermitian Mode Package

**Date:** 2026-04-15  
**Status:** exact structural decomposition theorem for the global active
Hermitian law on the canonical PMNS branch  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_global_hermitian_mode_package.py`

## Question

The current bank still does not derive the active branch Hermitian data as
axiom-side outputs.

But can the global Hermitian target at least be decomposed exactly into
axiom-native sectors, rather than treated as a generic seven-real object?

## Bottom line

Yes.

On the canonical active branch

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i phi}) C`,

the Hermitian law

`H = Y Y^dag`

admits an exact `2 + 2 + 3` package, but the correct global package is **not**
the raw linear `P_23`-even projection.

It is:

- a four-real **aligned real core**
  `H_core = [[a,b,b],[b,c,d],[b,d,c]]`
- plus a three-real **breaking triplet**
  `(delta,rho,gamma)`

with

- `a = H_11`
- `b = (r_12 + r_31 cos phi)/2`
- `c = (H_22 + H_33)/2`
- `d = r_23`
- `delta = (H_22 - H_33)/2`
- `rho = (r_12 - r_31 cos phi)/2`
- `gamma = r_31 sin phi`

and

`H = H_core + B(delta,rho,gamma)`

where

`B(delta,rho,gamma) = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`.

The aligned real core is then exactly equivalent to:

- weak-axis seed pair `(A,B)`
- aligned deformation pair `(u,v)`

So the global active Hermitian law is exactly:

- `2` weak-axis seed coordinates
- `2` aligned real-core deformations
- `3` breaking coordinates

and therefore exactly a `2 + 2 + 3` package.

## Atlas and axiom inputs

This theorem reuses:

- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB weak-axis Z3 seed`
- `PMNS EWSB residual-Z2 spectral primitive reduction`
- `PMNS EWSB breaking-slot nonrealization`

The point is not to derive the values of the global Hermitian data. The point
is to package them exactly into axiom-native sectors.

## Exact global decomposition

Write the canonical Hermitian data as

- `d_1 = H_11`
- `d_2 = H_22`
- `d_3 = H_33`
- `H_12 = r_12`
- `H_23 = r_23`
- `H_13 = r_31 e^{-i phi}`

with `r_12, r_23, r_31 >= 0`.

Then define the real aligned core

`H_core = [[a,b,b],[b,c,d],[b,d,c]]`

by

- `a = d_1`
- `b = (r_12 + r_31 cos phi)/2`
- `c = (d_2 + d_3)/2`
- `d = r_23`

and the breaking triplet by

- `delta = (d_2-d_3)/2`
- `rho   = (r_12-r_31 cos phi)/2`
- `gamma = r_31 sin phi`.

Then one checks directly that

`H = H_core + B(delta,rho,gamma)`.

So the global law is already split exactly into:

- a residual-`Z_2` real core
- plus a three-real global breaking package

without any leftover overlap.

## Exact coefficient-side moment law

On the canonical active chart,

- `d_1 = x_1^2 + y_1^2`
- `d_2 = x_2^2 + y_2^2`
- `d_3 = x_3^2 + y_3^2`
- `r_12 = x_2 y_1`
- `r_23 = x_3 y_2`
- `r_31 = x_1 y_3`.

Therefore the global package is also exactly:

- `a = x_1^2 + y_1^2`
- `b = (x_2 y_1 + x_1 y_3 cos phi)/2`
- `c = (x_2^2 + y_2^2 + x_3^2 + y_3^2)/2`
- `d = x_3 y_2`
- `delta = ((x_2^2 + y_2^2) - (x_3^2 + y_3^2))/2`
- `rho = (x_2 y_1 - x_1 y_3 cos phi)/2`
- `gamma = x_1 y_3 sin phi`

So the old breaking-slot vector is not the sharpest package anymore.
The exact global breaking sector is the triplet `(delta,rho,gamma)`.

## Exact inverse formulas

The package is exact in both directions.

From `(a,b,c,d,delta,rho,gamma)` one recovers the canonical Hermitian data:

- `d_1 = a`
- `d_2 = c + delta`
- `d_3 = c - delta`
- `r_12 = b + rho`
- `r_23 = d`
- `r_31 = sqrt((b-rho)^2 + gamma^2)`
- `phi = atan2(gamma, b-rho)`

away from the usual nongeneric `r_31 = 0` phase-degenerate locus.

So the package is not just a convenient coordinate choice. It is an exact
equivalent description of the global active Hermitian law.

## Relation to the aligned surface

The aligned residual-`Z_2` surface is exactly the vanishing of the breaking
triplet:

- `delta = 0`
- `rho = 0`
- `gamma = 0`.

On that surface, `H = H_core`, and the aligned core is already known to be
equivalent to the `2 + 1` spectral primitive package

`(lambda_+, lambda_-, lambda_odd, theta_even)`.

Relative to the weak-axis seed subcone, this becomes exactly:

- weak-axis seed pair `(A,B)`
- aligned deformation pair `(u,v)`

So the global package is correctly read as:

- real aligned core `(2 + 2)`
- plus breaking triplet `(3)`

not as a generic seven-real target.

## Theorem-level statement

**Theorem (Exact global `2 + 2 + 3` package for the PMNS active Hermitian
law).** Assume the canonical active PMNS branch. Then:

1. every active Hermitian matrix has the exact canonical form
   `H = H_core + B(delta,rho,gamma)` with `H_core` on the real aligned
   residual-`Z_2` core
2. the breaking part is exactly three-real-dimensional
3. the real aligned core is exactly equivalent to the spectral package
   `(lambda_+, lambda_-, lambda_odd, theta_even)`
4. relative to the weak-axis seed subcone, that aligned core is exactly a
   `2 + 2` package:
   weak-axis seed pair `(A,B)` plus aligned deformations `(u,v)`

So the global active Hermitian law is exactly a `2 + 2 + 3` package:

- weak-axis seed pair
- aligned deformation pair
- breaking triplet `(delta,rho,gamma)`.

## What this closes

This closes the structural question of how the global Hermitian law should be
organized.

It is now exact that the remaining global Hermitian object is not:

- an undifferentiated seven-real target
- a generic flavor matrix
- a raw `P_23`-even projection plus unrelated leftovers

It is one exact real aligned core plus one exact three-real breaking sector.

## What this does not close

This note does **not** derive:

- the values of `(A,B)`
- the aligned deformation law `(u,v)`
- the breaking-sector law `(delta,rho,gamma)`
- the monomial-edge / Higgs-offset selector on the seed patch

So it sharpens the global closure problem, but does not by itself complete it.

## Command

```bash
python3 scripts/frontier_pmns_global_hermitian_mode_package.py
```
