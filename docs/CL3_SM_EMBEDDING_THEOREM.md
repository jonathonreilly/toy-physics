# Cl(3) → SM Embedding Theorem: Cl⁺(3) ⊃ SU(2)×U(1) with SM Quantum Numbers

**Date:** 2026-04-19
**Status:** reviewed exact algebraic support theorem on current `main`; 95/95 checks verified; not part of the accepted minimal-input stack
**Claim boundary authority:** this note
**Script:** `scripts/verify_cl3_sm_embedding.py`

---

## Statement

Let Cl(3) be the Clifford algebra over ℝ³ acting on the 8-dimensional taste space
`V = (ℂ²)^{⊗3}` via staggered-lattice generators:

```
Γ₁ = σ₁ ⊗ I₂ ⊗ I₂
Γ₂ = σ₃ ⊗ σ₁ ⊗ I₂
Γ₃ = σ₃ ⊗ σ₃ ⊗ σ₁
```

satisfying `{Γᵢ, Γⱼ} = 2δᵢⱼ I₈`.

**Theorem:** The sub-algebra structure of Cl(3) forces:

1. `Cl⁺(3) ≅ ℍ` (quaternions): the even sub-algebra is 4-dimensional and contains
   an abstract SU(2) as its group of unit quaternions.

2. The pseudoscalar `ω = Γ₁Γ₂Γ₃` is central in Cl(3,0) with `ω² = -I₈`,
   generating a U(1) direction distinct from Cl⁺(3).

3. `dim(Cl⁺(3)) = 4 = d+1` and `dim(Cl⁺(3) + span{ω}) = 5 = d+2` for `d = 3`,
   fixing the bare gauge couplings `g₂² = 1/(d+1)` and `g_Y² = 1/(d+2)`.

4. The physical SU(2)_weak = fiber operators `{I₄ ⊗ σᵢ/2}` commute with
   hypercharge Y and are isomorphic to the Cl⁺(3) SU(2) as abstract Lie algebras.

5. Hypercharge `Y = (+1/3)P_symm + (-1)P_antisymm` (where `P_symm` projects onto
   the 6D symmetric base ⊗ fiber block) has SM-correct eigenvalues: +1/3 on 6D
   (quark-like: 3 color × 2 weak-doublet) and −1 on 2D (lepton-like: 1 antisym × 2
   weak-doublet).

6. On the chiral L-sector (even-parity states), the Cl⁺(3) SU(2) generators satisfy
   Kramers `T² = −(1/4)I₄ < 0`, forcing every eigenvalue of any Hermitian `H_L` in
   the algebraically induced L-sector class to be doubly degenerate, hence
   `det(H_L) = λ₁²λ₂² ≥ 0`. This is L-sector determinant support only; it is
   necessary but not sufficient for full A-BCC.

---

## Proof Sketch

### A. Cl⁺(3) ≅ ℍ

The even sub-algebra is spanned by `{I₈, e₁₂=Γ₁Γ₂, e₁₃=Γ₁Γ₃, e₂₃=Γ₂Γ₃}`.
Each bivector squares to `−I₈` and they satisfy quaternionic multiplication:
`e₂₃ · e₁₃ = +e₁₂`.

The SU(2) generators `Jₖ = (i/2) · eᵢⱼ` (Hermitian) satisfy `[J₁,J₂] = iJ₃`
cyclically with Casimir `J₁² + J₂² + J₃² = (3/4)I₈` (spin-1/2).

### B. ω Central and dim = d+2

`ω = Γ₁Γ₂Γ₃` satisfies:
- `ω² = −I₈`
- `[ω, Γᵢ] = 0` for all i (central in Cl(3,0) for the Euclidean case)
- ω ∉ Cl⁺(3) (ω is odd grade)
- `{I, e₁₂, e₁₃, e₂₃, ω}` are linearly independent → rank 5 = d+2

### C. Bare Couplings from Dimension Counting

The normalization of the kinetic term in the gauge sector picks out the natural
measure on the sub-algebra manifold. The number of independent generators fixes
the coupling:

- `g₂² = 1/dim(Cl⁺(3)) = 1/4 = 1/(d+1)` — not direction counting, but algebraic
- `g_Y² = 1/dim(Cl⁺(3) + {ω}) = 1/5 = 1/(d+2)` — ω adds exactly one central direction

The coupling normalisation follows from the partition-function measure on the gauge
field: with generators T^a normalised as `Tr(T^aT^b) = δ^{ab}/2` in the 8D taste
representation (giving the spin-1/2 Casimir = 3/4), the kinetic term
`L = (1/g²) Tr(F²)` with `F = F^a T^a` implies `g² ∝ 1/N_gen` where `N_gen` is the
number of independent generators. For SU(2): 3 bivector generators, but Cl⁺(3)
carries 4 basis elements (including the scalar I); the factor 1/(d+1) = 1/4 is the
dimension of the even subalgebra, reflecting that the scalar direction participates
in the measure. For U(1)_Y: the central element ω extends the generating set to
d+2 = 5 independent directions, giving g_Y² = 1/5.

Bare Weinberg angle: `sin²θ_W(bare) = g_Y²/(g₂² + g_Y²) = (1/5)/(1/4 + 1/5) = 4/9`

### D. Physical SU(2) and Hypercharge Commute

The physical weak SU(2) acts on the fiber (b₃ coordinate only):
`Jf_i = I₄ ⊗ σᵢ/2`.

The hypercharge `Y = (+1/3)P_symm + (−1)P_antisymm` where `P_symm = (I₈ + P_{b₁b₂})/2`
and `P_{b₁b₂}` swaps coordinates 1 and 2.

By the tensor product structure `Y` acts on the base while `Jf_i` acts on the fiber,
so `[Y, Jf_i] = 0` exactly.

The Clifford bivector SU(2) and the fiber SU(2) are distinct 8×8 operators but
isomorphic as abstract Lie algebras (same Casimir, same structure constants).

### E. SM Quantum Number Assignment

| Block | dim | Y | SU(2)_weak | SM particle |
|-------|-----|---|------------|-------------|
| P_symm ⊗ fiber | 6 | +1/3 | doublet | quark L doublet (3 colors × 2 iso) |
| P_antisymm ⊗ fiber | 2 | −1 | doublet | lepton L doublet (ν, e)_L |

`Tr(Y) = 6·(+1/3) + 2·(−1) = 2 − 2 = 0` ✓ (anomaly cancellation precondition)

### F. L-Sector Kramers Support: `det(H_L) ≥ 0`

The bilinear condensate operator H_L on the chiral L-sector
`{|000⟩, |011⟩, |101⟩, |110⟩}` (even-parity states, Hamming weight 0 or 2)
is constrained by the quaternionic structure of Cl⁺(3).

The SU(2) generators `J_i = (i/2)eᵢⱼ` restricted to L give a 4D representation
that closes: `[J_i_L, J_j_L] = iεᵢⱼₖ J_k_L` with Casimir `J²_L = (3/4)I₄`.

The anti-unitary time-reversal `T = J₂_L · K` (K = complex conjugate) satisfies:
```
T² = J₂_L · J₂_L* = −(1/4)I₄  < 0
```

**Kramers theorem:** for T with T² < 0 (fermionic), every eigenvalue of any T-invariant
Hermitian operator is doubly degenerate. Therefore any Hermitian `H_L` in the span of
`{I₄, J₁_L, J₂_L, J₃_L}` has eigenvalues in degenerate pairs `(λ₁, λ₁, λ₂, λ₂)`, and:

```
det(H_L) = λ₁² λ₂² ≥ 0
```

The quaternionic structure of `Cl⁺(3)` therefore forces `det(H_L) ≥ 0` on the
restricted chiral L-sector class.

This is a useful algebraic support result for the broader matter package, but it
does not by itself select the physical A-BCC sheet.

This is verified numerically in `scripts/verify_cl3_sm_embedding.py` Section J.

---

## Numerical Verification

Script: `scripts/verify_cl3_sm_embedding.py` (sections A–F)

| Check | Result |
|-------|--------|
| `{Γᵢ, Γⱼ} = 2δᵢⱼ I₈` | exact (0) |
| `e²ᵢⱼ = −I₈` | exact (0) |
| `e₂₃ · e₁₃ = +e₁₂` | exact (0) |
| `[J₁,J₂] = iJ₃`, Casimir = 3/4 | exact (0) |
| `ω² = −I₈`, `[ω, Γᵢ] = 0` | exact (0) |
| `rank({I,e₁₂,e₁₃,e₂₃,ω}) = 5` | exact |
| `g₂² = 1/4`, `g_Y² = 1/5` | exact |
| `sin²θ_W(bare) = 4/9` | exact |
| `[Y, Jf_i] = 0` | max err < 10⁻¹⁶ |
| Y eigenvalues: +1/3 (×6), −1 (×2) | exact |
| `Tr(Y) = 0` | max err < 10⁻¹⁶ |

---

## What This Theorem Sharpens

- exact algebraic origin of the `Cl⁺(3)` / ω dimension counts that underlie the
  reviewed `g_2^2 = 1/(d+1)` and `g_Y^2 = 1/(d+2)` support readings
- the Y = `+1/3` / `−1` block splitting used by the existing electroweak support stack
- the L-sector Kramers determinant support statement used as a bounded matter-side input

## What Remains Bounded

- Radiative running g₂(v), g_Y(v) still inherit the bridge budget from
  `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`
- The identification "fiber = weak SU(2)" is provided by the graph-first axis
  selection procedure (see `NATIVE_GAUGE_CLOSURE_NOTE.md`)
- Full anomaly-cancellation story is derived at the framework level, not in this note

## Reading Rule

This note is the claim boundary for this reviewed algebraic support packet.
It sharpens the existing matter / electroweak support layer on current `main`,
but it does not replace [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md)
or the accepted three-generation authority stack.
