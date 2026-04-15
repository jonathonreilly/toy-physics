# Higgs / Vacuum Promoted Authority

**Date:** 2026-04-15
**Status:** promoted quantitative lane on `main`
**Primary runners:** `scripts/frontier_higgs_buttazzo_calibration.py`,
`scripts/frontier_yt_color_projection_correction.py`

## Authority Role

This note is the standalone authority for the promoted Higgs / vacuum lane on
the current package surface.

It is separate from:

- the retained hierarchy / `v` lane
- the standalone `alpha_s` lane
- the EW normalization lane
- the Yukawa / top lane

The direct taste-sector formula in
[HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md) remains a
supporting auxiliary derivation. It is not the lane summary by itself.

## Safe Statement

Using the corrected Yukawa route and the promoted package inputs:

- `m_H(2-loop) = 119.8 GeV`
- `m_H(full 3-loop boundary) = 129.7 GeV`
- the framework predicts absolute vacuum stability rather than SM metastability

These are the current Higgs / vacuum rows promoted on `main`.

## Component Structure

1. The direct taste-sector Higgs formula gives the auxiliary lattice-scale
   support route:
   `m_H = v / (2 u_0) = 140.3 GeV`
2. The corrected Yukawa/color-projection route shifts the 2-loop CW/stability
   result to:
   `m_H(2-loop) = 119.8 GeV`
3. The full 3-loop boundary calibration with the derived package inputs gives:
   `m_H = 129.7 GeV`
4. On that same corrected-input route, the vacuum stays absolutely stable.

## Supporting Notes

- [HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md](./HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md)

## Validation Snapshot

- `m_H(2-loop) = 119.77 GeV`
- `m_H(full 3-loop) = 129.7 GeV`
- observed comparator: `125.25 GeV`
- vacuum prediction: absolutely stable

Primary reruns:

- `frontier_higgs_buttazzo_calibration.py`
- `frontier_yt_color_projection_correction.py`
