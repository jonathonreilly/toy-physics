# Koide A1 Investigation — Final Theoretical Status

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-22
**Iterations:** 13 investigation iterations across multiple sessions

## Work delivered

### New runners on working branch (6 A1-focused + 1 δ verification)

| Runner | PASS | Contribution |
|---|---|---|
| `frontier_koide_a1_quartic_potential_derivation.py` | 5/5 | Koide-Nishiura V(Φ) unique minimum at A1 |
| `frontier_koide_a1_n3_structural_uniqueness.py` | 5/5 | Four Q-formulas converge at n=3 via 3! = 6 |
| `frontier_koide_a1_cv_equals_one.py` | 4/4 | A1 ⟺ coefficient of variation = 1 |
| `frontier_koide_a1_block_democracy_max_entropy.py` | 5/5 | Block-democracy max-entropy principle explicit |
| `frontier_koide_a1_weyl_vector_kostant_coincidence.py` | 6/6 | Three-way match at 1/2 via Kostant |
| `frontier_koide_a1_a2_weyl_double_match.py` | 8/8 | A_1 AND A_2 Weyl vectors both match |
| `frontier_koide_a1_lie_theoretic_triple_match.py` | 10/10 | A1 = `|ω_{SU(2)_L, fund}|²` identified |
| `frontier_koide_a1_yukawa_casimir_identity.py` | 9/9 | `T(T+1) − Y² = 1/2` unique to Yukawa participants |
| `frontier_koide_a1_clifford_dimension_ratio.py` | 6/6 | A1 = dim(spinor)/dim(Cl⁺(3)) cleanest form |
| `frontier_koide_a1_spinor_normalization_proof_attempt.py` | 4/5 | 5th bridge mechanism tested, fails |
| `frontier_koide_radian_bridge_numerical_verification.py` | 3/3 | Radian-bridge empirically forced |

### Imported review-branch theorems (verified passing)

- `frontier_koide_frobenius_isotype_split_uniqueness.py` (SUPPORT_CHAIN=TRUE)
- `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` (16/16 PASS)
- `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` (9/9 PASS)
- `frontier_koide_peter_weyl_am_gm.py` (22/22 PASS)

### Documentation

- `KOIDE_A1_DERIVATION_STATUS_NOTE.md` — 6 closure routes
- `KOIDE_A1_LOOP_INVESTIGATION_SUMMARY.md` — iter-by-iter summary
- `KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md` — 4 bridge mechanisms
- `KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md` — Route A/B/C analysis
- `KOIDE_A1_LOOP_FINAL_STATUS_2026-04-22.md` — this note

## Theoretical status

### Rigorously established (RETAINED + /loop work)

1. **δ = 2/9 via AS/APS** (RIGOROUS, retained + textbook)
2. **Internal AM-GM chain for A1** (RIGOROUS, review branch theorem):
   E_+, E_⊥ forced unique Frobenius-orthogonal projections; AM-GM
   extremum at E_+ = E_⊥ = κ=2 = A1
3. **Spectrum-operator bridge identity** `a₀² − 2|z|² = 3(a² − 2|b|²)`
   (RIGOROUS, review branch)
4. **9 equivalent expressions for A1 = 1/2** (documented in /loop):
   - Pure Clifford dim ratio `dim(spinor)/dim(Cl⁺(3))`
   - Casimir difference `T(T+1) − Y²` (unique to L doublet + Higgs)
   - Lie-theoretic weight squared `|ω_{A_1, fund}|²`
   - ...and 6 others
5. **Radian-bridge postulate empirically forced** (this /loop iter 13):
   Only δ = η (numerically) matches PDG; standard Berry
   convention δ = 2π·η gives negative eigenvalue

### Open physical bridge (NOT CLOSED by any /loop attempt)

**Lemma needed**: the physical charged-lepton packet extremizes
`S_block = log E_+ + log E_⊥` (equivalently, lies at A1/κ=2).

**5 mechanism attempts all fail**:
1. W[J] = log|det D| extremum: wrong answer (|b|/a ≈ 3.3)
2. Coleman-Weinberg 1-loop V_CW: extremum at uniform eigenvalues (Q=1/3)
3. Gaussian max-entropy fixed Frobenius: ⟨a²⟩ = ⟨|b|²⟩ not 2|b|²
4. CV=1 / exponential max-entropy: continuous ≠ discrete 3-point
5. SU(2)_L Clebsch-Gordan normalization: CG same for all y_{αβ}

**Additional findings**:
- 1-loop QFT gauge contributions: uniform sign, cannot give T(T+1) − Y²
  structure
- Instanton corrections: exp(-32π²) ~ 10⁻¹³⁸ suppressed
- MRU SO(2)-quotient route demoted on review branch

## The three closure routes

**Route A (RECOMMENDED)**: Adopt block-total extremum as retained
primitive. Equivalent statements all derive from retained
CL3_SM_EMBEDDING:
- `|b|²/a² = dim(spinor)/dim(Cl⁺(3))`
- `|b|²/a² = T(T+1) − Y²` for Yukawa participants
- `|b|²/a² = |ω_{A_1, fund}|²` (Kostant)

9 natural quantities all equal 1/2 — strongest structural evidence.

**Route B**: Import Koide-Nishiura V(Φ) = [2(trΦ)² − 3tr(Φ²)]² into
retained EW-scalar lane. A1 as VEV minimum via SSB. Standard QFT.

**Route C**: Novel QFT mechanism (anomaly, topological, asymmetric
measure). Open research.

## Handoff

The investigation has produced a comprehensive landscape map. Further
progress now depends on theoretical bridge work, not more iterative
numerical verification.

For review, start with:
- `docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`
- `docs/KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- `docs/KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md`
