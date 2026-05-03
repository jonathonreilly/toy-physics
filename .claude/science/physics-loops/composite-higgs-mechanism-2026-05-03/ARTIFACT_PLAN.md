# Artifact Plan — Cycle 20 (Route B)

## Deliverables

1. **Loop pack** at `.claude/science/physics-loops/composite-higgs-mechanism-2026-05-03/`
   - STATE.yaml (resume surface)
   - GOAL.md (target + V1-V5)
   - ASSUMPTIONS_AND_IMPORTS.md (premise audit)
   - ROUTE_PORTFOLIO.md (5 routes scored)
   - OPPORTUNITY_QUEUE.md
   - ARTIFACT_PLAN.md (this file)
   - CLAIM_STATUS_CERTIFICATE.md (V1-V5 + status)
   - HANDOFF.md (post-cycle)

2. **Source note** at
   `docs/COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md`.
   Sections:
   - Header (date, status, runner, authority role)
   - A_min (minimal allowed premise set)
   - Forbidden imports
   - Worked attempt (Route B candidate analysis)
     - Step 1: Z3 cyclic group acting on generation triplet of bilinears
     - Step 2: Z3-covariant composite scalar Φ_eff = ⟨q̄_L u_R⟩ + ω⟨q̄_L d_R⟩ + ω²⟨l̄_L e_R⟩
     - Step 3: SU(2) × U(1)_Y quantum numbers of Z3 components
     - Step 4: Multi-channel suppression of effective top Yukawa
     - Step 5: Counterfactual on Z3 phase relations (1, ω², ω vs 1, ω, ω²)
     - Step 6: Mass-ratio constraints from Z3 symmetry
   - Three named residual obstructions (NO1: Z3 generation action; NO2:
     equal-magnitude condensate; NO3: strong-coupling magnitude)
   - What this narrows (sharpens cycle 08 O1/O2/O3 with candidate)
   - What this does NOT close (the strong-coupling magnitude itself)
   - Honest status

3. **Runner** at `scripts/frontier_composite_higgs_mechanism.py`. Aim for
   PASS=N/0 with N ≥ 20. Verifies:
   - Cycle 06 derived rep used at one hop (counterfactual: wrong rep
     gives wrong Y_total)
   - Cycle 08 quantum-number match recovered for q̄_L u_R, q̄_L d_R,
     l̄_L e_R bilinears
   - Z3 cube-root-of-unity arithmetic: 1 + ω + ω² = 0 exactly
   - Z3 phase covariance of multi-channel composite Φ_eff
   - SU(2) × U(1)_Y quantum numbers preserved across Z3 components
   - Multi-channel condensate basin dimension count
   - Counterfactual: alternative Z3 phase assignments give incompatible
     SU(2) × U(1)_Y structure
   - Counterfactual: single-channel condensation (one bilinear only)
     does NOT have Z3-invariant total
   - Three named obstructions explicit in note
   - Forbidden imports check (no PDG values consumed)
   - Effective top-Yukawa suppression formula
   - Multi-bilinear selector resolution via Z3 representation
   - Mass-ratio relations across Z3 components
   - Goldstone-mode counting for multi-channel condensate
   - Cycle 15 g_2² = 1/4 used at one hop (no admitted G_weak = 0.653)

## Out-of-scope (named as obstructions, not attempted)

- Strong-coupling magnitude derivation (cycle 08 O1 / NO3)
- Z3 generation action on quark sector derivation (NO1)
- Equal-magnitude condensate derivation (NO2)
- Specific value of v_EW from framework primitives
- Specific value of m_top, m_H, m_W, m_Z from framework primitives
