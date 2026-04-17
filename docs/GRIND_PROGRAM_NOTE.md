# Grind Program: Reusable Framework-Native Lemmas

**Date:** 2026-04-16 (program opened)
**Branch:** `claude/main-derived`
**Bar:** strictly unbounded — each theorem must be a pure-math result
applied to a specific framework object, with no structural identifications,
no scope bridges, no imported formulas, no downstream dependencies.

## Purpose

Produce small reusable algebraic theorems that can be composed into
larger derivations for the framework's major lanes (CKM, mass
hierarchy, gauge structure, confinement, etc.).

## Protocol

1. Each theorem is a self-contained result with:
   - A precisely stated claim (no "within scope of X" qualifiers)
   - A proof using standard textbook math (group theory, linear algebra,
     representation theory, finite-group characters, etc.)
   - An explicit runner that verifies the claim numerically to machine
     precision
   - Zero imports from SM / empirical values / structural identifications

2. Each theorem is 3x-checked against the bar:
   - Check 1: does the proof actually work as stated?
   - Check 2: does any step hide a bridge or structural identification?
   - Check 3: would a hostile reviewer find a gap?

3. Theorems ship in small batches (2-4 at a time) once each has passed
   3x check.

4. Session work (including rejected candidates) preserved on
   `claude/stoic-almeida` for reference.

## Batches

### Batch 1: Cube-shift and BZ-corner foundational algebra

- **Cube-Shift Joint-Eigenstructure Theorem** — the three cube-shift
  operators S_μ on C^8 pairwise commute and admit a simultaneous
  eigenbasis of 8 one-dim joint eigenspaces, indexed by sign triples
  s ∈ {±1}³, with explicit construction via Z_2³ Hadamard characters.
  Note: `CUBE_SHIFT_JOINT_EIGENSTRUCTURE_NOTE.md`
  Runner: `frontier_cube_shift_joint_eigenstructure.py` (69/69 PASS)

- **Translation-Eigenvalue Theorem on BZ Corners** — on Z_L³ (L even),
  the discrete translation T_μ acts on the BZ corner state |X_α⟩
  (α ∈ {0,1}³) as T_μ |X_α⟩ = (−1)^{α_μ} |X_α⟩. Generalizes the
  hw=1 translation result on main.
  Note: `TRANSLATION_EIGENVALUE_BZ_CORNERS_NOTE.md`
  Runner: `frontier_translation_eigenvalue_bz_corners.py` (70/70 PASS)

- **Hamming-Distance Selection Rule** — products of site-phase
  operators P_μ on C^{L³} act on BZ corners via ⟨X_β|P_{μ_1}...P_{μ_k}|X_α⟩
  = δ_{α ⊕ β, ⊕_i e_{μ_i}}. The minimum k connecting α and β equals
  the Hamming distance H(α ⊕ β). Consequence: hw=1 ↔ hw=1 transitions
  require ≥ 2 site-phase insertions.
  Note: `HAMMING_DISTANCE_SELECTION_RULE_NOTE.md`
  Runner: `frontier_hamming_distance_selection_rule.py` (473/473 PASS)

- **Site-Phase / Cube-Shift Intertwiner Theorem** (composition) — the
  site-phase P_μ on the BZ-corner subspace is intertwined with the
  cube-shift S_μ on C^8 via the isometry Φ: |α⟩ ↦ |X_α⟩. This is the
  canonical bridge between C^8 taste-cube arguments and C^{L³}
  lattice arguments.
  Note: `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`
  Runner: `frontier_site_phase_cube_shift_intertwiner.py` (60/60 PASS)

### Batch 2: S_3 / axis-permutation + parity structure

- **C₃[111] Cyclic-Permutation Action on All BZ Corners** — the axis
  cycle unitary U on C^8 has U³ = I; orbit structure 1 + 3 + 3 + 1
  (two fixed points, two 3-cycles); U S_μ U⁻¹ = S_{cyclic(μ)}.
  Extends main's hw=1 cycle to the full taste cube.
  Note: `C3_CYCLIC_ACTION_BZ_CORNERS_NOTE.md`
  Runner: `frontier_c3_cyclic_action_bz_corners.py` (32/32 PASS)

- **S₃ Axis-Permutation Decomposition of the Taste Cube** — C^8 ≅
  4·A_1 ⊕ 2·E as S_3 representation. Each 3-dim sector (hw=1, hw=2)
  carries the standard permutation rep A_1 ⊕ E. The sign irrep A_2
  does NOT appear in C^8.
  Note: `S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`
  Runner: `frontier_s3_action_taste_cube_decomposition.py` (57/57 PASS)

- **Hamming-Weight Parity Conservation** — even-order polynomials
  in site-phase P_μ preserve the hw-parity decomposition
  C^{L³}_{BZ} = C^4_{even-hw} ⊕ C^4_{odd-hw}; odd-order swap them.
  Explicit parity projectors Π_± = (1 ± T_1 T_2 T_3) / 2.
  Note: `HW_PARITY_CONSERVATION_NOTE.md`
  Runner: `frontier_hw_parity_conservation.py` (68/68 PASS)

## Reusability claim

These theorems are cited in any downstream derivation involving:
- The taste cube / staggered fermion taste structure
- BZ corner states and their algebraic properties
- Selection rules on gauge-mediated transitions
- CKM atlas derivations (framework-native)
- Mass matrix structure on hw=k sectors
- CPT, Lorentz, projector algebra applications
- Any argument that bridges the abstract taste cube (C^8) with the
  physical lattice (C^{L³})

Each replaces a "by inspection" or "direct computation" step in larger
arguments with a named citable theorem.

## Triple-check discipline

Lessons from the earlier triple-check:
- "Within scope of X" is a bridge — not allowed
- Structural identifications with downstream physics — not allowed
- Algebraic claims that don't rigorously follow from the stated
  mechanism — not allowed (e.g., off-diagonal mass-matrix from
  diagonal propagator)
- Trivial textbook results with no framework-specific content — not
  useful enough to ship

## Non-goals

This program is NOT:
- A flagship paper
- A replacement for main's existing content
- A substitute for the larger research program on Yukawa/CKM/masses
- A promise that any specific flagship claim will be reached

It IS: a sustainable engine of small, reusable, rigorous theorems.
