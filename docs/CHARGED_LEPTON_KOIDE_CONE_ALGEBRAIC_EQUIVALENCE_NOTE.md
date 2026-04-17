# Charged-Lepton Koide-Cone Algebraic Equivalence

**Date:** 2026-04-17
**Status:** exact algebraic identity on the retained `hw=1` triplet
**Runners:** `scripts/frontier_charged_lepton_observable_curvature.py` (28 PASS, 0 FAIL)

## Safe statement

On the retained `Cl(3)/Z^3` framework surface, Koide's relation

```
Q  ≡  (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²  =  2/3
```

is equivalent to the equal-character-weight condition
`a_0² = 2|z|²`, where `(a_0, z)` are the `C_3`-character components of
the mass-square-root vector under the retained three-generation
observable algebra.

This equivalence is exact and algebra-only; it makes no reference to
observed charged-lepton mass values.

## Retained inputs

- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
  retained `hw=1` triplet `T_1 = span{X_1, X_2, X_3}`, retained
  translation projectors `P_1, P_2, P_3`, retained induced
  `C_{3[111]}` cycle.
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):
  retained unique additive CPT-even scalar generator, retained
  source-response curvature kernel.

## Construction

Let `v = (v_1, v_2, v_3) = (√m_1, √m_2, √m_3) ∈ ℝ^3_+`. Decompose `v`
under the `C_3` characters using the unitary Fourier transform
on `C_3 = ℤ/3ℤ`:
```
e_+    = (1, 1, 1)/√3                  (trivial character,   χ = 1)
e_ω    = (1, ω, ω²)/√3                 (nontrivial,          χ = ω)
e_{ω²} = (1, ω², ω)/√3                 (nontrivial,          χ = ω²)
```
with `ω = e^{2πi/3}`. Then
```
v = a_0 e_+ + z e_ω + z̄ e_{ω²}
```
with
```
a_0 = (v_1 + v_2 + v_3) / √3           ∈ ℝ
z   = (v_1 + ω̄ v_2 + ω v_3) / √3       ∈ ℂ.
```
(Reality of `v` forces the `e_ω` and `e_{ω²}` coefficients to be
complex conjugate; hence `a_0 ∈ ℝ` and the nontrivial-character
subspace is two-dimensional over `ℝ`.)

## Theorem

**Theorem 1.**
```
Q = 2/3      ⟺      a_0² = 2 |z|².
```

*Proof.* Apply Plancherel/Parseval on the `C_3` character basis:
```
|v|²      = a_0² + 2 |z|²                                        (1)
(Σ v_i)²  = 3 a_0²                                               (2)
```
Equation (1) follows from unitarity of the Fourier transform (the two
complex-conjugate non-trivial components contribute `|z|² + |z̄|² =
2|z|²`). Equation (2) follows because
`Σ v_i = √3 · (v · e_+) = √3 · a_0`.

Now compute Koide's invariant:
```
Q  =  Σ m_i / (Σ √m_i)²
   =  Σ v_i² / (Σ v_i)²
   =  |v|² / (Σ v_i)²
   =  (a_0² + 2 |z|²) / (3 a_0²)
```
using (1) and (2). Setting `Q = 2/3` gives
`3(a_0² + 2|z|²) = 2 · 3 a_0²`, which simplifies to `a_0² = 2|z|²`.
Conversely, substituting `a_0² = 2|z|²` into the `Q` formula gives
`Q = (2|z|² + 2|z|²) / (3 · 2|z|²) = 2/3`. □

## Geometric interpretation

Define the fraction of `|v|²` carried by the trivial-character
subspace:
```
σ  ≡  |v_∥|² / |v|²  =  a_0² / (a_0² + 2|z|²).
```
Then Koide `Q = 2/3` is equivalent to `σ = 1/2`: the mass-square-root
vector sits at exactly **equal norm** between the one-dimensional
trivial-character subspace and the two-dimensional
nontrivial-character subspace. Equivalently, the angle between `v`
and the diagonal `(1, 1, 1)` is exactly **45°**.

## What this does not claim

- Theorem 1 establishes an algebraic equivalence only. It does NOT
  derive Koide `Q = 2/3`; it rephrases the Koide condition in
  `C_3`-character language.
- The theorem is independent of the specific mass values. It holds
  for any positive 3-vector `v` (not only the observed charged-lepton
  mass-square-roots).
- Theorem 1 says nothing about whether the retained framework
  selects the Koide cone. Forcing the physical mass-square-root
  vector onto `a_0² = 2|z|²` requires additional structure; see
  [HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md](./HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)
  and
  [STRUCTURAL_NO_GO_SURVEY_NOTE.md](./STRUCTURAL_NO_GO_SURVEY_NOTE.md).

## Use downstream

- Theorem 1 is the algebraic backbone for the observational-pin
  closure. After a three-real observational pin on the retained
  `hw=1` weight triple, Theorem 1 confirms that the pinned triple
  satisfies Koide whenever the observed mass-square-roots do (a
  tautological consequence of the pin equaling observation).
- Theorem 1 is also the algebraic backbone against which the three
  framework-derives routes (Theorems 4, 5, 6) are structurally
  tested.

## Dependency contract

- `scripts/frontier_three_generation_observable_theorem.py` must PASS
  on live `main` before this runner is trusted.
- `scripts/frontier_hierarchy_observable_principle_from_axiom.py`
  must PASS on live `main`.

## Paper-safe wording

> Koide's relation `Q = 2/3` is rigorously equivalent to the
> equal-character-weight condition `a_0² = 2|z|²` on the retained
> `hw=1` triplet, where `(a_0, z)` are the `C_3`-character components
> of the mass-square-root vector. The equivalence is exact and
> algebra-only.

## Status

**REVIEW.**
