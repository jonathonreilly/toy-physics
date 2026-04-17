# Z_2-Invariant Hw=1 Mass-Matrix Parametrization

**Status:** airtight
**Runner:** `scripts/frontier_z2_hw1_mass_matrix_parametrization.py` (10/10 PASS)

## Classical results applied

- **Schur's lemma** (Schur 1905), applied to the Z_2 decomposition
  V_1 ≅ 2·1 ⊕ sgn: dim End(V_1)^{Z_2} = 2² + 1² = 5.
- **Hermitian matrix spectral theorem** (standard linear algebra).
- **Secular equation for 2×2 Hermitian blocks** (the quadratic
  formula applied to the characteristic polynomial of a Hermitian
  2×2 matrix).
- **Texture-analysis language from the flavor-physics literature**
  (Fritzsch 1977; nearest-neighbor-interaction / GST, Gatto–Sartori–
  Tonin 1968; Ramond–Roberts–Ross 1993). We adopt the standard
  "texture + block-diagonal spectrum" organization of Hermitian
  mass matrices.

## Framework-specific step

Identification of V_1 with the hw=1 triplet of the taste cube
C^8 = (C²)^⊗³ and Z_2 = ⟨(12)⟩ with the residual subgroup of S_3
that arises from the V_sel axis-selection SSB pattern.

## Framework object

The 5-dimensional real space of Z_2-invariant Hermitian operators
on V_1 = span(X_1, X_2, X_3) with Z_2 = ⟨(12)⟩ swapping axes 1 and 2
and fixing axis 3. Schur's lemma applied to V_1 ≅ 2·1 ⊕ sgn fixes
the dim at 5; this theorem gives the explicit parametrization and
closed-form spectrum.

## Theorem

1. In the ordered basis (X_3, X_1, X_2), every Z_2-invariant
   Hermitian operator on V_1 has the form

        M(a, b, c, d)  =  ⎡ a       d       d    ⎤
                           ⎢ d*      b       c    ⎥
                           ⎣ d*      c       b    ⎦

   with a, b, c ∈ R and d ∈ C. Real parameter count: 5, matching
   dim End(V_1)^{Z_2}_{Hermitian} = 2² + 1² = 5 (Schur's lemma
   applied to V_1 ≅ 2·1 ⊕ sgn).

2. The Z_2-sign eigenvector (X_1 − X_2)/√2 is an exact eigenvector
   of M with eigenvalue

        λ_sgn  =  b − c.

3. On the 2-dim Z_2-trivial subspace spanned by X_3 and
   (X_1 + X_2)/√2, M acts as the 2×2 Hermitian block

        B  =  ⎡ a         √2 · d   ⎤
               ⎣ √2 · d*   b + c    ⎦

   with eigenvalues given by the secular equation

        λ_±  =  ( (a + b + c) ± √( (a − b − c)² + 8 |d|² ) ) / 2.

4. Generic (a, b, c, d) ∈ R^5 (with d ∈ C ≅ R^2) gives three
   distinct eigenvalues {λ_sgn, λ_+, λ_−}. Degenerate subloci
   (two or more eigenvalues coincide) are algebraic subvarieties
   of positive codimension in R^5 and hence of Lebesgue measure 0.

5. The S_3-invariant limit is the 2-parameter sublocus d = 0 and
   a = b + c; in that limit the spectrum collapses to
   {b − c, b + c, b + c}, exhibiting at most 2 distinct eigenvalues
   (consistent with the S_3 Mass-Matrix No-Go,
   `S3_MASS_MATRIX_NO_GO_NOTE.md`).

## Proof sketch

(1) Fixed-point equation U_Z2 M U_Z2 = M on a 3×3 Hermitian matrix
gives the stated constraints M_{11} = M_{22} = b, M_{12} = c,
M_{01} = M_{02} = d, with a, b, c real and d complex. (2) Direct
check: the sign vector has components (0, 1, −1)/√2, and
M · v_sgn = (b − c) · v_sgn. (3) Change basis to
(X_3, (X_1 + X_2)/√2, (X_1 − X_2)/√2); M becomes block-diagonal
with the 2×2 block B as stated, and the 2×2 secular equation gives
λ_±. (4) The degeneracy conditions λ_sgn = λ_±, λ_+ = λ_− are each
non-trivial polynomial equations in (a, b, c, Re d, Im d), cutting
out positive-codimension subvarieties. (5) Substituting d = 0 and
a = b + c collapses the discriminant to 0 and λ_± = b + c (double),
giving spectrum {b − c, b + c, b + c}.

## Verification

The runner (a) confirms that 10 random M(a, b, c, d) are Hermitian
and Z_2-invariant, (b) checks the full Z_2-invariant Hermitian space
has real dim 5 by projecting a 9-element Hermitian basis of End(V_1)
through the Z_2-averaging projector, (c) verifies the sign-vector
eigenvalue λ_sgn = b − c for 5 random samples, (d) verifies the 2×2
block form matches the prediction for 10 samples, (e) verifies the
{b − c, λ_+, λ_−} spectrum matches numerical eigenvalues for 10
samples, (f) samples 500 random parameter tuples and finds > 99%
give 3 distinct eigenvalues, (g) explicitly constructs the
S_3-invariant limit (d = 0, a = b + c) and confirms exactly 2
distinct eigenvalues, consistent with the S_3 Mass-Matrix No-Go.

## Reusability

- Closed-form parametrization for any framework construction that
  requires a Z_2-invariant Hermitian mass matrix on the hw=1
  generation triplet with prescribed spectrum.
- Completes the post-SSB chain: S_3 Mass-Matrix No-Go (SSB is
  necessary for 3 distinct masses) → Schur on V_1 ≅ 2·1 ⊕ sgn
  (dim 2 → 5 relief under S_3 → Z_2) → this theorem (explicit
  5-parameter family, separated sign eigenvalue b − c, trivial-
  block secular equation for the other two eigenvalues).
- Sets the stage for further sublocus analysis (NNI texture,
  Fritzsch zeros, etc.) within the 5-parameter family.
