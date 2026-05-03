# Fifth Family Complex Boundary Note

**Date:** 2026-04-06 (originally); 2026-05-03 (audit-driven runner-import repair)
**Status:** support - structural or confirmatory support note; runner now executes after 2026-05-03 import repair

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (fresh-agent-lovelace) recorded the runner as
failing at import, producing no rows. The runner imported `Family`,
`SOURCE_STRENGTH`, `SOURCE_Z`, and `_field_from_sources` from
`CONNECTIVITY_FAMILY_V2_QUADRANT_SWEEP`, which has been refactored to
a re-export shim of `CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP`. The
shim does not re-export the source-field helpers needed here.

Repair: point the imports at the current canonical module:

```python
from CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP import (
    Family, SOURCE_STRENGTH, SOURCE_Z, _field_from_sources,
)
```

The runner now executes and reproduces the boundary rows the note
documents:

| drift | seed | g0           | TOWARD→AWAY | Born+F~M gates |
|------:|-----:|-------------:|:-----------:|:--------------:|
|  0.05 |    0 | -2.26e-05    | no          | (no Born)      |
|  0.05 |    1 | +2.31e-05    | yes (1)     | (no Born)      |
|  0.20 |    0 | +2.03e-06    | yes (1)     | exact 0.000    |
|  0.20 |    1 | +2.54e-06    | yes (1)     | (no Born)      |
|  0.30 |    0 | -1.39e-05    | no          | (no Born)      |
|  0.30 |    1 | -1.13e-05    | no          | (no Born)      |

Confirms the SAFE READ: exactly 1 anchor row passes exact `gamma = 0`
+ Born/F~M gates; exactly 1 anchor row shows the `TOWARD → AWAY`
crossover; the `drift = 0.05, seed = 0` and `drift = 0.30` outer
rows do not retain the directional companion cleanly.

The note's substantive claim ("diagnosed selectivity boundary") is
unchanged. The audit's deeper concern — that the note has no
independent derivation of the boundary structure from retained inputs
— remains genuine open work; this repair restores the executable
evidence that re-audit needs to evaluate the bounded empirical
observation, not the theorem-level closure.

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
