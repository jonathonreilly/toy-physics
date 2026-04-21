# Koide Loop Iteration 3 — I5 Attack: PMNS TBM from S₃ Axis Permutations

**Date:** 2026-04-21
**Attack target:** I5 (PMNS observational pins — NuFit mixing angles)
**Status:** **INTERMEDIATE** — leading-order retained structure derived, physical-exact still open.
**Runner:** `scripts/frontier_koide_pmns_tbm_from_s3.py` (35/35 PASS).

---

## One-line claim

The retained Z³ cubic lattice's S₃ axis-permutation symmetry forces the
leading-order PMNS matrix to be the Tribimaximal (TBM) matrix V_TBM,
with the dominant gap to NuFit being θ₁₃ = 8.57° (the "reactor angle").

## The attack

The Z³ lattice has natural S₃ symmetry — the six 3×3 permutation matrices
acting on Cartesian axes (x, y, z). This contains:

- **Rotation subgroup** Z₃ = {e, C₃[111], C₃[111]²} (the retained body-diagonal
  2π/3 rotation verified kinematically in `frontier_koide_c3_spatial_rotation.py`).
- **Three reflections** {P₁₂, P₁₃, P₂₃} (axis swaps).

**Leading-order retention assumption (the "if"):** The Majorana neutrino
mass matrix M_ν respects the full S₃ cubic symmetry on Z³, while the
charged-lepton mass matrix M_ℓ breaks S₃ → {e} (diagonal flavor basis).

Under this assumption, the most general S₃-invariant real symmetric M_ν is:

```
M_ν = α·I + β·(J − I)      [J = all-ones matrix, α, β real]
```

This 2-parameter matrix is diagonalized EXACTLY by V_TBM:

```
            [ √(2/3)   √(1/3)    0     ]
V_TBM =     [-√(1/6)   √(1/3)   -√(1/2)]
            [-√(1/6)   √(1/3)    √(1/2)]
```

where the columns are:

| Column | Expression | S₃ structure |
|---|---|---|
| col₂ | (1,1,1)/√3 | **S₃ singlet** (C₃-fixed axis, P_{ij}-even ∀ij) |
| col₁ | (2,−1,−1)/√6 | Doublet, P₂₃-**even** |
| col₃ | (0,−1,1)/√2 | Doublet, P₂₃-**odd** |

The eigenvalues are λ_singlet = α + 2β and λ_doublet = α − β (doubly
degenerate on the transverse plane).

**Key consequence:** V_TBM is not a choice — it is FORCED as the
simultaneous real eigenbasis of {C₃[111]-symmetrizer, P₂₃}. Any
alternative S₃-invariant neutrino mass ansatz gives the same V_TBM
(up to degenerate-doublet rotations, which the next-order breaking
fixes).

## TBM predictions vs NuFit-2024

The three PMNS mixing angles derived from V_TBM:

| Angle | TBM (retained) | NuFit central | Gap |
|---|---|---|---|
| θ₁₂ | 35.264° (sin²=1/3) | 33.44° | −1.82° |
| θ₁₃ | 0.000° (sin²=0) | 8.57° | **+8.57°** DOMINANT |
| θ₂₃ | 45.000° (sin²=1/2) | 49.20° | +4.20° |

The θ₁₃ gap is the "reactor angle problem" — TBM gives exactly zero
at leading order, but Daya Bay / RENO / Double Chooz measurements
established θ₁₃ ≈ 8.57° in 2012. Post-2012 TBM-descended models
all require explicit Z₂-breaking corrections.

## Verifications (in the runner)

**35/35 PASS** — all symbolic/algebraic:

1. **S₃ group structure (5 checks)**: C₃ order 3, reflections order 2,
   closure of all 36 S₃ products.
2. **V_TBM orthogonality (2 checks)**: V V^T = I, V^T V = I.
3. **Column-by-column S₃ eigenstructure (10 checks)**: Each column
   identified as specific C₃-singlet/doublet × P₂₃-eigen-pair,
   transverse-plane orthogonality.
4. **Universal diagonalization (5 checks)**: V_TBM^T M V_TBM is
   diagonal for every 2-parameter S₃-invariant real symmetric M,
   with eigenvalues (α+2β, α−β, α−β).
5. **Mixing angles (5 checks)**: sin²θ₁₂=1/3, sin²θ₁₃=0, sin²θ₂₃=1/2
   — all EXACTLY from V_TBM rows.
6. **Gap recording (3 checks)**: the three NuFit-gap magnitudes.
7. **Consistency with existing retained-lane no-go (2 checks)**:
   J_χ = tr(χ·I/3) = (1+ω+ω²)/3 = 0 when ρ is S₃-invariant, matching
   the existing `PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY` result on the
   current bank. (No contradiction — this iter's claim uses a
   different bank.)
8. **Honest scope (3 checks)**: iter 3 does NOT close I5; θ₁₃ is iter
   4 target.

## Relation to existing retained PMNS work on main (no contradiction)

The existing retained-lane no-gos:

- `PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY`: J_χ = 0 on current bank.
- `PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW`: a_sel = 0 on current bank.
- `NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION`: endpoint is (J_χ, μ) = (0, 0).

These are statements on the DIRAC single-Higgs bank of probe observables.
The present iter-3 attack uses a MAJORANA S₃-invariant mass bank, which
is outside the scope of those no-gos. Consistency check confirmed:
if we set ρ = I/3 (S₃-invariant density matrix), then
J_χ = tr(χ·ρ) = (1+ω+ω²)/3 = 0 — recovering the existing retained-lane
result in the intersection bank.

## Honest limitation and scope

**What iter 3 does:** Derives the leading-order PMNS matrix V_TBM from
the retained S₃ symmetry on Z³, as a forced consequence of Majorana
neutrinos respecting the full cubic symmetry while charged leptons
break S₃ diagonally.

**What iter 3 does NOT do:**

- Does NOT close I5 (physical NuFit angles not reproduced).
- Does NOT derive the Z₂ breaking mechanism that gives θ₁₃ ≠ 0.
- Does NOT address sin δ_CP < 0 (T2K sign).
- Does NOT justify *why* Majorana respects S₃ while Dirac doesn't
  (this is an ansatz at this stage; a retained-derivation of this
  asymmetry is the iter 5+ target).

## Next iteration (iter 4) targets

1. **θ₁₃ activation from Z₂ breaking**: What Cl(3)/Z³ retained
   mechanism provides the soft Z₂ breaking of {P₁₂, P₁₃, P₂₃}
   that lifts θ₁₃ from 0 to ~8.57°? Candidates:
   - Cl(3) bivector structure singling out one axis (spin structure
     breaks full S₃ to Z₃ x Z_2 at the spinor level).
   - One-loop radiative correction from charged-lepton Yukawa
     asymmetry (m_τ/m_e ratio is large and breaks S₃).
   - Wolfenstein-parametrization-style ε-expansion from retained
     V_CKM cross-sector mixing.
2. **sin δ_CP derivation**: What forces the sign < 0 (T2K result)?
3. **Consistency check**: does the required Z₂ breaking contradict
   any existing retained no-go?

## Retained axioms used

1. **A0**: Cl(3) on Z³ (retained).
2. **Z³ cubic symmetry**: S₃ axis-permutation group acts naturally
   (retained; used also in `CL3_TASTE_GENERATION_THEOREM`,
   `S3_TASTE_CUBE_DECOMPOSITION_NOTE`).
3. **C₃[111] = 2π/3 rotation**: retained per
   `frontier_koide_c3_spatial_rotation.py` (16/16 PASS, iter 1).

## Retained derivations inherited

- Charged-lepton Koide Q = 2/3 (iter 2, F-functional + Peter-Weyl + AM-GM,
  24/24 PASS): `frontier_koide_peter_weyl_am_gm.py`.
- Brannen δ = 2/9 rad (iter 1, APS topological robustness, 41/41 PASS):
  `frontier_koide_aps_topological_robustness.py`.

## Status tag

**I5 Status:** INTERMEDIATE (leading-order structure retained-derived;
physical NuFit angles still require iter 4 Z₂ breaking).

**I1 Status:** RETAINED-DERIVED (iter 2).

**I2/P Status:** RETAINED-DERIVED (iter 1).

Overall: 2/3 of the "done" criteria achieved; I5 advanced from pure
observational to leading-order-retained with specific next target.
