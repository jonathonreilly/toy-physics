# Fifth Family Complex Boundary Note

**Date:** 2026-04-06 (originally); 2026-05-03 (review-loop runner repair)
**Status:** support - structural or confirmatory support note

**Primary runner:** [`scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py`](../scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py)

## Review-loop repair (2026-05-03)

The 2026-05-03 audit flagged the runner as failing at import. Root cause:
[`scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py`](../scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py)
imported `_field_from_sources` (and the helper constants) from
`CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP`, but that module re-exports its
peer module via `from CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP import *`,
and `import *` does **not** propagate underscore-prefixed names. The
repair points the import directly at `CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP`,
which is where `_field_from_sources` is actually defined.

Fresh runner log:
[`logs/2026-05-03-fifth-family-complex-targeted.txt`](../logs/2026-05-03-fifth-family-complex-targeted.txt)

The fresh log confirms every boundary-row statement in this note: 1
anchor row passes the exact `gamma=0` + Born/F~M gates, 1 row exhibits
the `TOWARD -> AWAY` crossover (the anchor row at `drift = 0.05`,
`seed = 1`), and the sampled outer rows at `drift = 0.05, seed = 0` and
`drift = 0.30, seed = 1` do not show the crossover.

## Artifact Chain

- [`scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py`](../scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py)
- [`logs/2026-04-06-fifth-family-complex-targeted.txt`](../logs/2026-04-06-fifth-family-complex-targeted.txt) (legacy log)
- [`logs/2026-05-03-fifth-family-complex-targeted.txt`](../logs/2026-05-03-fifth-family-complex-targeted.txt) (post-repair log)
- [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md`](../archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md)

## Boundary Rows

The sampled outer rows do not retain the same directional companion cleanly:

- `drift = 0.05`, `seed = 0`
  - exact controls remain clean
  - `gamma = 0` is already negative in the detector shift
  - `TOWARD -> AWAY` does not appear
- `drift = 0.30`, `seed = 1`
  - exact controls remain clean
  - the response stays on the same side of the crossover
  - `TOWARD -> AWAY` does not appear

## Safe Read

- the radial-shell fifth-family slice really does carry a complex companion on the anchor row
- the companion is selective, not family-wide
- the outer sampled rows show a clear response-sign boundary, not a control leak

## Final Verdict

**diagnosed selectivity boundary**
