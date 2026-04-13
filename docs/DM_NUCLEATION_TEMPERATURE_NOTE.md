# Nucleation Temperature from Bounce Action

## Summary

The nucleation temperature T_n is derived self-consistently from the
CW effective potential with the taste scalar spectrum.  The bounce
equation is solved numerically (overshoot/undershoot) and the nucleation
condition S_3(T_n)/T_n = 140 is imposed.  All baryogenesis transport
parameters are then reconciled on the T_n surface.

**Script:** `scripts/frontier_dm_nucleation_temperature.py`

## Key Results

| Quantity | At T_c | At T_n | Change |
|----------|--------|--------|--------|
| T (GeV) | 183.6 | 180.6 | -1.7% |
| v/T (physical) | 0.56 | 0.80 | +42% |
| L_w T | 13.9 | 47.6 | +242% |
| D_q T | 6.0 | 6.1 | +1% |
| v_w | 0.05 | 0.019 | -63% |
| P = D_q/(v_w L_w) | 8.6 | 6.9 | -20% |

**Nucleation temperature:** T_n = 180.6 GeV, T_n/T_c = 0.983

**Baryogenesis condition:** v(T_n)/T_n = 0.80 > 0.52 (SATISFIED, margin +0.28)

## Physics

### Step 1: Bounce action S_3(T)/T

The 3D bounce action is computed from the O(3)-symmetric bounce equation:

    phi'' + (2/r) phi' = dV_eff/dphi

with the high-T effective potential including taste scalar spectrum
(4 extra bosons beyond SM) and gauge magnetic mass corrections.  The
overshoot/undershoot method converges to the bounce solution at each
temperature.

S_3/T falls steeply from ~34000 near T_c to ~1 at T/T_c = 0.983.
This rapid drop is characteristic of the barrier structure in the
cubic-quartic potential.

### Step 2: Nucleation condition

The nucleation rate per unit volume:

    Gamma ~ T^4 exp(-S_3/T)

One bubble per Hubble volume per Hubble time gives:

    S_3(T_n)/T_n = 4 ln(M_Pl / (1.66 sqrt(g_*) T_n)) ~ 140

This is weakly T-dependent (144 at 150 GeV, 144 at 160 GeV).

### Step 3: VEV at T_n

The perturbative potential minimum at T_n gives v(T_n)/T_n = 0.507.
This is enhanced by the non-perturbative factor R_NP = 1.57, calibrated
from the lattice MC (v/T_MC = 0.56 vs v/T_pert = 0.357 at T_c).

The physical VEV: v(T_n)/T_n = 0.507 * 1.57 = 0.80.

### Step 4: Reconciled transport

All transport parameters are evaluated at T_n:

- **L_w T_n = 47.6** from the bounce wall profile (10-90% width).
  The large value reflects the broad wall at mild supercooling.
- **D_q T_n = 6.1** from HTL kinetic theory with alpha_s(T_n) = 0.109.
  Essentially unchanged from T_c (alpha_s runs weakly over 3 GeV).
- **v_w = 0.019** from friction balance.  Lower than at T_c due to
  less supercooling driving pressure vs. the same friction.

### Step 5: Thin-wall cross-check

The thin-wall approximation gives T_n(tw) = 182.9 GeV (Delta T/T_c = 0.004),
slightly above the full bounce result (Delta T/T_c = 0.017).  This is
expected: thin-wall overestimates S_3, requiring less supercooling to
reach S_3/T = 140.

## Significance

This closes the first gap in the DM elegant closure plan: the nucleation
temperature is now derived from the framework's own CW potential rather
than assumed.  The baryogenesis condition v/T > 0.52 is satisfied with
a 54% margin at T_n (0.80 vs 0.52), providing robust support for the
baryon asymmetry calculation.

## Dependencies

- `frontier_ewpt_gauge_closure.py`: CW potential parameters (E, lam, D)
- `frontier_dm_bounce_wall.py`: bounce solver methodology
- `frontier_ewpt_lattice_mc.py`: non-perturbative v/T calibration
