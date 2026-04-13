# BLM Scale for Hierarchy: alpha_V(q*) Determination

PStack experiment: blm-scale-hierarchy
Script: `scripts/frontier_blm_scale.py`

## Summary

The BLM (Brodsky-Lepage-Mackenzie) optimal scale q* for the staggered
fermion self-energy is computed from lattice integrals and used to evaluate
the V-scheme coupling alpha_V(q*).  The result is then fed into the
hierarchy formula to determine v.

**Result: alpha_V(q*) = 0.102, giving v = 6.0 GeV -- not 246 GeV.**

The BLM prescription does NOT naturally produce the alpha_V = 0.14
needed for v = 246 GeV.  The shortfall is a factor ~40 in v.

## Method

### Lattice integrals

Two d=4 lattice integrals are computed on periodic L^4 lattices
(L = 8, 16, 32, 64) with Richardson extrapolation:

| Integral | Definition | Value |
|----------|-----------|-------|
| I_stag(4) | (1/L^4) sum_{k!=0} 1/[sum_mu sin^2(k_mu)] | 0.6197 |
| I_log(4)  | (1/L^4) sum_{k!=0} ln(khat^2)/[sum_mu sin^2(k_mu)] | 1.2221 |

where khat^2 = sum_mu 4 sin^2(k_mu/2) is the Wilson gluon momentum.

Derived quantities:
- Sigma_1 = 4 * I_stag = 2.479 (confirms previous computations)
- Sigma_2 = 4 * I_log = 4.888

### BLM scale

The BLM prescription defines q* as the scale that absorbs all
beta_0-dependent terms:

    ln(q*^2 a^2) = I_log / I_stag = 1.972

This gives **q\*a = 2.68**, consistent with the Lepage-Mackenzie (1993)
result for Wilson fermion self-energy (q\*a = 2.63).  The BLM scale
sits near the edge of the Brillouin zone, as expected for UV-dominated
tadpole integrals.

### V-scheme coupling

With alpha_plaq = 0.092 and beta_0 = 7 (N_f = 6):

    alpha_V(q*) = alpha_plaq / (1 - alpha_plaq * beta_0 * ln(q*^2 a^2) / (4 pi))
                = 0.092 / (1 - 0.092 * 7 * 1.972 / 12.566)
                = 0.1023

### Hierarchy formula

    Z_chi = 1 - alpha_V * C_F * Sigma_1 / (4 pi) = 0.973
    N_eff = 12 * Z_chi^2 = 11.36
    v = M_Pl * exp(-8 pi^2 / (N_eff * y_t^2))
      = 2.435e18 * exp(-40.54)
      = 6.0 GeV

## Key findings

1. **BLM scale is physical**: q\*a = 2.68 matches the known Lepage-Mackenzie
   value for Wilson fermions (2.63), confirming the integral computation.

2. **alpha_V(q\*) = 0.102**: This is larger than alpha_plaq = 0.092 because
   the BLM scale is above 1/a (q\* > 1/a), where the coupling runs to
   larger values.  But 0.102 is still far from the 0.14 needed.

3. **v = 246 GeV requires alpha_V < 0**: The inverse calculation shows
   Z_chi > 1 is needed, requiring negative alpha_V.  This is unphysical
   within the perturbative framework.

4. **y_t sensitivity**: v = 246 GeV falls at y_t = 0.43, only 4% above
   the framework value y_t = 0.414.  The exponential sensitivity means
   small shifts in y_t have enormous effects on v.

## Sensitivity table (alpha_V variation)

| alpha_V | Z_chi  | N_eff  | v (GeV)  | v/v_EW  |
|---------|--------|--------|----------|---------|
| 0.08    | 0.979  | 11.50  | 9.77     | 0.040   |
| 0.10    | 0.974  | 11.38  | 6.33     | 0.026   |
| **0.102** | **0.973** | **11.36** | **6.01** | **0.024** |
| 0.12    | 0.968  | 11.25  | 4.07     | 0.017   |
| 0.14    | 0.963  | 11.13  | 2.60     | 0.011   |

## Sensitivity table (y_t variation)

| y_t   | v (GeV)  | v/v_EW  |
|-------|----------|---------|
| 0.40  | 0.34     | 0.0014  |
| 0.41  | 2.72     | 0.011   |
| **0.414** | **~6** | **~0.024** |
| 0.42  | 19.0     | 0.077   |
| 0.43  | 116      | 0.47    |
| 0.44  | 629      | 2.55    |

## Implications

The BLM prescription gives a well-defined, scheme-independent alpha_V(q*)
that is too small to generate v = 246 GeV from the hierarchy formula with
the framework parameters (y_t = 0.414).

Possible resolutions:
- The hierarchy formula needs higher-order corrections (2-loop self-energy)
- y_t(M_Pl) is slightly larger than the 1/sqrt(6) estimate
- Additional non-perturbative effects modify Z_chi
- The relation v = M_Pl * exp(...) requires modification at the lattice scale

The most economical resolution is a modest upward shift in y_t: even
y_t = 0.43 (4% shift) would bring v within an order of magnitude of 246 GeV.
