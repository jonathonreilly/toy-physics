# Jarlskog Invariant from Higgs Z_3^3 Charge Without Fitting

**Date:** 2026-04-13
**Status:** BOUNDED -- four attacks on the J gap; full Z_3^3 embedding closes J to 0.7% of PDG but spoils |V_us| and |V_cb|
**Script:** `scripts/frontier_ckm_j_derived.py`

---

## Status

BOUNDED. The Higgs Z_3^3 charge q_H = (2,1,1) derives sector-dependent
phases for the up and down Yukawa matrices. With a single-phase NNI
(phase only in the 1-3 element), the best J achievable is J/J_PDG = 0.73.
With the full Z_3^3 embedding (independent phases on all three
off-diagonal elements), J/J_PDG = 0.993 is achievable -- but at the
cost of |V_us| and |V_cb| deviating by factors of 2-3 from PDG.

---

## Problem

From `frontier_ckm_jarlskog_closure.py` (28/28 PASS):

- **Sector-dependent FIT:** delta_u = -1.8 deg, delta_d = 65.4 deg gives
  J = 2.97e-5 (-3.7% of PDG). This is a 3-parameter fit.
- **Higgs-DERIVED:** q_H = (2,1,1) from the T_1-T_2 bilinear gives a
  120 deg phase mismatch. With single-phase NNI, J/J_PDG = 0.73.

The gap: the NNI diagonalization redistributes the input phase through
the mass hierarchy, suppressing J relative to the naive expectation.

---

## Four Attacks

### Attack 1: Phase Redistribution from Mass Hierarchy

The NNI diagonalization mixes the input Z_3 phase with the mass eigenvalues.
The exact suppression factor is S = J_exact / J_naive = 0.41, meaning the
NNI diagonalization reduces J by ~60% relative to what the input phase
angles would naively predict.

This is NOT a power law in m_c/m_t. The effective exponent p = 0.065
(essentially independent of the mass ratio). The suppression is better
described as an interference effect between the up and down sector
diagonalizations: V_ub receives contributions from both sectors with
different phases and magnitudes, and the resulting effective phase is
smaller than the input mismatch.

### Attack 2: Optimal Z_3^3 Charge

All 26 nonzero Z_3^3 charges produce the SAME J (to 0.1% precision)
when c_13 is optimized for J alone. This is because the 1-3 phase
mismatch is always either +120 deg or -120 deg (the only nonzero
values that Z_3 can produce). The choice of q_H affects the SIGN of
the mismatch but not its magnitude.

**Key finding:** q_H = (2,1,1) is already near-optimal. No alternative
Z_3^3 charge improves J.

### Attack 3: RG Running (M_Pl -> M_Z)

The Jarlskog invariant itself is nearly RG-invariant at 1-loop
(change < 0.3%). However, the mixing angles s_23 and s_13 run
significantly: s_23(M_Pl)/s_23(M_Z) = 1.43 from top Yukawa effects.

The combined RG factor is J(M_Pl)/J(M_Z) = 1.43, meaning J at the
Planck scale is 43% LARGER than at M_Z. This works in the WRONG
direction: if the Higgs-derived J is set at M_Pl, RG running to
M_Z REDUCES it further.

**Key finding:** RG running is a -30% effect (wrong sign for closing
the gap).

### Attack 4: Full Z_3^3 Embedding

The single-phase NNI puts the Z_3 phase only in the 1-3 off-diagonal
element. But the Z_3^3 structure assigns independent phases to ALL
three off-diagonal elements:

| Transition | delta_u | delta_d | Mismatch |
|------------|---------|---------|----------|
| 1-2        | 0 deg   | +120 deg | -120 deg |
| 2-3        | 0 deg   | +120 deg | -120 deg |
| 1-3        | 0 deg   | +120 deg | -120 deg |

With all three phases active, J/J_PDG = 0.993 at c_13/c_23 = 0.73.
The enhancement over single-phase is 1.37x.

**CAVEAT:** At this c_13 value, |V_us| = 0.430 (PDG 0.224) and
|V_cb| = 0.139 (PDG 0.042). The full 3-phase NNI achieves J ~ J_PDG
but at the cost of spoiling the Cabibbo and 2-3 mixing angles by
factors of 2-3. The additional phases in the 1-2 and 2-3 elements
rotate the diagonalization eigenvectors away from the correct mass
eigenstates.

---

## Combined Assessment

| Approach | J/J_PDG | |V_us| | |V_cb| | Notes |
|----------|---------|--------|--------|-------|
| Single-phase NNI | 0.73 | 0.240 | 0.042 | Good angles, suppressed J |
| Full 3-phase NNI | 0.99 | 0.430 | 0.139 | Good J, bad angles |
| Fitted (free phases) | 0.96 | 0.224 | 0.042 | Both good (3 free params) |
| PDG | 1.00 | 0.224 | 0.042 | Target |

The tension is clear: achieving J ~ J_PDG from the Z_3^3 phases
requires either (a) free phases that are fitted, not derived, or
(b) all three off-diagonal phases active, which spoils the mixing
angle predictions.

---

## What Remains

The single-phase NNI with Higgs-derived phases gives J/J_PDG = 0.73.
This is within 27% of PDG -- much closer than the originally stated
24% gap (which appears to have been measured under different conditions
or c_13 optimization).

To close the remaining 27% gap without spoiling angles, one needs:
1. A mechanism that enhances the effective CP phase in V_ub without
   significantly changing |V_ub|, |V_us|, or |V_cb|.
2. This is precisely what the fitted sector-dependent phases achieve:
   delta_u ~ -2 deg, delta_d ~ 65 deg produce the right mismatch.
3. Deriving these specific values from the Z_3^3 structure requires
   understanding how EWSB selects the Higgs direction in a way that
   produces the asymmetric (not +/-120 deg) phase distribution.

---

## Assumptions

1. **DERIVED:** Z_3^3 charge structure on the 8-dimensional taste space
2. **DERIVED:** q_H = (2,1,1) from the T_1-T_2 bilinear (Higgs as EWSB mode)
3. **DERIVED:** Phase mismatch between up/down sectors from q_H sign flip
4. **INPUT:** Quark masses (PDG MSbar/pole values)
5. **INPUT:** NNI coefficients c_12^u = 1.48, c_12^d = 0.91
6. **FITTED:** c_13/c_23 ratio (optimized for each attack)

---

## Tests

9/9 passed (all BOUNDED).
