# Top-Yukawa Direct Measurement Scale Requirements Note

**Date:** 2026-05-01  
**Status:** scale requirement / direct measurement route open  
**Runner:** `scripts/frontier_yt_direct_measurement_scale_requirements.py`  
**Certificate:** `outputs/yt_direct_measurement_scale_requirements_2026-05-01.json`

## Purpose

The retained-closure certificate leaves direct physical measurement as the
cleanest route that bypasses the Ward/H-unit readout trap.  This note computes
what that route actually requires after the pilot mass-bracket exposed the
current-scale cutoff obstruction.

## Current Scale

The mass-bracket certificate uses

```text
1 lattice mass unit = 2.119291769496 GeV.
```

At that scale, the physical top mass corresponds to

```text
am_t = 172.56 / 2.119291769496 = 81.423428.
```

That is not a useful relativistic staggered-correlator target at the current
scale.

## Required Refinement

| Target `am_t` | Required `a^-1` | Required `a` | Refinement vs current |
|---:|---:|---:|---:|
| `1.0` | `172.56 GeV` | `0.00114362 fm` | `81.423x` |
| `0.5` | `345.12 GeV` | `0.00057181 fm` | `162.847x` |
| `0.25` | `690.24 GeV` | `0.00028590 fm` | `325.694x` |

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_direct_measurement_scale_requirements.py
# SUMMARY: PASS=7 FAIL=0
```

## Consequence

Production compute at the current Sommer-scale anchor would mainly certify the
same cutoff obstruction.  Retained direct-measurement closure needs one of:

1. a fine-scale campaign with an inverse lattice spacing of order
   `172 GeV` or higher;
2. a retained heavy-quark/top-integrated effective correlator and matching
   theorem;
3. a different physical observable that determines the top Yukawa without
   resolving a relativistic top at the current lattice spacing.

This is an execution requirement, not a new physics premise.
