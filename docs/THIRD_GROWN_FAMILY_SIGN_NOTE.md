# Third Grown Family Sign Note

**Date:** 2026-04-06  
**Status:** proposed_retained bounded positive third grown-family signed-source basin

## Artifact chain

- [`scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py)
- [`logs/2026-04-06-third-grown-family-sign.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-third-grown-family-sign.txt)
- [`docs/THIRD_GROWN_FAMILY_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_BOUNDARY_NOTE.md)

## Question

Can a third independent grown-family slice, distinct from the current
geometry-sector and parity-rotated sector families, preserve the signed-source
package under exact zero and neutral controls?

This probe is intentionally strict:

- geometry: no-restore grown slice
- connectivity: cross-quadrant load-balanced forward matching
- controls: exact zero-source baseline and exact neutral `+1/-1` cancellation
- sign test: positive `+1` versus negative `-1`
- scaling test: double-source charge exponent near `1`

## Result

The family has a real bounded basin. The gate passes on a subset of the tested
rows, with exact controls intact:

- passed rows: `5/15`
- drift coverage among passes: `0.1, 0.2, 0.3`
- mean charge exponent among passes: `0.999842`

The passed rows are genuinely retained:

- exact zero-source baseline remains zero
- exact neutral `+1/-1` cancellation remains zero
- the sign orientation is correct on the retained rows
- the weak charge response remains essentially linear

## Safe Read

This is a third independent grown-family positive, but it is still narrow.

What survives:

- exact zero and neutral controls
- sign orientation on the retained rows
- near-linear charge scaling
- a small drift basin rather than a one-row ridge

What does not survive:

- the full tested drift range
- any family-wide or geometry-generic claim

## Conclusion

**retained bounded positive third grown-family basin**
