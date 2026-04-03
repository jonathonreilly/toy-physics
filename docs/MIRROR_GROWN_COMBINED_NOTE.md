# Mirror + Grown Combined Note

**Date:** 2026-04-03  
**Status:** exploratory only; does not approximate the retained higher-symmetry benefit

This note records the grown-symmetry scout in:

[`scripts/mirror_grown_combined.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_grown_combined.py)

Log:

[`logs/2026-04-03-mirror-grown-combined.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-grown-combined.txt)

## Question

Can a grown symmetry scaffold approximate the retained `Z2xZ2` benefit near
the grown-graph density optimum, instead of relying on an imposed symmetry
construction?

The script tests:

- `d_growth = 2` with a y-mirror scaffold
- `d_growth = 3` with a y-mirror scaffold
- `n_layers = 18, 25, 30, 40`
- `npl = 30`

## Results

The grown mirror scout remains Born-safe where it runs, but the joint
performance is weak compared with the retained symmetry lanes.

### `d_growth = 2`

| N | pur_min | 1-pur_min | gravity |
|---|---:|---:|---:|
| 18 | `0.9729` | `0.0271` | `-0.074` |
| 25 | `0.9630` | `0.0370` | `+0.070` |
| 30 | `0.9602` | `0.0398` | `+0.111` |
| 40 | `0.9822` | `0.0178` | `+1.086` |

### `d_growth = 3`

| N | pur_min | 1-pur_min | gravity |
|---|---:|---:|---:|
| 18 | `0.9687` | `0.0313` | `+0.236` |
| 25 | `0.9633` | `0.0367` | `+0.068` |
| 30 | `0.9243` | `0.0757` | `+0.059` |
| 40 | `0.9355` | `0.0645` | `+0.478` |

## Narrow Read

- The grown mirror scaffold is Born-safe where it runs.
- It does not reproduce the mirror chokepoint pocket.
- It does not approximate the `Z2xZ2` joint benefit near the density optimum.
- The best row in this scout is still a weak joint result rather than a
  retained emergence-facing lead.

## Conclusion

The grown mirror scaffold is a useful negative control for the emergence-facing
story, but it is not the successor lane.

The safe statement is:

- **exploratory only:** yes
- **retained long-term vector:** no
- **approximation to retained `Z2xZ2` benefit:** no

If the emergence-facing symmetry story is to become a live successor lane, it
needs a new generator that preserves the symmetry benefit more directly than
this grown mirror scaffold does.
