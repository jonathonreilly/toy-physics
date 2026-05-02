# YT Flat-Toron Thermodynamic Washout Note

**Date:** 2026-05-01  
**Status:** exact-support / flat toron thermodynamic washout  
**Runner:** `scripts/frontier_yt_flat_toron_thermodynamic_washout.py`  
**Certificate:** `outputs/yt_flat_toron_thermodynamic_washout_2026-05-01.json`

## Purpose

The flat-toron obstruction showed that finite-volume scalar denominator
proxies change across action-degenerate constant Cartan sectors.  This note
checks the constructive thermodynamic limit: for a fixed physical holonomy
`phi`, the constant link angle is `theta = phi / N`.

## Theorem

For `m > 0` and fixed holonomy `phi`,

```text
N^-4 sum_k f(k + phi/N) -> integral_BZ f(k) dk / (2 pi)^4
N^-4 sum_k f(k)         -> integral_BZ f(k) dk / (2 pi)^4
```

with

```text
f(k) = 1 / (m^2 + sum_i sin(k_i)^2)^2.
```

The integrand is continuous and periodic because `m > 0`, so shifted uniform
Riemann sums converge to the same Brillouin-zone integral.

## Runner Result

```text
python3 scripts/frontier_yt_flat_toron_thermodynamic_washout.py
# SUMMARY: PASS=6 FAIL=0
```

The runner verifies the theorem prerequisites and checks that fixed-holonomy
finite-volume shifts decay rapidly from `N=8` to `N=24`; for `N >= 20`, the
maximum relative shift in both the bubble and inverse-denominator proxy is
below `1e-4` on the scan.

## Claim Boundary

This is positive support, not retained closure.  It retires the flat-toron
finite-volume ambiguity for the local massive scalar bubble in the
thermodynamic limit.  It does not derive the interacting scalar pole
denominator, the massless gauge zero-mode / IR prescription, the LSZ derivative
at the pole, finite-`N_c=3` continuum control, or production FH/LSZ evidence.
