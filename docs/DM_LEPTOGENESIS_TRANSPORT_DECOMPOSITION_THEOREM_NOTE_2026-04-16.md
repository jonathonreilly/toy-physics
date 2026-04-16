# DM Leptogenesis Transport-Decomposition Theorem

**Date:** 2026-04-16
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_transport_decomposition_theorem.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Result

The exact upstream leptogenesis package is now frozen on branch:

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`
- `K00 = 2`
- `epsilon_1 / epsilon_DI = 0.9276209209197268`

With those fixed, the baryon-to-photon ratio factors as

- `eta[H] = (s/n_gamma) * C_sph * d_N * epsilon_1 * kappa_axiom[H]`

where:

- `s/n_gamma` is a late equilibrium conversion factor
- `d_N = Y_{N1}^eq(0)` is the relativistic Majorana abundance factor
- `kappa_axiom[H]` is the direct transport functional

So the old `kappa_fit(K)` is no longer part of the authority path. It is
retained only as a benchmark comparator.

## Comparator status

The old physically consistent fit benchmark is preserved only diagnostically:

- legacy rounded bookkeeping: `eta/eta_obs = 0.557919848420251`
- same fit with exact bookkeeping: `eta/eta_obs = 0.557874966110017`

This confirms the fit is a comparator, not the theorem-native closure object.
