# Higher-Symmetry Gravity Probe Note

**Date:** 2026-04-03  
**Status:** bounded positive, but not a clean gravity-law contender

This note records the gravity-side follow-up to the higher-symmetry joint
validation.

Script:
[`scripts/higher_symmetry_gravity_probe.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_gravity_probe.py)

Log:
[`logs/2026-04-03-higher-symmetry-gravity-probe-z2z2-dense-n80-n120.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-higher-symmetry-gravity-probe-z2z2-dense-n80-n120.txt)

## Question

Does the dense `Z2 x Z2` extension inherit a usable gravity-side mass window
or distance tail, or does gravity flatten out as the symmetry lane is widened?

The probe uses the same slit/detector geometry as the joint validator and
checks:

- fixed-anchor mass windows
- fixed-mass distance sweeps
- the same phase-mediated `k`-band readout used in the joint note

## Dense Extension Setup

- `N = 80, 100, 120`
- `16` seeds
- `z2z2-quarter = 16` (`64` total nodes per layer)
- `connect_radius = 5.2`
- `anchor_b = 5.0`
- `mass_count = 4`

## Fixed-Anchor Mass Window

The mass window stays positive, but it is weak and only moderately fit-shaped:

| N | fit |
|---|---|
| 80 | `delta ~= 0.3668 * M^0.724`, `R^2 = 0.999` |
| 100 | `delta ~= 0.0748 * M^1.348`, `R^2 = 0.918` |
| 120 | `delta ~= 0.0504 * M^1.318`, `R^2 = 0.622` |

## Fixed-Distance Sweep

The distance response remains positive, but the tail is not a clean retained
gravity law:

| N | peak | tail fit |
|---|---|---|
| 80 | `b = 6.0` | `delta ~= C * b^-2.132`, `R^2 = 0.562` |
| 100 | `b = 6.0` | `delta ~= C * b^0.751`, `R^2 = 0.014` |
| 120 | `b = 4.0` | `delta ~= C * b^-0.563`, `R^2 = 0.151` |

## Narrow Read

- The dense `Z2 x Z2` extension is still gravity-positive.
- The mass response remains positive but weak, and the fit quality degrades by
  `N = 120`.
- The distance response is a broad bump / plateau rather than a clean retained
  law.
- So this lane is a real bounded gravity-side positive, but it is **not** the
  cleanest gravity law in the project.

## Conclusion

The dense `Z2 x Z2` extension survives as a review-safe coexistence lane, and
it does not lose Born safety at `N = 120`. But the gravity probe shows that the
lane is still a bounded pocket rather than a clean asymptotic gravity law.

The best current interpretation is:

- **decoherence lead:** yes
- **gravity-positive:** yes
- **gravity-law contender:** not yet

