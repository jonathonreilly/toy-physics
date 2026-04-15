# Vacuum Critical Stability Companion

**Date:** 2026-04-15
**Status:** bounded companion prediction on `main`
**Primary runners:** `scripts/frontier_higgs_mass_full_3loop.py`,
`scripts/frontier_yt_color_projection_correction.py`
**Boundary-support runner:** `scripts/frontier_direct_yt_extraction.py`

## Authority Role

This note is the standalone authority for the bounded vacuum-critical-stability
readout extracted from the current Higgs / vacuum package.

It is separate from:

- the retained hierarchy / `v` lane
- the broader bounded Higgs / vacuum package note
- the Yukawa / top lane that still controls the quantitative bound

## Safe Statement

On the current accepted framework route, the high-scale Higgs boundary
condition is

`lambda(M_Pl) = 0`.

Combined with the current bounded framework-side Yukawa lane and the direct
full 3-loop Higgs/vacuum running now present on `main`, the electroweak vacuum
lands on the critical-stability side of the usual Standard Model metastability
comparison surface rather than deep in a metastable regime.

This remains a **bounded companion prediction**, not a retained flagship row,
because the numerical vacuum readout still inherits the bounded `y_t` / QFP
route.

## What Is Exact On The Current Surface

- the framework-native composite-Higgs / no-elementary-scalar boundary
  structure that gives the natural high-scale condition `lambda(M_Pl) = 0`
- the existence of a direct framework-side full 3-loop Higgs/vacuum runner on
  `main`

## What Is Still Bounded

- the quantitative vacuum readout still inherits the bounded Yukawa / top lane
- the package does not yet promote vacuum critical stability as an independent
  retained theorem separate from the bounded Higgs package

## Current Readout

- `m_H(2-loop support route) = 119.8 GeV`
- `m_H(full 3-loop framework-side route) = 125.3 GeV`
- current vacuum readout: critical / non-metastable side on the
  `lambda(M_Pl)=0` route
- comparator: the usual Standard Model observed-input route is commonly read as
  metastable

## Falsification Surface

If precision measurements of `m_t`, `m_H`, and the associated running inputs
force the vacuum deep into the metastable region in a way incompatible with the
current bounded framework-side `y_t` band, this companion prediction is in
tension with the framework route.

## Supporting Notes

- [HIGGS_VACUUM_PROMOTED_NOTE.md](./HIGGS_VACUUM_PROMOTED_NOTE.md)
- [HIGGS_MASS_DERIVED_NOTE.md](./HIGGS_MASS_DERIVED_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)

## Validation Snapshot

- current package boundary condition: `lambda(M_Pl) = 0`
- full 3-loop framework-side Higgs runner exists and is live on `main`
- vacuum stability remains bounded through the same Yukawa / top route that
  controls the current Higgs package

Primary reruns:

- `frontier_higgs_mass_full_3loop.py`
- `frontier_yt_color_projection_correction.py`
- `frontier_direct_yt_extraction.py`
