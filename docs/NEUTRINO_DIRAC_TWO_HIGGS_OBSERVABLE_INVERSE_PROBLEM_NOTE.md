# Neutrino Dirac Two-Higgs Observable Inverse-Problem Theorem

**Date:** 2026-04-15  
**Status:** exact local-generic inverse-problem theorem on the canonical
minimal two-Higgs neutrino lane  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_dirac_two_higgs_observable_inverse_problem.py`

## Question

After the exact canonical reduction of the minimal surviving neutrino-side
class to

`Y_nu = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`,

is there still some hidden continuous redundancy between these seven canonical
quantities and the local Dirac-neutrino observables?

Or is the seven-parameter count already the real end of the freedom on this
minimal lane?

## Bottom line

There is no hidden continuous redundancy, generically.

On the canonical two-Higgs lane, the Hermitian matrix

`H_nu = Y_nu Y_nu^dag`

has the exact form

```text
[ x_1^2 + y_1^2       x_2 y_1             x_1 y_3 e^{-i delta} ]
[ x_2 y_1             x_2^2 + y_2^2       x_3 y_2              ]
[ x_1 y_3 e^{i delta} x_3 y_2             x_3^2 + y_3^2        ]
```

So the canonical lane carries a natural exact seven-coordinate observable
grammar:

- `d_1, d_2, d_3` = diagonal entries of `H_nu`
- `r_12, r_23, r_31` = off-diagonal moduli
- `phi = arg(H_12 H_23 H_31)`

These seven coordinates are exact local rephasing invariants on the monomial
charged-lepton boundary, and:

1. the map from `(x_1,x_2,x_3,y_1,y_2,y_3,delta)` to
   `(d_1,d_2,d_3,r_12,r_23,r_31,phi)` has full Jacobian rank on a generic open
   dense subset
2. those seven coordinates reconstruct `H_nu` exactly

So on the minimal surviving lane, deriving the seven canonical quantities is
already generically equivalent to **local full Dirac-neutrino closure**.

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Dirac two-Higgs canonical reduction`
- `Lepton single-Higgs PMNS triviality theorem`

and keeps the same bridge condition explicit:

- the charged-lepton sector stays on the monomial single-Higgs boundary
- the neutrino sector lives on the canonical minimal two-Higgs lane

## Exact seven-coordinate grammar of the canonical lane

On the canonical support class, `C` is the forward `3`-cycle, so

`Y_nu = D_x + D_y C`

with

- `D_x = diag(x_1,x_2,x_3)`
- `D_y = diag(y_1,y_2,y_3 e^{i delta})`

Therefore the Hermitian neutrino data are exactly:

- `H_11 = x_1^2 + y_1^2`
- `H_22 = x_2^2 + y_2^2`
- `H_33 = x_3^2 + y_3^2`
- `|H_12| = x_2 y_1`
- `|H_23| = x_3 y_2`
- `|H_31| = x_1 y_3`
- `arg(H_12 H_23 H_31) = delta`

So the lane already comes with a natural exact seven-coordinate observable map.

## Local-generic invertibility

Consider the map

`F : (x_1,x_2,x_3,y_1,y_2,y_3,delta) -> (d_1,d_2,d_3,r_12,r_23,r_31,phi)`.

The Jacobian is explicit and analytic on the generic positive-modulus patch.
The runner evaluates that Jacobian directly and finds full rank `7` at generic
sample points.

Because the Jacobian determinant is an analytic function and is not identically
zero, the full-rank set is open and dense on the generic patch.

So the canonical lane has no further hidden continuous redundancy beyond the
already-removed diagonal rephasings.

## Exact reconstruction of `H_nu`

From the seven local coordinates,

`H_nu` is reconstructed exactly as

```text
[ d_1              r_12               r_31 e^{-i phi} ]
[ r_12             d_2                r_23            ]
[ r_31 e^{i phi}   r_23               d_3             ]
```

So the seven coordinates do not merely count the data. They determine the full
local Hermitian neutrino matrix on this lane.

And on the monomial charged-lepton boundary, that is the full local
Dirac-neutrino data source.

## The theorem-level statement

**Theorem (Local inverse-problem closure on the canonical two-Higgs neutrino
lane).**
Assume the canonical minimal two-Higgs neutrino support class and the monomial
charged-lepton boundary. Then:

1. the canonical neutrino Hermitian matrix `H_nu = Y_nu Y_nu^dag` is exactly
   encoded by seven local rephasing-invariant coordinates
   `(d_1,d_2,d_3,r_12,r_23,r_31,phi)`
2. the map from the seven canonical lane quantities
   `(x_1,x_2,x_3,y_1,y_2,y_3,delta)` to those seven coordinates has full
   Jacobian rank on a generic open dense subset
3. those seven coordinates reconstruct `H_nu` exactly

Therefore the canonical minimal two-Higgs lane has no hidden continuous
redundancy, and local full Dirac-neutrino closure on that lane is generically
equivalent to deriving those seven canonical quantities.

## What this closes

This closes the next exact ambiguity after the seven-parameter count.

It is now exact that:

- the seven-parameter count is not hiding another continuous quotient
- the minimal surviving lane is locally well-posed as an inverse problem
- deriving the seven canonical quantities is a real closure target, not just a
  counting slogan

## What this does not close

This note does **not** derive:

- the seven quantities
- the global discrete branch structure
- the observed neutrino masses
- the observed PMNS angles or Dirac phase numerically

It is a local-generic inverse-problem theorem only.

## Safe wording

**Can claim**

- the canonical two-Higgs lane has an exact seven-coordinate observable grammar
- the local inverse problem is generically well-posed
- no hidden continuous redundancy remains on that lane
- full local Dirac-neutrino closure on that lane reduces to deriving the seven
  canonical quantities

**Cannot claim**

- the seven quantities are already derived
- the global inverse problem is uniquely solved on every discrete branch
- PMNS is numerically closed

## Command

```bash
python3 scripts/frontier_neutrino_dirac_two_higgs_observable_inverse_problem.py
```
