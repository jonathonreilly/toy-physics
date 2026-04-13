# Electroweak VEV from Cosmological Boundary Conditions

**Status:** INVESTIGATION -- negative result for cosmological route, partial positive for CW route

**Script:** `scripts/frontier_v_from_cosmology.py`

## Question

Can v = 246 GeV be derived from the cosmological boundary conditions (T_CMB, H_0) plus the framework's Coleman-Weinberg potential, eliminating v as a separate input?

## Summary of Findings

### What works

1. **Dimensionless structure fully derived.** The framework determines all couplings at M_Pl (alpha_unif = 0.092, sin^2 theta_W = 3/8, y_t/g_s = 1/sqrt(6)) and all mass ratios (m_W/v, m_Z/v, m_t/v, m_H/v) via RGE running. Lambda_QCD/M_Pl follows from alpha_s running alone.

2. **EWSB mechanism identified.** The CW potential with taste-enhanced top loop (N_taste = 16 copies of the top Yukawa) drives mu^2 negative, triggering EWSB. Without taste enhancement, gauge contributions dominate (C_quad = -1.97) and EWSB does not occur at 1-loop. With taste: C_quad(taste) = +15.4.

3. **Hierarchy parametrically correct.** The exponential formula v ~ M_Pl * exp(-8 pi^2 / (N_taste * y_t^2)) gives the right functional form for the hierarchy. With framework couplings: exponent = 25.6 vs needed = 38.4 (ratio 0.67).

4. **Best numerical estimate:** v_pred ~ 9.2 x 10^7 GeV from the taste-enhanced exponential, which is within 5.6 orders of magnitude of v_obs = 246 GeV. The log-hierarchy is 67% of the observed value.

### What does not work

1. **Cosmological route is circular.** T_CMB and H_0 both depend on v through the mass thresholds in g_*(T). The chain T_CMB -> T_EWSB -> v requires knowing v to compute g_*(T), which determines the cooling history. Specifically:
   - T_c = v * sqrt(lambda/c) is proportional to v
   - g_*(T) between m_e and T_EWSB depends on all particle masses ~ coupling * v
   - The baryon asymmetry eta depends on the EWPT strength, which depends on v

2. **Pure CW mechanism insufficient.** The SM CW potential (without taste) has |B| ~ 4.4 x 10^{-3}, giving 1/(4|B|) ~ 56 -- far too large an exponent (predicts v ~ 5 x 10^{-6} GeV). The taste enhancement helps but overshoots in a different way.

3. **Quantitative gap remains.** The exponential formula predicts an exponent of 25.6 vs the needed 38.4. This corresponds to v being ~10^{5.6} too large. Closing the gap requires either:
   - N_eff_taste ~ 10.7 instead of 16 (plausible: not all tastes couple to Higgs equally)
   - y_t(M_Pl) ~ 0.358 instead of 0.439 (needs ~18% correction)
   - Higher-loop or non-perturbative corrections to the CW exponent

## Circularity Analysis

| Quantity | v-dependent? | Source |
|----------|:---:|--------|
| alpha_unif, sin^2 theta_W | No | Cl(3) lattice |
| y_t/g_s = 1/sqrt(6) | No | Ward identity |
| g_2(M_Z), g'(M_Z), g_s(M_Z) | No | RGE from M_Pl |
| Lambda_QCD/M_Pl | No | alpha_s running |
| m_W/v, m_Z/v, m_t/v | No | Coupling ratios |
| T_CMB | Yes (observed) | Depends on v via recombination |
| H_0 | Yes (observed) | Depends on v via matter content |
| T_c (EWPT) | Yes | = v * sqrt(lambda/c) |
| mu^2 | Yes | = lambda * v^2 |
| g_*(T) thresholds | Yes | Mass thresholds ~ v |

## Parameter Sensitivity

To predict v within a factor of 2, the framework needs N_taste * y_t^2 known to ~1.8%. The framework gives exact ratios (y_t/g_s = 1/sqrt(6)) but the absolute coupling alpha_s(M_Pl) = 0.092 carries lattice artefact uncertainties.

## What Would Close the Gap

The exponent ratio is 0.67 (predicted/needed). Three plausible routes:

1. **Effective taste count.** If only ~11 of 16 taste modes couple to the Higgs in the CW potential, the exponent increases to match. Physical: some tastes may be in the singlet sector of the SU(2) decomposition and decouple from the Higgs.

2. **Higher-loop corrections.** The 2-loop CW potential adds O(alpha_s) corrections to the exponent. With alpha_s ~ 0.1, this is a ~10% effect, moving in the right direction but not enough alone.

3. **Non-perturbative lattice matching.** The V-scheme to MSbar conversion at the lattice cutoff includes power corrections that modify y_t(M_Pl) by O(alpha_s/pi) ~ 3%, which translates to a ~6% correction to the exponent.

## Scorecard

- Checks: 11 PASS / 6 FAIL out of 17
- Exact: 4/9 (expected failures: EWSB without taste, cosmological routes)
- Bounded: 7/8

## Verdict

**v/M_Pl is the ONE remaining dimensionless ratio that the framework has not closed.** The CW mechanism provides the correct parametric structure (exponential suppression via taste-enhanced dimensional transmutation) but a quantitative gap of ~1.5x in the exponent persists. Cosmological boundary conditions (T_CMB, H_0) cannot fill this gap because they depend on v themselves. The most promising path forward is precision determination of the effective taste multiplicity in the CW potential.
