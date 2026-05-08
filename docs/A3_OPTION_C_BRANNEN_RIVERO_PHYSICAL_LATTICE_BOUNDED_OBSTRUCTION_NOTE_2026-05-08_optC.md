# A3 Option C — Brannen-Rivero / Physical-Lattice Re-identification: Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_obstruction
**Claim type:** bounded_obstruction
**Status:** source-note proposal that **bounds** the Option C closure path
(Brannen-Rivero Fourier-basis re-identification under physical-lattice
reading) for AC_φλ. Result: Option C does NOT close AC_φλ under retained
content alone. Five named admissions are required (substrate-semantic
physical-lattice; A1 √2-equipartition; P1 √m identification; δ rad-unit
bridge; v_0 scale). The structural sub-claim R1+R2 (circulant form +
Brannen-Rivero eigenvalue spectrum) IS retained on hw=1, providing genuine
progress vs Routes 1-5 of the prior 10-probe campaign. Empirical match to
PDG charged-lepton masses < 0.003% per generation; Koide Q to 6 × 10⁻⁶.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** action-first-principles-bridge-gap-salvage-2026-05-08
**Primary runner:** [`scripts/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.py`](../scripts/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.py)
**Cache:** [`logs/runner-cache/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.txt`](../logs/runner-cache/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.txt)

## Authority disclaimer

This is a source-note proposal. Effective `effective_status` is generated
by the audit pipeline only after the independent audit lane reviews the
claim, dependency chain, and runner. The `claim_type`, scope, named
admissions, and bounded-obstruction classification are author-proposed;
the audit lane has full authority to retag, narrow, or reject the proposal.

## Question

The 10-probe campaign of PRs #709-#723 proved structural impossibility of
deriving A3 from A1+A2 under the standard "lattice as mathematical
regulator" interpretation. Under the user's proposed re-framing — "the
physical-lattice IS physical" + retained Brannen-Rivero / Koide-Brannen
lane + R1's circulant-equivariance theorem — the proposed closure chain
is:

```
[1] Physical-lattice substrate-semantic reading (load-bearing as retained)
    →
[2] R1+R2 circulant theorem on hw=1 (retained)
    →
[3] Brannen-Rivero formula λ_k = a + 2|b|cos(arg b + 2πk/3)
    →
[4] Empirical match to PDG charged-lepton masses
    →
[5] AC_φλ closure: 3 mass eigenstates ARE 3 SM generations
```

**Does this chain close AC_φλ via retained content?**

## Answer

**NO.** Under retained content alone, the chain has FIVE non-retained
admissions:

| # | Admission | Where it enters | Retained status |
|---|---|---|---|
| 1 | Substrate-semantic physical-lattice ("lattice IS physical") | Step 1 | NOT retained (PHYSICAL_LATTICE_NECESSITY_NOTE narrowed 2026-05-02; sibling notes open) |
| 2 | A1 (√2 equipartition) | Step 3 | NOT retained per KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18 |
| 3 | P1 (√m identification) | Step 3 | NOT retained per same note |
| 4 | δ rad-unit bridge | Step 3 | NOT retained per same note |
| 5 | v_0 scale derivation | Step 3 | HEURISTIC NEAR-MATCH only per same note |

The structural sub-claim R1+R2 (circulant form + Brannen-Rivero eigenvalue
spectrum) IS retained as axiom-clean per the Koide circulant character note,
which is genuine progress. But the closure of AC_φλ requires Steps 1, 3, 4
to be retained or for empirical match in Step 4 to serve as derivation —
and the framework's no-PDG-import-as-derivation rule (substep-4 AC note)
explicitly forbids the latter.

## Setup

### Premises (A_min)

| ID | Statement | Class |
|---|---|---|
| A1ax | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2ax | Z³ spatial substrate | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| Tr-canon | Canonical Killing-Hilbert-Schmidt trace form | retained per `G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md` |
| BlockT3 | hw=1 BZ-corner triplet has M_3(C) algebra | retained per `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` |
| NQ | M_3(C) on hw=1 has no proper exact quotient | retained per `THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md` |
| R1+R2 | Circulant Hermitian form on C_3 orbit + Brannen-Rivero eigenvalue spectrum | retained per `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` (sections 1.R1, 1.R2) |
| RP | A11 RP + OS reconstruction → unique vacuum | retained per `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` |
| CD | Cluster decomposition | retained per `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md` |
| AC_φλ | "3 mass eigenstates of framework circulant ARE the 3 SM generations" | residual per `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md` |
| HR1.6 | Brannen-Rivero implicit usage already in framework | confirmed per `A3_R1_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r1hr.md` (HR1.6 attack vector) |

### Forbidden imports

- NO PDG observed values in derivation (only as falsifiability anchor)
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms

## Theorem (bounded obstruction)

**Theorem.** Under the retained primitive stack (A1ax + A2ax + Tr-canon +
BlockT3 + NQ + R1+R2 + RP + CD), the Option C closure chain for AC_φλ is
**bounded** by FIVE named admissions:

```
admit_1: substrate-semantic physical-lattice reading
admit_2: A1 (√2 equipartition)
admit_3: P1 (√m identification)
admit_4: δ rad-unit bridge (2/dim_R(M_3(C)_Herm) = 2/9 → radians)
admit_5: v_0 scale (= (Σ √m_k)/3, derivation incomplete)
```

Specifically:

(a) **R1+R2 retained:** the C_3-equivariant Hermitian operators on hw=1
    form the circulant family `H = a·I + b·C + b̄·C²` with eigenvalues
    `λ_k = a + 2|b| cos(arg(b) + 2πk/3)` for k = 0, 1, 2, in the Fourier
    basis. This is axiom-clean retained per
    `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`.

(b) **AC_φλ residual unaffected by basis choice:** identifying the three
    SM generations with the three Fourier-basis eigenstates (instead of
    corner-basis states) does NOT eliminate the identification step that
    AC_φλ asks for. It relocates the identification — from "framework's
    3-fold structure ↔ SM generations" to "framework's 3 Fourier-basis
    eigenstates ↔ SM generations" — but the structural-level identification
    bridge remains. The latter still crosses into PDG-empirical territory.

(c) **Empirical match cannot serve as derivation:** per
    `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`
    Step 6, "AC_φλ is specifically the point at which framework derivation
    must cross into PDG-empirical territory, and the framework's retained-
    grade rule forbids using PDG data in a positive theorem proof. This
    is structural, not a small bookkeeping issue."

(d) **Substrate-semantic physical-lattice reading is OPEN:** per the
    2026-05-02 narrowing of `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, the
    physical-species semantics on the hw=1 triplet is delegated to
    OPEN sibling notes (`SINGLE_AXIOM_HILBERT_NOTE.md`,
    `SINGLE_AXIOM_INFORMATION_NOTE.md`).

(e) **A1 + P1 + δ + v_0 are non-retained:** per
    `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` Appendix A.5
    "Updated status summary," all four are explicitly marked as non-
    retained at varying levels of in-flight progress.

**Therefore** Option C does NOT close AC_φλ under retained content alone.

**Proof.** Steps (a)–(e) verified by the runner. ∎

## Sharpening achieved

What Option C DOES achieve, even though it does not close AC_φλ:

1. **Confirms** the Brannen-Rivero structure is the framework's cleanest
   candidate route, already implicit per HR1.6 of the R1 hostile review.

2. **Sharpens** AC_φλ's residual content from "physical-species
   identification" (one opaque clause per substep-4 narrowing) to a
   numbered list of 5 concrete research targets:
   - admit_1: close `SINGLE_AXIOM_HILBERT_NOTE.md` and
     `SINGLE_AXIOM_INFORMATION_NOTE.md` to retained-grade.
   - admit_2: derive A1 from a charged-lepton-specific selection
     principle (real-irrep-block-democracy candidate per
     `HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`).
   - admit_3: construct positive parent operator M whose principal square
     root is the circulant amplitude operator + readout primitive escape
     from `U_e = I_3` axis-diagonal.
   - admit_4: derive canonical rad-unit bridge for the dimensional ratio
     `2/dim_R(M_3(C)_Herm) = 2/9`.
   - admit_5: derive non-double-counted lepton-sector scale selector for
     `v_0`.

3. **Provides extraordinary numerical anchor:** at δ = 2/9, A1 + P1, the
   formula matches PDG charged-lepton masses to < 0.003% per generation
   and Koide Q to 6 × 10⁻⁶. This is among the strongest empirical
   matches in the entire framework.

4. **Validates structural ingredients:** the precision of the empirical
   match strongly suggests R1+R2+A1+P1 capture real physics. Future
   retained-grade upgrades to A1 and P1 would close the chain
   immediately.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| R1+R2 retention | A C_3-symmetric Hermitian operator on hw=1 that is NOT circulant. Verified by runner: 8 generic test operators, all confirmed circulant. |
| A1 √2 equipartition matches charged leptons specifically | √m_τ / v_0_lep > 1 + √2. Verified by runner: ratio = 2.379 < 2.414 (98.5% of envelope). |
| Brannen-Rivero match to PDG | Predicted √m_k differs from observed by > 0.01% relative. Verified by runner: max relative residual = 0.003%. |
| Q = 2/3 from circulant + A1 | Computed Q ≠ 2/3. Verified by runner: Q = 6/9 exactly under A1, observed Q matches to 6 × 10⁻⁶. |

## Status

```yaml
actual_current_surface_status: bounded_obstruction
proposed_claim_type: bounded_obstruction
audit_review_points: |
  Conditional on:
   (a) the 5 named admissions being recognized as the actual non-retained
       inputs to Option C closure;
   (b) R1+R2 retention per KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE
       being recognized as already-retained framework content;
   (c) the substep-4 AC_φλ residual being recognized as relocated, not
       eliminated, by Fourier-basis re-identification;
   (d) the empirical match (< 0.003% per generation, Q to 6e-6) being
       recognized as a numerical anchor but not a retained-tier derivation.
hypothetical_axiom_status: null
admitted_observation_status: |
  Five named admissions for full closure: substrate-semantic
  physical-lattice (substep-1), A1 √2-equipartition (substep-2),
  P1 √m-identification (substep-3), δ rad-unit bridge (substep-4),
  v_0 scale (substep-5). All five flagged as non-retained in the
  upstream Koide circulant character derivation note.
admitted_context_inputs:
  - substrate_semantic_physical_lattice
  - A1_sqrt2_equipartition
  - P1_sqrtm_identification
  - delta_rad_unit_bridge
  - v_0_scale_derivation
claim_type_reason: |
  This note proves a bounded-obstruction. Option C is the cleanest
  candidate route to closing AC_φλ but does not achieve closure
  under retained content alone. The R1+R2 sub-claim is retained
  (genuine progress vs Routes 1-5 obstructions); the residual AC_φλ
  identification is sharpened from one opaque clause to five
  concrete research targets; empirical match is < 0.003% per
  generation. The lane is BOUNDED by the five admissions.
independent_audit_required_before_any_effective_status_change: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | This note BOUNDS the Option C closure path with 5 named admissions. The structural sub-claim R1+R2 retention is genuine progress vs Routes 1-5. |
| V2 | New derivation? | Sharpening of AC_φλ residual into 5 concrete research targets; explicit basis-relocation argument (Fourier vs corner does not eliminate identification step); structural compatibility analysis between R1 hostile review HR1.6 and substep-4 AC narrowing. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the 5 admissions as the load-bearing non-retained inputs; (ii) R1+R2 retention via KOIDE_CIRCULANT_CHARACTER_DERIVATION; (iii) the substep-4 AC residual being relocated not eliminated; (iv) empirical match precision. |
| V4 | Marginal content non-trivial? | Yes — explicit 5-admission decomposition of the residual; Fourier-vs-corner basis-relocation argument; R1+R2 retention check; quantitative empirical match table; falsifiability predictions for each admission. |
| V5 | One-step variant? | No — this note is structurally distinct from R1, the substep-4 AC narrowing, and the Koide circulant derivation note. It synthesizes all three into a unified Option C bounded-obstruction analysis. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule is to
avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of any existing note. It synthesizes (R1 hostile review
  HR1.6) + (substep-4 AC narrowing) + (Koide circulant character derivation)
  + (physical-lattice narrowing) into a unified Option C analysis.
- Provides explicit 5-admission decomposition; previous notes left the
  residual either as "AC_φλ" opaque clause (substep-4) or as 4 open items
  (Koide circulant note Appendix A.6).
- Provides explicit Fourier-vs-corner basis-relocation argument, which
  is not in any of the cited upstream notes.
- Provides quantitative empirical-match table verified by paired runner.

## What this note does NOT close

- Does NOT close AC_φλ.
- Does NOT close A3 (since A3 ≡ AC_φλ closure under MINIMAL_AXIOMS_2026-05-03
  framing).
- Does NOT reduce the bridge gap admission count to 0.
- Does NOT promote substrate-semantic physical-lattice to retained.
- Does NOT promote A1, P1, δ-unit-bridge, or v_0 to retained.

## Cross-references

- Parent admission identifier: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- R1 hostile review (HR1.6 Brannen-Rivero implicit usage): [`A3_R1_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r1hr.md`](A3_R1_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r1hr.md)
- Brannen-Rivero retained chain: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Physical-lattice narrowing: [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- Physical-lattice dep declaration audit: [`PHYSICAL_LATTICE_NECESSITY_DEP_DECLARATION_AUDIT_NOTE_2026-05-02.md`](PHYSICAL_LATTICE_NECESSITY_DEP_DECLARATION_AUDIT_NOTE_2026-05-02.md)
- Koide-Brannen phase reduction: [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
- Koide-Brannen Callan-Harvey candidate: [`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`](KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md)
- Koide-Brannen geometry/Dirac support: [`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`](KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Z2 hw=1 mass matrix parametrization: [`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)
- YT Class 6 (no C_3-breaking operator): [`YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`](YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- No-proper-quotient: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)

## Command

```bash
python3 scripts/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.py
```

Expected output: structural verification of (i) R1+R2 retention as already
implicit; (ii) Fourier-basis basis-relocation argument; (iii) 5-admission
decomposition; (iv) PDG empirical match precision; (v) falsifiability
predictions for each admission.

Cached: [`logs/runner-cache/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.txt`](../logs/runner-cache/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note honestly
  classifies the empirical match as numerical anchor, NOT derivation.
  AC_φλ closure under PDG-import is forbidden per substep-4 narrowing.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  user's hypothesis at the action-level: does Fourier-basis re-identification
  ELIMINATE the identification step, or merely RELOCATE it? Finding:
  relocates, does not eliminate.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. Audit lane sets effective_status. The 5 admissions
  must each go through their own retention path.
- `feedback_physics_loop_corollary_churn.md`: this is NOT a one-step variant.
  It is a synthesis of 4 distinct upstream notes (R1 hostile review, substep-4
  AC narrowing, Koide circulant character derivation, physical-lattice
  narrowing) into a unified Option C analysis with explicit 5-admission
  decomposition.
- `feedback_review_loop_source_only_policy.md`: review-loop deliverables
  packaged as 1-theorem-note + 1-runner + 1-cache. Working analysis lives
  in `outputs/action_first_principles_2026_05_08/option_c_brannen_rivero_physical_lattice/`,
  not in `docs/` or `scripts/`.
- `feedback_compute_speed_not_human_timelines.md`: each admission's closure
  path is characterized in terms of WHAT additional content would be needed,
  not human-timeline estimates.
