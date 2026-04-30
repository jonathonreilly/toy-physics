# Fourth Family Complex Boundary Note

**Date:** 2026-04-06  
**Status:** support - structural or confirmatory support note

## Artifact Chain

- [`scripts/FOURTH_FAMILY_COMPLEX.py`](/Users/jonreilly/Projects/Physics/scripts/FOURTH_FAMILY_COMPLEX.py)
- [`logs/2026-04-06-fourth-family-complex.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fourth-family-complex.txt)

## Question

Does the retained fourth-family quadrant basin also carry a narrow complex-action
companion on the same grown slice?

## Result

The answer is **no, not cleanly**.

The anchor row at `drift = 0.20` retains the exact `gamma = 0` baseline and the
Born proxy is machine-clean on the tested row:

- anchor Born proxy: `1.247e-16`
- anchor `gamma = 0` centroid shift: `+1.406257e-06`

But the complex-action signature does **not** produce a retained
`TOWARD -> AWAY` crossover on this family:

- `drift = 0.00`: all tested rows stay `AWAY`
- `drift = 0.20`: mixed sign orientation, with `t01 = 2` and `t05 = 1`
- `drift = 0.50`: all tested rows stay `TOWARD`

That means the complex response is not organized as a clean retained basin on
this family. The gamma response is present, but it is not the same directional
companion we retained on the second-family complex lane.

## Safe Read

What survives:

- exact `gamma = 0` baseline on the anchor row
- Born proxy on the anchor row
- near-linear weak-field transfer on the tested rows

What does **not** survive:

- a clean anchor-row `TOWARD -> AWAY` crossover
- a seed-robust complex-action companion
- any broad family-level complex-action claim

## Conclusion

The fourth-family quadrant basin is a real signed-source basin, but it does not
retain the complex-action companion cleanly. The structural miss is not control
leakage; it is that the quadrant-reflection connectivity does not furnish the
same directional crossover channel that the second-family complex basin had.

That leaves the fourth family as a signed-source basin only, with the complex
lane diagnosed as a boundary failure.
