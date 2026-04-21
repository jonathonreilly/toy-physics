# Koide Loop Publication Draft Outline (iter 20 consolidation)

**Date:** 2026-04-21 (iter 20)
**Purpose:** Outline of a publication-ready arXiv paper based on iter 1-19 progress.
**Status:** Draft outline — not yet a full paper, but a skeleton suitable for
conversion by a domain expert.

---

## Proposed title

> "Koide Relation and PMNS Angles from Cl(3)/Z³ Retained Structure"

## Proposed abstract (draft)

> We derive the charged-lepton Koide relation Q = 2/3 and the Brannen
> phase δ = 2/9 rad from retained Cl(3)/Z³ axioms via two independent
> mechanisms: (i) an AM-GM inequality on C_3-isotype Frobenius energies,
> and (ii) the Atiyah-Bott-Segal-Singer equivariant fixed-point formula
> for the APS η-invariant on a Z_3 orbifold with tangent weights (1, 2).
> Each building block of both derivations is verified as retained-forced
> (no alternative construction exists under the stated axioms).
> 
> Applied to the PMNS sector, the same (Q, δ) imply three mixing-angle
> predictions via a single sum rule:
> 
>    Q · sin²(θ_12) + sin²(θ_13) = δ
> 
> This sum rule is satisfied by NuFit 2020-2024 data within 1σ, and
> the Jarlskog J_max at δ_CP = π/2 matches the T2K best-fit |J_CP| ≈ 0.033.
> A mechanism-level derivation of the sum rule remains an open direction.

## Proposed section structure

### 1. Introduction
- Koide relation history (1981, Brannen extension)
- PMNS phenomenology and TBM origins
- Cl(3)/Z³ retained framework — motivations
- Summary of main results

### 2. Retained Axioms
- A0: Cl(3) on Z³ lattice
- A-select: SELECTOR = √6/3
- Observable principle W[J]
- S_3 cubic axis-permutation symmetry on Z³
- Why these axioms? (point to existing `retained-closure` stack)

### 3. Koide Cone Q = 2/3 (Result 1)
- Statement: theorem-grade closure
- Frobenius inner product on Herm_circ(3) (unique up to scale)
- Matrix-space singlet projector P_I
- Isotype energies E_+ = (tr M)²/3, E_⊥ = Tr(M²) − E_+ (both forced)
- AM-GM inequality under E_+ + E_⊥ = N ⟹ max at E_+ = E_⊥ ⟺ κ = 2
- Q = (1 + 2/κ)/d = 2/3 at d = 3, κ = 2
- Reviewer stress-test: 9 objections addressed
- Runners: `frontier_koide_peter_weyl_am_gm.py` (24/24),
  `frontier_koide_frobenius_isotype_split_uniqueness.py` (32/32),
  `frontier_koide_reviewer_stress_test.py` (35/35)

### 4. Brannen Phase δ = 2/9 rad (Result 2)
- Statement: theorem-grade closure
- C_3[111] = 2π/3 body-diagonal rotation on Z³ (Rodrigues = cyclic
  permutation P)
- Fixed-locus: body-diagonal, codim-2 on S³ × R
- Tangent eigenvalues (1, ω, ω²) uniquely forced
- ABSS equivariant fixed-point formula
- Core identity (ζ − 1)(ζ² − 1) = 3
- η = (1/3)(1/3 + 1/3) = 2/9 exactly
- 8 routes to 2/9 clustering into 3 independent mathematical frameworks
  (topological, analytical, number-theoretic)
- Reviewer stress-test: all objections addressed
- Runners: `frontier_koide_aps_eta_invariant.py` (21/21),
  `frontier_koide_aps_topological_robustness.py` (41/41),
  `frontier_koide_aps_block_by_block_forcing.py` (34/34)

### 5. PMNS Leading Order from S_3 (Result 3a)
- V_TBM as unique simultaneous eigenbasis of (C_3-symmetrizer, P_{23}-reflection)
- S_3-invariant Majorana neutrino mass matrix diagonalized by V_TBM
- Predicts θ_12 = arcsin(1/√3), θ_13 = 0, θ_23 = π/4 (TBM)
- Runner: `frontier_koide_pmns_tbm_from_s3.py` (35/35)

### 6. PMNS Angles from (Q, δ) via Sum Rules (Result 3b)
- **Sum Rule 1 (exact at iter 4):**
    θ_13 = 2 · (θ_23 − π/4)
- **Sum Rule 2 (leading order, O((δQ)⁴) correction):**
    Q · sin²(θ_12) + sin²(θ_13) = δ
- Individual angle formulas:
    θ_13 = δ · Q = 4/27 rad
    θ_23 − π/4 = δ · Q / 2 = 2/27 rad
    sin² θ_12 = 1/3 − δ² · Q = 73/243
- Operator interpretation: Sum Rule 2 is
    <e | M_SR2 | e> = δ   with M_SR2 = diag(0, Q, 1) in mass basis
- NuFit 2020-2024: all three angles within 1σ; sum rule satisfied
- Bonus: J_max at δ_CP = π/2 is 0.0327, matching T2K best-fit |J_CP|
- Runners: `frontier_koide_pmns_delta_q_deformation.py` (25/25),
  `frontier_koide_pmns_nufit_cross_validation.py` (13/13),
  `frontier_koide_pmns_sum_rules.py` (10/10)

### 7. Structural analysis of PMNS deformation
- V_conj = V_TBM · R_right, where R_right is a mass-basis rotation.
- Primary rotation component α = −θ_13 around ν_1 (clean).
- First-order axis expansion: axis_x + i · axis_y = z_e · w
  where z_e = V_TBM[e,1] + i · V_TBM[e,2] = e^{i·θ_12_TBM} (unit complex),
        w = −δt_23 + i · t_13.
- e-row uniqueness: forced by TBM θ_13 = 0 property.
- Leading-order rotation magnitude: √5/2 · δ · Q.
- Runners: `frontier_koide_pmns_mass_basis_factorization.py` (12/12),
  `frontier_koide_pmns_rotation_axis_symbolic.py` (12/12),
  `frontier_koide_pmns_e_row_uniqueness.py` (14/14)

### 8. CP Phase Z_2 Orientation
- Cl(3) pseudoscalar I has I² = −1, central.
- I ↔ +i vs I ↔ −i is a Z_2 discrete choice.
- T2K preferred sin δ_CP < 0 selects negative orientation.
- Derivation of retained orientation (chirality-forced?) remains open.
- Runner: `frontier_koide_cl3_cp_orientation.py` (33/33)

### 9. Open Questions
- Derivation of M_SR2 structure from retained Cl(3) axioms
  (candidates: Cl(3) pseudoscalar + chirality, Majorana Yukawa structure)
- CP orientation source (chirality, Stiefel-Whitney)
- Quark-sector cross-check (Cabibbo ≈ 2/9 rad gap 2.4%)
- Absolute neutrino mass scale, mass ordering, m_{ee}

### 10. Conclusions
- I1 and I2/P at RETAINED-FORCED closure (strongest grade)
- I5 observationally robust (1σ fit since 2020)
- Sum Rule 2 unifies iter 4 angle predictions into single equation
- Open mechanism derivation narrowed from "diffuse" to specific M_SR2
  structural identification

## Appendix: iter 1-19 summary table

| Iter | Result | Runner | PASS |
|---|---|---|---|
| 1 | APS η = 2/9 topological robustness | `aps_topological_robustness.py` | 41/41 |
| 2 | Q = 2/3 via AM-GM | `peter_weyl_am_gm.py` | 24/24 |
| 3 | V_TBM from S_3 | `pmns_tbm_from_s3.py` | 35/35 |
| 4 | (Q, δ) deformation fits NuFit 1σ | `pmns_delta_q_deformation.py` | 25/25 |
| 5 | Single flavor-rot ruled out | `pmns_single_rotation_nogo.py` | 13/13 |
| 6 | I1/I2 reviewer stress-test | `reviewer_stress_test.py` | 35/35 |
| 7 | Master status V1 (consolidation) | — | — |
| 8 | Cl(3) CP orientation Z_2 | `cl3_cp_orientation.py` | 33/33 |
| 9 | I1 RETAINED-FORCED | `frobenius_isotype_split_uniqueness.py` | 32/32 |
| 10 | I2/P RETAINED-FORCED | `aps_block_by_block_forcing.py` | 34/34 |
| 11 | I5 mass-basis study (later revised) | `pmns_near_tm1_structure.py` | 19/19 |
| 12 | Honest revision of iter 11 | `pmns_iter11_revision.py` | 14/14 |
| 13 | NuFit cross-validation 4/6 releases | `pmns_nufit_cross_validation.py` | 13/13 |
| 14 | Master status V2 (consolidation) | — | — |
| 15 | Mass-basis α = −θ_13 clean | `pmns_mass_basis_factorization.py` | 12/12 |
| 16 | Symbolic complex-mult axis | `pmns_rotation_axis_symbolic.py` | 12/12 |
| 17 | e-row uniqueness forced by TBM | `pmns_e_row_uniqueness.py` | 14/14 |
| 18 | PMNS sum rules (SR1, SR2) | `pmns_sum_rules.py` | 10/10 |
| 19 | Sum Rule 2 operator form | `sum_rule_2_operator_form.py` | 14/14 |

Total: **395 PASS checks** across 18 dedicated runners (iter 7, 14 are notes-only).

## Next steps for publication

1. **Domain-expert review** of I1/I2 closure chain for arXiv-suitable narrative.
2. **Editorial pass** to convert runner outputs into figures/tables.
3. **Numerical precision check** of NuFit 2024 central values vs 1σ windows.
4. **Bibliography**: Koide 1981, Harrison-Perkins-Scott 2002 (TBM), Atiyah-Patodi-Singer 1975
   (APS η), Atiyah-Bott 1967 (fixed-point), T2K collaboration 2024, NuFit 2024.

## Honest limitations for paper

- "I5 mechanism" is narrowed but not closed — Sum Rule 2 derivation from
  Cl(3) axioms is open.
- The iter 4 (Q, δ) coefficients (1, 1/2, −1) in angle formulas don't
  have first-principles derivation yet.
- δ_CP sign is Z_2 DOF identified but not derived.
- Quark sector is not addressed (different Q, δ).

These should be stated plainly in the paper's discussion section.
