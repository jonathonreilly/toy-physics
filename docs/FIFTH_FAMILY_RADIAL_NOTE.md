# Fifth Family Radial Note

**Date:** 2026-04-06  
**Status:** retained narrow basin on the radial-shell no-restore grown slice

## Artifact Chain

- [`scripts/FIFTH_FAMILY_RADIAL_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_SWEEP.py)
- [`scripts/FIFTH_FAMILY_RADIAL_BASIN.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_BASIN.py)
- [`scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py`](/Users/jonreilly/Projects/Physics/scripts/FIFTH_FAMILY_RADIAL_FM_TRANSFER.py)
- [`logs/2026-04-06-fifth-family-radial.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial.txt)
- [`logs/2026-04-06-fifth-family-radial-basin.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial-basin.txt)
- [`logs/2026-04-06-fifth-family-radial-fm-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fifth-family-radial-fm-transfer.txt)

## Question

Does a genuinely different structured connectivity family survive the exact zero/neutral gate on the no-restore grown slice?

## Retained Rows

Sampled rows supporting the narrow basin:

- drift `0.05`, seed `0`
- drift `0.30`, seed `1`

Both rows satisfy:
- exact zero-source baseline
- exact neutral same-point cancellation
- sign orientation
- weak-field linearity near `F~M = 1`

## Boundary Row

The interior probe at:

- drift `0.20`, seed `0`

fails sign orientation even though exact controls remain clean. That makes this family selective, not broad.

## Safe Read

- the radial-shell connectivity rule is a real fifth structured family basin on the sampled rows
- the basin is narrow and seed-selective
- the miss is a sign-orientation boundary, not a control leak

