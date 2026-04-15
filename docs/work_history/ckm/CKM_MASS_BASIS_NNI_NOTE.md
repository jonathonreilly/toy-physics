# Historical CKM Mass-Basis NNI Note: V_ub from Schur Complement + Mass-Ratio Suppression

**Status**: historical bounded CKM route note -- V_ub closed to 1.14x PDG via mass-eigenvalue NNI normalization
**Depends on**: `CKM_SCHUR_COMPLEMENT_THEOREM`, `CKM_WOLFENSTEIN_CASCADE_THEOREM`, `EWSB_GENERATION_CASCADE`
**Script**: `scripts/frontier_ckm_mass_basis_nni.py`

**Current publication disposition:** bounded flavor companion only. Not on the
retained flagship claim surface.

---

## The Problem

The Schur complement of the 3x3 NNI mass matrix generates

    c_13^eff = c_12 * c_23

in the geometric-mean NNI normalization (M_ij = c_ij * sqrt(m_i * m_j)).

With O(1) geometric-mean coefficients (c_12 ~ 1.5, c_23 ~ 0.65), the naive
Schur complement gives |V_ub| ~ 0.02, overshooting PDG (0.00382) by ~5x.

---

## The Fix: Mass-Eigenvalue NNI Normalization

The geometric-mean NNI coefficients normalize off-diagonal elements by
sqrt(m_i * m_j). The physical mixing angles depend on the mass-eigenvalue
NNI coefficients, which normalize differently:

    c_ij^phys = c_ij^geom * sqrt(m_i / m_j)    for i < j

This is the standard NNI normalization (Branco, Lavoura, Silva -- "CP
Violation," Chapter 6). The mass-ratio factor sqrt(m_i/m_j) converts from
a basis where off-diagonal elements are O(sqrt(m_i * m_j)) to one where
they are O(m_j * epsilon_ij), with epsilon_ij carrying the physical
suppression.

---

## Results

### Mass-ratio suppression factors

| Ratio | Up sector | Down sector |
|-------|-----------|-------------|
| sqrt(m_1/m_2) | sqrt(m_u/m_c) = 0.041 | sqrt(m_d/m_s) = 0.224 |
| sqrt(m_2/m_3) | sqrt(m_c/m_t) = 0.086 | sqrt(m_s/m_b) = 0.149 |
| sqrt(m_1/m_3) | sqrt(m_u/m_t) = 0.0035 | sqrt(m_d/m_b) = 0.033 |

Chain rule: sqrt(m_1/m_3) = sqrt(m_1/m_2) * sqrt(m_2/m_3) -- exact.

### Mass-basis NNI coefficients

| Coefficient | Geom-mean | Mass-basis (up) | Mass-basis (down) |
|-------------|-----------|-----------------|-------------------|
| c_12 | 1.48 / 0.91 | 0.061 | 0.203 |
| c_23 | 0.65 / 0.65 | 0.056 | 0.097 |
| c_13 (Schur) | 0.96 / 0.59 | 0.0034 | 0.020 |

### CKM comparison

| Element | Mass-NNI | PDG | Ratio | Status |
|---------|----------|-----|-------|--------|
| |V_us| | 0.2251 | 0.2243 | 1.004 | GOOD |
| |V_cb| | 0.0420 | 0.0422 | 0.994 | GOOD |
| |V_ub| | 0.00435 | 0.00382 | 1.14 | GOOD |
| J | 4.5e-6 | 3.1e-5 | 0.15 | BOUNDED |

### V_ub gap closure

    Geometric-mean NNI: |V_ub| = 0.020  (5.3x PDG)
    Mass-basis NNI:     |V_ub| = 0.0043 (1.14x PDG)
    PDG:                |V_ub| = 0.0038

The mass-ratio suppression closes the gap by a factor of 4.6x.

---

## The Wolfenstein Identification

In the mass-eigenvalue NNI basis, the Schur complement chain becomes:

    c_13^phys = c_12^phys * c_23^phys

This follows from the chain rule: sqrt(m_1/m_3) = sqrt(m_1/m_2) * sqrt(m_2/m_3).

Identifying lambda ~ c_12^phys(down) ~ sqrt(m_d/m_s) and
A*lambda^2 ~ c_23^phys(down) ~ sqrt(m_s/m_b) gives:

    V_ub ~ c_13^phys = lambda * A*lambda^2 = A * lambda^3

This IS the Wolfenstein parametrization, derived from the Schur complement
plus mass-ratio normalization. The powers of lambda trace back to the
mass hierarchy from the EWSB cascade.

---

## Open Issues

1. **Jarlskog invariant**: J is suppressed by ~7x relative to PDG. The
   Berry phase delta = 2pi/3 combined with the small mass-basis c_13
   gives too little CP violation. The resolution likely involves the
   interplay between up and down sector phases.

2. **rho_bar and eta_bar**: These Wolfenstein parameters are off (rho_bar
   too large, eta_bar too small), related to the J suppression.

3. **All mass ratios are framework-derived**: The EWSB cascade
   (frontier_ewsb_generation_cascade.py) gives the mass hierarchy from
   loop suppressions. The mass-basis NNI normalization thus uses only
   framework inputs.

---

## Key Insight

The factor-6 gap between the naive Schur complement and PDG |V_ub| is
not a failure of the Schur complement structure. It is the expected
consequence of using the geometric-mean NNI normalization, where
coefficients are O(1) by construction. Converting to the mass-eigenvalue
basis via c_ij^phys = c_ij^geom * sqrt(m_i/m_j) applies the physical
suppression from the quark mass hierarchy, yielding |V_ub| within 14%
of the PDG value.
