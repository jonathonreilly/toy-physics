# 3D Dense Spent-Delay Refinement Reconciliation

**Date:** 2026-04-04  
**Status:** proposed_retained negative refinement reconciliation for the ordered 3D dense spent-delay family

## Purpose

This note freezes the corrected refinement comparison for the retained 3D dense
spent-delay family.

The question is narrow:

- compare `h = 1.0` vs `h = 0.5`
- keep the same ordered 3D family
- keep the same spent-delay action
- correct the physical mass-position mapping
- keep the same gravity-observable hierarchy
- keep the distance-law companion honest

The key correction is physical indexing:

- positions and slit coordinates are mapped by `round(coord / h)`
- the physical connectivity range stays fixed at `3.0` units
- therefore `span = 3` at `h = 1.0` and `span = 6` at `h = 0.5`

## Fixed family and harness

- graph family: ordered 3D lattice
- action: original spent-delay
- field strength: `5e-5`
- geometry: `L = 12`, `W = 6`
- retained barrier geometry: close-slit three-opening barrier on one layer
- mass positions: `z = 2, 3, 4, 5, 6` physical units
- distance companion: no-barrier propagation on the same family

Primary artifact chain:

- [`scripts/lattice_3d_dense_refinement_reconciliation.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_dense_refinement_reconciliation.py)
- [`logs/2026-04-04-lattice-3d-dense-refinement-reconciliation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-dense-refinement-reconciliation.txt)

## Comparison result

| `h` | span | barrier read | distance fit | hierarchy-aligned distance rows |
|---|---:|---|---|---:|
| `1.0` | `3` | MIXED | `b^(-0.94)`, `R² = 0.934` | `5/5` |
| `0.5` | `6` | MIXED | `n/a` | `0/5` |

Barrier-card summary at `mass_z = 6`:

| `h` | Born | `k=0` | MI | `d_TV` | decoherence | centroid | `P_near` | bias |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `1.0` | `4.95e-16` | `0` | `0.024` | `0.152` | `2.9%` | `-0.016759` | `+0.000533` | `-0.534936` |
| `0.5` | `2.54e-15` | `0` | `0.040` | `0.485` | `48.0%` | `+0.020256` | `-0.002062` | `+0.042266` |

Distance companion summary:

- `h = 1.0`: all tested `z` values are hierarchy-aligned attractive rows
- `h = 0.5`: no tested `z` value is hierarchy-aligned attractive

## Verdict

The older `h = 0.5` positive-refinement narrative does **not** survive the
corrected comparison.

What fails is the refinement claim, not the existence of the 3D dense branch
itself:

- the retained 3D dense spent-delay family still exists as a bounded branch
- but the corrected `h = 0.5` comparison does not preserve the earlier
  positive-refinement story
- the no-barrier distance companion loses positive hierarchy-aligned rows
  entirely at `h = 0.5`

So the safe read is:

- **3D dense spent-delay remains a bounded companion branch**
- **the older `h = 0.5` refinement-positive story fails under corrected
  physical mapping**

## What is retained

- the 3D dense spent-delay family remains canonical at `h = 1.0`
- the same-family barrier card still has a bounded companion read
- the corrected hierarchy makes the failure of the refinement story explicit

## What is not retained

- not a refinement theorem
- not a continuum theorem
- not a claim that the `h = 0.5` refinement point preserves the older
  positive narrative
- not a broader result about 4D or action-power

## Program read

This reconciliation is an important cleanup for the ordered-lattice branch:

- it keeps the 3D dense spent-delay card honest
- it prevents the older `h = 0.5` narrative from being overread
- it leaves the flagship ordering unchanged

The project ranking does not change:

- **mirror remains the flagship**
- **ordered lattice remains the secondary branch**
- **NN refinement remains the continuum-side bridge**

## Cited authority notes

The runner imports `BETA`, `K`, `LAM`, and `N_YBINS` action-normalization
constants from `scripts/action_power_canonical_harness.py`. The
authoritative source note for those harness choices is:

- [`ACTION_POWER_NOTE.md`](ACTION_POWER_NOTE.md).

This note's gravity-observable hierarchy reads through that canonical
harness; the bounded read above does not introduce new normalization choices.
