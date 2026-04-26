# Lane 5 — Hubble Constant H_0 Derivation

**Date:** 2026-04-26
**Status:** ACCEPTED PLANNING LANE on `main`; no theorem or claim promotion
**Lethality (external):** HIGH. Hubble tension is the most active cosmology
debate. Currently external input.
**Approachability:** Tier B (1–4 months — substantial recent structural-identity
landings have made this materially closer)

## 1. Outside-judge framing

A cosmologist evaluating the framework reads
[INPUTS_AND_QUALIFIERS_NOTE.md](../../publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md)
§2 and immediately flags:

> "H_0 = 67.4 km/s/Mpc is taken as external input. The framework structurally
> distinguishes H_0 from H_inf via Ω_Λ = (H_inf/H_0)², so the framework cares
> about the value of H_0. So why not derive it?"

Plus:
- "What does the framework predict about the Hubble tension (67.4 vs 73)?"
- "Where does the matter content Ω_m come from internally?"
- "Why is Ω_Λ ≈ 0.69 today specifically?"

**The current package commits exactly to ΛCDM at late times** (w = -1 retained,
Λ structural identity, no modified gravity at cosmological scales). This is a
genuine prediction — it rules out late-time tension-resolution proposals. But
it's not the same as predicting H_0 from first principles.

The framework has substantial recent structural-identity landings:
R_base = 31/9, FRW kinematic reduction, matter-radiation equality, N_eff
support, neutrino observable bounds, single-ratio inverse reconstruction
(2026-04-25). **These together are very close to closing the cosmology matter
bridge that gates the H_0 derivation.**

## 2. Current state of repo content

### Retained

- Λ = 3/R_Λ² spectral-gap structural identity
- w = -1 dark-energy EOS exactly
- m_g² = 6ℏ²/(c²R²) graviton mass structural identity
- DM relic ratio R = Ω_DM/Ω_b = 5.48 (exact group theory, 0.2% match)
- DM exact-target PMNS package CLOSED
- Λ spectral tower bridge (recent landing 2026-04-25)

### Bounded / structural identities (recent landings)

- R_base = 31/9 group-theory derivation (2026-04-24)
- FRW kinematic reduction theorem (2026-04-24)
- Matter-radiation equality structural identity (2026-04-24)
- N_eff support from three generations (2026-04-24)
- Neutrino retained observable bounds (2026-04-24)
- Cosmology single-ratio inverse reconstruction theorem (2026-04-25)

### External inputs

- T_CMB = 2.7255 K
- H_0 = 67.4 km/s/Mpc

### Absent

- H_0 derivation from framework
- Ω_m internal closure (the matter bridge)
- Hubble tension resolution stance (commit to early-time mechanism vs
  systematic vs unresolved)

## 3. Derivation targets

### 5A. Ω_m internal closure (the matter bridge)

**Target:** derive the present-day matter fraction Ω_m from framework
structure, without taking it as observational input.

**What the framework needs:**
- The retained DM relic ratio R = Ω_DM/Ω_b (already retained)
- An internal derivation of Ω_b (baryon density today)
- A structural identity connecting Ω_b to retained quantities (cosmological
  constant scale, FRW reduction, matter-radiation equality)

**Existing scaffolding:** the 5 recent structural identities (R_base, FRW,
m-r equality, N_eff, single-ratio inverse reconstruction) provide most of
the bridge content; the missing object is the closure step.

**Approachability:** Tier B. The bridge is materially shorter than 2 weeks
ago.

### 5B. H_0 derivation from internal Ω_m closure

**Target:** with Ω_m retained internally, derive H_0 via:

```
H_0² = (8πG/3) × (ρ_Λ + ρ_m + ρ_r) = H_inf² / Ω_Λ = H_inf² / (1 - Ω_m - Ω_r)
```

where Λ = 3·H_inf²/c² is retained, ρ_r is determined by T_CMB (still external)
or by retained N_eff + photon-temperature relation, and Ω_m comes from 5A.

**Approachability:** Tier A-B. Automatic chain once 5A lands.

### 5C. Hubble tension explicit stance

**Target:** retain a paper-grade statement on the framework's commitment to
ΛCDM at late times, with the implication that any genuine H_0 tension must
arise from pre-recombination physics (early dark energy, modified
recombination, extra relativistic species before CMB release) — NOT from
late-time modifications.

**Existing scaffolding:** w = -1 retained, Λ structural retained, no modified
gravity at cosmological scales. The commitment is already implicit.

**Approachability:** Tier A. This is largely a manuscript-surface clarification.

### 5D. Cosmological neutrino constraint Σm_ν integration

**Target:** integrate Σm_ν derivation from Lane 4 with the cosmology bridge
to verify H_0 prediction is consistent with retained neutrino content.

**Approachability:** Tier A-B once Lane 4 partial lands.

### 5E. Inflation mechanism (deferred to follow-on)

**Target:** retain an inflation mechanism that sources the observed CMB
anisotropy spectrum.

**Existing scaffolding:** [PRIMORDIAL_SPECTRUM_NOTE.md](../../PRIMORDIAL_SPECTRUM_NOTE.md)
bounded.

**Approachability:** Tier C. Substantial; deferred from initial closure of
this lane.

## 4. Existing scaffolding to build on

- [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
- [COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md](../../COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md)
- [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](../../R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
- [MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](../../N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md)
- [COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md](../../COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md)
- [GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md](../../GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md)
- [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
- DM closed package (R = Ω_DM/Ω_b retained)

## 5. Recommended attack approach

**Phase 1 (fast):**

1. **5C: Hubble tension explicit stance.** Manuscript-surface clarification.
   Tier A. ~1 week.

**Phase 2:**

2. **5A: Ω_m internal closure.** Connect the 5 recent structural identities
   to derive Ω_m. Tier B. The single most important step.
3. **5B: H_0 derivation from Ω_m.** Automatic chain once 5A lands. Tier A.

**Phase 3:**

4. **5D: Σm_ν integration.** After Lane 4 partial.

**Phase 4 (deferred):**

5. **5E: Inflation mechanism.** Tier C. Separate lane.

## 6. Out of scope / will not claim

- This lane does NOT propose to derive T_CMB from first principles in
  initial scope (it remains an external input for cosmology rows).
- This lane does NOT address inflation in initial scope (deferred to 5E).
- This lane does NOT propose to resolve the Hubble tension by fitting either
  end (67.4 vs 73). It commits to ΛCDM at late times structurally and lets
  the tension resolution be early-time-only.
- This lane does NOT address dark-energy detection or modified-gravity
  alternatives.

## 7. Cross-references

- Depends on: 5 recent cosmology structural identities (already retained)
- Connects to: Lane 4 (Σm_ν cosmological constraint)
- Independent of: Lanes 1, 2, 3 in primary closure path
- Predicts: an early-time-only resolution of any genuine Hubble tension

## 8. Reviewer questions

1. Is Ω_m internal closure (5A) the right entry point, or should we attempt
   H_0 derivation directly via a different route?
2. Should the Hubble tension stance (5C) be on the manuscript surface as
   a public prediction, or kept internal until 5A and 5B land?
3. Should inflation (5E) be folded into this lane or remain as a separate
   future lane?
4. What precision target should "H_0 retained" mean — sub-percent? 10%?
   Within current observational uncertainty?
