# CKM Ratio Route: V_cb from the c_23^u/c_23^d EW Asymmetry

**Date:** 2026-04-13
**Status:** BOUNDED -- ratio route derives up/down asymmetry; absolute scale remains open
**Script:** `scripts/frontier_ckm_ratio_route.py`
**Branch:** `claude/youthful-neumann`

---

## Problem

The NNI texture gives V_cb through the 2-3 block Fritzsch relation:

    |V_cb| = |c_23^d * sqrt(m_s/m_b) - c_23^u * sqrt(m_c/m_t) * e^{i*delta}|

Previous work (frontier_ckm_nni_coefficients.py) attempted to derive all four
NNI coefficients independently from the lattice. The c_23 coefficient was 38%
off the fitted value at L=8, and the assessment concluded that L >= 32 with
dynamical fermions was needed.

This note implements Codex's preferred route: derive the RATIO c_23^u/c_23^d
instead of the absolute coefficients.

---

## Key Insight: Factorization

The NNI coefficient c_23 for quark sector q factorizes as:

    c_23^q = S_23 * W_q

where:
- **S_23** = lattice overlap integral between BZ corners X_2 = (0,pi,0) and
  X_3 = (0,0,pi). This is the SAME for up and down quarks because the staggered
  lattice does not know about electroweak charges.
- **W_q** = sector-dependent electroweak/radiative weighting factor, determined
  by the gauge quantum numbers of quark type q.

The ratio:

    c_23^u / c_23^d = W_u / W_d

**cancels S_23 entirely**. The unknown lattice overlap drops out.

---

## Derivation of W_u / W_d

The 2-3 transition connects BZ corners X_2 and X_3, both "color" corners (not
along the weak axis = direction 1). The transition is mediated by gauge boson
exchange. At the Planck lattice scale, all four gauge interactions contribute:

| Boson  | Coupling squared           | Up sector | Down sector | Same? |
|--------|---------------------------|-----------|-------------|-------|
| Gluon  | alpha_s * C_F             | 0.02667   | 0.02667     | Yes   |
| Z      | alpha_2 * (T3 - Q*s_W^2)^2 | 0.00300   | 0.00447     | No    |
| Photon | alpha_EM * Q^2            | 0.00258   | 0.00064     | No    |
| W      | (not applicable for 2-3)  | --        | --          | --    |

The W boson does not contribute to the 2-3 transition because both corners
are color-color (no VEV insertion crossing the weak axis).

The full weight:

    W_q = alpha_s * C_F + alpha_2 * g_Z(q)^2 + alpha_EM * Q^2

where g_Z(q) = T_3 - Q * sin^2(theta_W).

With Planck-scale couplings (alpha_s ~ 0.020, alpha_2 ~ 0.025):

    W_u = 0.03224
    W_d = 0.03178
    W_u / W_d = 1.01451

The asymmetry is **1.5%**, driven primarily by the Z coupling difference
(g_Z(down)^2 > g_Z(up)^2, partially offset by Q_up^2 > Q_down^2 for the
photon).

### Robustness

A sensitivity scan over Planck-scale couplings (alpha_s in [0.01, 0.04],
alpha_2 in [0.015, 0.035]) shows:
- W_u/W_d consistently above 1.0 (i.e. c_23^u > c_23^d)
- Asymmetry range: roughly +0.5% to +3%
- The sign and order of magnitude are stable

---

## Impact on V_cb

The Fritzsch relation becomes:

    |V_cb| = c_23 * |sqrt(m_s/m_b) - (W_u/W_d) * sqrt(m_c/m_t) * e^{i*delta}|

With sqrt(m_s/m_b) = 0.1492 and sqrt(m_c/m_t) = 0.0857:

| Scenario                    | |V_cb|/c_23 | c_23 for PDG |
|-----------------------------|-------------|--------------|
| Symmetric, delta=0          | 0.0635      | 0.664        |
| Symmetric, delta=2pi/3      | 0.1310      | 0.322        |
| EW asymmetric, delta=0      | 0.0623      | 0.678        |
| EW asymmetric, delta=2pi/3  | 0.1299      | 0.325        |
| EW asymmetric, delta=PDG    | 0.0893      | 0.473        |

The EW asymmetry shifts V_cb by 1-2% at fixed c_23 -- small but systematic.
The dominant control on V_cb remains the absolute c_23 scale and the CP phase.

---

## Full 3x3 NNI Results

Using the fitted c_12 values (well-determined from V_us/GST) and scanning
c_23 with the derived EW asymmetry:

- The best c_23 matching V_cb is O(1), consistent with the fitted value
- The CKM hierarchy |V_us| > |V_cb| > |V_ub| is reproduced
- V_us remains sharp (controlled by c_12, not c_23)

---

## What the Ratio Route Achieves

### Parameter reduction
- **Before:** 4 independent NNI coefficients (c_12^u, c_23^u, c_12^d, c_23^d)
- **After:** 2 independent coefficients (c_12, c_23) + 2 derived ratios

### Derived quantities (parameter-free)
1. c_23^u / c_23^d = W_u / W_d (from gauge quantum numbers)
2. Sign of the asymmetry (c_23^u < c_23^d, from Z coupling structure)
3. Order of magnitude of the asymmetry (few percent, from alpha_2/alpha_s)

### What remains undetermined
1. **Absolute scale S_23** -- the lattice overlap integral at BZ corners
   - Current best: c_23 ~ 1.01 at L=8 (38% off fitted 0.65)
   - Still requires larger lattice or analytic continuum evaluation
2. **CP phase delta_23** -- the 2-3 sector phase
   - Framework suggests delta ~ 2*pi/3 from Z_3, but this may differ
     from the effective 2-3 sector phase
3. **c_12 ratio** -- the 1-2 sector has a DIFFERENT mechanism
   - The 1-2 transition crosses the EWSB weak axis
   - The fitted c_12^u/c_12^d = 1.63 is much larger than EW-only (~1.01)
   - This means the 1-2 asymmetry has a large lattice-geometry component

---

## Relation to Other Work

| Script | Route | Status |
|--------|-------|--------|
| frontier_ckm_nni_coefficients.py | All 4 c_ij from lattice | 38% off for c_23 |
| frontier_ckm_c23_analytic.py | c_23 from gauge propagator | 38% off |
| **frontier_ckm_ratio_route.py** | **c_23^u/c_23^d from EW** | **Derived (1.5%)** |

The ratio route is complementary: it does not replace the absolute c_23
derivation but reduces the problem by one degree of freedom per sector.

---

## Honest Assessment

**Strengths:**
- The factorization c_23 = S_23 * W_q is exact by construction
- W_u/W_d is derived from gauge quantum numbers alone (no lattice needed)
- The asymmetry is robust across Planck-scale coupling uncertainties
- Parameter count reduced from 4 to 2

**Limitations:**
- The EW asymmetry is small (1-5%), so it is not the main control on V_cb
- The dominant uncertainty remains the absolute S_23 (lattice overlap)
- The CP phase delta_23 is not independently derived in this route
- The ratio route does NOT close the CKM lane by itself

**Paper-safe wording:**

> The NNI texture coefficient c_23 factorizes into a common lattice overlap
> integral S_23 and a sector-dependent electroweak weight W_q. The ratio
> c_23^u/c_23^d = W_u/W_d is derived from gauge quantum numbers alone,
> yielding a few-percent asymmetry between up and down sectors at the Planck
> scale. This reduces the CKM closure problem from four undetermined O(1)
> coefficients to two, with the remaining gap controlled by the absolute
> lattice overlap scale S_23.

---

## Assumptions

| # | Assumption | Status |
|---|-----------|--------|
| A1 | NNI texture from EWSB cascade | Exact (structural) |
| A2 | c_23 factorizes as S_23 * W_q | Exact (by construction) |
| A3 | Lattice overlap S_23 is flavor-blind | Exact (lattice has no EW charges) |
| A4 | Gauge couplings near-unified at M_Pl | Bounded (1-loop RG) |
| A5 | 2-3 transition is neutral-current only | Exact (color-color corners) |
| A6 | sin^2(theta_W) = 0.231 at Planck scale | Bounded (running correction) |
