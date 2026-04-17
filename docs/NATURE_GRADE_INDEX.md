# Nature-Grade Index

**Branch:** `claude/main-derived`

Five airtight theorems — framework-specific identifications or
load-bearing physics-content results. Textbook algebra is not
listed here; a reader is expected to recognize Schur's lemma,
finite-group character theory, and Hermitian spectral calculations
on their own.

## The five

1. **K_R Vanishes on A1 Backgrounds**
   (`KR_A1_VANISHING_DERIVED_NOTE.md`, 30/30 PASS)
   — S_3 Schur orthogonality on the seven-site star tensor; K_R(q)
   projects onto E and T1 irreps, both zero on A1 backgrounds.

2. **Site-Phase / Cube-Shift Intertwiner**
   (`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`, 60/60 PASS)
   — Φ : |α⟩ ↦ |X_α⟩ intertwines P_μ and S_μ. The C^8 ↔ C^{L³}
   bridge.

3. **S_3 Axis-Permutation Decomposition of the Taste Cube**
   (`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`, 57/57 PASS)
   — C^8 ≅ 4·A_1 ⊕ 2·E. Input to every S_3-invariance argument.

4. **S_3 Mass-Matrix No-Go on the Hw=1 Triplet**
   (`S3_MASS_MATRIX_NO_GO_NOTE.md`, 13/13 PASS)
   — Every S_3-invariant Hermitian on hw=1 has spectrum (α, α, α+β);
   SSB required for 3 distinct generation masses.

5. **Z_2-Invariant Hw=1 Mass-Matrix Parametrization**
   (`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`, 10/10 PASS)
   — Explicit 5-parameter Hermitian family on the hw=1 triplet after
   S_3 → Z_2 SSB. Sign eigenvalue b − c separated; remaining
   eigenvalues from a 2×2 secular equation.

## Totals

```
170 total verification checks, 0 failures
```

## Reviewer workflow

```bash
python3 scripts/frontier_KR_A1_vanishing_proof.py
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py
python3 scripts/frontier_s3_action_taste_cube_decomposition.py
python3 scripts/frontier_s3_mass_matrix_no_go.py
python3 scripts/frontier_z2_hw1_mass_matrix_parametrization.py
```

Each exits 0 on success.

## Standards

- Every theorem is a pure-math result with explicit proof.
- No structural identifications, no imported SM formulas, no
  empirical values used as derivation inputs.
- Each note has a "Classical results applied" section naming the
  textbook machinery (Schur's lemma, character theory, secular
  equation, Fritzsch-texture language, etc.) and a "Framework-
  specific step" section identifying the contribution this repo
  makes beyond the classical input.
