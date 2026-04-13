# Taste Determinant Polynomial -- Zeros and EWSB

**Script:** `scripts/frontier_taste_polynomial.py`
**Status:** 16 PASS, 0 FAIL

## Question

On the 4D taste hypercube (16 vertices), does det(D_taste + m) -- a degree-16
polynomial in m -- have zeros that encode the electroweak symmetry breaking
scale v = 246 GeV?

## Setup

The taste Dirac operator on the 2^4 hypercube uses the Clifford algebra
representation:

    xi_1 = sigma_x (x) I (x) I (x) I
    xi_2 = sigma_z (x) sigma_x (x) I (x) I
    xi_3 = sigma_z (x) sigma_z (x) sigma_x (x) I
    xi_4 = sigma_z (x) sigma_z (x) sigma_z (x) sigma_x

These satisfy {xi_mu, xi_nu} = 2 delta_{mu,nu} and give

    D_taste = xi_1 + xi_2 + xi_3 + xi_4

With gauge coupling c = g/u_0 = sqrt(4*pi*alpha)/u_0, the physical operator is
D_phys = c * D_taste.

## Key Results

### 1. Analytic polynomial

The Clifford identity D^2 = d*I (here d = 4) forces all eigenvalues to be
+/- 2. Since tr(D) = 0, there are exactly 8 eigenvalues at +2 and 8 at -2.
The characteristic polynomial is:

    det(D_taste + m*I) = (m + 2)^8 * (m - 2)^8 = (m^2 - 4)^8

With gauge coupling:

    det(c*D_taste + m*I) = (m^2 - 4c^2)^8

Verified numerically to machine precision.

### 2. Zeros and their scale

The polynomial has 16 zeros (each 8-fold degenerate):

    m* = +/- 2c = +/- 2*sqrt(4*pi*alpha)/u_0

For alpha = alpha_EM = 1/137:

    m* = +/- 0.620 in Planck units = +/- 7.6e18 GeV

This is Planck-scale, not electroweak scale.

### 3. Coleman-Weinberg potential

    V(m) = -8 * log|m^2 - 4c^2|

- Minimum at m = 0 (symmetric vacuum)
- Curvature V''(0) = 4/c^2 gives Planck-scale Higgs mass
- Logarithmic singularities at m = +/- 2c (the zeros)
- No spontaneous symmetry breaking from the taste polynomial alone

### 4. Wilson term and degeneracy breaking

The Wilson term splits the 8-fold degeneracy into 5 groups by Hamming weight
(1 + 4 + 6 + 4 + 1 = 16). This creates nontrivial CW potential structure but
the minima remain at O(1) in Planck units.

### 5. Determinant at m = 0

    det(D_phys) = (2g/u_0)^16 = 2^16 * (4*pi*alpha)^8 / u_0^16

The 8th power of the coupling constant appears naturally from the 8 degenerate
doublets of the 4D taste structure.

### 6. Near-coincidence with hierarchy scale

A notable numerical observation:

    alpha_EM^8     = 8.04e-18
    (4*pi*alpha)^16 = 2.50e-17
    v/M_Pl         = 2.02e-17

The quantities alpha^8 and (4*pi*alpha)^16 are within an order of magnitude of
v/M_Pl. Whether this is a coincidence or has structural significance requires
further investigation.

## Conclusions

1. The taste polynomial has a clean analytic form: (m^2 - 4c^2)^8
2. The zeros are at Planck scale, not electroweak scale
3. The CW potential minimum is at the symmetric point m = 0
4. No hierarchy v/M_Pl ~ 10^-17 emerges from the taste structure alone
5. The Wilson term breaks degeneracy but does not solve the hierarchy problem
6. The determinant naturally contains (4*pi*alpha)^8, and the numerical near-match
   alpha^8 ~ v/M_Pl is suggestive but not yet explained mechanistically
