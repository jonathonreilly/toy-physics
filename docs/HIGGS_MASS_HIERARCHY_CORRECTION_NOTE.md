# Higgs Mass: Hierarchy Correction Analysis (Negative Result)

**Date:** 2026-04-14
**Status:** bounded - bounded or caveated result note
direction. No hierarchy correction chain reduces m_H from 140.3 toward 125.

---

## Question

Starting from m_H = v/(2 u_0) = 140.3 GeV (derived in HIGGS_MASS_FROM_AXIOM_NOTE),
does applying the hierarchy's L_t=4 APBC correction reduce m_H toward the
observed 125.25 GeV?

**Answer: No.** The correction increases m_H. Full derivation below.

---

## 1. Eigenvalue spectrum on the minimal APBC blocks

### 1.1 L_t = 2 block (2^3 x 2 = 16 sites)

APBC momenta: k_mu = pi(2n+1)/L_mu with n = 0, 1, ..., L_mu - 1.

Spatial (L_s = 2):  k_i in {pi/2, 3pi/2}.  sin^2(pi/2) = sin^2(3pi/2) = 1.
Temporal (L_t = 2):  k_0 in {pi/2, 3pi/2}.  sin^2(pi/2) = sin^2(3pi/2) = 1.

Staggered dispersion:

    |lambda_hop|^2 = sum_{mu=0}^{3} sin^2(k_mu) = 1 + 1 + 1 + 1 = 4

All 16 modes are degenerate: |lambda_hop| = 2.

Mean-field: |lambda_phys|^2 = u_0^2 * 4 = 4 u_0^2.

### 1.2 L_t = 4 block (2^3 x 4 = 32 sites)

Spatial (L_s = 2, APBC):  same as above, sin^2 = 1 for all spatial.
Temporal (L_t = 4, APBC):  k_0 in {pi/4, 3pi/4, 5pi/4, 7pi/4}.

    sin^2(pi/4) = sin^2(3pi/4) = sin^2(5pi/4) = sin^2(7pi/4) = 1/2

All 4 temporal modes contribute sin^2 = 1/2. Therefore:

    |lambda_hop|^2 = 1/2 + 1 + 1 + 1 = 7/2 = 3.5

All 32 modes are degenerate: |lambda_hop| = sqrt(7/2).

Mean-field: |lambda_phys|^2 = u_0^2 * 7/2 = (7/2) u_0^2.

---

## 2. Curvature of the effective potential

The taste-sector effective potential (convention from HIGGS_MASS_FROM_AXIOM_NOTE):

    V(m) = -(N_eig / 2) * log(m^2 + |lambda_phys|^2)

where N_eig is the number of eigenvalues on the block.

    dV/dm = -(N_eig / 2) * 2m / (m^2 + |lambda|^2)

    d^2V/dm^2 = -(N_eig / 2) * [2|lambda|^2 - 2m^2] / (m^2 + |lambda|^2)^2

At m = 0:

    d^2V/dm^2 |_{m=0} = -N_eig / |lambda_phys|^2

### 2.1 L_t = 2 curvature

N_eig = 16, |lambda_phys|^2 = 4 u_0^2.

    d^2V/dm^2 |_{m=0} = -16 / (4 u_0^2) = -4/u_0^2        [= -5.193]

Per-taste curvature (dividing by N_taste = 16):

    A_2 = |d^2V/dm^2| / N_taste = 4 / (u_0^2 * 16) = 1/(4 u_0^2)

### 2.2 L_t = 4 curvature

N_eig = 32, |lambda_phys|^2 = (7/2) u_0^2.

    d^2V/dm^2 |_{m=0} = -32 / ((7/2) u_0^2) = -64/(7 u_0^2)    [= -11.869]

The L_t=4 block contains 2 taste registers. Per taste register: -32/(7 u_0^2).
Per-taste curvature (dividing by N_taste = 16):

    A_4 = 32 / (7 u_0^2 * 16) = 2/(7 u_0^2) = 1/(3.5 u_0^2)

---

## 3. The curvature ratio

    A_4 / A_2 = [1/(3.5 u_0^2)] / [1/(4 u_0^2)] = 4/3.5 = 8/7

**The curvature at L_t=4 is LARGER than at L_t=2 by a factor 8/7.**

This is the INVERSE of the eigenvalue-magnitude-squared ratio:

    |lambda_2|^2 / |lambda_4|^2 = 4 / 3.5 = 8/7

The curvature 1/|lambda|^2 is larger where the eigenvalue is smaller.
At L_t=4, the temporal sin^2 drops from 1 to 1/2, reducing |lambda|^2,
which INCREASES the curvature.

---

## 4. How the curvature enters m_H

From HIGGS_MASS_FROM_AXIOM_NOTE, the Higgs mass formula is:

    (m_H / v)^2 = per-taste curvature = A_L

At L_t = 2:

    (m_H / v)^2 = A_2 = 1/(4 u_0^2)
    m_H = v / (2 u_0) = 246.22 / 1.7553 = 140.3 GeV

At L_t = 4:

    (m_H / v)^2 = A_4 = 2/(7 u_0^2) = 1/(3.5 u_0^2)
    m_H = v / (sqrt(7/2) * u_0) = 246.22 / 1.6420 = 150.0 GeV

**Using L_t=4 eigenvalues INCREASES m_H from 140.3 to 150.0 GeV.**
The correction factor is sqrt(8/7) = 1.069 (wrong direction).

---

## 5. Comparison of correction powers

Testing (A_2/A_4)^p = (7/8)^p as a multiplicative correction to m_H = 140.3:

| Power p | Factor (7/8)^p | m_H (GeV) | Deviation from 125.25 |
|---------|---------------|-----------|----------------------|
| 1/4     | 0.9672        | 135.7     | +8.3%                |
| 1/2     | 0.9354        | 131.2     | +4.8%                |
| 1       | 0.8750        | 122.8     | -2.0%                |
| 2       | 0.7656        | 107.4     | -14.3%               |

The linear power p = 1 gives 122.8 GeV (close to 125), but there is
no physical derivation justifying this power. Each power has a distinct
physical meaning:

- p = 1/4: dimensional compression (d=4 -> 1 dimension), as used in
  C_APBC for v. But C_APBC ALREADY appears in v = 246.22.
- p = 1/2: mass ratio (sqrt of eigenvalue-squared ratio). This would
  be appropriate if m_H scaled as eigenvalue magnitude, but the
  curvature goes as 1/|lambda|^2, not |lambda|.
- p = 1: curvature ratio. This would apply if m_H^2 scaled linearly
  with the curvature ratio, but the per-taste curvature IS the
  (m_H/v)^2 quantity -- no further ratio is needed.

---

## 6. Why C_APBC does NOT apply independently to m_H

The hierarchy formula already includes C_APBC:

    v = M_Pl * C_APBC * alpha_LM^16 = 246.28 GeV

where C_APBC = (7/8)^{1/4} = 0.9672 enters from the L_t=4 eigenvalue
magnitude ratio:

    sqrt(|lambda_4|^2 / |lambda_2|^2) = sqrt(7/8)

raised to the power 1/2 for a single eigenvalue mode (giving (7/8)^{1/4}).

The Higgs mass formula m_H = v/(2 u_0) uses this corrected v. Applying
a SECOND (7/8) correction to m_H would be double-counting the L_t=4
eigenvalue effect.

**The correction enters v, not m_H/v.** The ratio m_H/v = 1/(2 u_0) is
determined by the L_t=2 eigenvalue structure, which is the correct block
for the taste condensate (HIERARCHY_THEOREM Part 1). L_t=4 modifies the
overall scale (v) but not the curvature ratio (m_H/v).

---

## 7. The physical picture

The hierarchy theorem (HIERARCHY_THEOREM.md) proves that L_t=2 is the
unique block for the UV matching. The C_APBC correction accounts for
the finite-temperature effect of the L_t=4 bosonic bilinear selector.

For m_H, the relevant curvature is d^2V/dm^2 on the L_t=2 taste block.
This gives (m_H/v)^2 = 1/(4 u_0^2), independent of L_t=4.

The hierarchy correction to v from L_t=4 is already absorbed into the
observed v = 246 GeV used as input. No residual correction applies to
m_H/v.

---

## 8. What DOES reduce m_H from 140.3 GeV?

The 12% gap between 140.3 and 125.25 must close through:

1. **2-loop CW corrections.** The dominant O(alpha_s) correction to the
   top loop reduces m_H^2 by ~10-15%. Estimate:
   m_H = 140.3 * sqrt(1 - 0.12) = 131.6 GeV (+5.1%).

2. **Lattice spacing convergence.** The ratio m_H/m_W monotonically
   decreases as the effective lattice spacing decreases (from 1.85 at
   a=1.0 to 1.64 at a=0.5, approaching the SM value 1.56).

3. **Taste-breaking.** The Wilson term splits the 16-fold taste degeneracy
   into a (1,4,6,4,1) staircase, changing the effective N_taste in the
   per-channel curvature formula.

None of these involve the hierarchy L_t=4 correction.

---

## 9. Verdict on the claimed m_H = 124.4 GeV

The claim that applying the "same hierarchy correction chain" to m_H
gives 124.4 GeV is **incorrect**. Specifically:

**(a)** The curvature ratio A_4/A_2 = 8/7 means the L_t=4 curvature
is LARGER, not smaller. If you replace L_t=2 with L_t=4 in the Higgs
mass formula, m_H goes UP to 150 GeV.

**(b)** The factor (7/8)^1 = 0.875 applied to m_H = 140.3 gives 122.8,
close to 124.4, but there is no derivation justifying a first-power
correction. The hierarchy uses (7/8)^{1/4}, which already enters v.

**(c)** The previous agent likely confused the eigenvalue magnitude ratio
(7/8)^{1/2} with the curvature ratio 8/7, and applied the wrong power
to generate a number close to 125.

---

## Summary

| Quantity | L_t=2 | L_t=4 | Ratio (4/2) |
|----------|-------|-------|-------------|
| |lambda_hop|^2 | 4 | 7/2 | 7/8 |
| |lambda_phys| | 2 u_0 | sqrt(7/2) u_0 | sqrt(7/8) |
| per-taste curvature | 1/(4 u_0^2) | 1/(3.5 u_0^2) | 8/7 |
| m_H (with v=246 GeV) | 140.3 | 150.0 | sqrt(8/7) |

**m_H = v/(2 u_0) = 140.3 GeV remains the correct zero-parameter prediction.**
The +12% gap to 125.25 GeV must close through 2-loop CW and lattice
spacing convergence, not through hierarchy corrections.

---

## Dependencies

- `HIGGS_MASS_FROM_AXIOM_NOTE.md` -- m_H = v/(2 u_0) derivation
- `HIERARCHY_THEOREM.md` -- L_t=2 uniqueness, C_APBC origin
- `HIERARCHY_LT2_NOTE.md` -- factorization at L_t > 2
- `HIGGS_MASS_DERIVED_NOTE.md` -- CW analysis and honest status
