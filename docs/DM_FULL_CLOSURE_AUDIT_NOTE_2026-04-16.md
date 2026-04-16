# DM Full Closure Audit

**Date:** 2026-04-16
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_full_closure_audit.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Audit result

The refreshed branch now has theorem-native closure for:

- exact source amplitudes
- exact transfer coefficients
- exact denominator/projection law
- exact coherent leptogenesis kernel
- exact equilibrium conversion factors
- exact direct transport integral

The final authority runner no longer depends silently on:

- `texture_factor`
- `doublet_CP`
- `kappa_fit`
- `d_th`
- `7.04`

## Final status

The branch still lands at

- `FINAL EXACT BOUNDARY`

with exactly one remaining non-axiom ingredient:

- `H_rad(T)`

That is now the last remaining closure object on the refreshed latest-`main`
DM branch.
