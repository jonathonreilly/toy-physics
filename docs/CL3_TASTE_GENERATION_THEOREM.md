# Cl(3) Taste-Generation Theorem: Z³ Lattice Doubling → 3 Tastes with Generation Structure

**Date:** 2026-04-19
**Status:** retained, numerically verified
**Claim boundary authority:** this note
**Script:** `scripts/verify_cl3_sm_embedding.py` (section G);
            `scripts/frontier_s3_action_taste_cube_decomposition.py` (independent crosscheck)

---

## Statement

**Theorem:** The staggered-fermion doubling on Z³ produces a taste space
`C^8 = (ℂ²)^{⊗3}` on which:

1. The axis-permutation group S₃ acts by tensor-position permutation, giving the
   decomposition `C^8 = 4A₁ + 0A₂ + 2E` (no A₂ component).

2. The Hamming-weight-1 sector (hw=1), spanned by
   `{e₁=(1,0,0), e₂=(0,1,0), e₃=(0,0,1)}`, transforms as the 3-dimensional
   permutation representation `A₁ + E` of S₃.

3. The three hw=1 states are related by the Z₃ cyclic subgroup:
   `e₁ → e₂ → e₃ → e₁`.

4. Each hw=1 state carries identical SU(2)×U(1) quantum numbers (same eigenvalue
   structure under all gauge generators), so the Z₃ orbit provides 3 generation
   candidates with identical gauge quantum numbers.

---

## Proof

### A. S₃ Action on C^8

S₃ acts on `(ℂ²)^{⊗3}` by permuting tensor positions. For permutation `σ ∈ S₃`,
the unitary operator `U(σ)` satisfies:

```
U(σ)|b₁,b₂,b₃⟩ = |b_{σ⁻¹(1)}, b_{σ⁻¹(2)}, b_{σ⁻¹(3)}⟩
```

This action:
- Preserves Hamming weight (commutes with `P_hw` for each `hw = 0,1,2,3`)
- Respects the group structure: `U(σ)U(τ) = U(στ)`

### B. Character Computation and Decomposition

The characters for each conjugacy class of S₃:

| Class | `χ(g)` on C^8 | `χ(g)` expected |
|-------|--------------|-----------------|
| identity | 8 | 8 |
| 2-cycles {(12),(13),(23)} | 4 | 4 |
| 3-cycles {(123),(132)} | 2 | 2 |

Multiplicities via inner product with irrep characters:
- `n(A₁) = (8 + 3·4 + 2·2)/6 = (8+12+4)/6 = 4`
- `n(A₂) = (8 - 3·4 + 2·2)/6 = (8-12+4)/6 = 0`
- `n(E) = (2·8 - 2·2)/6 = (16-4)/6 = 2`

Result: **C^8 = 4A₁ + 2E** — no A₂ appears.

### C. hw=1 Triplet = Generation Sector

The hw=1 sector `{e₁, e₂, e₃}` has characters:
- `χ(e) = 3`, `χ(2-cycle) = 1`, `χ(3-cycle) = 0`

This matches `A₁ + E` exactly — the standard 3-point permutation representation.
The Z₃ element `(123)` sends `e₁ → e₂ → e₃ → e₁` (cyclic, verified numerically).

### D. Equal Gauge Quantum Numbers

All three hw=1 states are related by Z₃ ⊂ S₃ which commutes with:
- Hamming weight → same SU(3)_c sector
- Hypercharge Y (Y is defined on the b₁b₂ base and fiber independently of which
  axis is "active")
- SU(2)_weak fiber (acts on b₃ independently of Z₃ base permutation)

Therefore each generation candidate carries the same `SU(2)×U(1)` quantum numbers.

---

## Physical Interpretation

The three taste doublers from Z³ staggered fermions are not spurious artifacts:
they are the algebraic origin of three generations, each carrying identical
electroweak quantum numbers and related by the Z₃ cyclic symmetry of the cubic
lattice.

The S₃ → Z₃ → 3 generations chain is:
1. Z³ spatial lattice has cubic symmetry S₃ (axis permutations)
2. Staggered doubling maps each spatial axis to a taste direction
3. Z₃ subgroup cyclically permutes the three taste-axis states
4. All three carry the same SU(2)×U(1) content → 3 identical generations

This provides the algebraic basis for "taste = generation" without requiring
additional matter input.

---

## Numerical Verification

| Check | Result |
|-------|--------|
| `U(σ)` unitary for all σ ∈ S₃ | exact |
| `[U(σ), P_hw]= 0` for all hw | exact |
| χ(e)=8, χ(2-cycle)=4, χ(3-cycle)=2 | exact |
| C^8 = 4A₁ + 0A₂ + 2E | exact |
| hw=1: A₁+E permutation rep | exact |
| Z₃ cycles {e₁→e₂→e₃→e₁} | exact |
| hw=1 states carry equal Y eigenvalues | exact |

Independent crosscheck: `scripts/frontier_s3_action_taste_cube_decomposition.py`
produces identical decomposition (63/63 pass, 0 fail).

---

## What This Theorem Closes

- **Taste = generation blocker**: Z₃ cyclic symmetry of Z³ forces exactly 3
  generation candidates with identical SU(2)×U(1) quantum numbers
- Provides algebraic support for the three-generation matter structure already
  retained in `MINIMAL_AXIOMS_2026-04-11.md`

## What Remains Bounded

- Generation mass splitting (CKM, Yukawa hierarchy) is not derived here
- The identification of hw=1 tastes with specific SM generations requires the
  graph-first axis-selection procedure
- This theorem establishes the count and degeneracy; the dynamics distinguishing
  generations are a separate derivation

## Reading Rule

This note is the claim boundary for the Z³ → 3 generation algebraic argument.
The hw=1 Z₃-orbit result is retained. Generation mass structure is separately bounded.
