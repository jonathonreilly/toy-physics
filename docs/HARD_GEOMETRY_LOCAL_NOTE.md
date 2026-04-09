# Hard Geometry Local Support Note

**Date:** 2026-04-03  
**Status:** reviewed negative / bounded only

This note records the local hard-geometry pilot that asked whether a
purely local event-persistence rule could reproduce part of the hard-
geometry benefit without the nonlocal path-count asymmetry machinery.

Script:
[`scripts/hard_geometry_local_support_pilot.py`](/Users/jonreilly/Projects/Physics/scripts/hard_geometry_local_support_pilot.py)

## Setup

- graph family: 3D uniform DAG
- `npl = 60`
- `connect_radius = 3.0`
- `xyz_range = 12.0`
- seeds: 4
- `N = 40, 60, 80`
- local pruning applied only in the first third of the post-barrier region

## Local rules

- `local-1hop`: prune if immediate parent same-side support falls below threshold
- `local-2hop`: prune if 2-hop ancestor same-side support falls below threshold
- `|y|<2.0`: geometric comparator

## Main Results

Default threshold run (`support_thresh = 0.65`) showed:

| N | mode | `pur_cl` | `S_norm` | gravity | removed |
|---|---|---:|---:|---:|---:|
| 40 | baseline | `0.9441±0.037` | `0.1285` | `+0.0300` | -- |
| 40 | local-1hop | `0.9422±0.038` | `0.1398` | `-0.4460` | `7.6%` |
| 40 | local-2hop | `0.9563±0.039` | `0.1524` | `-0.6874` | `11.0%` |
| 40 | `|y|<2.0` | `0.9671±0.025` | `0.1769` | `-0.0564` | `17.1%` |
| 60 | baseline | `0.9748±0.010` | `0.0959` | `-1.6056` | -- |
| 60 | local-1hop | `0.9687±0.015` | `0.0972` | `-1.4505` | `7.4%` |
| 60 | local-2hop | `0.9563±0.012` | `0.1035` | `-1.3148` | `9.1%` |
| 60 | `|y|<2.0` | `0.9784±0.008` | `0.1401` | `-0.8216` | `16.2%` |
| 80 | baseline | `0.9847±0.014` | `0.0145` | `-0.2357` | -- |
| 80 | local-1hop | `0.9927±0.005` | `0.0144` | `+0.2137` | `7.9%` |
| 80 | local-2hop | `0.9936±0.004` | `0.0146` | `+0.2797` | `9.7%` |
| 80 | `|y|<2.0` | `0.9950±0.004` | `0.0181` | `+0.8871` | `16.7%` |

Threshold sanity checks:

- `support_thresh = 0.55`:
  - `N=60`: local-1hop `0.9810`, local-2hop `0.9786`
  - `N=80`: local-1hop `0.9940`, local-2hop `0.9868`
- `support_thresh = 0.75`:
  - `N=60`: local-1hop `0.9797`, local-2hop `0.9577`
  - `N=80`: local-1hop `0.9929`, local-2hop `0.9836`

## Narrow Conclusion

- Local support is a real observable, but it is not a clean scalable
  replacement for the hard-geometry rule.
- At `N=40/60`, local-1hop can slightly improve decoherence relative to
  baseline, but the effect is small and threshold-sensitive.
- By `N=80`, the local support rules no longer hold a stable advantage.
- The hard-gap comparator remains the more meaningful geometry action,
  but even that is bounded and not a scalable emergence law.

## Read

- This is a **bounded negative** for the purely local event-persistence
  hypothesis.
- The remaining hard-geometry vector is still geometry-based, but it is
  likely to need either a denser generated geometry or the already-retained
  Born-safe hard-geometry pockets, not a simple local support threshold.
