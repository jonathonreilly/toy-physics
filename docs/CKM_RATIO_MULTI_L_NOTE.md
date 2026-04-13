# CKM c_12/c_23 Ratio: Multi-L High-Statistics Measurement

**Script**: `scripts/frontier_ckm_ratio_multi_L.py`
**Status**: PENDING RUN

## Status

PENDING. Script written and ready for execution. Previous single-L measurement
gave R_12/23 = 3.68 from L=8 with 12 configs and large spread. This script
performs the multi-L, high-statistics measurement needed to reduce normalization
uncertainty.

## Problem

The ratio c_12/c_23 is the cheapest non-circular route to reduce the
normalization uncertainty in the CKM derivation (instructions.md, Target C,
route 3). The previous measurement (frontier_ckm_c23_analytic.py) found
c_12/c_23 = 3.68 from L=8 with only 12 configurations. The statistical spread
was large, and there was no check of volume dependence. With more configurations
and multiple L values, we can:

1. Reduce statistical error (jackknife + bootstrap)
2. Check L-dependence (should be weak if the ratio is physical)
3. Extrapolate to L -> infinity if there is a trend

## Method

### Observable

The ratio R = |T_12|/|T_23| is measured on each gauge configuration, where
T_ij = <psi_i| H |psi_j> is the inter-valley scattering amplitude between
BZ corners X_i and X_j.

This ratio eliminates the absolute normalization K entirely. It measures the
EWSB asymmetry between weak-axis (1-2) and color (2-3) transitions.

### Lattice setup

- SU(3) gauge configurations via Metropolis at beta = 6
- Staggered + Wilson Dirac operator with r_W = 1.0
- EWSB: H_EWSB = y*v*Gamma_1 with yv = 0.5
- Wave packets at BZ corners X_1=(pi,0,0), X_2=(0,pi,0), X_3=(0,0,pi)
- Color-averaged: T_ij summed over 3 color orientations

### Lattice plan

| L  | N_cfg | dim   | Memory  | Purpose                    |
|----|-------|-------|---------|----------------------------|
| 6  | 50    | 648   | 0.006 GB| Fast baseline              |
| 8  | 50    | 1536  | 0.04 GB | Primary measurement        |
| 10 | 30    | 3000  | 0.14 GB | Volume check               |
| 12 | 20    | 5184  | 0.40 GB | Large-volume anchor        |

Total: 150 configurations across 4 lattice sizes.

### Analysis

1. Per-L: jackknife and bootstrap error on R
2. L-dependence: weighted mean, chi^2/dof consistency test
3. If chi^2/dof < 2: use weighted mean as best R
4. If chi^2/dof > 2: fit R(L) = R_inf + c/L, extrapolate
5. Z2 check: R_13/23 should be close to 1 (X_2, X_3 degenerate)

### CKM extraction

From the best R, the NNI coefficient ratios are:

    c_12/c_23 (up)   = R * sqrt(kappa_12^u / kappa_23^u)
    c_12/c_23 (down)  = R * sqrt(kappa_12^d / kappa_23^d)

where kappa are EW charge factors. Absolute coefficients follow from the 1-loop
normalization C_base = N_c * alpha_s * L_enh / pi, with the ratio fixing c_12
relative to c_23.

## Previous result

From frontier_ckm_c23_analytic.py (L=8, 12 configs):
- R_12/23 = 3.68 (large spread)
- c_23 = c_12^u / R = 1.48 / 3.68 = 0.40
- Deviation from fitted c_23 = 0.65: 38%

## Expected outcome

With 150 total configs across 4 L values:
- Statistical error on R should drop by factor ~3 compared to 12-config run
- L-dependence check will establish whether the ratio is a physical observable
  or a finite-volume artifact
- If R stabilizes across L, this is strong evidence that the EWSB asymmetry
  is physical and the ratio method is the correct route

## Honest assessment

This measurement addresses the normalization uncertainty, which is the dominant
systematic in the CKM derivation. However:

- The absolute scale (C_base) still carries 1-loop normalization uncertainty
- The ratio alone does not close V_cb; it sharpens the c_12/c_23 input
- V_ub and J closure require separate c_13 and phase work (routes 5-6)
- Success here means tighter c_12/c_23, not full CKM closure

## Assumptions

1. Framework premise: Cl(3) on Z^3 with staggered taste = generation structure
2. Wilson gauge action at beta = 6 produces physical gauge configurations
3. BZ corner wave packets at X_1, X_2, X_3 correspond to the three generations
4. EWSB in direction 1 is the correct Higgs mechanism on the lattice
5. Metropolis thermalization (100 sweeps) is sufficient at beta = 6
