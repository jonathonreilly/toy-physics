# Nature-Grade Index

**Branch:** `claude/main-derived`
**Updated:** 2026-04-16 (Grind Program Batch 6)

## Airtight results on this branch

### Standing (session carryover)

- **K_R Vanishes on A1 Backgrounds** (`KR_A1_VANISHING_DERIVED_NOTE.md`)
  — S_3 Schur orthogonality applied to the seven-site star tensor
  carrier. 30/30 PASS.

### Batch 1: cube-shift and BZ-corner foundational algebra

- **Cube-Shift Joint-Eigenstructure Theorem**
  (`CUBE_SHIFT_JOINT_EIGENSTRUCTURE_NOTE.md`) — joint eigenbasis of
  S_1, S_2, S_3 on C^8 via Z_2³ Hadamard characters. 69/69 PASS.

- **Translation-Eigenvalue Theorem on BZ Corners**
  (`TRANSLATION_EIGENVALUE_BZ_CORNERS_NOTE.md`) — T_μ |X_α⟩ =
  (−1)^{α_μ} |X_α⟩ for all α ∈ {0,1}³. Full 8-dim generalization of
  the hw=1 result on main. 70/70 PASS.

- **Hamming-Distance Selection Rule**
  (`HAMMING_DISTANCE_SELECTION_RULE_NOTE.md`) — minimum number of
  site-phase operators connecting two BZ corners equals the Hamming
  distance between their α-labels. 473/473 PASS.

- **Site-Phase / Cube-Shift Intertwiner Theorem** (composition)
  (`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`) — canonical bridge
  C^8 ↔ C^{L³}_{BZ corners} via Φ: |α⟩ ↦ |X_α⟩ intertwining S_μ and P_μ.
  60/60 PASS.

### Batch 2: S_3 / axis-permutation + parity structure

- **C₃[111] Cyclic-Permutation Action on All BZ Corners**
  (`C3_CYCLIC_ACTION_BZ_CORNERS_NOTE.md`) — the axis-cycle unitary U
  on C^8 has U³ = I; orbit structure 1 + 3 + 3 + 1; two 3-cycles
  (hw=1 and hw=2). 32/32 PASS.

- **S₃ Axis-Permutation Decomposition of the Taste Cube**
  (`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`) — C^8 ≅ 4·A_1 ⊕ 2·E as S_3
  representation; no A_2 component. 57/57 PASS.

- **Hamming-Weight Parity Conservation**
  (`HW_PARITY_CONSERVATION_NOTE.md`) — even/odd-order polynomials in
  site-phase operators preserve/swap the hw-parity decomposition.
  Explicit projectors Π_± = (1 ± T_1 T_2 T_3)/2. 68/68 PASS.

### Batch 3: S_3-invariant algebra + hw-parity refinement

- **S_3-Invariant Operator Dimension on C^8**
  (`S3_INVARIANT_OPERATOR_DIMENSION_NOTE.md`) — dim End(C^8)^{S_3} = 20
  via Schur's lemma (4² + 0² + 2² = 20). 14/14 PASS.

- **Hadamard Basis: Simultaneous T_μ Eigenbasis + S_3 Label Action**
  (`HADAMARD_S3_COMPOSITION_NOTE.md`) — Hadamard basis diagonalizes
  each T_μ; S_3 acts by label permutation. Composition of Batch 1
  (intertwiner) and Batch 2 (S_3 / hw-parity). 117/117 PASS.

- **S_3 Decomposition of Hw-Parity Blocks**
  (`S3_HW_PARITY_BLOCK_DECOMPOSITION_NOTE.md`) — each hw-parity block
  V_± decomposes as 2·A_1 ⊕ E; refines total to 5+5+5+5 = 20. Shows
  10 S_3-invariants preserve hw-parity and 10 swap it. 20/20 PASS.

### Batch 4: cube-shift polynomial algebra + S_3 mass-matrix no-go

- **Cube-Shift Polynomial Algebra on C^8**
  (`CUBE_SHIFT_POLYNOMIAL_ALGEBRA_NOTE.md`) — the polynomial algebra
  A_S = ⟨I, S_1, S_2, S_3⟩ is abelian, 8-dim with basis the 8
  squarefree monomials M_T, and coincides with the full algebra of
  Hadamard-diagonal operators on C^8 (maximal abelian). 8/8 PASS.

- **S_3-Invariant Subalgebra of the Cube-Shift Polynomial Algebra**
  (`S3_INVARIANT_POLYNOMIAL_SUBALGEBRA_NOTE.md`) — A_S^{S_3} is
  4-dim with canonical basis {e_0, e_1, e_2, e_3} (elementary
  symmetric polynomials in the cube-shifts); strictly contained in
  the 20-dim End(C^8)^{S_3}. 21/21 PASS.

- **S_3 Mass-Matrix No-Go on the Hw=1 Triplet**
  (`S3_MASS_MATRIX_NO_GO_NOTE.md`) — every S_3-invariant Hermitian
  operator on the hw=1 triplet has spectrum (α, α, α+β) with at most
  2 distinct eigenvalues; SSB S_3 → Z_2 expands the allowed space
  from 2 to 5 real dimensions. 13/13 PASS.

### Batch 5: post-SSB structure + hw-grading refinement

- **Residual Z_2 Commutant on C^8**
  (`RESIDUAL_Z2_COMMUTANT_NOTE.md`) — C^8 ≅ 6·1 ⊕ 2·sgn as Z_2 rep;
  dim End(C^8)^{Z_2} = 40, doubling the S_3 case. Hw=1 restricted
  commutant jumps from 2 to 5 dims, sufficient for 3 distinct
  eigenvalues. 23/23 PASS.

- **Hw-Graded Decomposition of End(C^8)^{S_3}**
  (`S3_INVARIANT_HW_GRADED_DECOMPOSITION_NOTE.md`) — the 20-dim
  S_3-invariant commutant splits as 6 (hw-preserving) + 14
  (hw-changing). Refines Batch 3's hw-parity 10+10 split by full
  hw grading. 21/21 PASS.

- **Hw=1 ↔ Hw=2 S_3-Equivariant Iso via e_3**
  (`HW1_HW2_S3_EQUIVARIANT_ISO_NOTE.md`) — the top elementary
  symmetric polynomial e_3 = S_1 S_2 S_3 restricts to a unitary
  S_3-equivariant bijection V_1 → V_2 taking X_i to X_{jk}. Shows
  V_1 ≅ V_2 as S_3 reps (both A_1 ⊕ E). 29/29 PASS.

### Batch 6: Z_3 structure, hw=1 mass-matrix parametrization, lattice pullback

- **Z_3 Cyclic-Subgroup Commutant on C^8**
  (`Z3_CYCLIC_COMMUTANT_NOTE.md`) — Schur + Z_3 character theory
  applied to the taste cube: C^8 ≅ 4·1 ⊕ 2·χ_ω ⊕ 2·χ_{ω²} under
  Z_3 = ⟨(123)⟩, giving dim End(C^8)^{Z_3} = 24 (4-dim increase over
  the S_3 case). 20/20 PASS.

- **Z_2-Invariant Hw=1 Mass-Matrix Parametrization**
  (`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`) — explicit
  5-parameter family M(a, b, c, d) of Hermitian Z_2-invariant
  operators on hw=1; sign eigenvalue λ_sgn = b − c; remaining
  eigenvalues λ_± from the 2×2 secular equation on the trivial
  subspace. 10/10 PASS.

- **Pullback of S_3 Invariants via Site-Phase/Cube-Shift Intertwiner**
  (`INTERTWINER_PULLBACK_S3_INVARIANTS_NOTE.md`) — standard
  functoriality of commutants transports every Batch 3/4/5
  S_3-invariant result from C^8 to the BZ-corner subspace of
  C^{L³} via the Batch 1 intertwiner. 25/25 PASS.

## Totals

```
1180 total verification checks, 0 failures
```

## Reviewer workflow

```bash
# Standing
python3 scripts/frontier_KR_A1_vanishing_proof.py

# Batch 1
python3 scripts/frontier_cube_shift_joint_eigenstructure.py
python3 scripts/frontier_translation_eigenvalue_bz_corners.py
python3 scripts/frontier_hamming_distance_selection_rule.py
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py

# Batch 2
python3 scripts/frontier_c3_cyclic_action_bz_corners.py
python3 scripts/frontier_s3_action_taste_cube_decomposition.py
python3 scripts/frontier_hw_parity_conservation.py

# Batch 3
python3 scripts/frontier_s3_invariant_operator_dimension.py
python3 scripts/frontier_hadamard_s3_composition.py
python3 scripts/frontier_s3_hw_parity_block_decomposition.py

# Batch 4
python3 scripts/frontier_cube_shift_polynomial_algebra.py
python3 scripts/frontier_s3_invariant_polynomial_subalgebra.py
python3 scripts/frontier_s3_mass_matrix_no_go.py

# Batch 5
python3 scripts/frontier_residual_z2_commutant.py
python3 scripts/frontier_s3_invariant_hw_graded_decomposition.py
python3 scripts/frontier_hw1_hw2_s3_equivariant_iso.py

# Batch 6
python3 scripts/frontier_z3_cyclic_commutant.py
python3 scripts/frontier_z2_hw1_mass_matrix_parametrization.py
python3 scripts/frontier_intertwiner_pullback_s3_invariants.py
```

Each exits 0 on success, nonzero on failure. Each prints a TOTAL
line with PASS / FAIL counts.

## Standards maintained

- Every claim is a pure-math theorem with explicit proof
- No structural identifications (like "equivalent to alpha_s at scale v")
- No scope bridges (like "within the class of standard methods")
- No imported SM formulas or empirical values
- No downstream physics dependencies for the theorem itself
- Downstream applications flagged explicitly when present

## Grind program

See `GRIND_PROGRAM_NOTE.md` for the program's purpose, protocol,
and triple-check discipline.

## Relation to main

These theorems extend or complement existing airtight content on main:
- CMT (partition function identity)
- V_sel EWSB selector derivation (cube-shift Hermiticity + commutativity
  used, not the joint-eigenstructure which is added here)
- Anomaly-forced 3+1
- Native SU(2), graph-first SU(3)
- Three-generation observable algebra (hw=1 translation result,
  generalized here to full 8-dim)
- Discrete 3+1 GR + UV-finite QG chain
- CPT, I_3=0, emergent Lorentz

The new theorems are building blocks for future derivations, not
replacements for existing work.
