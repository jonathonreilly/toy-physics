# Unification Basin Failure Note

**Date:** 2026-04-06  
**Status:** diagnosed boundary note for the shared grown-family basin

## Artifact chain

- [`scripts/FIXED_FIELD_FAMILY_UNIFICATION_BASIN.py`](/Users/jonreilly/Projects/Physics/scripts/FIXED_FIELD_FAMILY_UNIFICATION_BASIN.py)
- [`logs/2026-04-06-unification-basin-failure.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-unification-basin-failure.txt)
- retained row-level positives:
  - [`docs/NONLABEL_GROWN_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/NONLABEL_GROWN_BASIN_NOTE.md)
  - [`docs/FIXED_FIELD_COMPLEX_GROWN_BASIN_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIXED_FIELD_COMPLEX_GROWN_BASIN_V2_NOTE.md)
  - [`docs/FIXED_FIELD_FAMILY_UNIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIXED_FIELD_FAMILY_UNIFICATION_NOTE.md)

## Question

Does the same retained grown-family neighborhood support both fixed-field
companions off-center, not just on the center row?

The checked shared neighborhood is the overlap of the two retained narrow
basins:

- signed-source basin around the geometry-sector candidate
- complex-action basin around the retained grown-row companion

The overlap rows checked here are:

- `drift = 0.20, restore = 0.60`
- `drift = 0.20, restore = 0.70`

## Frozen Result

The shared rows preserve the signed-source package:

- exact zero-source baseline
- exact neutral `+1/-1` cancellation
- correct sign orientation
- unit charge exponent

But the same shared rows do **not** preserve the complex-action crossover:

- gamma `= 0` remains positive, but
- gamma `= 0.2` and gamma `= 0.5` both move to the absorptive side
- the `TOWARD -> AWAY` crossover is lost off-center

### Observed row table

| drift | restore | sign zero | sign plus | sign minus | sign neutral | sign exp | gamma0 | delta@0.2 | delta@0.5 | fm0 | fm0.5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.20` | `0.60` | `0.000e+00` | `-3.393e-05` | `+3.392e-05` | `0.000e+00` | `1.000` | `+3.090e-02` | `-6.633e-02` | `-2.040e-01` | `1.000` | `1.000` |
| `0.20` | `0.70` | `0.000e+00` | `-3.535e-05` | `+3.534e-05` | `0.000e+00` | `1.000` | `+3.204e-02` | `-6.679e-02` | `-2.069e-01` | `1.000` | `1.000` |

## Safe Read

The old geometry-sector / non-label idea and the complex-action companion do
not share a compact basin on the same off-center rows.

What survives:

- the sign-law branch remains basin-positive
- the complex-action branch remains row-level positive on its own retained row

What fails:

- the unification does not survive the shared off-center neighborhood
- the complex-action crossover is more selective than the sign-law basin

## Boundary Diagnosis

The breaking mechanism is not a trivial sanity failure. It is a family-selective
transport failure:

- the geometry-sector candidate is robust enough to preserve the signed-source
  response on nearby rows
- but that same neighborhood does not keep the complex-action crossover
- so the compact same-row unification is real, but it does not broaden into a
  shared family basin on this geometry

## Final Verdict

**diagnosed boundary: shared basin fails off-center**

