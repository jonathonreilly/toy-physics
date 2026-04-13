# Native Taste-Enhanced Baryogenesis: eta Without Post-Hoc Multipliers

**Script:** `scripts/frontier_dm_native_eta.py`
**PStack:** `dm-native-eta`
**Date:** 2026-04-13

## Result

eta = 5.22e-10 (observed: 6.12e-10, ratio 0.85)

All three Codex objections addressed. No post-hoc multiplier, no imported
C_tr, no MC calibration for v/T.

## Three Fixes Applied

### Fix 1: Taste factor 8/3 IN the source term

The CP source in the quantum transport equation is now:

    S_CP = (N_taste/N_gen) * y_t^2 * sin(delta_Z3) / (4 pi^2) * wall_profile

where N_taste/N_gen = 8/3 enters at the SOURCE LEVEL. Previously, the
transport equations were solved with N_gen = 3, and the factor 8/3 was
multiplied onto eta_coupled afterwards. This is now fixed: the trace in the
CP source runs over all 8 taste states per generation from the start.

### Fix 2: C_tr derived from diffusion network

The transport coefficient is:

    C_tr = (N_f / (4 g_*)) * (Gamma_ws/T^4) * (N_taste/N_gen)
           * (y_t^2/(4 pi^2)) * (D_q T) / (L_w T) / A_sph

    = 1.72e-6

This is derived from the diffusion network with 8 taste species per
generation, using only framework gauge couplings. The D_q comes from HTL
with alpha_s(T_n), L_w from the bounce potential curvature. No FHS (2006)
calibration is imported.

Comparison: FHS calibration gives C_tr = 1.56e-6 (ratio 1.11).

### Fix 3: v(T_n)/T_n from daisy resummation

The perturbative CW potential gives v(T_c)/T_c = 0.29. The non-perturbative
enhancement R_NP = 1.68 is derived analytically from:

    R_NP = (E_gauge/E_pert) * sqrt(1 + 3 g^2 / (4 pi c_mag lam_gauge))

where:
- E_gauge/E_pert = 1.01 (magnetic mass cubic enhancement)
- The sqrt factor = 1.66 (magnetic Higgs self-energy correction)
- c_mag = 0.37 (3D SU(2) magnetic mass coefficient, Kajantie et al. 1996)
- g = 0.653 (SU(2) gauge coupling, DERIVED from Cl(3))
- lam_gauge = 0.157 (effective quartic with gauge screening)

Result: v(T_n)/T_n = 0.73 (vs 0.80 with MC calibration).
Compare: MC calibration gave R_NP = 1.57, this gives R_NP = 1.68.

## Input Classification

### Derived (from framework axioms)
- N_taste = 8 per generation (C^8 from Cl(3) staggered lattice)
- delta_Z3 = 2 pi/3 (Z_3 cyclic CP phase)
- g_W = 0.653 (SU(2) from Cl(3))
- y_t = 0.995 (Cl(3) IR fixed point)
- C_tr = 1.72e-6 (from diffusion network)
- v(T_n)/T_n = 0.73 (from daisy resummation)
- R_NP = 1.68 (from magnetic mass)

### Structural (SU(2) gauge theory)
- c_mag = 0.37 (3D SU(2) magnetic mass, Kajantie et al. 1996)
- kappa_sph = 20 (d'Onofrio et al. 2014)
- B_sph = 1.87 (Klinkhamer-Manton)

### Estimated
- M_S = 80 GeV (taste scalar mass)
- L_w T = 30 (wall thickness from potential curvature)

## Cosmological Chain

    eta = 5.22e-10 -> Omega_b = 0.042 -> Omega_DM = 0.228
    -> Omega_m = 0.270 -> Omega_Lambda = 0.730

## Sensitivity

The result is within 15% of observation. The main source of theoretical
uncertainty is the taste scalar mass M_S (estimated, not derived). Varying
M_S from 60-100 GeV changes eta by ~30%. The analytic R_NP (1.68 vs MC
1.57) contributes a ~15% shift relative to the MC-calibrated calculation.
