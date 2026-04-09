# Non-Label Grown Drift Basin Note

**Date:** 2026-04-06  
**Status:** retained bounded positive drift basin around the grown-row non-label signed-source transfer

## Artifact chain

- [`scripts/NONLABEL_GROWN_DRIFT_BASIN_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/NONLABEL_GROWN_DRIFT_BASIN_SWEEP.py)
- [`scripts/NONLABEL_GROWN_DRIFT_BASIN_DIAG.py`](/Users/jonreilly/Projects/Physics/scripts/NONLABEL_GROWN_DRIFT_BASIN_DIAG.py)
- [`logs/2026-04-06-nonlabel-grown-drift-basin-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-nonlabel-grown-drift-basin-sweep.txt)
- retained restore-basin anchor:
  [`docs/NONLABEL_GROWN_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/NONLABEL_GROWN_BASIN_NOTE.md)

## Question

Does the geometry-sector / non-label connectivity idea survive a tiny drift
neighborhood around the retained grown row while keeping restore fixed near the
promoted value?

This note is intentionally narrow:

- fixed restore: `restore = 0.7`
- nearby drifts: `drift = 0.15, 0.20, 0.25`
- exact zero-source baseline
- exact neutral `+1/-1` cancellation
- sign orientation
- weak charge-scaling estimate

## Frozen Result

All checked rows across seeds `0, 1, 2` pass:

| drift | seed | zero source | single `+1` | single `-1` | neutral `+1/-1` | double `+2` | charge exponent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.15` | `0` | `+0.000000e+00` | `-3.581785e-05` | `+3.580452e-05` | `+0.000000e+00` | `-7.163621e-05` | `1.000000` |
| `0.15` | `1` | `+0.000000e+00` | `-4.493534e-05` | `+4.492629e-05` | `+0.000000e+00` | `-8.989110e-05` | `1.000000` |
| `0.15` | `2` | `+0.000000e+00` | `-3.335325e-05` | `+3.334036e-05` | `+0.000000e+00` | `-6.671544e-05` | `1.000000` |
| `0.20` | `0` | `+0.000000e+00` | `-3.534838e-05` | `+3.533743e-05` | `+0.000000e+00` | `-7.070770e-05` | `1.000223` |
| `0.20` | `1` | `+0.000000e+00` | `-4.753707e-05` | `+4.752606e-05` | `+0.000000e+00` | `-9.510419e-05` | `1.000000` |
| `0.20` | `2` | `+0.000000e+00` | `-3.163285e-05` | `+3.162221e-05` | `+0.000000e+00` | `-6.326652e-05` | `1.000000` |
| `0.25` | `0` | `+0.000000e+00` | `-3.485833e-05` | `+3.484561e-05` | `+0.000000e+00` | `-6.974134e-05` | `1.000000` |
| `0.25` | `1` | `+0.000000e+00` | `-5.006985e-05` | `+5.005918e-05` | `+0.000000e+00` | `-1.001378e-04` | `1.000000` |
| `0.25` | `2` | `+0.000000e+00` | `-2.967155e-05` | `+2.966117e-05` | `+0.000000e+00` | `-5.934242e-05` | `1.000000` |

## Safe Read

The geometry-sector / non-label architecture does not only work on the single
retained grown row. It survives the nearest drift neighborhood at fixed
`restore = 0.7`:

- the zero-source baseline remains exactly zero
- the neutral same-point `+1/-1` control remains exactly zero
- the single-source response keeps the correct sign orientation
- the charge response stays linear to within the checked exponent

The drift axis is therefore not the immediate boundary for this retained
family. The basin is still narrow and selective, so this is not a
family-wide transfer claim, but it is a real local basin rather than a
one-row ridge.

## Final Verdict

**bounded positive drift basin**

