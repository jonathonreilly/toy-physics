# CKM Jarlskog Invariant Diagnosis

**Script:** `scripts/frontier_ckm_jarlskog_diagnosis.py`
**Status:** 9/9 PASS -- diagnostic complete
**Depends on:** `frontier_ckm_full_closure.py`

## Problem Statement

The full closure script (`frontier_ckm_full_closure.py`, 16/16 PASS) derives
all four CKM parameters from zero free parameters, achieving:

| Parameter | PDG    | This work | Deviation |
|-----------|--------|-----------|-----------|
| V_us      | 0.2243 | 0.2237    | -0.3%     |
| V_cb      | 0.0422 | 0.0421    | -0.4%     |
| V_ub      | 0.00382| 0.00376   | -1.6%     |
| **J**     | **3.08e-5** | **8.6e-8** | **~360x too small** |

The Jarlskog invariant J = c12 s12 c23 s23 c13^2 s13 sin(delta) is
suppressed by a factor of ~360 despite V_ub (= s13) being within 1.6%
of PDG. The suppression must therefore come from sin(delta_eff).

## Root Cause: Phase Washout in NNI Diagonalization

The Z_3 input phase delta = 2pi/3 = 120 degrees enters the NNI mass
matrix through M_13 = c13 sqrt(m1 m3) exp(i delta). The physical CKM
phase emerges after diagonalizing H = M M^dagger for both up and down
sectors and forming V = U_u^dag U_d.

Three multiplicative suppressions reduce the effective CKM phase from
120 degrees to ~0.1 degrees (in the V_ub-optimal regime) or ~7 degrees
(in the large-c_13 regime):

### 1. M M^dagger Phase Dilution

The complex phase in M_13 generates imaginary parts in H only through
cross-products:

    Im(H_01) ~ c13 sqrt(m1 m3) c23 sqrt(m2 m3) sin(delta)
    Im(H_02) ~ c13 sqrt(m1 m3) m3 sin(delta)

These are small compared to the diagonal H_ii ~ m_i^2 because
c13 sqrt(m1/m3) is tiny:

- Up sector: c13 sqrt(m_u/m_t) ~ 9e-4
- Down sector: c13 sqrt(m_d/m_b) ~ 8e-3

The Hermitian matrix H is only ~0.1% complex.

### 2. Perturbative Eigenvector Rotation

The small imaginary perturbation to H rotates the diagonalizing unitary
matrices by angles of order Im(H_ij) / (E_i - E_j). For the up sector,
the mass hierarchy (m_u << m_c << m_t) means the eigenvectors pick up
phases of order ~1 degree, not ~120 degrees.

### 3. Near-Degenerate EW Ratio

The CKM matrix V = U_u^dag U_d. If the up and down sectors were
identical, V = I and J = 0 exactly. The CP violation comes entirely
from the mismatch between sectors.

In our framework, c_13^u / c_13^d = c_23^u / c_23^d = W_u/W_d = 1.014.
This 1.4% EW mismatch means the up and down eigenvector phase rotations
nearly cancel, leaving a CKM phase that is a small DIFFERENCE of two
small numbers.

## Two Regimes

The tension manifests differently depending on c_13/c_23:

| Regime | c_13/c_23 | V_ub | V_us | J | J/J_PDG |
|--------|-----------|------|------|---|---------|
| V_ub optimal | 0.021 | 0.00376 | 0.224 | 8.6e-8 | 0.003 |
| V_ub from scan | 0.37 | 0.0038 | 0.175 | 3.7e-6 | 0.12 |
| PDG | -- | 0.00382 | 0.2243 | 3.08e-5 | 1.0 |

The V_ub-optimal regime (small c_13) breaks V_us. The large-c_13
regime gets V_ub right but loses V_us and still has J suppressed 8x.
Neither regime achieves J = J_PDG.

## Key Finding: sin(2pi/3) is Sufficient

If the Z_3 phase survived diagonalization intact, J would be:

    J_naive = c12 s12 c23 s23 c13^2 s13 sin(2pi/3)
            = 3.05e-5 (0.99x PDG)

The Z_3 phase value sin(2pi/3) = 0.866 is within 1% of what is needed
(sin(delta_needed) = 0.875). The problem is entirely in the phase
washout during diagonalization, not in the Z_3 phase value.

## Possible Resolutions

The diagnosis script tests three potential fixes:

### A. Phase in Both Sectors (delta_u != 0, delta_d != 0)

Assigning different Z_3 phases to up and down sectors. Result:
J ~ 5.5e-5 (1.8x PDG) with d_u = 2pi/3, d_d = 4pi/3. However,
this also shifts V_ub to 0.011 (3x too large). The V_ub-J tension
remains.

### B. Phase in M_23 (Not Just M_13)

If the Z_3 phase enters through the 2-3 element (c23 sqrt(m2 m3)),
the phase perturbation to H is much larger because c23 >> c13.
Result with d13=2pi/3, d23=4pi/3: J = 1.5e-4 (4.8x PDG).
This over-generates J but demonstrates the principle: phase placement
matters more than phase value.

### C. Independent c_13^u / c_13^d

Breaking the assumption that the 1-3 EW ratio equals the 2-3 EW ratio.
Best fit gives c_13^u/c_13^d ~ 22 (vs c_23^u/c_23^d = 1.014).
Result: J = 8e-7 (0.03x PDG). Helps but not sufficient alone.

## Conclusion

The J suppression is a structural feature of the NNI texture with:
1. Phase confined to the smallest off-diagonal element (M_13)
2. Nearly identical up/down EW weights (1.4% mismatch)
3. Extreme quark mass hierarchy (m_u/m_t ~ 10^{-5})

This is not a bug in the code. It is a genuine physics constraint that
the simplest NNI + single-Z_3-phase framework cannot simultaneously
reproduce V_ub and J. The most promising resolution is placing the
Z_3 phase in M_23 (or both M_13 and M_23), which leverages the larger
c_23 coefficient to preserve the phase through diagonalization.
