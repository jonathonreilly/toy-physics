# Strong CP + CKM Neutron EDM — New-Physics Discrimination

**Date:** 2026-05-03
**Type:** discrimination-test sharpening note
**Claim scope:** combine framework's strong-CP θ=0 prediction
([`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md)),
universal theta-EDM vanishing theorem
([`UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md`](UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md)),
and CKM-only neutron-EDM corollary
([`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md))
into a unified BSM-discrimination framework. Map to n2EDM (PSI)
2027+ sensitivity. Block 03 of `non-sm-prediction-sharpening-20260503`.
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_strong_cp_edm_new_physics_discrimination.py`

## 0. Question

The framework predicts:
- θ_eff = 0 EXACTLY on retained Wilson+staggered action surface (bounded
  conditional; STRONG_CP)
- d_n(QCD) = 0 exactly (corollary of θ_eff = 0)
- d_n(CKM) ≈ 10⁻³² to 10⁻³³ e·cm (CKM-only contribution; bounded EFT bridge)
- Universal theta-induced EDM response vanishes for ALL EDM observables

How does this discriminate from:
- (A) SM with θ as free parameter (θ < 10⁻¹⁰ from current d_n bound)
- (B) BSM with new CP sources (SUSY, multi-Higgs, axion) — typically predict
  d_n ≈ 10⁻²⁸ to 10⁻²⁵ e·cm

What does n2EDM at PSI 2027+ (target sensitivity ~10⁻²⁸ e·cm) tell us?

## 1. Framework's three sharp claims

| # | Prediction | SM | BSM (typical) |
|---|---|---|---|
| E1 | θ_eff = 0 EXACTLY (not just <10⁻¹⁰) | free param ≤ 10⁻¹⁰ | varies; often non-zero |
| E2 | d_n(QCD) = 0 EXACTLY | ≤ 10⁻²⁶ e·cm × θ/10⁻¹⁰ | typically larger if θ ≠ 0 |
| E3 | All theta-induced EDM components = 0 (universal) | individual EDMs untested at θ → 0 limit | distinct from BSM signatures |

**Combined claim:** framework predicts that the **only** source of neutron
EDM in the SM-extended sector is CKM CP, which gives `d_n ≈ 10⁻³² e·cm`
(bounded EFT estimate; not retained tier).

## 2. Comparison with experimental landscape

| Source | Predicted d_n | Detectable by n2EDM (~10⁻²⁸)? |
|---|---|---|
| Framework: CKM-only | ~10⁻³² e·cm | NO (4 orders below sensitivity) |
| SM (free θ ≤ 10⁻¹⁰) | up to ~10⁻²⁶ e·cm | YES (potentially) |
| SUSY (MSSM, generic) | ~10⁻²⁸ to 10⁻²⁵ e·cm | YES |
| Multi-Higgs | ~10⁻²⁷ e·cm | YES |
| Axion (Peccei-Quinn) | ~10⁻³² e·cm (post-PQ resolution) | NO |

**Current bound:** d_n < 1.8 × 10⁻²⁶ e·cm (PSI 2020, Abel et al)

## 3. Three discrimination scenarios from n2EDM

### Scenario E-1: n2EDM detects d_n at ~10⁻²⁸ to 10⁻²⁶ e·cm

**Framework status:** **STRONGLY DISFAVORED to FALSIFIED**
- Signal too large to be CKM-only (~10⁻³²)
- Source must be either: residual θ (framework predicts EXACTLY 0, not just small) OR new BSM CP source (framework predicts none from theta-related sectors)
- BSM scenarios (SUSY, multi-Higgs) consistent with this signal

### Scenario E-2: n2EDM sets bound d_n < 10⁻²⁸ e·cm with no detection

**Framework status:** **CONSISTENT** (predicted ~10⁻³² is well below 10⁻²⁸)
- Constrains BSM models (SUSY parameter space tightened)
- Does NOT discriminate framework from SM-axion (both consistent)
- Helps the "framework + SM-CKM-only" picture

### Scenario E-3: n2EDM detects d_n at exactly the CKM-only level (~10⁻³²)

**Framework status:** **NEUTRAL / WEAKLY SUPPORTED** (matches prediction)
- Likely beyond n2EDM precision; would require future-future generation EDM experiments (not in current planning)
- If achieved, it would CONFIRM CKM-only structure but not specifically the framework's θ=0 derivation

## 4. The "axion null test"

Critical framework prediction: **NO axion mechanism is needed** because
θ_eff is structurally zero. This contrasts with:

- **SM with θ free**: requires axion or fine-tuning to explain observed θ ≤ 10⁻¹⁰
- **BSM-with-axion**: predicts axion-photon coupling g_aγγ ~ 10⁻¹⁵ to 10⁻¹⁰ GeV⁻¹

**Discrimination:**
- Axion DETECTED (e.g., ADMX, IAXO, BabyIAXO observations) → framework's "axion not needed" loses motivation but is not strictly falsified (could still derive θ=0 as bonus to a discovered axion)
- Axion NOT detected with negative results from ADMX-EFR, IAXO at projected sensitivity → framework's "axion not needed" claim STRENGTHENED

## 5. Universal theta-EDM vanishing (E3) experimental tests

Per [`UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md`](UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md),
ALL EDM observables have zero theta-induced component. This means:

| EDM observable | Framework prediction (theta-induced) | Other contributions |
|---|---|---|
| neutron d_n | 0 | CKM-only (~10⁻³²) |
| electron d_e | 0 | SM-CKM contribution + BSM |
| 199-Hg atomic EDM | 0 | nuclear / atomic CP |
| 129-Xe atomic EDM | 0 | similarly |
| muon d_μ | 0 | weak-sector CKM contribution |

**Discrimination:** detection of EDM in MULTIPLE species at correlated levels consistent with a SINGLE θ-source would discriminate against the framework's universal vanishing claim. Detection in species at uncorrelated levels would be consistent with multiple-BSM-source picture (some other-than-θ explanation; could still be consistent with framework's θ=0).

## 6. n2EDM @ PSI 2027+ specifics

[Next-generation n2EDM experiment](https://arxiv.org/abs/2104.04514):
- Target sensitivity: σ(d_n) ≈ 10⁻²⁸ e·cm (currently 10⁻²⁶)
- Timeline: data-taking 2024-2027; results 2027-2029
- Could detect d_n at ~10⁻²⁸ if BSM source exists; would falsify framework's CKM-only-EDM claim

**Future generation (not yet funded):**
- nEDM++ proposals: target 10⁻³⁰ e·cm sensitivity
- Storage-ring EDM (proposed): target 10⁻²⁹ for proton, deuteron, muon EDMs
- These would push deeper into framework territory; CKM-only signal at ~10⁻³² is still beyond.

## 7. New-physics discrimination value

**Distinguishing power vs SM:** moderate
- Both framework and SM-CKM predict same d_n ≈ 10⁻³²
- Framework FORBIDS what SM ALLOWS (θ free param)
- SM-with-axion-resolution gives same prediction; framework distinguishes by NOT NEEDING axion

**Distinguishing power vs BSM with new CP sources:** HIGH
- BSM (SUSY, multi-Higgs) typically predict d_n ≈ 10⁻²⁸ to 10⁻²⁵
- n2EDM detection at >10⁻³⁰ would falsify framework's CKM-only claim
- n2EDM null result at ~10⁻²⁸ tightens BSM parameter space

**Connection to LV (block 02):** CPT-odd LV would falsify framework's θ=0 derivation route (since CPT-odd structure is what allows θ to escape vanishing). Block 02's L2 falsification connects to this lane.

## 8. Honest status

```yaml
actual_current_surface_status: discrimination-test sharpening note + cluster synthesis
target_claim_type: positive_theorem (E1, E2, E3 already retained-bounded);
  open_gate (BSM falsification scenarios)
proposal_allowed: false
proposal_allowed_reason: |
  Sharpening note. Underlying θ_eff=0 + universal-EDM-vanishing claims
  already documented. This note adds n2EDM discrimination scenarios.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 9. What this note closes

- Maps framework's strong-CP + universal-EDM-vanishing predictions to **3 specific n2EDM discrimination scenarios**
- Identifies n2EDM @ PSI 2027+ as primary near-term test
- Connects to block 02 (LV CPT-odd falsification)
- Identifies axion null-test discrimination

## 10. What this note does NOT close

- The retained-tier upgrade of strong-CP closure (still bounded conditional)
- Direct detection of CKM-only d_n (~10⁻³² is below all near-future sensitivity)

## 11. Cross-references

- Strong CP source: [`STRONG_CP_THETA_ZERO_NOTE.md`](STRONG_CP_THETA_ZERO_NOTE.md)
- Universal EDM vanishing: [`UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md`](UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md)
- CKM EDM bound: [`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md)
- Block 01 of this campaign (Higgs+vacuum stability): PR [#436](https://github.com/jonathonreilly/cl3-lattice-framework/pull/436)
- Block 02 of this campaign (Lorentz violation): PR [#437](https://github.com/jonathonreilly/cl3-lattice-framework/pull/437)
- n2EDM @ PSI: [arXiv:2104.04514](https://arxiv.org/abs/2104.04514)
- Current d_n bound: Abel et al 2020, Phys. Rev. Lett. 124, 081803
