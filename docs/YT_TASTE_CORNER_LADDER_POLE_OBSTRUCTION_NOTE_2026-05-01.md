# Taste-Corner Ladder Pole-Witness Obstruction

**Date:** 2026-05-01
**Status:** exact negative boundary / finite-ladder taste-corner pole-witness obstruction
**Runner:** `scripts/frontier_yt_taste_corner_ladder_pole_obstruction.py`
**Certificate:** `outputs/yt_taste_corner_ladder_pole_obstruction_2026-05-01.json`

## Purpose

The previous zero-mode-removed ladder search found four finite
`lambda_max >= 1` witnesses after color-singlet `q=0` cancellation.  This
block tests whether those witnesses survive once non-origin Brillouin-zone
taste corners are not allowed as an implicit scalar carrier.

## Result

```text
python3 scripts/frontier_yt_taste_corner_ladder_pole_obstruction.py
# SUMMARY: PASS=8 FAIL=0
```

All finite crossing rows sit on even grids with 16 `sin(p)=0` taste corners.
The non-origin corners supply `70.4828%` to `92.2308%` of the full crossing
scale, and the corner-only kernel reproduces `92.7618%` to `98.7049%` of it.

When the non-origin corners are excluded while keeping the physical origin
corner and non-corner modes, every finite crossing disappears:

```text
max physical-origin-only lambda = 0.269595077382
max no-corner lambda            = 0.0779554723582
```

## Claim Boundary

This is a negative boundary on the finite witness, not a no-go theorem for all
interacting scalar dynamics.  The finite `lambda_max >= 1` witnesses cannot be
used as retained scalar-pole or LSZ evidence unless a separate retained
continuum/taste/projector theorem admits those non-origin corners into the
scalar carrier and derives the inverse-propagator derivative.

PR #230 still needs that theorem or production same-source FH/LSZ pole data.
