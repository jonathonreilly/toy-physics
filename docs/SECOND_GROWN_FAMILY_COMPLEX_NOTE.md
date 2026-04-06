# Second Grown Family Complex Note

**Date:** 2026-04-06  
**Status:** retained narrow anchor-row positive on the no-restore geometry-sector slice

## Artifact chain

- [`scripts/SECOND_GROWN_FAMILY_COMPLEX.py`](/Users/jonreilly/Projects/Physics/scripts/SECOND_GROWN_FAMILY_COMPLEX.py)
- [`logs/2026-04-06-second-grown-family-complex.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-second-grown-family-complex.txt)
- [`docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md)

## Question

Does the best second grown family candidate also carry the complex-action companion in a narrow retained sense?

This probe was intentionally strict:

- family: no-restore Gate B grown geometry
- connectivity: geometry-sector stencil
- controls: exact gamma=0 baseline on the anchor row, Born proxy where feasible, and a `TOWARD -> AWAY` crossover check
- weak-field check: `F~M` near 1 on the tested rows

## Result

The probe passed the retained safety gates on the anchor row and showed the expected narrow crossover pattern:

- anchor row retained `gamma=0` baseline
- Born proxy was machine-clean where measured
- `TOWARD -> AWAY` crossover survived on the tested rows
- weak-field `F~M` stayed at `1.000`

Row summary:

| drift | born | g0 | d01 | d02 | d05 | e01 | e05 | fm0 | fm05 | t01 | t05 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.15` | n/a | `+8.578e-03` | `-1.645e-03` | `-1.194e-02` | `-4.350e-02` | `1.108` | `0.322` | `1.000` | `1.000` | `1` | `0` |
| `0.20` | `2.299e-16` | `+6.562e-03` | `+3.425e-04` | `-5.489e-03` | `-2.122e-02` | `1.101` | `0.316` | `1.000` | `1.000` | `1` | `0` |
| `0.25` | n/a | `-1.766e-04` | `-2.031e-02` | `-3.967e-02` | `-9.396e-02` | `1.106` | `0.331` | `1.000` | `1.000` | `1` | `0` |

## Safe Read

The narrow review-safe statement is:

- the retained anchor row does carry the complex-action companion
- the support is selective, not family-wide
- the geometry-sector / no-restore slice is distinct from the earlier retained drift/restore neighborhood
- the retention is real but narrow, so this is not a generalized grown-family claim

## Final Verdict

**retained narrow anchor-row positive**
