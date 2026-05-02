# YT Flat-Toron Scalar-Denominator Obstruction Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / flat toron scalar-denominator obstruction  
**Runner:** `scripts/frontier_yt_flat_toron_scalar_denominator_obstruction.py`  
**Certificate:** `outputs/yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json`

## Purpose

The prior zero-mode blocks showed that the scalar ladder denominator depends
on a gauge-zero-mode / IR / finite-volume prescription, and that the repo does
not currently hide such a prescription.

This block checks whether the compact lattice gauge action itself selects the
trivial zero mode.

## Result

It does not.  Constant commuting Cartan links,

```text
U_mu = diag(exp(i theta), exp(-i theta), 1),
```

have identity plaquettes and therefore zero plaquette action, but they carry
different Polyakov phases.  Charged fermion momenta are shifted in these flat
sectors, so the scalar-source bubble proxy changes while the plaquette action
does not.

## Runner Result

```text
python3 scripts/frontier_yt_flat_toron_scalar_denominator_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```

The runner verifies:

- all tested constant Cartan sectors have zero plaquette action;
- their Polyakov traces differ from the trivial sector;
- the scalar bubble and inverse-bubble denominator proxies change across those
  flat sectors;
- selecting the trivial toron is therefore an extra prescription unless a
  theorem derives it.

## Claim Boundary

This is not retained closure.  It does not determine `kappa_s`, a pole
residue, or a physical `y_t`.  It only blocks a possible shortcut: treating
the trivial gauge zero mode as automatically selected by the lattice action.

The next analytic theorem must say whether flat Cartan sectors are fixed,
averaged, or suppressed in the scalar-channel denominator, then prove pole and
inverse-propagator derivative convergence in that selected prescription.
