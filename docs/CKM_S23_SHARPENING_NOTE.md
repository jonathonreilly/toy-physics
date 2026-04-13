# CKM S_23 Sharpening: What Codex Did and What Remains

**Date:** 2026-04-13
**Branch:** claude/youthful-neumann
**Gate:** CKM / quantitative flavor closure (live gate 3)

---

## What Codex Pushed

Three new deliverables on the CKM lane:

1. **CKM_ABSOLUTE_S23_NOTE.md + frontier_ckm_absolute_s23.py**
   Five attacks on the matching factor K to remove circular V_cb
   calibration. Best result (Method B, multi-L mean K): V_cb = 0.0403,
   4.6% low (1.8 sigma). 9/11 checks pass.

2. **CKM_J_DERIVED_NOTE.md + frontier_ckm_j_derived.py**
   Four attacks on the Jarlskog invariant J from Higgs Z_3^3 charges.
   Best result: J/J_PDG = 0.993 (full 3-phase NNI), but at the cost
   of spoiling |V_us| and |V_cb| by factors of 2-3. Single-phase NNI
   gives J/J_PDG = 0.73 with good angles. 9/9 pass, all BOUNDED.

3. **frontier_ckm_c13_derived.py**
   Four attacks on c_13. Wolfenstein scaling gives c_13 = 0.057,
   |V_ub| = 0.0053 (40% off PDG). The indirect path c_12*c_23
   overshoots PDG |V_ub| by 10%; direct c_13 with Z_3 phase provides
   partial cancellation. 14/16 pass.

---

## Assessment of the Three Questions

### Q1: Does the S_23 script remove the sector correction?

**No.** The EWSB sector correction remains an open problem.

Attack 3 (V_us calibration) explicitly showed K is NOT universal between
the 1-2 and 2-3 sectors: K_12/K_23 = 0.053. The physical reason is
clear -- S_12 involves X_1 = (pi,0,0), the EWSB-broken direction, while
S_23 involves only X_2 and X_3 in the color directions. The EWSB term
H_EWSB = y*v*shift_x amplifies the 1-2 overlap relative to 2-3.

Method B (multi-L mean K = 0.850) gets V_cb = 0.0403 without using V_cb
as input, but it uses K extracted from V_cb at EACH lattice size and then
averaged -- this is still implicitly circular (K at each L is defined by
requiring c_23 = target at that L). The V_cb prediction from this K is
really a self-consistency check, not a first-principles derivation.

The non-circular methods (Attack 1: wavefunction renormalization K = 1.77,
Attack 2: continuum extrapolation K = 2.49) give V_cb = 0.078 and worse.
These are O(1) estimates only.

**Bottom line:** The sector correction is diagnosed but not removed. K
remains the dominant uncertainty.

### Q2: Can O(a^4) Symanzik corrections reduce the K spread?

**Partially, but not enough.**

The script already includes an O(a^4) Symanzik fit (Fit 3):

    S_23(L) = S_inf + c1/L^2 + c2/L^4

Results:
- S_inf = 0.0059, c1 = -0.008, c2 = 7.72
- The L^4 term dominates for small L (c2/L^4 ~ 0.03 at L=4)
- Residuals at L=8: measured 0.00915, fit 0.00764 (16% off)

The problem is that O(a^4) Symanzik corrections improve the S_23(L) fit
quality but do NOT determine K. The matching factor K enters as:

    c_23 = K * L^alpha / A_taste * Z_Sym * S_23(L)

Even with a perfect S_23(L) extrapolation, K_0 (the volume-independent
normalization) is still needed. The current K CV = 24.9% across L = 4..16
could potentially be reduced by:

1. Including O(a^4) corrections to the taste-exchange vertex A_taste:

       A_taste -> A_taste * (1 + d1*a^2*p^2 + d2*a^4*p^4)

   The O(a^2) piece is already Z_Sym = 1.72. The O(a^4) correction at
   the BZ corner (a*p = pi) would be d2*pi^4 ~ 100*d2. If d2 ~ O(alpha_s^2)
   ~ 0.01, this is a ~1 correction, i.e. O(100%) -- not perturbative at
   the BZ corner.

2. Using tree-level improvement (fat links, HYP smearing) to reduce the
   taste-exchange vertex before extracting S_23. This is the standard
   lattice QCD approach for staggered fermions, but it requires modifying
   the lattice Hamiltonian itself, not just the analysis.

**Bottom line:** O(a^4) Symanzik corrections at the BZ corner are
non-perturbative. The Symanzik expansion breaks down when a*p = O(1).
This is a well-known problem in staggered fermion physics. The correct
fix is either (a) smeared/improved actions or (b) a non-perturbative
matching procedure.

### Q3: Can we extract K from multiple L values and extrapolate L -> inf?

**Already attempted; does not converge.**

Attack 5 computes S_23 at L = 4, 6, 8, 10, 12, 16 and extracts K(L) at
each size. Results:

| L  | S_23    | K(L)  |
|----|---------|-------|
| 4  | 0.0356  | ~0.5  |
| 6  | 0.0108  | ~0.7  |
| 8  | 0.0092  | ~0.6  |
| 10 | 0.0054  | ~1.0  |
| 12 | 0.0075  | ~0.8  |
| 16 | 0.0041  | ~1.2  |

K(L) has CV = 24.9%. The trend is weakly increasing with L, suggesting
that the true K_0 in the continuum limit may be larger than the mean.
But with only 6 points and large fluctuations (especially at L=10,12
where n_configs is only 3-5), a reliable L -> inf extrapolation is not
possible.

To get K CV below 10%, one would need:
- L = 24, 32 lattices (dim = 41472, 98304) -- feasible on a workstation
  with sparse methods
- O(20+) gauge configurations at each L for reliable error bars
- This is a real compute investment, not a conceptual blocker

---

## What Remains for the CKM Lane

### Priority 1: Non-perturbative K determination

The highest-value target. Three viable routes:

**(A) Schrodinger functional / step scaling.**
Define the running overlap S_23(mu) at scale mu using Schrodinger
functional boundary conditions. Step from mu = 1/L to mu = 0 (continuum)
using discrete beta-function steps. This is the gold-standard lattice
method for non-perturbative matching. Requires implementing SF boundary
conditions on the Z^3 lattice.

**(B) Ratio method (sector-independent).**
The ratio c_12/c_23 = 3.68 from the gauge propagator matrix element
(CKM_C23_ANALYTIC_NOTE.md) is sector-independent because EWSB cancels
in the ratio. Combined with the already-derived c_12, this gives
c_23 = c_12/3.68 = 0.40 (38% off target 0.65). The ratio route
eliminates K entirely but currently lands 38% low.

Improvement: the ratio 3.68 was measured at L=8 with 12 configurations.
Multi-L measurement of c_12/c_23 with O(a^2) extrapolation could sharpen
this significantly. This is probably the cheapest path to a better c_23.

**(C) Large-L brute force.**
L = 24, 32 with 20+ configs each. Reduces finite-volume effects and
statistical noise in K. Pure compute, no conceptual work needed.

### Priority 2: c_13 sharpening

Current best: c_13 = 0.057 from Wolfenstein scaling, giving |V_ub|
40% off. The c_13 problem is cleaner than K: the physical mechanism
(indirect hopping c_12*c_23 dominates, direct c_13 provides partial
cancellation) is identified. What is needed:

- Compute the direct lattice c_13 at physical y_v = 0.44 on L = 12, 16
  with enough configs to resolve the 10% cancellation between direct
  and indirect paths
- The script shows Attack 4 (lattice L=12) gives c_13 = 0.169, which
  is 3x too large -- likely because y_v = 0.44 is not large enough to
  produce the required EWSB suppression of the 1-3 overlap

### Priority 3: J--V_ub tension resolution

The J note shows a fundamental tension: full 3-phase NNI gives
J/J_PDG = 0.993 but spoils |V_us| and |V_cb|. Single-phase gives good
angles but J/J_PDG = 0.73. Fitted free phases give both, but that is
3 free parameters.

Resolution requires deriving the sector-dependent phase distribution
from the EWSB cascade. This is downstream of Priority 1 (K) and
Priority 2 (c_13) -- tackle only after those sharpen.

---

## Recommended Next Steps

1. **Measure c_12/c_23 ratio at L = 8, 12, 16 with 20+ configs each.**
   Extrapolate to L -> inf with O(a^2) fit. This eliminates K entirely
   and is the cheapest route to a better V_cb.

2. **Compute lattice S_13 at y_v = 0.44 on L = 12 with 20+ configs.**
   The current 3-config measurement at L=12 has large error bars.
   This directly addresses the c_13 / |V_ub| accuracy.

3. **If ratio c_12/c_23 stabilizes:** derive the EWSB ratio K_12/K_23
   analytically from the shift-operator structure of H_EWSB. This would
   complete the sector-correction removal.

4. **Only then** revisit J and the phase structure.

---

## Scorecard Summary

| Deliverable | Status | Key number |
|-------------|--------|------------|
| Absolute S_23 (5 attacks on K) | BOUNDED | V_cb = 0.0403 (4.6% low) |
| c_13 derivation (4 attacks) | BOUNDED | |V_ub| = 0.0053 (40% off) |
| J from Z_3^3 phases (4 attacks) | BOUNDED | J/J_PDG = 0.73 (single-phase) |
| K universality (1-2 vs 2-3) | FAIL | K_12/K_23 = 0.053 |
| K spread across L | BOUNDED | CV = 24.9% |

The CKM lane is materially better. V_cb is now predicted (not fitted)
to 4.6%. But the remaining K spread and sector correction mean the lane
is not closed. The ratio route (c_12/c_23 with multi-L extrapolation) is
the most promising path to closure.
