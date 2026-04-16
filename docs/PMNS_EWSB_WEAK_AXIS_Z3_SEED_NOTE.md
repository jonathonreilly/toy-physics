# PMNS EWSB Weak-Axis `Z_3` Seed Theorem

**Date:** 2026-04-15  
**Status:** exact bridge-conditioned theorem on the weak-axis-inherited
Hermitian seed and its canonical active-lane realization boundary  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_ewsb_weak_axis_z3_seed.py`

## Question

The current bank does not yet derive the full active Hermitian law on the
PMNS-producing branch.

But does the exact weak-axis `1+2` generation split already give any concrete
axiom-native Hermitian seed on the canonical active two-Higgs lane?

## Bottom line

Yes, but with a precise compatibility boundary.

Let the exact weak-axis generation seed be the site-basis `1+2` Hermitian
split

`D_12(A,B) = diag(A,B,B)`,

with `A >= B >= 0`.

Then the canonical `Z_3` bridge sends it to the even-circulant Hermitian
matrix

`H_seed = U_Z3^dag D_12(A,B) U_Z3 = mu I + nu (C + C^2)`,

with

- `mu = (A + 2 B) / 3`
- `nu = (A - B) / 3`

So the current bank already derives a concrete two-parameter active Hermitian
seed in `H`-space.

On the canonical active two-Higgs chart

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`,

that Hermitian seed is realized exactly if and only if

`A <= 4 B`.

When that compatibility condition holds, the realization is forced onto the
unique symmetric slice

`Y_seed = x I + y C`,

with

- `x = (sqrt(A) + sqrt((4 B - A) / 3)) / 2`
- `y = (sqrt(A) - sqrt((4 B - A) / 3)) / 2`

and hence

`Y_seed Y_seed^dag = H_seed`.

So the current bank already derives a concrete weak-axis Hermitian seed, and
it also derives the exact boundary of when that seed lies on the canonical
active Yukawa lane.

## Atlas and axiom inputs

This theorem reuses:

- `Graph-first weak-axis selector derivation`
- `Generation axiom boundary`
- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB residual-Z2 spectral primitive reduction`
- `Neutrino Dirac two-Higgs canonical reduction`

The bridge used here is exact and explicit:

- the weak-axis theorem supplies the exact `1+2` diagonal seed `diag(A,B,B)`
- the canonical `Z_3` bridge diagonalizes the circulant generation operators
- the canonical active two-Higgs chart supplies the exact Yukawa-side test for
  whether that Hermitian seed is actually realized on the PMNS active lane

## Exact `Z_3` lift of the weak-axis split

Let

- `C` be the cyclic shift on the generation basis
- `U_Z3` be the canonical discrete Fourier / `Z_3` bridge

Then

`U_Z3^dag diag(A,B,B) U_Z3`

is exactly

`mu I + nu (C + C^2)`,

with

`mu = (A + 2 B) / 3`,
`nu = (A - B) / 3`.

This is the exact even-circulant Hermitian slice singled out by the weak-axis
`1+2` seed.

## Exact realization equations on the canonical active chart

On the canonical active PMNS lane

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`,

the Hermitian matrix is exactly

```text
[ x_1^2 + y_1^2        x_2 y_1          x_1 y_3 e^{-i delta} ]
[ x_2 y_1              x_2^2 + y_2^2    x_3 y_2              ]
[ x_1 y_3 e^{i delta}  x_3 y_2          x_3^2 + y_3^2        ]
```

Matching to the weak-axis seed

`H_seed = [[mu,nu,nu],[nu,mu,nu],[nu,nu,mu]]`

forces

- `delta = 0`
- `x_2 y_1 = nu`
- `x_3 y_2 = nu`
- `x_1 y_3 = nu`
- `x_1^2 + y_1^2 = x_2^2 + y_2^2 = x_3^2 + y_3^2 = mu`

Setting `a_i = x_i^2`, these equations become the polynomial system

- `a_1 a_2 + nu^2 - mu a_2 = 0`
- `a_2 a_3 + nu^2 - mu a_3 = 0`
- `a_3 a_1 + nu^2 - mu a_1 = 0`

whose Groebner basis is exactly

- `a_1 - a_3`
- `a_2 - a_3`
- `a_3^2 - mu a_3 + nu^2`

So any exact canonical active-lane realization is forced onto the symmetric
slice

- `x_1 = x_2 = x_3 = x`
- `y_1 = y_2 = y_3 = y`
- `delta = 0`

with

- `x^2 + y^2 = mu`
- `x y = nu`

There is no non-symmetric positive realization on the canonical active chart.

## Compatibility boundary and explicit symmetric realization

The symmetric realization equations reduce to

`t^2 - mu t + nu^2 = 0`,

with `t = x^2`.

So exact canonical active-lane realization exists if and only if

`Delta = mu^2 - 4 nu^2 >= 0`.

In terms of the weak-axis parameters,

`Delta = A (4 B - A) / 3`.

Since `A >= B >= 0`, this is equivalent to

`A <= 4 B`.

When that condition holds, the positive canonical realization is unique up to
the exchange `x <-> y`. On the standard gauge patch `x >= y >= 0`, it is

- `x = (sqrt(A) + sqrt((4 B - A) / 3)) / 2`
- `y = (sqrt(A) - sqrt((4 B - A) / 3)) / 2`

and therefore

`Y_seed = x I + y C`,
`Y_seed Y_seed^dag = H_seed`.

So the weak-axis seed always exists in Hermitian space, but it lies on the
canonical active Yukawa chart only on the exact compatibility patch
`A <= 4 B`.

## Relation to the aligned residual-`Z_2` core

The even-circulant seed

`H_seed = mu I + nu (C + C^2)`

is

```text
[ mu  nu  nu ]
[ nu  mu  nu ]
[ nu  nu  mu ]
```

in the generation basis.

So it lies inside the aligned residual-`Z_2` Hermitian core

`[[a,b,b],[b,c,d],[b,d,c]]`

with the extra exact relations

- `a = c = mu`
- `b = d = nu`

Therefore the weak-axis inherited seed is a strict two-parameter subcone of
the four-parameter aligned core.

## Relation to the aligned spectral primitives

On the aligned spectral package

`(lambda_+, lambda_-, lambda_odd, theta_even)`,

the weak-axis seed obeys the exact conditions

- `lambda_+ = A`
- `lambda_- = lambda_odd = B`
- `theta_even = arctan(sqrt(2))`

on the generic patch `A > B`.

So the aligned four-parameter / spectral target now has an exact axiom-native
two-parameter seed:

- two primitive values are already fixed by the weak-axis split
- two aligned deformation directions remain open:
  `lambda_- - lambda_odd` and `theta_even - arctan(sqrt(2))`

This is the aligned analogue of the generic `4 + 3` split already isolated by
the bank.

## Theorem-level statement

**Theorem (Exact weak-axis `1+2` lift to the PMNS active Hermitian seed).**
Assume the exact weak-axis `1+2` generation split, the canonical `Z_3` bridge,
and the canonical active two-Higgs PMNS chart. Then:

1. the weak-axis seed `diag(A,B,B)` lifts exactly to the even-circulant
   Hermitian matrix `mu I + nu(C + C^2)`
2. on the canonical active chart, exact realization of that seed is possible
   if and only if `A <= 4 B`
3. when realization exists, it is forced onto the unique symmetric slice
   `Y_seed = x I + y C` on the standard gauge patch `x >= y >= 0`
4. the lifted seed lies inside the aligned residual-`Z_2` Hermitian core
5. on the aligned spectral primitive package it satisfies
   `lambda_- = lambda_odd` and
   `theta_even = arctan(sqrt(2))`

So the current bank already derives a concrete two-parameter active Hermitian
seed from the weak-axis `1+2` split, together with the exact boundary of when
that seed is realized on the canonical active Yukawa lane.

## What this closes

This closes the question of whether the current bank gives any positive
Hermitian seed beyond the conditional aligned-core packaging.

It is now exact that:

- the weak-axis `1+2` split already lands on the PMNS active Hermitian lane
- it lands there on a strict two-parameter seed subcone
- its canonical active-lane realization boundary is exactly `A <= 4 B`
- when that realization exists, it is unique on the positive canonical gauge
- the remaining aligned gap is not four unconstrained numbers anymore on this
  seed, but two aligned deformation directions

## What this does not close

This note does **not** derive:

- that the full PMNS-producing extension stays on this weak-axis inherited seed
- the two aligned deformation directions away from the seed
- the three generic breaking slots away from the aligned surface
- the residual selected-branch coefficient sheet

So this note gives a concrete Hermitian seed and its exact compatibility
boundary, not full positive neutrino closure.

## Command

```bash
python3 scripts/frontier_pmns_ewsb_weak_axis_z3_seed.py
```
