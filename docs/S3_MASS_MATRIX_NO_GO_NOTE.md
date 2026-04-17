# S_3 Mass-Matrix No-Go Note

**Date:** 2026-04-17
**Status:** exact support theorem on the retained `hw=1` carrier
**Script:** `scripts/frontier_s3_mass_matrix_no_go.py`
**Authority role:** canonical symmetry constraint for mass-like Hermitian
operators on the `hw=1` triplet

## Safe statement

Let `V = span(X_1, X_2, X_3)` be the `hw=1` triplet with the natural
axis-permutation action of `S_3`. Then `V ~= A_1 + E`, and every
`S_3`-invariant Hermitian operator on `V` has the form

```text
M = alpha I_3 + beta P_(A_1),
```

where `P_(A_1) = J_3 / 3` is the orthogonal projector onto the symmetric line.
Hence every such operator has spectrum

```text
{alpha, alpha, alpha + beta},
```

so the exact unbroken `S_3` class allows at most two distinct eigenvalues on
the `hw=1` carrier.

Under the residual axis-fixing subgroup `Z_2 < S_3`, the invariant Hermitian
space expands to real dimension `5`.

## Classical results applied

- Schur's lemma on `V ~= A_1 + E`
- the Hermitian spectral theorem
- the fixed-space dimension formula `dim End(V)^G = sum_i m_i^2`

## Framework-specific step

- identification of the retained `hw=1` triplet as the relevant generation
  carrier for this support theorem
- reuse of the exact taste-cube `S_3` decomposition on the current package
  surface

## Why it matters on `main`

This note is not a retained flavor-numerics claim. Its safe job is narrower:
it gives the exact symmetry-theoretic boundary for any future flavor lane that
tries to keep the `hw=1` carrier inside an unbroken `S_3` mass class. On that
carrier, a three-way split requires leaving the exact `S_3`-invariant class.

## Verification

Run:

```bash
python3 scripts/frontier_s3_mass_matrix_no_go.py
```

The runner checks the invariant-algebra dimension, the form
`alpha I_3 + beta P_(A_1)`, the forced two-value spectrum, and the residual
`Z_2` dimension jump from `2` to `5`.
