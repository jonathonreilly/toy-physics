# Dirac Source Smoothing Note

**Status:** bounded source-initialization scan on the historical Dirac 3+1D v3/v4 harnesses

This note freezes a narrow question:

> does smoothing the initial source packet improve the remaining gravity
> failures in the Dirac 3+1D harness?

The scan keeps the best current mass point fixed at `m0=0.10` and compares
the point-like source against Gaussian source widths using the same periodic
Dirac walk machinery as the historical v3/v4 harnesses.

## What was scanned

- `m0 = 0.10`
- `strength = 5e-4`
- N-growth sweep: `N = 6, 8, 10, 12, 14` at offset `3`
- distance-law sweep: offsets `2, 3, 4, 5` at `N = 10`
- source initialization: point-like vs Gaussian widths

## Script

- [`scripts/frontier_dirac_walk_3plus1d_source_smoothing_scan.py`](../scripts/frontier_dirac_walk_3plus1d_source_smoothing_scan.py)

## Result summary

The scan does not find a smoothing fix for the remaining Dirac 3+1D gravity
failures.

| source | sigma | N-growth TOWARD | N monotone | distance-law TOWARD | distance-law power law |
| --- | ---: | ---: | --- | ---: | --- |
| point | 0.00 | 2/5 | NO | 4/4 | alpha=3.688, R^2=0.7756 |
| gaussian | 0.75 | 2/5 | NO | 3/4 | n/a |
| gaussian | 1.25 | 4/5 | NO | 3/4 | n/a |
| gaussian | 2.00 | 2/5 | NO | 3/4 | n/a |

Exact signed readouts:

- Point source N-growth: `[-4.998117e-08, -6.597447e-12, +1.423305e-08, +4.076026e-09, -1.098863e-09]`
- Gaussian `sigma=0.75` N-growth: `[-3.894144e-08, +7.094952e-08, +7.994847e-09, -1.941730e-08, -1.397760e-09]`
- Gaussian `sigma=1.25` N-growth: `[+1.483299e-08, +4.095225e-08, +7.659475e-09, -3.639420e-09, +1.406360e-11]`
- Gaussian `sigma=2.00` N-growth: `[-1.565835e-08, +2.136509e-08, +3.639815e-09, -5.764271e-09, -1.021471e-08]`
- Point source offsets: `[+6.181186e-09, +1.423820e-08, +2.207141e-07, +9.711581e-08]`
- Gaussian `sigma=0.75` offsets: `[-7.765673e-09, +8.035397e-09, +9.573527e-08, +7.681030e-08]`
- Gaussian `sigma=1.25` offsets: `[-4.072661e-09, +7.344138e-09, +2.086168e-08, +3.210921e-08]`
- Gaussian `sigma=2.00` offsets: `[+2.855904e-09, -1.219403e-09, +8.268559e-09, +2.548897e-08]`

## Interpretation

The point of the scan is not to claim closure. It is to check whether a
smoother initial packet repairs the specific Dirac 3+1D gravity failures:

- non-monotone `N`-growth
- mixed-sign distance-law offsets

If the Gaussian widths do not improve the signed readouts relative to the
point-like source, then source smoothing is not the missing fix and the
remaining issue is likely in the walk, the mass field, or the readout
geometry instead.

The measured scan shows a partial trade-off only: `sigma=1.25` gives the
best N-growth sign count (`4/5` TOWARD), but still fails monotonicity, and
none of the Gaussian widths repair the mixed-sign distance-law offsets.
The point-like source remains the only case with all four tested offsets
TOWARD.
