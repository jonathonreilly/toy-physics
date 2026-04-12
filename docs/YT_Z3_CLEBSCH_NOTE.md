# Top Yukawa from Z_3 Clebsch-Gordan Coefficients

**Script:** `scripts/frontier_yt_z3_clebsch.py`
**Date:** 2026-04-12
**Status:** 12/12 tests PASS

## Derivation chain

1. **Z_3 generation symmetry.** The cyclic permutation of d=3 spatial axes on
   the staggered lattice assigns eigenvalues {1, omega, omega^2} to three
   fermion generations, with Z_3 charges {0, 1, 2}.

2. **Higgs Z_3 charge.** The Coleman-Weinberg Higgs emerges from the taste
   pseudoscalar channel (Gamma = gamma_5 * xi_5). Since xi_5 = xi_1*xi_2*xi_3
   is invariant under cyclic permutation, the Higgs carries charge q_H = 0
   (Z_3 singlet).

3. **Left-right charge conjugation.** Left-handed fermions (T_1 orbit,
   Hamming weight 1) carry charges {0, 1, 2}. Right-handed fermions (T_2
   orbit, Hamming weight 2) carry the conjugate charges {0, 2, 1}. The
   Yukawa vertex requires q_L(i) + q_R(j) + q_H = 0 mod 3.

4. **Diagonal texture.** With conjugate R charges and q_H = 0, the selection
   rule allows ONLY diagonal entries: Y_11, Y_22, Y_33. All off-diagonal
   entries are Z_3-forbidden.

5. **CG coefficients.** Z_3 is abelian, so every Clebsch-Gordan coefficient
   for the allowed channels equals 1. The Yukawa matrix at the Planck scale
   is Y = g_0 * I_3 (universal, degenerate).

6. **Z_3 breaking.** Lattice anisotropy lifts the degeneracy by
   epsilon ~ 0.04 (from the neutrino mass ratio fit). First-order breaking
   gives Y_1 > Y_2 = Y_3; second-order (with a phase from higher taste
   corrections) splits all three.

7. **RG amplification.** Over 17 decades of running (M_Planck -> M_Z), the
   positive y^3 feedback in the Yukawa beta function exponentially amplifies
   the initial splitting. The largest Yukawa is attracted to the
   Pendleton-Ross infrared quasi-fixed point.

8. **Prediction.** At the 2-loop corrected Pendleton-Ross fixed point:
   y_t = 1.035, m_t = 180 GeV (4.2% above observed 173 GeV). The smaller
   Yukawas (charm, up) remain far below the fixed point, explaining
   m_t >> m_c >> m_u.

## Key result

| Quantity | Predicted | Observed | Deviation |
|----------|-----------|----------|-----------|
| y_t      | 1.035     | 0.994    | 4.2%      |
| m_t      | 180 GeV   | 173 GeV  | 4.2%      |

## What the CG coefficients determine

- **Texture:** which Yukawa entries are zero (off-diagonal forbidden)
- **Universality:** all allowed entries equal at tree level (CG = 1)
- **Mechanism:** Z_3-degenerate Yukawa + small breaking + RG amplification
  = one heavy generation at the IRFP
- **Not determined by CG alone:** the absolute scale g_0 (but this cancels
  in the IRFP prediction)

## Cross-checks

- Same Z_3 structure governs the Majorana mass matrix in the neutrino
  sector (M_R = [[A,0,0],[0,0,B],[0,B,0]]), predicting normal hierarchy.
- Same breaking parameter epsilon ~ 0.04 from the neutrino mass ratio fit.
- The diagonal Yukawa texture is consistent with the small observed CKM
  mixing angles (mixing arises from Z_3 breaking corrections).

## Limitations

- The 2-loop correction factor (0.82) is approximate; a full 2-loop RGE
  with threshold matching would refine the prediction.
- The charm/up mass hierarchy requires higher-order Z_3 breaking or
  non-perturbative lattice effects near the Planck scale that are not
  captured by the simple cosine parametrization.
- The down-type and lepton Yukawa base coupling g_0^d is a separate
  parameter not fixed by the up-type analysis alone.
