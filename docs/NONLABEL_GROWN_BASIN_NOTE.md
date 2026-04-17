# Non-Label Grown Basin Note

**Date:** 2026-04-06
**Status:** bounded positive basin around the retained grown-row signed-source transfer

## Artifact chain

- [`scripts/NONLABEL_GROWN_BASIN_TARGETED.py`](/Users/jonreilly/Projects/Physics/scripts/NONLABEL_GROWN_BASIN_TARGETED.py)
- [`logs/2026-04-06-nonlabel-grown-basin-targeted.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-nonlabel-grown-basin-targeted.txt)

## Question

Does the old geometry-sector / non-label connectivity idea extend beyond the single
retained grown row into a tiny neighborhood for the fixed-field signed-source
transfer?

This note stays intentionally narrow:

- fixed drift row: `drift = 0.2`
- nearby restore values: `restore = 0.6, 0.7, 0.8`
- exact zero-source baseline
- exact neutral `+1/-1` cancellation
- sign orientation
- weak charge-scaling estimate

## Frozen Result

Seed `0`, geometry-sector candidate:

| restore | zero source | single `+1` | single `-1` | neutral `+1/-1` | double `+2` | charge exponent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.60` | `+0.000000e+00` | `-3.392803e-05` | `+3.391622e-05` | `+0.000000e+00` | `-6.787447e-05` | `1.000000` |
| `0.70` | `+0.000000e+00` | `-3.534838e-05` | `+3.533743e-05` | `+0.000000e+00` | `-7.070770e-05` | `1.000223` |
| `0.80` | `+0.000000e+00` | `-3.620420e-05` | `+3.619258e-05` | `+0.000000e+00` | `-7.241011e-05` | `1.000000` |

## Safe Read

The geometry-sector / non-label architecture does not only work on the single
retained grown row. It survives the nearest restore neighborhood at fixed
`drift = 0.2`:

- the zero-source baseline remains exactly zero
- the neutral same-point `+1/-1` control remains exactly zero
- the single-source response keeps the correct sign orientation
- the charge response stays linear to within the checked exponent

## Final Verdict

**bounded positive basin**

