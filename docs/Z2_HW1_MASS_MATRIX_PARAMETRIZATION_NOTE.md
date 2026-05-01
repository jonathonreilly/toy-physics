# Z_2 `hw=1` Mass-Matrix Parametrization Note

**Date:** 2026-04-17
**Status:** proposed_retained exact structural theorem on the residual
axis-selected carrier; audit pending
**Script:** `scripts/frontier_z2_hw1_mass_matrix_parametrization.py`
**Authority role:** canonical normal-form theorem for residual
`Z_2`-invariant Hermitian operators on the `hw=1` triplet; not a standalone
mass-hierarchy theorem

## Safe statement

Let `V_1 = span(X_1, X_2, X_3)` and let `Z_2 = <(12)>` fix axis `3` while
swapping axes `1` and `2`. In the ordered basis `(X_3, X_1, X_2)`, every
`Z_2`-invariant Hermitian operator on `V_1` has the form

```text
M(a, b, c, d) = [[a,  d,  d ],
                 [d*, b,  c ],
                 [d*, c,  b ]]
```

with `a, b, c in R` and `d in C`. This is a `5`-real-parameter family.

The vector `(X_1 - X_2) / sqrt(2)` is an exact sign eigenvector with eigenvalue
`b - c`. On the two-dimensional trivial block spanned by
`X_3` and `(X_1 + X_2)/sqrt(2)`, the operator reduces to the Hermitian block

```text
[[a,        sqrt(2) d],
 [sqrt(2)d*, b + c   ]]
```

with eigenvalues

```text
lambda_pm = ((a + b + c) +- sqrt((a - b - c)^2 + 8 |d|^2)) / 2.
```

Generic points in this `5`-real-parameter family give three distinct
eigenvalues, while the exact `S_3`-invariant locus is the subspace
`d = 0`, `a = b + c`.

## Classical results applied

- Schur's lemma on the `Z_2` decomposition `V_1 ~= 2 * trivial + sign`
- the Hermitian spectral theorem
- the quadratic formula for the `2 x 2` Hermitian secular equation

## Framework-specific step

- identification of the residual subgroup with the axis-selected `Z_2` left
  after the current `S_3 -> Z_2` support picture
- use of the retained `hw=1` triplet as the carrier

## Why it matters on `main`

This is the exact post-`S_3` support tool complementary to the
`S_3` mass-matrix no-go. It does not claim a derived flavor hierarchy or
select a point in the five-real-parameter family. Its safe retained-grade role
is narrower: it exposes the full residual `Z_2` Hermitian normal form
available on the retained carrier once one leaves the exact unbroken `S_3`
class.

## Verification

Run:

```bash
python3 scripts/frontier_z2_hw1_mass_matrix_parametrization.py
```

The runner checks invariance, the `5`-dimensional real parameter count, the
sign eigenvector, the explicit `2 x 2` block, the closed-form spectrum, and
the collapse to the two-value spectrum on the exact `S_3` locus.
