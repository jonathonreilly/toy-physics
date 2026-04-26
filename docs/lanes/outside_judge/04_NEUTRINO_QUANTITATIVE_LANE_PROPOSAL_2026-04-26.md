# Lane 4 — Neutrino Quantitative Closure

**Date:** 2026-04-26
**Status:** ACCEPTED PLANNING LANE on `main`; no theorem or claim promotion
**Lethality (external):** HIGH. Most experimentally-active sector. Current
experimental program (KATRIN, JUNO, DUNE, Hyper-K) is targeting these.
**Approachability:** Tier B-C (3–9 months for full closure)

## 1. Outside-judge framing

A neutrino physicist or cosmologist evaluating the framework asks:

- "What is the absolute mass of the lightest neutrino?"
- "Δm²_21 (solar) and Δm²_31 (atmospheric) — what does the framework predict?"
- "Are neutrinos Dirac or Majorana? If Majorana, what are α_21, α_31?"
- "Why is m_ν so small? Where does the seesaw scale come from?"

The framework currently has the neutrino sector labeled as "different carriers"
in the [CHARGED_LEPTON_KOIDE_REVIEW_PACKET](../../CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md)
— meaning the neutrino mass-spectrum questions live on a separate carrier than
the charged-lepton Koide structure. The DM closed package gives δ_CP ≈ -81° and
θ_23 upper octant, but absolute mass scales and Δm² values are bounded
companion at best.

**External judges treat the neutrino sector as the most experimentally testable
near-term lane.** Not closing it means leaving the most active experimental
front open.

## 2. Current state of repo content

### Retained

- δ_CP ≈ -81° (DM closed package, falsifiable at DUNE/Hyper-K)
- θ_23 ≥ 0.5410 upper octant (DM closed package, falsifiable)
- Exact PMNS selector / current-stack zero law (neutrino retained boundary
  packet)
- Exact Majorana zero law on current stack (suggests Dirac lane)
- Anomaly-forced 3+1 + three-generation structure
- N_eff support from three generations (recent)

### Bounded

- Seesaw mass scale (Phase 4 of mass-spectrum derived note — retained partial)
- Solar/PMNS bounded support
- Neutrino retained observable bounds (recent landing 2026-04-24)

### Absent ("different carriers")

- Absolute neutrino mass m_lightest
- Δm²_21 (solar mass-squared difference)
- Δm²_31 (atmospheric mass-squared difference)
- Majorana phases α_21, α_31 (if Majorana)
- Confirmation of Dirac vs Majorana globally
- Quantitative seesaw mass spectrum (not just scale)
- Cosmological constraints on neutrino masses (Σm_ν from CMB)

## 3. Derivation targets

### 4A. Absolute neutrino mass scale m_lightest

**Target:** derive m_lightest from framework structure, ideally as a function
of the retained seesaw scale + retained EW scale + retained generation
structure.

**What the framework needs:**
- The retained seesaw scale (Phase 4 partial)
- A specific neutrino-Yukawa structural identity (analog to charged-lepton
  Koide for the neutrino carrier)
- Connection to the retained Dirac lane

**Approachability:** Tier C. Substantial structural extension.

### 4B. Δm²_21 derivation

**Target:** derive the solar mass-squared difference from framework structure.

**Approachability:** Tier B-C. Likely follows from the seesaw mass spectrum
in Phase 4.

### 4C. Δm²_31 derivation

**Target:** derive the atmospheric mass-squared difference.

**Approachability:** Tier B-C. Same seesaw spectrum.

### 4D. Dirac vs Majorana global confirmation

**Target:** retain a global statement (not just current-stack) that neutrinos
are Dirac OR derive the Majorana phases if Majorana.

**Existing scaffolding:**
- Exact current-stack Majorana zero law
- Mass reduction to Dirac lane (retained)
- PMNS selector zero law

**Approachability:** Tier B. The Dirac lane is favored by retained content;
the global lift is a structural extension.

### 4E. Seesaw mass spectrum quantitative closure

**Target:** retain the quantitative right-handed neutrino mass spectrum
(M_R1, M_R2, M_R3) and connect to active neutrino masses.

**Approachability:** Tier B-C.

### 4F. Cosmological neutrino constraint Σm_ν

**Target:** derive Σm_ν consistent with retained cosmology bounded surface
(matter-radiation equality, N_eff support, neutrino retained observable
bounds).

**Approachability:** Tier B. Connects to Lane 5.

### 4G. Cross-validation with retained δ_CP and θ_23

**Target:** verify the now-retained mass spectrum is consistent with the
already-retained δ_CP ≈ -81° and θ_23 upper octant predictions.

**Approachability:** Tier A. Internal consistency check.

## 4. Existing scaffolding to build on

- [NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md](../../NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md)
- [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md)
- [MASS_SPECTRUM_DERIVED_NOTE.md](../../MASS_SPECTRUM_DERIVED_NOTE.md) — Phase 4
- [NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md](../../NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md)
- [NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md](../../NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md)
- [PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md](../../PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md)
- [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](../../N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md)
- The DM closed package (δ_CP, θ_23 forecast)
- [NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md](../../NEUTRINO_TWO_AMPLITUDE_LAST_MILE_REDUCTION_NOTE.md)

## 5. Recommended attack approach

**Phase 1:**

1. **4D: Dirac vs Majorana global confirmation.** Lift the current-stack
   zero law to a global statement. Tier B.
2. **4E: Seesaw quantitative closure.** Promote Phase 4 partial to retained
   spectrum.

**Phase 2 (after Phase 1):**

3. **4B + 4C: Δm²_21 and Δm²_31** — derive from the seesaw spectrum.
4. **4F: Σm_ν cosmological constraint** — connect to Lane 5.

**Phase 3:**

5. **4A: m_lightest absolute scale.** This is the hardest sub-target.
6. **4G: Cross-validation with δ_CP and θ_23.** Internal consistency check.

## 6. Out of scope / will not claim

- This lane does NOT propose to derive 0νββ rates in initial scope (depends
  on Majorana confirmation + nuclear matrix elements).
- This lane does NOT propose to predict neutrino oscillation amplitudes
  beyond the already-retained PMNS structure.
- This lane does NOT address sterile-neutrino searches or eV-scale anomalies
  (LSND, MiniBooNE, gallium) in initial scope.

## 7. Cross-references

- Depends on: existing neutrino retained boundary packet; DM closed package
  (for δ_CP and θ_23 cross-validation)
- Connects to: Lane 5 (cosmological Σm_ν constraint, N_eff)
- Independent of: Lane 1 (hadrons), Lane 2 (atomic-scale), Lane 3 (quarks)
  in primary closure path

## 8. Reviewer questions

1. Should this lane be split into "Dirac confirmation + seesaw spectrum" as
   one sub-lane and "absolute mass scale" as another, given the very
   different difficulty profiles?
2. Is the seesaw route the right entry point, or is there a more direct
   neutrino-Yukawa derivation analogous to charged-lepton Koide?
3. How should this lane interact with the DM closed package's δ_CP forecast?
   Is there a risk the closed package's δ_CP gets revised when the absolute
   mass spectrum is retained?
4. Should cosmological neutrino constraints (Σm_ν) be addressed here or in
   Lane 5?
