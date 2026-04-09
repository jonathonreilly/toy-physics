# Fourth Family Quadrant Note

**Date:** 2026-04-06  
**Status:** retained narrow signed-source basin on the quadrant-reflection family

## Artifact Chain

- [`scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py)
- [`logs/2026-04-06-fourth-family-quadrant.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fourth-family-quadrant.txt)

## Question

Can a quadrant-reflection connectivity rule on the grown slice preserve the
signed-source response in a retained way, while remaining distinct from the
original grown family, the second grown family, and the alt connectivity
family?

## Result

The quick diagnostic sweep gives a **real but narrow basin**, not a family-wide
closure.

Controls are clean:

- exact zero-source baseline passes
- exact neutral `+1/-1` cancellation passes
- sign orientation is correct on the passing rows
- weak charge scaling stays near linear

Quick sweep summary:

- tested drifts: `0.0, 0.2, 0.5`
- tested seeds: `0, 1, 2`
- passing rows: `5/9`

Representative rows:

- `drift = 0.0`: all three seeds pass cleanly
- `drift = 0.2`: mixed sign orientation, so the basin is already narrow here
- `drift = 0.5`: mostly passes, but still seed-selective

## Safe Read

This is a distinct structured connectivity family, and it is not just a minor
retune of the earlier lanes.

What we have now is:

- a fourth-family narrow signed-source basin
- exact zero and neutral controls preserved
- near-linear charge scaling on the passing rows

What we do **not** have:

- family-wide closure
- seed-universal retention
- any basis to claim geometry-generic behavior

## Conclusion

The quadrant-reflection family is a genuine new retained basin, but it is
clearly narrow. The family space is still producing fresh structure, yet the
basin shape says we should keep treating these as selectivity-dominated
families rather than universal ones.
