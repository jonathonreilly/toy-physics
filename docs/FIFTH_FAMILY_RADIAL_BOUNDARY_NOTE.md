# Fifth Family Radial Boundary Note

**Date:** 2026-04-06 (originally); 2026-05-03 (audit-driven runner-import repair via PR #485)
**Status:** support - structural or confirmatory support note; runner now executes after PR #485 import repair

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (codex-fresh-radial-boundary-auditor) recorded
the runner as failing to import `_build_radial_shell_connectivity`
from `CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP`. That module became a
re-export shim of `CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP`, which
does not include the radial connectivity builder.

The 2026-05-03 runner repair (landed in PR #485, commit `46d9fda67`)
points the imports at the current API: `_build_radial_shell_connectivity`
from `DISTANCE_LAW_PORTABILITY_COMPARE` and `_measure_family` from
`CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP`. The runner now executes
and reproduces the exact `(drift = 0.20, seed = 0)` boundary row
this note claims:

```text
plus  = -2.028e-06
minus = +2.028e-06
zero  = 0.000e+00 (baseline exact)
neutral = 0.000e+00 (cancellation exact)
```

The sign-orientation flip the note documents (plus < 0, minus > 0
inside the radial-shell family at the test row) is now backed by an
executable runner, not a stale import. The note's substantive claim
(the fifth family is real but only as a narrow basin, with a clear
local boundary at this row) is unchanged.

The audit's deeper concern — that the note has no independent
derivation of the zero/neutral exactness or sign-flip from retained
inputs — remains genuine open work; this repair restores the
executable evidence that re-audit needs to evaluate the bounded
empirical observation, not the theorem-level closure.

## Artifact Chain

- [`scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py)
- [`logs/2026-04-06-fifth-family-radial-failure-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial-failure-audit.txt)
- [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_RADIAL_NOTE.md)

## Boundary

The interior test row at drift `0.20`, seed `0` keeps:
- zero-source baseline exact
- neutral cancellation exact

but flips sign orientation:
- `plus < 0`
- `minus > 0`

This is not a control leak. It is a structural orientation miss inside the radial-shell family.

## Safe Read

- the fifth family is real, but only as a narrow basin
- the family-construction space is not saturated yet, but this particular shell rule has a clear local boundary
- any broader family claim would be overstated until a wider basin or a second independent radial variant lands

