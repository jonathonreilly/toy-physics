# Unit-Projector Pole-Threshold Obstruction

**Date:** 2026-05-01
**Status:** exact negative boundary / unit-projector finite-ladder pole-threshold obstruction
**Runner:** `scripts/frontier_yt_unit_projector_pole_threshold_obstruction.py`
**Certificate:** `outputs/yt_unit_projector_pole_threshold_obstruction_2026-05-01.json`

## Purpose

The taste/projector normalization attempt showed that the unit taste singlet is
algebraically available, while the physical scalar carrier and pole derivative
remain open.  This block asks whether the finite ladder still has a pole at the
retained scout kernel strength after the unit taste projector is applied.

## Result

```text
python3 scripts/frontier_yt_unit_projector_pole_threshold_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

The unit-projector eigenvalues are all below the pole threshold:

| Witness | Unit-projector `lambda_max` | Kernel multiplier needed for `lambda_max = 1` |
|---|---:|---:|
| `N=4`, `m=0.20`, local | `0.442298920672` | `2.26091440260` |
| `N=6`, `m=0.20`, local | `0.0929651925869` | `10.7567127365` |
| `N=4`, `m=0.30`, local | `0.0914604870307` | `10.9336833038` |
| `N=4`, `m=0.20`, point-split normalized | `0.149456019531` | `6.69092982747` |

Even the best finite row would need an additional scalar-channel kernel
multiplier of `2.26091440260` to reach `lambda_max = 1`.

## Claim Boundary

This is not retained or proposed-retained closure.  It does not fit a
scalar-channel coupling, set `kappa_s = 1`, use `H_unit`, use
`yt_ward_identity`, select by observed values, or import alpha/plaquette/`u0`,
reduced pilots, `c2 = 1`, or `Z_match = 1`.

The result blocks using the unit-projector finite ladder as pole evidence at
the retained scout kernel strength.  A positive analytic route must derive the
interacting scalar-channel kernel enhancement and `K'(x_pole)` from retained
dynamics, or the campaign must use production same-source FH/LSZ pole data.
