# Second Grown Family Complex Boundary Note

**Date:** 2026-04-06  
**Status:** diagnosed boundary on the tighter single-seed window

## Artifact chain

- [`scripts/SECOND_GROWN_FAMILY_COMPLEX_QUICK.py`](/Users/jonreilly/Projects/Physics/scripts/SECOND_GROWN_FAMILY_COMPLEX_QUICK.py)
- [`logs/2026-04-06-second-grown-family-complex-quick.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-second-grown-family-complex-quick.txt)
- [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)

## Question

Does the second grown-family complex-action companion stay retained when we tighten the window to a single seed and the immediately nearby drifts?

This probe intentionally tightened the scan:

- family: no-restore grown geometry + geometry-sector stencil
- seeds: `0`
- drifts: `0.18, 0.20, 0.22`
- guards: exact gamma=0 baseline, Born proxy where feasible, and `TOWARD -> AWAY` crossover

## Result

The tightened window keeps the linear/Born-like structure, but it loses the desired crossover:

- the anchor row still has a Born proxy at drift `0.20`
- weak-field `F~M` remains near `1.000`
- but the gravitational response is **AWAY** already at `gamma = 0`
- and it stays **AWAY** at `gamma = 0.1` and `gamma = 0.5`

Quick-row summary:

| drift | born | g0 | d01 | d05 | e01 | e05 | fm0 | fm05 | t01 | t05 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.18` | n/a | `-5.498e-03` | `-1.080e-02` | `-3.110e-02` | `1.079` | `0.301` | `1.000` | `1.000` | `0` | `0` |
| `0.20` | `2.299e-16` | `-1.134e-02` | `-1.577e-02` | `-3.350e-02` | `1.073` | `0.307` | `1.000` | `1.000` | `0` | `0` |
| `0.22` | n/a | `-2.214e-02` | `-3.080e-02` | `-6.687e-02` | `1.088` | `0.313` | `1.000` | `1.000` | `0` | `0` |

## Safe Read

The narrow review-safe statement is:

- the second grown-family candidate does not retain the complex-action crossover cleanly in this tighter single-seed window
- the failure is not a Born collapse or weak-field scaling failure
- it is a **response-sign / crossover boundary**: the response stays on the AWAY side even at `gamma = 0`
- that means the earlier positive is a tiny retained basin, not a broad basin

## Final Verdict

**diagnosed boundary**
