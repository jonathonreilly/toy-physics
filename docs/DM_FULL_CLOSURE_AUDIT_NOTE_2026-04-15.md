# DM Full Closure Audit

**Date:** 2026-04-15
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_full_closure_audit.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Audit conclusion

The refreshed branch now has:

- theorem-native exact source amplitudes
- theorem-native exact transfer coefficients
- theorem-native exact denominator/projection law
- theorem-native exact coherent leptogenesis kernel

The final authority runner no longer relies on the old reduced-DM inputs
(`texture_factor`, `doublet_CP`) and no longer hides the remaining benchmark
dependence.

## Final result

The current branch does **not** yet satisfy `FULL THEOREM CLOSURE`.

It lands at

- `FINAL EXACT BOUNDARY`

with exactly one remaining non-axiom ingredient named explicitly:

- `T_rad(K) = 7.04 * C_sph * d_th * kappa_fit(K)`

That is the last remaining closure object on the refreshed latest-`main`
branch.
