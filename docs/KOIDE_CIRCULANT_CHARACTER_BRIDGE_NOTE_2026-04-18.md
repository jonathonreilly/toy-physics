# Koide Circulant / Character Bridge Note

**Date:** 2026-04-18
**Status:** exact algebraic bridge on the candidate Koide lane; does not alter
the current retained charged-lepton status
**Runner:** `scripts/frontier_koide_circulant_character_bridge.py`

## Safe statement

Let
```
H = a·I + b·C + b̄·C²
```
be a `C_3`-circulant Hermitian on the retained `hw=1` triplet, with
`C = C_3[111]`. Let `λ = (λ_0, λ_1, λ_2)` be its eigenvalue triple. Then the
`C_3` character coefficients `(a_0, z)` of the triple `λ` satisfy
```
a_0 = √3 · a,
z   = √3 · b.
```
Consequently,
```
a_0² = 2 |z|²    ⟺    3a² = 6|b|².
```

So the circulant-matrix equipartition condition
`3a² = 6|b|²` is exactly the operator-space restatement of the Koide
equal-character-weight condition on the eigenvalue triple.

## Why this matters

The April 17 charged-lepton review package already isolated Koide as the
equal-character-weight condition
```
a_0² = 2 |z|²
```
on the mass-square-root vector. The new circulant lane introduces the matrix
parameters `(a, b)` from the natural `C_3[111]` commuting Hermitians. This note
proves that these are not two unrelated stories:

- the **review package** works in character space of the spectral triple;
- the **circulant lane** works in operator space of the commuting Hermitian;
- the bridge between them is exact.

## Proof

Write `ω = e^{2πi/3}`. The eigenvalues of `H` are
```
λ_k = a + b ω^k + b̄ ω^{-k}.
```
Take the `C_3` Fourier decomposition of the triple `λ`:
```
a_0 = (λ_0 + λ_1 + λ_2) / √3,
z   = (λ_0 + ω̄ λ_1 + ω λ_2) / √3.
```
Using the standard root-of-unity sums
```
1 + ω + ω² = 0,
1 + ω̄ω + ωω̄ = 3,
```
one gets
```
a_0 = √3 · a,
z   = √3 · b.
```
Then
```
a_0² - 2|z|² = 3a² - 6|b|²,
```
so the two equalities are equivalent.

## Consequence for the science stack

This bridge cleans up the charged-lepton science stack:

- `A1` in the April 18 circulant note is **not** a new independent primitive.
- It is the matrix-space form of the same equal-character-weight condition
  already isolated in
  [CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md](./CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md).
- The genuine unresolved science is the **selection principle** for that
  equality, not the bridge itself.

On the current package, the sharpest named selection principle remains the
real-irrep-block-democracy lane in
[HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](./HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md).

## Selection-principle bridge

Define the operator-space block energies
```
E_+   = 3a²,
E_⊥   = 6|b|².
```
Then `A1` is simply
```
E_+ = E_⊥.
```

Now consider the unweighted block-log-volume functional
```
S = log(E_+) + log(E_⊥)
```
at fixed total Frobenius norm
`E_tot = E_+ + E_⊥`. Its unique stationary point is
```
E_+ = E_⊥ = E_tot / 2,
```
with negative second derivative, so it is the unique maximum.

This is exactly the April 17 **real-irrep-block-democracy** primitive, but
expressed on the circulant operator blocks instead of directly on the
character-space powers. So the science stack does not carry two separate open
selection principles:

- April 17: equal weighting of the trivial and nontrivial real-irrep blocks;
- April 18 circulant lane: equal weighting of the diagonal and off-diagonal
  circulant Frobenius blocks.

They are the same candidate principle under the exact bridge above.

## What this does not claim

- It does **not** derive the selection principle `3a² = 6|b|²`.
- It does **not** derive the identification `λ_k = √m_k`.
- It does **not** upgrade the current retained charged-lepton status, which
  remains the bounded April 17 review package.

## Paper-safe wording

> On the retained `hw=1` triplet, the `C_3[111]`-commuting Hermitian operators
> are circulants `H = aI + bC + \bar b C²`. The Fourier coefficients of the
> eigenvalue triple are exactly `a_0 = √3 a` and `z = √3 b`. Hence the matrix
> equipartition condition `3a² = 6|b|²` is algebraically identical to the Koide
> equal-character-weight condition `a_0² = 2|z|²`. This is an exact bridge
> between the circulant operator lane and the April 17 character-space review
> package; the missing science remains the selection principle for that
> equality.
