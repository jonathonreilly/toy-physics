# DM Lane: Nucleation Finding — Detonation Regime

**Status:** BOUNDED (important finding)  
**Date:** 2026-04-13  
**Script:** frontier_dm_nucleation.py

## Finding

The bounce equation computation gives:
- T_c = 222.6 GeV (Daisy-resummed CW potential)
- T_n = 200.5 GeV (where S_3/T crosses 140)
- **T_n/T_c = 0.90** — significantly more supercooling than previously estimated

## The Problem

At T_n/T_c = 0.90, the driving pressure DeltaV/T^4 is too large for the
Boltzmann friction to balance. The force balance equation:

    eta(v_w) * v_w = DeltaV / T^4

has no solution below v_J (the Jouguet velocity). The wall velocity is
pushed into the **detonation regime** (v_w > c_s).

This is a problem for baryogenesis because:
1. Detonation walls create a rarefaction wave behind the wall, not a
   compression wave in front
2. The diffusion-transport mechanism for baryogenesis requires subsonic
   (deflagration) walls where CP-violating currents diffuse ahead of the wall
3. With detonation, the transport prefactor P = D_q*T / (v_w * L_w*T) is
   suppressed by the large v_w

## Possible Resolutions

1. **The m_s = 120 GeV taste scalar may not be the right mass.**
   At m_s = 200 GeV, the nucleation is weaker:
   T_n/T_c ~ 0.90 but DeltaV/T^4 ~ 1.6 (much smaller), giving
   v_w ~ 0.01 (subsonic, deflagration). The framework does NOT
   uniquely predict m_s.

2. **The high-T expansion may overestimate the barrier.**
   The 1-loop Daisy resummation at T_n/T_c = 0.90 may not be
   reliable. Full 3D lattice simulations of the phase transition
   are needed.

3. **The friction computation may underestimate the drag.**
   The Boltzmann friction uses linearized transport coefficients.
   At large v_w, non-linear effects (particle-production backreaction)
   can increase friction substantially.

4. **The nucleation criterion S_3/T = 140 may be too aggressive.**
   Using S_3/T = 160 would give T_n closer to T_c and less supercooling.

## Impact on DM Lane

This finding does NOT invalidate the DM relic ratio derivation, because:
- R = Omega_DM / Omega_b depends on eta (baryon asymmetry) not on v_w directly
- eta depends on the EWPT strength v(T_c)/T_c (still derived ≥ 0.52)
  and on the transport coefficients

But it DOES highlight that the transport sector has a genuine dynamical
issue that the previous v_w range [0.006, 0.048] did not capture.

## Honest Status

The DM lane transport sector is now NARROWED but the v_w determination
requires either:
- A different taste scalar mass (m_s ~ 200 GeV region where deflagration holds)
- Full 3D lattice simulation of the phase transition
- Non-linear friction computation

The lane remains BOUNDED on the transport side.
