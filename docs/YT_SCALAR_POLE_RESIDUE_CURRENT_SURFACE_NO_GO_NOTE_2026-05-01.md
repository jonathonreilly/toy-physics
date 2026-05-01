# Top-Yukawa Scalar Pole-Residue Current-Surface No-Go

**Date:** 2026-05-01  
**Status:** exact negative boundary / closure unavailable on the current
analytic surface  
**Runner:** `scripts/frontier_yt_scalar_pole_residue_current_surface_no_go.py`  
**Certificate:** `outputs/yt_scalar_pole_residue_current_surface_no_go_2026-05-01.json`

## Purpose

The Ward physical-readout repair narrowed the analytic blocker to scalar pole
residue and common scalar/gauge dressing.  This note checks whether that
remaining normalization can be derived from the current retained algebraic
surface alone.

It cannot.

## Current Surface Held Fixed

The runner holds fixed the data that the current Ward repair actually has:

| Quantity | Value |
|---|---:|
| `N_c` | `3` |
| `N_iso` | `2` |
| source coefficient | `1/sqrt(6)` |
| color channel ratio | `R_conn = 8/9` |
| SSB identity | `sqrt(2) m / v` returns the canonical doublet coefficient |
| one-Higgs selector | `Qbar_L H_tilde u_R` |

Then it varies only the scalar pole residue and the relative scalar/gauge
dressing.  Those are exactly the missing theorem data.

## Countermodel Result

All models have the same visible current-surface signature, but they produce
different physical `y_t/g_s` readouts:

| Model | Physical `y/g` |
|---|---:|
| unit residue, common dressing | `0.408248290463863` |
| `R_conn` residue, common dressing | `0.384900179459751` |
| half residue, common dressing | `0.288675134594813` |
| unit residue, non-common dressing | `0.367423461417477` |
| `R_conn` residue, non-common dressing | `0.445673892006027` |

Therefore the current algebraic surface is underdetermined for the physical
Yukawa readout.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_pole_residue_current_surface_no_go.py
# SUMMARY: PASS=7 FAIL=0
```

## Closure Consequence

PR #230 cannot reach retained top-Yukawa closure by repairing the old Ward
wording alone.  One of the following must be supplied:

1. a retained scalar two-point pole-residue theorem deriving `Z_phi` for the
   source-selected scalar;
2. a retained common-dressing theorem equating or deriving the scalar/gauge
   dressing ratio;
3. direct physical measurement evidence from the strict lattice-correlator
   route.

Without one of those, setting the scalar pole residue or common dressing is an
extra normalization choice.

## Non-Claims

- This note does not deny the tree-level `1/sqrt(6)` source coefficient.
- This note does not deny the `R_conn = 8/9` channel arithmetic.
- This note does not promote the Ward theorem.
- This note does not use observed top mass or observed Yukawa values.
