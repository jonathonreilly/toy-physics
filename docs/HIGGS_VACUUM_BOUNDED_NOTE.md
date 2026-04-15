# Higgs / Vacuum Bounded Authority

**Date:** 2026-04-15
**Status:** bounded quantitative lane on `main`
**Primary runners:** `scripts/frontier_higgs_mass_full_3loop.py`,
`scripts/frontier_yt_color_projection_correction.py`
**Boundary-support runner:** `scripts/frontier_direct_yt_extraction.py`

## Authority Role

This note is the standalone authority for the bounded Higgs / vacuum lane on
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

The framework derives the Higgs mechanism and the composite-Higgs boundary
structure, and the repo now contains a direct framework-side full 3-loop Higgs
computation with no Buttazzo-style calibrated-fit dependence.

Using the current accepted package inputs:

- `m_H(2-loop corrected-input route) = 119.8 GeV`
- `m_H(full 3-loop framework-side route) = 125.3 GeV`
- vacuum stability is qualitatively favorable on the same route

These rows remain `BOUNDED` on `main` only because they inherit the bounded
`y_t` / QFP route. The remaining Higgs blocker is no longer “missing
framework-native 3-loop implementation.”

## Component Structure

1. The direct taste-sector Higgs formula gives the auxiliary lattice-scale
   support route:
   `m_H = v / (2 u_0) = 140.3 GeV`
2. The corrected Yukawa/color-projection route shifts the 2-loop CW/stability
   result to:
   `m_H(2-loop) = 119.8 GeV`
3. The direct full 3-loop Higgs runner now computes the current central
   framework-side value:
   `m_H = 125.3 GeV`
4. On that same route, the vacuum readout stays qualitatively favorable, but
   it remains bounded because the lane still inherits the bounded Yukawa/QFP
   route.

## Supporting Notes

- [HIGGS_MASS_DERIVED_NOTE.md](./HIGGS_MASS_DERIVED_NOTE.md)
- [HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_FLAGSHIP_CLOSURE_NOTE.md](./YT_FLAGSHIP_CLOSURE_NOTE.md)

## Validation Snapshot

- `m_H(2-loop corrected-input route) = 119.77 GeV`
- `m_H(full 3-loop framework-side route) = 125.3 GeV`
- observed comparator: `125.25 GeV`
- inherited Higgs band from bounded `y_t`: `115.2-135.3 GeV`
- vacuum prediction: qualitatively favorable, but bounded through the `y_t`
  lane

Primary reruns:

- `frontier_higgs_mass_full_3loop.py`
- `frontier_yt_color_projection_correction.py`
- `frontier_direct_yt_extraction.py`
