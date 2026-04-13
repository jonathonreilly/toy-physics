# CKM from Z3 Fourier Texture + Observed Quark Masses

**Script:** `scripts/frontier_ckm_from_texture.py`
**Status:** 9/9 checks pass, 5 bounded
**Lane status:** BOUNDED -- texture predicts hierarchy + CP violation but V_cb too small by 8x

## Status

BOUNDED. The Z3 Fourier texture with observed quark masses as input
produces a CKM matrix with the correct qualitative features (hierarchy
ordering, CP violation, approximate Cabibbo angle) but fails
quantitatively: |V_cb| is too small by a factor ~8 with a universal
coupling, and the two-parameter extension over-predicts |V_ub| by ~17x.

## Approach

The mass matrix texture is:

    M_q = diag(m_1, m_2, m_3) + epsilon * F3_off

where F3_off is the off-diagonal part of the Z3 Fourier matrix:

    F3 = (1/sqrt(3)) [[1,1,1],[1,w,w^2],[1,w^2,w]]    w = e^{2*pi*i/3}

The diagonal encodes the EWSB-selected hierarchy (observed masses).
The off-diagonal F3 encodes the Z3 cyclic symmetry of BZ corners.
The Z3 phases (omega) provide CP violation.

Given observed masses, V_CKM = U_u^dag U_d where U_q diagonalizes
M_q M_q^dagger. With a single universal epsilon, the Cabibbo angle
fixes epsilon = 40.9 MeV, and V_cb, V_ub, J are predictions.

## Results

### Part A: Single universal epsilon (1 input, 2 predictions)

| Element | Predicted | PDG | Ratio |
|---------|-----------|-----|-------|
| V_us | 0.2243 | 0.2243 | 1.00 (input) |
| V_cb | 0.0054 | 0.0422 | 0.13 |
| V_ub | 0.0056 | 0.0039 | 1.41 |
| J | 5.6e-6 | 3.2e-5 | 0.18 |

### Part B: Separate epsilons (2 inputs, 1 prediction)

eps_u = 1533 MeV, eps_d = 460 MeV (ratio 3.3)

| Element | Predicted | PDG | Ratio |
|---------|-----------|-----|-------|
| V_us | 0.2243 | 0.2243 | 1.00 (input) |
| V_cb | 0.0422 | 0.0422 | 1.00 (input) |
| V_ub | 0.066 | 0.0039 | 16.8 |
| J | 6.0e-4 | 3.2e-5 | 18.9 |

## Root Cause of Deficit

The analytic perturbative formula reveals the core issue:

    |V_cb|/|V_us| ~ (m_s - m_d)/(m_b - m_s) = 88.7/4086.6 = 0.022

but the PDG requires 0.188 -- an 8.3x discrepancy.

With universal |F_ij| = 1/sqrt(3) (Z3 symmetry), all off-diagonal
couplings are equal. The CKM hierarchy is then controlled entirely
by mass splittings. The down-type mass splittings are too hierarchical
(m_b >> m_s >> m_d) to reproduce the observed CKM pattern.

## What Would Close the Gap

1. **Broken Z3 in off-diagonal couplings:** Need |F_23|/|F_12| ~ 8.7.
   This would require the (2,3) inter-generation coupling to be much
   stronger than (1,2), breaking the Z3 universality.

2. **Sector-dependent coupling:** eps_u/eps_d ~ 3.3 (tan beta ~ 3.3
   in 2HDM language). But even with two parameters, V_ub is over-predicted
   by factor 17.

3. **RG running:** The quark masses at mu = 2 GeV may not be the
   relevant scale. Running between m_s and m_b could modify the
   effective texture.

## What Is Actually Proved

1. The Z3 Fourier texture produces CP violation from omega = e^{2*pi*i/3}
   with no additional CP phase input.

2. The CKM hierarchy |V_us| > |V_cb| emerges from mass splittings
   (this is borderline since V_cb ~ V_ub in the single-eps case).

3. The Cabibbo angle scale is reproduced with eps ~ 41 MeV ~ sqrt(m_d * m_s)/2.

4. The quantitative CKM pattern CANNOT be reproduced with universal
   off-diagonal Z3 couplings and observed masses.

## Assumptions

1. MS-bar quark masses at mu = 2 GeV (light) and mu = m_q (heavy)
2. Z3 Fourier matrix as the off-diagonal texture
3. Universal or sector-dependent epsilon coupling
4. First-order perturbation theory validated by numerical diagonalization
