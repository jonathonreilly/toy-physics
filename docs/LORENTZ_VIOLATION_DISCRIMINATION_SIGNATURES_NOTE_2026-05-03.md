# Lorentz Violation — Discrimination Signatures + Falsification Map

**Date:** 2026-05-03
**Type:** discrimination-test sharpening note
**Claim scope:** sharpen the framework's Lorentz-violation prediction
(already in [`LORENTZ_VIOLATION_DERIVED_NOTE.md`](LORENTZ_VIOLATION_DERIVED_NOTE.md))
into specific experimental discrimination scenarios + explicit
falsification map. NOT a re-derivation; the LV prediction is already
documented with experimental-status table.
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_lorentz_violation_discrimination_signatures.py`

## 0. Why this note

The framework's `LORENTZ_VIOLATION_DERIVED_NOTE.md` already states the
prediction (cubic harmonic K_4 with c_44/c_40 = √(5/14), quadratic E/E_Pl
suppression, CPT exact). That note also tabulates the prediction vs
current bounds (SAFE by ≥7 orders of magnitude on all current
experiments).

This note **sharpens the discrimination map**: under what experimental
scenarios is the framework FALSIFIED, SUPPORTED, DISFAVORED, or
UNCONSTRAINED? Maps to specific near-future experiments.

## 1. The four sharp framework predictions

| # | Prediction | Distinct from |
|---|---|---|
| L1 | NO linear E/E_Pl LV (only quadratic) | Loop quantum gravity (LQG), some DSR variants |
| L2 | NO CPT-odd LV (CPT exact at lattice level) | generic Planck-scale models, some spacetime foam |
| L3 | Cubic harmonic K_4 angular signature with c_44/c_40 = √(5/14) | LQG (isotropic), DSR (isotropic), spacetime foam (stochastic), generic SO(3,1) breaking patterns |
| L4 | Quadratic E/E_Pl with prefactor 1/12 (lattice-spacing-derived) | other lattice models with different a |

## 2. Discrimination scenarios

### Scenario A: linear E/E_Pl LV detected at any level
**Framework status:** **FALSIFIED** (L1 violated)
**Likely interpretation:** Loop quantum gravity, dimension-5 SME operator
**Best experiments:** GRB time-of-flight (Fermi-LAT, MAGIC, HESS); CTA upcoming

### Scenario B: CPT-odd LV detected (e.g., neutron-spin asymmetry, kaon mass difference)
**Framework status:** **FALSIFIED** (L2 violated)
**Likely interpretation:** SME with CPT-odd coefficients (a_μ, b_μ, e_μ, f_μ, g_λμν)
**Best experiments:** Hughes-Drever experiments, atomic clock comparisons, neutron EDM as CPT probe

### Scenario C: Quadratic LV with K_4 angular signature detected
**Framework status:** **STRONGLY SUPPORTED** (smoking gun)
**Best experiments:** vacuum birefringence in GRBs (high-energy polarization), UHECR angular distribution (Pierre Auger / TA), CTA large-statistics gamma observations
**Required precision:** signal at ~10⁻³² GeV⁻² for direct detection; the angular signature can be tested at much higher signal levels (would distinguish from isotropic quadratic LV)

### Scenario D: Quadratic LV with isotropic (non-K_4) angular signature
**Framework status:** **DISFAVORED but not falsified** (alternative quadratic source)
**Likely interpretation:** continuum quantum gravity, isotropic Planck-scale model
**Best experiments:** CTA + statistical isotropy tests on UHECR angular distribution

### Scenario E: No LV detected at any level (current state)
**Framework status:** **CONSISTENT** (predicted signal is ~10⁻³⁹ GeV⁻², far below current ~10⁻²² GeV⁻² bounds)
**Note:** consistent with most Planck-scale LV models too; not currently discriminating

## 3. Falsification thresholds

| Test | Current bound | Framework prediction | Falsification trigger |
|---|---|---|---|
| Photon dispersion (GRB time delay) | linear: ~10⁻¹⁵ s/GeV; quadratic: ~10⁻²² GeV⁻² | linear: 0; quadratic: 5.6 × 10⁻⁴⁰ GeV⁻² | linear LV at any precision-level above 0 |
| Vacuum birefringence (polarization rotation) | ~10⁻³² GeV⁻² | 5.6 × 10⁻⁴⁰ GeV⁻² | quadratic LV without K_4 signature at >10⁻³² level |
| CPT-odd coefficients (Hughes-Drever, neutron spin) | ~10⁻²⁷ to 10⁻³¹ GeV | exactly 0 | any CPT-odd LV detected at any precision |
| UHECR angular distribution (Pierre Auger) | order 10% deviations from isotropy | K_4 signature with factor-3 anisotropy (axis vs body diagonal) | non-K_4 angular signature at >5σ |
| CMB statistical isotropy | Planck constraints on directional asymmetry | K_4 signature in statistical anisotropy of low-l multipoles | well-motivated non-K_4 anisotropy |

## 4. Best near-future experiments

| Experiment | Timeline | Relevant claim | Discrimination potential |
|---|---|---|---|
| **CTA** (Cherenkov Telescope Array) | operational ~2026-2030 | photon dispersion at TeV; AGN/GRB monitoring | ~10× current Fermi-LAT bound; can test linear LV; angular discrimination if signal found |
| **Pierre Auger upgrade** (AugerPrime) | now-2030 | UHECR mass-composition + angular | tests K_4 cubic harmonic via composition-resolved anisotropy |
| **CMB-S4** (proposed 2030+) | proposed | CMB statistical isotropy | constraints on K_4 in low-l multipoles |
| **AION-100 / MAGIS** (atomic interferometry) | 2030+ | high-precision atomic clocks | improved CPT-odd bounds |
| **n2EDM at PSI** (related, see block 03) | 2027+ | neutron EDM | CPT bounds via T-violating moment |

## 5. Honest precision assessment

The framework's quantitative LV signal (~10⁻³⁹ GeV⁻²) is **completely beyond** any near-future direct detection. Even CTA at ~10× Fermi-LAT precision pushes to ~10⁻²³ GeV⁻², still 16 orders above the predicted signal.

**Therefore:** the framework cannot be DIRECTLY DETECTED in this lane in the foreseeable future via signal magnitude.

**However:** the framework CAN be FALSIFIED if any of the following are observed at any level:
- (L1 violation) linear E/E_Pl LV
- (L2 violation) CPT-odd LV
- (L3 violation) Quadratic LV with non-K_4 angular signature

These are **easier to detect** than the framework's predicted signal because they would manifest at higher levels in models that allow them.

## 6. New-physics discrimination value

**Distinguishing power vs SM:** very high (SM has exact Lorentz; framework breaks to O_h)

**Distinguishing power vs other BSM (LQG, DSR, spacetime foam, SME):** very high
- Specific angular signature (K_4 with c_44/c_40 = √(5/14))
- Specific suppression order (quadratic, not linear)
- Specific CPT structure (all CPT-odd vanish)

**Caveat:** very small predicted signal magnitude limits direct testability. Best discrimination is via FALSIFICATION (looking for what the framework FORBIDS rather than confirming what it predicts).

## 7. Honest status

```yaml
actual_current_surface_status: discrimination-test sharpening note
target_claim_type: positive_theorem (framework's LV prediction already retained-bounded);
  open_gate (direct experimental discrimination)
proposal_allowed: false
proposal_allowed_reason: |
  Sharpening note. The underlying LV prediction is already documented in
  LORENTZ_VIOLATION_DERIVED_NOTE.md (bounded tier). This note adds
  discrimination scenarios + falsification map.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 8. What this note closes

- Maps the framework's LV prediction to **5 specific experimental scenarios**
- Identifies **falsification triggers**: linear LV, CPT-odd LV, non-K_4 quadratic LV
- Identifies **best near-future experiments** with timeline (CTA, AugerPrime, CMB-S4, AION/MAGIS, n2EDM)
- **Honest assessment**: direct detection beyond reach (~16 orders); falsification via forbidden signatures is achievable

## 9. What this note does NOT close

- Direct detection of the framework's predicted ~10⁻³⁹ GeV⁻² signal (beyond reach)
- The retained-tier upgrade of LV prediction (still bounded; not retained)

## 10. Cross-references

- Underlying LV prediction: [`LORENTZ_VIOLATION_DERIVED_NOTE.md`](LORENTZ_VIOLATION_DERIVED_NOTE.md)
- Standard SME framework: Kostelecky et al, sme-data tables (annually updated)
- Loop quantum gravity LV: Amelino-Camelia 2013 (Living Rev. Relativ.)
- Vacuum birefringence: Gleiser-Kozameh 2001; Stecker 2011
- CTA project: cta-observatory.org
- Pierre Auger: auger.org
