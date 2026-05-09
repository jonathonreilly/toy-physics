# DM Leptogenesis Washout / Thermal Axiom Boundary

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-15
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_washout_axiom_boundary.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/frontier_dm_leptogenesis_washout_axiom_boundary.py` exits 0 with PASS in the current cache; the prior audit verdict citing a nonzero exit was generated against a stale cache and is invalidated by this source-note hash drift. The runner output and pass/fail semantics are otherwise unchanged.

## Result

The projection theorem forces the physically consistent effective mass to use
the same exact denominator channel:

- `(Y^dag Y)11 = K00 = 2`
- `m_tilde = K00 * y0^2 * v^2 / M1`

So the consistent sharp-branch value is

- `m_tilde = 0.10116572813579411 eV`

not the older intermediate benchmark value

- `m_tilde_old = 0.050582864067897054 eV`.

## Consequence on the retained benchmark transport map

Using the same retained transport benchmark class

- `m_*`
- `d_th`
- `kappa_fit(K) = (0.3/K)(ln K)^0.6`

with the now-consistent `m_tilde`, one gets

- `K = 47.23597962989828`
- `kappa_fit = 0.01427162724743994`
- `eta / eta_obs = 0.557919848420251`

and even the Davidson-Ibarra ceiling on that same retained map gives only

- `eta_DI / eta_obs = 0.6014524207443263`.

So the old `0.9907` exact-kernel benchmark was an intermediate benchmark
closure, not the final physically consistent authority once `/K00` is enforced
everywhere it belongs.

## Boundary

The remaining non-axiom object can now be named exactly as one map:

- `T_rad(K) = 7.04 * C_sph * d_th * kappa_fit(K)`

Everything before that map is theorem-native on the branch.

To hit observation from the consistent retained benchmark would require

- `T_rad / T_rad,bench = 1.7923721531533574`.

So the source/kernel side is no longer the blocker. The remaining blocker is
the radiation transport map.
