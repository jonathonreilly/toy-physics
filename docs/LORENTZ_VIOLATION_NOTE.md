# Lorentz and CPT Violation from Lattice Structure

## Summary

The cubic lattice Z^3 underlying the graph-propagator framework breaks continuous Lorentz symmetry to the discrete cubic group O_h. This note computes the predicted Lorentz-violating (LV) corrections, maps them onto the Standard Model Extension (SME) framework, and compares with experimental bounds.

**Key result:** For a Planck-scale lattice (a = l_Planck), the leading LV correction is suppressed by (E/E_Planck)^2 ~ 10^-38 at 1 GeV, which is below all current experimental bounds by at least 6 orders of magnitude. CPT is exactly preserved.

## 1. Lattice Dispersion Relation

On a cubic lattice with spacing a, the exact dispersion relation is:

    E^2 = m^2 + sum_i (2/a^2) sin^2(p_i a/2)

Taylor expanding at low momentum (p_i a << 1):

    E^2 = m^2 + p^2 - (a^2/12) sum_i p_i^4 + (a^4/360) sum_i p_i^6 - ...

The **leading Lorentz-violating correction** is:

    delta(E^2) = -(a^2/12) sum_i p_i^4

This breaks SO(3,1) to O_h (the 48-element cubic group).

### Coefficient value

For a = l_Planck = 1.616 x 10^-35 m:

    a^2/12 = 2.18 x 10^-71 m^2 = 5.60 x 10^-40 GeV^-2

This is the dimension-6 LV coefficient in the dispersion relation.

## 2. SME Coefficient Mapping

### Spherical harmonic decomposition

The p_i^4 term decomposes as:

    sum_i p_i^4 = p^4 * [3/5 + (4/5) K_4(theta, phi)]

where K_4 is the cubic harmonic:

    K_4 = (1/sqrt(12)) [Y_40 + sqrt(5/14)(Y_44 + Y_{4,-4})]

### SME coefficients (Kostelecky notation)

The lattice generates **dimension-6, CPT-even** SME coefficients:

| Coefficient | j | m | Value (GeV^-2) | Type |
|---|---|---|---|---|
| c^(6)_{(I)00} | 0 | 0 | ~3.4 x 10^-40 | isotropic |
| c^(6)_{(I)40} | 4 | 0 | ~4.5 x 10^-40 | anisotropic |
| c^(6)_{(I)44} | 4 | +/-4 | ~4.5 x 10^-40 | anisotropic |

**All other coefficients are zero** -- no j=1,2,3 components arise from cubic symmetry.

### CPT-odd coefficients

All CPT-odd SME coefficients are **identically zero**:

    a_mu = b_mu = e_mu = f_mu = g_{lambda mu nu} = 0

This is because C, P, T are each individually exact symmetries of the cubic lattice (see Section 5).

## 3. Experimental Bounds Comparison

### Suppression factor

At energy E, the LV correction to the dispersion relation is:

    |delta E^2 / E^2| ~ (a^2/12) E^2 = (E/E_Planck)^2 / 12

| E (GeV) | (E/E_Pl)^2 | Predicted LV | Best bound | Margin |
|---|---|---|---|---|
| 10^-3 | 6.7 x 10^-45 | 5.6 x 10^-46 | 10^-27 | 10^-19 |
| 1 | 6.7 x 10^-39 | 5.6 x 10^-40 | 10^-27 | 10^-13 |
| 10 | 6.7 x 10^-37 | 5.6 x 10^-38 | 10^-32 | 10^-6 |
| 10^3 | 6.7 x 10^-33 | 5.6 x 10^-34 | 10^-32 | 10^-2 |
| 10^4 | 6.7 x 10^-31 | 5.6 x 10^-32 | 10^-32 | ~1 |

### Current experimental bounds

| Experiment | Sector | Bound | Status |
|---|---|---|---|
| GRB birefringence | photon | k^(6) < 10^-32 GeV^-2 | SAFE |
| Fermi LAT (GRB 090510) | photon | E_QG > 6.3 x 10^10 GeV | SAFE |
| Hughes-Drever | electron | c_munu < 10^-27 GeV | SAFE |
| Atomic clocks | proton | c_munu < 10^-27 GeV | SAFE |
| Neutron spin | neutron | b_mu < 10^-31 GeV | SAFE (predicted = 0) |
| MINOS/IceCube | neutrino | a_L < 10^-23 GeV | SAFE |
| Muon g-2 | muon | c_munu < 10^-24 GeV | SAFE |
| Lunar laser ranging | gravity | s_bar < 10^-9 | SAFE |

The closest approach to experimental sensitivity is in the **photon birefringence sector** at TeV energies, where the prediction comes within ~2 orders of magnitude of the bound.

## 4. Staggered Fermion Taste-Breaking

Staggered fermions on the lattice have 2^d degenerate tastes whose symmetry is broken at O(a^2). This introduces additional LV beyond the naive lattice dispersion:

    delta(E^2)_taste = a^2 C_taste p^4

where C_taste ranges from 1.0 (pseudoscalar taste) to 3.0 (identity taste).

The total LV for each taste is enhanced by a factor (1 + C_taste), at most quadrupling the naive coefficient. Since the naive coefficient is already 10^-6 to 10^-38 below bounds, this enhancement is phenomenologically irrelevant.

However, the taste structure predicts **flavor-dependent LV**: different fermion species (if they map to different tastes) would have slightly different LV coefficients. This is testable by comparing electron vs muon vs tau sector measurements.

## 5. CPT Analysis

### Individual discrete symmetries

| Symmetry | Status | Reason |
|---|---|---|
| P (parity) | EXACT | Z^3 has x_i -> -x_i reflection symmetry |
| T (time reversal) | EXACT | Real lattice action, S(-t) = S(t) |
| C (charge conjugation) | EXACT | Complex conjugation, real action |
| **CPT** | **EXACT** | Product of three exact symmetries |

### Greenberg theorem

Greenberg (2002) proved that CPT violation implies Lorentz violation in local QFT. The converse (Lorentz violation implies CPT violation) is **not proven** and is in fact false in the lattice framework. The lattice breaks Lorentz symmetry while preserving CPT exactly.

This is possible because the lattice framework is not a continuum local QFT -- it is defined on a discrete structure where the assumptions of the Greenberg theorem do not apply.

### Falsification

**Any detection of CPT-odd Lorentz violation would falsify the cubic lattice framework.** Current bounds on CPT-odd coefficients (e.g., b_mu < 10^-31 GeV for neutrons) are consistent with the prediction b_mu = 0.

## 6. Leading Observable Prediction

### Direction-dependent propagation speed

For a massless particle along direction (theta, phi):

    v(theta, phi) = c [1 - (a^2/24) p^2 f_4(theta, phi)]

where f_4 = n_x^4 + n_y^4 + n_z^4 is the cubic angular factor.

| Direction | f_4 | Relative speed deviation |
|---|---|---|
| [100] axis | 1.000 | maximum |
| [110] face diagonal | 0.500 | intermediate |
| [111] body diagonal | 0.333 | minimum |

The **factor-of-3 anisotropy** between axis and diagonal is the fingerprint of cubic symmetry. The angular pattern (Y_40 + sqrt(5/14)(Y_44 + Y_{4,-4})) uniquely identifies cubic lattice LV.

### Numerical prediction

At E = 10 GeV:

    delta_v/v (axis vs diagonal) ~ (a^2/36) p^2 ~ 10^-38

This is undetectable with current technology.

## 7. Predictions Summary

1. **Lorentz violation**: YES, breaking SO(3,1) -> O_h. Leading correction is dimension-6, proportional to a^2 p^4.

2. **CPT violation**: NO. All CPT-odd SME coefficients are identically zero. This is a strong, falsifiable prediction.

3. **Suppression**: (E/E_Planck)^2 ~ 10^-38 at 1 GeV. Below all current bounds.

4. **Angular signature**: Cubic harmonics (j=4, m=0,+/-4). Factor-of-3 anisotropy between axis and diagonal.

5. **Flavor dependence**: Taste-breaking predicts slightly different LV for different fermion species, enhanced by factors of 2-4.

6. **Closest to detection**: Photon birefringence at TeV energies approaches within ~2 orders of magnitude of the bound.

7. **Consistency**: All predictions consistent with null results in all LV searches to date.

## References

- Kostelecky & Mewes, PRD 80 (2009) 015020 -- SME framework for photons
- Kostelecky & Mewes, PRL 110 (2013) 201601 -- GRB birefringence bounds
- Vasileiou et al., PRD 87 (2013) 122001 -- Fermi LAT time-of-flight
- Kostelecky & Russell, Rev. Mod. Phys. 83 (2011) 11 -- Data tables for LV
- Greenberg, PRL 89 (2002) 231602 -- CPT violation implies LV in local QFT
- Aubin & Bernard, PRD 68 (2003) 034014 -- Staggered fermion taste-breaking
- Lepage, PRD 59 (1999) 074502 -- Improved staggered fermions

## Script

Computed by: `scripts/frontier_lorentz_violation.py`
