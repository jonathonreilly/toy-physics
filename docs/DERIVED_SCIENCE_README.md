# Derived Science — Framework-Native Lemmas

**Branch:** `claude/main-derived`

Five airtight theorems. Each is a framework-specific identification
or a load-bearing physics-content result — differentiated from
textbook algebra that a reader can re-derive on their own.

## The five

### 1. K_R Vanishes on A1 Backgrounds

Pure S_3 Schur orthogonality applied to the seven-site star tensor
carrier. The components of K_R(q) are inner products with E and
T1 irrep basis vectors; both vanish on A1 backgrounds.

- Note: `KR_A1_VANISHING_DERIVED_NOTE.md`
- Runner: `scripts/frontier_KR_A1_vanishing_proof.py` (30/30 PASS)

### 2. Site-Phase / Cube-Shift Intertwiner

The isometry Φ : C^8 → C^{L³}, |α⟩ ↦ |X_α⟩ (BZ corner states of
Z_L³, L even) satisfies Φ^† P_μ Φ = S_μ, intertwining the
site-phase operator P_μ on the lattice with the cube-shift S_μ
on the taste cube. The canonical bridge between C^8 and C^{L³}
arguments.

- Note: `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`
- Runner: `scripts/frontier_site_phase_cube_shift_intertwiner.py` (60/60 PASS)

### 3. S_3 Axis-Permutation Decomposition of the Taste Cube

C^8 = (C²)^⊗³ decomposes under the axis-permutation S_3 action as

    C^8  ≅  4 · A_1  ⊕  2 · E

(no sign irrep A_2). Each 3-dim Hamming-weight sector (hw=1, hw=2)
carries the standard permutation rep A_1 ⊕ E. The specific
multiplicities (4, 0, 2) are the input for every S_3-invariance
argument on the taste cube.

- Note: `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`
- Runner: `scripts/frontier_s3_action_taste_cube_decomposition.py` (57/57 PASS)

### 4. S_3 Mass-Matrix No-Go on the Hw=1 Triplet

Every S_3-invariant Hermitian operator on the hw=1 triplet has
spectrum (α, α, α+β) — at most 2 distinct eigenvalues. Three
distinct generation masses therefore require spontaneous S_3
breaking. Under S_3 → Z_2 SSB, the allowed Hermitian-operator
space on hw=1 expands from 2 real dims to 5.

- Note: `S3_MASS_MATRIX_NO_GO_NOTE.md`
- Runner: `scripts/frontier_s3_mass_matrix_no_go.py` (13/13 PASS)

### 5. Z_2-Invariant Hw=1 Mass-Matrix Parametrization

In the basis (X_3, X_1, X_2), the 5-dim real space of Z_2-invariant
Hermitian operators on hw=1 is

    M(a, b, c, d)  =  ⎡ a   d   d ⎤        a, b, c ∈ R,
                       ⎢ d*  b   c ⎥        d ∈ C.
                       ⎣ d*  c   b ⎦

Spectrum: λ_sgn = b − c (from the Z_2-sign vector (X_1 − X_2)/√2);
remaining eigenvalues

    λ_±  =  ( (a + b + c) ± √( (a − b − c)² + 8 |d|² ) ) / 2

from the 2×2 secular equation on the Z_2-trivial block. Generic
(a, b, c, d) gives three distinct eigenvalues. The explicit
closed-form relief delivered by S_3 → Z_2 SSB on the hw=1 triplet.

- Note: `Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`
- Runner: `scripts/frontier_z2_hw1_mass_matrix_parametrization.py` (10/10 PASS)

## Verification

```bash
python3 scripts/frontier_KR_A1_vanishing_proof.py                     # PASS=30
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py         # PASS=60
python3 scripts/frontier_s3_action_taste_cube_decomposition.py        # PASS=57
python3 scripts/frontier_s3_mass_matrix_no_go.py                      # PASS=13
python3 scripts/frontier_z2_hw1_mass_matrix_parametrization.py        # PASS=10
```

Total: 170 PASS, 0 FAIL.

Each script exits 0 on success, non-zero on failure.

## Standards

- Every theorem is a pure-math result with explicit proof.
- No structural identifications, no imported SM formulas, no
  empirical values used as derivation inputs.
- Every note lists the classical results applied (Schur's lemma,
  character theory, Fritzsch-texture language, etc.) and the
  framework-specific step — making the applied-vs-invented split
  explicit.
