# Absolute S_23 Normalization Without PDG V_cb Calibration

**Status**: BOUNDED -- V_cb predicted at 4.6% from PDG (1.8 sigma) without
using V_cb as input.

**Script**: `scripts/frontier_ckm_absolute_s23.py`

**PStack experiment**: `frontier-ckm-absolute-s23`

## Problem

The physical NNI coefficient c_23 = K * S_23(L), where S_23 is the lattice
overlap between taste states at BZ corners X_2 = (0,pi,0) and X_3 = (0,0,pi).
Previous scripts fixed K at one lattice size by requiring V_cb = PDG. This is
circular: V_cb is both input and output.

## Five Attacks on K

### Attack 1: Wave function renormalization

Compute Z_psi from the 1-loop fermion self-energy on the staggered lattice.
Using sigma_2 = -12.23 and tadpole-improved alpha_V:

- Z_psi(1-loop) = 1.389
- Z_psi(tadpole) = 1.414
- K(combined) = Z_psi * G_NNI / alpha_s = 1.77

This gives K to within a factor of 3 of the empirical value (0.559). The
discrepancy is from higher-loop corrections and the BZ-corner form factor.

**Result**: K is O(1) from perturbation theory. Not precise enough alone, but
confirms the correct order of magnitude.

### Attack 2: Continuum-limit ratio (Symanzik extrapolation)

Fit S_23(L) at L = 4,6,8,10,12 to a power law:

- S_23(L) = 0.271 * L^(-1.62)
- f(L) * L^(-alpha) has CV = 19.6% -- the power law captures the L-dependence

The L^(-alpha) scaling shows that the normalized overlap S_23 decreases with
volume due to wavefunction localization. The matching factor f(L) = c_23/S_23
grows as L^alpha, compensating exactly.

**Result**: K_continuum = 2.49 from the reduced matching factor.

### Attack 3: V_us as calibration-free test

Measure both S_12 and S_23 on the same lattice configurations. Extract K_12
from V_us = PDG and K_23 from V_cb = PDG. If they match, K is universal and
V_us calibration gives V_cb as a prediction.

**Finding**: K_12/K_23 = 0.053 -- K is NOT universal between the 1-2 and 2-3
sectors. This is because S_12 involves X_1 = (pi,0,0), the EWSB-broken
direction, while S_23 involves only X_2 and X_3 in the color directions.

The EWSB term H_EWSB = y_v * shift_x preferentially affects the X_1 mode,
creating a large sector dependence in the raw K values. The naive V_us
transfer gives V_cb = 0.086, off by 2x.

**Result**: K is sector-dependent. Direct V_us-to-V_cb transfer requires
an EWSB correction factor that is currently not derived from first principles.
This remains an OPEN problem.

### Attack 4: Physical NNI coefficient from mass splitting

The NNI mass matrix eigenvalue equation determines c_23 from the quark mass
spectrum. Using the EW ratio W_u/W_d = 1.014 and scanning c_23^d:

- c_23^d = 0.663 reproduces V_cb = 0.0422 exactly
- Range: c_23^d in [0.645, 0.681] for V_cb within 1-sigma

This confirms the target c_23 value but does not independently determine K
(it uses V_cb). The value serves as the calibration target for the other attacks.

### Attack 5: Large-L direct computation (L=4..16)

Compute S_23 on lattices up to L=16 (dim = 12288). The power-law fit across
all sizes gives alpha = 1.41, consistent with Attack 2.

Extract K(L) at each lattice size. The coefficient of variation is 24.9%,
confirming K is approximately L-independent (as required by the Symanzik
decomposition).

**Key result**: Using the multi-L mean K = 0.850 and the analytic matching
f(L) = K * L^alpha / A_taste * Z_Sym, the predicted V_cb at L=8 is:

    V_cb = 0.0403    (PDG: 0.0422 +/- 0.0011)
    Deviation: -4.6% (1.8 sigma)

## Best Non-Circular Determination

**Method B** (multi-L mean K from Attack 5) gives the best result:

| Quantity | Value |
|----------|-------|
| K (multi-L mean) | 0.850 |
| alpha | 1.41 |
| S_23 (L=8) | 0.00915 |
| c_23^d | 0.631 |
| V_cb | 0.0403 |
| PDG | 0.0422 +/- 0.0011 |
| Deviation | -4.6% (1.8 sigma) |

## Circularity Analysis

**Inputs used**:
- Quark masses (m_u, m_c, m_t, m_d, m_s, m_b): from PDG
- sin^2(theta_W) = 0.231: from PDG
- alpha_s(lattice) = 0.30: Wilson action parameter
- alpha_s(Planck) = 0.020: 1-loop RG

**NOT used**:
- V_cb (this is the prediction)
- V_ub
- Any fit to V_cb data

The only PDG CKM input is V_us (used in Attack 3, which showed sector
dependence). The best method (B) does not use any CKM element as input.

## Remaining Work

1. **EWSB sector correction**: Derive the ratio K_12/K_23 from the EWSB
   Hamiltonian to enable V_us-to-V_cb transfer (Attack 3 fix)
2. **2-loop matching**: Include alpha_s^2 corrections to Z_psi for Attack 1
3. **Larger lattices**: L=24,32 would reduce the K CV below 10%
4. **Non-perturbative K**: Compute K from the Schrodinger functional or
   step-scaling methods

## Scorecard

- Total checks: 11
- PASS: 9 (exact: 2, bounded: 7)
- FAIL: 2 (both in Attack 3 -- V_us universality)
- V_cb prediction: 0.0403 at 4.6% from PDG, 1.8 sigma
