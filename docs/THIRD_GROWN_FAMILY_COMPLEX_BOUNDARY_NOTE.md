# Third Grown Family Complex Boundary Note

**Date:** 2026-04-06  
**Status:** diagnosed boundary for the third grown-family complex-action probe

## Artifact chain

- [`scripts/THIRD_GROWN_FAMILY_COMPLEX.py`](/Users/jonreilly/Projects/Physics/scripts/THIRD_GROWN_FAMILY_COMPLEX.py)
- [`logs/2026-04-06-third-grown-family-complex.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-third-grown-family-complex.txt)
- [`docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md)

## Question

Does the retained third grown-family signed basin also carry a narrow
complex-action companion, with an exact `gamma = 0` baseline and a clean
`TOWARD -> AWAY` crossover?

The probe was intentionally strict:

- geometry: the retained no-restore third-family grown slice
- connectivity: the cross-quadrant load-balanced rule from the signed basin
- controls: exact `gamma = 0` baseline, exact zero-source reference, and weak
  `F~M` sanity
- crossover test: `gamma = 0.1` versus `gamma = 0.5`

## Result

The complex branch does **not** retain a clean narrow companion.

What survives:

- exact `gamma = 0` reduction on representative rows
- Born proxy remains machine-clean on the representative seed-0 rows
- weak-field `F~M` remains essentially linear where measured

What does not survive:

- a seed-consistent `TOWARD -> AWAY` crossover across the retained interior
  drift window
- a family-wide or even basin-wide complex-action companion

Representative rows:

| drift | seed | born | d0 | d0.1 | d0.5 | esc@0.5 | F~M@0 | F~M@0.5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.1` | `0` | `5.73e-17` | `-8.40e-03` | `-1.19e-02` | `-2.59e-02` | `0.876` | `1.000` | `0.999` |
| `0.1` | `1` | n/a | `-1.36e-03` | `-5.22e-03` | `-1.94e-02` | `0.838` | `1.000` | `0.999` |
| `0.1` | `2` | n/a | `-2.29e-02` | `-2.49e-02` | `-3.25e-02` | `0.949` | `1.000` | `1.000` |
| `0.2` | `0` | `2.68e-16` | `+3.71e-03` | `+3.02e-03` | `+3.91e-04` | `0.867` | `1.000` | `1.000` |
| `0.2` | `1` | n/a | `+3.56e-03` | `+1.99e-03` | `-4.00e-03` | `0.872` | `1.000` | `1.000` |
| `0.2` | `2` | n/a | `-1.31e-02` | `-1.38e-02` | `-1.68e-02` | `0.885` | `1.000` | `1.000` |
| `0.3` | `0` | `5.73e-17` | `-8.40e-03` | `-1.19e-02` | `-2.59e-02` | `0.876` | `1.000` | `0.999` |
| `0.3` | `1` | n/a | `-1.36e-03` | `-5.22e-03` | `-1.94e-02` | `0.838` | `1.000` | `0.999` |
| `0.3` | `2` | n/a | `-1.85e-03` | `-2.07e-03` | `-2.95e-03` | `0.837` | `1.000` | `1.000` |

## Safe Read

The right interpretation is a structural boundary, not a retained companion:

- the third-family sign basin is real
- the complex-action branch is seed-selective and drift-sensitive
- the exact `gamma = 0` baseline is fine, but the crossover is not robust

## Conclusion

**diagnosed boundary for the third grown-family complex-action companion**
