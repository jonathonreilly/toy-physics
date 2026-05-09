# Central-Band Dense Boundary Note

**Date:** 2026-04-03  
**Status:** boundary probe for the dense central-band pocket

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/central_band_dense_boundary_sweep.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

This note records a narrow radius sweep around the dense central-band
same-graph pocket.

Script:
[`scripts/central_band_dense_boundary_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/central_band_dense_boundary_sweep.py)

## Quick Probe

The short probe used:

- `N = 80, 100`
- `npl = 60`
- `connect_radius = 2.8, 3.0, 3.2, 3.4`
- `y_cut = 2.0`
- `2` seeds
- `2` realizations

## What It Shows

The boundary is sharp rather than smoothly extendable.

### `N = 80`

- `r = 2.8`: `LN + |y|` gravity `-0.020±0.000`, purity `1.000±0.000`
- `r = 3.0`: `LN + |y|` gravity `-0.595±0.000`, purity `1.000±0.000`
- `r = 3.2`: `LN + |y|` gravity `-0.241±0.357`, purity `1.000±0.000`
- `r = 3.4`: `LN + |y|` gravity `-0.189±0.363`, purity `1.000±0.000`

The `LN + |y| + collapse` rows lower purity, but gravity remains negative
through this `N = 80` probe.

### `N = 100`

- `r = 2.8`: `LN + |y|` gravity `-0.007±0.000`, purity `1.000±0.000`
- `r = 3.0`: `LN + |y|` gravity `-0.044±0.000`, purity `1.000±0.000`
- `r = 3.2`: `LN + |y|` gravity `+10.428±0.000`, purity `0.500±0.000`
- `r = 3.4`: both rows become thin and mixed, with Born already degraded to
  `0.333±0.080`

## Narrow Conclusion

- The dense central-band pocket is not broadly extendable by tweaking
  `connect_radius` a little.
- Gravity is still geometry-sensitive and rolls over in the dense pocket at
  the large-`N` extension.
- The `r = 3.0` family is the most Born-stable, but it is not the clean
  gravity winner at `N = 80..100`.

