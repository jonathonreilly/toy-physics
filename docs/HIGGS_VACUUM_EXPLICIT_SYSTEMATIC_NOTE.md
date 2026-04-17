# Higgs / Vacuum Authority

**Date:** 2026-04-15
**Status:** derived with inherited explicit systematic quantitative lane on the current package
**Primary runners:** `scripts/frontier_higgs_mass_full_3loop.py`,
`scripts/frontier_yt_color_projection_correction.py`
**Boundary-support runner:** `scripts/frontier_direct_yt_extraction.py`

## Authority Role

This note is the standalone authority for the Higgs / vacuum lane on
the current package surface.

It is separate from:

- the retained hierarchy / `v` lane
- the standalone `alpha_s` lane
- the EW normalization lane
- the Yukawa / top lane

The direct taste-sector formula in
[HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md) remains a
supporting auxiliary derivation. It is not the lane summary by itself.

The exact taste-block Coleman-Weinberg isotropy theorem in
[TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](./TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md)
is also part of the current support stack. It does not unbound the Higgs lane
by itself, but it does close one exact question about the taste block: the
fermion Coleman-Weinberg Hessian cannot split the Higgs-direction curvature
from the two orthogonal taste directions at the retained axis-aligned minimum.

## Safe Statement

The framework derives the Higgs mechanism and the composite-Higgs boundary
structure, and the repo now contains a direct framework-side full 3-loop Higgs
computation with no Buttazzo-style calibrated-fit dependence.

Using the current accepted package inputs:

- canonical framework-side central value:
  `m_H(full 3-loop framework-side route) = 125.1 GeV`
- retained support route:
  `m_H(2-loop corrected-input route) = 119.8 GeV`
- vacuum stability is qualitatively favorable on the same route

These rows are now best read as `DERIVED WITH INHERITED EXPLICIT SYSTEMATIC`
because they inherit the explicit `y_t` bridge budget on the current package
support stack. The remaining Higgs blocker is no longer “missing
framework-native 3-loop implementation.”

## Component Structure

1. The direct taste-sector Higgs formula gives the auxiliary lattice-scale
   support route:
   `m_H = v / (2 u_0) = 140.3 GeV`
2. The corrected Yukawa/color-projection route shifts the 2-loop CW/stability
   result to:
   `m_H(2-loop) = 119.8 GeV`
3. The direct full 3-loop Higgs runner now computes the canonical current
   framework-side value:
   `m_H = 125.1 GeV`
4. On that same route, the vacuum readout stays qualitatively favorable, but
   it remains systematic-limited because the lane still inherits the explicit
   Yukawa bridge budget.
5. The exact taste-block Coleman-Weinberg isotropy theorem closes the
   fermion-CW part of the Higgs/taste splitting question. On the current
   bounded gauge-only split model, this supports a near-degenerate taste-scalar
   pair at `m_taste = 124.91 GeV` and a scalar-only thermal-cubic estimate
   `v_c/T_c = 0.3079`. Those are bounded downstream consequences, not promoted
   quantitative Higgs rows.

## Supporting Notes

- [HIGGS_MASS_DERIVED_NOTE.md](./HIGGS_MASS_DERIVED_NOTE.md)
- [HIGGS_MASS_FROM_AXIOM_NOTE.md](./HIGGS_MASS_FROM_AXIOM_NOTE.md)
- [TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](./TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_FLAGSHIP_BOUNDARY_NOTE.md](./YT_FLAGSHIP_BOUNDARY_NOTE.md)

## Validation Snapshot

- canonical framework-side central value:
  `m_H(full 3-loop framework-side route) = 125.1 GeV`
- retained support route:
  `m_H(2-loop corrected-input route) = 119.77 GeV`
- observed comparator: `125.25 GeV`
- inherited Higgs band from explicit-systematic `y_t`: `121.1-129.2 GeV`
  conservative, `122.6-127.7 GeV` support-tight
- vacuum prediction: qualitatively favorable, with inherited explicit
  systematic through the `y_t` lane

Primary reruns:

- `frontier_higgs_mass_full_3loop.py`
- `frontier_yt_color_projection_correction.py`
- `frontier_direct_yt_extraction.py`
