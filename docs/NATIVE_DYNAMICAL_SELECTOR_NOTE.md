# Native Dynamical Selector Note

**Status:** PARTIAL CLOSURE - low-degree native `Cl(3)` triplets are too isotropic; a larger projector-valued axis simplex does support a genuine `S_3`-symmetric selector potential  
**Script:** `scripts/frontier_native_dynamical_selector.py`  
**Date:** 2026-04-12

## Claim under test

Can the missing weak-axis selector be obtained without importing the Kawamoto-
Smit factorization, by starting from the native graph / `Cl(3)` data and
building a genuine dynamical potential on a larger native operator surface?

The answer is two-part:

1. **No** on the low-degree native Clifford triplets themselves.
2. **Yes** on the minimal larger projector-valued axis simplex.

## Part 1: what the native low-degree Clifford surface does

The retained low-degree native surface contains the obvious axis-labelled
triplets:

- the vector triplet `Gamma_i`
- the bivector triplet `A_i = -i Gamma_j Gamma_k`

For either triplet, any source of the form

`H(phi) = sum_i phi_i Phi_i`

satisfies the exact Clifford identity

`H(phi)^2 = |phi|^2 I`.

So all trace/spectral invariants built from these lowest-degree native triplets
are isotropic:

- `Tr H^3 = 0`
- `Tr H^4 = 8 |phi|^4`

That means the low-degree native `Cl(3)` surface cannot distinguish axis,
planar, or fully symmetric directions. It gives triplets, but not a selector.

## Part 2: the minimal larger native surface that does work

The first genuinely selector-capable surface is the axis-occupancy simplex:

`p = (p1, p2, p3),  p_i >= 0,  sum_i p_i = 1`

equivalently the diagonal projector-valued order parameter

`P = diag(p1, p2, p3)`.

On this surface, the minimal `S_3`-symmetric Landau functional is the
purity-deficit / pairwise-overlap potential

`F(p) = sum_{i<j} p_i p_j = 1/2 * (1 - sum_i p_i^2)`

or, equivalently,

`F(P) = 1/2 * (Tr P - Tr P^2)`.

This potential has exactly three axis-selecting minima:

- `(1,0,0)`
- `(0,1,0)`
- `(0,0,1)`

Each minimum has residual `Z_2` stabilizer given by swapping the other two
axes.

## Verdict

The current native low-degree Clifford algebra does **not** provide a same-
surface `S_3 -> Z_2` selector.

But the larger projector-valued axis simplex does support a genuine dynamical
selector potential, and the simplest such potential is unique up to affine
rescaling:

`F = 1/2 * (1 - sum_i p_i^2)`.

That is the right next theorem if the full paper is to keep the expansive
claim alive without importing KS factorization or fitted taste-breaking
coefficients.

## Safe reading

- Low-degree native `Cl(3)` triplets: no selector.
- Larger projector-valued axis simplex: yes, minimal `S_3`-symmetric selector
  potential.
- Microscopic derivation of why this potential should arise from the native
  graph dynamics is still open.

