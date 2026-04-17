# Derived Science — Grind Program, Batch 1

**Branch:** `claude/main-derived`
**Date:** 2026-04-16

Strictly unbounded theorems. Each is a pure-math result applied to a
specific framework object, with no structural identifications, no
scope bridges, no imported formulas.

## Standing airtight result (session carryover)

- **K_R Vanishes on A1 Backgrounds** — pure S_3 Schur orthogonality
  applied to the seven-site star tensor carrier. The components of
  K_R(q) are inner products with E and T1 irrep basis vectors; both
  vanish on A1 backgrounds.
  Note: `KR_A1_VANISHING_DERIVED_NOTE.md`
  Runner: `frontier_KR_A1_vanishing_proof.py` (30/30 PASS)

## Batch 3: S_3-invariant algebra + hw-parity refinement

Three more reusable theorems, including two compositions that bridge
the earlier batches.

### 8. S_3-Invariant Operator Dimension on C^8

`dim End(C^8)^{S_3} = 20`. Direct consequence of the S_3 Taste-Cube
Decomposition (C^8 ≅ 4·A_1 ⊕ 2·E) via Schur's lemma: Σ m_irrep² =
4² + 0² + 2² = 20.

- Note: `S3_INVARIANT_OPERATOR_DIMENSION_NOTE.md`
- Runner: `frontier_s3_invariant_operator_dimension.py` (14/14 PASS)

### 9. Hadamard Basis: Simultaneous T_μ Eigenbasis + S_3 Label Action (composition)

The Hadamard basis |ψ_s⟩ diagonalizes each T_μ (eigenvalue s_μ)
and each hw-parity projector. S_3 acts by label permutation on s.
Bridges Batch 1 (Hadamard / intertwiner) with Batch 2 (S_3 /
hw-parity) into a unified picture.

- Note: `HADAMARD_S3_COMPOSITION_NOTE.md`
- Runner: `frontier_hadamard_s3_composition.py` (117/117 PASS)

### 10. S_3 Decomposition of Hw-Parity Blocks (composition)

Each 4-dim hw-parity block V_± decomposes under S_3 as
2·A_1 ⊕ E. Hence among the 20 S_3-invariants on C^8, exactly 10
preserve hw-parity and exactly 10 swap it. Refines theorem 8 with
explicit block structure.

- Note: `S3_HW_PARITY_BLOCK_DECOMPOSITION_NOTE.md`
- Runner: `frontier_s3_hw_parity_block_decomposition.py` (20/20 PASS)

## Batch 2: S_3 / axis-permutation + parity structure

Three new reusable theorems strengthening the algebraic toolkit.

### 5. C₃[111] Cyclic-Permutation Action on All BZ Corners

The axis-cycle unitary on C^8 has U³ = I; its orbit structure on the
computational basis is 1 + 3 + 3 + 1, with two 3-cycles (hw=1 and hw=2)
and two fixed points (hw=0 and hw=3). Extends main's hw=1 observable
theorem to the full taste cube.

- Note: `C3_CYCLIC_ACTION_BZ_CORNERS_NOTE.md`
- Runner: `frontier_c3_cyclic_action_bz_corners.py` (32/32 PASS)

### 6. S₃ Axis-Permutation Decomposition of the Taste Cube

S_3 acts on C^8 with hw-orbit structure 1 + 3 + 3 + 1. As an S_3
representation, C^8 ≅ 4·A_1 ⊕ 2·E (no sign-irrep A_2 appears).
Each 3-dim sector (hw=1, hw=2) carries the standard permutation
representation A_1 ⊕ E.

- Note: `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`
- Runner: `frontier_s3_action_taste_cube_decomposition.py` (57/57 PASS)

### 7. Hamming-Weight Parity Conservation

Even-order polynomials in site-phase operators P_μ preserve the
hw-parity decomposition C^8_{BZ} = C^4_{even-hw} ⊕ C^4_{odd-hw};
odd-order polynomials swap the two subspaces. Explicit parity
projectors Π_± = (1 ± T_1 T_2 T_3) / 2.

- Note: `HW_PARITY_CONSERVATION_NOTE.md`
- Runner: `frontier_hw_parity_conservation.py` (68/68 PASS)

## Batch 1: cube-shift and BZ-corner foundational algebra

Four small reusable theorems establishing the canonical bridge
between the abstract taste cube C^8 and the physical lattice C^{L³}.

### 1. Cube-Shift Joint-Eigenstructure Theorem

The three cube-shift operators S_μ on C^8 pairwise commute and admit
a simultaneous eigenbasis of 8 one-dimensional joint eigenspaces,
indexed by sign triples s ∈ {±1}³. Explicit construction via
Z_2³ Hadamard characters.

- Note: `CUBE_SHIFT_JOINT_EIGENSTRUCTURE_NOTE.md`
- Runner: `frontier_cube_shift_joint_eigenstructure.py` (69/69 PASS)

### 2. Translation-Eigenvalue Theorem on BZ Corners

On Z_L³ (L even), the discrete translation T_μ acts on BZ corner
states |X_α⟩ with α ∈ {0,1}³ as T_μ |X_α⟩ = (−1)^{α_μ} |X_α⟩. This
generalizes the hw=1 translation result on main to the full 8-dim
BZ corner spectrum.

- Note: `TRANSLATION_EIGENVALUE_BZ_CORNERS_NOTE.md`
- Runner: `frontier_translation_eigenvalue_bz_corners.py` (70/70 PASS)

### 3. Hamming-Distance Selection Rule

The minimum number of site-phase operators (P_μ with (P_μ ψ)(x) =
(−1)^{x_μ} ψ(x)) needed to connect two BZ corners equals the Hamming
distance between their α-labels. Consequently, hw=1 ↔ hw=1 transitions
require at least two site-phase insertions.

- Note: `HAMMING_DISTANCE_SELECTION_RULE_NOTE.md`
- Runner: `frontier_hamming_distance_selection_rule.py` (473/473 PASS)

### 4. Site-Phase / Cube-Shift Intertwiner Theorem (composition)

The site-phase P_μ on the BZ-corner subspace of C^{L³} is intertwined
with the cube-shift S_μ on C^8 via the isometry Φ: |α⟩ ↦ |X_α⟩. This
is the canonical bridge between C^8 taste-cube arguments and C^{L³}
lattice arguments.

- Note: `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`
- Runner: `frontier_site_phase_cube_shift_intertwiner.py` (60/60 PASS)

## All-batch verification

```bash
# Standing
python3 scripts/frontier_KR_A1_vanishing_proof.py                # PASS=30

# Batch 1
python3 scripts/frontier_cube_shift_joint_eigenstructure.py      # PASS=69
python3 scripts/frontier_translation_eigenvalue_bz_corners.py    # PASS=70
python3 scripts/frontier_hamming_distance_selection_rule.py      # PASS=473
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py    # PASS=60

# Batch 2
python3 scripts/frontier_c3_cyclic_action_bz_corners.py          # PASS=32
python3 scripts/frontier_s3_action_taste_cube_decomposition.py   # PASS=57
python3 scripts/frontier_hw_parity_conservation.py               # PASS=68

# Batch 3
python3 scripts/frontier_s3_invariant_operator_dimension.py          # PASS=14
python3 scripts/frontier_hadamard_s3_composition.py                  # PASS=117
python3 scripts/frontier_s3_hw_parity_block_decomposition.py         # PASS=20

# Total: 1010 PASS, 0 FAIL
```

## Grind program philosophy

The program is defined in `GRIND_PROGRAM_NOTE.md`. Its purpose is
sustainable production of reusable framework-native theorems at
strict unbounded bar. Each theorem becomes a citable lemma for
larger derivations.

## Out of scope (not in this branch)

- Quantitative CKM / Yukawa / mass predictions (conjectural)
- Plaquette ⟨P⟩ derivation work (on main, under separate review)
- Flagship paper content
- Structural identifications of any kind
