# Fifth Family Complex Boundary Note

**Date:** 2026-04-06  
**Status:** support - structural or confirmatory support note

## Artifact Chain

- [`scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py)
- [`logs/2026-04-06-fifth-family-complex-targeted.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-complex-targeted.txt)
- [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md)

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
