# Sign Portability Invariant Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow comparison positive

## Artifact Chain

- [`scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py)
- [`logs/2026-04-06-sign-portability-invariant.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-sign-portability-invariant.txt)
- retained family notes: [`docs/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWN_TRANSFER_BASIN_NOTE.md), [`docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md), [`docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md), [`docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md), [`docs/FOURTH_FAMILY_QUADRANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_QUADRANT_NOTE.md)
- holdout confirmation: [`docs/FIFTH_FAMILY_RADIAL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_NOTE.md), [`docs/FIFTH_FAMILY_RADIAL_FM_TRANSFER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_FM_TRANSFER_NOTE.md), [`docs/FIFTH_FAMILY_RADIAL_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_RADIAL_BOUNDARY_NOTE.md)

## Question

What is the smallest invariant that explains why signed-source transfer now
survives across the retained structured families?

## Comparison

| family | exact controls | sign orientation | weak-field response | basin shape |
| --- | --- | --- | --- | --- |
| Grown transfer basin | exact zero-source and neutral same-point cancellation | retained on nearby rows | `F~M = 1.000` | narrow and selective |
| Alternative connectivity family | exact zero-source and neutral same-point cancellation | retained on passing rows | `F~M = 0.999994` | bounded but broadest of the retained sign-law families |
| Second grown-family sign | exact zero-source and neutral same-point cancellation | retained on all tested rows | mean exponent `1.000072` | independent basin, still narrow in architecture space |
| Third grown-family sign | exact zero-source and neutral same-point cancellation | retained on passing rows | mean exponent `0.999842` | bounded drift basin |
| Fourth family quadrant | exact zero-source and neutral same-point cancellation | retained on passing rows; mixed at `drift=0.2` | alpha near `1.0` | narrow and seed-selective |

## Out-Of-Band Confirmation

The later fifth-family radial holdout agrees on the same control surface:

| family | exact controls | sign orientation | weak-field response | basin shape |
| --- | --- | --- | --- | --- |
| Fifth family radial | exact zero-source and neutral same-point cancellation | retained on sampled rows; flips at the interior boundary | mean exponent `0.999439` | narrow holdout confirmation |

## Safe Read

Across the retained sign-law basins, the thing that survives is not the
geometry family itself.

What survives is the signed-control fixed point:

- exact zero-source cancellation
- exact neutral same-point cancellation
- plus/minus antisymmetry
- weak-field response pinned near unit slope

The family construction only changes basin width and selectivity.
Some families are broad, some are narrow, and some are seed-selective, but the
sign-law fixed point remains the same.

## Exact Mismatch

- basin width is not invariant
- seed selectivity is not invariant
- complex-action selectivity is not part of this invariant
- the `gamma = 0` branch analog is not the same control surface as the
  zero-source signed branch

## Final Verdict

**retained narrow comparison positive: signed-source transfer is portable
across the retained structured families, with the signed-control fixed point as
the order parameter and basin width as the family-dependent variable**
