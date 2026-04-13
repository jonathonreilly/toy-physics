# DM Relic Density: Independence from Spatial Curvature k

**Script:** `scripts/frontier_dm_k_independence.py`
**Date:** 2026-04-13
**Status:** 9/9 PASS (4 EXACT, 5 DERIVED, 0 BOUNDED)

## Result

The DM relic density derivation does **not** depend on the assumption k=0 (spatial flatness). The curvature term k/a^2 in the Friedmann equation is negligible at freeze-out by ~29 orders of magnitude relative to the radiation energy density, for any k in {-1, 0, +1}.

This removes the "k=0 flatness" bounded assumption (check 11 in `frontier_dm_friedmann_from_newton.py`) from the DM derivation chain.

## Argument

The full first Friedmann equation:

    H^2 = (8piG/3) rho - k/a^2 + Lambda/3

At temperature T in the radiation era, the three terms scale as:

| Term | Scaling | Value at T=40 GeV | Ratio to H^2_rho |
|------|---------|-------------------|-------------------|
| (8piG/3)rho | T^4 / M_Pl^2 | 5.05e-30 GeV^2 | 1 |
| k/a^2 | H_0^2 Omega_k (T/T_0)^2 | 6.01e-59 GeV^2 | 1.2e-29 |
| Lambda/3 | H_0^2 | 2.07e-84 GeV^2 | 4.1e-55 |

The curvature-to-radiation ratio:

    R(T) = |Omega_k| / Omega_rad(g_*) * (T_0/T)^2

scales as T^{-2}: going backwards in time, radiation (rho ~ a^{-4}) grows faster than curvature (k/a^2 ~ a^{-2}). By freeze-out, curvature has been swamped by ~29 orders of magnitude.

## Numerical scan

| Epoch | T | R(T) |
|-------|---|------|
| Today | 2.35e-13 GeV | ~11 |
| Recombination | 0.26 eV | 9e-6 |
| BBN | 1 MeV | 1.9e-19 |
| DM freeze-out | 40 GeV | 1.2e-29 |
| EW scale | 246 GeV | 3.1e-31 |

## Sensitivity through freeze-out

The freeze-out equation Gamma = n_eq <sigma v> = H(T_F) depends on k only through H. With H^2 = H^2_rho (1 + R), the shift is:

- delta(H)/H = R/2 ~ 6e-30
- delta(x_F)/x_F ~ R/(2 x_F) ~ 2e-31
- delta(Omega h^2)/(Omega h^2) ~ 2e-31

Numerically confirmed: the iterative x_F solver returns identical values for k=0 and k=+1 to machine precision (the correction is below float64 resolution).

## Theorem

For k in {-1, 0, +1} and any freeze-out temperature T_F > 1 MeV:

    |Omega_DM(k) - Omega_DM(0)| / Omega_DM(0) < 10^{-20}

## Impact on DM chain

The bounded assumption list in `frontier_dm_friedmann_from_newton.py` (check 11) stated that "k=0 flatness" was required. This analysis shows it was never actually needed -- the curvature term is dynamically negligible at all temperatures relevant to DM freeze-out. The assumption may be removed from the bounded list for the DM lane.

Remaining bounded assumptions for the DM chain are unchanged (g_bare=1, Stosszahlansatz, second Friedmann equation not needed, etc.).
