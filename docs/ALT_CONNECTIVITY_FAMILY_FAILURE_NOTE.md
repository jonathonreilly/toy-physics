# ALT Connectivity Family Failure Note

**Date:** 2026-04-06  
**Status:** diagnosed failure boundary for the alternative connectivity family

## Artifact Chain

- [`scripts/ALT_CONNECTIVITY_FAMILY_FAILURE_AUDIT.py`](/Users/jonreilly/Projects/Physics/scripts/ALT_CONNECTIVITY_FAMILY_FAILURE_AUDIT.py)
- [`logs/2026-04-06-alt-connectivity-family-failure-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-alt-connectivity-family-failure-audit.txt)
- [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)
- [`docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md)

## Question

Why do some rows in the alternative connectivity basin fail if the zero and
neutral controls are exact?

## Result

The misses are a **pure sign-orientation boundary**.

Summary of the audit:

- zero-control leakage: `0`
- neutral-cancellation leakage: `0`
- sign-orientation failures: `13`
- scaling failures: `0`

Representative failing rows all have the same pattern:

- `zero = 0`
- `neutral = 0`
- `plus < 0`
- `minus > 0`
- exponent stays `~1.000`

So the failure is not a control artifact and not a weak-scaling artifact.
The family simply flips the sign on a subset of seeds/drifts.

## Safe Read

This is an honest diagnosed boundary:

- the alternative structured connectivity family is a real bounded positive
  basin overall
- the surviving basin is seed- and drift-selective
- the misses are explained by orientation reversal, not by hidden leakage

## Conclusion

The old sector-style lesson does generalize to a new structured connectivity
family, but the family is not uniformly sign-stable across all tested seeds.
The failure mode is now mechanistically understood.
