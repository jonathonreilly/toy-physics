# V_ub from Full 3x3 NNI Mass Matrix Diagonalization

**Status:** BOUNDED -- V_ub within factor 2 of PDG; structural suppression verified  
**Script:** `scripts/frontier_ckm_v_ub_exact.py`  
**Date:** 2026-04-13  
**Route:** Target C route 3 (CKM / flavor closure)

## Setup

The NNI (nearest-neighbor interaction) texture for each quark sector q:

    M_q = [[m_1,  c_12 * sqrt(m_1 m_2),  0                    ],
            [c_12 * sqrt(m_1 m_2),  m_2,  c_23 * sqrt(m_2 m_3)],
            [0,  c_23 * sqrt(m_2 m_3),  m_3                    ]]

The key structural feature: **c_13 = 0** (2-loop suppressed, measured at 0.19 on L=6 lattice). With c_13 = 0, the 1-3 mixing V_ub is controlled entirely by the indirect path 1 -> 2 -> 3.

The CKM matrix is V = U_u^T U_d, where U_q diagonalizes M_q.

## Result 1: Symmetric case (c_12^u = c_12^d, c_23^u = c_23^d)

Fixing c_12 and c_23 to reproduce V_us = 0.2243 and V_cb = 0.0412:

| Parameter | Value |
|-----------|-------|
| c_12      | 0.758 |
| c_23      | 0.635 |
| \|V_us\|  | 0.2243 (exact match) |
| \|V_cb\|  | 0.0412 (exact match) |
| **\|V_ub\|** | **0.00181** |
| PDG \|V_ub\| | 0.00382 |
| Ratio     | **0.47** (factor 2.1 low) |

V_ub is predicted within a factor of 2 of PDG with zero free parameters
beyond those already fixed by V_us and V_cb.

## Result 2: Structural suppression

The 3x3 NNI diagonalization produces V_ub that is significantly suppressed
below the naive Wolfenstein product:

    |V_ub| / (|V_us| * |V_cb|) = 0.196

This is a factor ~5 suppression relative to the simple product |V_us| * |V_cb| = 0.00924.  PDG gives the ratio 0.41.

The suppression arises from the coupled 1-2 and 2-3 rotations in the full 3x3
eigenvector problem. The sequential two-rotation formula overestimates V_ub by
a factor of 5-8x. The full diagonalization is essential.

## Result 3: c_13 sensitivity

| c_13 | \|V_ub\| | PDG ratio |
|------|----------|-----------|
| 0.00 | 0.00181  | 0.47      |
| 0.10 | 0.00131  | 0.34      |
| 0.15 | 0.00288  | 0.75      |
| **0.19** | **0.00413** | **1.08** |
| 0.25 | 0.00600  | 1.57      |

At c_13 = 0.19 (L=6 lattice value), V_ub = 0.00413 -- within 8% of PDG.

The direct 1-3 path (c_13 * sqrt(m_1 * m_3)) is comparable to the indirect
product when c_13 ~ 0.19. The interference between direct and indirect paths
is constructive in this region, pushing V_ub toward the PDG value.

This is an important finding: the L=6 lattice c_13 value is not negligible
for V_ub. The NNI structural suppression (c_13 ~ 0 at 2-loop level) puts
V_ub in the right ballpark, but the residual c_13 ~ 0.19 is actually needed
to reach PDG.

## Result 4: Asymmetric scan

With the EW-derived c_23 asymmetry (c_23^u/c_23^d = 1.015 from ratio route)
and scanning c_12 asymmetry:

| c_12^u/c_12^d | \|V_ub\| | PDG ratio |
|----------------|----------|-----------|
| 0.50           | 0.00066  | 0.17      |
| 0.80           | 0.00135  | 0.35      |
| 1.00           | 0.00187  | 0.49      |

The c_12 asymmetry is the main lever for V_ub, but even at r_12 = 1.0
(symmetric), V_ub stays below PDG by factor ~2.  No physically motivated
c_12 asymmetry in the range scanned reaches PDG without also invoking nonzero
c_13 or the CP phase delta.

## Result 5: Full CKM matrix (symmetric, c_13 = 0)

    |V| =  0.9745   0.2243   0.0018
           0.2240   0.9737   0.0412
           0.0110   0.0397   0.9992

Unitarity: max|V V^T - I| < 1e-15.

Hierarchy |V_us| > |V_cb| > |V_ub| reproduced.

## What this closes

- V_ub is computed from the full 3x3 NNI texture for the first time, not
  from the naive Wolfenstein product.
- The symmetric NNI texture (c_13 = 0) gives V_ub = 0.00181, within factor 2
  of PDG, with zero additional free parameters.
- The structural suppression |V_ub| / (|V_us| * |V_cb|) ~ 0.2 is a prediction
  of the NNI texture, though it undershoots the PDG value of 0.41.
- Including the L=6 lattice c_13 = 0.19 brings V_ub within 8% of PDG.

## What remains open

1. **c_13 value:** The NNI texture predicts c_13 ~ 0 at 2-loop level, but
   the L=6 lattice gives c_13 ~ 0.19, which is the value needed for V_ub.
   This c_13 is not derived from first principles at the precision needed.

2. **CP phase:** This analysis uses real symmetric mass matrices (delta = 0).
   The CP phase delta can shift V_ub by O(1) via interference. A complex NNI
   analysis with the Z_3 phase structure would be the next step.

3. **Absolute NNI scale:** c_12 and c_23 are still set by fitting V_us and
   V_cb, not derived from first principles. The lattice overlap integral
   (L >= 32 or analytic continuum) is still needed.

4. **c_12 asymmetry:** The fitted c_12^u/c_12^d ~ 1.63 (from NNI coefficients
   script) is much larger than the EW-only ~1.015. The 1-2 sector has a large
   lattice-geometry component that is not yet derived.

## Honest assessment

**Strengths:**
- First complete 3x3 NNI computation of V_ub in this framework
- V_ub within factor 2 of PDG with no free parameters (c_13 = 0 case)
- V_ub within 8% of PDG when using the L=6 lattice c_13 = 0.19
- All checks pass (11/11)
- Structural suppression below V_us * V_cb is a genuine texture prediction

**Limitations:**
- The symmetric c_13 = 0 result is factor 2.1 low
- Reaching PDG requires either nonzero c_13 or the CP phase -- both not yet
  sharp from first principles
- The sequential-rotation formula does not work for V_ub; full 3x3 diag is
  required
- This does NOT close the CKM lane by itself

**Paper-safe wording:**

> The NNI texture with structural c_13 suppression predicts |V_ub| within
> a factor of 2 of the PDG value from the full 3x3 mass matrix
> diagonalization, using no free parameters beyond those fixed by |V_us| and
> |V_cb|. Including the residual c_13 ~ 0.19 from the L = 6 lattice brings
> |V_ub| within 8% of PDG. The structural suppression
> |V_ub| / (|V_us| |V_cb|) ~ 0.2 is a prediction of the NNI texture, though
> it undershoots the observed ratio of 0.41. Quantitative closure requires
> first-principles control of c_13 and the CP phase.

## Assumptions

| # | Assumption | Status |
|---|-----------|--------|
| A1 | NNI texture from EWSB cascade | Exact (structural) |
| A2 | c_13 = 0 (2-loop suppressed) | Bounded (L=6 gives 0.19) |
| A3 | Real symmetric mass matrices (delta = 0) | Approximation |
| A4 | PDG quark masses as input | Standard |
| A5 | c_12, c_23 fitted to V_us, V_cb | By construction |
