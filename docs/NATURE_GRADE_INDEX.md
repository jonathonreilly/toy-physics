# Nature-Grade Index

**Branch:** `claude/main-derived`
**Updated:** 2026-04-16 (Grind Program Batch 1)

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

## Totals

```
859 total verification checks, 0 failures
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
