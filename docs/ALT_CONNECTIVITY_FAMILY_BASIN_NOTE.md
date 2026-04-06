# ALT Connectivity Family Basin Note

**Date:** 2026-04-06  
**Status:** retained bounded basin for the alternative connectivity family

## Artifact Chain

- [`scripts/ALT_CONNECTIVITY_FAMILY_BASIN.py`](/Users/jonreilly/Projects/Physics/scripts/ALT_CONNECTIVITY_FAMILY_BASIN.py)
- [`logs/2026-04-06-alt-connectivity-family-basin.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-alt-connectivity-family-basin.txt)
- [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)

## Question

Does the parity-rotated sector-transition family survive beyond a few hand-picked
rows on the no-restore grown slice?

## Result

The family survives as a **real bounded basin**, not just a sparse row-level
positive.

Controls remain clean:

- exact zero-source baseline passes
- exact neutral `+/-` cancellation passes
- sign orientation remains correct on retained rows
- weak charge scaling stays near linear

Sweep summary:

- tested drifts: `0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5`
- tested seeds: `0, 1, 2, 3, 4`
- passing rows: `32/45`

The basin is broad but not family-wide:

- some seeds fail at `drift = 0.1, 0.15, 0.25, 0.3, 0.4, 0.5`
- the zero-drift and mid-drift rows are especially stable
- the family is therefore a bounded positive, not a universal closure

## Safe Read

The old sector-style lesson does generalize beyond the current geometry-sector
rule.

What we have now is a distinct alternative connectivity family on the
no-restore grown slice that preserves:

- exact zero / neutral controls
- sign orientation
- near-linear charge scaling

What we do not have:

- seed-wide closure at all tested drifts
- a geometry-generic theorem
- any claim that this is the only surviving structured family

## Conclusion

This alternative family is a real structured-connectivity basin, and it is
different enough from the current geometry-sector rule to count as a separate
architecture lane.
