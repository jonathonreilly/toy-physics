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

## Batch 1 total verification

```bash
python3 scripts/frontier_cube_shift_joint_eigenstructure.py      # PASS=69
python3 scripts/frontier_translation_eigenvalue_bz_corners.py    # PASS=70
python3 scripts/frontier_hamming_distance_selection_rule.py      # PASS=473
python3 scripts/frontier_site_phase_cube_shift_intertwiner.py    # PASS=60
python3 scripts/frontier_KR_A1_vanishing_proof.py                # PASS=30

# Total: 702 PASS, 0 FAIL
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
