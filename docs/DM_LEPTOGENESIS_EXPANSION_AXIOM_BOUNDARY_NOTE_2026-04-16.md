# DM Leptogenesis Expansion Axiom Boundary

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_expansion_axiom_boundary.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/frontier_dm_leptogenesis_expansion_axiom_boundary.py` exits 0 with PASS in the current cache; the prior audit verdict citing a nonzero exit was generated against a stale cache and is invalidated by this source-note hash drift. The runner output and pass/fail semantics are otherwise unchanged.

## Result

After closing:

- the exact source package
- the exact transfer coefficients
- the exact projection law
- the exact coherent kernel
- the exact equilibrium conversion factors
- the exact direct transport integral

the single remaining non-axiom object is now:

- `H_rad(T)`

equivalently:

- the normalized expansion profile `E_H(z)` together with its normalization at
  `z = 1`

This is sharper than the older boundary

- `T_rad(K) = 7.04 * C_sph * d_th * kappa_fit(K)`

because the bookkeeping factors and the fit are no longer part of the
authority path.

## Why the boundary remains

The current branch still does not carry a strict theorem-grade radiation-era
expansion law from `Cl(3)` on `Z^3` alone. The older `H(T)` lane still uses a
bounded `k = 0` sub-assumption, so full theorem closure cannot yet be claimed.

Given `H_rad(T)`, however, the refreshed branch now fixes `eta` uniquely.
