# Non-Label Grown Drift Basin Note

**Date:** 2026-04-06  
**Status:** bounded positive drift basin on the retained grown family

## Artifact chain

- [`scripts/NONLABEL_GROWN_DRIFT_BASIN_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/NONLABEL_GROWN_DRIFT_BASIN_SWEEP.py)
- [`scripts/NONLABEL_GROWN_DRIFT_BASIN_DIAG.py`](/Users/jonreilly/Projects/Physics/scripts/NONLABEL_GROWN_DRIFT_BASIN_DIAG.py)
- [`logs/2026-04-06-nonlabel-grown-drift-basin-diag.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-nonlabel-grown-drift-basin-diag.txt)

## Question

Starting from the retained restore-basin positive, does the geometry-sector /
non-label signed-source package survive a tiny drift neighborhood around
`drift = 0.2` on the same grown family?

The basin is intentionally narrow:

- fixed restore: `restore = 0.7`
- nearby drift values: `drift = 0.15, 0.20, 0.25`
- exact zero-source baseline
- exact neutral `+1/-1` cancellation
- sign orientation
- weak charge-scaling estimate

## Frozen Result

Seed `0`, geometry-sector candidate:

| drift | zero source | single `+1` | single `-1` | neutral `+1/-1` | double `+2` | charge exponent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.15` | `+0.000000e+00` | `-3.582e-05` | `+3.580e-05` | `+0.000000e+00` | `-7.164e-05` | `1.000` |
| `0.20` | `+0.000000e+00` | `-3.535e-05` | `+3.534e-05` | `+0.000000e+00` | `-7.071e-05` | `1.000` |
| `0.25` | `+0.000000e+00` | `-3.486e-05` | `+3.485e-05` | `+0.000000e+00` | `-6.974e-05` | `1.000` |

## Safe Read

The geometry-sector / non-label architecture survives the tiny drift
neighborhood at fixed `restore = 0.7`:

- the zero-source baseline remains exactly zero
- the neutral same-point `+1/-1` control remains exactly zero
- the single-source response keeps the correct sign orientation
- the charge response stays linear to within the checked exponent

## Final Verdict

**bounded positive drift basin**
