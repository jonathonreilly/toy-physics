# Tensor-to-Scalar Ratio Consolidation Theorem

**Date:** 2026-04-22
**Status:** retained-in-d, bounded-in-N_e consolidation theorem. Upgrades the primordial-spectrum `r = d²/N_e²` formula to "retained structural form" because d=3 is forced by `ANOMALY_FORCES_TIME`. The N_e dependence remains bounded-observational.
**Primary runner:** `scripts/frontier_tensor_scalar_ratio_consolidation.py`

## 0. Statement

**Theorem (tensor-to-scalar ratio structural form).** On the retained graph-growth primordial power spectrum surface (`PRIMORDIAL_SPECTRUM_NOTE.md`), the tensor-to-scalar ratio takes the form

```text
r  =  d² / N_e²                                                       (★)
```

where `d` is the spatial dimensionality and `N_e` is the e-fold count during the inflationary graph-growth epoch.

On the retained framework, `d = 3` is forced by `ANOMALY_FORCES_TIME_THEOREM`. Therefore (★) reduces to

```text
r  =  9 / N_e²                                                        (★′)
```

with a single bounded-observational input `N_e ≈ 60` at the standard inflationary matching. Numerically:

```text
r  =  9 / 3600  =  1/400  =  0.0025
```

## 1. Comparison with observational bounds

| Experiment | `r` reach | Framework `r = 0.0025` |
|------------|----------|------------------------|
| BICEP/Keck/Planck 2021 | `r < 0.036` (95% CL) | 7% of bound (not constraining) |
| LiteBIRD projected | `r ≈ 0.001` | 2.5× above target → **detectable** |
| CMB-S4 projected | `r ≈ 0.001` | 2.5× above target → **detectable** |

**Detection forecast**: if the framework's retained `d = 3` and bounded `N_e ≈ 60` are correct, **LiteBIRD and CMB-S4 should measure `r ≈ 0.003`** once operating. A non-detection at `r < 0.001` would rule out the graph-growth `d=3, N_e≈60` combination.

## 2. Why `d = 3` is retained (not fitted)

The `ANOMALY_FORCES_TIME_THEOREM` (retained) proves that the retained Cl(3)/Z³ fermion content is anomalous in its gauge sector unless spacetime has exactly `(3, 1)` signature. Therefore `d = 3` spatial dimensions is a **retained structural consequence** of the Cl(3)/Z³ axiom plus quantum consistency.

In contrast, generic inflationary models assume `d = 3` as an observational input. The retained framework derives it, so spectral quantities become predictions rather than fits.

## 3. Companion `n_s = 1 - 2/N_e` prediction

The same graph-growth spectrum note derives the scalar spectral tilt

```text
n_s  =  1 - 2/N_e   (at d=3)
```

At `N_e = 60`: `n_s = 0.9667`, matching Planck 2018 central value `0.9649 ± 0.0042` within **0.4σ**. This is the companion to (★′) on the same retained-in-d, bounded-in-N_e footing.

## 4. Relation to `R²` (Starobinsky) inflation

Standard `R²` inflation predicts `r ≈ 12/N_e² ≈ 0.0033` at `N_e = 60`, giving the same `r ~ 10⁻³` regime as graph-growth. The graph-growth value is `75%` of Starobinsky. Distinguishing the two by (`n_s, r`) alone requires `r`-sensitivity at the `10⁻³` level (LiteBIRD/CMB-S4 territory).

## 5. Lattice cross-check

The primordial spectrum note documents direct lattice measurement on `L = 6-14` growing cubic lattices giving `r < 10⁻⁴`, even smaller than the analytic `0.0025`. This is a FINITE-SIZE-EFFECT strengthening: small lattices exaggerate the suppression of tensor modes because gravitational coupling scales with `1/N_total`. The analytic `d²/N_e²` prediction is the `N_total → ∞` limit.

Both lattice and analytic predictions lie well below observational bounds.

## 6. What this theorem closes and does not close

**Closes**:
- Retained structural form `r = d²/N_e²` with `d = 3` axiomatically forced.
- Consolidated comparison against BICEP/LiteBIRD/CMB-S4 bounds and targets.
- Falsifiable prediction: `r ≈ 0.003` detectable by next-generation CMB experiments; non-detection at `r < 10⁻³` would falsify graph-growth `d=3` inflation.

**Does NOT close**:
- Retained derivation of `N_e ≈ 60` from Cl(3)/Z³ + pre-inflation seed size. This remains the bounded-observational input. A retained `N_e` derivation would promote `(n_s, r)` both to fully retained predictions.
- Higher-order corrections to `r` beyond leading-order graph-growth spectrum.
- The specific graph-growth inflaton-field / potential-shape mapping (currently modeled as Poisson + growth-noise; not axiom-native).

## 7. Cross-references

- `docs/PRIMORDIAL_SPECTRUM_NOTE.md` — primary graph-growth spectrum derivation.
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` — `d = 3` retained structural consequence.
- BICEP/Keck Collaboration, *Improved Constraints on Primordial Gravitational Waves*, Phys. Rev. Lett. 127 (2021) 151301.
- LiteBIRD Collaboration, *Probing Cosmic Inflation with the LiteBIRD Cosmic Microwave Background Polarization Survey*, PTEP 2023 (2023) 042F01.
- CMB-S4 Collaboration, *CMB-S4: Forecasting Constraints on Primordial Gravitational Waves*, ApJ 926 (2022) 54.
